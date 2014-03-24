

def getFFTs(T, timeamplitudes):
    frequencyamplitudes = []
    for ta in timeamplitudes:
        frequencyamplitudes.append(getFFT(T, ta))

def getFFT(T, timeamplitude):
    N = len(timeamplitudes[0])
    fourieramplitudes = fftpack.fft(timeamplitudes[1])
    realamplitudes = 2.0/N * np.abs(fourieramplitudes[0:N/2])
    frequencies = np.linspace(0.0, 1.0/(2.0*T), N/2)
    return [frequencies, realamplitudes]