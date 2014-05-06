import wave

def enterValues():
    wavReader = raw_input('Enter file name [filename.wav]:')
    decision = raw_input('Should the program run through the entire file [Y/N]:')
    if decision == 'N':       
        start = float(raw_input('Enter start time [sec]:'))
        end = float(raw_input('Enter end time [sec]":'))
    else:
        start = 0.0
        end = 0.0
    carrierFrequency = float(raw_input('Enter the carrier frequency [Hz]:'))
    satelliteVelocity = float(raw_input('Enter the satellite speed [m/s]:'))
    return wavReader,decision,start,end,carrierFrequency,satelliteVelocity

wavReader,decision,start,end,carrierFrequency,satelliteVelocity = enterValues()
raw=wave.open(wavReader)    
values = raw.getparams()
if decision == 'Y':
    end = values[3]/float(values[2])