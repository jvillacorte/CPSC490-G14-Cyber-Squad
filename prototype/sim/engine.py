from dataclasses import dataclass
from datetime import datetime, timezone

from scenario.models import Scenario, SimulatedFile


@dataclass(frozen=True)
class Action:
    action_type: str
    path: str
    recorded_at: datetime


class SimulationEngine:
    def __init__(self, scenario: Scenario):
        self._files = {file.path: file for file in scenario.files}
        self._actions: list[Action] = []

    @property
    def paths(self) -> tuple[str, ...]:
        return tuple(sorted(self._files))

    @property
    def actions(self) -> tuple[Action, ...]:
        return tuple(self._actions)

    def inspect_file(self, path: str) -> SimulatedFile:
        file = self._get_file(path)
        self._record("FILE_INSPECT", path)
        return file

    def delete_file(self, path: str) -> None:
        self._get_file(path)
        del self._files[path]
        self._record("FILE_DELETE", path)

    def _get_file(self, path: str) -> SimulatedFile:
        try:
            return self._files[path]
        except KeyError:
            raise ValueError("The simulated file no longer exists") from None

    def _record(self, action_type: str, path: str) -> None:
        self._actions.append(Action(action_type, path, datetime.now(timezone.utc)))
