from .config import Config


class Pipeline:
    def __init__(self, config: Config, data):
        self.config = config
        self.data = data
        self.status = data['status']
