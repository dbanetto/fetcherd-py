import logging

from glob import glob
from os import path
from fetcherd.source import Source


def get_sources(src_path=path.dirname(__file__)):
    sources = {}
    logger = logging.getLogger('fetcherd')

    # reflection time
    # Load all Base Providers in this directory
    for file in glob(src_path + '/*.py'):
        name = path.basename(file)

        # skip __init__.py
        if name in ['__init__.py', path.basename(__file__)]:
            continue

        # Get the module and class name
        # it is assumed that the class is the .title() of the file name
        file_name = name.split('.')[0]
        class_name = file_name.title().replace('_', '')
        # Load the class and store it with its class_name
        try:
            type = getattr(__import__(__name__ + '.' + file_name,
                                      fromlist=[class_name]),
                           class_name)
            if issubclass(type, Source):
                sources.update({file_name: type})
                logger.info('{} loaded as a source from {}/{}.py'
                            .format(class_name, src_path, file_name))
            else:
                logger.error('{} is not a sub-class of Source'.format(class_name))
        except:
            logger.error('Failed to load {1} from {0}'.format(file_name,
                                                              class_name))

    return sources
