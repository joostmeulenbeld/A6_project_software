from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer
from maxfrequencyclean import maxFrequencies
from rangerate import rangerateconvert
from tlerangerate import compare,tlerangerate,errorCount

class rangeRate:


    def __init__(self, wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency,listeningfrequency, satelliteVelocity):
		self.wavFileName = wavFileName
		self.start = start
		self.end = end
		self.intervalWidth = intervalWidth
		self.intervalStartFrequency = intervalStartFrequency
		self.carrierfrequency = carrierfrequency
                self.listeningfrequency = listeningfrequency
		self.cutOff = 3.0*satelliteVelocity/(3e8)*self.carrierfrequency

		self.wavReader = wavReaderFourierTransformer(self.wavFileName, self.start, self.end, self.intervalWidth, self.intervalStartFrequency, self.cutOff)
		self.lowfrequency = self.carrierfrequency - self.wavReader.getMaxFourierFrequency()

    def doCalculations(self):
		self.wavReaderCalc()
		self.maxFrequencyCalc()
		self.dopplerTrackingCalc()

    def dopplerTracking(self, maxFrequency, wavReader):
           freq = []
           for maxfreq in maxFrequency:
               freq.append(maxfreq)    
           time = wavReader.getTimes()
           print time
           timefreq = [time,freq]        
           rangerate = rangerateconvert(timefreq, self.carrierfrequency)
           self.timedeltav = [time,rangerate]	
           
           
           newcarrier = self.Differential(timefreq[0],timefreq[1])[2]
           newtime = self.Differential(timefreq[0],timefreq[1])[1]
           print "Old Carrier:",self.carrierfrequency
           print "TCA experiment: ",newtime+240.5
           print "New Carrier:",newcarrier
           
           newrangerate = rangerateconvert(timefreq, newcarrier)
           self.newtimedeltav = [time,newrangerate]
           
           self.trr=tlerangerate()
           self.tletime=range(len(self.trr[0][1]))
           index,mint,miny=self.Differential(self.tletime,self.trr[0][1])
           print "TCA TLE: ",mint
            
           newIndex=0
           i=0
           while time[i]>=mint:
               newIndex=i
               i=i+1
                   
           print 'Carrier frequency from the tle data :'
           print timefreq[0][newIndex]
           newValue = self.interpolation(timefreq[1][newIndex],timefreq[1][newIndex+1],mint,timefreq[0][newIndex],timefreq[0][newIndex+1])
           
           newrangerate = rangerateconvert(timefreq,newValue)
           self.newtimedeltav2 = [time,newrangerate]
           return timefreq
           

    def __init__(self, wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency,listeningfrequency, satelliteVelocity):
        self.wavFileName = wavFileName
        self.start = start
        self.end = end
        self.intervalWidth = intervalWidth
        self.intervalStartFrequency = intervalStartFrequency
        self.carrierfrequency = carrierfrequency
        self.listeningfrequency = listeningfrequency
        self.cutOff = 3.0*satelliteVelocity/(3e8)*self.carrierfrequency

        self.wavReader = wavReaderFourierTransformer(self.wavFileName, self.start, self.end, self.intervalWidth, self.intervalStartFrequency, self.cutOff)
        self.lowfrequency = self.carrierfrequency - self.wavReader.getMaxFourierFrequency()

    def doCalculations(self):
        self.wavReaderCalc()
        self.maxFrequencyCalc()
        self.dopplerTrackingCalc()


    def dopplerTracking(self, maxFrequency, wavReader):
        freq = []
        for maxfreq in maxFrequency:
            freq.append(maxfreq)    
        time = wavReader.getTimes()
        timefreq = [time,freq]        
        rangerate = rangerateconvert(timefreq, self.carrierfrequency)
        self.timedeltav = [time,rangerate]   


        newcarrier = self.Differential(timefreq[0],timefreq[1])[2]
        print "New Carrier:",newcarrier
        print "Old Carrier:",self.carrierfrequency
        newrangerate = rangerateconvert(timefreq, newcarrier)
        self.newtimedeltav = [time,newrangerate]

        self.trr=tlerangerate()
        self.tletime=range(len(self.trr[0][1]))
        index,mint,miny=self.Differential(self.tletime,self.trr[0][1])
        newIndex=0
        i=0
        while time[i]<=mint:
            newIndex=i
            i=i+1

        newValue = self.interpolation(timefreq[1][newIndex],timefreq[1][newIndex+1],mint,timefreq[0][newIndex],timefreq[0][newIndex+1])

        newrangerate = rangerateconvert(timefreq,newValue)
        self.newtimedeltav2 = [time,newrangerate]
        return timefreq
           
           
    def interpolation(self,y0,y1,x,x0,x1):
        newValue=y0+(y1-y0)*((x-x0)/(x1-x0))
        return newValue

    def plot2DWaterfallPlot(self):
        self.wavReader.plot2DWaterfallPlot()

    def plotComparison(self):
        compare(self.timedeltav,self.newtimedeltav,self.newtimedeltav2)
 

    def wavReaderCalc(self):
        print("Start .wav reading and fourier transforming")
        self.wavReader.getFrequencyAmplitudes()

    def maxFrequencyCalc(self):
        print("Start noise reduction and maximum interval frequency detection")
        self.maxFrequencySum = maxFrequencies(self.wavReader, self.listeningfrequency, "sum")

    def dopplerTrackingCalc(self):
        print("Start Doppler tracking")
        return self.dopplerTracking(self.maxFrequencySum, self.wavReader)
         
    def Differential(self,time,ylist): 
        dy = 0
        dx = time[1]-time[0]    
        slope = []            
        for i in range(1,len(ylist)):                      
            dy = (ylist[i]-ylist[i-1])
            slope.append(dy/dx) 
        lwall = int(divmod(600,dx)[0])
        rwall = int(divmod(1000,dx)[0])
        minslope = min(slope[lwall:rwall])
        minslopeindex = slope.index(minslope)
        minslopetime = (minslopeindex*dx)
        minslopey = ylist[minslopeindex]

        return minslopeindex,minslopetime,minslopey
    

def init():
    wavFileName = "Delfi-n3xt.wav"  # The location of the wav file
    start = 60*4.0          # What time is the first interval in seconds
    end = 60*21.0+33        # What time is the last interval in seconds
    intervalWidth = 1.0     # How many seconds is one interval
    intervalStartFrequency = 1.0   # Every this many seconds a new interval starts
    carrierfrequency = 145870000    # Hz
    listeningfrequency = 145870000
    satelliteVelocity = 8000

    rr = rangeRate(wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency,listeningfrequency, satelliteVelocity)
    return rr
    # rr.plotFrequencyHeatMap()


if __name__ == "__main__":
    rr = init()
    rr.doCalculations()
    rr.plotComparison()
