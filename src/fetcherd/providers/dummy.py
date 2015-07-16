from fetcherd.provider import Provider


class Dummy(Provider):

    def get_options_schema():
        return {"properties": {
            "id": {
                "type": "string",
                "title": "String"
            }
            }
        }

    def fetch(self, series):
        return []

    def download(self, link):
        pass
