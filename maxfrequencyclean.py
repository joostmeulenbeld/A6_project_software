import numpy as np

def getSum(interval):
    return np.sum(np.abs(interval))

def getMedian(interval):
    return np.median(np.abs(interval))

def getInitialGuess(amplitudesArray, frequencies):
    lst = []
    for amplitudes in amplitudesArray:
        lst2 = []
        tempSum = np.sum(amplitudes[0:1000])
        oldTenSum = np.sum(amplitudes[0:10])
        lst2.append(tempSum)
        for index in range(10, np.size(amplitudes)-1000, 10):
            newTenSum = np.sum(np.abs(amplitudes[index+990:index+1000]))
            oldTenSum = np.sum(np.abs(amplitudes[index-10:index]))
            tempSum += newTenSum - oldTenSum
            lst2.append(tempSum)

        lst.append(lst2)

    return lst

def getInitialGuessByMethod(A, frequencies, method):
    lst = []
    for interval in range(len(A)): 
        lst2=[]
        absLst = [h if h > 0 else -h for h in A[interval][0:1000]] 
        lst2.append(method(absLst))        
        for i in range((len(A[interval])-3010)/10):
            lst3 = [h if h > 0 else -h for h in A[interval][1000+(i*10):(i*10)+1010]]
            absLst = absLst[10:1000]
            absLst.extend(lst3)
            lst2.append(method(absLst))
        lst.append(lst2)
        print "Searching first estimate in interval: ",interval+1,"/",len(A)
    return lst

def maxFrequencies(wavReader, carrierfrequency, intervalMethodString):
    #############################################################################################
            #Read in Matrix A 
    #############################################################################################
    #find/make matrix A

    frequencies, A = wavReader.getFrequencyAmplitudes()

    A = np.array(A)

    if (intervalMethodString == "sum"):
        lst = getInitialGuess(A, frequencies)
    else:
        intervalMethod = {
                "median": getMedian,
            }.get(intervalMethodString, getSum)
        print(intervalMethod)
        lst = getInitialGuessByMethod(A, frequencies, intervalMethod)

    
    
    
    #############################################################################################
            #First run of least square finding and rewrite matrix B with least square coordinates
    #############################################################################################
        
    maxfreqlist = []
    print "Found first estimate intervals"
    print "Searching for max frequencies in intervals"
    for g in range(len(lst)):
        maxintervalindex = lst[g].index(max(lst[g]))
        maxfreqindex = A[g][((maxintervalindex*10)):(maxintervalindex*10)+1000].argmax()
        maxfreqindex += (maxintervalindex*10)
        maxfreqlist.append(frequencies[maxfreqindex])
        print "Interval: ",g+1,"/",len(lst)," Found Max Freq: ",maxfreqindex
    
    print "Found all maximum frequencies"
            
            
            
            
    #############################################################################################
            #Give coordinates of the maxes found on the matrix close to its least squares in B
    #############################################################################################
    
    for n in range(len(maxfreqlist)):
        maxfreqlist[n]+=carrierfrequency
    print "Added base frequencies"
    return maxfreqlist
    

