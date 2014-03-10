# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 12:40:36 2014
Range-rate calculation
Input: Max Frequency over time matrix
Output: Range rate over time matrix
@author: Maarten Schild
"""
import numpy
import random
debugfreq = 146*10**6

carrierfreq = debugfreq #Hz
speedoflight = 299792458 #m/s

m = []
l = numpy.linspace(0,1200,80000)
for a in l:
    m.append([a,carrierfreq-random.randint(0,1000)*1000])

timefreq = m


#Function to calculate the difference in velocity between receiver and transmitter
#Inputs are received frequency(Hz), transmitted frequency(Hz) and speed of light(m/s)
#Output is difference in velocity (m/s)
def calcrangerate(freq,carrierfreq,speedoflight):
    deltafreq = freq - carrierfreq
    deltav = (deltafreq * speedoflight)/carrierfreq
    return deltav
    
#Function to convert the time-maxfrequency matrix to a time-deltavelocity matrix
#Inputs are the time-maxfrequency matrix(list[t][Hz]), transmitted frequency (Hz) and speed of light(m/s)
#Output is a time-rangerate matrix (list[t][m/s])
#Uses calcrangerate function
def rangerateconvert(timefreq,carrierfreq,speedoflight):
    timerangerate = timefreq
    for i in range(len(timefreq)):
        timerangerate[i][1] = calcrangerate(timefreq[i][1],carrierfreq,speedoflight)
    return timerangerate

    
#print rangerateconvert(timefreq,carrierfreq,speedoflight)