import requests
from functools import cached_property

from . import repo
from .exceptions import *


class Approvals:
    def __init__(self, repo: "repo.Repo", data):
        self.repo = repo
        self.data = data

    @classmethod
    def get_by_mr_iid(cls, mr_iid: str, repo: "repo.Repo") -> "Approvals":
        resp = requests.get(
            f"https://{repo.gitlab_domain}/api/v4/projects/{repo.project_id}/merge_requests/{mr_iid}/approvals",
            headers={'Authorization': f"Bearer {repo.access_token}"})
        if resp.status_code != 200:
            raise GitLabErr(resp.text)

        apprs = cls(repo, resp.json())
        return apprs

    @cached_property
    def approvals_left(self) -> int:
        return int(self.data['approvals_left'])
