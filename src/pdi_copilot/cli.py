"""Interface pública dos scripts. Veja docs/scripts.md."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

from . import __version__
from .model import PDIError, SCHEMA, cycle, find, new_id, now, validate, window
from .operations import (apply_proposal, backup, close_cycle, connect, create_cycle, doctor, import_source,
                         check_connection, check_environment, init_git, policy_alignment, prepare_proposal, restore, start_cycle, verify_archive)
from .storage import Store, read_json, write_json
from .views import export_pdi, render
from .journey import guidance, guidance_text, status_report

INNIE = Path(__file__).resolve().parents[2]

def parser():
    p = argparse.ArgumentParser(description="Innie/Outtie — ferramentas locais de acompanhamento do PDI")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--outtie", help="Espaço individual; por padrão usa pessoal/configuração local")
    commands = p.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("setup", help="Criar espaço individual ou preparar o já conectado")
    setup.add_argument("--format", choices=["json", "text"], default="json", help="Formato da orientação de preparação")
    setup.add_argument("--two-roots", action=argparse.BooleanOptionalAction, default=True,
                       help="Abrir innie e outtie no workspace local (padrão)")
    conn = commands.add_parser("connect", help="Conectar espaço existente")
    conn.add_argument("--format", choices=["json", "text"], default="json", help="Formato da orientação de preparação")
    conn.add_argument("--switch", action="store_true")
    conn.add_argument("--two-roots", action=argparse.BooleanOptionalAction, default=True,
                      help="Abrir innie e outtie no workspace local (padrão)")
    commands.add_parser("doctor", help="Conferir arquivos e dependências; Copilot exige teste manual")
    commands.add_parser("state", help="Imprimir estado canônico atual")
    onboarding = commands.add_parser("onboarding", help="Orientar início/retomada a partir do estado e de propostas pendentes")
    onboarding.add_argument("--cycle")
    onboarding.add_argument("--format", choices=["json", "text"], default="json")
    commands.add_parser("validate", help="Validar estado atual")
    criteria = commands.add_parser("criteria", help="Listar critérios aplicáveis; não decide elegibilidade")
    criteria.add_argument("--type", choices=["horizontal", "vertical", "bonus"], default="horizontal")
    criteria.add_argument("--cycle", help="Ciclo cuja versão institucional será conferida")
    git = commands.add_parser("init-git", help="Inicializar Git local; sem remote/push")
    git.add_argument("--scope", choices=["outtie", "innie"], default="outtie")
    imp = commands.add_parser("import", help="Preservar arquivo e extrair texto quando possível")
    imp.add_argument("file"); imp.add_argument("--kind", choices=["personal", "institutional", "mixed", "example"], default="personal")
    imp.add_argument("--title")
    prop = commands.add_parser("proposal", help="Criar proposta de operações documentadas")
    prop.add_argument("--changes", required=True); prop.add_argument("--reason", required=True)
    app = commands.add_parser("apply", help="Aplicar proposta revisada")
    app.add_argument("--proposal", required=True); app.add_argument("--approve", action="store_true")
    ren = commands.add_parser("render", help="Regenerar plano/painel")
    ren.add_argument("--cycle"); ren.add_argument("--preserve-edits", action="store_true")
    status = commands.add_parser("status", help="Indicadores operacionais, sem prever promoção")
    status.add_argument("--cycle"); status.add_argument("--on")
    status.add_argument("--format", choices=["json", "text"], default="json")
    exp = commands.add_parser("export", help="Exportar uma ação para revisão/cópia")
    exp.add_argument("action_id"); exp.add_argument("--cycle"); exp.add_argument("--max-chars", type=int, default=16000)
    exp.add_argument("--preserve-edits", action="store_true")
    b = commands.add_parser("backup", help="Criar backup verificado fora do espaço")
    b.add_argument("--destination", required=True)
    r = commands.add_parser("restore", help="Restaurar backup em pasta nova")
    r.add_argument("backup_file"); r.add_argument("--destination", required=True)
    commands.add_parser("migrate", help="Validar versão atual; versão desconhecida preservada")
    win = commands.add_parser("window", help="Calcular janela inclusiva, com limites pendentes")
    win.add_argument("--event", required=True); win.add_argument("--cutoff", required=True)
    win.add_argument("--months", required=True, type=int); win.add_argument("--boundary-confirmed", action="store_true")
    cyc = commands.add_parser("cycle", help="Administrar ciclos")
    sub = cyc.add_subparsers(dest="cycle_command", required=True)
    cr = sub.add_parser("create"); cr.add_argument("id"); cr.add_argument("--label", required=True)
    cr.add_argument("--start"); cr.add_argument("--end"); cr.add_argument("--cutoff"); cr.add_argument("--evaluation")
    st = sub.add_parser("start"); st.add_argument("id"); st.add_argument("--reviewed", action="store_true")
    cl = sub.add_parser("close"); cl.add_argument("id"); cl.add_argument("--approve", action="store_true")
    ve = sub.add_parser("verify"); ve.add_argument("archive")
    co = sub.add_parser("carry"); co.add_argument("--from", dest="from_cycle", required=True)
    co.add_argument("--to", dest="to_cycle", required=True); co.add_argument("--action", required=True)
    co.add_argument("--due", required=True); co.add_argument("--approve", action="store_true")
    ad = sub.add_parser("adendum"); ad.add_argument("id"); ad.add_argument("--file", required=True)
    ad.add_argument("--reason", required=True); ad.add_argument("--approve", action="store_true")
    return p

def connected_outtie():
    """Recuperar somente o vínculo local, sem assumir a pasta irmã."""
    if (INNIE / "pessoal").is_symlink():
        return (INNIE / "pessoal").resolve()
    config = INNIE / ".local/config.json"
    if config.exists():
        return Path(read_json(config)["outtie"]).expanduser().resolve()
    return None

def existing_space_error(root):
    command = shlex.join(["python3", "scripts/pdi.py", "--outtie", str(root), "connect"])
    return PDIError(
        f"Espaço individual existente sem vínculo com esta instalação: {root}. "
        f"Para usar esse espaço, confira o destino e execute: {command}. "
        "Para criar outro, use python3 scripts/pdi.py --outtie NOVO_CAMINHO setup."
    )

def resolve(args):
    if args.outtie:
        return Store(args.outtie)
    connected = connected_outtie()
    if connected is not None:
        return Store(connected)
    store = Store(INNIE.parent / "outtie")
    if (store.root / "metadata.json").exists():
        raise existing_space_error(store.root)
    return store

def preparation_result(store, paths, environment, initialized=None):
    state = store.load()
    open_command = shlex.join(["code", paths['workspace']])
    open_step = (f"Abra o workspace: {open_command}" if environment['optional_tools']['code'] else
                 f"No VS Code, use Arquivo > Abrir Workspace e escolha: {paths['workspace']}")
    cli = ["python3", str(INNIE / "scripts/pdi.py")]
    result = {**paths, "local_ready": True, "environment": environment,
              "copilot_context": "manual_check_required",
              "context_to_verify": {"revision": state['revision'], "active_cycle": state['active_cycle']},
              "next_steps": [
                  "Confira o ambiente: " + shlex.join([*cli, 'doctor']),
                  open_step,
                  "No chat do Copilot, autentique sua conta e selecione o agente copiloto-desenvolvimento.",
                  "Peça: Leia minha revisão atual, informe o ciclo ativo e não modifique nada. "
                  "Compare a resposta com: " + shlex.join([*cli, 'state']),
                  "Depois da conferência, use /pdi-iniciar ou escreva Quero começar; diga se já tem PDI ou rascunho."]}
    if initialized is not None:
        result['initialized'] = initialized
    return result

def preparation_text(result):
    if result.get('initialized') is True:
        space = "Espaço individual criado."
    elif result.get('initialized') is False:
        space = "Espaço individual já conectado."
    else:
        space = "Espaço individual conectado."
    lines = ["Preparação local concluída.", space,
             f"Seus dados: {result['outtie']}", f"Workspace: {result['workspace']}",
             "Python e Git verificados."]
    if not result['environment']['optional_tools']['pdftotext']:
        lines.append("Extração de texto de PDF indisponível; você pode começar com texto ou leitura manual.")
    context = result['context_to_verify']
    lines.extend([f"Contexto a conferir: revisão {context['revision']}; ciclo ativo: {context['active_cycle'] or 'nenhum'}.",
                  "A integração com o assistente aguarda verificação no editor.", "", "Próximos passos:"])
    lines.extend(f"{i}. {step}" for i, step in enumerate(result['next_steps'], 1))
    return '\n'.join(lines)

def carry(store, args):
    if not args.approve: raise PDIError("Revise a transferência e informe --approve.")
    with store.lock():
        state = store.load(); old = cycle(state, args.from_cycle); dest = cycle(state, args.to_cycle)
        if old["status"] != "archived" or dest["status"] == "archived":
            raise PDIError("Transferência exige origem encerrada e destino aberto.")
        action = find(old["actions"], args.action, "Ação")
        if action["status"] == "done": raise PDIError("Realização concluída não pode ser transferida como nova ação.")
        if any(a.get("carried_from") == {"cycle_id": old["id"], "action_id": action["id"]} for a in dest["actions"]):
            return {"carried": False, "reason": "already_transferred"}
        new = copy.deepcopy(action); new.update({"id": new_id("action"), "status": "planned", "due_on": args.due,
                    "completed_on": None, "evidence_ids": [], "objective_ids": [], "depends_on": [],
                    "carried_from": {"cycle_id": old["id"], "action_id": action["id"]}})
        for field in ("result", "pdi_description", "external_id", "external_registration"):
            new.pop(field, None)
        candidate = copy.deepcopy(state); cycle(candidate, dest["id"])["actions"].append(new)
        result = store.commit(candidate, state["revision"], f"Transferência revisada de {old['id']} para {dest['id']}")
    return {"carried": True, "action_id": new["id"], "revision": result["revision"], "previous_cycle_pending_status_preserved": True}

def adendum(store, args):
    if not args.approve: raise PDIError("Adendo exige revisão e --approve.")
    # Adendos ficam fora do archive e são registrados como fontes e propostas.
    state = store.load(); c = cycle(state, args.id)
    if c["status"] != "archived": raise PDIError("Adendo é destinado a ciclo encerrado.")
    imported = import_source(store, args.file)
    with store.lock():
        state = store.load(); candidate = copy.deepcopy(state); row = cycle(candidate, args.id)
        row.setdefault("adenda", []).append({"id": new_id("adendum"), "source_id": imported["id"], "reason": args.reason, "at": now()})
        result = store.commit(candidate, state["revision"], f"Adendo de {args.id}: {args.reason}")
    return {"revision": result["revision"], "archive_unchanged": True, "source_id": imported["id"]}

def run(args):
    if args.command == "window":
        return window(args.event, args.cutoff, args.months, args.boundary_confirmed)
    if args.command == "restore": return restore(args.backup_file, args.destination)
    if args.command == "init-git" and args.scope == "innie": return init_git(INNIE)
    environment = check_environment() if args.command in {"setup", "connect"} else None
    store = resolve(args)
    if args.command == "setup":
        check_connection(INNIE, store.root)
        if (store.root / "metadata.json").exists() and connected_outtie() != store.root:
            raise existing_space_error(store.root)
        created = store.initialize()
        paths = connect(INNIE, store.root, two_roots=args.two_roots)
        return preparation_result(store, paths, environment, created)
    if args.command == "connect":
        paths = connect(INNIE, store.root, args.switch, args.two_roots)
        return preparation_result(store, paths, environment)
    if args.command == "init-git": return init_git(store)
    if args.command == "doctor": return doctor(INNIE, store)
    if args.command == "state": return store.load()
    if args.command == "onboarding": return guidance(store, args.cycle)
    if args.command == "validate":
        state = store.load(); return {"valid": True, "revision": state["revision"]}
    if args.command == "criteria":
        state = store.load(); area = str(state["profile"].get("area", "")).casefold()
        selected = cycle(state, args.cycle) if args.cycle else (cycle(state) if state['active_cycle'] else None)
        alignment = policy_alignment(INNIE, selected)
        if not alignment['aligned']:
            raise PDIError(f"Versão institucional divergente: {alignment}. Revise a política do ciclo antes de usar os critérios atuais.")
        index = read_json(INNIE / "knowledge/index.json")
        catalog = read_json(INNIE / "knowledge" / index['criteria'])
        records = [{**c, "classification": c["types"][args.type]} for c in catalog["criteria"]
                   if c["scope"] == "all" or area in {c["scope"].casefold(), "operacao"} and c["scope"] == "Operação"]
        return {"type": args.type, "policy_confirmation": catalog["cycle_validity"], "criteria": records,
                "policy_alignment": alignment,
                "area_pending": state["profile"].get("area") is None,
                "minimum_interval_between_promotions": "not_confirmed", "official_eligibility": "not_determined"}
    if args.command == "migrate":
        state = store.load(); return {"schema_version": state["schema_version"], "migration": "not_required", "unknown_schemas": "not_modified"}
    if args.command == "import": return import_source(store, args.file, args.kind, args.title)
    if args.command == "proposal": return prepare_proposal(store, read_json(args.changes), args.reason)
    if args.command == "apply": return apply_proposal(store, args.proposal, args.approve)
    if args.command == "render": return render(store, args.cycle, args.preserve_edits)
    if args.command == "status": return status_report(store, args.cycle, args.on)
    if args.command == "export": return export_pdi(store, args.action_id, args.cycle, args.max_chars, args.preserve_edits)
    if args.command == "backup": return backup(store, args.destination)
    if args.command == "cycle":
        if args.cycle_command == "create": return create_cycle(store, args.id, args.label, args.start, args.end, args.cutoff, args.evaluation)
        if args.cycle_command == "start": return start_cycle(store, args.id, args.reviewed)
        if args.cycle_command == "close": return close_cycle(store, args.id, INNIE, args.approve)
        if args.cycle_command == "verify":
            from .storage import inside
            return verify_archive(inside(store.root / "archives", args.archive))
        if args.cycle_command == "carry": return carry(store, args)
        if args.cycle_command == "adendum": return adendum(store, args)
    raise PDIError("Comando não implementado.")

def main(argv=None):
    try:
        args = parser().parse_args(argv)
        result = run(args)
        if getattr(args, 'format', 'json') == 'text':
            print(guidance_text(result) if args.command in {'onboarding', 'status'} else preparation_text(result))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if result.get("ok", True) else 1
    except (PDIError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc), "state_not_silently_replaced": True}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
