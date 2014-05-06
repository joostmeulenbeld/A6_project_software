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
		self.carrierfrequency = self.carrierfrequency
		self.wavReader = wavReaderFourierTransformer(self.wavFileName, self.start, self.end, self.intervalWidth, self.intervalStartFrequency)
		self.lowfrequency = self.carrierfrequency - self.wavReader.getMaxFourierFrequency()
		self.cutOff = satelliteVelocity/(3e8)*self.carrierfrequency


	def doCalculations():
		print("start .wav reading and fourier transforming")
		self.wavReader.getFrequencyAmplitudes()

		print("start noise reduction and maximum interval frequency detection")
		self.maxFrequency = maxFrequencies(wavReader.getAmplitudesRimsky(), carrierfrequency)

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
		wavReader.plotNarrowCompressedHeatMap(10, "maxMedianDifference", self.cutOff)

	def plotWaterfallPlot(self):
		wavReader.waterFallPlot(10, "maxMedianDifference", self.cutOff)

	def plotComparison(self):
		compare(self.timedeltav)
