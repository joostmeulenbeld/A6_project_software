from scipy import fftpack
import numpy as np

# Input: 
#       T           = Time between two samples (1/fs)
#       amplitudes  = Amplitudes of the signal
# Output:
#       frequencies = frequencies in the input signal
#       amplitudes  = amplitudes for the frequencies 
def getFFT(T, amplitudes):
    N = len(amplitudes[0])
    fourieramplitudes = fftpack.fft(amplitudes[1])
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

# def getFFTs(T, amplitudess):
#     frequencyamplitudes = []
#     outputmatrix = []
#     frequencies = []
#     for amplitude in amplitudess:
#         N = len(amplitude)
#         t = []
#         for i in range(0, N):
#             t.append(i*T)
#         print([t, amplitude])
#         # frequencies, power = fourier.getFFT(T, [t, amplitude])
#         # outputmatrix.append([sum(t)/float(len(t)), frequencies])

#     return frequencies, outputmatrix