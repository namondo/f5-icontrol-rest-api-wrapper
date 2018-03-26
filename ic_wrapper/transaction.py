# -*- coding: utf-8 -*-

from config import *
from icr_lib import *
import ast


def create_trans_session(transaction_id):
    trans_session = F5icrSession(login, pwd, token=True)
    trans_session.update_header(transaction_id)
    return trans_session


class F5icrTransaction(object):
    """"""
    def __init__(self):
        self.logger = logging.getLogger("bigip_api")
        self.trans_url = F5 + "tm/transaction/"
        self.tr_session = F5icrSession(login, pwd, token=True)
        self.id = self._create()
        self.trans_session = create_trans_session(self.id)
        self.url = self.trans_url + str(self.id) + "/"

    def _create(self):
        success, result = self._create_transaction()
        if not success:
            raise Exception(result)
        self.logger.info("TRANSACTION created. ID: {}".format(result['transId']))
        return result['transId']

    def _create_transaction(self):
        try:
            result = self.tr_session.post(self.trans_url, json={})
            r = ast.literal_eval(result.content.replace("false", "False").replace("true", "True"))
            print r
            return True, r
        except BigIPInvalidURL:
            return False, "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            return False, e.message

    def list(self):
        result = self.tr_session.get(self.url + "commands")
        self.logger.debug("TRANSACTION {} commands: {}".format(self.id, result.content))
        return json.loads(result.content)

    def list_command(self, number):
        result = self.tr_session.get(self.url + "commands/{}".format(str(number)))
        return result.content

    def remove(self, number):
        self.logger.info("TRANSACTION {} command {} removed.".format(number, self.id))
        self.tr_session.delete(self.url + "commands/{}".format(str(number)))

    def commit(self):
        result = self.tr_session.patch(self.url, json={"state": "VALIDATING"})
        self.logger.info("TRANSACTION commited. ID: {}".format(self.id))
        self.logger.debug("TRANSACTION {} result: {}".format(self.id, result.content))
        return result.content

    def delete(self):
        try:
            self.tr_session.delete(self.url)
            self.logger.info("TRANSACTION (ID: {}) deleted.".format(self.id))
        except BigIPInvalidURL:
            self.logger.critical("TRANSACTION (ID: {}) FAILED".format(self.id))
            raise Exception("Invalid API URL.")
        except iControlUnexpectedHTTPError as e:
            self.logger.critical("TRANSACTION (ID: {}) FAILED".format(self.id))
            raise Exception(e.message + "(TRANSACTION ID: {})".format(self.id))

