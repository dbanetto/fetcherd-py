import logging

from glob import glob
from os import path
from fetcherd.provider import Provider


def get_providers(src_path=path.dirname(__file__)):
    providers = {}
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
            if issubclass(type, Provider):
                providers.update({file_name: type})
                logger.info('{} loaded as a provider from {}/{}.py'
                            .format(class_name, src_path, file_name))
            else:
                logger.error('{} is not a sub-class of Provider'
                             .format(class_name))
        except:
            logging.error('Failed to load {1} from {0}'.format(file_name,
                                                               class_name))
    return providers
