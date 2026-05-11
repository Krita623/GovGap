from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a project logger."""

    return logging.getLogger(name)

