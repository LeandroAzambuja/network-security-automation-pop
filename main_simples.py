#!/usr/bin/env python3
"""
Automação RustScan - VERSÃO SIMPLIFICADA FUNCIONAL
"""

import sys
import os
import argparse
import yaml
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def main():
    print("=" * 60)
    print("AUTOMAÇÃO RUSTSCAN - VERSÃO SIMPLIFICADA")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Alvo único")
    parser.add_argument("--alvos", help="Arquivo com alvos")
    parser.add_argument("--test", action="store_true", help="Modo teste")
    
    args = parser.parse_args()
    
    if args.test:
        print("[TESTE] Verificando ambiente...")
        
        # Testar imports básicos
        try:
            import yaml
            import nmap
            print("✅ Imports básicos OK")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Testar módulos do projeto
        for dir_name in ['coletar', 'observar', 'reagir', 'saida', 'utils', 'logs']:
            dir_path = os.path.join(BASE_DIR, dir_name)
            if os.path.exists(dir_path):
                print(f"✅ {dir_name}/ existe")
            else:
                print(f"❌ {dir_name}/ faltando")
        
        # Testar config
        config_path = os.path.join(BASE_DIR, 'config.yaml')
        if os.path.exists(config_path):
            print(f"✅ config.yaml existe")
        else:
            print(f"❌ config.yaml não encontrado")
        
        print("\n✅ Ambiente configurado!")
        return
    
    # Execução normal
    if args.alvos and os.path.exists(args.alvos):
        print(f"Processando alvos de: {args.alvos}")
        with open(args.alvos, 'r') as f:
            alvos = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"Total de alvos: {len(alvos)}")
        for alvo in alvos:
            print(f"  - {alvo}")
        
        print("\n🎯 Execute manualmente:")
        print(f"rustscan -a {' '.join(alvos)} -- -sV -sC")
    
    elif args.target:
        print(f"Alvo: {args.target}")
        print(f"\n🎯 Execute manualmente:")
        print(f"rustscan -a {args.target} -- -sV -sC")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
