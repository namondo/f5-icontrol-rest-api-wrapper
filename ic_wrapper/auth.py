#!/usr/bin/python
# -*- coding: utf-8 -*-


from config import *
from bigip_objects import *


partition_url = F5 + "tm/auth/partition/"


class Partition(BigIPGeneral):
    def __init__(self, icontrol_session, name, **kwargs):
        super(Partition, self).__init__(
            class_url=partition_url,
            session=icontrol_session,
            name=name,
            **kwargs
        )
        self.init()


class PartitionTrans(BigIPGeneralTransaction):
    def __init__(self, transaction, name, **kwargs):
        super(PartitionTrans, self).__init__(
            class_url=partition_url,
            transaction=transaction,
            name=name,
            **kwargs
        )
