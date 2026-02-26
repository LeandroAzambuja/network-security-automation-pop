"""
Wrapper completo para RustScan.
Hackers do Bem
"""

import subprocess
import json

class RustScanWrapper:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    def executar_scan(self, alvo, tipo_scan="rapido"):
        """Executa scan baseado no tipo."""
        if tipo_scan == "rapido":
            return self._scan_rapido(alvo)
        elif tipo_scan == "completo":
            return self._scan_completo(alvo)
        else:
            return self._scan_rapido(alvo)
    
    def _scan_rapido(self, alvo):
        """Scan rápido nas portas comuns."""
        comando = f"rustscan -a {alvo} -t 1500 -b 500 --ulimit 1000 -- -sS -T5"
        
        try:
            self.logger.info(f"Executando scan rápido em: {alvo}")
            resultado = subprocess.run(comando.split(), capture_output=True, text=True)
            
            if resultado.returncode == 0:
                portas = self._extrair_portas(resultado.stdout)
                return {"alvo": alvo, "sucesso": True, "portas": portas}
            else:
                return {"alvo": alvo, "sucesso": False, "erro": resultado.stderr}
                
        except Exception as e:
            return {"alvo": alvo, "sucesso": False, "erro": str(e)}
    
    def _scan_completo(self, alvo):
        """Scan completo em todas as portas."""
        comando = f"rustscan -a {alvo} -t 2000 -b 1000 --ulimit 5000 -- -sS -sV -sC -O -A"
        
        try:
            self.logger.info(f"Executando scan completo em: {alvo}")
            resultado = subprocess.run(comando.split(), capture_output=True, text=True, timeout=300)
            
            if resultado.returncode == 0:
                portas = self._extrair_portas(resultado.stdout)
                return {"alvo": alvo, "sucesso": True, "portas": portas}
            else:
                return {"alvo": alvo, "sucesso": False, "erro": resultado.stderr}
                
        except subprocess.TimeoutExpired:
            return {"alvo": alvo, "sucesso": False, "erro": "timeout"}
        except Exception as e:
            return {"alvo": alvo, "sucesso": False, "erro": str(e)}
    
    def _extrair_portas(self, output):
        """Extrai portas do output do RustScan."""
        portas = []
        linhas = output.split('\n')
        
        for linha in linhas:
            if '/tcp' in linha and 'open' in linha:
                partes = linha.split()
                if len(partes) >= 3:
                    porta_proto = partes[0]  # "80/tcp"
                    porta = int(porta_proto.split('/')[0])
                    
                    portas.append({
                        "porta": porta,
                        "protocolo": "tcp",
                        "status": "open",
                        "servico": partes[2]
                    })
        
        return portas
    
    def testar_conexao(self):
        """Testa se RustScan funciona."""
        try:
            resultado = subprocess.run(["rustscan", "--version"], 
                                     capture_output=True, text=True)
            return resultado.returncode == 0
        except FileNotFoundError:
            self.logger.error("RustScan não encontrado")
            return False