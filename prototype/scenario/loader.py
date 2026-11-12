from pathlib import Path

from scenario.models import Scenario


def load_scenario_file(path: str) -> Scenario:
    return Scenario.model_validate_json(Path(path).read_text(encoding="utf-8"))
