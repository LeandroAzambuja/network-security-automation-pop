#!/usr/bin/env python3
"""Teste do wrapper RustScan."""

import sys
sys.path.append('.')

from logs.logger_config import setup_logger
from coletar.rustscan_wrapper import RustScanWrapper

# Configuração básica
config = {
    "configuracao": {
        "tipo_scan": "rapido"
    }
}

# Logger
logger = setup_logger("INFO")

# Cria wrapper
wrapper = RustScanWrapper(config, logger)

print("=" * 60)
print("TESTE DO WRAPPER RUSTSCAN")
print("=" * 60)

# Testa disponibilidade
print("\n1. Testando disponibilidade do RustScan...")
if wrapper.testar_rustscan():
    print("✓ RustScan disponível")
    
    # Teste básico (apenas se RustScan estiver instalado)
    print("\n2. Testando scan básico (apenas demonstração)...")
    print("   (Não executará scan real neste teste)")
    
    # Simulação de resultado
    resultado_simulado = {
        "alvo": "scanme.nmap.org",
        "sucesso": True,
        "portas": [
            {"porta": 80, "protocolo": "tcp", "status": "open"},
            {"porta": 22, "protocolo": "tcp", "status": "open"}
        ]
    }
    
    print(f"   Alvo: {resultado_simulado['alvo']}")
    print(f"   Portas encontradas: {len(resultado_simulado['portas'])}")
    for porta in resultado_simulado['portas']:
        print(f"   - Porta {porta['porta']}/{porta['protocolo']}: {porta['status']}")
    
else:
    print("✗ RustScan não disponível")
    print("   Instale com: cargo install rustscan")

print("\n" + "=" * 60)
print("Teste concluído!")
print("=" * 60)
