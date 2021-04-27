import re
import requests
from functools import cached_property
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote_plus

from . import branch
from . import git
from .exceptions import *


class Repo:
    def __init__(self, git_folder: str):
        if not Path(git_folder).exists():
            raise ValueError("Not a Git repository. Folder .git not exists")

        self.git_folder = Path(git_folder)
        if not self._is_gitlab():
            raise ValueError("Not a gitlab repo")

    def read(self, key: str) -> Optional[str]:
        return git(f"git config --file={self.git_folder}/config --get {key}")

    def write(self, key: str, value: str) -> None:
        git(f"git config --file={self.git_folder} {key} {value}")

    @cached_property
    def gitlab_domain(self) -> str:
        remote_origin_url = self.read('remote.origin.url')
        if m := re.search(r'@([^:]+)', remote_origin_url):
            return m.group(1)

        raise RuntimeError(f"Can't find domain name in remote_origin_url: {remote_origin_url}")

    @cached_property
    def gitlab_https_new_merge_request(self) -> str:
        """
        https://<host>/<username>/<project>/-/merge_requests/new?merge_request%5Bsource_branch%5D=
        """
        remote_origin_url = self.read('remote.origin.url')
        if m := re.search(r'@([^:]+):(.+).git', remote_origin_url):
            https_url = "https://" + m.group(1) + "/" + m.group(2) + "/-/merge_requests/new?merge_request%5Bsource_branch%5D="
            return https_url

        raise RuntimeError(f"Can't find domain name in remote_origin_url: {remote_origin_url}")

    @cached_property
    def remote_origin_url(self) -> str:
        """
        git@<host>:<username>/<project>.git
        """
        return self.read('remote.origin.url')

    @cached_property
    def current_branch(self) -> "branch.Branch":
        name = git(f"git --git-dir={self.git_folder} branch --show-current")
        return branch.Branch(self, name)

    def local_branches(self) -> List["branch.Branch"]:
        names = git(f"git --git-dir={self.git_folder} branch --format='%(refname:short)'").split('\n')
        return [branch.Branch(self, name) for name in names]

    def _is_gitlab(self) -> bool:
        remote_origin_url = self.read('remote.origin.url')
        return bool(re.search(r'@gitlab', remote_origin_url))

    @cached_property
    def project_id(self) -> int:
        if project_id := self.read('R2D2.projectid'):
            return int(project_id)

        path_with_namespace = self._path_with_namespace()
        project_id = self._get_project_id(path_with_namespace)
        self.write('R2D2.projectid', str(project_id))
        return project_id

    def _path_with_namespace(self) -> str:
        remote_origin_url = self.read('remote.origin.url')
        if m := re.search(r':(.+)\.git', remote_origin_url):
            return m.group(1)
        raise RuntimeError(f"Can't find path_with_namespace: {remote_origin_url}")

    def _get_project_id(self, path_with_namespace: str) -> int:
        project_path_encoded = quote_plus(path_with_namespace)
        resp = requests.get(f"https://{self.gitlab_domain}/api/v4/projects/{project_path_encoded}",
                            headers={'Authorization': f"Bearer {self.access_token}"})
        if resp.status_code != 200:
            raise RuntimeError(resp.text)

        project_id = resp.json()['id']
        return project_id

    @cached_property
    def access_token(self) -> str:
        if access_token := self.read('R2D2.accesstoken'):
            return access_token

        username = input('GitLab username:')
        password = input('GitLab password:')
        access_token = self._get_access_token(username, password)
        self.write('R2D2.accesstoken', access_token)
        return access_token

    def _get_access_token(self, username: str, password: str) -> str:
        resp = requests.post(f"https://{self.gitlab_domain}/oauth/token",
                             json={"username": username, "password": password, "grant_type": "password"})
        if resp.status_code != 200:
            raise GitLabAuthErr(resp.text)

        access_token = resp.json()['access_token']
        return access_token

    @cached_property
    def check_merged_to(self) -> Optional[str]:
        return self.read('R2D2.checkmergedto')
