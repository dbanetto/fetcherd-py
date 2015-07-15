"""fetcherd

Usage:
    fetcherd (-h | --help)
    fetcherd --version
    fetcherd (-d | --daemon) [-c <path> | --config=<config>] [--log=<path>] [--verbose]
    fetcherd [--fetch | --sort] [-c <path> | --config=<config>]
    fetcherd --dump-providers [-c <path> | --config=<config>]

Options:
    -h --help                   Show this screen
    --version                   Show version
    -d --daemon                 Run as daemon
    -c <path> --config=<path>   Config path [default: config.json]
    --log=<path>                Path to save log [default: fetcherd.log]
    --verbose                   Raise log level
    --fetch                     Run fetch
    --sort                      Run sort
    --push-providers            Prints provider schema
"""
from docopt import docopt

from settings import Settings
from fetch import fetch
from sort import sort
import sources
import providers

from logging import handlers
import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
        'full': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
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


def init():
    pass


def main():
    pass


def daemonize(args, config):
    import os
    file = handlers.RotatingFileHandler(
        args['--log'],
        maxBytes=10485760,
        encoding='utf8'
    )
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    logging.getLogger('').addHandler(file)

    logger = logging.getLogger('daemon')

    pid = config.daemon['pid'] if 'pid' in config.daemon else '/tmp/fetcherd.pid'

    working_dir = config.daemon['working_dir'] if 'working_dir' in config.daemon else '/tmp'

    logger.info("change dir to {}".format(working_dir))
    os.chdir(working_dir)


if __name__ == '__main__':
    args = docopt(__doc__, version='fetcherd 0.1')
    config = Settings(args['--config'])

    loaded_sources = sources.get_sources()
    current_souce = loaded_sources[config.source['class']](config.source['settings'])

    logging.debug("Loaded Source {}".format(config.source['class']))
    logging.debug("Args {}".format(args))

    if args['--daemon']:
        daemonize(args, config)
    elif args['--fetch']:
        fetch(config, current_souce,
              providers.get_providers())
    elif args['--sort']:
        sort(config, current_souce)
    elif args['--dump-providers']:
        import json
        for (key, prov) in providers.get_providers().items():
            print(key, json.dumps(prov.get_options_schema()))
