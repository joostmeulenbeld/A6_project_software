import math
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

ewi_latt = 51.999218            #lattitude position ground station (degree)
ewi_long = 4.373389             #longitude position ground station (degree)
ewi_heigth = 0.095              #heigth groundstation with respect to the ground (km)
ewi_nap = -0.001                #sealevel at groundstation (km)
earth_a = 6378.135              #radius of the earth at the equatorial plane (km)
earth_b = 6356.750              #radius of the earth at the polaire plane (km)
earth_omega = 7.292115*10**-5   #angular velocity of the earth (rad/s)

meas_t0 = [2013,11,21,10,16,46] #start datetime of measurement (YYYY-MM-DD-HH-MM-SS)
meas_dur = [0,0,0,21,33]      #duration of measurement (WW-DD-HH-MM-SS)

ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)
gs_y0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)
gs_z0 = gs_radius*math.sin(ewi_latt*math.pi/180)

t2000 = dt.datetime(2000,01,01,11,58,55)
t0 = dt.datetime(meas_t0[0],meas_t0[1],meas_t0[2],meas_t0[3],meas_t0[4],meas_t0[5])
tdelta = dt.timedelta(meas_dur[1],meas_dur[4],0,0,meas_dur[3],meas_dur[2],meas_dur[0])
tdelta_sec = (tdelta).total_seconds()
tend = t0+tdelta

trange = (t0-t2000).total_seconds()

def gs_position(t):
    gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180+earth_omega*(trange+t))
    gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180+earth_omega*(trange+t))
    gs_z = gs_radius*math.sin(ewi_latt+math.pi/180)

    return gs_x, gs_y, gs_z

     
def gs_plot(dt):

    xtab = []
    ytab = []
    ztab = []
    for i in xrange(int(trange),int(trange)+dt):
        gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180+earth_omega*i)
        gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180+earth_omega*i)
        gs_z = gs_z0

        xtab.append(gs_x)
        ytab.append(gs_y)
        ztab.append(gs_z)
        dt = dt + 1
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xtab,ytab,ztab)
    tlextab,tleytab,tleztab = tle_dataimport()
    ax.plot(tlextab,tleytab,tleztab)
    plt.show()

    
def tle_dataimport():
    f = np.genfromtxt("tle23.xyz",delimiter="")
    tlextab=[]
    tleytab=[]
    tleztab=[]
    for i in range(len(f)):
        if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11]),int(f[i][12])) >= t0:
            if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11]),int(f[i][12])) <= tend:
                tlextab.append(f[i][1])
                tleytab.append(f[i][2])
                tleztab.append(f[i][3])
                print 'added'
    return tlextab,tleytab,tleztab

gs_plot(int(tdelta_sec))
#tle_dataimport()
