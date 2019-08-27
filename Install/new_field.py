# -*- coding: utf-8 -*-

import improc
import sys
from logger import get_log



message = 'Flight id: {0}, farm id : {1}'.format(str(sys.argv[1]),str(sys.argv[2]))


try:
    get_log("New field button", message = "Start upsync {}".format(message), infol = 1)
    upsyn = improc.qc.syncer.upsync(int(sys.argv[1]),sys.argv[2])
    get_log("New field button", message = "Done upsync {}".format(message), infol = 1)
except Exception as e:
    get_log("New field button", "Failed upsync for {}, the error is : {}".format(message,e), errorl = 1)
    print (e)