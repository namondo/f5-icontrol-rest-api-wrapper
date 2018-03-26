# -*- coding: utf-8 -*-

from icr_lib import *


class BigIPGeneral(object):
    """Defines the common parts of F5 BIG-IP's objects."""
    def __init__(self, class_url, session, name,
                 create_if_not_exists=True, debug=True, **kwargs):
        self.debug = debug
        self.class_url = class_url
        self.session = session
        self.params = dict(name=name)
        self.name = self.params['name']
        if kwargs:
            self.params.update(kwargs)
        self.create_if_not_exists = create_if_not_exists
        self.url = self.class_url + self.name
        self.logger = logging.getLogger("bigip_api")

    def init(self):
        if not self._object_exists() and self.create_if_not_exists:
            self.create()
        self.update()

    def _object_exists(self):
        try:
            _ = self.session.get(self.url)
            self.logger.debug("Object {} already exists.".format(self.name))
            return True
        except iControlUnexpectedHTTPError:
            return False

    def read_params(self):
        try:
            result = self.session.get(self.url)
            self.params = json.loads(result.content)
            return self.params
        except BigIPInvalidURL:
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            self.logger.error(e)
            return e.errno, e.message

    def _create(self):
        try:
            result = self.session.post(self.class_url, json=self.params)
            return True, result.content
        except BigIPInvalidURL as e:
            self.logger.error(e)
            return False, "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            self.logger.error(e)
            return False, e.message

    def create(self):
        success, msg = self._create()
        if not success:
            self.logger.critical(msg)
            raise Exception(msg)
        self.logger.info("{} created.".format(self.name))
        return None

    def patch(self, patch):
        if type(patch) is not dict:
            return "Patch must be a hash (dict)."
        try:
            result = self.session.patch(self.url, json=patch)
            self.update()
            self.logger.info("{} modified.".format(self.name))
            return result.content
        except BigIPInvalidURL as e:
            self.logger.error(e)
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            self.logger.error(e)
            return e.message

    def delete(self):
        valid = 'name' in self.params
        if not valid:
            return "RD is not defined. Cannot delete."
        try:
            self.session.delete(self.url)
            self.params = {'name': "DELETED"}
            self.logger.info("Object '{}' deleted.".format(self.name))
            return None
        except BigIPInvalidURL:
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            return e.message

    """Updates object parameters (params)"""

    def update(self):
        self.read_params()


class BigIPGeneralTransaction(object):
    """Defines the common parts of F5 BIG-IP's objects for transactional operations."""
    def __init__(self, class_url, transaction, name, debug=True, **kwargs):
        self.debug = debug
        self.class_url = class_url
        self.session = transaction.trans_session
        self.params = dict(name=name, transaction_id=transaction.id)
        self.name = self.params['name']
        self.tr_id = self.params['transaction_id']
        if kwargs:
            self.params.update(kwargs)
        self.url = self.class_url + self.params['name']
        self.logger = logging.getLogger("bigip_api")

    def read_params(self):
        try:
            result = self.session.get(self.url)
            self.params = json.loads(result.content)
            return self.params
        except BigIPInvalidURL:
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            return e.errno, e.message

    def _create(self):
        try:
            result = self.session.post(self.class_url, json=self.params)
            return True, result.content
        except BigIPInvalidURL as e:
            self.logger.error(e)
            return False, "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            self.logger.error(e)
            return False, e.message

    def create(self):
        success, msg = self._create()
        if not success:
            self.logger.critical(msg)
            raise Exception(msg)
        self.logger.info("TRANSACTION ({}): Object '{}' creating added."
                         .format(self.tr_id, self.name))
        return None

    def patch(self, patch):
        if type(patch) is not dict:
            return "Patch must be a hash (dict)."
        try:
            result = self.session.patch(self.url, json=patch)
            self.params.update(patch)
            self.logger.info("TRANSACTION ({}): Object '{}' parameter(s) update added."
                             .format(self.tr_id, self.name))
            return result.content
        except BigIPInvalidURL:
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            return e.message

    def delete(self):
        valid = 'name' in self.params
        if not valid:
            return "Object is not defined. Cannot delete."
        try:
            self.session.delete(self.url)
            self.params = {'name': "DELETED"}
            self.logger.info("TRANSACTION ({}): Object '{}' deleted."
                             .format(self.tr_id, self.name))
            return None
        except BigIPInvalidURL as e:
            self.logger.error(e)
            return "Invalid API URL."
        except iControlUnexpectedHTTPError as e:
            self.logger.error(e)
            return e.message
