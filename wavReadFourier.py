import recursion3 as amplitude

from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
import fourier

from matplotlib import cm  
from numpy import meshgrid  
from mpl_toolkits.mplot3d import Axes3D

class wavReaderFourierTransformer:

	def __init__(self, wavFileName, startSeconds, endSeconds, intervalWidthSeconds, intervalStartSeconds, spectrumWidth):
		self.wavFileName = wavFileName

		self.wavFile = Sndfile(self.wavFileName, 'r')
		self.fs=self.wavFile.samplerate
		self.nc=self.wavFile.channels
		self.enc=self.wavFile.encoding
		self.wavFile.close()
		del self.wavFile

		self.spectrumWidth = spectrumWidth

		self.sampling_interval = 1.0/self.fs

		self.start = int(self.fs*startSeconds)
		self.end = int(self.fs*endSeconds)
		self.intervalWidth = int(self.fs*intervalWidthSeconds)
		self.intervalStartFrequency = int(self.fs*intervalStartSeconds)
		self.amplitudes = []
		self.frequencies = []
		self.times = []
		self.narrowAmplitudes = []

	def getFrequencyAmplitudes(self):
		self.wavFile = Sndfile(self.wavFileName, 'r')

		for intervalStartFrame in range(self.start, self.end, self.intervalStartFrequency):
			startTime = intervalStartFrame*self.sampling_interval
			endTime = (intervalStartFrame+self.intervalWidth)*self.sampling_interval

			output = amplitude.output_signal(self.intervalWidth, intervalStartFrame, self.wavFile)
			self.frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)

			self.amplitudes.append(amplitudes)
			self.times.append(startTime)
			print (intervalStartFrame/self.fs),"/",self.end/self.fs

		self.wavFile.close()

		del self.wavFile

		self.narrowSpectra, self.narrowFrequencies = self.__getNarrowSpectra(self.spectrumWidth)

		return self.frequencies, self.amplitudes


	def plotHeatMapWithoutStoringData(self):
		self.wavFile = Sndfile(self.wavFileName, 'r')

		output = amplitude.output_signal(self.intervalWidth, 0, self.wavFile)
		self.frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)		

		spectrumWidth = -abs(self.spectrumWidth)
		cutOffIndex = -1

		for i in range(np.size(self.frequencies)-1):
			if ((self.frequencies[i]-spectrumWidth)*(self.frequencies[i+1]-spectrumWidth)<=0):
				cutOffIndex = i
				break

		if (cutOffIndex==-1):
			print("given frequency was not found")
			cutOffIndex = 0
				

		for intervalStartFrame in range(self.start, self.end, self.intervalStartFrequency):
			startTime = intervalStartFrame*self.sampling_interval
			endTime = (intervalStartFrame+self.intervalWidth)*self.sampling_interval

			output = amplitude.output_signal(self.intervalWidth, intervalStartFrame, self.wavFile)
			self.frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)
			amplitudes, self.frequencies = self.getNarrowSpectrum(amplitudes, self.frequencies, cutOffIndex)
			amplitudes, self.frequencies = self.compress(amplitudes, self.frequencies, 10, "maxMedianDifference")

			self.narrowAmplitudes.append(amplitudes)
			self.times.append(startTime)
			print (intervalStartFrame/self.fs),"/",self.end/self.fs

		self.wavFile.close()
		del self.wavFile
		self.plotHeatMap(self.narrowAmplitudes, self.frequencies)


	def plotFourierTransforms(self):
		for i in range(len(self.intervals)):
			plt.plot(self.frequencies, self.intervals[i][1])

		plt.show()

	def saveFourierTransformPlots(self):
		times = self.getTimes()
		for i in range(len(self.intervals)):
			plt.plot(self.frequencies, self.intervals[i][1])
			plt.savefig('img/fourier/fourier_' + str(times[i]) + '_seconds.png', bbox_inches='tight', dpi=400)
			plt.close()

	def saveNarrowFourierPlots(self):
		times = self.getTimes()
		for i in range(len(self.intervals)):
			plt.plot(self.narrowFrequencies, self.narrowSpectra[i])
			plt.savefig('img/narrowFourier/fourier_' + str(times[i]) + '_seconds.png', bbox_inches='tight', dpi=400)
			plt.close()

	def saveFourierTransformPlotsWithoutStoringData(self):
		self.wavFile = Sndfile(self.wavFileName, 'r')

		for intervalStartFrame in range(self.start, self.end, self.intervalStartFrequency):
			startTime = intervalStartFrame*self.sampling_interval
			endTime = (intervalStartFrame+self.intervalWidth)*self.sampling_interval
			meanTime = (startTime+endTime)/2.0

			output = amplitude.output_signal(self.intervalWidth, intervalStartFrame, self.wavFile)
			self.frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)

			plt.plot(self.frequencies, amplitudes)
			plt.savefig('img/fourier/fourier_' + str(startTime) + '_seconds.png', bbox_inches='tight', dpi=400)
			plt.close()

			print(intervalStartFrame/self.fs)

		self.wavFile.close()
		del self.wavFile			

	def getFrequencies(self):
		return self.frequencies

	def getTimes(self):
		return self.times

	def getMaxFourierFrequency(self):
		return self.fs/2.0

	def getDeltaFourierFrequency(self):
		return self.fs/self.intervalWidth

	def plotAmplitudeHeatMap(self):
		self.plotHeatMap(self.amplitudes, self.frequencies)

	def plotNarrowCompressedHeatMap(self, intervalSize, compressionMethodString, spectrumWidth):
		print("narrowing")
		amplitudes, frequencies = self.__getNarrowSpectra(spectrumWidth)
		print("compressing")
		amplitudes, frequencies = self.compressAmplitudes(amplitudes, frequencies, intervalSize, compressionMethodString)
		print("plotting")
		self.plotHeatMap(amplitudes, frequencies)

	def plotHeatMapNew(self, amplitudes, frequencies):
		times = self.getTimes()
		amplitudes = np.array(amplitudes)
		freqGrid, timesGrid = np.meshgrid(frequencies, times, sparse=False)

		fig, ax = plt.subplots()
		heatmap = plt.pcolor(freqGrid, timesGrid, amplitudes, cmap='RdBu',
			vmin=np.min(amplitudes), vmax=np.max(amplitudes))
		# heatmap = ax.pcolor(data)


		times = np.floor(np.array(self.getTimes())/60.0)
		# put the major ticks at the middle of each cell, notice "reverse" use of dimension
		# ax.set_yticks(times, minor=False)
		# ax.set_xticks(smallFrequencies, minor=False)

		ax.axis([np.min(frequencies), np.max(frequencies), np.min(times), np.max(times)])
		# ax.set_xticklabels(frequencies, minor=False)
		# ax.set_yticklabels(times, minor=False)
		plt.show()		

	def plotHeatMap(self, amplitudes, frequencies):
		data = np.array(amplitudes)
		fig, ax = plt.subplots()
		heatmap = ax.pcolor(data, cmap='spectral')

		column_labels = frequencies
		row_labels = np.floor(np.array(self.getTimes())/60.0)
		# put the major ticks at the middle of each cell, notice "reverse" use of dimension
		ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
		ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)


		ax.set_xticklabels(column_labels, minor=False)
		ax.set_yticklabels(row_labels, minor=False)
		plt.show()	

	def getNarrowSpectraFromAmplitudes(self, inputamplitudes, inputfrequencies, spectrumWidth):
		amplitudes = []
		frequencies = []
		spectrumWidth = -abs(spectrumWidth)
		cutOffIndex = -1
		for i in range(np.size(inputfrequencies)-1):
			if ((inputfrequencies[i]-spectrumWidth)*(inputfrequencies[i+1]-spectrumWidth)<=0):
				cutOffIndex = i
				break

		if (cutOffIndex==-1):
			print("given frequency was not found")
			cutOffIndex = 0

		for amp in inputamplitudes:
			amplitude, frequencies = self.getNarrowSpectrum(amp, inputfrequencies, cutOffIndex)
			amplitudes.append(amplitude)
		return amplitudes, frequencies

	def __getNarrowSpectra(self, spectrumWidth):
		return self.getNarrowSpectraFromAmplitudes(self.amplitudes, self.frequencies, spectrumWidth)


	def getNarrowSpectra(self):
		return self.narrowSpectra, self.narrowFrequencies

	def getNarrowSpectrum(self, amplitudes, frequencies, cutOffIndex):
		amplitudes = amplitudes[cutOffIndex:-cutOffIndex]
		frequencies = frequencies[cutOffIndex:-cutOffIndex]
		return amplitudes, frequencies

	def median(self, amplitudes):
		return np.median(amplitudes)

	def mean(self, amplitudes):
		return np.mean(amplitudes)

	def maxMeanDifference(self, amplitudes):
		return np.amax(amplitudes)-np.mean(amplitudes)

	def maxMedianDifference(self, amplitudes):
		return np.amax(amplitudes)-np.median(amplitudes)

	def compressAmplitudes(self, amplitudes, frequencies, intervalSize, compressionMethodString):
		compressedAmplitudes = []
		for amp in amplitudes:
			resultAmplitudes, resultFrequencies = self.compress(amp, frequencies, intervalSize, compressionMethodString)
			compressedAmplitudes.append(resultAmplitudes)
		return compressedAmplitudes, resultFrequencies

	def compress(self, amplitudes, frequencies, intervalSize, compressionMethodString):
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
		return self.compressAmplitudes(self.amplitudes, self.frequencies, intervalSize, compressionMethodString)
	
	def waterFallPlot(self, compressionIntervalWidth, compressionMethodString, spectrumWidth):

		tt=self.getTimes()
		aa,ff=self.__getNarrowSpectra(spectrumWidth)
		aa,ff=self.compressAmplitudes(aa,ff,compressionIntervalWidth,compressionMethodString)
		fig=plt.figure(1)
		ax=fig.add_subplot(1,1,1,projection='3d')

		X,Y=meshgrid(ff,tt)
		p = ax.plot_surface(X, Y, aa, rstride=4, cstride=4, cmap=cm.coolwarm, linewidth=0, antialiased=False)



		ax.view_init(elev=45, azim=-100)

		ax.set_xlabel('Frequency (Hz)')
		ax.set_ylabel('Time (sec)')
		ax.set_zlabel('Magnitude')
	    
		plt.show() 
	    
