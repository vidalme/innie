#!/usr/bin/env python3
"""Verifica estrutura, JSON e links Markdown locais sem rede/dependências."""
from pathlib import Path
import json
import hashlib
import re
import sys
root = Path(__file__).resolve().parents[1]
errors = []

def check_sources(knowledge):
    """Verifica os artefatos disponíveis, sem presumir acesso aos originais."""
    problems = []
    try:
        registry = json.loads((knowledge / 'sources/registry.json').read_text())
        if registry.get('path_base') != 'knowledge':
            problems.append('Registro de fontes precisa declarar path_base=knowledge.')
        ids = set()
        for entry in registry['sources']:
            sid = entry['id']
            if not re.fullmatch(r'[IPX]\d{2}', sid) or sid in ids:
                problems.append(f'ID de fonte inválido/duplicado: {sid}')
            ids.add(sid)
            relative = entry.get('file')
            if relative is None:
                if entry.get('availability') != 'not_distributed' or not entry.get('limitation'):
                    problems.append(f'Fonte ausente sem limitação explícita: {sid}')
                continue
            path = (knowledge / relative).resolve()
            if not path.is_relative_to(knowledge.resolve()):
                problems.append(f'Fonte fora de knowledge: {sid}')
            elif not path.is_file():
                problems.append(f'Artefato de fonte ausente: {sid}: {relative}')
            elif entry.get('availability') != 'distributed' or hashlib.sha256(path.read_bytes()).hexdigest() != entry.get('sha256'):
                problems.append(f'Hash/disponibilidade da fonte divergente: {sid}')
        for folder in ('criteria', 'policies', 'competencies', 'evidence-guidance'):
            for path in (knowledge / folder).rglob('*'):
                if path.suffix not in {'.json', '.md'}:
                    continue
                for sid in set(re.findall(r'\b[IPX]\d{2}\b', path.read_text())) - ids:
                    problems.append(f'Fonte não registrada em {path.relative_to(knowledge)}: {sid}')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        problems.append(f'Registro de fontes inválido: {exc}')
    return problems

errors.extend(check_sources(root / 'knowledge'))
if "--distribution" in sys.argv:
    for private in ("pessoal", ".local"):
        if (root / private).exists() or (root / private).is_symlink():
            errors.append(f"Distribuição contém configuração individual: {private}")
required = ["README.md", "INSTALL.md", "AGENTS.md", "docs/architecture.md", "docs/scripts.md", "docs/data-contracts.md", "templates/example-changes.json", "schemas/state.schema.json", "knowledge/index.json"]
for rel in required:
    if not (root / rel).is_file(): errors.append(f"Ausente: {rel}")
for folder, glob, count in [(".github/agents", "*.agent.md", 7), (".github/skills", "*/SKILL.md", 14), (".github/prompts", "*.prompt.md", 9)]:
    actual = len(list((root / folder).glob(glob)))
    if actual != count: errors.append(f"{folder}: {actual}, esperado {count}")
for p in root.rglob("*.json"):
    if any(x in p.parts for x in [".git", ".local", "pessoal"]): continue
    try: json.loads(p.read_text())
    except (ValueError, OSError) as exc: errors.append(f"JSON {p.relative_to(root)}: {exc}")
for p in root.rglob("*.md"):
    if any(x in p.parts for x in [".git", ".local", "pessoal", "planning", "sources"]): continue
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", p.read_text()):
        target = target.split("#")[0]
        if not target or "://" in target or target.startswith(("mailto:", "sandbox:", "#")): continue
        if " " in target: continue
        if not (p.parent / target).exists(): errors.append(f"Link ausente em {p.relative_to(root)}: {target}")
if errors:
    print("\n".join(errors), file=sys.stderr); sys.exit(1)
print("Pacote válido: estrutura, 7 agentes, 14 skills, 9 prompts, JSON, links locais e proveniência das fontes.")
