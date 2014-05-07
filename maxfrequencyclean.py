import numpy as np

def getSum(interval):
    return np.sum(np.abs(interval))

def getMedian(interval):
    return np.median(np.abs(interval))

def getInitialGuess(amplitudesArray, frequencies, method):
    lst = []
    for amplitudes in amplitudesArray:
        lst2 = []
        tempSum = method(amplitudes[0:1000])
        oldTenSum = method(amplitudes[0:10])
        lst2.append(tempSum)
        for index in range(10, np.size(amplitudes)-1000, 10):
            newTenSum = np.sum(np.abs(amplitudes[index+1000:index+1010]))
            oldTenSum = np.sum(np.abs(amplitudes[index-10:index]))
            tempSum += newTenSum - oldTenSum
            lst2.append(tempSum)

        lst.append(lst2)

    return lst

def maxFrequencies(wavReader, carrierfrequency):
    #############################################################################################
            #Read in Matrix A 
    #############################################################################################
    #find/make matrix A

    A, frequencies = wavReader.getNarrowSpectra()
    A = np.array(A)

    lst = getInitialGuess(A, frequencies, getMedian)
    
    
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
    

