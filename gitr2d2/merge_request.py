from typing import List

import requests
from .config import Config
from .approvals import Approvals
from .pipeline import Pipeline
from .exceptions import *


class MergeRequest:
    def __init__(self, config: Config, data):
        self.config = config
        self.data = data
        self.iid = data['iid']
        self.web_url = data['web_url']

    def approvals(self) -> Approvals:
        r = requests.get(
            f"https://{self.config.gitlab_domain}/api/v4/projects/{self.config.project_id}/merge_requests/{self.iid}/approvals",
            headers={'Authorization': f"Bearer {self.config.access_token}"})
        if r.status_code != 200:
            raise GitLabErr(r.text)

        apprs = Approvals(self.config, r.json())
        return apprs

    def pipelines(self) -> List[Pipeline]:
        r = requests.get(
            f"https://{self.config.gitlab_domain}/api/v4/projects/{self.config.project_id}/merge_requests/{self.iid}/pipelines",
            headers={'Authorization': f"Bearer {self.config.access_token}"})
        if r.status_code != 200:
            raise GitLabErr(r.text)
        ppls = [Pipeline(self.config, data) for data in r.json()]
        return ppls
