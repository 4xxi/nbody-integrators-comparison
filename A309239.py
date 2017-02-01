import rebound as rp
import my_jd
import math as m

d2r=m.pi/180.0
sim=rp.Simulation()
sim.units=('au','msun','yr')# 'yr' is Julian Year (365.25 days)
sim.add(m=1., hash='sun')
# Getting planet positions
f=open('big.in').readlines()[6:]
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

sim.t=0.0
#Here we should integrate big bodies to an epoch for asteroid
sim.integrate(sim.t+(2457600.5-2457724.5)/365.25) # for A309239

#Now we can add asteroids ("primary" option is needed - all orbit data must be respected to theSun)
sim.add(primary=sim.particles[0],hash='A309239',m=0.0, a= 30.1599737273,
        e= 0.299867632834,inc= 36.171537173*d2r, omega=95.6848079103*d2r,
        Omega=187.073106753*d2r, M=66.9833825759*d2r)

f=open('A309239.dat','w')
# Full time in Julian Years
tmax=(38976000.5-2457600.5)/365.25 # for A309239
sim.t=0.0
while sim.t < tmax:
    sim.integrate(min(sim.t+3650.25/365.25, tmax)) # output time for A309239
    orbit=sim.particles[10].calculate_orbit(sim.particles[0]) # Asteroid is 11-th in body list. The orbit calculates with respect to the Sun
    # Making output to be almost the same as in .aei
    print( sim.t,orbit.pomega/d2r, orbit.M/d2r, orbit.a, orbit.e, orbit.inc/d2r,
        orbit.omega/d2r, orbit.Omega/d2r, file=f)
    
    #Uncomment next string for getting Cartesian instead of aei (and comment the string above)
    #print(sim.t,sim.particles[10].x,sim.particles[10].y,sim.particles[10].z)
    print(sim.t)
print('Done')
f.close()