from pydantic import ValidationError
from PySide6.QtCore import QSignalBlocker, Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from scenario.loader import load_scenario_file
from scenario.sample import SAMPLE_SCENARIO
from sim.controller import SimulationController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = SimulationController()
        self.setWindowTitle("Cyber Sandbox")
        self.resize(800, 500)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)
        self._build_start_page()
        self._build_scenario_page()

    def _build_start_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Cyber Sandbox — offline prototype"))
        layout.addWidget(QLabel("Start the sample or load a scenario JSON file."))
        self.start_button = QPushButton("Start scenario")
        self.start_button.clicked.connect(self._start_scenario)
        layout.addWidget(self.start_button)
        self.load_button = QPushButton("Load scenario JSON")
        self.load_button.clicked.connect(self._load_scenario)
        layout.addWidget(self.load_button)
        layout.addStretch()
        self.pages.addWidget(page)

    def _build_scenario_page(self) -> None:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.title = QLabel()
        self.description = QLabel()
        self.title.setTextFormat(Qt.TextFormat.PlainText)
        self.description.setTextFormat(Qt.TextFormat.PlainText)
        self.description.setWordWrap(True)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addWidget(QLabel("Simulated files"))

        self.directory_label = QLabel()
        layout.addWidget(self.directory_label)
        files_layout = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.currentItemChanged.connect(self._selection_changed)
        self.details = QPlainTextEdit()
        self.details.setReadOnly(True)
        self.details.setPlaceholderText("Select a simulated file to inspect it.")
        files_layout.addWidget(self.file_list)
        files_layout.addWidget(self.details)
        layout.addLayout(files_layout)

        actions = QHBoxLayout()
        self.up_button = QPushButton("Up")
        self.up_button.clicked.connect(self._go_up)
        actions.addWidget(self.up_button)
        self.create_button = QPushButton("New simulated file")
        self.create_button.clicked.connect(self._create_file)
        actions.addWidget(self.create_button)
        self.delete_button = QPushButton("Delete simulated file")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_selected)
        actions.addWidget(self.delete_button)
        self.back_button = QPushButton("Back to start")
        self.back_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        actions.addWidget(self.back_button)
        layout.addLayout(actions)
        self.pages.addWidget(page)

    def _start_scenario(self) -> None:
        self._show_scenario(SAMPLE_SCENARIO)

    def _load_scenario(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load scenario JSON", "", "JSON files (*.json);;All files (*)"
        )
        if not path:
            return
        try:
            scenario = load_scenario_file(path)
        except (OSError, UnicodeError) as error:
            QMessageBox.critical(self, "Cannot read scenario", str(error))
            return
        except ValidationError as error:
            QMessageBox.critical(self, "Scenario validation failed", str(error))
            return
        self._show_scenario(scenario)

    def _show_scenario(self, data: object) -> None:
        try:
            scenario = self.controller.start_scenario(data)
        except ValidationError as error:
            QMessageBox.critical(self, "Scenario validation failed", str(error))
            return

        self.title.setText(scenario.title)
        self.description.setText(scenario.description)
        initial_directory = (
            "/home/student"
            if any(file.path.startswith("/home/student/") for file in scenario.files)
            else "/"
        )
        self._show_directory(initial_directory)
        self.pages.setCurrentIndex(1)

    def _show_directory(self, path: str) -> None:
        self.current_directory = path
        self.directory_label.setText(f"Virtual path: {path}")
        self.up_button.setEnabled(path != "/")
        self.file_list.clear()
        for entry in self.controller.list_directory(path):
            label = f"{entry.name}/" if entry.is_directory else entry.name
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, entry.path)
            item.setData(Qt.ItemDataRole.UserRole + 1, entry.is_directory)
            self.file_list.addItem(item)
        self.details.clear()
        self.delete_button.setEnabled(False)

    def _go_up(self) -> None:
        if self.current_directory == "/":
            return
        parent = self.current_directory.rsplit("/", 1)[0] or "/"
        self._show_directory(parent)

    def _create_file(self) -> None:
        name, accepted = QInputDialog.getText(
            self, "New simulated file", "File name:"
        )
        if not accepted:
            return
        contents, accepted = QInputDialog.getMultiLineText(
            self, "New simulated file", "Text contents:"
        )
        if not accepted:
            return
        try:
            path = self.controller.create_file(self.current_directory, name, contents)
        except ValueError as error:
            QMessageBox.warning(self, "Cannot create file", str(error))
            return
        self._show_directory(self.current_directory)
        for row in range(self.file_list.count()):
            item = self.file_list.item(row)
            if item.data(Qt.ItemDataRole.UserRole) == path:
                self.file_list.setCurrentItem(item)
                break

    def _selection_changed(self, current: QListWidgetItem | None) -> None:
        self.details.clear()
        self.delete_button.setEnabled(current is not None)
        if current is None:
            return
        path = current.data(Qt.ItemDataRole.UserRole)
        if current.data(Qt.ItemDataRole.UserRole + 1):
            self._show_directory(path)
            return
        try:
            file = self.controller.inspect_file(path)
        except ValueError as error:
            self.delete_button.setEnabled(False)
            QMessageBox.warning(self, "Cannot inspect file", str(error))
            return
        self.details.setPlainText(f"Virtual path: {file.path}\n\n{file.contents}")

    def _delete_selected(self) -> None:
        item = self.file_list.currentItem()
        if item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        answer = QMessageBox.question(
            self,
            "Delete simulated file",
            f"Delete {path} from this scenario? No host file will be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.controller.delete_file(path)
        except ValueError as error:
            QMessageBox.warning(self, "Cannot delete file", str(error))
            return
        with QSignalBlocker(self.file_list):
            self.file_list.takeItem(self.file_list.row(item))
            self.file_list.setCurrentRow(-1)
        self.details.clear()
        self.delete_button.setEnabled(False)
