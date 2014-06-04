import numpy as np
from math import factorial as fact

width=1000

def getSum(interval):
    return np.sum(np.abs(interval))

def getMedian(interval):
    return np.median(np.abs(interval))

def getInitialGuess(amplitudesArray, frequencies):
    lst = []
    for amplitudes in amplitudesArray:
        lst2 = []
        tempSum = np.sum(np.abs(amplitudes[0:width]))
        oldTenSum = np.sum(np.abs(amplitudes[0:10]))
        lst2.append(tempSum)
        for index in range(10, np.size(amplitudes)-width, 10):
            newTenSum = np.sum(np.abs(amplitudes[index+990:index+width]))
            oldTenSum = np.sum(np.abs(amplitudes[index-10:index]))
            tempSum += newTenSum - oldTenSum
            lst2.append(tempSum)

        lst.append(lst2)

    return lst

def derivative(x, y, t, mode="forward"):

    # if sum(np.diff(x, n=2)) != 0:
    #     return None #check if the x spacing is constant
    #let's assume this is correct for computational quickness
    bino = lambda n, k: fact(n)/(fact(k)*fact(n-k))

    h = float(x[1]-x[0])
    derivatives = [0]*(len(y))

    if mode=="forward":
        f = lambda n, i, y: (-1)**i*bino(n,i)*y[n-i]
        x0=x[0]
        derivatives[0]=y[0]
    else:
        f = lambda n, i, y: (-1)**i*bino(n,i)*y[-i-1]
        x0=x[-1]
        derivatives[0]=y[-1]

    for n in range(1,len(y)):
        for i in range(0, n+1):
            # print(n, i, f(n, i, y, bino))
            derivatives[n] += f(n, i, y)
        derivatives[n] /= h**n
    return sum([derivatives[n]/fact(n)*(t-x0)**n for n in range(len(y))])


def getInitialGuessByMethod(A, frequencies, method):
    lst = []
    for interval in range(len(A)): 
        lst2=[]
        absLst = [h if h > 0 else -h for h in A[interval][0:width]] 
        lst2.append(method(absLst))        
        for i in range((len(A[interval])-3010)/10):
            lst3 = [h if h > 0 else -h for h in A[interval][width+(i*10):(i*10)+1010]]
            absLst = absLst[10:width]
            absLst.extend(lst3)
            lst2.append(method(absLst))
        lst.append(lst2)
        print "Searching first estimate in interval: ",interval+1,"/",len(A)
    return lst

def getMaxFrequency(frequencies, amplitudes):
    lst2 = []
    tempSum = np.sum(np.abs(amplitudes[0:width]))
    oldTenSum = np.sum(np.abs(amplitudes[0:10]))
    lst2.append(tempSum)
    for index in range(10, np.size(amplitudes)-width, 10):
        newTenSum = np.sum(np.abs(amplitudes[index+990:index+width]))
        oldTenSum = np.sum(np.abs(amplitudes[index-10:index]))
        tempSum += newTenSum - oldTenSum
        lst2.append(tempSum)

    maxIntervalIndex = np.argmax(lst2)
    maxfreqindex = amplitudes[((maxIntervalIndex*10)):(maxIntervalIndex*10)+width].argmax()
    maxfreqindex += (maxIntervalIndex*10)
    return frequencies[maxfreqindex]

def getMaxFrequenciesWithWindow(frequencies, A, times, intervalMethodString):
    if (intervalMethodString == "sum"):
        lst = getInitialGuess(A, frequencies)
    else:
        intervalMethod = {
                "median": getMedian,
            }.get(intervalMethodString, getSum)
        print(intervalMethod)
        lst = getInitialGuessByMethod(A, frequencies, intervalMethod)

    maxfreqlist = []
    print "Found first estimate intervals"
    print "Searching for max frequencies in intervals"
    for g in range(len(lst)):
        maxIntervalIndex = lst[g].index(max(lst[g]))
     
        maxfreqindex = A[g][((maxIntervalIndex*10)):(maxIntervalIndex*10)+width].argmax()
        maxfreqindex += (maxIntervalIndex*10)
        maxfreqlist.append(frequencies[maxfreqindex])
        print "Interval: ",g+1,"/",len(lst)," Found Max Freq: ",maxfreqindex
    return maxfreqlist

