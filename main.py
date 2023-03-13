#!/bin/env python3

"""
    work fast, die young
"""

import argparse
import logging
import base64
import re

from pathlib import Path

import pandas as pd

from sync_products.connector import Connection

logger = logging.getLogger(__file__)

def get_code(pathfile: Path):
    name = pathfile.stem

    group = re.split(r'[_-]+', name)
    if len(group) > 1:
        group = group[:-1]

    return ''.join(group)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog=__file__,
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument("--path", help="images path", required=True)
    parser.add_argument("-u", "--user", help="odoo user", required=True)
    parser.add_argument("-P", "--password", help="odoo password", required=True)
    parser.add_argument("-d", "--database", help="database name", default="odoo")
    parser.add_argument("-h", "--host", help="database host", default="http://localhost")
    args = parser.parse_args()

    conn = Connection(args.host, args.database, args.user, args.password)

    # Get list of files
    files = list(Path(args.path).rglob('*.jpg')) + list(Path(args.path).rglob('*.JPG'))
    codes = {code for code in map(lambda pathfile: get_code(pathfile), files)}

    productos = dict()
    for code in codes:
        productos[code] = Product(conn, code)

    for filepath in files:
        p = productos[get_code(filepath)]
        if not p.image_principal:
            p.image_principal = str(filepath)
        else:
            p.image_list.append(str(filepath))

    try:
        for product in productos.values():
            print(product.barcode)
            product.update()

    except Exception as e:
        print(e)

