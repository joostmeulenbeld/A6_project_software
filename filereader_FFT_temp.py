import scipy.io.wavfile as wav
import scipy, wave, binascii
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
    flag=1
    bytenum=0
    p=nsample - 1
    numbappend=[]
    ampleft=[]
    ampright=[]
    l=''
    r=''
    amptab=[]
    itab=[]
    for i in range(nsample,nsample+fourierwidth):
        amp=str(w.readframes(1))
        p+1
        w.setpos(p)
        ## Delimiting hexadecimal characters between bytes: \x
        ## This presents us with the problem that '\x' is a command in Python syntax...
        c=len(w.readframes(1))
        
        
    print amptab
    print ampleft, " Left channel"
    print ampright, " Right channel"
    print itab, "Sample number"
