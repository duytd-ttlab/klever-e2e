from dataclasses import dataclass
from enum import Enum

from constants.role import Role


@dataclass
class Credentials:
    EMAIL: str
    PASSWORD: str


@dataclass
class Config:
    BASE_URL: str
    CREDENTIALS_BY_ROLE: dict[Role, Credentials]


class UrlPath(Enum):
    PROJECT = 'project/'
    PROJECT_TASK_BOARD = '/project/project/{}/board'
    TASK = 'task/'
    SETTINGS = 'settings/'
