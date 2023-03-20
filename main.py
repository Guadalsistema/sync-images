#!/bin/env python3

"""
    work fast, die young
"""

import sys

from PyQt6.QtWidgets import QApplication

from app.gui.window.main import MainWindow



__version__ = "0.0.3"


if __name__ == "__main__":
    # Start the app
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName("Enviar imágenes")

    window = MainWindow()
    window.show()  # Windows are hidden by default.

    sys.exit(app.exec())
