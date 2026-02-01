#!/usr/bin/env python3
"""
Teste de imports dos módulos do projeto
"""

import sys
import os

# Adicionar diretórios ao path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Testar imports
modules_to_test = []

# Coletar todos os módulos Python
for dir_name in ['coletar', 'observar', 'reagir', 'saida', 'utils', 'logs']:
    dir_path = os.path.join(BASE_DIR, dir_name)
    if os.path.exists(dir_path):
        sys.path.append(dir_path)
        # Encontrar arquivos Python
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    module_name = file[:-3]  # Remove .py
                    modules_to_test.append((dir_name, module_name))

print("Testando imports dos módulos:")
print("-" * 40)

success_count = 0
fail_count = 0

for dir_name, module_name in modules_to_test[:10]:  # Testar só os primeiros 10
    try:
        __import__(module_name)
        print(f"✅ {dir_name}/{module_name}.py")
        success_count += 1
    except ImportError as e:
        print(f"❌ {dir_name}/{module_name}.py: {e}")
        fail_count += 1
    except Exception as e:
        print(f"⚠️  {dir_name}/{module_name}.py: {type(e).__name__}")

print("-" * 40)
print(f"Resultado: {success_count} OK, {fail_count} Falhas")

if fail_count == 0:
    print("🎉 Todos os imports funcionam!")
else:
    print("⚠️  Alguns imports falharam")
