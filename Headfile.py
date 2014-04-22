import recursion3 as amplitude

from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as p

fft_frame=12
start=10
end=60
output=np.zeros(fft_frame)

raw = Sndfile('Delfi-n3xt.wav', 'r')

fs=raw.samplerate
nc=raw.channels
enc=raw.encoding


x=start
while x<=end:    
    output=amplitude.output_signal(fft_frame,x,raw)
    x=x+start


raw.close()
