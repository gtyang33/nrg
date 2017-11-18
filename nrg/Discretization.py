# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 09:40:41 2017

@author: Administrator
"""

'''discretization'''
import matplotlib.pyplot as plt
from numpy import*
from numpy.linalg import eigh,inv,eigvalsh,norm
from scipy.interpolate import InterpolatedUnivariateSpline,interp1d
from scipy.integrate import quadrature,cumtrapz
from Tridiagonalize import tridia
from iteration import iteration_H
from hybri_sc import get_hybri
from ticker import Ticker,get_wlist,adaptiveTicker
from check import*

__all__=['Quick_map','construct']
class Simpleband:
    ''' class for singleband map to discretization:
        
        rho:      a function hybridization function 
        wlist:    an 1D array for frequency space
        rholists: an array for hybridization define on the frequency space
        ticker:   a Ticker 
        '''
    def __init__(self,wlist,rholist,ticker):
        pmask=wlist>0
        self.D=[wlist[0],wlist[-1]]
        self.wlists=[wlist[~pmask][::-1],wlist[pmask]]
        self.rholists=[rholist[~pmask][::-1],rholist[pmask]]
        self.ticker=ticker
        self.int_rho=[append([0],cumtrapz(rholist,wlist)) for rholist,wlist in zip(self.rholists,self.wlists)]
        
    def get_hop(self,xmax,sgn=1,Nx=5000):
        ticker=self.ticker
        wlist=self.wlists[sgn]
        int_rho=self.int_rho[sgn]
        Rfun=interp1d(wlist,int_rho)
        Tfun=lambda x:sqrt(abs(Rfun(ticker(x,sgn))-Rfun(ticker(x+1,sgn))))
        xlist=array(linspace(1,xmax,Nx))
        NewRfun=interp1d(int_rho,wlist)
        Newint_rho=append([0],cumtrapz(Rfun(ticker(xlist,sgn)),xlist))
        print(sgn)
        RRfun=interp1d(xlist,Newint_rho)
        Efun=lambda x:NewRfun(RRfun(x+1)-RRfun(x))
        return Tfun,Efun
class Multiband():
    def __init__(self,wlist,rho,tickers):
        self.wlist=wlist
        self.rho=rho
        self.rholist=array([rho(w)for w in wlist])
        self.ticker=tickers
        self.nband=self.rholist.shape[-1]
        self.rho_evals=array([eigvalsh(rho) for rho in self.rholist])
        self.multiband=[]
        for i in range(self.nband):
            self.multiband.append(Simpleband(self.wlist,self.rho_evals[:,i],self.ticker))
    def get_hop(self,xmax,sgn=0,Nx=500000):
        Ef=[]
        Tf=[]
        for i in arange(self.nband):
            tf,ef=self.multiband[i].get_hop(xmax=xmax,Nx=Nx,sgn=sgn)
            Ef.append(ef)
            Tf.append(tf)
        def Efun(arr):
            E=[]
            ei0=Inf
            Shape=arr.shape
            for j in arange(Shape[0]):
                for k in arange(Shape[1]):
                    for i in arange(self.nband):
                        ei=Ef[i](arr[j][k])
                        E.append(ei)
                        #if ei0-ei>1e-12:
                            #Ui=eigh(self.rho(ei))[1]
                            #ei0=ei
                        #U.append(Tf[i](arr[j][k])*Ui[:,i])
            Ee=array([E]).reshape((-1,self.nband))
            E=array([diag(e) for e in Ee])
            return E
        def Tfun(arr):
            U=[]
            ei0=Inf
            Shape=arr.shape
            for j in arange(Shape[0]):
                for k in arange(Shape[1]):
                    for i in arange(self.nband):
                        ei=Ef[i](arr[j][k])
                        if ei0-ei>1e-12:
                            Ui=eigh(self.rho(ei))[1]
                            ei0=ei
                        U.append(Tf[i](arr[j][k])*Ui[:,i])
            return U
        return Tfun,Efun
def Quick_map(wlist,rho,N,D=1,z=[0],Nx=5000,Lambda=2,Gap=0,Tickertype='Ticker'):
    z=array(z)
    nz=len(z)
    lat=[]
    branch=[0,1]
    for i in z:
        lat.append(arange(1+i,N+1+i))
    lat=array(lat)
    if Tickertype=='Ticker':
        Tick=Ticker(Lambda,D,Gap)
    if Tickertype=='adaptiveTicker':
        Tick=adaptiveTicker(Lambda,wlist,rho(wlist))
    rholist=array([rho(w) for w in wlist])
    if ndim(rholist)==1:
        band=Simpleband(wlist,rholist,Tick)
    else:band=Multiband(wlist,rho,Tick)
    funcs=[band.get_hop(xmax=N+2,Nx=Nx,sgn=s) for s in branch]
    Tf0=array([funcs[0][0](lat)]).reshape((nz,N,-1))
    Tf1=array([funcs[1][0](lat)]).reshape((nz,N,-1))
    Ef0=array([funcs[0][1](lat)]).reshape((nz,N,-1))
    Ef1=array([funcs[1][1](lat)]).reshape((nz,N,-1))
    a0=Tf0[0,:]
    a1=Tf1[0,:]
    b0=Ef0[0,:]
    b1=Ef1[0,:]
    if nz!=1:
        for i in arange(1,nz):
            a0=a0+Tf0[i,:]
            a1=a1+Tf1[i,:]
            b0=b0+Ef0[i,:]
            b1=b1+Ef1[i,:]
    a=append(a0,a1)
    b=append(b0,b1)
    tf=array(a)/nz
    ef=array(b)/nz
    return tf,ef
        
def construct_H(tf,ef,e0):
    xlen=len(ef)
    H0=zeros([xlen+1,xlen+1])
    H0[0,0]=e0
    for i in arange(xlen):
        H0[i+1,i+1]=ef[i]
        H0[0,i+1]=H0[i+1,0]=tf[i]
        H=tridia(H0,H0[:,0])
    return H

if __name__=='__main__':
    wlist=get_wlist(1e-12,1000,'log')
    #wlist=append(linspace(-1,0,100000),linspace(0,1,100000))
    #rho=lambda x:log((x+1j*1e-12+1.001)/(1.001-x-1j*1e-12))-log((x-1j*1e-12+1)/(1-x+1j*1e-12))
    rho=lambda x:0.5*abs(x)
    Z=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    T,E=Quick_map(wlist,rho,17,z=Z,Gap=0,Tickertype='adaptiveTicker')
    '''
    pmask=T<T[0]
    T=T[pmask]
    E=E[pmask]
    sun=check_sun(wlist,T,E)
    plt.plot(wlist,sun)
    plt.show()
    #print(E)
    b=construct_H(T,E,0)
    Tlist=b[0][0]
    Elist=b[0][1][1:]
    hybri=check_hybri(wlist,Tlist,Elist)
    plt.plot(wlist,hybri)
    plt.show()
    #plt.plot(wlist,rho(wlist))
    #H=iteration_H(V=-8,Tlist=b[0][0],Elist=b[0][1],k=30)
    #Rho=get_hybri(0.1,1)
    #t,e=quick_map(wlist,Rho,6,z=Z)
    #plt.plot(rho(wlist))
    '''
        
    
            
            
            
        
        
        


        