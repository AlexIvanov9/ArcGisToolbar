# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 00:56:37 2019

@author: Administrator
"""

import os
import time
import datetime
import logging


def get_log(nameapp,message,infol = None, errorl = None):
    tfolder = os.path.join('C:\\', 'Users', 'Administrator', 'Desktop','Toolbar')# path to save log file 
    if not os.path.exists(tfolder):
        os.makedirs(tfolder)
    now = datetime.datetime.now()
    name = now.strftime("%Y-%m-%d")
    logfile = os.path.join(tfolder,str(name) + '.log')
    logger = logging.getLogger(nameapp)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M")
    handler.setFormatter(formatter)
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(handler)
    if infol is not None:
        logger.info(message)
    if errorl is not None:
        logger.error(message)
    
    return 