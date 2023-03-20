#!/bin/env python
import base64


def path_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('ascii')


class Product:
    code: str
    image_principal: str | None = None
    image_list: list = []

    def __init__(self, conn, code: str):
        self.conn = conn
        self.code = code
        self.image_list = []

    def update(self):
        if not self.image_principal:
            return

        # Products without image
        found = self.conn.execute("product.template",
                             "search",
                             [
                                '|',
                                ["barcode", '=', self.code],
                                ["default_code", '=', self.code],
                                ['image_1920', '=', False]
                             ])
        if found:
            self.conn.write("product.template",
                         [found[0], {
                             "image_1920": path_to_base64(self.image_principal),
                             }])

        if found and self.image_list:
            for idx, image in enumerate(self.image_list):
                self.conn.write("product.template",
                             [found[0], {
                                 "product_template_image_ids": [(0,0, {'name': f'image: {idx}', 'image_1920': path_to_base64(image)})]
                                }])

