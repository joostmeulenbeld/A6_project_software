import wave
from rangeRateClass import rangeRate

def enterValues():
    wavReader = None
    decision = None
    start = -1.0
    end = -1.0
    carrierFrequency = None
    satelliteVelocity = None
    Flag=0
    while Flag==0:
        try:
            Flag=1
            wavReader = raw_input('Enter file name [filename.wav]:')
            raw=wave.open(wavReader) 
           
        except IOError:
            Flag=0
            print 'File not found.'
    
    values = raw.getparams()    
    
    flag=0
    flag2=False
    while not flag2:
        decision = raw_input('Should the program run through the entire file [Y/N]:')
        if decision == 'Y':
            flag=1
        elif decision == 'N':
            flag=2
        else:
            flag=3
            print 'Invalid Entry.'
            
        if flag == 1 or flag == 2:
            flag2 = True

    
    endTime = values[3]/float(values[2])
    if decision == 'N':       
        flag3=0
        while start<0.0 or start>endTime:
            if flag3==1:
                print 'Invalid Entry.'
            flag3=0
            start = float(raw_input('Enter start time [between 0.0 sec and %f sec]:' %endTime))
            flag3=1
        flag3=0
        while end<0.0 or end>endTime or end<start:
            if flag3==1:
                print 'Invalid Entry.'
            flag3=0
            end = float(raw_input('Enter end time [between 0.0 sec and %f sec]:' %endTime))
            flag3=1
    else:
        start = 0.0
        end = endTime
    
    while not carrierFrequency:
        try:
            carrierFrequency = float(raw_input('Enter the carrier frequency [Hz]:'))
           
        except ValueError:
            print 'Invalid Entry.'
    
    while not satelliteVelocity:
        try:
            satelliteVelocity = float(raw_input('Enter the satellite speed [m/s]:'))
           
        except ValueError:
            print 'Invalid Entry.'
    
    return wavReader,decision,start,end,carrierFrequency,satelliteVelocity

wavFileName,decision,start,end,carrierFrequency,satelliteVelocity = enterValues()
#intervalWidth = 1.0
#intervalStartFrequency = 20.0
#rr = rangeRate(wavFileName, start, end, intervalWidth, intervalStartFrequency, carrierfrequency, satelliteVelocity)
#rr.doCalculations()
#rr.plotFrequencyHeatMap()