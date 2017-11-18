# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 19:37:26 2017

@author: Administrator
"""
def f1(self,a,b):
    return min(a,b)
class Myclass:
    """A simple example class"""
    i=12345
    name=[]
    g1=f1
    
    def f(self):
        return 'hello world'

    def __init__(self,grade,age):
        self.grade=grade
        self.age=age
        self.num=[]
        
    def add_name(self,name):#直接改变class中name元素
        self.name.append(name)
        
    def add_num(self,num):#只改变具体class的num
        self.num.append(num)
        
    def add2(self,num):
        self.add_num(num)
        self.add_num(num)
    g2=f
x=Myclass(97,17)
x.counter=2
while x.counter<10:
    x.counter*=2
print(x.counter)
del x.counter
y=Myclass(20,20)
z=Myclass(30,30)
y.add_name('xiaoming')
y.add_num(10)
print(z.name)
print(y.num)
z.add_name('xiaowang')
z.add_num(20)
print(z.num)
print(y.name)