#!/usr/bin/env python3
"""Verifica estrutura, JSON e links Markdown locais sem rede/dependências."""
from pathlib import Path
import json
import re
import sys
root = Path(__file__).resolve().parents[1]
errors = []
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
print("Pacote válido: estrutura, 7 agentes, 14 skills, 9 prompts, JSON e links locais.")
