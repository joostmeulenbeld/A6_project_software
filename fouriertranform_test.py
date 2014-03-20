import numpy as np
import filereader_FFT as frfft
from matplotlib import pyplot as plt

# t = np.arange(0, 2*np.pi, 0.1)
# x = np.sin(t) + np.sin(3*t)
# timeamplitude = np.array([t, x])
# print(timeamplitude)

fs = 1000
N = 1000
T = 1.0/fs
x = np.linspace(0.0, N*T, N)
y = 1.0+np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x) + np.sin(40.0* 2.0*np.pi*x)*1j

yf = frfft.getFFT(T, [x, y])

plt.plot(yf[0], yf[1])
plt.show()