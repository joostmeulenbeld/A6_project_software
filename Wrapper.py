from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer

''' Input variables '''

wavFileName = "Delfi-n3xt.wav"	# the location of the wav file
start = 11.0					# What time is the first interval in seconds
end = 13.0						# What time is the last interval in seconds
intervalWidth = 1.0				# How many seconds is one interval
intervalStartFrequency = 1.0	# Every this many seconds a new interval starts

''' End of input variable

No code here
No code here

Wav reading and Fourier transforming'''

wavReader = wavReaderFourierTransformer(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()

print("Maximum Fourier frequency: " + str(wavReader.getMaxFourierFrequency()))
print("Delta Fourier frequency: " + str(wavReader.getDeltaFourierFrequency()))

for i in range(len(intervals)):
	plt.plot(frequencies, intervals[i][1])

plt.show()

''' End of wav reading and fourier transforming

No code here
No code here

Maximum frequency and outlier detection '''






''' End of Maximum frequency and outlier detection

No code here
No code here

Doppler tracking '''







''' End of Doppler tracking 

No code here
No code here

Post-processing'''




''' End of Post-processing

No code here
No code here

'''