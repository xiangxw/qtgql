import dataclasses
import re
from enum import Enum
from pathlib import Path

RELEASE_TYPE_REGEX = re.compile(r"^[Rr]elease [Tt]ype: (major|minor|patch)$")


class InvalidReleaseFileError(Exception):
    pass


class ChangeType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclasses.dataclass
class ReleaseInfo:
    change_type: ChangeType
    changelog: str


def get_release_info(file_path: Path) -> ReleaseInfo:
    with file_path.open("r") as f:
        line = f.readline()
        match = RELEASE_TYPE_REGEX.match(line)

        if not match:
            raise InvalidReleaseFileError()

        change_type_key = match.group(1)
        change_type = ChangeType[change_type_key.upper()]
        changelog = "".join([line for line in f.readlines()]).strip()

    return ReleaseInfo(change_type, changelog)
