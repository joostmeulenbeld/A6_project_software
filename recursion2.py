from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as p

fft_frame=12
left_channel=np.zeros(fft_frame)
right_channel=np.zeros(fft_frame)

t=[0 for i in range(fft_frame)]
start=10
end=60

output=np.zeros((end/start,fft_frame,2))

raw = Sndfile('Delfi-n3xt.wav', 'r')

fs=raw.samplerate
nc=raw.channels
enc=raw.encoding


x=start
raw.seek(start)
c=0
while x<=end:
    data = np.array(raw.read_frames(fft_frame), dtype=np.float64)
    for y in range(0,fft_frame):
        left_channel[y]=data[y][0]
        right_channel[y]=data[y][1]
        t[y]=(x+y)/float(fs)
    signal = left_channel + right_channel*1j
    for y in range(0,fft_frame):
        output[c][y][0]=t[y]
        output[c][y][1]=signal[y]
    x=x+start
    raw.seek(x)
    c+=1


raw.close()








