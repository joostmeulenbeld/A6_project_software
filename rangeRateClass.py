from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer
from maxfrequencyclean import maxFrequencies
from rangerate import rangerateconvert
from tlerangerate import compare

class rangeRate:


	def __init__(self, wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity):
		self.wavFileName = wavFileName
		self.start = start
		self.end = end
		self.intervalWidth = intervalWidth
		self.intervalStartFrequency = intervalStartFrequency
		self.carrierfrequency = carrierfrequency
		self.wavReader = wavReaderFourierTransformer(self.wavFileName, self.start, self.end, self.intervalWidth, self.intervalStartFrequency)
		self.lowfrequency = self.carrierfrequency - self.wavReader.getMaxFourierFrequency()
		self.cutOff = 1.5*satelliteVelocity/(3e8)*self.carrierfrequency
		print(self.cutOff)


	def doCalculations(self):
		print("start .wav reading and fourier transforming")
		self.wavReader.getFrequencyAmplitudes()

		print("start noise reduction and maximum interval frequency detection")
		self.maxFrequency = maxFrequencies(self.wavReader, self.carrierfrequency)

		print("Start Doppler tracking")
		self.dopplerTracking(self.maxFrequency, self.wavReader)

	def dopplerTracking(self, maxFrequency, wavReader):
		freq = []
		for maxfreq in maxFrequency:
		    freq.append(maxfreq)    
		time = wavReader.getTimes()
		timefreq = [time,freq]

		rangerate = rangerateconvert(timefreq, carrierfrequency)
		self.timedeltav = [time,rangerate]	

	def plotFrequencyHeatMap(self):
		self.wavReader.plotNarrowCompressedHeatMap(10, "maxMedianDifference", self.cutOff)

	def plotWaterfallPlot(self):
		self.wavReader.waterFallPlot(10, "maxMedianDifference", self.cutOff)

	def plotComparison(self):
		compare(self.timedeltav)


if __name__ == "__main__":
	wavFileName = "Delfi-n3xt.wav"			# The location of the wav file
	start = 60*12.0							# What time is the first interval in seconds
	end = 60*13.0+33						# What time is the last interval in seconds
	intervalWidth = 1.0						# How many seconds is one interval
	intervalStartFrequency = 20.0			# Every this many seconds a new interval starts
	carrierfrequency = 145870000			# Hz
	satelliteVelocity = 7000

	rr = rangeRate(wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity)
	rr.doCalculations()
	rr.plotWaterfallPlot()
	rr.plotComparison()