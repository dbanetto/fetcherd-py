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
    -c <path> --config=<path>   Config path [default: /etc/fetcherd/config.json]
    --log=<path>                Path to save log [default: /tmp/fetcherd.log]
    --verbose                   Raise log level
    --fetch                     Run fetch
    --sort                      Run sort
    --push-providers            Prints provider schema
"""
from docopt import docopt

from fetcherd.settings import Settings
from fetcherd.fetch import fetch
from fetcherd.sort import sort
from fetcherd.util import load_source, load_providers

from daemonize import Daemonize
import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s'
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
            'level': 'WARN',
            'propagate': True
        }
    }
})


def daemonize(args, config):
    from fetcherd.daemon import main
    logger = logging.getLogger('daemon')
    pid = config.daemon['pid'] if 'pid' in config.daemon else '/tmp/fetcherd.pid'
    user = config.daemon['user'] if 'user' in config.daemon else None
    group = config.daemon['group'] if 'group' in config.daemon else None

    daemon = Daemonize("fetcherd",
                       pid,
                       main,
                       privileged_action=lambda: [args, config],
                       user=user,
                       group=group,
                       )
    try:
        daemon.start()
    except Exception as e:
        logger.critical("Error during daemonize: {}".format(e))


def main():
    args = docopt(__doc__, version='fetcherd 0.1')
    config = Settings(args['--config'])
    logger = logging.getLogger('setup')

    if args['--daemon']:
        daemonize(args, config)
    elif args['--dump-providers']:
        import json
        for (key, prov) in load_providers(config.providers['modules_path']).items():
            print(key, json.dumps(prov.get_options_schema()))
        exit()

    logger.debug("Start with args {}".format(args))

    loaded_source = load_source(config.source['modules_path'], config.source['class'])
    current_souce = loaded_source(config.source['settings'])

    logger.debug("Loaded Source {}".format(config.source['class']))

    if args['--fetch']:
        fetch(config, current_souce,
              load_providers(config.providers['modules_path']))
    elif args['--sort']:
        sort(config, current_souce)

if __name__ == '__main__':
    main()
