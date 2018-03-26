from icr_lib import F5icrSession
from config import *
from net import *
from auth import *
from ltm import *
from transaction import F5icrTransaction
import json
import logging.handlers

logger = logging.getLogger("bigip_api")
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
logger.setLevel(LOGLEVEL)
# handler = logging.handlers.SysLogHandler(address='/dev/log')
handler = logging.handlers.RotatingFileHandler(filename="/var/log/bigip-api.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
