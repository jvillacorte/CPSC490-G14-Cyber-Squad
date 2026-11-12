import json

import pytest
from pydantic import ValidationError

from scenario.loader import load_scenario_file
from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController


def test_load_generated_json_into_simulation(tmp_path):
    scenario_file = tmp_path / "scenario.json"
    scenario_file.write_text(json.dumps(SAMPLE_SCENARIO), encoding="utf-8")

    controller = SimulationController()
    controller.start_scenario(load_scenario_file(str(scenario_file)))

    assert controller.inspect_file(
        "/home/student/Downloads/unexpected-update.txt"
    ).contents == SAMPLE_SCENARIO["files"][1]["contents"]
    controller.delete_file("/home/student/Downloads/unexpected-update.txt")
    assert scenario_file.read_text(encoding="utf-8") == json.dumps(SAMPLE_SCENARIO)


@pytest.mark.parametrize(
    "contents",
    ['not json', '{"title": "Incomplete"}', '{"title": 5}'],
)
def test_reject_invalid_json_without_replacing_active_simulation(tmp_path, contents):
    scenario_file = tmp_path / "scenario.json"
    scenario_file.write_bytes(contents.encode("latin-1"))
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    previous_engine = controller.engine

    with pytest.raises(ValidationError):
        controller.start_scenario(load_scenario_file(str(scenario_file)))

    assert controller.engine is previous_engine


def test_reject_file_that_is_also_a_directory(tmp_path):
    scenario_file = tmp_path / "scenario.json"
    scenario = {
        "title": "Conflict",
        "description": "A file and a directory share a path.",
        "files": [
            {"path": "/tmp/item", "contents": "file"},
            {"path": "/tmp/item/child", "contents": "child"},
        ],
    }
    scenario_file.write_text(json.dumps(scenario), encoding="utf-8")

    with pytest.raises(ValidationError, match="cannot also be a directory"):
        load_scenario_file(str(scenario_file))


def test_unreadable_file_is_reported(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scenario_file(str(tmp_path / "missing.json"))

    scenario_file = tmp_path / "invalid-encoding.json"
    scenario_file.write_bytes(b"\xff")
    with pytest.raises(UnicodeDecodeError):
        load_scenario_file(str(scenario_file))
