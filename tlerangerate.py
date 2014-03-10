import math

ewi_latt = 51.999218    #lattitude position ground station
ewi_long = 4.373389     #longitude position ground station
ewi_heigth = 0.095      #heigth groundstation with respect to the ground
ewi_nap = -0.001        #sealevel at groundstation
earth_a = 6378.135     #radius of the earth at the equatorial plane
earth_b = 6356.750    #radius of the earth at the polaire plane
earth_omega = 7.292115*10**-5   #angular velocity of the earth


ewi_sealevel = math.sqrt(((((earth_a**2)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b**2)*math.sin(ewi_latt*math.pi/180))**2))/((((earth_a)*math.cos(ewi_latt*math.pi/180))**2)+(((earth_b)*math.sin(ewi_latt*math.pi/180))**2)))
gs_radius = ewi_sealevel + ewi_nap + ewi_heigth

gs_x0 = math.cos(ewi_latt*math.pi/180)*math.cos(ewi_long*math.pi/180)*gs_radius
gs_y0 = math.cos(ewi_latt*math.pi/180)*math.sin(ewi_long*math.pi/180)*gs_radius
gs_z0 = math.sin(ewi_latt*math.pi/180)*gs_radius

t = 24*3600

gs_x = gs_radius*math.cos(ewi_long*math.pi/180+earth_omega*t)
gs_y = gs_radius*math.sin(ewi_long*math.pi/180+earth_omega*t)
gs_z = gs_z0

print earth_omega*t+ewi_long*math.pi/180
