import scipy.io.wavfile as wav
import scipy
import wave

w=wave.open("Delfi-n3Xt.wav","r")
params=w.getparams()
print params
