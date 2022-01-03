import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import datetime


# -----------------------------------------------------------------------------------------+
archive1 = '/home/adrisanj/informe_practicas/outputs_opendrift/OD_eco_sim.nc'

nc1 = netCDF4.Dataset(archive1)
lon1 = nc1.variables['lon'][:]
lat1 = nc1.variables['lat'][:]
time1 = nc1.variables['time'][:]
egg1 = nc1.variables['hatched'][:]
l1 = nc1.variables['length'][:]
z1 = nc1.variables['z'][:]

# -----------------------------------------------------------------------------------------+
archive2 = '/home/adrisanj/informe_practicas/outputs_ichthyop/roms3d_ichthyop-run202112311950.nc'

nc2 = netCDF4.Dataset(archive2)
lon2 = nc2.variables['lon'][:]
lat2 = nc2.variables['lat'][:]
time2 = nc2.variables['time'][:]
egg2 = nc2.variables['stage'][:]
l2 = nc2.variables['length'][:]
z2 = nc2.variables['depth'][:]

# -----------------------------------------------------------------------------------------+

# OpenDrift

initime_1 = datetime.datetime(1970,1,1)
fintime_1 = []
for t in time1:
    fintime_1.append(initime_1+datetime.timedelta(t/86400.))
    
    
plt.figure()
plt.subplot(311)
for i in range(0,1000):
    plt.plot(fintime_1, l1[i,:])

plt.subplot(312)
for i in range(0,1000):    
    plt.plot(fintime_1, egg1[i,:])

plt.subplot(313)
medias1 = []
for i in range(len(z1[0,:])):
    medias1.append(np.mean(z1[:,i]))
for i in range(0,5000):       # Here we represent the total media of the depth, and a few trajectories.
    plt.plot(fintime_1,z1[i,:],'g--')
plt.plot(fintime_1,medias1,'b-')
plt.show()

# -----------------------------------------------------------------------------------------+

initime_2=datetime.datetime(2006,1,1)
fintime_2=[]
for t in time2:
    fintime_2.append(initime_2+datetime.timedelta(t/86400.))
    
plt.figure()
plt.subplot(311)
for i in range(0,1000):
    plt.plot(fintime_2,l2[:,i])

plt.subplot(312)
for i in range(0,10):    
    plt.plot(fintime_2,egg2[:,i])
#plt.plot(fintime,egg[:])

plt.subplot(313)
medias2 = []
for i in range(0,len(z2[:,0])):
    medias2.append(np.mean(z2[i,:]))
for i in range(0,100):
    plt.plot(fintime_2,z2[:,i], 'g--')

#plt.plot(fintime,z[:], 'g--')
plt.plot(fintime_2,medias2,'b-')
plt.show()

# -----------------------------------------------------------------------------------------+

# Depth comparision

plt.figure()
plt.plot(fintime_1,medias1,'r-')
plt.plot(fintime_2,medias2,'b-')
plt.grid()
plt.title('Profundidades vs tiempo')
plt.show()
