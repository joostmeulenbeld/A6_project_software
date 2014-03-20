import numpy as np
import filereader_FFT as frfft
import pylab
from matplotlib import pyplot as plt

# t = np.arange(0, 2*np.pi, 0.1)
# x = np.sin(t) + np.sin(3*t)
# timeamplitude = np.array([t, x])
# print(timeamplitude)


N = 600
T = 1.0/800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)

yf = frfft.getFFT(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

print(xf)
print(yf)

plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
plt.show()
