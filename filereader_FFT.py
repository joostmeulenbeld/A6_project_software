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
    bytenum=0
    p=nsample - 1
    numbappend=[]
    ampleft=[]
    ampright=[]
    ampleftfull=[0] * fourierwidth
    amprightfull=[0] * fourierwidth
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
            if k%2!=0: ## Right channel
                r=amplitude.encode("hex")
                ampright.append(str(r))
        itab.append(i)
    for j in range(0,3*fourierwidth):
        numbappend.append(ampleft[j])
        bytenum+1
        if bytenum==2:
            bytenum=0
    print amptab
    print ampleft, " Left channel"
    print ampright, " Right channel"
    print itab, "Sample number"
