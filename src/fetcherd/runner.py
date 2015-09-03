import os
import getpass
import logging
from logging import handlers

from fetcherd.fetch import fetch
from fetcherd.sort import sort
from fetcherd.util import load_source, load_providers

from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler

def start(args, config):
    if config.webui['enable']:
        scheduler = BackgroundScheduler(logger=logging.getLogger('schedule'))
        logging.info("Using Background Scheduler")
    else:
        scheduler = BlockingScheduler(logger=logging.getLogger('schedule'))
        logging.info("Using Blocking Scheduler")

    provs = load_providers(config.providers['modules_path'])

    loaded_source = load_source(config.source['modules_path'],
                                config.source['class'])
    current_souce = loaded_source(config.source['settings'])

    scheduler.add_job(lambda: fetch(config, current_souce, provs),
                      'cron', minute=30, id='fetch')
    scheduler.add_job(lambda: sort(config, current_souce),
                      'cron', minute=00, id='sort')

    # run once at launch
    fetch(config, current_souce, provs)
    sort(config, current_souce)

    scheduler.start()

    if config.webui['enable']:
        from fetcherd import webui
        webui.run(args, config)
