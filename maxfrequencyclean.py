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


    lst = []
    for amplitudes in A:
        lst2 = []
        tempSum = np.sum(np.abs(amplitudes[0:1000]))
        oldTenSum = np.sum(np.abs(amplitudes[0:10]))
        lst2.append(tempSum)
        for index in range(10, np.size(amplitudes)-1000, 10):
            newTenSum = np.sum(np.abs(amplitudes[index+1000:index+1010]))
            oldTenSum = np.sum(np.abs(amplitudes[index-10:index]))
            tempSum += newTenSum - oldTenSum
            # print("joost index: " + str(index) + " sum: " + str(tempSum))
            lst2.append(tempSum)
        # print("joost index 500 value: " + str(lst2[500]))
        # print(np.size(lst2))
        lst.append(lst2)
    
    
    #############################################################################################
            #First run of least square finding and rewrite matrix B with least square coordinates
    #############################################################################################
#    lst=[]    
#    for j in range(len(A)):
#        lst2=[]
#        for i in range((len(A[j])-1000)/10):
#            absLst = [h if h > 0 else -h for h in A[j][i*10:(i*10)+1000]] 
#            lst2.append(sum(absLst))
#        
#        lst.append(lst2)
#        print "Searching first estimate in interval: ",j+1,"/",len(A)
#    maxfreqlist = []
#    print "Found first estimate intervals"
#    print "Searching for max frequencies in intervals"
#    for g in range(len(lst)):
#        print max(lst[g])
#        maxintervalindex = lst[g].index(max(lst[g]))
#        maxfreqindex = A[g][((maxintervalindex*10)):(maxintervalindex*10)+1000].argmax()
#        maxfreqindex +=(maxintervalindex*10)
#        maxfreqlist.append(frequencies[maxfreqindex])
#        print "Interval: ",g+1,"/",len(lst)," Found Max Freq: ",maxfreqindex
#    
#    print "Found all maximum frequencies OLLD"
    ##
    # lst = []
    # for interval in range(len(A)): 
    #     lst2=[]
    #     absLst = [h if h > 0 else -h for h in A[interval][0:1000]] 
    #     lst2.append(sum(absLst))        
    #     for i in range((len(A[interval])-1010)/10):
    #         lst3 = [h if h > 0 else -h for h in A[interval][1000+(i*10):(i*10)+1010]]
    #         absLst = absLst[10:1000]
    #         absLst.extend(lst3)
    #         lst2.append(sum(absLst))
    #     lst.append(lst2)
    #     print "Searching first estimate in interval: ",interval+1,"/",len(A)
        
        
    maxfreqlist = []
    print "Found first estimate intervals"
    print "Searching for max frequencies in intervals"
    for g in range(len(lst)):
        print max(lst[g])
        maxintervalindex = lst[g].index(max(lst[g]))
        maxfreqindex = A[g][((maxintervalindex*10)):(maxintervalindex*10)+1000].argmax()
        maxfreqindex +=(maxintervalindex*10)
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