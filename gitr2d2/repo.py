from typing import Optional, List
from pathlib import PurePath

from .common import run
from .config import Config
from .branch import Branch


class Repo:
    def __init__(self, git_dir: Optional[str] = '.git'):
        self.git_dir = PurePath(git_dir)
        config_file = self.git_dir / PurePath('config')
        self.config = Config(config_file)

    def current_branch(self) -> Branch:
        name = run(f"git --git-dir={self.git_dir} branch --show-current")
        return Branch(name, self.config)

    def local_branches(self) -> List[Branch]:
        names = run(f"git --git-dir={self.git_dir} branch --format='%(refname:short)'").split('\n')
        branches = [Branch(name, self.config) for name in names]
        return branches
