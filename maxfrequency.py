import numpy as np

#############################################################################################
            #Read in Matrix A and set matrix with coordinates of maxes B
#############################################################################################

#find/make matrix A
#find frequency vector f

A=np.array([[0.,0.,0.,0.,0.,0.,1.],
            [0.,0.,1.,0.,0.,1.,0.],
            [0.,1.,0.,0.,1.,0.,0.],
            [0.,0.,0.,1.,0.,1.,0.],
            [0.,0.,1.,0.,0.,1.,0.],
            [0.,1.,0.,0.,1.,0.,0.],
            [1.,0.,0.,0.,0.,0.,0.]])
#make zero matrix B for x,y values 
B=np.zeros((7,2))
columnsA=7

#############################################################################################
        #First run of least square finding and rewrite matrix B with elast square coordinates
#############################################################################################

#for loop for each row in matrix A
for n in range (7):
    #find max value in row A
    h=max(A[n,:])
    k=0
    #find x,y value for the max in row n
    while A[n,k]<>h:
        k=k+1
    #print x,y value in matrix B
    B[n]=n,k
    
# Chose a model that will create bimodality.
def func(x, a, b, c ,d):
    return a + b*x +c*x*x +d*x*x*x

# Create the data for curve_fit.
xdata = B[:,0]
ydata = B[:,1]
sigma = np.ones(columnsA)
x0    = np.array([0.0, 0.0, 0.0, 0.0])
import scipy.optimize as optimization

#print values for the least square function
[popt, pcov] = optimization.curve_fit(func, xdata, ydata, x0, sigma)

#look for closest points to the least square function
for m in range(7):
    p=popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0]
    pr=round(popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0])  
    #replace values of B by closest values in the least square  
    B[m]=[m,pr]
    
print B #for check, new matrix with least square values

#############################################################################################
       #Same as above but iterate within a range next to the least square which gets smaller     
#############################################################################################

q=0
for z in range (3):
        #for loop for each row in matrix A
    for n in range (7):
        #find max value in row A CLOSE TO least square
        c=B[n,1]
        
        d=int(c-2+q)
        if d <= 0:
            d = 0
        e=int(c+5-q)
        if e <= 0:
            e = 0
        if e >= 7:
            e=7
        k=0
        
        print "-"
        print n
        print c
        print d
        print e
        h=max(A[n][d:e])
        print h
        #find x,y value for the max in row n in A
        while A[n,d]<>h:
            d=d+1
           
            
        #print x,y value in matrix B, c being the new place of the CLOSE TO least square maximum
        B[n]=n,d
        
        
    # Chose a model that will create bimodality.
    def func(x, a, b, c ,d):
        return a + b*x +c*x*x +d*x*x*x
    
    # Create the data for curve_fit.
    xdata = B[:,0]
    ydata = B[:,1]
    sigma = np.ones((columnsA))
    x0    = np.array([0.0, 0.0, 0.0, 0.0])
    import scipy.optimize as optimization
    
    #print values for the least square function
    [popt, pcov] = optimization.curve_fit(func, xdata, ydata, x0, sigma)
    
    
    #look for closest points to the least square function
    for m in range(7):
        p=popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0]
        pr=round(popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0])  
        #replace values of B by closest values in the least square  
        B[m]=[m,pr]
    q=q+1
    print "next q is",q
    print B

#############################################################################################
        #Give coordinates of the maxes found ion the matrix close to its least squares in B
#############################################################################################
print B 