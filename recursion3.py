from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as p

def output_signal(no_of_frames,start,raw):
    left_channel=np.zeros(no_of_frames)
    right_channel=np.zeros(no_of_frames)
    signal=[0 for i in range(no_of_frames)]
    raw.seek(start)
    data = np.array(raw.read_frames(no_of_frames), dtype=np.float64)
    for y in range(0,no_of_frames):
        left_channel[y]=data[y][0]
        right_channel[y]=data[y][1]
        #t[y]=(x+y)/float(fs)
        signal[y]=complex(left_channel[y],right_channel[y])
    return signal

