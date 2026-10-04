#!/usr/bin/env python3
"""Entrada portátil: python3 scripts/pdi.py --help."""
from pathlib import Path
import json
import os
import sys

if sys.version_info < (3, 11) or os.name != "posix":
    print(json.dumps({"error": "Use Python 3.11 ou superior no Ubuntu/Linux. No Windows, execute dentro do Ubuntu/WSL2; confira INSTALL.md."}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pdi_copilot.cli import main
if __name__ == "__main__":
    raise SystemExit(main())
