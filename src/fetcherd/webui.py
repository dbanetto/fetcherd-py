from bottle import Bottle
import json

class WebUI:
    webui = Bottle()

    def __init__(self, args, config):
        self.args = args
        self.config = config

    def run(self):
        # defaults
        host = 'localhost'
        port = 8181

        if 'host' in self.config.webui and type(self.config.webui['host']) is str:
            host = self.config.webui['host']

        if 'port' in self.config.webui and self.config.webui['port'] is int:
            port = self.config.webui['port']

        self.webui.run(server='paste', host=host, port=port)

    @webui.get('/')
    def index():
        return "Web API is running"

    @webui.get('/status')
    def status():
        return {
            'running' : True,
        }

    @webui.post('/force/fetch')
    def force_fetch():
        pass

    @webui.post('/force/sort')
    def force_sort():
        pass


def run(args, config):
    WebUI(args, config).run()

