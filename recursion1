from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as p
import wave

fft_frame=12
left_channel=[0 for i in range(fft_frame)]
right_channel=[0 for i in range(fft_frame)]
t=[]
start=10
end=60

raw = Sndfile('Delfi-n3xt.wav', 'r')

fs=raw.samplerate
nc=raw.channels
enc=raw.encoding


x=start
raw.seek(start)
while x<=end:
    data = np.array(raw.read_frames(fft_frame), dtype=np.float64)
    for y in range(0,fft_frame):
        left_channel[y]=data[y][0]
        right_channel[y]=data[y][1]
    p.plot(left_channel)
    p.show()
    x=x+start
    raw.seek(x)


raw.close()
    






