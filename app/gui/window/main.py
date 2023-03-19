from PyQt6.QtWidgets import (
        QWidget,
        QFileDialog,
        QDialogButtonBox,
        QVBoxLayout,
        QTextEdit
        )

class MainWindow(QWidget):
    """ Main class window """
    def mainButtonsBehaviour(self, button):
        pass
        raise NotImplementedError("Unknown button")

    def __init__(self, parent: QWidget | None = None):
        """ Layout creation and connections """
        QWidget.__init__(self, parent)

        self.mainButtons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Apply | QDialogButtonBox.StandardButton.Open)
        self.mainButtons.clicked.connect(self.mainButtonsBehaviour)

        layout = QVBoxLayout()
        layout.addWidget(self.mainButtons)
        self.textDisplay = QTextEdit(self)
        self.textDisplay.setReadOnly(True)
        layout.addWidget(self.textDisplay)

        self.setLayout(layout)
