<<<<<<< HEAD
#import filereader_FFT
=======
import filereader_FFT as fft
>>>>>>> Fourier transform added, not working yet
# import maxfrequency
# import rangerate
import tlerangerate
# import filewriter

import wave

wav_filename = "Delfi-n3Xt.wav"
fourierwidth = 100


<<<<<<< HEAD
#w = wave.open(wav_filename,"r")
t = 20
print tlerangerate.gs_plot(t)
=======
w = wave.open(wav_filename,"r")
fouriermatrix = fft.mainfft(w, fourierwidth)
>>>>>>> Fourier transform added, not working yet
