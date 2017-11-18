# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:19:48 2017

@author: Administrator
J0hamiltonian
"""
import math
import numpy as np
import scipy.sparse as sps
from scipy.sparse import kron,identity
import scipy.sparse.linalg
def Hamil(N):
    rows = [i for i in range(N-1)]
    cols = [i+1 for i in range(N-1)]
    entries = [2**((N-i-1)/2) for i in range(N-1)]
    H = sps.csr_matrix((entries, (rows, cols)), shape=(N,N))
    H += H.getH()
    H = H.toarray()
    vals=np.linalg.eigvalsh(H)
    evals=[]
   # if N>1000:
        #vals,evecs=sps.linalg.eigsh(H,k=1000, which="SA")
   # else:
        #vals,evec=sps.linalg.eigsh(H,k=N-2, which="SA")
    for i in vals:
        if i>0:
            evals.append(i)
    #print(evals[0])
    #print(evals[1])
    return(math.log(evals[0],2))
    

#if __name__ == "__main__":
  #  Hamil(5)