import requests
import json
import logging
from requests.exceptions import ConnectionError
from fetcherd.source import Source


class WebClient(Source):
    """
    A class abstraction of the fetch-django API
    """

    def __init__(self, config):
        """
        Args:
            url: url to the base of the fetch-django server.
            Must end with forward slash '/'
        """
        url = config['url']

        if type(url) is not str:
            raise TypeError('Expected a str for url got a ' + str(type(url)))

        # correct base url
        if url[-1] != '/':
            url = url + '/'

        self.url = url
        self.logger = logging.getLogger('web_client')

    def get_series(self):
        """
        Returns:
            dict made from the json of the series in fetch-django
        """
        try:
            r = requests.get(self.url + 'series/',
                             headers={'Content-Type': 'application/json'})
            return r.json()
        except ConnectionError as e:
            self.logger.error("Failed to get series: {}".format(e))
            return []

    def get_providers(self):
        """
        Returns:
            dict made from the json of the providers in fetch-django
        """
        try:
            r = requests.get(self.url + 'provider/',
                             headers={'Content-Type': 'application/json'})
            return r.json()
        except ConnectionError as e:
            self.logger.error("Failed to get providers: {}".format(e))
            return []

    def get_base_providers(self):
        """
        Returns:
            dict made from the json of the base providers in fetch-django
        """
        try:
            r = requests.get(self.url + 'provider/base/',
                             headers={'Content-Type': 'application/json'})
            return r.json()
        except ConnectionError as e:
            self.logger.error("Failed to base providers: {}".format(e))
            return []

    def post_update_episode_count(self, id, numb):
        try:
            requests.post(self.url + 'series/' + str(id) + '/count/',
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps({'current_count': numb}))
        except ConnectionError as e:
            self.logger.error("Failed to post new count: {}".format(e))
