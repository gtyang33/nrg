# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 21:34:57 2017

@author: Administrator
"""

class c1(object):
    def bar(self):
        return bar
class c2:
    z=10
    _y=10
    def __init__(self,x):
        self.x=x
       # return x init can't return
    def __getattr__(self,name): #属性查找当class中没有改属性时调用
        return getattr(c1,name)
            
a=c2(19)
print('before',a.__dict__)
a.name="yang"
print(a.bar)
print('after',a.__dict__)
print(a.__new__)
#print(a.x)
#print(c2.__dict__)

