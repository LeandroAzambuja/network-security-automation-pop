#!/usr/bin/env python3
"""
Automação RustScan - VERSÃO QUE EXECUTA REALMENTE
"""

import sys
import os
import argparse
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def executar_rustscan(alvo, modo_rapido=True):
    """Executa RustScan no alvo"""
    print(f"\n🔍 Executando RustScan em: {alvo}")
    
    if modo_rapido:
        comando = ["rustscan", "-a", alvo, "--", "-sV", "-sC", "-T4"]
    else:
        comando = ["rustscan", "-a", alvo, "--", "-sV", "-sC", "-A", "-p-", "-T4"]
    
    print(f"Comando: {' '.join(comando)}")
    print("-" * 60)
    
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        print("SAÍDA DO RUSTSCAN:")
        print(resultado.stdout)
        
        if resultado.stderr:
            print("ERROS:")
            print(resultado.stderr)
        
        # Salvar resultado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"resultado_scan_{alvo.replace('.', '_')}_{timestamp}.txt"
        
        with open(nome_arquivo, 'w') as f:
            f.write(f"Alvo: {alvo}\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Comando: {' '.join(comando)}\n")
            f.write("\n" + "="*60 + "\n")
            f.write(resultado.stdout)
            if resultado.stderr:
                f.write("\nERROS:\n")
                f.write(resultado.stderr)
        
        print(f"\n✅ Resultado salvo em: {nome_arquivo}")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout ao escanear {alvo}")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar RustScan: {e}")
        return False

def main():
    print("=" * 60)
    print("AUTOMAÇÃO RUSTSCAN - EXECUÇÃO REAL")
    print("Hackers do Bem - Residência")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="Alvo único")
    parser.add_argument("--alvos", help="Arquivo com alvos")
    parser.add_argument("--test", action="store_true", help="Modo teste")
    parser.add_argument("--completo", action="store_true", help="Scan completo (mais lento)")
    
    args = parser.parse_args()
    
    if args.test:
        print("[TESTE] Verificando RustScan...")
        
        # Testar se RustScan está instalado
        try:
            resultado = subprocess.run(["rustscan", "--version"], 
                                     capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"✅ RustScan instalado: {resultado.stdout.strip()}")
            else:
                print("❌ RustScan não funciona corretamente")
        except FileNotFoundError:
            print("❌ RustScan não encontrado. Instale com: sudo apt install rustscan")
        
        # Testar scan rápido em localhost (sem rede)
        print("\n[TESTE] Scan rápido em localhost (portas comuns)...")
        comando_teste = ["rustscan", "-a", "127.0.0.1", "-p", "22,80,443", "--", "-sS", "-T4"]
        print(f"Comando teste: {' '.join(comando_teste)}")
        
        try:
            subprocess.run(comando_teste, timeout=10)
            print("✅ Teste de comando OK")
        except:
            print("⚠️  Teste básico concluído")
        
        return
    
    # Execução normal
    alvos = []
    
    if args.alvos and os.path.exists(args.alvos):
        print(f"📄 Carregando alvos de: {args.alvos}")
        with open(args.alvos, 'r') as f:
            alvos = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    elif args.target:
        alvos = [args.target]
        print(f"🎯 Alvo único: {args.target}")
    
    else:
        parser.print_help()
        return
    
    if not alvos:
        print("❌ Nenhum alvo válido especificado")
        return
    
    print(f"📊 Total de alvos: {len(alvos)}")
    
    # Confirmar execução
    if len(alvos) > 1:
        resposta = input(f"\n⚠️  Executar scan em {len(alvos)} alvos? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Cancelado pelo usuário")
            return
    
    # Executar scans
    resultados = []
    modo_rapido = not args.completo
    
    for i, alvo in enumerate(alvos, 1):
        print(f"\n{'='*60}")
        print(f"ALVO {i}/{len(alvos)}: {alvo}")
        print(f"{'='*60}")
        
        sucesso = executar_rustscan(alvo, modo_rapido)
        resultados.append((alvo, sucesso))
        
        # Pequena pausa entre scans
        if i < len(alvos):
            print("\n⏳ Aguardando 2 segundos antes do próximo alvo...")
            import time
            time.sleep(2)
    
    # Resumo
    print(f"\n{'='*60}")
    print("RESUMO DA EXECUÇÃO:")
    print(f"{'='*60}")
    
    sucessos = sum(1 for _, sucesso in resultados if sucesso)
    print(f"✅ Sucessos: {sucessos}/{len(resultados)}")
    print(f"📁 Resultados salvos em arquivos .txt")
    
    if sucessos > 0:
        print("\n🎯 Para análise avançada, execute:")
        print("python3 main.py --fase observar  # Analisar resultados")
        print("python3 main.py --fase reagir    # Scans direcionados")

if __name__ == "__main__":
    main()
