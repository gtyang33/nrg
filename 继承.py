# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 21:09:53 2017

@author: Administrator
"""

class student:
    s=10
    __s=100
    def __init__(self):
        self.num=[]
        self.grade=[]
        self.name=[]
    
    def get_name(self,name):
        self.name=name
        
    def get_num(self,num):
        self.num=num
        
    def get_grade(self,grade):
        self.grade=grade
a=student()
a.get_grade(10)
print(a.grade)
class graduate(student):
    __s=101
    def __init__(self):
        self.age=[]
    
    def get_age(self,age):
        self.age=age
b=graduate()
b.get_age(20)
b.get_name('xiaowang')
a=student()
print(b.name)
print(b._graduate__s)
print(a._student__s)