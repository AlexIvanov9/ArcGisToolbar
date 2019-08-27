# -*- coding: utf-8 -*-

import sys
import improc
import os

os.environ['GDAL_DATA']='C:/Users/Administrator/Anaconda3/envs/improc/Library/share/gdal'
os.environ['PROJ_LIB'] = os.path.join('C:\\', 'Users', 'Administrator', 'Anaconda3', 'envs', 'improc', 'Library', 'share')

try:
    registered = improc.georeference.georeference_from_gcps(str(sys.argv[1]))
    if 'rank' in os.path.basename(registered):
        improc.singleshot.promote_file(registered,replace=True)
except Exception as e:
    print(e)

