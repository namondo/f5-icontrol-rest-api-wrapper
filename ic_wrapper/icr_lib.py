# -*- coding: utf-8 -*

# from config import *
import json
from icontrol.exceptions import *
from icontrol.session import *
# from bigip_objects import BigIPGeneral
# from bigip_transactional_objects import BigIPGeneralTransaction
# import logging.handlers


class F5icrSession(iControlRESTSession):
    def update_header(self, transaction_id):
        self.session.headers.update({'X-F5-REST-Coordination-Id': str(transaction_id)})


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
