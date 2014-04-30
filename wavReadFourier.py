import recursion3 as amplitude

from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
import fourier

class wavReaderFourierTransformer:

	def __init__(self, wavFileName, startSeconds, endSeconds, intervalWidthSeconds, intervalStartSeconds):
		self.wavFileName = wavFileName

		self.wavFile = Sndfile(self.wavFileName, 'r')
		self.fs=self.wavFile.samplerate
		self.nc=self.wavFile.channels
		self.enc=self.wavFile.encoding
		self.wavFile.close()
		del self.wavFile

		self.sampling_interval = 1.0/self.fs

		self.start = int(self.fs*startSeconds)
		self.end = int(self.fs*endSeconds)
		self.intervalWidth = int(self.fs*intervalWidthSeconds)
		self.intervalStartFrequency = int(self.fs*intervalStartSeconds)
		self.intervals = []
		self.frequencies = []

	def getFrequencyAmplitudes(self):
		self.wavFile = Sndfile(self.wavFileName, 'r')

		for intervalStartFrame in range(self.start, self.end, self.intervalStartFrequency):
			startTime = intervalStartFrame*self.sampling_interval
			endTime = (intervalStartFrame+self.intervalWidth)*self.sampling_interval
			meanTime = (startTime+endTime)/2.0

			output = amplitude.output_signal(self.intervalWidth, intervalStartFrame, self.wavFile)
			self.frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)

			self.intervals.append([meanTime, amplitudes])
			self.amplitudes = self.getAmplitudes()
			print(intervalStartFrame/self.fs)

		self.wavFile.close()
		del self.wavFile

		return self.frequencies, self.intervals

	def plotFourierTransforms(self):
		for i in range(len(self.intervals)):
			plt.plot(self.frequencies, self.intervals[i][1])

		plt.show()

	def getAmplitudes(self):
		amplitudes = []
		for data in self.intervals:
			amplitudes.append(data[1].tolist())
		return amplitudes

	def getAmplitudesRimsky(self):
		return np.array(self.getAmplitudes())

	def getFrequencies(self):
		return self.frequencies

	def getTimes(self):
		times = []
		for data in self.intervals:
			times.append(data[0])
		return times

	def getMaxFourierFrequency(self):
		return self.fs/2.0

	def getDeltaFourierFrequency(self):
		return self.fs/self.intervalWidth

	def plotAmplitudeHeatMap(self):
		self.plotHeatMap(self.amplitudes, self.frequencies)

	def plotCompressedHeatMap(self, intervalSize, compressionMethodString):
		amplitudes, frequencies = self.compressAll(intervalSize, compressionMethodString)
		self.plotHeatMap(amplitudes, frequencies)

	def plotNarrowHeatMap(self, spectrumWidth):
		amplitudes, frequencies = self.getNarrowSpectra(spectrumWidth)
		self.plotHeatMap(amplitudes, frequencies)

	def plotHeatMap(self, amplitudes, frequencies):
		data = np.array(amplitudes)
		fig, ax = plt.subplots()
		heatmap = ax.pcolor(data)

		column_labels = frequencies
		row_labels = self.getTimes()
		# put the major ticks at the middle of each cell, notice "reverse" use of dimension
		ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
		ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)


		ax.set_xticklabels(column_labels, minor=False)
		ax.set_yticklabels(row_labels, minor=False)
		plt.show()		

	def getNarrowSpectraFromAmplitudes(self, amplitudes, frequencies, spectrumWidth):
		amplitudes = []
		frequencies = []
		for amp in amplitudes:
			amplitude, frequency = self.getNarrowSpectrum(amp, frequencies, spectrumWidth)
			amplitudes.append(amplitude)
			frequencies.append(frequency)

		return amplitudes, frequencies

	def getNarrowSpectra(self, spectrumWidth):
		return getNarrowSpectraFromAmplitudes(self.amplitudes, self.frequencies, spectrumWidth)


	def getNarrowSpectrum(self, amplitudes, frequencies, spectrumWidth):
		cutOff = np.where(frequencies==-spectrumWidth)
		cutOff = cutOff[0][0]
		amplitudes = amplitudes[cutOff:-cutOff]
		frequencies = frequencies[cutOff:-cutOff]
		return amplitudes, frequencies


	def median(self, amplitudes):
		return np.median(amplitudes)

	def mean(self, amplitudes):
		return np.mean(amplitudes)

	def maxMeanDifference(self, amplitudes):
		return np.amax(amplitudes)-np.mean(amplitudes)

	def maxMedianDifference(self, amplitudes):
		return np.amax(amplitudes)-np.median(amplitudes)

	def compress(self, frequencies, amplitudes, intervalSize, compressionMethodString):
		resultFrequencies = []
		resultAmplitudes = []

		method = {
			"mean": self.mean,
			"median": self.median,
			"maxMeanDifference": self.maxMeanDifference,
			"maxMedianDifference": self.maxMedianDifference
		}.get(compressionMethodString, self.mean)

		for i in range(0, np.size(amplitudes), intervalSize):
			currentInterval = amplitudes[i:i+intervalSize]
			resultAmplitudes.append(method(currentInterval))
			resultFrequencies.append(np.mean(frequencies[i:i+intervalSize]))

		return resultAmplitudes, resultFrequencies

	def compressAll(self, intervalSize, compressionMethodString):
		compressedAmplitudes = []
		for amp in self.amplitudes:
			resultAmplitudes, resultFrequencies = self.compress(self.frequencies, amp, intervalSize, compressionMethodString)
			compressedAmplitudes.append(resultAmplitudes)
		return compressedAmplitudes, resultFrequencies


