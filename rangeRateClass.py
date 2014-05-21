from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer
from maxfrequencyclean import maxFrequencies
from rangerate import rangerateconvert
from tlerangerate import compare,groundmap

class rangeRate:


	def __init__(self, wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity):
		self.wavFileName = wavFileName
		self.start = start
		self.end = end
		self.intervalWidth = intervalWidth
		self.intervalStartFrequency = intervalStartFrequency
		self.carrierfrequency = carrierfrequency
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

	def plot2DWaterfallPlot(self):
		self.wavReader.plot2DWaterfallPlot()

	def plot3DWaterfallPlot(self):
		self.wavReader.plot3DWaterfallPlot()
		
	def plotGroundMap(self):
		groundmap()

	def plotComparison(self):
		compare(self.timedeltav)

	def wavReaderCalc(self):
		print("Start .wav reading and fourier transforming")
		self.wavReader.getFrequencyAmplitudes()

	def maxFrequencyCalc(self):
		print("Start noise reduction and maximum interval frequency detection")
		self.maxFrequencySum = maxFrequencies(self.wavReader, self.carrierfrequency, "sum")

	def dopplerTrackingCalc(self):
		print("Start Doppler tracking")
		self.dopplerTracking(self.maxFrequencySum, self.wavReader)


def init():
	wavFileName = "Delfi-n3xt.wav"	# The location of the wav file
	start = 60*4.0			# What time is the first interval in seconds
	end = 60*21.0+33		# What time is the last interval in seconds
	intervalWidth = 1.0		# How many seconds is one interval
	intervalStartFrequency = 60.0	# Every this many seconds a new interval starts
	carrierfrequency = 145870000	# Hz
	satelliteVelocity = 8000

	rr = rangeRate(wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity)
	return rr
	# rr.plotFrequencyHeatMap()


if __name__ == "__main__":
	rr = init()


