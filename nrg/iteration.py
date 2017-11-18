# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 20:39:49 2017

@author: Administrator
"""
from numpy import*
from scipy.sparse import diags,kron

__all__=['iteration_H']
u=array([[1,0],[0,0]])
U=kron(u,u)
sz=array([[1,0],[0,-1]])
I=array([[1,0],[0,1]])
sg=array([[0,1],[0,0]])
sd=array([[0,0],[1,0]])
IL=kron(I,I)
szL=kron(sz,sz)
def iteration_H(V,Tlist,Elist,k=20):
    '''nrg iteration
       using Jordan-Wigner transformation make  the creation and annihilation
       operator convert to spin raising and lowering operator
    
    
       V:   Hubbard interation
       Tlist:  an array for hopping coefficient
       Elist:  an array for localized energy
       Lambda: constant for scaling factor
       k:      constant for the total steps of iteration
       '''
    n=len(Elist)
    Elist[0]=-0.5*V
    #Lambda=Lambda**0.5
    #Lambdal=Lambda**arange(n,dtype=float64)
    #Tlist=Tlist*Lambdal[1:]
    #Elist=Elist*Lambdal
    A=[]
    e0=[]
    IL=kron(I,I)
    szL=kron(sz,sz)
    kg1=qg1=kron(sg,I)
    kd1=qd1=kron(sd,I)
    kg2=qg2=kron(sz,sg)
    kd2=qd2=kron(sz,sd)
    H0=Elist[0]*(dot(qg1,qd1)+dot(qg2,qd2))+V*U
    
    for i in arange(k):
        #H0*=Lambda
        H0=kron(H0,IL)
        sg1=kron(szL,kg1)
        sd1=kron(szL,kd1)
        sg2=kron(szL,kg2)
        sd2=kron(szL,kd2)
        t1=Tlist[i]*kron(qg1,IL).dot(sd1)
        t2=Tlist.conj()[i]*sg1.dot(kron(qd1,IL))
        t3=Tlist[i]*kron(qg2,IL).dot(sd2)
        t4=Tlist.conj()[i]*sg2.dot(kron(qd2,IL))
        E=Elist[i+1]*(dot(sg1,sd1)+dot(sg2,sd2))
        H0+=t1+t2+t3+t4+E
        H0=H0.toarray()
        a,b=linalg.eigh(H0)
        #print(Lambdal[i])
        print(a[0])
        #e0.append(a[0]/Lambdal[i])
        
        
        if i<3:
            u=b.reshape(4**(i+1),4,-1) 
        else:
            a=a[:500]
            b=b[:,:500]
            u=b.reshape((-1,4,500))
        u=u.swapaxes(0,1)
        A.append(u)
        H0=diags(a,0).toarray()
        bH=b.conj().T
        qg1=bH.dot(sg1.dot(b))
        qg2=bH.dot(sg2.dot(b))
        qd1=bH.dot(sd1.dot(b))
        qd2=bH.dot(sd2.dot(b))
        szL=kron(szL,kron(sz,sz))
        szL=bH.dot(szL.dot(b))   
    return a,A
def H(V,Tlist,Elist,k):
    #Elist[0]=-0.5*V
    IL=kron(I,I)
    szL=kron(sz,sz)
    kg1=qg1=kron(sg,I)
    kd1=qd1=kron(sd,I)
    kg2=qg2=kron(sz,sg)
    kd2=qd2=kron(sz,sd)
    H1=Elist[0]*(dot(qg1,qd1)+dot(qg2,qd2))+V*U
    for i in arange(k):
        H1=kron(H1,IL)
        t1=Tlist[i]*kron(kg1,IL).dot(kron(szL,kd1))
        t2=Tlist.conj()[i]*kron(szL,kg1).dot(kron(kd1,IL))
        t3=Tlist[i]*kron(kg2,IL).dot(kron(szL,kd2))
        t4=Tlist.conj()[i]*kron(szL,kg2).dot(kron(kd2,IL))
        E=Elist[i+1]*(dot(kron(szL,kg1),kron(szL,kd1))+dot(kron(szL,kg2),kron(szL,kd2)))
        H1+=t1+t2+t3+t4+E
        kg1=kron(szL,kg1)
        kg2=kron(szL,kg2)
        kd1=kron(szL,kd1)
        kd2=kron(szL,kd2)
    a,b=linalg.eigh(H1.toarray())
    return a
        
if __name__=='__main__':
    a=array([10,5,2.5,1.25,0.6])
    b=array([10,5,2.5,1.25])
    H0=iteration_H(10,b,a,k=3)
    h=H(10,b,a,k=3)
    print(abs(h-H0[0])<1e-5)
