
class Source():
    """
    Interface for a data source
    """

    def __init__(self, config):
        pass

    def get_series(self):
        pass

    def get_providers(self):
        pass

    def get_base_providers(self, id, epi_count):
        pass
