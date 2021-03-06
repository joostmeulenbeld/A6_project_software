import math
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
try:
    from mpl_toolkits.basemap import Basemap
except:
        pass
#===============================================================================
#                           Definition of variables
#===============================================================================
ewi_latt = 51.999218            #lattitude position ground station (degree)
ewi_long = 4.373389             #longitude position ground station (degree)
ewi_heigth = 0.095              #heigth groundstation (km)
ewi_nap = -0.001                #sealevel at groundstation (km)
earth_a = 6378.135              #radius of the earth at the equatorial plane (km)
earth_b = 6356.750              #radius of the earth at the polaire plane (km)
earth_omega = 7.2921151467064*10**-5 #angular velocity of the earth (rad/s)

#===============================================================================
#                  User Input of Measurement time and files
#===============================================================================
date_meas = [2013,11,21,10,16,46]                   #Start datetime of measurement (YYYY-MM-DD-HH-MM-SS)
meas_dur = [0,0,0,21,33]                            #Duration of measurement (WW-DD-HH-MM-SS)
filelist = ['tle23.xyz','tle24.xyz','tle25.xyz']    #Have to be in the same folder as this script

#===============================================================================
#                                          Main Code
#               Written by projectgroup A6 for the second year project AE2223-I
#                                      Required Modules
#   Matplotlib      -http://matplotlib.org/
#   Numpy           -http://www.numpy.org/
#   Basemap         -http://matplotlib.org/basemap/
#
#                           This file consists of four functions
#   gs_pos()        -Determines the position of the groundstation for the given datetime
#   tle_import()    -Returns (x,y,z) arrays in J2000 of the satellite for a given TLE data file
#   position_diff() -Returns an [filename,time,distance,x,y,z] array for all TLE data files
#   groundmap()     -Draws the position of the groundstation and groundtracks for all TLE data files
#===============================================================================
#Calculation of the start position of the groundstation in J2000
ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)
gs_y0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)
gs_z0 = gs_radius*math.sin(ewi_latt*math.pi/180)

#Time definitions and difference calculations

t_ref = dt.datetime(2000,01,01,11,58,55,816000) #Is start of J2000 in UTC

t_start = dt.datetime(date_meas[0],date_meas[1],date_meas[2],date_meas[3],date_meas[4],date_meas[5])
t_dif = dt.timedelta(meas_dur[1],meas_dur[4],0,0,meas_dur[3],meas_dur[2],meas_dur[0])
t_dif_sec = (t_dif).total_seconds()
t_end = t_start+t_dif
trange = (t_start-t_ref).total_seconds()
j = t_start - t_ref

#Returns an array (x,y,z,vx,vy,vz) of the position and velocity of the groundstation during the measurement
def gs_pos():
    #Create empty lists
    xtab = []
    ytab = []
    ztab = []
    vxtab = []
    vytab = []
    vztab = []

    for t in xrange(int(trange),int(trange)+int(t_dif_sec)+1):
        #Determine the rotation of the earth with rspect to J2000    
        julianfraction = ((j.seconds+t)/86400.)+(j.microseconds/1000000.)
        julianday = j.days + julianfraction
        EarthRotAngle = 2*np.pi*(0.7790572732640+1.00273781191135448*julianday)
        #Calculate position and velocity
        gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos((ewi_long*math.pi/180)+EarthRotAngle)	
        gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin((ewi_long*math.pi/180)+EarthRotAngle)	
        gs_z = gs_z0
        gs_vx = ((math.pi*2)*gs_radius*math.cos(ewi_latt*math.pi/180))*(earth_omega/(math.pi*2))*(math.cos((ewi_long*math.pi/180)+EarthRotAngle))	
        gs_vy = ((math.pi*2)*gs_radius*math.cos(ewi_latt*math.pi/180))*(earth_omega/(math.pi*2))*(math.sin((ewi_long*math.pi/180)+EarthRotAngle))	
        gs_vz = 0
        #Store values in list
        xtab.append(gs_x)
        ytab.append(gs_y)
        ztab.append(gs_z)      
        vxtab.append(gs_vx)
        vytab.append(gs_vy)
        vztab.append(gs_vz)
    return np.array(xtab),np.array(ytab),np.array(ztab),np.array(vxtab),np.array(vytab),np.array(vztab)
    
