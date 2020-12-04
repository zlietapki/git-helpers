import re
from urllib.parse import quote_plus
from pathlib import PurePath

import requests

from .common import run
from .exceptions import *


class Config:
    def __init__(self, file=PurePath('.git/config')):
        self.file = file

        # gitlab_domain
        remote_origin_url = self.read('remote.origin.url')
        if m := re.search(r'@([^:]+)', remote_origin_url):
            self.gitlab_domain = m.group(1)
        else:
            raise RuntimeError(f"Can't find domain name in remote_origin_url: {remote_origin_url}")

        self.access_token = self._get_access_token()

        #project_id
        self.project_id = self._get_project_id()

    def _get_access_token(self) -> str:
        if access_token := self.read('R2D2.accesstoken'):
            return access_token

        username = input('GitLab username:')
        password = input('GitLab password:')
        access_token = self._request_access_token(username, password)
        self.write('R2D2.accesstoken', access_token)
        return access_token

    def _request_access_token(self, username: str, password: str) -> str:
        r = requests.post(f"https://{self.gitlab_domain}/oauth/token",
                          json={"username": username, "password": password, "grant_type": "password"})
        if r.status_code != 200:
            raise GitLabAuthErr(r.text)

        access_token = r.json()['access_token']
        return access_token

    def _get_project_id(self) -> int:
        if project_id := self.read('R2D2.projectid'):
            return int(project_id)

        path_with_namespace = self.path_with_namespace()
        project_id = self._request_project_id(path_with_namespace)
        self.write('R2D2.projectid', str(project_id))
        return project_id

    def _request_project_id(self, path_with_namespace) -> int:
        project_path_encoded = quote_plus(path_with_namespace)
        r = requests.get(f"https://{self.gitlab_domain}/api/v4/projects/{project_path_encoded}",
                         headers={'Authorization': f"Bearer {self.access_token}"})
        if r.status_code != 200:
            raise GitLabErr(r.text)

        project_id = r.json()['id']
        return project_id

    def read(self, key: str) -> str:
        value = run(f"git config --file={self.file} --get {key}")
        return value

    def write(self, key: str, value: str) -> None:
        run(f"git config --file={self.file} {key} {value}")


    def path_with_namespace(self):
        remote_origin_url = self.read('remote.origin.url')
        if m := re.search(r':(.+)\.git', remote_origin_url):
            return m.group(1)
        raise RuntimeError(f"Can't find project name in remote_origin_url: {remote_origin_url}")
