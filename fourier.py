from scipy import fftpack
from scipy import signal
import numpy as np

def getFFT(T, timeamplitude):
    N = len(timeamplitude[0])
    fourieramplitudes = fftpack.fft(timeamplitude[1])
    if N % 2 == 0:
    	positiveamplitude = 2.0/N * np.real(fourieramplitudes[0:N/2])
    	negativeamplitude = 2.0/N * np.imag(fourieramplitudes[N/2:N])
    else:
    	positiveamplitude = 2.0/N * np.real(fourieramplitudes[0:(N+1)/2])
    	negativeamplitude = 2.0/N * np.imag(fourieramplitudes[(N+1)/2:N])

    positiveamplitude = positiveamplitude[::-1] #The negative frequencies have to be reversed
    negativeamplitude = negativeamplitude[::-1]
    amplitudes = np.append(positiveamplitude, negativeamplitude)

    frequencies = fftpack.fftshift(np.fft.fftfreq(N, T))
    return frequencies, amplitudes

# def getFFTs(T, timeamplitudes):
#     frequencyamplitudes = []
#     outputmatrix = []
#     frequencies = []
#     for amplitude in timeamplitudes:
#         N = len(amplitude)
#         t = []
#         for i in range(0, N):
#             t.append(i*T)
#         print([t, amplitude])
#         # frequencies, power = fourier.getFFT(T, [t, amplitude])
#         # outputmatrix.append([sum(t)/float(len(t)), frequencies])

#     return frequencies, outputmatrix