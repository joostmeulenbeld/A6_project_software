import numpy as np
import filereader_FFT as frfft
import math
import pylab

t = np.arange(0, 10*math.pi, 0.1)

x = np.sin(t) + np.sin(3*t)



print(frfft.getFFT(x))