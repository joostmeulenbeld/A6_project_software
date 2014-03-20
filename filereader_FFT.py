import scipy.io.wavfile as wav
import scipy, wave, struct
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
    p=nsample - 1
    ampleft=[]
    ampright=[]
    amptab=[]
    itab=[]
    for i in range(nsample,nsample+fourierwidth):
        amp=str(w.readframes(1))
        p=p+1
        w.setpos(p)
        ## Delimiting hexadecimal characters between bytes: \x
        amprep=amp.replace("\\","0")
        amptab.append(amp)
        for k in range(0,len(amprep)):
            amplitude=amprep[k]
            if k%2==0: ## Left channel
                ampleft.append(amplitude)
            if k%2!=0: ## Right channel
                ampright.append(amplitude)
        itab.append(i)
    print amptab
    print ampleft, " Left channel"
    print ampright, " Right channel"
    print itab

## Return the fast fourier transform of the given interval
def getFFT(timeamplitude):
    return fftpack.fft(timeamplitude)
