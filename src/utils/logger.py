"""Logging setup."""
import logging
import os


def setup_logger(log_file, level="INFO"):
    """Create a logger that writes to a file and to the console."""
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    logger = logging.getLogger("student_system")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if logger.handlers:
        return logger
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
