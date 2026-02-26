"""
Wrapper otimizado para RustScan rápido.
Hackers do Bem
"""

import subprocess
import json
import re

class RustScanWrapperFast:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
    def testar_rustscan(self):
        """Testa se RustScan está disponível."""
        try:
            resultado = subprocess.run(["rustscan", "--version"], 
                                     capture_output=True, text=True)
            return resultado.returncode == 0
        except FileNotFoundError:
            self.logger.error("RustScan não encontrado. Instale com: cargo install rustscan")
            return False
    
    def executar_scan_rapido(self, alvo):
        """Executa scan rápido em TODAS as portas (1-65535)."""
        
        comando = [
            "rustscan",
            "-a", alvo,
            "-t", "1500",
            "-b", "500",
            "--ulimit", "5000",
            "--range", "1-65535",
            "--",
            "-sT", "-T5", "--max-retries", "1", "--host-timeout", "120s"
        ]
         
        self.logger.debug(f"Comando rápido: {' '.join(comando)}")
        
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True, timeout=180)
            
            if resultado.returncode != 0:
                self.logger.error(f"Erro no RustScan: {resultado.stderr[:200]}")
                return {"alvo": alvo, "sucesso": False, "erro": resultado.stderr[:200]}
            
            # Parse do resultado
            portas_encontradas = self._parsear_resultado_rustscan(resultado.stdout)
            
            return {
                "alvo": alvo,
                "sucesso": True,
                "portas": portas_encontradas,
                "comando": " ".join(comando),
                "raw_output": resultado.stdout[:500] + "..." if len(resultado.stdout) > 500 else resultado.stdout
            }
             
        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout no scan de {alvo}")
            return {"alvo": alvo, "sucesso": False, "erro": "timeout"}
        except Exception as e:
            self.logger.error(f"Erro executando scan: {e}")
            return {"alvo": alvo, "sucesso": False, "erro": str(e)}
    
    def _parsear_resultado_rustscan(self, output):
        """Parseia output do RustScan para lista de portas."""
        portas = []
        
        # Procura por linhas com portas abertas
        for linha in output.split('\n'):
            linha = linha.strip()
            
            # Formato: PORT   STATE SERVICE REASON
            if re.match(r'^\d+/tcp\s+open', linha):
                partes = linha.split()
                if len(partes) >= 3:
                    porta_proto = partes[0]  # "80/tcp"
                    porta_num = porta_proto.split('/')[0]
                    
                    portas.append({
                        "porta": int(porta_num),
                        "protocolo": "tcp",
                        "status": "open",
                        "servico": partes[2] if len(partes) > 2 else "unknown"
                    })
        
        self.logger.info(f"Portas encontradas (scan rápido): {len(portas)}")
        return portas
