#!/usr/bin/env python3
"""Teste do módulo de análise."""

import sys
sys.path.append('.')

from logs.logger_config import setup_logger
from observar.analise_resultados import AnalisadorResultados
import json

# Configura logger
logger = setup_logger("INFO")

# Carrega resultados salvos
with open('resultado_teste_1766788280/resultados_coleta.json', 'r') as f:
    resultados_coleta = json.load(f)

print("=" * 60)
print("TESTE DO MÓDULO OBSERVAR (ANÁLISE)")
print("=" * 60)

print(f"Resultados carregados: {len(resultados_coleta)} alvo(s)")

# Cria analisador
analisador = AnalisadorResultados({}, logger)

# Executa análise
analise = analisador.analisar(resultados_coleta, "resultado_teste_1766788280")

print("\n📊 RESUMO DA ANÁLISE:")
print("=" * 40)

resumo = analise.get("resumo", {})
print(f"Alvos analisados: {resumo.get('alvos_analisados', 0)}")
print(f"Portas encontradas: {resumo.get('portas_encontradas', 0)}")
print(f"Riscos identificados: {resumo.get('riscos_identificados', 0)}")
print(f"  - Riscos ALTOS: {resumo.get('riscos_altos', 0)}")
print(f"  - Riscos MÉDIOS: {resumo.get('riscos_medios', 0)}")
print(f"Serviços web: {resumo.get('servicos_web', 0)}")
print(f"Serviços banco de dados: {resumo.get('servicos_banco_dados', 0)}")
print(f"Status geral: {resumo.get('status', 'DESCONHECIDO')}")

print("\n🔍 SERVIÇOS IDENTIFICADOS:")
print("=" * 40)

servicos = analise.get("servicos_identificados", {})
for categoria, lista_servicos in servicos.items():
    if lista_servicos:
        print(f"\n{categoria.upper()}:")
        for servico in lista_servicos[:3]:  # Mostra apenas 3 de cada
            print(f"  - {servico['alvo']}:{servico['porta']} ({servico['servico']})")
        if len(lista_servicos) > 3:
            print(f"  ... e mais {len(lista_servicos) - 3}")

print("\n⚠️  RISCOS IDENTIFICADOS:")
print("=" * 40)

riscos = analise.get("riscos_potenciais", [])
if riscos:
    for risco in riscos:
        print(f"\nAlvo: {risco['alvo']}")
        print(f"Porta: {risco['porta']} ({risco['servico']})")
        print(f"Severidade: {risco['severidade'].upper()}")
        print(f"Descrição: {risco['descricao']}")
        print(f"Recomendação: {risco['recomendacao']}")
else:
    print("Nenhum risco identificado 👍")

print("\n💡 RECOMENDAÇÕES:")
print("=" * 40)

for recomendacao in analise.get("recomendacoes", []):
    print(f"• {recomendacao}")

print("\n" + "=" * 60)
print("✅ Análise concluída com sucesso!")
print("=" * 60)
