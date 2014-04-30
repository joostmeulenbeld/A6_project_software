import filereader_FFT
# import maxfrequency
# import rangerate
import tlerangerate
# import filewriter

import wave

wav_filename = "Delfi-n3Xt.wav"
fourierwidth = 100


t = 20
w = wave.open(wav_filename,"r")
fouriermatrix = fft.mainfft(w, fourierwidth)
