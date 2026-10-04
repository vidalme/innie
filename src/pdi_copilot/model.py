"""Contratos, validação sem dependências e cálculos transparentes."""
from __future__ import annotations

import calendar
import copy
import datetime as dt
import re
import uuid
from zoneinfo import ZoneInfo

SCHEMA = 1
ACTION_STATUSES = {"proposed", "planned", "in_progress", "done", "suspended", "cancelled", "carried_over"}
CRITERION_STATUSES = {"not_applicable", "unknown", "pending", "supported", "confirmed", "expired"}
EVIDENCE_STATUSES = {"claimed", "inspected", "reviewed", "institutionally_confirmed"}
COLLECTIONS = {"objectives", "actions", "criterion_assessments", "competency_assessments", "metrics", "events"}
ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$")

class PDIError(Exception):
    """Erro esperado que pode ser apresentado ao usuário."""

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def new_id(prefix):
    return prefix + "-" + uuid.uuid4().hex[:12]

def valid_id(value):
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise PDIError(f"Identificador inválido: {value!r}. Use letras, números, hífen ou underscore.")
    return value

def date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise PDIError(f"Data inválida: {value!r}; use AAAA-MM-DD.")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise PDIError(str(exc)) from exc

def shift_months(value, count):
    source = date(value)
    number = source.year * 12 + source.month - 1 + count
    year, month = divmod(number, 12)
    month += 1
    return source.replace(year=year, month=month, day=min(source.day, calendar.monthrange(year, month)[1])).isoformat()

def window(event_on, cutoff_on, months, boundary_confirmed=False):
    if type(months) is not int or months <= 0:
        raise PDIError("A janela precisa ser um número inteiro positivo de meses.")
    lower = date(shift_months(cutoff_on, -months))
    event, cutoff = date(event_on), date(cutoff_on)
    uncertain = event in {lower, cutoff} and not boundary_confirmed
    return {"event_on": event_on, "cutoff_on": cutoff_on, "months": months,
            "lower_bound": lower.isoformat(), "within_inclusive_window": lower <= event <= cutoff,
            "status": "boundary_pending" if uncertain else ("within_window" if lower <= event <= cutoff else "outside_window"),
            "institutional_validation": "not_implied"}

def blank_state():
    return {"schema_version": SCHEMA, "revision": 0, "updated_at": now(),
            "profile": {"name": None, "role": None, "seniority": None, "step": None,
                        "area": None, "client": None, "timezone": None,
                        "weekly_capacity_hours": None, "leadership": None},
            "active_cycle": None, "sources": [], "evidence": [], "cycles": [], "changes": []}

def blank_cycle(cycle_id, label, starts_on=None, ends_on=None, cutoff_on=None, evaluation_on=None, policy_version="2025-07-29"):
    return {"id": valid_id(cycle_id), "label": label, "status": "draft",
            "starts_on": starts_on, "ends_on": ends_on, "evidence_cutoff_on": cutoff_on,
            "pdi_closes_on": None, "evaluation_on": evaluation_on,
            "policy_version": policy_version, "policy_confirmation": "pending",
            "milestones": [], **{k: [] for k in sorted(COLLECTIONS)}}

def find(records, record_id, label="registro"):
    result = next((r for r in records if r["id"] == record_id), None)
    if result is None:
        raise PDIError(f"{label} não encontrado: {record_id}")
    return result

def cycle(state, cycle_id=None):
    return find(state["cycles"], cycle_id or state["active_cycle"], "Ciclo")

def number(value, label):
    if type(value) not in {int, float} or value < 0 or value != value or value == float("inf"):
        raise PDIError(f"{label} deve ser um número finito não negativo.")

def unique(records, label):
    if not isinstance(records, list):
        raise PDIError(f"{label} precisa ser uma lista.")
    ids = []
    for row in records:
        if not isinstance(row, dict):
            raise PDIError(f"Cada item de {label} precisa ser um objeto.")
        ids.append(valid_id(row.get("id")))
    if len(ids) != len(set(ids)):
        raise PDIError(f"IDs duplicados em {label}.")
    return set(ids)

def refs(row, field, available):
    values = row.get(field, [])
    if not isinstance(values, list) or any(not isinstance(x, str) for x in values):
        raise PDIError(f"{field} deve ser uma lista de IDs.")
    missing = set(values) - available
    if missing:
        raise PDIError(f"Referências inexistentes em {field}: {sorted(missing)}")

