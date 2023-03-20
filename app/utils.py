#!/bin/env python
import re
import base64
from pathlib import Path

from .controller.xmlrpc import Connection

def get_code(pathfile: Path):
    name = pathfile.stem
    group = re.split(r'[_-]+', name)
    code = ''
    if len(group) >= 1:
        code = group[0]
    return code


def get_recursive_image_list(pathdir: str) -> list[Path]:
    extensions = ['*.jpg', '*.png']

    files = []
    for ext in extensions:
        files += list(Path(pathdir).rglob(ext))

    return files

def path_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('ascii')

def send_image_list(conn: Connection, search_folder: str, log):
    """ """
    img_list = get_recursive_image_list(search_folder)
    log.append(f"Images: {len(img_list)}")
    
    codes = dict()
    for file in img_list:
        codes[get_code(file)] = []
        codes[get_code(file)].append(str(file))

    for code in codes.keys():
        found = conn.execute("product.template",
                             "search",
                             [[
                                '|',
                                ["barcode", '=', code],
                                ["default_code", '=', code],
                                ['image_1920', '=', False]
                             ]])

        if not found:
            log.append(f"{code} not found or image presented")
            continue
        
        image = codes[code].pop(0)
        conn.execute("product.template",
                   "write",
                    [found[0], {
                        "image_1920": path_to_base64(image),
                    }])

        log.append(f"image({code} - {found[0]}): {image} -> updated")
        
        for idx, image in enumerate(codes[code]):
            conn.execute("product.template",
                       "write",
                        [found[0], {
                            "product_template_image_ids": [(0,0, {'name': f'image: {idx}', 'image_1920': path_to_base64(image)})]
                        }])