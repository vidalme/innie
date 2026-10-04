"""Visões Markdown regeneráveis e exportação revisável para Team Guide."""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

from .model import PDIError, cycle, date, find, new_id
from .storage import atomic, digest, inside, read_json, write_json

DEFAULT_TIMEZONE = "America/Fortaleza"

def escaped(value):
    return str(value if value is not None else "Não informado").replace("|", "\\|").replace("\n", " ")

def today(state):
    return dt.datetime.now(ZoneInfo(state["profile"].get("timezone") or DEFAULT_TIMEZONE)).date()

def overview(state, cycle_id=None, on=None):
    c = cycle(state, cycle_id)
    reference = date(on) if on else today(state)
    actions = c["actions"]
    due = [a for a in actions if a.get("due_on") and date(a["due_on"]) <= reference and a["status"] not in {"cancelled", "suspended", "carried_over", "proposed"}]
    late = [a["id"] for a in due if a["status"] != "done"]
    missing = [a["id"] for a in actions if a["status"] == "done" and not a.get("evidence_ids")]
    changes = [a["id"] for a in actions if a["status"] in {"cancelled", "suspended", "carried_over"}]
    remaining = (date(c["evidence_cutoff_on"]) - reference).days if c.get("evidence_cutoff_on") else None
    pending = [a for a in actions if a["status"] in {"planned", "in_progress"}]
    missing_effort = [a["id"] for a in pending if a.get("effort_hours") is None]
    known_effort = sum(a["effort_hours"] for a in pending if a.get("effort_hours") is not None)
    effort = None if missing_effort else known_effort
    capacity = state["profile"].get("weekly_capacity_hours")
    available = max(remaining, 0) / 7 * capacity * .8 if remaining is not None and capacity is not None else None
    over_capacity = None
    if available is not None:
        if known_effort > available:
            over_capacity = True
        elif not missing_effort:
            over_capacity = False
    return {"cycle_id": c["id"], "revision": state["revision"], "status": c["status"], "reference_on": reference.isoformat(),
            "reference_timezone": (state["profile"].get("timezone") or DEFAULT_TIMEZONE) if on is None else None,
            "reference_timezone_assumed": on is None and state["profile"].get("timezone") is None,
            "days_to_cutoff": remaining, "late_actions": late, "done_without_evidence": missing,
            "changed_commitments": changes, "due_actions": len(due), "due_done": sum(a["status"] == "done" for a in due),
            "operational_completion_percent": round(100 * sum(a["status"] == "done" for a in due) / len(due), 1) if due else None,
            "official_pdi_compliance": "not_determined", "estimated_remaining_effort_hours": effort,
            "known_remaining_effort_hours": known_effort, "actions_missing_effort": missing_effort,
            "suggested_available_hours_with_20pct_margin": available,
            "over_capacity": over_capacity,
            "promotion_probability": "not_calculated", "interval_since_promotion_rule": "requires_institutional_confirmation"}

def write_view(store, relative, text, preserve_edits=False):
    path = inside(store.root, store.root / relative)
    indexpath = inside(store.root, store.root / ".runtime/views.json")
    index = read_json(indexpath) if indexpath.exists() else {}
    if path.exists() and (relative not in index or digest(path) != index[relative]):
        if not preserve_edits:
            raise PDIError(f"Edição manual ou arquivo não gerado em {relative}. Use --preserve-edits para guardá-lo na inbox antes de regenerar.")
        saved = inside(store.root, store.root / f"inbox/{new_id('manual')}--{path.name}")
        atomic(saved, path.read_bytes())
    atomic(path, text.encode("utf-8"))
    index[relative] = digest(path)
    write_json(indexpath, index)
    return str(path)

