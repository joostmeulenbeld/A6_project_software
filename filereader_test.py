import scipy.io.wavfile as wav
import scipy, wave, struct
import matplotlib.pyplot as plt
import filereader_FFT as fft
    
a=fft.mainfft(wave.open('Delfi-n3Xt.wav','r'),5)
b=fft.readout(wave.open('Delfi-n3Xt.wav','r'),10,5)
