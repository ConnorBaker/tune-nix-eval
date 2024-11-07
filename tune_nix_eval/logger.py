import logging

import rich.logging

LOGGING_LEVEL = logging.INFO

CONSOLE = rich.console.Console(
    color_system=None,
    emoji=False,
    highlight=False,
    markup=False,
    stderr=True,
)
HANDLER = rich.logging.RichHandler(
    console=CONSOLE,
    rich_tracebacks=True,
    show_time=False,
)
HANDLER.setFormatter(logging.Formatter("%(message)s"))


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(HANDLER)

    return logger
