"""Manage views."""
import json
from pathlib import Path
import tempfile

import cherrypy

from pisa.lis import lis_to_dict
from pisa.db import TmpDB
from views.manschaftsliste import make_manschaftsliste


class AppViews(object):
    """Handle/process views."""

    @cherrypy.expose
    def manschaftsliste(self, lis_upload):
        """Generate manschaftsliste."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            lis_file = Path(tmp_dir, 'data.lis')

            with lis_file.open('wb') as tmp_file:
                tmp_file.write(lis_upload.file.read())

            data = lis_to_dict(Path(lis_file))

            db = TmpDB()
            db.create(data['head'])
            db.insert(data['rows'])

            view_config = Path(
                Path(__file__).parents[1], "manschaftsliste.json")
            with view_config.open('r', encoding='utf-8') as js_file:
                config = json.loads(js_file.read())

            xlsx_liste = Path(tmp_dir, "liste.xlsx")
            make_manschaftsliste(xlsx_liste, db, config)

            xlsx_temp = tempfile.NamedTemporaryFile(suffix="xlsx")
            with xlsx_liste.open('rb') as tmp_list:
                xlsx_temp.write(tmp_list.read())

            xlsx_temp.seek(0)
            return cherrypy.lib.static.serve_fileobj(
                xlsx_temp, disposition='attachment',
                content_type=('application/vnd.openxmlformats-officedocument.'
                              'spreadsheetml.sheet'),
                name='manschaftsliste.xlsx'
            )
