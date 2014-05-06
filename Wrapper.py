from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer
from maxfrequencyclean import maxFrequencies
from rangerate import rangerateconvert
from tlerangerate import compare

''' Input variables '''
print "Starting Program"

wavFileName = "Delfi-n3xt.wav"			# The location of the wav file
start = 60*0.0							# What time is the first interval in seconds
end = 60*21.0+33						# What time is the last interval in seconds
intervalWidth = 1.0						# How many seconds is one interval
intervalStartFrequency = 60.0			# Every this many seconds a new interval starts
carrierfrequency = 145870000			# Hz
lowfrequency = carrierfrequency-125000	# Hz
    
''' End of input variable

No code here
No code here

Wav reading and Fourier transforming'''
print "Start .wav reading and Fourier transforming"

wavReader = wavReaderFourierTransformer(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()

print "Completed .wav reading and Fourier transforming"
''' End of wav reading and fourier transforming

No code here
No code here

Maximum frequency and outlier detection '''
print "Start noise reduction and maximum interval frequency detection"

maxFrequency = maxFrequencies(wavReader.getAmplitudesRimsky(),lowfrequency)

print "Completed noise reduction and maximum interval frequency detection"
''' End of noise reduction and maximum interval frequency detection

No code here
No code here

Doppler tracking '''
print "Start Doppler tracking"

freq = []
for i in range(len(maxFrequency)):
    freq.append(maxFrequency[i])    
time = wavReader.getTimes()
timefreq = [time,freq]

rangerate = rangerateconvert(timefreq,carrierfrequency)
timedeltav = [time,rangerate]
compare(timedeltav)

print "Start Doppler tracking"
''' End of Doppler tracking 

No code here
No code here

Post-processing'''
print "Start Post-processing"

print("Maximum Fourier frequency: " + str(wavReader.getMaxFourierFrequency()))
print("Delta Fourier frequency: " + str(wavReader.getDeltaFourierFrequency()))

wavReader.plotNarrowCompressedHeatMap(10, "maxMedianDifference", 10000)
# amplitudes, frequencies = wavReader.compressAll(100, "maxMedianDifference")
# for amp in amplitudes:
# 	plt.plot(frequencies, amp)
# plt.show()

# wavReader.plotFourierTransforms()

# wavReader.waterFallPlot(10, "maxMedianDifference", 10000)

print "Completed Post-processing"
print "End of program"
''' End of Post-processing

No code here
No code here

'''