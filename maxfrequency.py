import numpy as np

# here comes some syntax to read the file from group 1
file=open("C:\Users\Rimsky\Documents\Canopy Enthought Python\Python codes\ja.txt","r")
f=file.readlines()



# column per time interval with the frequencies versus the amplitude
g = np.genfromtxt(f,delimiter=" ")

# while loop for all the time intervals
# search for highest amplitude and give back the frequency
# need some kind of algorithm to filter:
#   noise, or peaks out of the boundary
#   do we start in the middle because we know the carrier frequency
#   and work outwards, so we can track it compared to result before?
print str(g)
h=max(g[:,1])
n=0
while g[n,1]!=h:
    n=n+1
print g[n,0]

#print a file with for each time interval the highest frequency
#i  | t(s)| f(Hz)
#0  |  1  |  304
#1  |  11 |  301
#2  |  21 |  297
#3  |  31 |  293
