#import filereader_FFT
import filereader_FFT as fft
# import maxfrequency
# import rangerate
import tlerangerate
# import filewriter

import wave

wav_filename = "Delfi-n3Xt.wav"
fourierwidth = 100


#w = wave.open(wav_filename,"r")
t = 20
print tlerangerate.gs_plot(t)
w = wave.open(wav_filename,"r")
fouriermatrix = fft.mainfft(w, fourierwidth)
