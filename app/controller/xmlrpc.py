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
    uid: int = 0

    def __init__(self, base, dbase, user, password):
        self.base = base
        self.user = user
        self.dbase = dbase
        self.password = password

    def connect(self):
        common = xmlrpc.client.ServerProxy(f'{self.base}/xmlrpc/2/common')
        self._models = xmlrpc.client.ServerProxy(f'{self.base}/xmlrpc/2/object')
        self.uid = common.authenticate(self.dbase, self.user, self.password, {})

    def execute(self, model: str, method: str, payload, options: dict = {}):
        """ execute direct function"""
        return self._models.execute_kw(
            self.dbase,
            self.uid,
            self.password,
            model,
            method,
            payload,
            options)
