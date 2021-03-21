__all__ = [
    'GitLabErr',
    'GitLabAuthErr',
]


class GitLabErr(Exception):
    pass


class GitLabAuthErr(GitLabErr):
    pass
