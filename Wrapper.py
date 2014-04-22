from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer

wavFileName = "Delfi-n3xt.wav"
start = 11.0
end = 13.0
intervalWidth = 1.0
intervalStartFrequency = 1.0

wavReader = wavReaderFourierTransformer(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()

print("Maximum Fourier frequency: " + str(wavReader.getMaxFourierFrequency()))
print("Delta Fourier frequency: " + str(wavReader.getDeltaFourierFrequency()))



for i in range(len(intervals)):
	plt.plot(frequencies, intervals[i][1])

plt.show()