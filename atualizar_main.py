#!/usr/bin/env python3
"""Script para atualizar o main.py."""

with open('main.py', 'r') as f:
    content = f.read()

# Adiciona import do wrapper rápido
import_line = 'from coletar.rustscan_wrapper import RustScanWrapper'
new_import_line = 'from coletar.rustscan_wrapper import RustScanWrapper\nfrom coletar.rustscan_wrapper_fast import RustScanWrapperFast'

if import_line in content:
    content = content.replace(import_line, new_import_line)
    print("✓ Import adicionado")
else:
    print("✗ Linha de import não encontrada")

# Salva
with open('main.py', 'w') as f:
    f.write(content)

print("✓ main.py atualizado")
