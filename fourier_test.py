import numpy as np
import fourier
from matplotlib import pyplot as plt

fs = 250e3
measurementTime = 5
N = fs*measurementTime
T = 1.0/fs
t = np.linspace(0.0, N*T, N)


print("max frequency (fs/2): " + str(fs/2))
print("delta frequency (fs/N): " + str(fs/N))
if N%2==0:
	print("N is even")
else:
	print("N is odd")

realFrequencies = np.arange(1, 1000, 87)
imagFrequencies = [1001]

y = np.zeros(len(t), 'complex')

for f in realFrequencies:
	y += 2*np.sin(f*2.0*np.pi*t)

for f in imagFrequencies:
	y += np.sin(f*2.0*np.pi*t)*1j


frequencies, power = fourier.getFFT(T, [t, y])

plt.plot(frequencies, power)
plt.show()