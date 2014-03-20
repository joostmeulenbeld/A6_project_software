import numpy as np

#find/make matrix A
#find frequency vector f
#A=np.random.rand(4,4)
A=np.array([[0.,0.,0.,1.],[0.,0.,1.,0.],[0.,1.,0.,0.],[1.,0.,0.,0.]])
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

# Chose a model that will create bimodality.
def func(x, a, b, c ,d):
    return a + b*x #+c*x*x +d*x*x*x

# Create toy data for curve_fit.
xdata = B[:,0]
ydata = B[:,1]
sigma = np.array([1.0,1.0,1.0,1.0])
x0    = np.array([0.0, 0.0, 0.0, 0.0])
import scipy.optimize as optimization

print optimization.curve_fit(func, xdata, ydata, x0, sigma)





