"""Module to read a LIS file."""
import logging

_LOGGER = logging.getLogger(__name__)


def lis_to_dict(lis_file):
    """Convert a LIS into a dict.

        Return a list with dict:
        {
            "head": [],
            "rows": [(), ()]
        }
    """
    data = []

    try:
        with lis_file.open('r') as input_data:
            lines = input_data.readlines()

    except OSError as err:
        _LOGGER.error("Error while read %s: %s", lis_file, err)
        return []

    head = ((lines.pop(0).lower()).replace(" ", "_")).split(';')

    # loop trought list
    rows = list()
    for line in lines:
        rows.append(cell for cell in line.split(';'))

    # set data
    data['head'] = head
    data['rows'] = rows

    return data
