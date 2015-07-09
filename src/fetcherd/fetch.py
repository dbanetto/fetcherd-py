import logging
import html


def fetch(config, source, base_providers):
    providers = {}
    logger = logging.getLogger('fetcherd')

    for prov in source.get_base_providers():
        if prov['name'] not in base_providers:
            logger.info('Unsupported Base Provider : ' + prov['name'])
        else:
            logger.info('Loaded', prov['name'])

    for prov in source.get_providers():
        if prov['base_provider'] in base_providers:
            providers.update({prov['id']:
                              base_providers[prov['base_provider']](prov)})
            logger.info('Loaded', prov['name'],
                        'with options',
                        prov['base_provider_options'])
        else:
            logger.warning('Unsupported Base Provider \"' +
                           prov['base_provider'] +
                           "\" used by " +
                           prov['name'])

    for series in source.get_series():
        if series['provider_id'] in providers:
            logger.info("Fetching", html.unescape(series['title']))
            provider = providers[series['provider_id']]

            for ep in provider.fetch(series):
                numb, link, title = ep
                logger.info('Downloading', title)
                provider.download(link, config)
                logging.info('Updating', title, 'to episode count', numb)
                source.post_update_episode_count(series['id'], numb)

        else:
            logger.warning("Unsupported provider id: {}".format(series['provider_id']))
