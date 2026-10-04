#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null; then
  echo "Python 3 ausente. No Ubuntu, use bash scripts/install.sh --install-deps; confira INSTALL.md." >&2
  exit 2
fi
if [[ $# -eq 0 ]]; then
  set -- setup --format text
fi
exec python3 "$script_dir/pdi.py" "$@"
