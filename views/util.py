"""Utils for work with excel."""


def write_head(workbook, sheet, config):
    """Write header to excel."""
    if 'head_style' in config:
        form = workbook.add_format(config['head_style'])
    else:
        form = workbook.add_format()

    for idx, data in enumerate(config['head']):
        sheet.write(0, idx, data['cell'], form)

    # generate head / styles
    head_style = {}
    for row in config['head']:
        if 'format' in row:
            form_cell = workbook.add_format(row['format'])
        else:
            form_cell = workbook.add_format()

        head_style[row['link']] = form_cell

    return head_style


def write_group_head(workbook, sheet, group, size, row):
    """Write header to excel."""
    if 'format' in group:
        form = workbook.add_format(group['format'])
    else:
        form = workbook.add_format()

    sheet.merge_range(row, 0, row, size, group['cell'], form)
