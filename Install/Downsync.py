# -*- coding: utf-8 -*-

import sys
import improc
import os
import time,datetime
from logger import get_log



os.environ['GDAL_DATA']='C:/Users/Administrator/Anaconda3/envs/improc/Library/share/gdal'
os.environ['PROJ_LIB'] = os.path.join('C:\\', 'Users', 'Administrator', 'Anaconda3', 'envs', 'improc', 'Library', 'share')


message = 'Flight id: {0}, farm id : {1}'.format(str(sys.argv[1]),str(sys.argv[2]))

def upsyn(flight,farm):
    try:
        get_log("Downsync button", message = "Start downsync {}".format(message), infol = 1)
        upsyn = improc.qc.syncer.downsync_registration(flight,farm)
    except Exception as e:
        get_log("Downsync button", "Failed updated ref {}, the error is : {}".format(message,e), errorl = 1)
        print (e)
    return
 
    
up = upsyn(int(sys.argv[1]),int(sys.argv[2]))

print (len(os.environ))