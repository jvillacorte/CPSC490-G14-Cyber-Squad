import pytest
import shiboken6
from PySide6.QtWidgets import QApplication, QMessageBox

from ui.window import MainWindow


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
    window.start_button.click()
    assert window.pages.currentIndex() == 1
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
    window.start_button.click()
    assert window.file_list.count() == 2
    window.close()


def test_cancel_delete_leaves_file_in_place(app, monkeypatch):
    window = MainWindow()
    window.start_button.click()
    window.file_list.setCurrentRow(0)
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args: QMessageBox.StandardButton.No
    )
    window.delete_button.click()
    assert window.file_list.count() == 2
    assert len(window.controller.engine.actions) == 1
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
