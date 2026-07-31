"""Central logging configuration for the automation framework."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "framework.log"
DEFAULT_LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _ensure_log_file() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)


def _build_formatter() -> logging.Formatter:
    return logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)


def _build_console_handler(level: int) -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(_build_formatter())
    return console_handler


def _build_file_handler(level: int) -> logging.FileHandler:
    _ensure_log_file()
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(_build_formatter())
    return file_handler


def get_logger(name: str = "automation", level: int = DEFAULT_LOG_LEVEL) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_build_console_handler(level))
        logger.addHandler(_build_file_handler(logging.DEBUG))

    return logger
