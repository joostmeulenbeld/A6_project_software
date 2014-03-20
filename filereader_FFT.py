import scipy.io.wavfile as wav
import scipy, wave, struct
import matplotlib.pyplot as plt
<<<<<<< HEAD
=======
from scipy import fftpack
import numpy as np
>>>>>>> 48eb21684ac627a058666f67c69ebfd1c45285b1

def mainfft(w,fourierwidth):
    ttab=scipy.linspace(0,fourierwidth)
    params=w.getparams()
    nchannels=params[0]
    sampwidth=params[1]
    sampfreq=params[2]
    totalsamp=params[3]
    print params ## Channels, sample width [bytes], sample frequency

<<<<<<< HEAD
=======
def getFFT(T, timeamplitude):
    N = len(timeamplitudes[0])
    fourieramplitudes = fftpack.fft(timeamplitudes[1])
    realamplitudes = 2.0/N * np.abs(fourieramplitudes[0:N/2])
    frequencies = np.linspace(0.0, 1.0/(2.0*T), N/2)
    return [frequencies, realamplitudes]

def getFFTs(T, timeamplitudes):
    frequencyamplitudes = []
    for ta in timeamplitudes:
        frequencyamplitudes.append(getFFT(T, ta))


>>>>>>> 48eb21684ac627a058666f67c69ebfd1c45285b1
## Divide sample file into intervals, one for every Fast Fourier Transform
def readout(w,nsample,fourierwidth):
    bytenum=0
    p=nsample - 1
    numbappend=[]
    ampleft=[]
    ampleftcurframe=[]
    ampright=[]
    ampleftfull=[]
    amptab=[]
    itab=[]
    for i in range(nsample,nsample+fourierwidth):
        amp=str(w.readframes(1))
        p+1
        w.setpos(p)
        ## Delimiting hexadecimal characters between bytes: \x
        ## This presents us with the problem that '\x' is a command in Python syntax...
        amprep=amp.replace("\\","0")
        amptab.append(amp)
        for k in range(0,len(amprep)):
            amplitude=amprep[k]
            if k%2==0: ## Left channel
                l=amplitude.encode("hex")
                ampleft.append(str(l))
                ampleftcurframe.append(str(l))
            if k%2!=0: ## Right channel
                r=amplitude.encode("hex")
                ampright.append(str(r))
            ampleftfull= ampleftcurframe.join()
            print ampleftfull
        itab.append(i)
        
        
    print amptab
    print ampleft, " Left channel"
    print ampright, " Right channel"
    print itab, "Sample number"
