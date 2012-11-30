"""
Entry point - read environment and set up logging

Follows principles of twelve-factor app - all input data is
obtained from environment

"""
from logging import getLogger
import os

from . import about
from .logger import set_logger
from .rest import entry as rest_entry

LOGGER = getLogger(__name__)


def main():
    """
    Setup logger and read command line
    """
    set_logger(
        os.environ.get('LNXPROC_LOGLEVEL', 'CRITICAL'),
    )

    LOGGER.debug("Start V%s", about.__version__)

    LOGGER.debug("environ %s", os.environ)

    root = os.environ.get('LNXPROC_ROOT')
    LOGGER.debug("root %s", root)

    port = os.environ.get('LNXPROC_PORT')
    if port is not None:
        port = int(port)

    LOGGER.debug("port %s", port)

    rest_entry(
        root=root,
        port=port,
    )
