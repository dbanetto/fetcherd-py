import re
import logging
import pkgutil
import imp

from os import path
from fetcherd.provider import Provider
from fetcherd.source import Source


def get_path(name, folders, default=None):
    for (k, v) in folders.items():
        if k == name.lower():
            return v
    return default


def get_path_regex(name, folders, default=None):
    for (k, v) in folders.items():
        if re.match(k, name.lower()):
            return v
    return default


def load_providers(src_path, blacklist=None, whitelist=None):
    return load_modules(src_path,
                        parent_type=Provider,
                        blacklist=None, whitelist=None)


def load_source(src_path, current):
    return load_modules(src_path,
                        parent_type=Source,
                        whitelist=[current])[current]


def load_modules(src_path, parent_type=object, whitelist=None, blacklist=None):
    loaded = {}
    logger = logging.getLogger('fetcherd')

    if not blacklist:
        blacklist = []
    blacklist = blacklist + ['__init__']

    # reflection time
    # Load all Base Providers in this directory
    modules = pkgutil.iter_modules(path=[src_path])

    for loader, mod_name, ispkg in modules:
        # Get the module and class name
        # it is assumed that the class is the .title() of the file name
        class_name = mod_name.title().replace('_', '')

        if mod_name in blacklist:
            logger.debug('Blacklisted: {}'.format(class_name))
            continue

        if whitelist:
            if mod_name not in whitelist:
                logger.debug('Not Whitelisted: {}'.format(class_name))
                continue

        # Load the class and store it with its class_name
        try:
            mod_path = path.join(loader.path, mod_name + '.py')
            loaded_mod = imp.load_source(mod_name, mod_path)

            # Load class from imported module
            type = getattr(loaded_mod, class_name)

            if issubclass(type, parent_type):
                loaded.update({mod_name: type})
                logger.info('{} loaded as a {type} from {}/{}.py'
                            .format(class_name, src_path, mod_name,
                                    type=parent_type))
            else:
                logger.error('{} is not a sub-class of {}'
                             .format(class_name, parent_type))
        except Exception as e:
            logging.error('Failed to load {} from {} {}'
                          .format(class_name, mod_name, e))
    return loaded
