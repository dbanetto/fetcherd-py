import os
import getpass
import logging
from logging import handlers

def daemon(args, config):
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

    working_dir = config.daemon['working_dir'] if 'working_dir' in config.daemon else '/tmp'

    os.chdir(working_dir)
    logger.info("Working directory: {}".format(working_dir))
    logger.info("Running as user {}".format(getpass.getuser()))

    runner.start(args, config)
