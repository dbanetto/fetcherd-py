import requests
import json
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

    def get_series(self):
        """
        Returns:
            dict made from the json of the series in fetch-django
        """
        r = requests.get(self.url + 'series/',
                         headers={'Content-Type': 'application/json'})
        return r.json()

    def get_providers(self):
        """
        Returns:
            dict made from the json of the providers in fetch-django
        """
        r = requests.get(self.url + 'provider/',
                         headers={'Content-Type': 'application/json'})
        return r.json()

    def get_base_providers(self):
        """
        Returns:
            dict made from the json of the base providers in fetch-django
        """
        r = requests.get(self.url + 'provider/base/',
                         headers={'Content-Type': 'application/json'})
        return r.json()

    def post_update_episode_count(self, id, numb):
        requests.post(self.url + 'series/' + str(id) + '/count/',
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps({'current_count': numb}))
