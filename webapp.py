"""Webapp for ziv-pisa."""
from pathlib import Path

from web.views import AppViews

import cherrypy

WEB_PORT = 9293


class ZivPisaApp(object):

    @cherrypy.expose
    def index(self):
        """Return index."""
        index_file = Path(Path(__file__).parent, "web", "index.html")
        with index_file.open("r") as index:
            return index.read()


cherrypy.tree.mount(ZivPisaApp(), '/')
cherrypy.tree.mount(AppViews(), '/views')

cherrypy.config.update({
    'global': {
        'tools.log_tracebacks.on': True,
        'engine.autoreload.on': True,
        'server.socket_port': WEB_PORT,
        'server.socket_host': '0.0.0.0'
    }
})

cherrypy.engine.start()
cherrypy.engine.block()
