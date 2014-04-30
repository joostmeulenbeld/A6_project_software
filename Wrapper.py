
from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
from wavReadFourier import wavReaderFourierTransformer
from maxfrequencyclean import maxFrequencies
from rangerate import rangerateconvert
from tlerangerate import compare

''' Input variables '''

wavFileName = "Delfi-n3xt.wav"	# the location of the wav file
start = 60*0.				# What time is the first interval in seconds
end = 60*20.001					# What time is the last interval in seconds
intervalWidth = 1.0				# How many seconds is one interval
intervalStartFrequency = 60.0	# Every this many seconds a new interval starts

carrierfrequency = 145870000 #Hz
lowfrequency = carrierfrequency-125000 #Hz
    
''' End of input variable

No code here
No code here

Wav reading and Fourier transforming'''
print "Wav reading and Fourier transforming"

wavReader = wavReaderFourierTransformer(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()


''' End of wav reading and fourier transforming

No code here
No code here

Maximum frequency and outlier detection '''
print "Maximum frequency and outlier detection"

maxFrequency = maxFrequencies(wavReader.getAmplitudesRimsky(),lowfrequency)




''' End of Maximum frequency and outlier detection

No code here
No code here

Doppler tracking '''
print "Doppler tracking"

freq = []
for i in range(len(maxFrequency)):
    freq.append(maxFrequency[i][1])    
time = wavReader.getTimes()
timefreq = [time,freq]

rangerate = rangerateconvert(timefreq,carrierfrequency)
timedeltav = [time,rangerate]
compare(timedeltav)


''' End of Doppler tracking 

No code here
No code here

Post-processing'''


print("Maximum Fourier frequency: " + str(wavReader.getMaxFourierFrequency()))
print("Delta Fourier frequency: " + str(wavReader.getDeltaFourierFrequency()))

print("narrowing")
amplitudes, frequencies = wavReader.getNarrowSpectra(10000)
print("compressing")
amplitudes, frequencies = wavReader.compressAmplitudes(amplitudes, frequencies, 10, "maxMedianDifference")
print("plotting")
wavReader.plotHeatMap(amplitudes, frequencies)




''' End of Post-processing

No code here
No code here

'''