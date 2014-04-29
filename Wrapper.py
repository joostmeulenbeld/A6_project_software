
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

carrierfrequency=145870000 #Hz
lowfrequency=carrierfrequency-125000 #Hz
factorrange=0.25  #factor of how much of the columns of A range will be used for r n plus and minus
factorr=0.1       #q=r-round(factorr*r) how much smaller q should be if its bigger than r
factorq=0.2       #q=q+round(factorq*columnsA) how much smaller the interval gets
iterationsZ=3     #number of iterations done 


    
''' End of input variable

No code here
No code here

Wav reading and Fourier transforming'''

wavReader = wavReaderFourierTransformer(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()


''' End of wav reading and fourier transforming

No code here
No code here

Maximum frequency and outlier detection '''


maxFrequency = maxFrequencies(wavReader.getAmplitudesRimsky(), factorrange, factorr, factorq, iterationsZ,lowfrequency)




''' End of Maximum frequency and outlier detection

No code here
No code here

Doppler tracking '''

freq = []
lst = []
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

# wavReader.plotWaterfallPlot()
# wavReader.plotFourierTransforms()
# amplitudes, frequencies = wavReader.compressAll(1000, "maxMedianDifference")
# print(np.size(amplitudes))
# plt.plot(wavReader.getFrequencies(), wavReader.getAmplitudes()[0])
# plt.plot(frequencies, amplitudes[0])
# plt.show()


''' End of Post-processing

No code here
No code here

'''