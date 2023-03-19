#!/bin/env python3

"""
    work fast, die young
"""

import base64
import re
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from app.gui.window.main import MainWindow


def get_code(pathfile: Path):
    name = pathfile.stem

    group = re.split(r'[_-]+', name)
    if len(group) > 1:
        group = group[0]

    return ''.join(group)


def get_position(pathfile: Path) -> int:
    name = pathfile.stem

    group = re.split(r'[_-]+', name)
    if len(group) == 1:
        return 0

    return int(group[1])


def path_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('ascii')


class InternalCategory:
    name: str
    _id: int
    ids: list = []
    PARENT_ID: int = 2

    def __init__(self, path_name: str):
        """ Check """
        path = Path(path_name)
        val = self.browse(path.parts[4])
        if val:
            self = val
            return

        self.name = path.parts[4]

        remote_categ = \
                conn.execute(
                        "product.category",
                        "search_read",
                        [["name", "=", self.name]],
                        {'fields': ["id"]}
                )

        if remote_categ:
            if len(remote_categ) > 1:
                raise Exception("Same category multiple names")
            self._id = remote_categ[0]["id"]
        else:
            self._id = conn.execute("product.category", "create", {
                "name": self.name,
                "parent_id": self.PARENT_ID})
        self.ids.append(self)
        return

    def browse(self, name: str):
        for i in self.ids:
            if i.name == name:
                return i

        return False


class Product:
    barcode: str
    image_principal: str = None

    def __init__(self, conn, barcode: str):
        self.conn = conn
        self.barcode = barcode
        self.image_list = []

    def update(self):
        if not self.image_principal:
            return

        # Products without image
        found = self.conn.execute("product.template",
                             "search",
                             [
                                '|',
                                ["barcode", '=', self.barcode],
                                ["default_code", '=', self.barcode],
                                ['image_1920', '=', False],
                                ['active', '=', True]
                             ])
        if found:
            #categ = InternalCategory(self.image_principal)
            self.conn.write("product.template",
                         [found[0], {
                             "image_1920": path_to_base64(self.image_principal),
                       #      "categ_id": categ._id
                             }])

        if found and self.image_list:
            for idx, image in enumerate(self.image_list):
                self.conn.write("product.template",
                             [found[0], {
                                 "product_template_image_ids": [(0,0, {'name': f'image: {idx}', 'image_1920': path_to_base64(image)})]
                                }])


__version__ = "0.0.3"


if __name__ == "__main__":
    # Start the app

    # necesary
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName("Enviar imágenes")

    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())
