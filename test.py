from pathlib import Path
import json

from pisa.lis import lis_to_dict
from pisa.db import TmpDB
from views.manschaftsliste import make_manschaftsliste

data = lis_to_dict(Path("D:\\test\\aw.lis"))

db = TmpDB()
db.create(data['head'])
db.insert(data['rows'])

view_config = Path("manschaftsliste.json")
with view_config.open('r', encoding='utf-8') as js_file:
    config = json.loads(js_file.read())

make_manschaftsliste(Path("test.xlsx"), db, config)
