# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 19:41:50 2017

@author: Administrator
"""

import matplotlib.pyplot as plt
from J0hamiltonian import Hamil
for j in range(0,10):
    b=range(100*j+4,100*j+100,2)
    a=[]
    for i,k in enumerate(b):
        a.append(Hamil(k))
    plt.plot(b,a,'ro')
    plt.show()


