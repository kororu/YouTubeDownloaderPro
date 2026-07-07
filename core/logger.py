"""Application logging configuration."""

from __future__ import annotations

import logging
from logging import Formatter, Logger, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.paths import AppPaths, get_app_paths

LOGGER_NAME: str = "youtube_downloader_pro"
LOG_FILE_NAME: str = "application.log"
LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
MAX_LOG_BYTES: int = 1_000_000
BACKUP_COUNT: int = 5


def configure_logging(level: int = logging.INFO, app_paths: AppPaths | None = None) -> Logger:
    """Configure application logging.

    Args:
        level: Minimum logging level.
        app_paths: Optional resolved application paths.

    Returns:
        Configured application logger.
    """
    logger: Logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    paths: AppPaths = app_paths or get_app_paths()
    paths.logs_dir.mkdir(parents=True, exist_ok=True)

    formatter: Formatter = Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    console_handler: StreamHandler[str] = StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler: RotatingFileHandler = RotatingFileHandler(
        filename=Path(paths.logs_dir / LOG_FILE_NAME),
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger() -> Logger:
    """Return the application logger.

    Returns:
        Configured or existing application logger.
    """
    logger: Logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        return configure_logging()
    return logger
