import re
import logging
from urllib.parse import quote_plus
import requests
import xml.etree.ElementTree as ET

from fetcherd.provider import Provider


class Nyaa(Provider):

    def __init__(self, provider):
        self.provider = provider
        self.options = provider['base_provider_options']

        self.url = "http://www.nyaa.se/?page=rss&user={id}&term=" \
                   .format(id=self.options['id'])

    def get_options_schema():
        """
        Get JSON Schema used for validating providers from sources
        """
        return {"properties": {
            "id": {
                "type": "integer",
                "title": "Nyaa User ID"
            }
            }, "required": ["id"]
        }

    def fetch(self, series):
        """
        Fetches the episodes of the given series

        Args:
            series: a json dictionary of a Series from fetcher.Fetcher

        Returns:
            list of tuples cotaining (episode #, download link)
        """
        logger = logging.getLogger("nyaa")

        search_title = series['title'].strip()
        if 'search_title' in series:
            if series['search_title'].strip() != '':
                search_title = series['search_title'].strip()

        if 'quality' in series['media_type_options']:
            quality = series['media_type_options']['quality']
        else:
            quality = ""

        series_url = self.url + quote_plus(quality + ' ' + search_title)
        logger.debug(series_url)

        res = requests.get(series_url)
        xml = ET.fromstring(res.text)

        titles = xml.findall('.//item/title')
        links = xml.findall('.//item/link')
        assert(len(titles) == len(links))

        regex = re.compile(self.provider['regex_find_count'])
        found = []
        i = 0
        for t in titles:
            title = t.text
            if search_title not in title:
                continue

            # remove series name and search for episode number
            numbs = regex.findall(title.replace(series['search_title'], ''))
            if len(numbs) > 0:
                numb = int(numbs[0])
            else:
                numb = 0

            logger.debug("Fected {} #{}".format(title, numb))
            found.append((numb, links[i].text, title))
            i += 1

        return found

    def download(self, link, settings):
        """
        Downloads the given link to the given path

        File name based from the header 'content-disposition' otherwise the url

        Args:
            link: a string of the download link
            path: path to where the file should be saved
        """
        if type(link) is not str:
            raise TypeError('link must be a str')

        re = requests.get(link, stream=True)
        filename = link.split('/')[-1]

        if 'content-disposition' in re.headers:
            for item in re.headers['content-disposition'].split(';'):
                if 'filename=' in item:
                    filename = item.split('=')[-1].strip('"')

        return (re.iter_content(chunk_size=1024), filename)
