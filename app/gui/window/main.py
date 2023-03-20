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
from ...controller.xmlrpc import Connection
from ...utils import send_image_list

class MainWindow(QWidget):
    """ Main class window """

    def mainButtonsBehaviour(self, button):
        """ Button box behaviour """
        tr = QObject.tr
        role = self.mainButtons.buttonRole(button)
        if role == QDialogButtonBox.ButtonRole.AcceptRole:
            searchFolder = QFileDialog.getExistingDirectory(self)
            if not searchFolder:
                self.textDisplay.append(tr("Invalid folder"))
                return

            self.textDisplay.append(tr(f"Open folder {searchFolder}"))
            url = self.urlLineEdit.text()
            dbase = self.databaseLineEdit.text()
            user = self.userLineEdit.text()
            password = self.passwordLineEdit.text()

            conn = Connection(url, dbase, user, password)
            try:
                conn.connect()
            except OSError as e:
                self.textDisplay.append(str(e))
                return

            if conn.uid == 0:
                self.textDisplay.append(tr(f"Error connecting to {url}. Aborting"))
                return

            send_image_list(conn, searchFolder, self.textDisplay)


    def __init__(self, parent: QWidget | None = None):
        """ Layout creation and connections """
        QWidget.__init__(self, parent)
        tr = QObject.tr

        self.urlLineEdit: QLineEdit = QLineEdit()
        self.urlLineEdit.setPlaceholderText("https://website.com")
        self.databaseLineEdit: QLineEdit = QLineEdit()
        self.userLineEdit: QLineEdit = QLineEdit()
        self.passwordLineEdit: QLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.mainButtons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Open)
        self.mainButtons.clicked.connect(self.mainButtonsBehaviour)

        formLayout = QFormLayout()
        formLayout.addRow(tr("url:"), self.urlLineEdit);
        formLayout.addRow(tr("database:"), self.databaseLineEdit);
        formLayout.addRow(tr("user:"), self.userLineEdit);
        formLayout.addRow(tr("password:"), self.passwordLineEdit);

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.mainButtons)
        self.textDisplay = QTextEdit(self)
        self.textDisplay.setReadOnly(True)
        layout.addWidget(self.textDisplay)

        self.setLayout(layout)
