import numpy as np

#find/make matrix A
#find frequency vector f

A=np.random.rand(4,4)
B=np.zeros((4,2))
for n in range (4):
    h=max(A[n,:])
    k=0
    while A[n,k]<>h:
        k=k+1
    
    B[n]=n,k
    print h
print A
print B


