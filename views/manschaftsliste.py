"""Create a excel for Manschaftliste."""
import logging

import xlsxwriter

from .util import init_document, write_head, write_group_head

_LOGGER = logging.getLogger(__name__)


def make_manschaftsliste(filename, db, config):
    """Write manschaftsliste to excel."""
    workbook = xlsxwriter.Workbook(str(filename))
    sheet = workbook.add_worksheet()
    head = [row['link'] for row in config['head']]

    # document settings
    if 'document' in config:
        init_document(sheet, config['document'])

    # head
    head_style = write_head(workbook, sheet, config)

    row = 1
    for group in config['group']:
        # write group
        write_group_head(workbook, sheet, group, len(head) - 1, row)
        row += 1

        # write members of group
        members = db.fetch(group.get('select'), group.get('sort'))
        for man in members:
            for idx, cell in enumerate(head):
                sheet.write(row, idx, man[cell], head_style[cell])
            row += 1

    workbook.close()
