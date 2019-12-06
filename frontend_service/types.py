import typing


class AuthorizedUser(typing.NamedTuple):
    user: str
    auth_roles: typing.List[str]


class SampleResult:
    def __init__(self, errors: dict = None, data: dict = None, task=None):
        self.errors = errors
        self.data = data
        self.task = task
