from enum import Enum, auto


class Role(Enum):
    PLATFORM_ADMIN = auto()
    ORG_ADMIN = auto()
    ORG_USER = auto()
    PUBLIC_USER = auto()
