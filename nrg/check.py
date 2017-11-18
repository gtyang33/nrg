# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:18:53 2017

@author: Administrator
"""
from numpy import*
import matplotlib.pyplot as plt


__all__=['check_sun','check_hybri','check_scaling']

def gaussian(x,mean,b,weights=1.):
    '''
    Gaussian distribution.

    Parameters:
        :x: ndarray, x or a list of x.
        :mean: num, mean value.
        :b: num, broadening.
        :weights: ndarray, weights of specific spectrum, it should take the same shape as mean.

    Return: ndarray,
    '''
    return 1./b/sqrt(pi)*exp(-((x-mean)/b)**2)*weights
    
def check_sun(w,Tlist,Elist):
    n=len(Tlist)
    hybri=Tlist[0]**2*gaussian(w,Elist[0],abs(0.5*Elist[0]))
    for i in arange(1,n):
        hybri=hybri+Tlist[i]**2*gaussian(w,Elist[i],abs(0.5*Elist[i]))
    return hybri


def check_hybri(w,Tlist,Elist,eta=1e-12):
    z=w+eta*1j
    Tlist=Tlist[::-1]
    Elist=Elist[::-1]
    G0=(z-Elist[0])**(-1)
    for i in arange(1,len(Elist)-1):
        G0=(z-Elist[i]-Tlist[i-1]*G0*Tlist.conj()[i-1])**(-1)
        selfE=Tlist[-1]*G0*Tlist.conj()[-1]
    res=1j/2/pi*(selfE-selfE.conj())
    return res

def check_scaling(Tlist):
    n=len(Tlist)
    tlist=log(Tlist)
    plt.plot(arange(n),tlist)
    