import numpy as np
#from matplotlib.pylab import *

def maxFrequencies(A):
    #############################################################################################
                #Read in Matrix A and set matrix with coordinates of maxes B
    #############################################################################################
    #find/make matrix A
    A[:,0] *= 0.
    
    
    #make zero matrix B for x,y values, same amount of rows as A 
    C=np.shape(A)
    rowsA=C[0]
    columnsA=C[1]
    B=np.zeros((rowsA,2))
    E=np.zeros((rowsA,2))
    VectorZ=np.zeros((rowsA,2))
    factorrange=0.25  #factor of how much of the columns of A range will be used for r n plus and minus
    factorr=0.1       #q=r-round(factorr*r) how much smaller q should be if its bigger than r
    factorq=0.2       #q=q+round(factorq*columnsA) how much smaller the interval gets
    iterationsZ=3     #number of iterations done 
    #############################################################################################
            #First run of least square finding and rewrite matrix B with least square coordinates
    #############################################################################################
    
    #for loop for each row in matrix A
    for n in range (rowsA):
        #find max value in row A
        h=max(A[n,:])
        #set k to zero so we know we have not yet executed the next step
        k=0
        for o in range (columnsA):
            #search row for max values that are the same
            if A[n,o]==h:
                #if max is found it is checked to be existing in matrix B
                #if its still 0,0 then k is set to 1 and the coordinates are printed in B
                if ((B[n]==[0,0]).all() and k==0):
                    B[n]=n,o
                    k=k+1
                #if above is already eprformed (k=1) then this part is executed  
                if (k<>0): 
                    B[n,1]=round(((B[n,1]+o)/2))

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
        #Same as above but iterate within a range next to the least square which gets smaller     
    #############################################################################################
    #define range r interval of 25% one ach side, q will make this smaller each time
    r=round(columnsA*factorrange)
    q=0
    for z in range (int(iterationsZ)):
            #for loop for each row in matrix A
        for n in range (rowsA):
            #find max value in row A CLOSE TO least square
            c=B[n,1]
            
            d=int(c-(2*r)+q)-1
            if d <= 0:
                d = 0
            if d >= columnsA:
                d=columnsA-1
            e=int(c+(2*r)+(-q))
            if e <= 0:
                e = 0
            if e >= columnsA:
                e=columnsA
            
            #find max value in row A between d and e
            h=max(A[n][d:e])
           
            #set k to zero so we know we have not yet executed the next step
            k=0
            
            for o in range (d ,e):
                #search row for max values that are the same
                if A[n,o]==h:
                    #if max is found it is checked to be existing in matrix B
                    #k is set to 1 and the coordinates are printed in B
                    if (k==0):
                        B[n]=n,o
                        VectorZ[n]=n,h
                        k=k+1
                    #if above is already eprformed (k=1) then this part is executed  
                    if (k<>0): 
                        B[n,1]=round(((B[n,1]+o)/2))

            
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
     
    #############################################################################################
            #Give coordinates of the maxes found on the matrix close to its least squares in B
    #############################################################################################
   
    print VectorZ

if __name__ == "__main__":
    maxFrequencies()