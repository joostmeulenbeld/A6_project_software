import scipy.io.wavfile as wav
import scipy
import wave

w=wave.open("Delfi-n3Xt.wav","r")

params=w.getparams()
nchannels=params[0]
sampfreq=params[2]
totalsamp=params[3]
print params
amp=w.readframes(1)
print amp
