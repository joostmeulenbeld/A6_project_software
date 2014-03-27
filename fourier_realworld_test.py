import numpy as np
import fourier
from matplotlib import pyplot as plt
import csv


def readoutputfile():
	with open('output.txt', 'r') as f:
		left_channel = []
		right_channel = []
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			left_channel.append(float(row[0]))
			right_channel.append(float(row[1]))
		left_channel = np.array(left_channel)
		right_channel = np.array(right_channel)
		return left_channel+right_channel*1.0j

signal = readoutputfile()

fs = 250e3
N = len(signal)
T = 1.0/fs

print("max frequency (fs/2): " + str(fs/2))
print("delta frequency (fs/N): " + str(fs/N))

if N%2==0:
	print("N is even")
else:
	print("N is odd")

t = []
for i in range(0, N):
    t.append(i*T)

frequencies, amplitudes = fourier.getFFT(T, [t, signal])

plt.plot(frequencies, amplitudes)
plt.show()