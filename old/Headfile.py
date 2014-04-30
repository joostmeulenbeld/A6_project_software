import recursion3 as amplitude

from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
import fourier

fft_frame=250000
start=25000000
end=100000000+5*start
output=np.zeros(fft_frame)

raw = Sndfile('Delfi-n3xt.wav', 'r')

fs=raw.samplerate
nc=raw.channels
enc=raw.encoding
sampling_interval = 1.0/fs


x=100000000

intervals = []
frequencies = []

while x<=end:
	startTime = x*sampling_interval
	endTime = (x+fft_frame)*sampling_interval
	meanTime = (startTime+endTime)/2.0

	output = amplitude.output_signal(fft_frame,x,raw)
	frequencies, amplitudes = fourier.getFFT(sampling_interval, output)

	intervals.append([meanTime, amplitudes])

	print(intervals[-1])
	plt.plot(frequencies, amplitudes)
	x=x+start

plt.show()

raw.close()
