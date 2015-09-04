"""fetcherd

Usage:
    fetcherd (-h | --help)
    fetcherd --version
    fetcherd [-d | --daemon] [-c <path> | --config=<config>] [--log=<path>] [--verbose]
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
from fetcherd.fetcherd import Fetcherd

from daemonize import Daemonize
import logging
import logging.config

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

def daemonize(fetcher, args, config):
    logger = logging.getLogger('daemon')
    pid = config.daemon['pid'] if 'pid' in config.daemon else '/tmp/fetcherd.pid'
    user = config.daemon['user'] if 'user' in config.daemon else None
    group = config.daemon['group'] if 'group' in config.daemon else None

    daemon = Daemonize("fetcherd",
                       pid,
                       daemon_setup,
                       privileged_action=lambda: [fetcher, args, config],
                       user=user,
                       group=group,
                       )
    try:
        logger.info("Forked")
        daemon.start()
    except Exception as e:
        logger.critical("Error during daemonize: {}".format(e))


def daemon_setup(fetcher, args, config):
    file = handlers.RotatingFileHandler(
        args['--log'],
        maxBytes=10485760,
        encoding='utf8'
    )
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    logger = logging.getLogger('daemon')
    logger.addHandler(file)
    logging.getLogger('').addHandler(file)

    logger.debug("Setup log file in {}".format(args['--log']))

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

    if args['--daemon']:
        daemonize(Fetcher, args, config)
    elif args['--dump-providers']:
        import json
        for (key, prov) in Fetcher.providers.items():
            print(key, json.dumps(prov.get_options_schema()))
        exit(0)

    logger.debug("Start with args {}".format(args))

    if args['--fetch']:
        Fetcher.fetch()
    elif args['--sort']:
        Fetcher.sort()
    else:
        Fetcher.start()

if __name__ == '__main__':
    main()
