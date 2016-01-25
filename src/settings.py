import json
import logging
import os
import shutil

from fetcherd.util import get_data, get_config_home


class Settings(object):
    """Collection of settings"""

    def __init__(self, path):
        """path is a string to the file to be loaded as settings"""

        # if no path is given try default
        if not path:
            path = get_config_home()

        config_json = json.loads(open(path).read())
        for key, val in config_json.items():
            logging.debug("Loaded setting {}: {}".format(key, val))
            setattr(self, key, val)

        self._json = json
        self._path = path

    def __getitem__(self, key):
        return self.get(self, key)

    def get(self, key, default=None):
        """get a value from the settings, returns default if does not exist"""

        return getattr(self, key) if key in dir(self) else default
