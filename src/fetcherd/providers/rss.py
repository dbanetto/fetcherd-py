import re
import logging
import requests
import xml.etree.ElementTree as ET

from fetcherd.provider import Provider


class Rss(Provider):

    def __init__(self, provider):
        self.count_regex = re.compile(provider['regex_find_count'])
        self.options = provider['base_provider_options']

    def get_options_schema():
        return {"properties": {
            "feed_url": {
                "type": "string", "title": "Feed URL"
            }
        }}

    def fetch(self, series):
        logger = logging.getLogger("rss")

        feed_url = self.options['feed_url']

        logger.debug(feed_url)

        res = requests.get(feed_url)
        xml = ET.fromstring(res.text)

        titles = xml.findall(".//item/title")
        links = xml.findall(".//item/enclosure")

        found = []
        i = 0
        for t in titles:
            title = t.text
            numbs = self.count_regex.findall(title)
            if len(numbs) > 0:
                numb = int(numbs[0])
            else:
                numb = 0

            logger.info("Fected {} #{}".format(title, numb))
            found.append((numb, links[i].attrib['url'], title))
            i += 1

        return found

    def download(self, link, settings):
        if type(link) is not str:
            raise TypeError('link must be a str')

        re = requests.get(link, stream=True)
        filename = link.split('/')[-1]

        if 'content-disposition' in re.headers:
            for item in re.headers['content-disposition'].split(';'):
                if 'filename=' in item:
                    filename = item.split('=')[-1].strip('"')

        logging.info("Downloading to " + filename)
        return (re.iter_content(chunk_size=1024), filename)
