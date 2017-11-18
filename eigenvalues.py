# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 09:46:45 2017

@author: Administrator
"""

import numpy as np
import scipy.sparse as sps
from scipy.sparse import kron,identity
import scipy.sparse.linalg
def Hamil(N):
    assert(N>1000)
    transport_matrix=sps.lil_matrix((N,1000))
    possible_eigenstate=[]
    vals,vecs=sps.linalg.eigs(H(N),k=1000)
    for eval,evec in zip(vals,vecs):
        possible_eigenstate.append((eval,evec))
    possible_eigenstate.sort(key=lambda x:x[0])
    for i,(eval,evec) in enumerate(possible_eigenstate[:]):
        transport_matrix[:,i]=evec
    U=transport_matrix.conjugate().T
    effect_H(N)=U.dot(H(N).dot(transport_matrix)
    