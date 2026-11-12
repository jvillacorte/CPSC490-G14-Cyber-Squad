import builtins
import os

import pytest

from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController


def test_inspect_delete_and_reject_missing_file():
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    path = "/home/student/Downloads/unexpected-update.txt"

    entries = controller.list_directory("/home/student")
    assert [(entry.name, entry.is_directory) for entry in entries] == [
        ("Downloads", True)
    ]
    download_entries = controller.list_directory("/home/student/Downloads")
    assert all(not entry.is_directory for entry in download_entries)
    assert [entry.name for entry in download_entries] == [
        "readme.txt",
        "unexpected-update.txt",
    ]
    assert "suspicious email" in controller.inspect_file(path).contents
    controller.delete_file(path)
    assert path not in controller.file_paths()
    with pytest.raises(ValueError, match="no longer exists"):
        controller.delete_file(path)
    assert [action.action_type for action in controller.engine.actions] == [
        "FILE_INSPECT",
        "FILE_DELETE",
    ]


def test_create_file_and_reject_invalid_names():
    controller = SimulationController()
    controller.start_scenario(SAMPLE_SCENARIO)
    directory = "/home/student/Downloads"
    path = controller.create_file(directory, "notes.txt", "My notes")

    assert controller.inspect_file(path).contents == "My notes"
    assert path in controller.file_paths()
    assert controller.engine.actions[0].action_type == "FILE_CREATE"

    for invalid_name in ("", ".", "..", "folder/file", "folder\\file", "x" * 256):
        with pytest.raises(ValueError):
            controller.create_file(directory, invalid_name, "contents")
    with pytest.raises(ValueError, match="already exists"):
        controller.create_file(directory, "readme.txt", "duplicate")
    with pytest.raises(ValueError, match="already exists"):
        controller.create_file("/home/student", "Downloads", "file conflicts with folder")
    with pytest.raises(ValueError, match="does not exist"):
        controller.create_file("/missing", "new.txt", "contents")


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
        controller.create_file(
            "/home/student/Downloads", "created-in-memory.txt", "simulated"
        )
        controller.inspect_file("/home/student/Downloads/unexpected-update.txt")
        controller.delete_file("/home/student/Downloads/unexpected-update.txt")

    assert host_file.read_text() == "host file remains unchanged"
    assert list(tmp_path.iterdir()) == [host_file]
