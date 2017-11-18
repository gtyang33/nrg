# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 16:39:28 2017

@author: Administrator
"""

from numpy import*
from scipy.integrate import quadrature,cumtrapz
from scipy.interpolate import InterpolatedUnivariateSpline,interp1d


__all__=['Ticker','get_wlist','adaptiveTicker']


class Ticker:
    def __init__(self,Lambda,D,Gap=0):
        self.Lambda=Lambda
        self.D=D
        self.Gap=Gap
    def __call__(self,x,sgn=1):
        D=self.D
        Gap=self.Gap
        Lambda=self.Lambda
        if ndim(x)==0:
            if x>2:
                return ((D-Gap)*Lambda**(2-x)+Gap)*(2*sgn-1)
            else:
                return D*(2*sgn-1)
        else:
            x=x.astype(float)
            res=D*ones(shape(x))
            Bool=x>2
            res[Bool]=(D-Gap)*Lambda**(2-x[Bool])+Gap    #numpy中不允许负幂次，必须x转换为浮点型
            return res*(2*sgn-1)
class adaptiveTicker:
    def __init__(self,Lambda,wlist,Rlist):
        self.Lambda=Lambda
        pmask=wlist>0
        self.wlist=[wlist[~pmask],wlist[pmask]]
        self.Rlist=[Rlist[~pmask],Rlist[pmask]]
        self.D=wlist[-1]
        self.xf=lambda x:Lambda**(2-x)
        
    def __call__(self,x,sgn=0):
        wlist=self.wlist[sgn][::-1]
        Rlist=self.Rlist[sgn][::-1]
        int_r=concatenate([[0],cumtrapz(Rlist,wlist)])
        D=self.D
        RD=int_r[-1]
        Rfun=interp1d(int_r,wlist)
        if ndim(x)==0:
            if x<=2:
                return D
            else:
                return Rfun(RD*self.xf(x))
        else:
            #inds=searchsorted(x,2)
            #xs,xm=split(x,(inds,))
            #res=concatenate([D*ones(len(xs)),iRfunc(RD*self.xf(xm))])
            res=D*ones(len(x),dtype='float64')
            fit_mask=x>2
            res[fit_mask]=Rfun(RD*self.xf(x[fit_mask]))
            return res
        
        
def get_wlist(w0,Nw,mesh_type,D=1,Gap=0):
    '''
    A log mesh can make low energy component of rho(w) more accurate.

    Parameters:
        :w0: float, The starting w for wlist for `log` and `sclog` type wlist, it must be smaller than lowest energy scale!
        :Nw: integer/len-2 tuple, The number of samples in each branch.
        :mesh_type: string, The type of wlist.

            * `linear` -> linear mesh.
            * `log` -> log mesh.
            * `sclog` -> log mesh suited for superconducto8rs.
        :D: Interger/len-2 tuple, the band interval.
        :Gap: Interger/len-2 tuple, the gap interval.

    Return:
        1D array, the frequency space.
    '''
    assert(mesh_type=='linear' or mesh_type=='log' or mesh_type=='sclog')
    if ndim(Gap)==0: Gap=[-Gap,Gap]
    if ndim(D)==0: D=[-D,D]
    if ndim(Nw)==0: Nw=[Nw/2,Nw-Nw/2]

    if mesh_type=='linear':
        wlist=[linspace(-Gap[0],-D[0],Nw[0]),linspace(Gap[1],D[1],Nw[1])]
        return concatenate([-wlist[0][::-1],wlist[1]])
    elif mesh_type=='log':
        wlist=[logspace(log(w0)/log(10),log(-D[0]+Gap[0])/log(10),Nw[0]-1)-Gap[0],logspace(log(w0)/log(10),log(D[1]-Gap[1])/log(10),Nw[1]-1)+Gap[1]]
        #add zeros
        return concatenate([-wlist[0][::-1],array([Gap[0]-1e-30,Gap[1]+1e-30]),wlist[1]])
    elif mesh_type=='sclog':
        wlist=[logspace(log(w0),log(-D[0]+Gap[0]),Nw[0]-1,base=e)-Gap[0],logspace(log(w0),log(D[1]-Gap[1]),Nw[1]-1,base=e)+Gap[1]]
        #add zeros
        return concatenate([-wlist[0][::-1],array([Gap[0]-1e-30,Gap[1]+1e-30]),wlist[1]])
    if (wlist[0][1]-wlist[0][0])==0 or (wlist[1][1]-wlist[1][0])==0:
        raise Exception('Precision Error, Reduce your scaling factor or scaling level!')
        
        
if __name__=='__main__':
    tick=Ticker(2,1)
    #print(wlist)
    ad=adaptiveTicker(2,wlist,rho(wlist))
    a=ad(linspace(1,20))
