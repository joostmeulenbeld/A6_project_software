import numpy as np

#find/make matrix A
#find frequency vector f
A=np.random.rand(4,4)
#make zero matrix B for x,y values 
B=np.zeros((4,2))

#for loop for each row in matrix A
for n in range (4):
    #find max value in row A
    h=max(A[n,:])
    k=0
    #find x,y value for the max in row n
    while A[n,k]<>h:
        k=k+1
    #print x,y value in matrix B
    B[n]=n,k
    
    print h
print A
print B


