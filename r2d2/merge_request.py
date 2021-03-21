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
        self.repo = repo
        self.data = data

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
        return self.data['web_url']

    @cached_property
    def iid(self) -> str:
        return self.data['iid']

    @cached_property
    def state(self) -> str:
        return self.data['state']

    def approvals(self) -> approvals.Approvals:
        apprs = approvals.Approvals.get_by_mr_iid(self.iid, self.repo)
        return apprs

    def pipelines(self) -> List[pipeline.Pipeline]:
        r = requests.get(
            f"https://{self.repo.gitlab_domain}/api/v4/projects/{self.repo.project_id}/merge_requests/{self.iid}/pipelines",
            headers={'Authorization': f"Bearer {self.repo.access_token}"})
        if r.status_code != 200:
            raise GitLabErr(r.text)
        ppls = [pipeline.Pipeline(self.repo, data) for data in r.json()]
        return ppls
