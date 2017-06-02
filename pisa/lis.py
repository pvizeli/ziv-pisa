"""Module to read a LIS file."""
import logging
import re

_LOGGER = logging.getLogger(__name__)

RE_SCORE = re.compile(r"( |-)")
RE_SLUGIFY = re.compile(r"[^\w0-9;]+")
RE_DATE = re.compile(r"(\d{2,2})\.(\d{2,2})\.(\d{4,4})")


def lis_to_dict(lis_file):
    """Convert a LIS into a dict.

        Return a list with dict:
        {
            "head": [],
            "rows": [(), ()]
        }
    """
    data = {}

    try:
        with lis_file.open('r', encoding='utf-8') as input_data:
            lines = input_data.readlines()

    except OSError as err:
        _LOGGER.error("Error while read %s: %s", lis_file, err)
        return []

    # create head names
    head = lines.pop(0).lower()
    head = RE_SCORE.sub("_", head)
    head = RE_SLUGIFY.sub("", head)
    head = head.split(';')[0:-1]

    # remove dublicate
    cleanup = []
    for cell in head:
        if cell in cleanup:
            for i in range(1, 20):
                cell = "{0}_{1}".format(cell, i)
                if cell not in cleanup:
                    break

        cleanup.append(cell)

    data['head'] = cleanup

    # loop trought list
    rows = list()
    for line in lines:
        rows.append(RE_DATE.sub(r"\3-\2-\1", line).split(';')[0:-1])

    # set data
    data['rows'] = rows

    return data
