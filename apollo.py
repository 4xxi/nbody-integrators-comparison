import rebound as rp
import my_jd
import math as m

# Initialization of Simulation object
sim=rp.Simulation()

# This was a try to get planet XYZ from NASA Horizons web-interface
# It required strict date format (e.g. "2012-12-31 15:48", only Gregorian calendar).
# In Mercury6 we used Julian Dates, so that I used a handmade module for transform

# This is a test for my_jd
jdate=list(reversed(m.modf(2457724.5)))
date=my_jd.gregdat(*jdate)
yr=int(date[0])
mon=int(date[1])
day=int(date[2])
hour=int(m.trunc(date[3]))
mi=int(m.trunc((date[3]-hour)*60.0))
# No seconds - Rebound doesn't get it
date="{y:4}-{m:02}-{d:02} {h:02}:{mi:02}".format(y=yr,m=mon,d=day,h=hour,mi=mi)
print(date)

# There were strings:
#sim.add("Sun",date=date)
#sim.add("Mercury",date=date)
# etc. However, it tooks coordinate only in.. umm.. barycentric system
# Mercury6 uses heliocentric, transformations are long,
# so i desided to avoid using this way of getting planet XYZ and use "big.in"

# Use units as in Mercury (but not exactly, unfortunately)
sim.units=('au','msun','yr')# 'yr' is Julian Year (365.25 days)
sim.add(m=1., hash='sun')

f=open('big.in').readlines()[6:]
print(len(f))
j=0
for i in range(9):

    s=f[j].strip().split()
    name=s[0]
    mass=float(s[1].split('=')[1].replace('D','e'))# Defortranization of floats
    j+=1

    s=f[j].strip().replace('D','e').split()# Defortranization of floats
    x=float(s[0])
    y=float(s[1])
    z=float(s[2])
    j+=1

    s=f[j].strip().replace('D','e').split()
    vx=float(s[0])*365.25
    vy=float(s[1])*365.25# Converting from AU/d to AU/year
    vz=float(s[2])*365.25
    
    j+=2
    print(name)
    sim.add(x=x,y=y,z=z,vx=vx,vy=vy,vz=vz,m=mass,hash=name)# Adding a planet in Simulation
    # I hoped that cartesian coordinates had not been in Jacobi system. It seems to be right.

sim.t=0.0


#Here we should integrate big bodies to an epoch for asteroid

#sim.integrate(sim.t+(2457600.5-2457724.5)/365.25) # for A309239
sim.integrate(sim.t+(2454441.5-2457724.5)/365.25) # for APOPHIS

# deg2rad transformer
d2r=m.pi/180.0

#Now we can add asteroids ("primary" option is needed - all orbit data must be respect to Sun)

#sim.add(primary=sim.particles[0],hash='A309239',m=0.0, a= 30.1599737273,
        #e= 0.299867632834,inc= 36.171537173*d2r, omega=95.6848079103*d2r,
        #Omega=187.073106753*d2r, M=66.9833825759*d2r)
sim.add(primary=sim.particles[0],hash='APOPHIS',m=0.0, a= 0.9222788903126814,
        e= 0.1910795219761208,inc= 3.331290217797427*d2r, omega=126.3936405969297*d2r,
        Omega=204.4571896287176*d2r, M=215.5399783483177*d2r)
# Omega is Node, omega is pericenter 


# here will be output
f=open('APOPHIS.dat','w')
#fk=open('MERCURY.dat','w')

# it was for Apophis, because I forgot to
# change start time of integration in Mercury6 test sample
sim.integrate(sim.t+(2457600.5-2454441.5)/365.25)

# Full time in Julian Years
#tmax=(38976000.5-2457600.5)/365.25 # for A309239
tmax=(2501000.5-2457600.5)/365.25 # for APOPHIS

# Adjust start time 
sim.t=0.0
while sim.t < tmax:
    #sim.integrate(min(sim.t+3650.25/365.25, tmax)) # output time for A309239
    sim.integrate(min(sim.t+3., tmax)) # output time for APOPHIS

    orbit=sim.particles[10].calculate_orbit(sim.particles[0]) # Asteroid is 11-th in body list
    # Orbit calculates with respect to Sun
    
    # Making output to be almost the same as in .aei
    print(sim.t, orbit.pomega/d2r, orbit.M/d2r, orbit.a, orbit.e, orbit.inc/d2r,
          orbit.omega/d2r, orbit.Omega/d2r, file=f)

    print(sim.t)

print('Done')
f.close()
# Test sample is ready