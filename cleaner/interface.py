import sys
from asyncio import run
from os import system
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QCheckBox, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from qdarktheme import setup_theme

from cleaner import remove, resource_path, threading

tasks_setup = {
    "Pastas e arquivos temporários": [
        "%USERPROFILE%/AppData/Local/Temp/",
        "/Windows/Temp/",
        "/Windows/prefetch",
    ],
    "Google Chrome": ["%USERPROFILE%/AppData/Local/Google"],
    "Microsoft Edge": ["%USERPROFILE%/AppData/Local/Microsoft/Edge"],
    "Brave": ["%USERPROFILE%/AppData/Local/BraveSoftware/Brave-Browser/User Data"],
    "Opera": ["%USERPROFILE%/AppData/Roaming/Opera Software/Opera GX Stable"],
    "Mozilla": ["%USERPROFILE%/AppData/Roaming/Mozilla"],
}


class Application(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout()
        self.tasks: list[QCheckBox] = []

        self.setup()
        self.show()

    def setup(self) -> None:
        icon_path = resource_path("assets/icon.png")
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

        self.setFixedSize(340, 270)
        self.change_title()
        self.fill_layout()

        base = QWidget()
        base.setLayout(self.layout)
        self.setCentralWidget(base)

    def fill_layout(self) -> None:
        label = QLabel("🔎 Observação sobre navegadores")
        label.setToolTip("Limpar um navegador vai apagar todos os dados dele")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        for path in tasks_setup:
            self.create_task(path)

        clean_button = QPushButton("🔎 Executar tarefas selecionadas")
        clean_button.setToolTip("Cuidado, não existe uma confirmação de remoção")
        clean_button.clicked.connect(self.clean_button_callback)
        self.layout.addWidget(clean_button)

        clean_terminal_button = QPushButton("Limpar o terminal")
        clean_terminal_button.clicked.connect(lambda: system("cls"))
        self.layout.addWidget(clean_terminal_button)

    def clean_button_callback(self) -> None:
        paths = []

        for task in self.tasks:
            if not task.isChecked():
                continue

            path = tasks_setup[task.text()]
            paths.append(path)

        run(remove.process(paths))

    def create_task(self, text: str) -> QCheckBox:
        check_box = QCheckBox(text)
        self.tasks.append(check_box)
        self.layout.addWidget(check_box)
        return check_box

    @threading
    def change_title(self) -> None:
        texts = [
            "Cleaner",
            "Controlado",
            "Balaclava#1912",
        ]
        while True:
            for text in texts:
                self.setWindowTitle(text)
                sleep(5)


def start() -> None:
    app = QApplication(sys.argv)
    setup_theme(additional_qss="QToolTip {color: #555555}")
    _ = Application()
    sys.exit(app.exec())
