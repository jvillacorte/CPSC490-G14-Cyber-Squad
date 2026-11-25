import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import PurePosixPath

from scenario.models import Scenario, SimulatedFile


@dataclass(frozen=True)
class DirectoryEntry:
    name: str
    path: str
    is_directory: bool


@dataclass(frozen=True)
class FileDetails:
    """What the explorer shows when a simulated file is inspected."""

    path: str
    name: str
    contents: str
    size_bytes: int
    sha256: str
    created_at: datetime
    modified_at: datetime


@dataclass(frozen=True)
class _Timestamps:
    created_at: datetime
    modified_at: datetime


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Action:
    action_type: str
    path: str
    recorded_at: datetime


class SimulationEngine:
    def __init__(
        self, scenario: Scenario, clock: Callable[[], datetime] = _utc_now
    ):
        self._clock = clock
        self._files = {file.path: file for file in scenario.files}
        loaded_at = clock()
        self._timestamps = {
            path: _Timestamps(loaded_at, loaded_at) for path in self._files
        }
        self._directories = {"/"}
        for path in self._files:
            parent = PurePosixPath(path).parent
            while str(parent) != "/":
                self._directories.add(str(parent))
                parent = parent.parent
        self._actions: list[Action] = []

    @property
    def paths(self) -> tuple[str, ...]:
        return tuple(sorted(self._files))

    @property
    def actions(self) -> tuple[Action, ...]:
        return tuple(self._actions)

    def list_directory(self, path: str) -> tuple[DirectoryEntry, ...]:
        directory = self._normalize_directory(path)
        if directory not in self._directories:
            raise ValueError("The simulated directory does not exist")

        entries: list[DirectoryEntry] = []
        for child in self._directories:
            if child != directory and str(PurePosixPath(child).parent) == directory:
                entries.append(
                    DirectoryEntry(PurePosixPath(child).name, child, True)
                )
        for file_path in self._files:
            if str(PurePosixPath(file_path).parent) == directory:
                entries.append(
                    DirectoryEntry(
                        PurePosixPath(file_path).name, file_path, False
                    )
                )
        return tuple(
            sorted(
                entries,
                key=lambda entry: (not entry.is_directory, entry.name.casefold()),
            )
        )

    def inspect_file(self, path: str) -> FileDetails:
        file = self._get_file(path)
        encoded = file.contents.encode("utf-8")
        times = self._timestamps[path]
        details = FileDetails(
            path=file.path,
            name=PurePosixPath(file.path).name,
            contents=file.contents,
            size_bytes=len(encoded),
            sha256=hashlib.sha256(encoded).hexdigest(),
            created_at=times.created_at,
            modified_at=times.modified_at,
        )
        self._record("FILE_INSPECT", path)
        return details

    def create_file(self, directory: str, name: str, contents: str = "") -> str:
        parent = self._normalize_directory(directory)
        if parent not in self._directories:
            raise ValueError("The simulated directory does not exist")
        if not isinstance(name, str) or not name or len(name) > 255:
            raise ValueError("File name must contain between 1 and 255 characters")
        if name in (".", "..") or "/" in name or "\\" in name or "\x00" in name:
            raise ValueError("File name must be a single valid path component")
        if not isinstance(contents, str):
            raise ValueError("File contents must be text")

        path = str(PurePosixPath(parent) / name)
        if path in self._files or path in self._directories:
            raise ValueError("A simulated entry with that name already exists")
        self._files[path] = SimulatedFile(path=path, contents=contents)
        created_at = self._clock()
        self._timestamps[path] = _Timestamps(created_at, created_at)
        self._record("FILE_CREATE", path)
        return path

    def delete_file(self, path: str) -> None:
        self._get_file(path)
        del self._files[path]
        del self._timestamps[path]
        self._record("FILE_DELETE", path)

    def _get_file(self, path: str) -> SimulatedFile:
        try:
            return self._files[path]
        except KeyError:
            raise ValueError("The simulated file no longer exists") from None

    def _record(self, action_type: str, path: str) -> None:
        self._actions.append(Action(action_type, path, self._clock()))

    @staticmethod
    def _normalize_directory(path: str) -> str:
        if not isinstance(path, str) or not path.startswith("/") or "\\" in path:
            raise ValueError("Directory must be an absolute virtual path")
        normalized = str(PurePosixPath(path))
        if path != normalized or any(part in (".", "..") for part in path.split("/")):
            raise ValueError("Directory path must be normalized")
        return normalized