#Import the TLE data of a single file during the selected measurement datetime 
#Returns an array (x,y,z,vx,vy,vz) with the position and velocity of the satellite
def tle_import(fname):
    f = np.genfromtxt(fname,delimiter="")
    tlextab=[]
    tleytab=[]
    tleztab=[]
    tlevxtab=[]
    tlevytab=[]
    tlevztab=[]
    for i in range(len(f)):
        if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11]),int(f[i][12])) >= t_start:
            sfix =  int(round(f[i][12]))
            if sfix == 60:
                sfix = 05
                mfix = 1
            else:
                mfix=0
            if dt.datetime(int(f[i][7]),int(f[i][8]),int(f[i][9]),int(f[i][10]),int(f[i][11])+mfix,sfix) <= t_end:
                    tlextab.append(f[i][1])
                    tleytab.append(f[i][2])
                    tleztab.append(f[i][3])
                    tlevxtab.append(f[i][4])
                    tlevytab.append(f[i][5])
                    tlevztab.append(f[i][6])
    return np.array(tlextab),np.array(tleytab),np.array(tleztab),np.array(tlevxtab),np.array(tlevytab),np.array(tlevztab)


#Determination of the distance between the satellite and the groundstation
def position_diff():
    posdif = []
    xtab,ytab,ztab,vxtab,vytab,vztab = gs_pos()
    for l in range(len(filelist)):
        fname = filelist[l]
        tlextab,tleytab,tleztab,tlevx,tlevy,tlevz = tle_import(fname)
        dtab = []
        ttab = []
        dxtab=[]
        dytab=[]
        dztab=[]
        t = 0
        for i in range(len(xtab)):
            x = xtab[i]-tlextab[i]
            y = ytab[i]-tleytab[i]
            z = ztab[i]-tleztab[i]
            t = t + 1
    
            dist = ((x**2)+(y**2)+(z**2))**0.5
            dxtab.append(x)
            dytab.append(y)
            dztab.append(z)            
            dtab.append(dist)
            ttab.append(t)
        dummy = [filelist[l],ttab,dtab,dxtab,dytab,dztab]
        posdif.append(dummy)
        
    return posdif

def tlerangerate():
    rrlist=[]
    for l in range(len(filelist)):
        fname = filelist[l]
        x,y,z,vx,vy,vz = tle_import(fname)
        xgs,ygs,zgs,vxgs,vygs,vzgs = gs_pos()
        
        tvx = vx-vxgs
        tvy = vy-vygs
        tvz = vz-vzgs

        posd = position_diff()
        dotprod = []
        for m in range(len(tvx)):
            
            tvect = np.array([tvx[m],tvy[m],tvz[m]])
            pvect = np.array([posd[l][3][m],posd[l][4][m],posd[l][5][m]])
            
            plen = math.sqrt(pvect[0]*pvect[0]+pvect[1]*pvect[1]+pvect[2]*pvect[2])
            pvectnorm = [pvect[0]/plen,pvect[1]/plen,pvect[2]/plen]
            dotprod.append(np.dot(tvect,pvectnorm))
                        
        dummy2 = [filelist[l],dotprod]
                    
        rrlist.append(dummy2)
        
    return rrlist
    
def interpolation(y0,y1,x,x0,x1):
    newValue=y0+(y1-y0)*((x-x0)/(x1-x0))
    return newValue
