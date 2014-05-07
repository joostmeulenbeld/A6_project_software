import numpy as np

def maxFrequencies(wavReader, carrierfrequency):
    #############################################################################################
            #Read in Matrix A 
    #############################################################################################
    #find/make matrix A

    A, frequencies = wavReader.getNarrowSpectra()
    A = np.array(A)

    # frequencies = wavReader.getFrequencies()
    # A = wavReader.getAmplitudesRimsky()

    # C=np.shape(A)
    # rowsA=C[0]
    # columnsA=C[1]
    
    # for n in range(rowsA):
    #     for o in range(columnsA):
    #         if o<=110000 or o>=140000:
    #             A[n][o]=0

    # print "Cut Off Done"

    #############################################################################################
            #noise filtering removing 0->75000 and 125000->250000
    #############################################################################################


    
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
        print "Searching first estimate in interval: ",j+1,"/",len(A)
    maxfreqlist = []
    print "Found first estimate intervals"
    print "Searching for max frequencies in intervals"
    for g in range(len(lst)):
        maxintervalindex = lst[g].index(max(lst[g]))
        maxfreqindex = A[g][((maxintervalindex*1000)-1000):(maxintervalindex*1000)+1000].argmax()
        maxfreqindex +=(maxintervalindex*1000)-1000
        maxfreqlist.append(frequencies[maxfreqindex])
        print "Interval: ",g+1,"/",len(lst)," Found Max Freq: ",maxfreqindex
    
    print "Found all maximum frequencies"
     
    #############################################################################################
            #Give coordinates of the maxes found on the matrix close to its least squares in B
    #############################################################################################
    
    for n in range(len(maxfreqlist)):
        maxfreqlist[n]+=carrierfrequency
    print "Added base frequencys"
    return maxfreqlist
    

#if __name__ == "__main__":
 #maxFrequencies()