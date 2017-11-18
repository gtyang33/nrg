# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:47:01 2017

@author: Administrator
"""
import numpy as np
d=ones(10)
class student:
    def __call__(self,x):
        self.x=x
    def __init__(self,num,grade,name):
        self.num=num
        self.grade=grade
        self.name=name
class Teacher:
    def __new__(cls):
        return student

a=Teacher()
