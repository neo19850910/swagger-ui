#-*- coding:utf8 -*-
#__author__ = "neo"

import random

def rand_name(m):
    db = ['a','b','c','d','e','f','g','h','i','g','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',1,2,3,4,5,6,7,8,9,0]
    result = ""
    for i in range(m):
        result+=str(db[random.randint(0,35)])
    return result