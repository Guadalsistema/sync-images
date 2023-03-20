#!/bin/env python3

"""
    work fast, die young
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject

from app.gui.window.main import MainWindow

__version__ = "0.0.3"

if __name__ == "__main__":
    # Start the app
    tr = QObject.tr
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(tr("Enviar imágenes"))

    window = MainWindow()
    window.show()  # Windows are hidden by default.

    sys.exit(app.exec())
