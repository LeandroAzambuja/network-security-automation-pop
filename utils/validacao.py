"""
Validação de alvos e configurações.
Hackers do Bem
"""

import re
import ipaddress
from typing import List, Union

def validar_ip(ip: str) -> bool:
    """Valida se é um IP válido."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validar_hostname(hostname: str) -> bool:
    """Valida se é um hostname válido."""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, hostname))

def validar_cidr(cidr: str) -> bool:
    """Valida se é uma rede CIDR válida."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False

def processar_alvos(entrada: str, tipo: str) -> List[str]:
    """
    Processa diferentes tipos de entrada de alvos.
    
    Args:
        entrada: String com alvo(s)
        tipo: 'ip', 'arquivo', ou 'cidr'
    
    Returns:
        Lista de alvos válidos
    """
    alvos = []
    
    if tipo == 'ip':
        # Alvo único (IP ou hostname)
        if validar_ip(entrada) or validar_hostname(entrada):
            alvos.append(entrada)
    
    elif tipo == 'arquivo':
        # Arquivo com lista de alvos
        try:
            with open(entrada, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        if validar_ip(linha) or validar_hostname(linha):
                            alvos.append(linha)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {entrada}")
    
    elif tipo == 'cidr':
        # Rede CIDR - expande para lista de IPs
        try:
            rede = ipaddress.ip_network(entrada, strict=False)
            # Limita a 256 IPs para não explodir
            for ip in list(rede.hosts())[:256]:
                alvos.append(str(ip))
        except ValueError:
            print(f"CIDR inválido: {entrada}")
    
    return alvos

def validar_configuracao(caminho_config: str) -> dict:
    """
    Valida e carrega configuração do arquivo YAML.
    
    Args:
        caminho_config: Caminho para arquivo config.yaml
    
    Returns:
        Dicionário com configuração
    """
    config_padrao = {
        "configuracao": {
            "tipo_scan": "rapido",
            "timeout": 30,
            "threads": 100,
            "portas_rapidas": "20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443"
        }
    }
    
    try:
        import yaml
        with open(caminho_config, 'r') as f:
            config = yaml.safe_load(f)
        
        # Mescla com padrão se faltar alguma chave
        if "configuracao" not in config:
            config["configuracao"] = config_padrao["configuracao"]
        else:
            for chave, valor in config_padrao["configuracao"].items():
                if chave not in config["configuracao"]:
                    config["configuracao"][chave] = valor
        
        return config
        
    except FileNotFoundError:
        print(f"Arquivo de configuração não encontrado: {caminho_config}")
        return config_padrao
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return config_padrao