def validate(state):
    required = set(blank_state())
    if not isinstance(state, dict) or set(state) != required:
        raise PDIError("Campos inválidos no estado; utilize o formato documentado.")
    if state["schema_version"] != SCHEMA or type(state["revision"]) is not int or state["revision"] < 0:
        raise PDIError("Schema/revisão não suportados.")
    profile = state["profile"]
    if not isinstance(profile, dict):
        raise PDIError("Perfil inválido.")
    try:
        if profile.get("timezone") is not None:
            ZoneInfo(profile["timezone"])
    except Exception as exc:
        raise PDIError("Timezone inválido.") from exc
    if profile.get("weekly_capacity_hours") is not None:
        number(profile["weekly_capacity_hours"], "Capacidade semanal")
    if profile.get("step") is not None and (type(profile["step"]) is not int or profile["step"] < 1):
        raise PDIError("Step deve ser inteiro positivo ou null.")
    source_ids = unique(state["sources"], "sources")
    evidence_ids = unique(state["evidence"], "evidence")
    cycle_ids = unique(state["cycles"], "cycles")
    if state["active_cycle"] is not None and state["active_cycle"] not in cycle_ids:
        raise PDIError("Ciclo ativo inexistente.")
    if not isinstance(state["changes"], list):
        raise PDIError("Histórico inválido.")
    for source in state["sources"]:
        if source.get("kind") not in {"institutional", "personal", "example", "mixed"}:
            raise PDIError("Fonte deve declarar kind: institutional/personal/example/mixed.")
        for field in {"local_path", "extracted_path"}:
            if source.get(field):
                local_path(source[field])
    for item in state["evidence"]:
        if item.get("local_path"):
            local_path(item["local_path"])
        if item.get("verification", "claimed") not in EVIDENCE_STATUSES:
            raise PDIError("Situação de evidência inválida.")
        if item.get("occurred_on") is not None:
            date(item["occurred_on"])
        refs(item, "source_ids", source_ids)
        if item.get("verification") == "institutionally_confirmed" and not item.get("confirmation_source"):
            raise PDIError("Confirmação institucional precisa de origem identificada.")
    active = []
    for c in state["cycles"]:
        if c.get("status") not in {"draft", "active", "archived"}:
            raise PDIError("Situação do ciclo inválida.")
        for key in {"starts_on", "ends_on", "evidence_cutoff_on", "pdi_closes_on", "evaluation_on"}:
            if c.get(key) is not None:
                date(c[key])
        if c.get("starts_on") and c.get("ends_on") and date(c["starts_on"]) > date(c["ends_on"]):
            raise PDIError("Início do ciclo é posterior ao fim.")
        if c.get("evidence_cutoff_on") and c.get("starts_on") and date(c["evidence_cutoff_on"]) < date(c["starts_on"]):
            raise PDIError("Data de corte é anterior ao início.")
        if c.get("status") == "active":
            active.append(c["id"])
            if not c.get("starts_on") or not c.get("ends_on") or not c.get("evidence_cutoff_on"):
                raise PDIError("Ativar ciclo exige início, fim e corte concretos.")
        for milestone in c.get("milestones", []):
            date(milestone["on"])
        for key in COLLECTIONS:
            unique(c.get(key), key)
        objective_ids = {x["id"] for x in c["objectives"]}
        action_ids = {x["id"] for x in c["actions"]}
        for objective in c["objectives"]:
            refs(objective, "source_ids", source_ids)
            refs(objective, "evidence_ids", evidence_ids)
        for action in c["actions"]:
            if not action.get("title") or action.get("status") not in ACTION_STATUSES:
                raise PDIError("Ação precisa de título e status válido.")
            if action.get("due_on") is not None:
                date(action["due_on"])
            if action.get("completed_on") is not None:
                date(action["completed_on"])
            if action.get("effort_hours") is not None:
                number(action["effort_hours"], "Esforço")
            refs(action, "objective_ids", objective_ids)
            refs(action, "evidence_ids", evidence_ids)
            refs(action, "source_ids", source_ids)
            refs(action, "depends_on", action_ids)
            if action["id"] in action.get("depends_on", []):
                raise PDIError("Uma ação não pode depender de si mesma.")
            for key in {"description", "result", "pdi_description"}:
                if action.get(key) is not None and not isinstance(action[key], str):
                    raise PDIError(f"Texto inválido: {key}.")
        graph = {a["id"]: a.get("depends_on", []) for a in c["actions"]}
        visiting, visited = set(), set()
        def visit(node):
            if node in visiting:
                raise PDIError("Dependências circulares entre ações.")
            if node in visited:
                return
            visiting.add(node)
            for parent in graph[node]:
                visit(parent)
            visiting.remove(node); visited.add(node)
        for node in graph:
            visit(node)
        for assessment in c["criterion_assessments"]:
            valid_id(assessment.get("criterion_id"))
            if assessment.get("status") not in CRITERION_STATUSES:
                raise PDIError("Situação de critério inválida.")
            refs(assessment, "evidence_ids", evidence_ids)
            refs(assessment, "source_ids", source_ids)
            if assessment.get("reference_on") is not None:
                date(assessment["reference_on"])
            if assessment.get("status") == "confirmed" and not assessment.get("confirmation_source"):
                raise PDIError("Critério confirmado exige confirmation_source.")
        for assessment in c["competency_assessments"]:
            if assessment.get("assessment_type") not in {"official", "self", "inferred"}:
                raise PDIError("Avaliação técnica deve distinguir official/self/inferred.")
            refs(assessment, "source_ids", source_ids)
            if assessment.get("assessed_on") is not None:
                date(assessment["assessed_on"])
        for event in c["events"]:
            refs(event, "source_ids", source_ids)
            refs(event, "related_action_ids", action_ids)
            if event.get("occurred_on") is not None:
                date(event["occurred_on"])
        for metric in c["metrics"]:
            refs(metric, "source_ids", source_ids)
            for key in ("value", "baseline"):
                if metric.get(key) is not None:
                    number(metric[key], f"Métrica: {key}")
            for key in ("period_start", "period_end"):
                if metric.get(key) is not None:
                    date(metric[key])
            if metric.get("period_start") and metric.get("period_end") and date(metric["period_start"]) > date(metric["period_end"]):
                raise PDIError("Período da métrica invertido.")
    if len(active) > 1 or (active and state["active_cycle"] != active[0]) or (not active and state["active_cycle"] is not None):
        raise PDIError("Ponteiro de ciclo ativo inconsistente.")
    return state

