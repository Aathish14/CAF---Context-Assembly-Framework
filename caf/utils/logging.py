"""
Application logging configuration.
"""

import logging
import logging.handlers
import sys
from pathlib import Path

from caf.config import settings


def setup_logging(
    name: str | None = None,
    log_level: str | None = None,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> logging.Logger:
    """Set up and configure a logger.

    Args:
        name: Logger name. If None, returns root logger.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  If None, uses setting from config.
        log_to_file: Whether to log to file.
        log_to_console: Whether to log to console.

    Returns:
        Configured logger instance.
    """
    # Get logger
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Determine log level
    if log_level is None:
        log_level = getattr(settings, "LOG_LEVEL", "INFO")

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logger.setLevel(numeric_level)

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_to_file:
        # Ensure logs directory exists
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Rotating file handler (10 MB per file, keep 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{name or 'app'}.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent duplicate logs if propagating to root
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.

    This is the preferred way to get loggers throughout the application.

    Args:
        name: Usually __name__ from the calling module.

    Returns:
        Configured logger instance.
    """
    return setup_logging(name)


# Configure root logger for early startup messages
root_logger = setup_logging(log_to_file=False)  # Console only for root initially

# Export for convenience
__all__ = ["setup_logging", "get_logger"]
