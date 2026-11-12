from copy import deepcopy

import pytest
from pydantic import ValidationError

from scenario.models import Scenario
from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController


@pytest.mark.parametrize(
    "changes",
    [
        {},
        {"title": "Another scenario"},
        {"files": [{"path": "/tmp/note.txt", "contents": "A note"}]},
    ],
)
def test_valid_scenarios_are_accepted(changes):
    data = deepcopy(SAMPLE_SCENARIO)
    data.update(changes)
    assert Scenario.model_validate(data).title == data["title"]


@pytest.mark.parametrize(
    "changes",
    [
        {"title": None},
        {"description": ""},
        {"files": []},
        {"files": [{"path": "/home/../host", "contents": "bad"}]},
        {"files": [{"path": "/tmp/note", "contents": 42}]},
        {"files": [{"path": "/tmp/a", "contents": "a"}] * 2},
        {"unsupported": True},
    ],
)
def test_invalid_scenarios_are_rejected(changes):
    data = deepcopy(SAMPLE_SCENARIO)
    data.update(changes)
    with pytest.raises(ValidationError):
        Scenario.model_validate(data)


def test_invalid_scenario_does_not_replace_active_state():
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    controller.delete_file("/home/student/Downloads/unexpected-update.txt")
    previous_paths = controller.file_paths()

    with pytest.raises(ValidationError):
        controller.start_scenario({"title": "incomplete"})

    assert controller.file_paths() == previous_paths
    assert controller.scenario.title == SAMPLE_SCENARIO["title"]


def test_restart_restores_files_and_separate_action_history():
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    controller.delete_file("/home/student/Downloads/unexpected-update.txt")
    previous_engine = controller.engine

    controller.start_scenario(SAMPLE_SCENARIO)

    assert len(controller.file_paths()) == 2
    assert previous_engine.actions[0].action_type == "FILE_DELETE"
    assert controller.engine.actions == ()
