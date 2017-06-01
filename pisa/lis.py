"""Module to read a LIS file."""
import logging

_LOGGER = logging.getLogger(__name__)


def lis_to_dict(lis_file):
    """Convert a LIS into a dict.

        Return a list with dict:
        [
            {"cell": "dat", ...}  // row
        ]
    """
    result = []

    try:
        with lis_file.open('r') as input_data:
            lines = input_data.readlines()

    except OSError as err:
        _LOGGER.error("Error while read %s: %s", lis_file, err)
        return []

    head = (lines.pop(0).lower()).split(';')

    # loop trought list
    for line in lines:
        line = line.split(';')

        # cells
        row = {}
        for i in range(0, len(head)):
            row[head[i]] = line[i]

        # done
        result.append(row)

    return result