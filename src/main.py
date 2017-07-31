"""fetcherd

Usage:
    fetcherd (-h | --help)
    fetcherd --version
    fetcherd [-c <path> | --config=<config>]
    fetcherd [--fetch | --sort] [-c <path> | --config=<config>]
    fetcherd --dump-providers [-c <path> | --config=<config>]

Options:
    -h --help                   Show this screen
    --version                   Show version
    -c <path> --config=<path>   Config path 
    --fetch                     Run fetch
    --sort                      Run sort
    --push-providers            Prints provider schema
"""
from docopt import docopt

from fetcherd.settings import Settings
from fetcherd.fetcherd import Fetcherd

import logging
import os
import logging.config
import getpass
from logging import handlers

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '[%(name)s] %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'formatter': 'simple',
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
})

def run(fetcher, args, config):
    log_path = config.daemon['log'] if 'log' in config.daemon else 'fetcherd.log'
    config.daemon['log'] = log_path
    file = handlers.RotatingFileHandler(
        log_path,
        maxBytes= 4 * 1024 * 1024,
        encoding='utf8'
    )
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    logger = logging.getLogger('daemon')
    logger.addHandler(file)
    logging.getLogger('').addHandler(file)

    logger.debug("Setup log file in {}".format(log_path))

    working_dir = config.daemon['working_dir'] if 'working_dir' in config.daemon else '/tmp'

    os.chdir(working_dir)
    logger.info("Working directory: {}".format(working_dir))
    logger.info("Running as user {}".format(getpass.getuser()))

    fetcher.start()


def main():
    args = docopt(__doc__, version='fetcherd 0.1')
    config = Settings(args['--config'])
    logger = logging.getLogger('setup')

    Fetcher = Fetcherd(args, config)

    logger.debug("Start with args {}".format(args))

    if args['--dump-providers']:
        import json
        for (key, prov) in Fetcher.providers.items():
            print(key, json.dumps(prov.get_options_schema()))
        exit(0)
    elif args['--fetch']:
        Fetcher.fetch()
    elif args['--sort']:
        Fetcher.sort()
    else:
        run(Fetcher, args, config)

if __name__ == '__main__':
    main()
