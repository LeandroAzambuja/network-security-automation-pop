#!/usr/bin/env python3
"""
Automação de Varredura de Segurança
POP – Residência Técnica
"""

import os
import sys
import yaml
import time
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

for d in ["coletar", "observar", "reagir", "saida", "utils", "logs"]:
    sys.path.append(os.path.join(BASE_DIR, d))


def setup_logger(config):
    from logs.logger_config import setup_logger as _setup
    return _setup(config.get("logs", {}))


def carregar_configuracao():
    with open(os.path.join(BASE_DIR, "config.yaml"), "r") as f:
        return yaml.safe_load(f)


def interface_interativa():
    print("=" * 50)
    print("CONFIGURAÇÃO INTERATIVA")
    print("=" * 50)

    scan = "rapido" if input("[1] Rápida | [2] Completa: ").strip() == "1" else "completo"
    alvo = input("Alvo: ").strip()
    duracao = int(input("Duração (dias): ").strip())

    return {
        "scan": scan,
        "alvos": [alvo],
        "duracao_dias": duracao,
        "modo": "interativo",
    }


def executar_pipeline(config_usuario, config, logger):
    from coletar.rustscan_wrapper_fast import RustScanWrapperFast
    from observar.analise_resultados import AnalisadorResultados
    from reagir.scans_direcionados import ScansDirecionados
    from saida.defectdojo_csv import DefectDojoCSVExporter

    base = os.path.join(
        "resultados",
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%H%M%S"),
    )

    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, "reagir"), exist_ok=True)
    os.makedirs(os.path.join(base, "saida_defectdojo"), exist_ok=True)

    logger.info(f"Resultados em: {base}")

    coletor = RustScanWrapperFast(config, logger)
    resultados = [coletor.executar_scan_rapido(a) for a in config_usuario["alvos"]]

    analisador = AnalisadorResultados(config, logger)
    analise = analisador.analisar(resultados)

    if config_usuario["scan"] == "completo":
        ScansDirecionados(config, logger).executar_scans(
            resultados, analise, os.path.join(base, "reagir")
        )

    caminho = DefectDojoCSVExporter(logger).exportar(
        resultados, analise, os.path.join(base, "saida_defectdojo")
    )

    logger.info(f"CSV pronto para importação: {caminho}")


def executar(config_usuario=None):
    from utils.lock import acquire_lock, release_lock, status

    config = carregar_configuracao()
    logger = setup_logger(config)

    if not config_usuario:
        config_usuario = interface_interativa()

    meta = {
        "scan": config_usuario["scan"],
        "alvos": config_usuario["alvos"],
        "expires_at": (
            datetime.now()
            + timedelta(days=config_usuario.get("duracao_dias", 1))
        ).strftime("%Y-%m-%d %H:%M:%S"),
    }

    if not acquire_lock(meta):
        print("❌ Já existe uma execução em andamento.")
        sys.exit(1)

    try:
        executar_pipeline(config_usuario, config, logger)
    finally:
        release_lock()

