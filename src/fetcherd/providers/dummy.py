from fetcherd.provider import Provider


class Dummy(Provider):

    def __init__(self, provider):
        """
        Setup the Base Provider

        Args:
            provider: a json dictionary of Provider that is based
            on this base provider
        """
        pass

    def get_options_schema():
        """
        Get JSON Schema used for validating providers from sources
        """
        return {"properties": {
            "id": {
                "type": "string",
                "title": "String"
            }
            }
        }

    def fetch(self, series):
        """
        Fetches the episodes of the given series

        Args:
            series: a json dictionary of a Series from fetcher.Fetcher

        Returns:
            list of tuples cotaining (episode #, download link)
        """
        return []

    def download(self, link):
        """
        Downloads the given link to the given path

        Args:
            link: a string of the download link
            path: path to where the file should be saved
        """
        pass
