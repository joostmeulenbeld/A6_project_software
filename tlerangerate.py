import math
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import scipy
from mpl_toolkits.mplot3d import Axes3D

ewi_latt = 51.999218            #lattitude position ground station (degree)
ewi_long = 4.373389             #longitude position ground station (degree)
ewi_heigth = 0.095              #heigth groundstation with respect to the ground (km)
ewi_nap = -0.001                #sealevel at groundstation (km)
earth_a = 6378.135              #radius of the earth at the equatorial plane (km)
earth_b = 6356.750              #radius of the earth at the polaire plane (km)
earth_omega = 7.292115*10**-5   #angular velocity of the earth (rad/s)

date_meas = [2013,11,21,10,16,46]   #start datetime of measurement (YYYY-MM-DD-HH-MM-SS)
meas_dur = [0,0,0,21,33]            #duration of measurement (WW-DD-HH-MM-SS)

ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)
gs_y0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)
gs_z0 = gs_radius*math.sin(ewi_latt*math.pi/180)

t_ref = dt.datetime(2000,01,01,11,58,55)
t_start = dt.datetime(date_meas[0],date_meas[1],date_meas[2],date_meas[3],date_meas[4],date_meas[5])
t_dif = dt.timedelta(meas_dur[1],meas_dur[4],0,0,meas_dur[3],meas_dur[2],meas_dur[0])
t_dif_sec = (t_dif).total_seconds()
t_end = t_start+t_dif

trange = (t_start-t_ref).total_seconds()

def gs_position(t):
    gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180+earth_omega*(trange+t))
    gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180+earth_omega*(trange+t))
    gs_z = gs_radius*math.sin(ewi_latt+math.pi/180)

    return gs_x, gs_y, gs_z

     
def gs_plot(dt,filename):

    earth_xtab = []
    earth_ytab = []
    earth_ztab = []

    for latt in range(-180,181):
        for longi in range(-90,91):
            earth_radius = math.sqrt(((((earth_a**2)*math.cos(latt*math.pi/180))**2)+(((earth_b**2)*math.sin(latt*math.pi/180))**2))/((((earth_a)*math.cos(latt*math.pi/180))**2)+(((earth_b)*math.sin(latt*math.pi/180))**2)))
            earth_x = earth_radius*math.cos(latt*math.pi/180)*math.cos(longi*math.pi/180)
            earth_y = earth_radius*math.cos(latt*math.pi/180)*math.sin(longi*math.pi/180)
            earth_z = earth_radius*math.sin(latt*math.pi/180)

            earth_xtab.append(earth_x)
            earth_ytab.append(earth_y)
            earth_ztab.append(earth_z)

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
    #ax.plot(earth_xtab,earth_ytab,earth_ztab,color='b')
    ax.plot(xtab,ytab,ztab,color='r',linewidth=5.)
    tlextab,tleytab,tleztab = tle_dataimport(filename)
    ax.plot(tlextab,tleytab,tleztab,color='g', linewidth=5.)
    ax.plot(tlextab[0:10],tleytab[0:10],tleztab[0:10],color='b', linewidth=5.)
    ax.plot(xtab[0:10],ytab[0:10],ztab[0:10],color='y',linewidth=5.)
    
def tle_dataimport(filename):
    f = np.genfromtxt(filename,delimiter="")
    tlextab=[]
    tleytab=[]
    tleztab=[]
    for i in range(len(f)):
        if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11]),int(f[i][12])) >= t_start:
            if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11]),int(f[i][12])) <= t_end:
                tlextab.append(f[i][1])
                tleytab.append(f[i][2])
                tleztab.append(f[i][3])
    return tlextab,tleytab,tleztab    
def tle_temp(filename):
    f = np.genfromtxt(filename,delimiter="")
    tlextab=[]
    tleytab=[]
    tleztab=[]
    for i in range(len(f)):
        tlextab.append(f[i][1])
        tleytab.append(f[i][2])
        tleztab.append(f[i][3])  
    return tlextab,tleytab,tleztab   
if __name__=="__main__":
           
    tle23x, tle23y, tle23z = tle_temp('tle23.xyz')
    tle24x, tle24y, tle24z = tle_temp('tle24.xyz')
    tle25x, tle25y, tle25z = tle_temp('tle25.xyz')

    tle23r =[]
    tle23an = []
    delta = []
    labda = []
    for i in range(len(tle23x)):
        r = np.sqrt(tle23x[i]**2+tle23y[i]**2+tle23z[i]**2)
        tle23r.append(r)
        delta.append(np.arcsin(tle23z[i]/tle23r[i]))
        tle23rxy = np.sqrt(tle23x[i]**2+tle23y[i]**2)
        labda.append(np.arctan2(tle23y[i]/tle23rxy,tle23x[i]/tle23rxy))
        #tle23an.append()
    plt.plot(labda)
    plt.show()
    