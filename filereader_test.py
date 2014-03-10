import scipy.io.wavfile as wav
import scipy
import wave

w=wave.open("Delfi-n3Xt.wav","r")

params=w.getparams()
nchannels=params[0]
sampfreq=params[2]
sampwidth=params[1]
totalsamp=params[3]
print params

for i in range(0,1000):
    amp=w.readframes(i)
    print amp
