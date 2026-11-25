import builtins
import hashlib
import os
from datetime import datetime, timedelta, timezone

import pytest

from scenario.models import Scenario
from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController
from sim.engine import SimulationEngine


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


def test_inspect_reports_file_information():
    start = datetime(2026, 11, 25, 12, 0, tzinfo=timezone.utc)
    ticks = iter(start + timedelta(minutes=minute) for minute in range(10))
    engine = SimulationEngine(
        Scenario.model_validate(SAMPLE_SCENARIO), clock=lambda: next(ticks)
    )
    path = "/home/student/Downloads/readme.txt"
    contents = SAMPLE_SCENARIO["files"][0]["contents"]

    details = engine.inspect_file(path)
    assert details.path == path
    assert details.name == "readme.txt"
    assert details.contents == contents
    assert details.size_bytes == len(contents.encode("utf-8"))
    assert details.sha256 == hashlib.sha256(contents.encode("utf-8")).hexdigest()
    assert details.created_at == details.modified_at == start

    created = engine.create_file("/home/student/Downloads", "café.txt", "naïve")
    new_details = engine.inspect_file(created)
    assert new_details.size_bytes == len("naïve".encode("utf-8")) == 6
    assert new_details.created_at == new_details.modified_at > start
    assert new_details.sha256 != details.sha256


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
