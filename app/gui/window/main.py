from PyQt6.QtWidgets import (
        QWidget,
        QDialogButtonBox,
        QFileDialog,
        QVBoxLayout,
        QFormLayout,
        QLineEdit,
        QTextEdit)
from PyQt6.QtCore import QObject

from ...service.odoo import Product 


class MainWindow(QWidget):
    """ Main class window """
    def mainButtonsBehaviour(self, button):
        """ Button box behaviour """
        tr = QObject.tr
        role = self.mainButtons.buttonRole(button)
        if role == QDialogButtonBox.ButtonRole.AcceptRole:
            searchFolder = QFileDialog.getExistingDirectory(self)
            self.textDisplay.append(tr(f"Open folder {searchFolder}"))

    def __init__(self, parent: QWidget | None = None):
        """ Layout creation and connections """
        QWidget.__init__(self, parent)
        tr = QObject.tr

        self.mainButtons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Open)
        self.mainButtons.clicked.connect(self.mainButtonsBehaviour)

        formLayout = QFormLayout()
        self.urlLineEdit = QLineEdit()
        formLayout.addRow(tr("url:"), self.urlLineEdit);
        self.databaseLineEdit = QLineEdit()
        formLayout.addRow(tr("database:"), self.databaseLineEdit);
        self.userLineEdit = QLineEdit()
        formLayout.addRow(tr("user:"), self.userLineEdit);
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        formLayout.addRow(tr("password:"), self.passwordLineEdit);

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.mainButtons)
        self.textDisplay = QTextEdit(self)
        self.textDisplay.setReadOnly(True)
        layout.addWidget(self.textDisplay)

        self.setLayout(layout)
