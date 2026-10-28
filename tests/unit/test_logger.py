"""Testes unitários para o módulo utils/logger.py."""

import logging

from f1.utils.logger import configurar_logging, get_logger


def test_get_logger():
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_configurar_logging():
    configurar_logging("DEBUG")
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) >= 1

