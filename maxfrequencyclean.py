import numpy as np

def maxFrequencies(wavReader, carrierfrequency):
    #############################################################################################
                #Read in Matrix A and set matrix with coordinates of maxes B
    #############################################################################################
    #find/make matrix A
       
    
    #make zero matrix B for x,y values, same amount of rows as A 
    A = wavReader.getAmplitudesRimsky()
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

    print "Noise filtering done!"
    
    #############################################################################################
            #First run of least square finding and rewrite matrix B with least square coordinates
    #############################################################################################
    lst=[]    
    for j in range(len(A)):
        lst2=[]
        for i in range(len(A[j])/1000):
            absLst = [h if h > 0 else -h for h in A[j][i*1000:(i*1000)+1000]] 
            lst2.append(sum(absLst))
            
        lst.append(lst2)
        print "Searching in interval: ",j
    maxfreqlist = []
    print "Found first estimate interval"
    frequencies = wavReader.getFrequencies()
    for g in range(len(lst)):
        maxintervalindex = lst[g].index(max(lst[g]))
        maxfreqindex = A[g][((maxintervalindex*1000)-1000):(maxintervalindex*1000)+1000].argmax()
        maxfreqindex +=(maxintervalindex*1000)-1000
        maxfreqlist.append(frequencies[maxfreqindex])
        print "Interval: ",g," Found Max Freq: ",maxfreqindex
    
    print "Found all maximum frequencies"
     
    #############################################################################################
            #Give coordinates of the maxes found on the matrix close to its least squares in B
    #############################################################################################
    #print B
    for n in range(len(maxfreqlist)):
        maxfreqlist[n]+=carrierfrequency

    return maxfreqlist
    print "Added base frequencyS"

#if __name__ == "__main__":
 #maxFrequencies()