# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:59:36 2017

@author: Administrator
"""

from hybri_sc import get_hybri
from Discretization import quick_map
import math
import matplotlib.pyplot as plt




rho=lambda x:10*log((x+1.001)/(1.001-x))
wlist=linspace(0,1,100)
plt.plot(wlist,rho(wlist))
plt.show()
Tlist,Elist=quick_map(wlist,rho,20,Gap=0)
n=len(Tlist)
y=arange(100)
for j in arange(100):
    y[j]=Tlist[0]**2/(wlist[j]-Elist[0][0])
    for i in arange(1,n):
        y[j]+=Tlist[i]**2/(wlist[j]-Elist[0][i])

    
plt.plot(wlist,y)
plt.show()
    