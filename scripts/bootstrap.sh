#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -eq 0 ]]; then
  set -- setup
fi
exec python3 "$script_dir/pdi.py" "$@"
