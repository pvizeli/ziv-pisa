"""A in memory database handle for temporary transform."""
import logging
import sqlite3

_LOGGER = logging.getLogger(__name__)


class TmpDB(object):
    """Handle a in memory database."""

    def __init__(self):
        """Initialize in memory database."""
        self._con = sqlite3.connect(":memory:")

    def close(self):
        """Destroy temporary database."""
        self._con.close()
