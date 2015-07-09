from provider import Provider


class Dummy(Provider):

    def fetch(self, series):
        return []

    def download(self, link):
        pass
