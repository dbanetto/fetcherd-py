import logging
import os
import shutil
from os import path
from util import get_path


def sort(config, source):
    logger = logging.getLogger('sort')

    for series in source.get_series():
        logger.info('Sorting {}'.format(series['title']))
        base_save_path = get_path(series['media_type'],
                                  config.sort['save_paths'],
                                  default=config.sort['save_path_default'])
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

        for search_path in config.sort['search_paths']:
            logger.info("Searching in {}".format(search_path))

            for root, dirs, files in os.walk(search_path):
                for f in files:
                    if search_title in f:
                        os.makedirs(save_path, exist_ok=True)
                        if not path.isfile(path.join(save_path, f)):
                            logger.info('Found {}'.format(f))
                            if 'providers_to_move' in config.sort and \
                               series['provider'] in config.sort['providers_to_move']:
                                shutil.move(path.join(root, f), save_path)
                                op = 'Moving '
                            else:
                                shutil.copy(path.join(root, f), save_path)
                                op = 'Copying'

                            logger.info('{} {} to {}'.format(op, f, save_path))
