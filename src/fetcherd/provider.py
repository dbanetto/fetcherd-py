
class Provider():

    def __init__(self, base_provider):
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
        """Get a list of episodes for the given series

        The episodes are a tuple of (episode #, Link to download, Episode Name)
        """
        pass

    def download(self, link):
        """Start the download for the given link

        Return a tuple of (file name, stream of bytes)
        """
        pass
