#!/bin/env python
import re
from pathlib import Path

from .controller.xmlrpc import Connection

def get_code(pathfile: Path):
    name = pathfile.stem

    group = re.split(r'[_-]+', name)
    if len(group) > 1:
        group = group[0]

    return ''.join(group)


def get_recursive_image_list(pathdir: str) -> list[Path]:
    extensions = ['*.jpg', '*.png']

    files = []
    for ext in extensions:
        files += list(Path(pathdir).rglob(ext))

    return files


def send_image_list(conn: Connection, search_folder: str, log):
    """ """
    img_list = get_recursive_image_list(search_folder)
    log.append(f"Images: {len(img_list)}")
    pass
