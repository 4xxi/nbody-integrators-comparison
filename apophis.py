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
#Here we should integrate planets to an epoch for asteroid
sim.integrate(sim.t+(2454441.5-2457724.5)/365.25) # for APOPHIS

#Now we can add asteroids ("primary" option is needed - all orbit data must be respected to the Sun)
sim.add(primary=sim.particles[0],hash='APOPHIS',m=0.0, a= 0.9222788903126814,
        e= 0.1910795219761208,inc= 3.331290217797427*d2r, omega=126.3936405969297*d2r,
        Omega=204.4571896287176*d2r, M=215.5399783483177*d2r)

f=open('APOPHIS.dat','w')
# Full time in Julian Years

#----------<< Gregorian final date (if needed to be changed)
tmax=sum(my_jd.juldat(2030,1,1,0.0))

tmax=(tmax-2454441.5)/365.25 # for APOPHIS
sim.t=0.0

#----------<< Output step in days (if needed to be changed)
step=10.

while sim.t < tmax:
    sim.integrate(min(sim.t+step/365.25, tmax)) # output time for APOPHIS
    orbit=sim.particles[10].calculate_orbit(sim.particles[0])# The orbit calculates with respect to the Sun
    # Making output to be almost the same as in .aei
    print( sim.t,orbit.pomega/d2r, orbit.M/d2r, orbit.a, orbit.e, orbit.inc/d2r,
        orbit.omega/d2r, orbit.Omega/d2r, file=f)# .aei format is very-very native

    #Uncomment next string for getting Cartesian instead of aei (and comment the string above)
    #print(sim.t,sim.particles[10].x,sim.particles[10].y,sim.particles[10].z)
    print(sim.t)
print('Done')
f.close()