import requests
from urllib.parse import quote_plus
from typing import List
from functools import cached_property

from . import repo
from . import approvals
from . import pipeline
from .exceptions import *


class MergeRequest:
    def __init__(self, repo: "repo.Repo", data: dict):
        self._repo = repo
        self._data = data

    @classmethod
    def mrs_by_branchname(cls, branch_name: str, repo: "repo.Repo") -> List["MergeRequest"]:
        branch_encoded = quote_plus(branch_name)
        url = f"https://{repo.gitlab_domain}/api/v4/projects/{repo.project_id}/merge_requests?source_branch={branch_encoded}"
        try:
            resp = requests.get(url, headers={'Authorization': f"Bearer {repo.access_token}"})
        except ConnectionError as e:
            raise RuntimeError(f"Connection error: {e}")

        if resp.status_code != 200:
            raise GitLabErr(resp.text)

        mr_list = resp.json()
        mrs = [cls(repo, data) for data in mr_list]
        return mrs

    @cached_property
    def web_url(self) -> str:
        return self._data['web_url']

    @cached_property
    def iid(self) -> str:
        return self._data['iid']

    @cached_property
    def state(self) -> str:
        return self._data['state']

    @cached_property
    def description(self) -> str:
        return self._data['description']

    def approvals(self) -> approvals.Approvals:
        apprs = approvals.Approvals.get_by_mr_iid(self.iid, self._repo)
        return apprs

    def pipelines(self) -> List[pipeline.Pipeline]:
        r = requests.get(
            f"https://{self._repo.gitlab_domain}/api/v4/projects/{self._repo.project_id}/merge_requests/{self.iid}/pipelines",
            headers={'Authorization': f"Bearer {self._repo.access_token}"})
        if r.status_code != 200:
            raise GitLabErr(r.text)
        ppls = [pipeline.Pipeline(self._repo, data) for data in r.json()]
        return ppls
