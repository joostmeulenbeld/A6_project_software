import scipy.io.wavfile as wav
import scipy
import wave
import matplotlib.pyplot as plt

fourierwidth= 100 ## Fourier transform interval width
w=wave.open("Delfi-n3Xt.wav","r")
nsample=0
amptab=[]
itab=[]
ttab=scipy.linspace(0,fourierwidth)
params=w.getparams()
nchannels=params[0]
sampwidth=params[1]
sampfreq=params[2]
totalsamp=params[3]
print params

## Divide sample file into intervals, one for every Fast Fourier Transform
for i in range(nsample,nsample+fourierwidth):
    amp=w.readframes(i)
    amptab.append(amp)
    itab.append(i)

print amptab
print itab
