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

		self.wavFile.close()
		del self.wavFile

		return self.frequencies, self.intervals

	def plotFourierTransforms(self):
		for i in range(len(self.intervals)):
			plt.plot(self.frequencies, self.intervals[i][1])

		plt.show()

	def plotWaterfallPlot(self):
		column_labels = list('Frequencies')
		row_labels = list('Time')
		amplitudes = np.ndarray(shape=(np.size(self.intervals[0]), np.size(self.frequencies)))
		for data in self.intervals:
			amplitudes.append(data[1])
		print(data)
		data = amplitudes
		fig, ax = plt.subplots()
		heatmap = ax.pcolor(data, cmap=plt.cm.Blues)

		# put the major ticks at the middle of each cell
		ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
		ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

		# want a more natural, table-like display
		ax.invert_yaxis()
		ax.xaxis.tick_top()

		ax.set_xticklabels(row_labels, minor=False)
		ax.set_yticklabels(column_labels, minor=False)
		plt.show()

	def getAmplitudes(self):
		amplitudes = []
		for data in self.intervals:
			amplitudes.append(data[1])
		return amplitudes

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
