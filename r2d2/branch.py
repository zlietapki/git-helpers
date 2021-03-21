from typing import List

from . import repo
from . import merge_request

from . import run


class Branch:
    def __init__(self, repo: "repo.Repo", name: str):
        self.repo = repo
        self.name = name

    def description(self) -> str:
        description = self.repo.read(f"branch.{self.name}.description")
        return description

    def merge_requests(self) -> List["merge_request.MergeRequest"]:
        mrs = merge_request.MergeRequest.mrs_by_branchname(self.name, self.repo)
        return mrs

    def is_merged_in(self, into: str) -> bool:
        return bool(run(f"git branch {self.name} --merged {into}"))
