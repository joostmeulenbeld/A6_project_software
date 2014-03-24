import scipy.io.wavfile as wav
import scipy, wave, struct
import matplotlib.pyplot as plt
import filereader_FFT_temp as fft

a=fft.mainfft(wave.open('Delfi-n3Xt.wav','r'),10)
b=fft.readout(wave.open('Delfi-n3Xt.wav','r'),10,10)


## all = [interval1, interval2, ...]
##
## interval1 = [ [sample1, amp1], [sampl2, amp2], ...]
