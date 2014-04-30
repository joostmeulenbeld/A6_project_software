import numpy as np
#from matplotlib.pylab import *

def maxFrequencies(A, lowfrequency):
    #############################################################################################
                #Read in Matrix A and set matrix with coordinates of maxes B
    #############################################################################################
    #find/make matrix A
       
    
    #make zero matrix B for x,y values, same amount of rows as A 
    C=np.shape(A)
    rowsA=C[0]
    columnsA=C[1]
    B=np.zeros((rowsA,2))
    E=np.zeros((rowsA,2))
    VectorZ=np.zeros((rowsA,2))
    SUM=0

    #############################################################################################
            #noise filtering removing 0->75000 and 125000->250000
    #############################################################################################
   
    for n in range(rowsA):
        for o in range(columnsA):
            if o<=75000 or o>=175000:
                A[n][o]=0
            if A[n][o]>=0.00015:
                A[n][o]=0
    print n      
    
    #############################################################################################
            #First run of least square finding and rewrite matrix B with least square coordinates
    #############################################################################################
    
                    
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
        
   
     
    #############################################################################################
            #Give coordinates of the maxes found on the matrix close to its least squares in B
    #############################################################################################
    #print B
    for n in range(rowsA):
        B[n][1]=(B[n][1])+lowfrequency

    
    return B
    

#if __name__ == "__main__":
 #maxFrequencies()