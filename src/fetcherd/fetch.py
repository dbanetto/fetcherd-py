import logging
import html
import os

from fetcherd.util import get_path_regex

def fetch(config, source, base_providers):
    providers = {}
    logger = logging.getLogger('fetcherd')

    for prov in source.get_base_providers():
        if prov['name'] not in base_providers:
            logger.warning('Unsupported Base Provider : ' + prov['name'])
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
            logger.warning('Unsupported Base Provider \"' +
                           prov['base_provider'] +
                           "\" used by " +
                           prov['name'])

    for series in source.get_series():
        if series['provider_id'] in providers:
            logger.info("Fetching {}".format(html.unescape(series['title'])))
            provider = providers[series['provider_id']]
            current = series['current_count']

            for ep in provider.fetch(series):
                numb, link, title = ep
                current = max(numb, current)
                if numb > series['current_count']:
                    logger.info('Downloading {}'.format(title))
                    (dwn, name) = provider.download(link, config)
                    download(config, dwn, name)

            if current > series['current_count']:
                logging.info('Updating {} to episode count {}'
                             .format(series['title'], current))
                source.post_update_episode_count(series['id'], current)

        else:
            logger.warning("Unsupported provider id: {}"
                           .format(series['provider_id']))


def download(config, stream, filename):
    logger = logging.getLogger('fetcherd')
    path = get_path_regex(filename, config.fetch['save_paths'],
                          default=config.fetch['save_path_default'])
    logger.info("Downloading {} to {}".format(filename, path))
    with open(os.path.join(path, filename), 'wb') as f:
        for chunk in stream:
            if chunk:
                f.write(chunk)
                f.flush()
