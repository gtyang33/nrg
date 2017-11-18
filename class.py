# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 19:38:50 2017

@author: Administrator
"""

class Student(object):
    ''' this is a Student class'''
    count = 0
    books = []
    def __init__(self,name,age):
        self.name=name
        self.age=age
    @property
    def print():
        print(Student.count)
        pass
print(Student.__name__)#类的名字Student
print(Student.__bases__)#类的所有父类组成的元组(<class 'object'>,)
print(Student.__doc__)#类的文档字符串 this is a Student class
print(Student.__module__)#类所属的模块__main__
print(Student.__class__)#类对象的类型<class 'type'>
print(Student.__dict__)#类的字典
a=Student
a.grade=10
print(dir(a))
    
    