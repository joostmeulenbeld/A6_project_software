import numpy as np

#############################################################################################
            #Read in Matrix A and set matrix with coordinates of maxes B
#############################################################################################

#find/make matrix A
#find frequency vector f
A=np.array([[0.,0.,0.,0.,0.,0.,1.],
            [0.,1.,0.,0.,0.,1.,0.],
            [0.,0.,0.,0.,1.,0.,0.],
            [0.,0.,0.,1.,0.,0.,0.],
            [0.,0.,1.,0.,0.,1.,1.],
            [0.,1.,0.,0.,1.,0.,0.],
            [1.,0.,0.,1.,0.,0.,1.]])
#make zero matrix B for x,y values, same amount of rows as A 
C=np.shape(A)
rowsA=C[0]
columnsA=C[1]
B=np.zeros((rowsA,2))
factorrange=0.75 #factor of how much of the columns of A range will be used
factorr=0.25      #q=r-round(factorr*r) how much smaller q should be if its bigger than r
factorq=0.1      #q=q+round(factorq*columnsA) how much smaller the interval gets
#############################################################################################
        #First run of least square finding and rewrite matrix B with elast square coordinates
#############################################################################################

#for loop for each row in matrix A
for n in range (rowsA):
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
sigma = np.ones(rowsA)
x0    = np.array([0.0, 0.0, 0.0, 0.0])
import scipy.optimize as optimization

#print values for the least square function
[popt, pcov] = optimization.curve_fit(func, xdata, ydata, x0, sigma)

#look for closest points to the least square function
for m in range(rowsA):
    p=popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0]
    pr=round(popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0])  
    #replace values of B by closest values in the least square  
    B[m]=[m,pr]
    
print B #for check, new matrix with least square values

#############################################################################################
       #Same as above but iterate within a range next to the least square which gets smaller     
#############################################################################################
#define range r interval of 25% one ach side, q will make this smaller each time
r=round(columnsA*factorrange)
print r
q=0
for z in range (5):
        #for loop for each row in matrix A
    for n in range (rowsA):
        #find max value in row A CLOSE TO least square
        c=B[n,1]
        
        d=int(c-r+q)
        if d <= 0:
            d = 0
        e=int(c+(2*r)+(-q))
        if e <= 0:
            e = 0
        if e >= columnsA:
            e=columnsA
        k=0
        
     #   print "-"
      #  print n
       # print c
        #print d
        #print e
        h=max(A[n][d:e])
        #print h
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
    sigma = np.ones((rowsA))
    x0    = np.array([0.0, 0.0, 0.0, 0.0])
    import scipy.optimize as optimization
    
    #print values for the least square function
    [popt, pcov] = optimization.curve_fit(func, xdata, ydata, x0, sigma)
    
    
    #look for closest points to the least square function
    for m in range(rowsA):
        p=popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0]
        pr=round(popt[0] + popt[1]*B[m,0] + popt[2]*B[m,0]*B[m,0] + popt[3]*B[m,0]*B[m,0]*B[m,0])  
        #replace values of B by closest values in the least square  
        B[m]=[m,pr]
    #if q gets larger than r(range) it gets maxed to r minus 10 percent
    q=q+round(factorq*columnsA)
    if q >= r:
        q=r-round(factorr*r)
    print "next q is",q
    print "the r is", r
    print B

#############################################################################################
        #Give coordinates of the maxes found on the matrix close to its least squares in B
#############################################################################################
print B 
#print popt
#for s in range(rowsA):
   # B[s,1]=A[s,B[s,1]]
#print A
#print B


