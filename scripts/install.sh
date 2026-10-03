#!/usr/bin/env bash
# Executar dentro do Ubuntu/WSL2. Instalação de pacotes exige opção explícita.
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == "--install-deps" ]]; then
  shift
  if ! command -v apt-get >/dev/null; then
    echo "Esta opção exige Ubuntu/Debian. Instale Python 3 e Git por seu gerenciador." >&2
    exit 2
  fi
  sudo apt-get update
  sudo apt-get install -y python3 git poppler-utils
fi
if ! command -v python3 >/dev/null; then
  echo "Python 3 ausente. Use bash scripts/install.sh --install-deps no Ubuntu." >&2
  exit 2
fi
exec python3 "$script_dir/pdi.py" "$@" setup
