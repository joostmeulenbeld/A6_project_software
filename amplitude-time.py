from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as p

numframes=100
left_channel=[]
right_channel=[]
t=[]
fs=250000

raw = Sndfile('Delfi-n3xt.wav', 'r')
data = np.array(raw.read_frames(numframes), dtype=np.float64)
raw.close()

for x in range(0,numframes):
    left_channel.append(data[x][0])
    right_channel.append(data[x][1])

t=np.linspace(0, len(left_channel)/fs, num=len(left_channel))
p.plot(left_channel)
p.show()

np.savetxt('output.txt',data)
