import scipy.io.wavfile as wav
import scipy, wave, binascii
import matplotlib.pyplot as plt
import scipy.io as sio

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
    matfile=scipy.io.loadmat('Matlabfile.mat')
    
