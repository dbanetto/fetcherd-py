from bottle import Bottle


class WebUI(Bottle):

    def __init__(self, fetcher, config):
        super(WebUI, self).__init__()
        self.fetcher = fetcher
        self.config = config
        self._route()

    def _route(self):
        # Double ups to support both trailing and non-trailing slashes
        # GET
        self.get('/', callback=self.index)
        self.get('/status', callback=self.status)
        self.get('/status/', callback=self.status)
        self.get('/dump_provider_options', callback=self.dump_providers)
        self.get('/dump_provider_options/', callback=self.dump_providers)

        # POSTs
        self.post('/force/fetch', callback=self.force_fetch)
        self.post('/force/fetch/', callback=self.force_fetch)
        self.post('/force/sort', callback=self.force_sort)
        self.post('/force/sort/', callback=self.force_sort)

    def run(self):
        # defaults
        host = 'localhost'
        port = 8181
        server = 'paste'

        if 'host' in self.config.webui and type(self.config.webui['host']) is str:
            host = self.config.webui['host']

        if 'port' in self.config.webui and self.config.webui['port'] is int:
            port = self.config.webui['port']

        if 'server' in self.config.webui and self.config.webui['server'] is str:
            server = self.config.webui['server']

        super(WebUI, self).run(host=host, port=port, server=server)

    def index(self):
        return "Web API is running"

    def status(self):
        return {
            'running': True,
            'fetch_lock': self.fetcher.fetch_lock,
            'sort_lock': self.fetcher.sort_lock
        }

    def force_fetch(self):
        try:
            self.fetcher.fetch()
            return {
                'success': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': '{}'.format(str(e))
            }

    def force_sort(self):
        try:
            self.fetcher.sort()
            return {
                'success': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': '{}'.format(str(e))
            }

    def dump_providers(self):
        options = {}
        for (key, prov) in self.fetcher.providers.items():
            options[key] = prov.get_options_schema()
        return options
