#!/usr/bin/python
# -*- coding: utf-8 -*-


import ic_wrapper as f5
from ic_wrapper.config import *
from pprint import pprint
import sys


session = f5.F5icrSession(login, pwd, token=True)

print "###################"
print "# Basic examples: #\n"

# (auth) Partition:
part = f5.auth.Partition(session, "test-part")

# Create VLAN (on an auth patition):
vlan_test = f5.net.VLAN(session, "vlan-test", tag=2200)

# Patch VLAN:
vlan_test.patch({'tag': 3000})
print

# IP address to VLAN:
testip = f5.net.IPAddress(session, "TESTIP3", address="1.1.1.3/32", vlan="vlan-test")
pprint(testip.read_params())

# Delete VLAN:
## the associated self ip first
testip.delete()
vlan_test.delete()
print

# ROUTE DOMAIN
rd = f5.ltm.RouteDomain(icontrol_session=session,
                        name="test-rd",
                        rd_id=999)
                        # vlans=["vlan-test"])

pprint(rd.params)
print
# patch:
rd.patch({"routingProtocol": ["BGP"]})
pprint(rd.params)
print

# törlés:
rd.delete()
pprint(rd.params)
print

# Create some objects for transaction:
vlan_test = f5.net.VLAN(session, "vlan-test", tag=2200)
testip = f5.net.IPAddress(session, "TESTIP3", address="1.1.1.3/32", vlan="vlan-test")


print "##########################"
print "#  Transaction examples  #\n"

#### Start ####
trans = f5.F5icrTransaction()
print trans.id

vlan_test = f5.net.VLANTrans(transaction=trans, name="vlan-test", tag=2200)
vlan_test.patch({'tag': 2222})
testip = f5.net.IPAddressTrans(trans, name="TESTIP3", address="1.1.1.3/32", vlan="vlan-test")

# New partition:
new_part = f5.PartitionTrans(transaction=trans, name="test-part2")
new_part.create()
# print
# pprint(part.params)

print trans.list()
trans.commit()
# trans.delete()
print "##########################"


# Cleanup:
_part = f5.Partition(session, name="test-part2")
_part.delete()
vlan_test.delete()
testip.delete()
