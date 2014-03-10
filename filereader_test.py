import scipy.io.wavfile as wav
import scipy
import wave

fourierwidth= 100 ## Fourier transform interval width
w=wave.open("Delfi-n3Xt.wav","r")
nsample=0
params=w.getparams()
nchannels=params[0]
sampwidth=params[1]
sampfreq=params[2]
totalsamp=params[3]

## Divide sample file into intervals, one for every Fast Fourier Transform
for i in range(nsample,nsample+fourierwidth):
    amp=w.readframes(i)
    print i
