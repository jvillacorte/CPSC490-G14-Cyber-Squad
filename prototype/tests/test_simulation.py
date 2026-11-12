import builtins
import os

import pytest

from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController


def test_inspect_delete_and_reject_missing_file():
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    path = "/home/student/Downloads/unexpected-update.txt"

    assert "suspicious email" in controller.inspect_file(path).contents
    controller.delete_file(path)
    assert path not in controller.file_paths()
    with pytest.raises(ValueError, match="no longer exists"):
        controller.delete_file(path)
    assert [action.action_type for action in controller.engine.actions] == [
        "FILE_INSPECT",
        "FILE_DELETE",
    ]


def test_simulated_file_actions_do_not_touch_host_files(tmp_path, monkeypatch):
    host_file = tmp_path / "unexpected-update.txt"
    host_file.write_text("host file remains unchanged")
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)

    def forbidden(*args, **kwargs):
        raise AssertionError("Simulation attempted a host file operation")

    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", forbidden)
        patch.setattr(os, "remove", forbidden)
        patch.setattr(os, "unlink", forbidden)
        controller.inspect_file("/home/student/Downloads/unexpected-update.txt")
        controller.delete_file("/home/student/Downloads/unexpected-update.txt")

    assert host_file.read_text() == "host file remains unchanged"
    assert list(tmp_path.iterdir()) == [host_file]
