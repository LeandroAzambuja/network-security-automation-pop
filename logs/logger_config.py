"""
Configuração do sistema de logs.
Hackers do Bem
"""

import logging
import sys

# Tentar importar colorlog, se não existir usar logging padrão
try:
    import colorlog
    COLORLOG_DISPONIVEL = True
except ImportError:
    COLORLOG_DISPONIVEL = False
    print("[AVISO] colorlog não instalado. Usando logging padrão.")

def setup_logger(nivel="INFO"):
    """Configura logger."""
    
    logger = logging.getLogger('automacao_hackers')
    
    # Configura nível do logger
    if isinstance(nivel, str):
        logger.setLevel(getattr(logging, nivel.upper()))
    else:
        logger.setLevel(logging.INFO)
    
    # Remove handlers existentes
    if logger.handlers:
        logger.handlers.clear()
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    
    if COLORLOG_DISPONIVEL:
        # Formato com cores
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    else:
        # Formato sem cores
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()
