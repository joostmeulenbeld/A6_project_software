# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 12:40:36 2014
Range-rate calculation
Input: Max Frequency over time matrix
Output: Range rate over time matrix
@author: Maarten Schild, Project A6
"""
import maxfrequency

timefreq = maxfrequency #Add variable name of maxfrequency file here#

debugfreq = 146*10**6

carrierfreq = debugfreq #Hz
speedoflight = 299792458 #m/s

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
def rangerateconvert(timefreq,carrierfreq):
    timerangerate = timefreq
    for i in range(len(timefreq)):
        timerangerate[i][1] = calcrangerate(timefreq[i][1],carrierfreq,speedoflight)
    return timerangerate
