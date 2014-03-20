import scipy.io.wavfile as wav
from scipy import fftpack
import scipy
import wave
import matplotlib.pyplot as plt

def mainfft(w,fourierwidth):
    ttab=scipy.linspace(0,fourierwidth)
    params=w.getparams()
    nchannels=params[0]
    sampwidth=params[1]
    sampfreq=params[2]
    totalsamp=params[3]
    print params ## Channels, sample width [bytes], sample frequency

## Divide sample file into intervals, one for every Fast Fourier Transform
def readout(w,nsample,fourierwidth):
    amptab=[]
    itab=[]
    for i in range(nsample,nsample+fourierwidth):
        amp=w.readframes(i)
        amptab.append(amp)
        itab.append(i)
    print amptab
    print itab

## Return the fast fourier transform of the given interval
def getFFT(timeamplitude):
    return fftpack.fft(timeamplitude)
