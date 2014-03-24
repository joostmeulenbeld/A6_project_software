from scipy import fftpack
import numpy as np

def getFFTs(T, timeamplitudes):
    frequencyamplitudes = []
    for ta in timeamplitudes:
        frequencyamplitudes.append(getFFT(T, ta))

def getFFT(T, timeamplitude):
    N = len(timeamplitude[0])
    fourieramplitudes = fftpack.fft(timeamplitude[1])
    realamplitude = 2.0/N * np.abs(fourieramplitudes[0:N])
    frequencies = np.fft.fftfreq(N)
    return [frequencies, realamplitude]