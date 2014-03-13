import math
import matplotlib.pyplot as plt
import datetime as dt

ewi_latt = 51.999218            #lattitude position ground station (degree)
ewi_long = 4.373389             #longitude position ground station (degree)
ewi_heigth = 0.095              #heigth groundstation with respect to the ground (km)
ewi_nap = -0.001                #sealevel at groundstation (km)
earth_a = 6378.135              #radius of the earth at the equatorial plane (km)
earth_b = 6356.750              #radius of the earth at the polaire plane (km)
earth_omega = 7.292115*10**-5   #angular velocity of the earth (rad/s)


ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)
gs_y0 = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)
gs_z0 = gs_radius*math.sin(ewi_latt*math.pi/180)

t=0
xtab = []
ytab = []

t0 = dt.datetime(2000,01,01,11,58,55)
t1 = dt.datetime(2013,11,21,10,16,46)

trange = (t1-t0).total_seconds()

for t in range(0,):
    gs_x = gs_radius*math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180+earth_omega*t)
    gs_y = gs_radius*math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180+earth_omega*t)
    gs_z = gs_z0

    xtab.append(gs_x)
    ytab.append(gs_y)

    t = t + 1

print xtab[0],ytab[0]
print trange

#plt.plot(xtab,ytab)
#plt.plot(gs_x,gs_y,marker='x')
#plt.show()