def compare(exprangerate,newtimedeltav,tletimedeltav, mode="disp"):
    tlerr = tlerangerate()
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(tlerr[0][1],color='red',label='TLE')
    
    check=exprangerate[0][0]
    ax1.plot(exprangerate[0][0],exprangerate[1][0],'gs',label='Model 1')
    for i in range(len(exprangerate[0])):
        if check<=exprangerate[0][i]:
            ax1.plot(exprangerate[0][i],exprangerate[1][i],'gs')
            check=check+100           
    ax1.plot(exprangerate[0],exprangerate[1],'g')
    
    check=newtimedeltav[0][0]
    ax1.plot(newtimedeltav[0][0],newtimedeltav[1][0],'c<',label='Model 2')
    for i in range(len(newtimedeltav[0])):
        if check<=newtimedeltav[0][i]:
            ax1.plot(newtimedeltav[0][i],newtimedeltav[1][i],'c<')
            check=check+100  
    ax1.plot(newtimedeltav[0],newtimedeltav[1],'c')
    
    check=tletimedeltav[0][0]
    ax1.plot(tletimedeltav[0][0],tletimedeltav[1][0],'bo',label='Model 3')
    for i in range(len(tletimedeltav[0])):
        if check<=tletimedeltav[0][i]:
            ax1.plot(tletimedeltav[0][i],tletimedeltav[1][i],'bo')
            check=check+100 
    ax1.plot(tletimedeltav[0],tletimedeltav[1],'b')
    
    plt.xlabel("Time (s)")
    plt.ylabel("Range-Rate (km/s)")
    plt.xlim(400,1200)
    plt.ylim(-11, 15)
    plt.legend()
    if mode == "save":
        plt.savefig("img/RangeRate-Time.png", bbox_inches='tight', dpi=400)


    error1temp = errorCount(exprangerate)
    error1 = [abs(error1temp[n]) for n in range(len(error1temp))]
    error2temp = errorCount(newtimedeltav)
    error2 = [abs(error2temp[n]) for n in range(len(error2temp))]
    error3temp = errorCount(tletimedeltav)
    error3 = [abs(error3temp[n]) for n in range(len(error3temp))]
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    
    check=exprangerate[0][0]
    ax2.plot(exprangerate[0][0],error1[0],'gs',label='Model 1')
    for i in range(len(exprangerate[0])):
        if check<=exprangerate[0][i]:
            ax2.plot(exprangerate[0][i],error1[i],'gs')
            check=check+100           
    ax2.plot(exprangerate[0],error1,'g')
    
    check=newtimedeltav[0][0]
    ax2.plot(newtimedeltav[0][0],error2[0],'c<',label='Model 2')
    for i in range(len(newtimedeltav[0])):
        if check<=newtimedeltav[0][i]:
            ax2.plot(newtimedeltav[0][i],error2[i],'c<')
            check=check+100           
    ax2.plot(newtimedeltav[0],error2,'c')
    
    check=tletimedeltav[0][0]
    ax2.plot(tletimedeltav[0][0],error3[0],'bo',label='Model 3')
    for i in range(len(tletimedeltav[0])):
        if check<=tletimedeltav[0][i]:
            ax2.plot(tletimedeltav[0][i],error3[i],'bo')
            check=check+100           
    ax2.plot(tletimedeltav[0],error3,'b')
    
    plt.xlabel("Time (s)")
    plt.ylabel("Error (km/s)")
    plt.xlim(550,1020)
    plt.ylim(0,5.5)
    plt.legend()

    if mode == "disp":
        plt.show()
    else:
        plt.savefig("img/ErrorPlot.png", bbox_inches='tight', dpi=400)


    
    
def errorCount(rangerate):
    tlerr = tlerangerate()
    errorlist = []
    for i in range(len(rangerate[0])):
        rr0 = tlerr[0][1][int(rangerate[0][i])]
        rr1 = tlerr[0][1][int(rangerate[0][i])+1]
        t = rangerate[0][i]
        t0 = int(rangerate[0][i])
        t1 = int(rangerate[0][i])+1
        rr = interpolation(rr0,rr1,t,t0,t1)
        errorlist.append(rangerate[1][i]-rr)
    return errorlist
        
