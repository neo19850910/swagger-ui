#-*- coding:utf8 -*-
#__author__ = "neo"

import ConfigParser
import os
import logging

def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '\config.conf'
    config.read(path)
    return config.get(section, key)
