from . import repo


class Pipeline:
    def __init__(self, repo: "repo.Repo", data):
        self.repo = repo
        self.data = data
        self.status = data['status']