def local_path(value):
    from pathlib import PurePosixPath
    if not isinstance(value, str) or not value or "\\" in value or PurePosixPath(value).is_absolute() or ".." in PurePosixPath(value).parts:
        raise PDIError("Arquivo individual deve usar caminho relativo sem '..' ou backslash.")
    return value

def apply_operations(state, operations):
    result = copy.deepcopy(state)
    if not isinstance(operations, list) or not operations:
        raise PDIError("Proposta precisa de operações.")
    for op in operations:
        if not isinstance(op, dict):
            raise PDIError("Cada operação precisa ser um objeto.")
        kind = op.get("op")
        if kind == "profile":
            if not isinstance(op.get("value"), dict):
                raise PDIError("Perfil deve ser um objeto.")
            result["profile"].update(op["value"])
        elif kind == "calendar":
            c = cycle(result, op.get("cycle_id"))
            if c["status"] == "archived":
                raise PDIError("Ciclo encerrado não pode ser editado.")
            allowed = {"label", "starts_on", "ends_on", "evidence_cutoff_on", "pdi_closes_on", "evaluation_on", "policy_version", "policy_confirmation", "milestones"}
            if not isinstance(op.get("value"), dict) or set(op["value"]) - allowed:
                raise PDIError("Campos de calendário não permitidos.")
            c.update(op["value"])
        elif kind == "upsert":
            key = op.get("collection")
            if key in {"sources", "evidence"}:
                rows = result[key]
            elif key in COLLECTIONS:
                c = cycle(result, op.get("cycle_id"))
                if c["status"] == "archived":
                    raise PDIError("Ciclo encerrado não pode ser editado.")
                rows = c[key]
            else:
                raise PDIError("Coleção não permitida.")
            row = op.get("value")
            if not isinstance(row, dict):
                raise PDIError("Registro precisa ser objeto.")
            valid_id(row.get("id"))
            old = next((x for x in rows if x["id"] == row["id"]), None)
            if old is None:
                rows.append(copy.deepcopy(row))
            else:
                old.update(copy.deepcopy(row))
        else:
            raise PDIError("Operação desconhecida. Exclusão de registros não é suportada.")
    return validate(result)
