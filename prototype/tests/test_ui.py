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
