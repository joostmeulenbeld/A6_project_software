import math
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap

ewi_latt = 51.999218            #lattitude position ground station (degree)
ewi_long = 4.373389             #longitude position ground station (degree)
ewi_heigth = 0.095              #heigth groundstation with respect to the ground (km)
ewi_nap = -0.001                #sealevel at groundstation (km)
earth_a = 6378.135              #radius of the earth at the equatorial plane (km)
earth_b = 6356.750              #radius of the earth at the polaire plane (km)
earth_omega = 7.29211509*10**-5   #angular velocity of the earth (rad/s)

date_meas = [2013,11,21,10,16,46]   #start datetime of measurement (YYYY-MM-DD-HH-MM-SS)
meas_dur = [0,0,0,21,33]            #duration of measurement (WW-DD-HH-MM-SS)

filelist = ['tle23.xyz','tle24.xyz','tle25.xyz']
#1 Calculation position groundstation in J2000
ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)
gs_y0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)
gs_z0 = gs_radius*math.sin(ewi_latt*math.pi/180)


#2 time calculations
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


#De aardbol, de banen van de gs en sataliet plotten.    
def gs_plot(dt):

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
    for i in xrange(int(trange),int(trange)+dt+1):
        gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180+earth_omega*i)
        gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180+earth_omega*i)
        gs_z = gs_z0

        xtab.append(gs_x)
        ytab.append(gs_y)
        ztab.append(gs_z)
        dt = dt + 1
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot(earth_xtab,earth_ytab,earth_ztab,color='b')         #plot earth
    #ax.plot(xtab,ytab,ztab,color='r',linewidth=1.)              #plot groundstation track
    #tlextab,tleytab,tleztab = tle_dataimport()
    #ax.plot(tlextab,tleytab,tleztab,color='g', linewidth=1.)    #plot satalite track
    #plt.show()

    return np.array(xtab),np.array(ytab),np.array(ztab)


#TLE data importeren en het gedeelte selecteren dat de juiste tijd heeft.   
def tle_dataimport(fname):
    f = np.genfromtxt(fname,delimiter="")
    tlextab=[]
    tleytab=[]
    tleztab=[]
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
    return np.array(tlextab),np.array(tleytab),np.array(tleztab)


#De verschillen in x, y, z positie bepalen tussen gs en sataliet. Die vervolgens kwadrateren, bij elkaar optellen en de wortel daarvan geeft de afstand.
def position_diff():
    xtab,ytab,ztab = gs_plot(int(t_dif_sec))
    tlextab,tleytab,tleztab = tle_dataimport()
    distance = []
    barx = []
    bary = []
    barz = []
    ttab = []
    t = 0
    for i in range(len(xtab)):
        x = abs(xtab[i]-tlextab[i])
        y = abs(ytab[i]-tleytab[i])
        z = abs(ztab[i]-tleztab[i])
        t = t + 1

        dist = ((x**2)+(y**2)+(z**2))**0.5

        distance.append(dist)
        barx.append(x)
        bary.append(y)
        barz.append(z)
        
        ttab.append(t)

    return distance, ttab, barx, bary,barz

def groundmap(gsx,gsy,gsz,trange):
    
    gmap = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    gmap.drawcoastlines(linewidth=.25)
    gmap.drawcountries(linewidth=.25)
    gmap.fillcontinents(color='g',lake_color='b')
    gmap.drawmapboundary(fill_color='b')
    gmap.drawmeridians(np.arange(0,360,30))
    gmap.drawparallels(np.arange(-90,90,30))
    
    tlong = np.arange(trange,trange+t_dif_sec+1,1)
    
    longref = (((tlong*earth_omega)%(2*np.pi))*(180./np.pi))
    longref = 360-longref
    longgs = (180./np.pi)*np.arctan2(gsy,gsx)
    latgs = (180./np.pi)*np.arctan2(gsz,np.sqrt(gsx*gsx+gsy*gsy))
    for i in range(len(tlong)):
        longgs[i] += longref[i]   
    debuglist = []    
    for i in range(len(filelist)):
        fname = filelist[i]
        lcolor = ['r','y','black'] 
        print i,lcolor[i]
        x,y,z = tle_dataimport(fname)
        longsat = ((180./np.pi)*np.arctan2(y,x))   
        latsat = (180./np.pi)*np.arctan2(z,np.sqrt(x*x+y*y))        
        for j in range(len(tlong)):
            longsat[j] += longref[j]
        
        x,y = gmap(longsat,latsat)
        gmap.plot(x,y,color=lcolor[i],linewidth=1)
        debuglist.append(x)
    gsx,gsy = gmap(longgs,latgs)
    gmap.plot(gsx,gsy,color='y',linewidth=2)
    
    plt.show()
    
    
    return debuglist
#Plot tijd vs. afstand gs/sataliet
#plt.plot(position_diff()[1],position_diff()[0])
#plt.plot(position_diff()[1],position_diff()[2])
#plt.plot(position_diff()[1],position_diff()[3])
#plt.plot(position_diff()[1],position_diff()[4])

#aanpassing
gsx,gsy,gsz = gs_plot(int(t_dif_sec))
debuglist = groundmap(gsx,gsy,gsz,trange)


plt.show()
