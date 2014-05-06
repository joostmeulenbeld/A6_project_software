import wave
from rangeRateClass import rangeRate

def enterValues():
    wavReader = raw_input('Enter file name [filename.wav]:')
    raw=wave.open(wavReader)    
    values = raw.getparams()
    decision = raw_input('Should the program run through the entire file [Y/N]:')
    if decision == 'N':       
        start = float(raw_input('Enter start time [sec]:'))
        end = float(raw_input('Enter end time [sec]":'))
    else:
        start = 0.0
        end = values[3]/float(values[2])
    carrierFrequency = float(raw_input('Enter the carrier frequency [Hz]:'))
    satelliteVelocity = float(raw_input('Enter the satellite speed [m/s]:'))
    return wavReader,decision,start,end,carrierFrequency,satelliteVelocity

wavFileName,decision,start,end,carrierFrequency,satelliteVelocity = enterValues()
intervalWidth = 1.0
intervalStartFrequency = 20.0
rr = rangeRate(wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity)
rr.doCalculations()
rr.plotFrequencyHeatMap()