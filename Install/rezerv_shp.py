# -*- coding: utf-8 -*-

import improc
import sys
import os
import time

os.environ['GDAL_DATA']='C:/Users/Administrator/Anaconda3/envs/improc/Library/share/gdal'
os.environ['PROJ_LIB'] = os.path.join('C:\\', 'Users', 'Administrator', 'Anaconda3', 'envs', 'improc', 'Library', 'share')
try:
    print (sys.argv[1])
    print (sys.argv[2])
    improc.dbops.spatial.save_visit_shapefile(int(sys.argv[1]),int(sys.argv[2]), overwrite=True )
except Exception as e:
    print (e)
