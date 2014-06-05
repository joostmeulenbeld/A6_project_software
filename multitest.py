__author__ = 'Joost'
import numpy as np

def maxMeanDifference(amplitudes):
    return np.amax(amplitudes)-np.mean(amplitudes)

def maxMedianDifference(amplitudes):
    return np.amax(amplitudes)-np.median(amplitudes)


def compressSpectrum(frequencies, amplitudes, intervalSize, compressionMethodString):
    resultFrequencies = []
    resultAmplitudes = []

    method = {
        "mean": np.mean,
        "median": np.median,
        "maxMeanDifference": maxMeanDifference,
        "maxMedianDifference":maxMedianDifference
    }.get(compressionMethodString, np.mean)

    for i in range(0, np.size(amplitudes), intervalSize):
        currentInterval = amplitudes[i:i+intervalSize]
        resultAmplitudes.append(method(currentInterval))
        resultFrequencies.append(np.mean(frequencies[i:i+intervalSize]))

    return resultFrequencies, resultAmplitudes
