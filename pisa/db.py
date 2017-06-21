"""A in memory database handle for temporary transform."""
from datetime import datetime
import logging
import sqlite3

from .sql_functions import sql_order_grad

_LOGGER = logging.getLogger(__name__)

MAP_FIELD_TO_TYPE = {
    'geburtsdatum': 'DATETIME',
    'brevetdatum': 'DATETIME',
    'plz': 'INTEGER',
    'geleistete_tage': 'INTEGER',
}

DEFAULT_TYPE = 'TEXT'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class TmpDB(object):
    """Handle a in memory database."""

    def __init__(self, filename=":memory:"):
        """Initialize in memory database."""
        self._head = None

        self._con = sqlite3.connect(str(filename))
        self._con.row_factory = dict_factory

        # add sql functions
        self._con.create_function('SortGrad', 1, sql_order_grad)

    def close(self):
        """Destroy temporary database."""
        self._con.close()

    def create(self, head):
        """Create table from head data."""
        self._head = head
        fields = []

        for field in head:
            fields.append("{0} {1}".format(
                field, MAP_FIELD_TO_TYPE.get(field, DEFAULT_TYPE)
            ))

        self._con.execute("CREATE TABLE data({0})".format(", ".join(fields)))
        self._con.commit()

    def insert(self, data):
        """Insert data into table."""
        val_count = ['?' for _ in range(0, len(self._head))]

        self._con.executemany(
            "INSERT INTO data({0}) VALUES ({1})".format(
                ", ".join(self._head), ", ".join(val_count)
            ), data)
        self._con.commit()

    def fetch(self, where=None, order=None):
        """Fetch data with db."""
        cmd = ["SELECT * FROM data"]

        if where:
            cmd.append("WHERE {0}".format(where))

        if order:
            cmd.append("ORDER BY {0}".format(order))

        curs = self._con.cursor()
        curs.execute(" ".join(cmd))
        data = curs.fetchall()

        # convert types
        for row in data:
            for cell, db_type in MAP_FIELD_TO_TYPE.items():
                if db_type == 'DATETIME':
                    row[cell] = datetime.strptime(row[cell], '%Y-%m-%d')
                elif db_type == 'INTEGER':
                    row[cell] = int(row[cell])

        return data
