#!/usr/bin/python
# -*- coding: utf-8 -*-


from config import *
from bigip_objects import *


rd_url = F5 + "tm/net/route-domain/"


class RouteDomain(BigIPGeneral):
    def __init__(self, icontrol_session, name, **kwargs):
        super(RouteDomain, self).__init__(
            class_url=rd_url,
            session=icontrol_session,
            name=name,
            **kwargs
        )
        if "rd_id" in self.params:
            self.params['id'] = self.params['rd_id']
            del self.params['rd_id']
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(rd_url, self.params['partition'], self.params['name'])
        self.init()


class RouteDomainTrans(BigIPGeneralTransaction):
    def __init__(self, transaction, name, **kwargs):
        super(RouteDomainTrans, self).__init__(
            class_url=rd_url,
            transaction=transaction,
            name=name,
            **kwargs
        )
        if "rd_id" in self.params:
            self.params['id'] = self.params['rd_id']
            del self.params['rd_id']
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(rd_url, self.params['partition'], self.params['name'])
