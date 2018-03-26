#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from bigip_objects import *


ipa_url = F5 + "tm/net/self/"
vlan_url = F5 + "tm/net/vlan/"


class VLAN(BigIPGeneral):
    def __init__(self, icontrol_session, name, **kwargs):
        super(VLAN, self).__init__(
            class_url=vlan_url,
            session=icontrol_session,
            name=name,
            **kwargs
        )
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(vlan_url, self.params['partition'], self.params['name'])
        self.init()


class VLANTrans(BigIPGeneralTransaction):
    def __init__(self, transaction, name, **kwargs):
        super(VLANTrans, self).__init__(
            class_url=vlan_url,
            transaction=transaction,
            name=name,
            **kwargs
        )
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(vlan_url, self.params['partition'], self.params['name'])


class IPAddress(BigIPGeneral):
    def __init__(self, icontrol_session, name, **kwargs):
        super(IPAddress, self).__init__(
            class_url=ipa_url,
            session=icontrol_session,
            name=name,
            **kwargs
        )
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(vlan_url, self.params['partition'], self.params['name'])
        self.init()


class IPAddressTrans(BigIPGeneralTransaction):
    def __init__(self, transaction, name, **kwargs):
        super(IPAddressTrans, self).__init__(
            class_url=ipa_url,
            transaction=transaction,
            name=name,
            **kwargs
        )
        if "partition" in self.params:
            self.url = "{}~{}~{}".format(vlan_url, self.params['partition'], self.params['name'])
