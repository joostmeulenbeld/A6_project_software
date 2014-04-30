# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 12:40:36 2014
Range-rate calculation
Input: Max Frequency over time matrix
Output: Range rate over time matrix
@author: Maarten Schild, Project A6
"""
#Add variable name of maxfrequency file here#
speedoflight = 299792.458 #km/s

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
    test = []
    for i in range(len(timefreq[1])):
        test.append(calcrangerate(timefreq[1][i],carrierfreq,speedoflight))
        
    return test
