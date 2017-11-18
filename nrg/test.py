# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 23:23:31 2017

@author: Administrator
"""
def get_hop(x):
    def hop(z):
        u=x+z
        e=x+1+z
        return u,e
    def U(y):
        return hop(y)[0]
    def E(y):
        return hop(y)[1]
    return U,E