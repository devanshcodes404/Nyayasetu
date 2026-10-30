"""
Structured application logging setup.
Prevents leaking sensitive data, tokens, or raw document content.
"""
import logging
import sys


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("nyayasetu")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = setup_logging()

