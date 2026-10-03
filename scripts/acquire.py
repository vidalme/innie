#!/usr/bin/env python3
"""Clonar um innie já publicado. Não cria repositórios remotos ou credenciais."""
import argparse
from pathlib import Path
import subprocess

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--innie-url', required=True)
    p.add_argument('--destination', required=True)
    a = p.parse_args()
    target = Path(a.destination).expanduser().resolve()
    if target.exists(): p.error('Destino já existe; não será sobrescrito.')
    if not a.innie_url.startswith(('https://', 'ssh://', 'git@')):
        p.error('Use URL HTTPS ou SSH do repositório autorizado.')
    subprocess.run(['git', 'clone', '--', a.innie_url, str(target)], check=True)
    print('Núcleo clonado. Execute python3 scripts/pdi.py setup dentro dele.')

if __name__ == '__main__': main()
