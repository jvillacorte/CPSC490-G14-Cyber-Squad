import json

import pytest

# Skip UI tests where Qt's system libraries (e.g. libEGL) are unavailable, such as CI.
QtWidgets = pytest.importorskip(
    "PySide6.QtWidgets", exc_type=ImportError, reason="Qt runtime libraries unavailable"
)
import shiboken6  # noqa: E402

QApplication = QtWidgets.QApplication
QMessageBox = QtWidgets.QMessageBox

from ui.window import MainWindow  # noqa: E402


def open_downloads(window):
    window.start_button.click()
    assert window.pages.currentIndex() == 1
    assert window.directory_label.text() == "Virtual path: /home/student"
    window.file_list.setCurrentRow(0)
    assert window.directory_label.text() == "Virtual path: /home/student/Downloads"


@pytest.fixture(scope="module")
def app():
    application = QApplication([])
    yield application
    application.closeAllWindows()
    application.processEvents()
    shiboken6.delete(application)


def test_start_inspect_delete_and_restart(app, monkeypatch):
    window = MainWindow()
    window.show()
    open_downloads(window)
    assert window.file_list.count() == 2

    window.file_list.setCurrentRow(1)
    assert "suspicious email" in window.details.toPlainText()
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.Yes
    )
    window.delete_button.click()
    assert window.file_list.count() == 1
    assert window.details.toPlainText() == ""
    assert not window.delete_button.isEnabled()
    assert [action.action_type for action in window.controller.engine.actions] == [
        "FILE_INSPECT",
        "FILE_DELETE",
    ]

    window.back_button.click()
    open_downloads(window)
    assert window.file_list.count() == 2
    window.close()


def test_cancel_delete_leaves_file_in_place(app, monkeypatch):
    window = MainWindow()
    open_downloads(window)
    window.file_list.setCurrentRow(0)
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.No
    )
    window.delete_button.click()
    assert window.file_list.count() == 2
    assert len(window.controller.engine.actions) == 1
    window.close()


def test_create_file_in_current_virtual_directory(app, monkeypatch):
    window = MainWindow()
    open_downloads(window)
    monkeypatch.setattr(
        "ui.window.QInputDialog.getText", lambda *args: ("notes.txt", True)
    )
    monkeypatch.setattr(
        "ui.window.QInputDialog.getMultiLineText",
        lambda *args: ("Course notes", True),
    )

    window.create_button.click()

    assert window.file_list.count() == 3
    assert window.file_list.currentItem().text() == "notes.txt"
    assert window.details.toPlainText().endswith("Course notes")
    assert window.controller.engine.actions[0].action_type == "FILE_CREATE"
    window.close()


def test_directory_navigation_and_file_creation_cancel(app, monkeypatch):
    window = MainWindow()
    open_downloads(window)
    window.up_button.click()
    assert window.directory_label.text() == "Virtual path: /home/student"
    assert window.file_list.currentItem() is None

    monkeypatch.setattr(
        "ui.window.QInputDialog.getText", lambda *args: ("", False)
    )
    window.create_button.click()

    assert window.controller.engine.paths == (
        "/home/student/Downloads/readme.txt",
        "/home/student/Downloads/unexpected-update.txt",
    )
    window.close()


def test_invalid_sample_shows_error_without_starting(app, monkeypatch):
    window = MainWindow()
    errors = []
    monkeypatch.setattr("ui.window.SAMPLE_SCENARIO", {"title": "Incomplete"})
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: errors.append(args))

    window.start_button.click()

    assert window.pages.currentIndex() == 0
    assert window.controller.engine is None
    assert errors and "validation" in errors[0][1].lower()
    window.close()


def test_load_json_file_and_navigate_from_root(app, monkeypatch, tmp_path):
    scenario_file = tmp_path / "scenario.json"
    scenario_file.write_text(json.dumps({
        "title": "Generated scenario",
        "description": "Investigate the note.",
        "files": [{"path": "/tmp/note.txt", "contents": "Generated evidence"}],
    }), encoding="utf-8")
    monkeypatch.setattr(
        "ui.window.QFileDialog.getOpenFileName",
        lambda *args: (str(scenario_file), "JSON files (*.json)"),
    )
    window = MainWindow()

    window.load_button.click()

    assert window.pages.currentIndex() == 1
    assert window.title.text() == "Generated scenario"
    assert window.directory_label.text() == "Virtual path: /"
    window.file_list.setCurrentRow(0)
    window.file_list.setCurrentRow(0)
    assert "Generated evidence" in window.details.toPlainText()
    window.close()


def test_invalid_file_and_cancel_keep_active_scenario(app, monkeypatch, tmp_path):
    scenario_file = tmp_path / "bad.json"
    scenario_file.write_text("invalid json", encoding="utf-8")
    window = MainWindow()
    window.start_button.click()
    engine = window.controller.engine
    window.back_button.click()
    errors = []
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: errors.append(args))
    monkeypatch.setattr(
        "ui.window.QFileDialog.getOpenFileName",
        lambda *args: (str(scenario_file), ""),
    )

    window.load_button.click()
    assert errors and "validation" in errors[0][1].lower()
    assert window.controller.engine is engine
    assert window.pages.currentIndex() == 0

    monkeypatch.setattr("ui.window.QFileDialog.getOpenFileName", lambda *args: ("", ""))
    window.load_button.click()
    assert len(errors) == 1
    assert window.controller.engine is engine
    window.close()


def test_missing_scenario_file_reports_read_error(app, monkeypatch, tmp_path):
    window = MainWindow()
    errors = []
    monkeypatch.setattr(QMessageBox, "critical", lambda *args: errors.append(args))
    monkeypatch.setattr(
        "ui.window.QFileDialog.getOpenFileName",
        lambda *args: (str(tmp_path / "missing.json"), ""),
    )

    window.load_button.click()

    assert errors and "Cannot read" in errors[0][1]
    assert window.controller.engine is None
    assert window.pages.currentIndex() == 0
    window.close()
