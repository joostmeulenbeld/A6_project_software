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
delfi_carrier = 145.87*10**6    #Carrier frequency
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
t_2000 = dt.datetime(2000,01,01,12,00,00)
t_ref = dt.datetime(2000,01,01,11,58,55)
t_start = dt.datetime(date_meas[0],date_meas[1],date_meas[2],date_meas[3],date_meas[4],date_meas[5])
t_dif = dt.timedelta(meas_dur[1],meas_dur[4],0,0,meas_dur[3],meas_dur[2],meas_dur[0])
t_dif_sec = (t_dif).total_seconds()
t_end = t_start+t_dif

trange = (t_start-t_ref).total_seconds()
j = t_start - t_2000

julianfraction = ((j.seconds)/86400.)
julianday = j.days + julianfraction
EarthRotAngle = 2*np.pi*(0.7790572732640+1.00273781191135448*julianday)

#Returns three arrays (x,y,z) of the position of the groundstation
def gs_pos():
    #Calculates the shape of the earth
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
    #Calculates the position of the groundstation
    xtab = []
    ytab = []
    ztab = []
    vxtab = []
    vytab = []
    vztab = []

    for i in xrange(int(trange),int(trange)+int(t_dif_sec)+1):
    #for i in xrange(0,60*60*24*2):

        julianfraction = ((j.seconds+i)/86400.)
        julianday = j.days + julianfraction
        EarthRotAngle = 2*np.pi*(0.7790572732640+1.00273781191135448*julianday)
        gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos((ewi_long+EarthRotAngle)*math.pi/180)	#earth_omega*i)
        gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin((ewi_long+EarthRotAngle)*math.pi/180)	#earth_omega*i)
        gs_z = gs_z0
        gs_vx = ((math.pi*2)*gs_radius*math.cos(ewi_latt*math.pi/180))*(earth_omega/(math.pi*2))*(math.cos((ewi_long+EarthRotAngle)*math.pi/180))	#earth_omega*i))
        gs_vy = ((math.pi*2)*gs_radius*math.cos(ewi_latt*math.pi/180))*(earth_omega/(math.pi*2))*(math.sin((ewi_long+EarthRotAngle)*math.pi/180))	#earth_omega*i))
        gs_vz = 0
        xtab.append(gs_x)
        ytab.append(gs_y)
        ztab.append(gs_z)      
        vxtab.append(gs_vx)
        vytab.append(gs_vy)
        vztab.append(gs_vz)
    return np.array(xtab),np.array(ytab),np.array(ztab),np.array(vxtab),np.array(vytab),np.array(vztab)
    
#Import the TLE data of a single file during the selected measurement datetime   
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
                sfix = 0
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
    
 
#Draws the groundtracks and position of the groundstation 
def groundmap():
    #Determine position of groundstation
    gsx,gsy,gsz,gsvx,gsvy,gsvz = gs_pos()
    
    #BaseMap drawings
    gmap = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    #gmap.drawcoastlines(linewidth=.25)
    #gmap.drawcountries(linewidth=.25)
    #gmap.fillcontinents(color='g',lake_color='b')
    gmap.drawmapboundary(fill_color='b')
    gmap.drawmeridians(np.arange(0,360,30))
    gmap.drawparallels(np.arange(-90,90,30))
    gmap.bluemarble()
    tlong = np.arange(trange,trange+t_dif_sec+1,1)


    #Converting from xyz j2000 to longitude and latitude
    longref = ((EarthRotAngle%(2*np.pi))*(180./np.pi))
    longref = 360-longref
    longgs = (180./np.pi)*np.arctan2(gsy,gsx)
    latgs = (180./np.pi)*np.arctan2(gsz,np.sqrt(gsx*gsx+gsy*gsy))
    #Compensates for the rotation of the earth for groundstation
    for i in range(len(tlong)):
        longgs[i] +=longref
        longgs[i] = longgs[i]%(360)

    
    #Converts xyz of TLE files to longitude and latitude  
    for k in range(len(filelist)):
        fname = filelist[k]
        lcolor = ['y','y','y'] 
        x,y,z,vx,vy,vz = tle_import(fname)
        longsat = ((180./np.pi)*np.arctan2(y,x))   
        latsat = (180./np.pi)*np.arctan2(z,np.sqrt(x*x+y*y))        
        for j in range(len(tlong)):
            longsat[j] += longref
            longsat[i] = longsat[i]%(360)
        #Rescales satellite coordinates for map draw and draws the track
        x,y = gmap(longsat,latsat)
        
        gmap.plot(x,y,color=lcolor[k],linewidth=2)
       
    #Rescales groundstation coordinates for map draw and draws the position  
    gsx,gsy = gmap(longgs,latgs)
    
    gmap.plot(gsx,gsy,color='aqua',linewidth=5)
    EarthRotAngle
    return plt.show()
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
def zenangle():
    posdif = position_diff()
             
    for l in range(len(filelist)):
        fname = filelist[l]
        x,y,z,vx,vy,vz = tle_import(fname)
        
        xgs,ygs,zgs,vxgs,vygs,vzgs = gs_pos()
        
        alpha = np.arcsin(ewi_sealevel/gs_radius)
        heightsat = np.sqrt(x*x+y*y+z*z)
        r = posdif[l][2]
        
        r = np.array(r)
          
        beta = np.arccos(((gs_radius*gs_radius)+r*r-(heightsat*heightsat))/(2*(gs_radius)*r))
        horangle = (beta-alpha)*(180./np.pi)
        plt.plot(horangle)        
        
    plt.show()
    
def compare(exprangerate):
    tlerr = tlerangerate()
    
    for i in range(len(tlerr)):
        pltlabel = filelist[i]
        plt.plot(tlerr[i][1],label=pltlabel)
    plt.plot(exprangerate[0],exprangerate[1],label='Experiment')
    plt.xlabel("Time (s)")
    plt.ylabel("Range-Rate (km/s)")
    plt.legend()
    plt.show()
    
    for s in range(len(tlerr)):
        errorlist = []
        for t in range(len(exprangerate[1])):
            print len(exprangerate[0])
            time = exprangerate[0][t]
            timelow= int(time)
            timedif=time-timelow
            interpolated = tlerr[s][1][timelow]+timedif*(tlerr[s][1][timelow+1]-tlerr[s][1][timelow])
            error = abs(exprangerate[1][t]-interpolated)
            
            errorlist.append(error)
        plt.plot(exprangerate[0],errorlist)
    plt.xlabel("Time (s)")
    plt.ylabel("Error (km/s)")
    plt.show()
#dummydif = position_diff()
#plt.plot(dummydif[0][1],dummydif[0][2])
#plt.show()
#groundmap()