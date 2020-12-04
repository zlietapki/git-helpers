from .config import Config


class Approvals:
    def __init__(self, config: Config, data):
        self.config = config
        self.approvals_left = data['approvals_left']
        self.data = data
