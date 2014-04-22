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

	def getMaxFourierFrequency(self):
		return self.fs/2.0

	def getDeltaFourierFrequency(self):
		return self.fs/self.intervalWidth
