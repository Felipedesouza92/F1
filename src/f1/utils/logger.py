"""Logger padrão do projeto F1 Dashboard."""

import logging
import sys

FORMATO = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Retorna o logger do módulo `name`, sem configurar handlers."""
    return logging.getLogger(name)


def configurar_logging(nivel: str = "INFO") -> None:
    """Configura o handler único da aplicação. Chamar apenas no ponto de entrada."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=FORMATO, datefmt=FORMATO_DATA))
    raiz = logging.getLogger()
    raiz.handlers[:] = [handler]
    raiz.setLevel(nivel)
