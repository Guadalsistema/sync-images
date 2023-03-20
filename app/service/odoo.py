#!/bin/env python
import base64
import re
from pathlib import Path

def get_code(pathfile: Path):
    name = pathfile.stem

    group = re.split(r'[_-]+', name)
    if len(group) > 1:
        group = group[0]

    return ''.join(group)


def path_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('ascii')


class Product:
    barcode: str
    image_principal: str | None = None

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