def render(store, cycle_id=None, preserve_edits=False):
    with store.lock():
        state = store.load(); c = cycle(state, cycle_id)
        if c["status"] == "archived":
            raise PDIError("Leia as saídas congeladas no archive; não regenerar o ciclo encerrado.")
        report = overview(state, c["id"])
        header = f"> Gerado da revisão {state['revision']}. Edite o estado por proposta, não este arquivo.\n\n"
        title = f"# {c['label']}\n\n" + header
        plan = title + f"Início: {c.get('starts_on') or 'pendente'} • fim: {c.get('ends_on') or 'pendente'} • corte: {c.get('evidence_cutoff_on') or 'pendente'}\n\n"
        plan += f"Fechamento do PDI: {c.get('pdi_closes_on') or 'pendente'} • avaliação: {c.get('evaluation_on') or 'pendente'}\n\n"
        plan += "## Objetivos\n\n"
        for obj in c["objectives"]:
            plan += f"- **{obj.get('title', obj['id'])}** — {obj.get('description', '')}\n"
        if not c["objectives"]: plan += "Ainda sem objetivos revisados.\n"
        plan += "\n## Ações\n\n| ID | Título | Estado | Prazo | Esforço restante | Evidências |\n| --- | --- | --- | --- | --- | --- |\n"
        for a in sorted(c["actions"], key=lambda x: x.get("due_on") or "9999"):
            effort_text = f"{a['effort_hours']} h" if a.get('effort_hours') is not None else "pendente"
            plan += f"| {a['id']} | {escaped(a['title'])} | {a['status']} | {a.get('due_on') or 'pendente'} | {effort_text} | {', '.join(a.get('evidence_ids', [])) or 'pendentes'} |\n"
        plan += "\n## Marcos\n\n"
        for milestone in c.get("milestones", []):
            plan += f"- {milestone['on']}: {milestone.get('label', 'Revisão')}\n"
        if not c.get("milestones"): plan += "Informe marcos oficiais ou revise uma proposta de cronograma.\n"
        plan += "\n## Critérios\n\n| ID | Critério | Situação | Evidências |\n| --- | --- | --- | --- |\n"
        for row in c["criterion_assessments"]:
            plan += f"| {row['id']} | {escaped(row.get('criterion_id'))} | {row['status']} | {', '.join(row.get('evidence_ids', [])) or 'pendentes'} |\n"
        dashboard = title + "## Próximos passos\n\n"
        for a in sorted([x for x in c["actions"] if x["status"] in {"planned", "in_progress"}], key=lambda x:x.get("due_on") or "9999")[:5]:
            dashboard += f"- {a['title']} — {a.get('due_on') or 'prazo pendente'} ({a['id']}).\n"
        if not c["actions"]: dashboard += "- Converse com o assistente para importar ou construir seu plano.\n"
        dashboard += "\n## Pendências e indicadores\n\n"
        dashboard += f"- Data de referência: {report['reference_on']} ({report['reference_timezone']}).\n"
        if report['reference_timezone_assumed']:
            dashboard += "- Fuso horário provisório do piloto; confirme seu fuso no perfil.\n"
        dashboard += f"- Dias até o corte: {report['days_to_cutoff'] if report['days_to_cutoff'] is not None else 'calendário pendente'}.\n"
        dashboard += f"- Ações em atraso: {', '.join(report['late_actions']) or 'nenhuma identificada'}.\n"
        dashboard += f"- Realizadas sem evidência: {', '.join(report['done_without_evidence']) or 'nenhuma identificada'}.\n"
        dashboard += f"- Canceladas, suspensas ou transferidas: {', '.join(report['changed_commitments']) or 'nenhuma'}; revisar efeito institucional.\n"
        if report['actions_missing_effort']:
            dashboard += f"- Esforço restante total: pendente; soma das estimativas informadas: {report['known_remaining_effort_hours']} horas.\n"
            dashboard += f"- Ações sem estimativa de esforço: {', '.join(report['actions_missing_effort'])}.\n"
        else:
            dashboard += f"- Esforço restante estimado: {report['estimated_remaining_effort_hours']} horas.\n"
        capacity_text = {True: 'sim', False: 'não', None: 'a avaliar; esforço, capacidade ou calendário pendente'}[report['over_capacity']]
        dashboard += f"- Possível sobrecarga: {capacity_text}.\n"
        dashboard += f"- Cumprimento operacional: {report['operational_completion_percent'] if report['operational_completion_percent'] is not None else 'não aplicável'}%; não equivale a CI-05 oficial.\n"
        dashboard += "- Elegibilidade, 9box e eventual intervalo mínimo entre promoções: confirmar com liderança/RH.\n"
        dashboard += "\n## P2P e entrega parcial\n\nRevise prioridades, capacidade, atrasos, qualidade das evidências e critérios desconhecidos. Solicite /pdi-p2p ou /pdi-marco ao Copiloto.\n"
        root = f"cycles/{c['id']}/outputs"
        paths = [write_view(store, root + "/plano.md", plan, preserve_edits), write_view(store, root + "/painel.md", dashboard, preserve_edits)]
        # Cópias estruturadas também são visões, não segunda fonte de verdade.
        write_view(store, root + "/estado.json", __import__('json').dumps(c, ensure_ascii=False, indent=2)+"\n", preserve_edits)
    return {"revision": state["revision"], "files": paths}

def export_pdi(store, action_id, cycle_id=None, maximum=16000, preserve_edits=False):
    if maximum < 1: raise PDIError("Limite inválido.")
    with store.lock():
        state = store.load(); c = cycle(state, cycle_id)
        if c["status"] == "archived":
            archive = inside(store.root, store.root / c["archive_path"])
            c = read_json(archive / "cycle.json")
            evidence = read_json(archive / "evidence.json")
        else:
            evidence = state["evidence"]
        action = find(c["actions"], action_id, "Ação")
        title = action["title"]
        body = action.get("pdi_description")
        if body is None:
            body = action.get("description") or ""
            if action.get("due_on"): body += f"\n\nPrazo planejado: {action['due_on']}."
            if action["status"] == "done":
                body += f"\n\nSituação: realização informada; data: {action.get('completed_on') or 'a confirmar'}."
                if action.get("result"): body += "\n\nResultado registrado: " + action["result"]
            else: body += "\n\nSituação: ação ainda não concluída."
            if action.get("evidence_ids"):
                body += "\n\nEvidências:\n"
                for eid in action["evidence_ids"]:
                    ev = find(evidence, eid, "Evidência")
                    body += f"- {ev.get('title', eid)}: {ev.get('url') or ev.get('local_path') or 'localização pendente'} ({ev.get('verification', 'claimed')}).\n"
        utf16 = len(body.encode("utf-16-le")) // 2
        if utf16 > maximum:
            raise PDIError(f"Descrição excede o limite: {utf16} unidades UTF-16, máximo {maximum}. Revise sem cortar evidências silenciosamente.")
        root = f"exports/{c['id']}/{action_id}-r{state['revision']}"
        path = write_view(store, root + ".md", f"# {title}\n\n{body.strip()}\n", preserve_edits)
        meta = {"cycle_id": c["id"], "action_id": action_id, "revision": state["revision"], "title": title,
                "description": body.strip(), "characters": len(body), "utf16_units": utf16,
                "external_registration": "not_confirmed", "review_required": True}
        write_view(store, root + ".json", __import__('json').dumps(meta, ensure_ascii=False, indent=2)+"\n", preserve_edits)
    return {"file": path, "characters": len(body), "utf16_units": utf16, "external_registration": "not_confirmed"}
