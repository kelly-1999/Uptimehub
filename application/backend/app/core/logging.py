import logging
import sys

from app.core.config import settings


LOG_FORMAT = (
    "%(asctime)s "
    "%(levelname)s "
    "%(name)s "
    "%(message)s"
)


def configure_logging() -> None:
    log_level = logging.DEBUG if settings.debug else logging.INFO

    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )
