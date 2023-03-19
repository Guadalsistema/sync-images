#!/bin/env python3
"""
    Odoo connector
"""

import xmlrpc.client

class Connection:
    """ Xmlrpc odoo helper conenction """
    base: str
    dbase: str
    user: str
    password: str
    _uid: int

    def __init__(self, base, dbase, user, password):
        common = xmlrpc.client.ServerProxy(f'{base}/xmlrpc/2/common')
        self._models = xmlrpc.client.ServerProxy(f'{base}/xmlrpc/2/object')
        self._uid = common.authenticate(dbase, user, password, {})
        self.base = base
        self.user = user
        self.dbase = dbase
        self.password = password

    def execute(self, model: str, method: str, payload, options: dict = {}):
        """
            TODO example
        """
        return self._models.execute_kw(
            self.dbase,
            self._uid,
            self.password,
            model,
            method,
            [payload],
            options
        )

    def write(self, model: str, payload, options: dict = {}):
        """
            TODO example
        """
        return self._models.execute_kw(
            self.dbase,
            self._uid,
            self.password,
            model,
            "write",
            payload,
            options
        )
