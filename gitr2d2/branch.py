from typing import List
from urllib.parse import quote_plus

import requests
from requests.exceptions import ConnectionError

from .config import Config
from .merge_request import MergeRequest
from .common import run
from .exceptions import *


class Branch:
    def __init__(self, name: str, config: Config):
        self.name = name
        self.config = config

    def description(self) -> str:
        text = self.config.read(f"branch.{self.name}.description")
        return text

    def is_merged(self, into: str) -> bool:
        res = run(f"git branch {self.name} --merged {into}")
        return True if res else False

    def merge_requests(self) -> List[MergeRequest]:
        branch_encoded = quote_plus(self.name)
        try:
            r = requests.get(
                f"https://{self.config.gitlab_domain}/api/v4/projects/{self.config.project_id}/merge_requests?source_branch={branch_encoded}",
                headers={'Authorization': f"Bearer {self.config.access_token}"})
        except ConnectionError as e:
            exit(f"Connection error: {e}")

        if r.status_code != 200:
            raise GitLabErr(r.text)

        mr_list = r.json()
        mrs = [MergeRequest(self.config, data) for data in mr_list]
        return mrs
