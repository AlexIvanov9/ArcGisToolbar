# -*- coding: utf-8 -*-

import improc
import glob,os
import sys
import time
import datetime
from logger import get_log



registered_files = glob.glob(os.path.join('D:\\Flight {}', 'registered', '*{}*.tif').format(sys.argv[1],sys.argv[2]))

message = 'Flight id: {0}, farm id : {1}'.format(str(sys.argv[1]),str(sys.argv[2]))
os.environ['GDAL_DATA']='C:/Users/Administrator/Anaconda3/envs/improc/Library/share/gdal'
os.environ['PROJ_LIB'] = os.path.join('C:\\', 'Users', 'Administrator', 'Anaconda3', 'envs', 'improc', 'Library', 'share')


try:
    get_log("Gen product button", message = "Start gen prod for {}".format(message), infol = 1)
    improc.postprocess.generate_products(registered_files)
    get_log("Gen product button",message =  "Done for Flight {}".format(message), infol = 1)
except Exception as e:
    get_log("Gen product button","Failed gen product for {}, the error is : {}".format(message,e), errorl = 1)
    print(e)


  
try:
    get_log("Gen product button","Start upsync for {}".format(message), infol = 1)
    upsyn = improc.qc.syncer.upsync(int(sys.argv[1]),sys.argv[2])
    get_log("Gen product button","Finished upsync for {}".format(message), infol = 1)
except Exception as e:
    get_log("Gen product button","Failed upsync for {}, the error is : {}".format(message,e), errorl = 1)
    print (e)

print(registered_files)