def getMaxFrequenciesWithDerivative(frequencies, A, times):
    getIndex = lambda lst, value: int((value-lst[0])/(lst[1]-lst[0]))

    maxfreqlist = [0]*(len(times))
    expectedmaxfreqlist = [0]*(len(times))

    initialIndex = getIndex(times, 770)
    for i in range(initialIndex, initialIndex+5):
        maxfreqlist[i] = getMaxFrequency(frequencies, A[i])


    # From initial time until the end
    for i in range(initialIndex+5, len(times)):
        print(times[i])
        expectedMaxFrequency = derivative(times[i-4:i], maxfreqlist[i-4:i], times[i], mode="backward")
        expectedMaxFrequencyIndex = getIndex(frequencies, expectedMaxFrequency)


        if expectedMaxFrequency > frequencies[-1] or expectedMaxFrequency < frequencies[0]:
            print("Differencing towards the end: Expected frequency was outside the spectrum")
            break
        expectedmaxfreqlist[i] = frequencies[expectedMaxFrequencyIndex]

        expectedMaxFrequency = frequencies[expectedMaxFrequencyIndex] #find the actual frequency
        difference = abs(expectedMaxFrequency - maxfreqlist[i-1])
        print("exp, cur, diff: ", expectedMaxFrequency, maxfreqlist[i-1], difference)
        minIntervalIndex = getIndex(frequencies, expectedMaxFrequency-0.5*difference)
        maxIntervalIndex = getIndex(frequencies, expectedMaxFrequency+0.5*difference)
        print("min, max: ", minIntervalIndex, maxIntervalIndex)
        print("______________")
        if minIntervalIndex < 0:
            minIntervalIndex = 0
        if maxIntervalIndex > len(frequencies):
            maxIntervalIndex = len(frequencies)
        maxfreqlist[i] = frequencies[minIntervalIndex+np.argmax(A[i][minIntervalIndex:maxIntervalIndex])]

    for i in range(initialIndex, 0, -1):
        print(times[i])
        expectedMaxFrequency = derivative(times[i+1:i+5], maxfreqlist[i+1:i+5], times[i], mode="forward")
        expectedMaxFrequencyIndex = getIndex(frequencies, expectedMaxFrequency)


        if expectedMaxFrequency > frequencies[-1] or expectedMaxFrequency < frequencies[0]:
            print("Differencing towards the beginning: Expected frequency was outside the spectrum")
            break
        expectedmaxfreqlist[i] = frequencies[expectedMaxFrequencyIndex]

        expectedMaxFrequency = frequencies[expectedMaxFrequencyIndex] #find the actual frequency
        difference = abs(expectedMaxFrequency - maxfreqlist[i-1])
        print("exp, cur, diff: ", expectedMaxFrequency, maxfreqlist[i-1], difference)
        minIntervalIndex = getIndex(frequencies, expectedMaxFrequency-0.5*difference)
        maxIntervalIndex = getIndex(frequencies, expectedMaxFrequency+0.5*difference)
        print("min, max: ", minIntervalIndex, maxIntervalIndex)
        print("______________")
        if minIntervalIndex < 0:
            minIntervalIndex = 0
        if maxIntervalIndex > len(frequencies):
            maxIntervalIndex = len(frequencies)
        maxfreqlist[i] = frequencies[minIntervalIndex+np.argmax(A[i][minIntervalIndex:maxIntervalIndex])]
    return maxfreqlist, expectedmaxfreqlist


def maxFrequencies(wavReader, carrierfrequency, intervalMethodString):
    #find/make matrix A
    print("Finding the signal")
    frequencies, A = wavReader.getFrequencyAmplitudes()
    times = wavReader.getTimes()
    A = np.array(A)


    # maxfreqlist = getMaxFrequenciesWithWindow(frequencies, A, times, intervalMethodString)
    maxfreqlist, expectedmaxfreqlist = getMaxFrequenciesWithDerivative(frequencies, A, times)
    print("Done finding the maximum frequencies")
    return map(lambda x: x+carrierfrequency, maxfreqlist), expectedmaxfreqlist
    

