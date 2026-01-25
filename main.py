#!/usr/bin/env python3
"""
Automação RustScan + Nmap + DefectDojo
Hackers do Bem - Residência POP
"""

import os
import sys
import yaml
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for d in ["coletar", "observar", "reagir", "saida", "utils", "logs"]:
    sys.path.append(os.path.join(BASE_DIR, d))


# =========================================================
# SETUP
# =========================================================

def setup_logger(config):
    from logs.logger_config import setup_logger as _setup
    logger = _setup(config.get("logs", {}))
    print("✅ Logger configurado")
    return logger


def carregar_configuracao():
    with open(os.path.join(BASE_DIR, "config.yaml"), "r") as f:
        config = yaml.safe_load(f)
    print(f"✅ Configuração carregada: {list(config.keys())}")
    return config


# =========================================================
# INTERFACE INICIAL
# =========================================================

def interface_inicial():
    print("=" * 50)
    print("CONFIGURAÇÃO INICIAL DA AUTOMAÇÃO")
    print("=" * 50)

    print("\nTipo de varredura:")
    print("[1] Rápida  (descoberta de portas)")
    print("[2] Completa (descoberta + scans direcionados)")
    tipo = input("Escolha [1/2]: ").strip()
    tipo_scan = "rapido" if tipo == "1" else "completo"

    print("\nAlvo da varredura")
    print("- IP único        → 192.168.0.10")
    print("- Hostname/DNS   → scanme.nmap.org")
    print("- Range (CIDR)   → 192.168.0.0/24")
    alvo = input("Alvo: ").strip()

    print("\nFrequência:")
    print("[1] A cada 24 horas (recomendado)")
    print("[2] A cada 12 horas")
    print("[3] A cada 6 horas")
    freq_map = {"1": 24, "2": 12, "3": 6}
    freq = freq_map.get(input("Escolha [1/2/3]: ").strip(), 24)

    print("\nDuração da automação (dias)")
    duracao = int(input("Ex: 7, 30, 90 → ").strip())

    print("\nCONFIGURAÇÃO FINALIZADA\n")

    return {
        "tipo_scan": tipo_scan,
        "alvos": [alvo],
        "frequencia_horas": freq,
        "duracao_dias": duracao,
    }


# =========================================================
# FASES
# =========================================================

def executar_coleta(alvos, config, logger):
    from coletar.rustscan_wrapper_fast import RustScanWrapperFast
    coletor = RustScanWrapperFast(config, logger)
    return [coletor.executar_scan_rapido(a) for a in alvos]


def executar_analise(resultados, config, logger):
    from observar.analise_resultados import AnalisadorResultados
    analisador = AnalisadorResultados(config, logger)
    return analisador.analisar(resultados)


def executar_reagir(resultados, analise, config, logger, output_dir):
    from reagir.scans_direcionados import ScansDirecionados
    reagir = ScansDirecionados(config, logger)
    return reagir.executar_scans(resultados, analise, output_dir)


def executar_saida_defectdojo(resultados, logger, output_dir):
    from saida.nmap_xml import NmapXMLExporter
    exportador = NmapXMLExporter(logger)
    return exportador.exportar(resultados, output_dir)


# =========================================================
# MAIN
# =========================================================

def main():
    print("=" * 60)
    print("INICIANDO AUTOMAÇÃO DE SEGURANÇA – POP")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    config = carregar_configuracao()
    logger = setup_logger(config)

    config_usuario = interface_inicial()

    # Estrutura de diretórios
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H%M%S")
    base = os.path.join("resultados", data_hoje, hora)

    dirs = {
        "base": base,
        "coleta": os.path.join(base, "coleta"),
        "analise": os.path.join(base, "analise"),
        "reagir": os.path.join(base, "reagir"),
        "saida": os.path.join(base, "saida_defectdojo"),
    }

    for d in dirs.values():
        os.makedirs(d, exist_ok=True)

    print(f"📁 Resultados em: {base}")

    # FASE 1
    print("\n[FASE 1: COLETAR]")
    resultados = executar_coleta(config_usuario["alvos"], config, logger)

    # FASE 2
    print("\n[FASE 2: OBSERVAR]")
    analise = executar_analise(resultados, config, logger)

    # FASE 3 (opcional)
    if config_usuario["tipo_scan"] == "completo":
        print("\n[FASE 3: REAGIR]")
        executar_reagir(resultados, analise, config, logger, dirs["reagir"])

    # FASE 4
    print("\n[FASE 4: SAÍDA – DEFECTDOJO]")
    caminho = executar_saida_defectdojo(resultados, logger, dirs["saida"])
    print(f"📤 Arquivo pronto para importação: {caminho}")

    print("\n" + "=" * 60)
    print("✅ EXECUÇÃO CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
