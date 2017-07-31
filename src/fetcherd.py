import logging
import os
import shutil
import html
from os import path

from fetcherd.settings import Settings
from fetcherd.util import get_path, get_path_regex, load_source, load_providers

class Fetcherd:

    def __init__(self, args, config):
        self.logger = logging.getLogger('fetcherd')
        self.args = args
        self.config = config
        self.fetch_lock = False
        self.sort_lock = False

        loaded_source = load_source(config.source['modules_path'],
                                    config.source['class'])
        self.source = loaded_source(config.source['settings'])
        self.logger.info("Current source {}"
                         .format(self.config.source['class']))

        self.providers = load_providers(self.config.providers['modules_path'])

    def sort(self, source=None):
        if source is None:
            source = self.source

        logger = logging.getLogger('sort')

        if self.sort_lock:
            raise Exception("Sort is already in use")

        try:
            self.sort_lock = True

            for series in source.get_series():
                logger.info('Sorting {}'.format(series['title']))
                base_save_path = get_path(series['media_type'],
                                          self.config.sort['save_paths'],
                                          default=self.config.sort['save_path_default'])

                os.makedirs(base_save_path, exist_ok=True)

                search_title = series['title']
                if 'search_title' in series:
                    if series['search_title'] != '':
                        search_title = series['search_title']

                save_path = series['title']
                if 'save_path' in series:
                    if series['save_path'] != '':
                        save_path = series['save_path']

                save_path = path.join(base_save_path,
                                      save_path)

                for search_path in self.config.sort['search_paths']:
                    logger.info("Searching in {}".format(search_path))

                    for root, dirs, files in os.walk(search_path):
                        for f in files:
                            if search_title in f:
                                os.makedirs(save_path, exist_ok=True)
                                if not path.isfile(path.join(save_path, f)):
                                    logger.info('Found {}'.format(f))

                                    if 'providers_to_move' in self.config.sort \
                                       and series['provider'] in self.config.sort['providers_to_move']:
                                        shutil.move(path.join(root, f), save_path)
                                        op = 'Moving '
                                    else:
                                        shutil.copy(path.join(root, f), save_path)
                                        op = 'Copying'

                                    logger.info('{} {} to {}'
                                                .format(op, f, save_path))

        except Exception as e:
            logging.error('Error: {}'.format(str(e)))
        finally:
            self.sort_lock = False

    def fetch(self, source=None, base_providers=None):
        if source is None:
            source = self.source

        if base_providers is None:
            base_providers = self.providers

        if self.fetch_lock:
            raise Exception("Fetch is already in use")

        try:
            self.fetch_lock = True
            providers = {}
            logger = logging.getLogger('fetcher')

            for prov in source.get_base_providers():
                if prov['name'] not in base_providers:
                    logger.warning('Unsupported Base Provider: {0}'.format(prov['name'])) 
                else:
                    logger.info('Loaded {}'.format(prov['name']))

            for prov in source.get_providers():
                if prov['base_provider'] in base_providers:
                    providers.update({prov['id']:
                                      base_providers[prov['base_provider']](prov)})
                    logger.info('Loaded {} with options {}'
                                .format(prov['name'],
                                        prov['base_provider_options']))
                else:
                    logger.warning('Unsupported Base Provider \"{0}\" used by {1}'
                                    .format(prov['base_provider'], prov['name']))

            for series in source.get_series():
                if series['provider_id'] in providers:
                    logger.info("Fetching {}"
                                .format(html.unescape(series['title'])))
                    provider = providers[series['provider_id']]
                    current = series['current_count']

                    for ep in provider.fetch(series):
                        numb, link, title = ep
                        current = max(numb, current)
                        if numb > series['current_count']:
                            logger.info('Downloading {}'.format(title))
                            (dwn, name) = provider.download(link, self.config)
                            self.download(dwn, name)

                    if current > series['current_count']:
                        logging.info('Updating {} to episode count {}'
                                     .format(series['title'], current))
                        source.post_update_episode_count(series['id'], current)

                else:
                    logger.warning("Unsupported provider id: {}"
                                   .format(series['provider_id']))
        except Exception as e:
            logging.error('Error: {}'.format(str(e)))
        finally:
            self.fetch_lock = False

    def download(self, stream, filename):
        logger = logging.getLogger('downloads')
        path = get_path_regex(filename, self.config.fetch['save_paths'],
                              default=self.config.fetch['save_path_default'])

        logger.info("Downloading {} to {}".format(filename, path))

        with open(os.path.join(path, filename), 'wb') as f:
            for chunk in stream:
                if chunk:
                    f.write(chunk)
                    f.flush()

    def start(self):
        if self.config.webui['enable']:
            logging.debug("Setting up WebUI")
            from fetcherd.webui import WebUI
            self.webui = WebUI(self, self.config)
            logging.debug("Starting WebUI")
            self.webui.run()

    def reload_providers(self):
        self.logger.info("Reloading proivders")
        self.providers = load_providers(self.config.providers['modules_path'])

    def reload_source(self):
        self.logger.info("Reloading source")

        loaded_source = load_source(self.config.source['modules_path'],
                                    self.config.source['class'])
        self.source = loaded_source(self.config.source['settings'])
        self.logger.info("Current source {}"
                         .format(self.config.source['class']))

    def reload_config(self):
        self.logger.info("Reloading config")

        self.config = Settings(self.args['--config'])
