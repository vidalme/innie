"""Interface pública dos scripts. Veja docs/scripts.md."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from . import __version__
from .model import PDIError, SCHEMA, cycle, find, new_id, now, validate, window
from .operations import (apply_proposal, backup, close_cycle, connect, create_cycle, doctor, import_source,
                         check_connection, init_git, prepare_proposal, restore, start_cycle, verify_archive)
from .storage import Store, read_json, write_json
from .views import export_pdi, overview, render

INNIE = Path(__file__).resolve().parents[2]

def parser():
    p = argparse.ArgumentParser(description="Innie/Outtie — ferramentas locais de acompanhamento do PDI")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--outtie", help="Espaço individual; por padrão usa pessoal/configuração local")
    commands = p.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("setup", help="Preparar/conectar espaço individual")
    setup.add_argument("--two-roots", action=argparse.BooleanOptionalAction, default=True,
                       help="Abrir innie e outtie no workspace local (padrão)")
    conn = commands.add_parser("connect", help="Conectar espaço existente")
    conn.add_argument("--switch", action="store_true")
    conn.add_argument("--two-roots", action=argparse.BooleanOptionalAction, default=True,
                      help="Abrir innie e outtie no workspace local (padrão)")
    commands.add_parser("doctor", help="Conferir arquivos e dependências; Copilot exige teste manual")
    commands.add_parser("state", help="Imprimir estado canônico atual")
    commands.add_parser("validate", help="Validar estado atual")
    criteria = commands.add_parser("criteria", help="Listar critérios aplicáveis; não decide elegibilidade")
    criteria.add_argument("--type", choices=["horizontal", "vertical", "bonus"], default="horizontal")
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

def resolve(args):
    if args.outtie:
        return Store(args.outtie)
    if (INNIE / "pessoal").is_symlink():
        return Store((INNIE / "pessoal").resolve())
    config = INNIE / ".local/config.json"
    if config.exists():
        return Store(read_json(config)["outtie"])
    return Store(INNIE.parent / "outtie")

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
    store = resolve(args)
    if args.command == "setup":
        check_connection(INNIE, store.root)
        created = store.initialize()
        return {"initialized": created, **connect(INNIE, store.root, two_roots=args.two_roots)}
    if args.command == "connect": return connect(INNIE, store.root, args.switch, args.two_roots)
    if args.command == "init-git": return init_git(store if args.scope == "outtie" else INNIE)
    if args.command == "doctor": return doctor(INNIE, store)
    if args.command == "state": return store.load()
    if args.command == "validate":
        state = store.load(); return {"valid": True, "revision": state["revision"]}
    if args.command == "criteria":
        state = store.load(); area = str(state["profile"].get("area", "")).casefold()
        catalog = read_json(INNIE / "knowledge/criteria/catalog.json")
        records = [{**c, "classification": c["types"][args.type]} for c in catalog["criteria"]
                   if c["scope"] == "all" or area in {c["scope"].casefold(), "operacao"} and c["scope"] == "Operação"]
        return {"type": args.type, "policy_confirmation": catalog["cycle_validity"], "criteria": records,
                "minimum_interval_between_promotions": "not_confirmed", "official_eligibility": "not_determined"}
    if args.command == "migrate":
        state = store.load(); return {"schema_version": state["schema_version"], "migration": "not_required", "unknown_schemas": "not_modified"}
    if args.command == "import": return import_source(store, args.file, args.kind, args.title)
    if args.command == "proposal": return prepare_proposal(store, read_json(args.changes), args.reason)
    if args.command == "apply": return apply_proposal(store, args.proposal, args.approve)
    if args.command == "render": return render(store, args.cycle, args.preserve_edits)
    if args.command == "status": return overview(store.load(), args.cycle, args.on)
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
        result = run(parser().parse_args(argv))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if result.get("ok", True) else 1
    except (PDIError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc), "state_not_silently_replaced": True}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
