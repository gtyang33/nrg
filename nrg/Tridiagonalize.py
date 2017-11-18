# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 20:49:49 2017

@author: Administrator
"""
'''tridiagonalization'''
from numpy import*
import scipy.sparse as sps
from scipy.linalg import qr,inv,sqrtm,eigh,norm

__all__=['tridia_qr','tridia']
def icgs(u,Q,M=None,return_norm=False,maxiter=3):
    '''
    Iterative Classical M-orthogonal Gram-Schmidt orthogonalization.

    Parameters:
        :u: vector, the column vector to be orthogonalized.
        :Q: matrix, the search space.
        :M: matrix/None, the matrix, if provided, perform M-orthogonal.
        :return_norm: bool, return the norm of u.
        :maxiter: int, the maximum number of iteractions.

    Return:
        vector, orthogonalized vector u.
    '''
    assert(ndim(u)==2)
    uH,QH=u.T.conj(),Q.T.conj()
    alpha=0.5
    it=1
    Mu=M.dot(u) if M is not None else u
    r_pre=norm(uH.dot(Mu))
    for it in arange(maxiter):
        u=u-Q.dot(QH.dot(Mu))
        Mu=M.dot(u) if M is not None else u
        r1=norm(uH.dot(Mu))
        #print(r1)
        if r1>alpha*r_pre:
            break
        r_pre=r1
    if r1<=alpha*r_pre:
        warnings.warn('loss of orthogonality @icgs.')
    return (u,r1) if return_norm else u
def tridia(A,q):
    if sps.issparse(A): A=A.toarray()
    alpha=[]
    beta=[]
    qq=q/(sqrt(dot(q.T,q)))
    Q=qq[...,newaxis]
    n=shape(A)[1]
    for i in arange(n):
        q=Q[:,i]
        z=A.dot(q)
        ei=q.conj().T.dot(z)
        Q_i=z-Q.dot(dot(Q.conj().T,z))
        ti=sqrt(Q_i.conj().T.dot(Q_i))
        alpha.append(ei)
        if i==n-1:break
        beta.append(ti)
        Q_i=Q_i/ti
        Q_i=Q_i[:,newaxis]
        #print(Q_i.T.dot(Q))
        Q=append(Q,Q_i,axis=-1)
    beta=array(beta)
    alpha=array(alpha)
    data=array([conj(beta),alpha,beta])
    offsets=array([-1,0,1])
    return data,offsets,Q
def tridia_qr(A,q):
    if sps.issparse(A): A=A.toarray()
    n=shape(q)[-1]
    m=shape(A)[-1]/n
    Q=qr(q,mode='economic')[0]
    alpha=[]
    beta=[]
    for i in range(m):
        Q_i=Q[:,i*n:i*n+n]
        z=A.dot(Q_i)
        temp=z-Q.dot(dot(Q.conj().T,z))
        ei=Q_i.dot(z)
        ti=sqatm(temp.conj().T.dot(temp))
        alpha.append(ei)
        if i==m-1:break
        beta.append(ti)
        temp=temp.dot(inv(ti))
        Q=append(Q,temp,axis=-1)
    data=array([conj(beta),alpha,beta])
    offsets=array([-1,0,1])
    return data,offsets,Q

    
    
        
        
        