import os
import getpass
import logging
from logging import handlers

from fetch import fetch
from sort import sort
import sources
import providers

from apscheduler.schedulers.background import BlockingScheduler

def main(args, config):
    file = handlers.RotatingFileHandler(
        args['--log'],
        maxBytes=10485760,
        encoding='utf8'
    )
    file.setLevel(logging.DEBUG)
    file.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    logging.getLogger('').addHandler(file)

    scheduler = BlockingScheduler(logger=logging.getLogger('schedule'))

    logger = logging.getLogger('daemon')
    logger.info("Entered main")

    working_dir = config.daemon['working_dir'] if 'working_dir' in config.daemon else '/tmp'

    os.chdir(working_dir)
    logger.info("Working directory: {}".format(working_dir))
    logger.info("Running as user {}".format(getpass.getuser()))

    provs = providers.get_providers()
    loaded_sources = sources.get_sources()
    current_souce = loaded_sources[config.source['class']](config.source['settings'])

    scheduler.add_job(lambda: fetch(config, current_souce, provs),
                      'cron', minute=30, id='fetch')
    scheduler.add_job(lambda: sort(config, current_souce),
                      'cron', minute=00, id='sort')

    fetch(config, current_souce, provs)
    sort(config, current_souce)

    scheduler.start()
