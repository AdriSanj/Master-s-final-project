import numpy as np
import sys
#import matplotlib as mpl
import matplotlib.pyplot as plt
import netCDF4
import datetime
import glob
import os
os.environ['PROJ_LIB'] ='/opt/miniconda/miniconda3/share/proj'
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata

# --------------------------------------------------------------------------+

particle_size = 0.1

# Mapping selection zone with lon and lat of the globe
minlon = -9.4
maxlon = -8.6
minlat = 41.4
maxlat = 42.2


# For all particles run
#minlon = -13
#maxlon = -1
#minlat = 37
#maxlat = 46.5

# --------------------------------------------------------------------------+

# Dont touch unless specified by the archive
#initime = datetime.datetime(1900,1,1)		# For Ichthyop comparisions
#initime = datetime.datetime(2013,5,1)
initime = datetime.datetime(2009,1,1)

# --------------------------------------------------------------------------+

# Opendrift

archive_1 = '/home/adrisanj/informe_practicas/outputs_opendrift/may_2013_diffusivity_hor_vert.nc'

nc_1 = netCDF4.Dataset(archive_1)
lon_od = nc_1.variables['lon'][:]
lat_od = nc_1.variables['lat'][:]
z_od = nc_1.variables['z'][:]
time_od = nc_1.variables['time'][:]

# --------------------------------------------------------------------------+

# Ihcthyop 

archive_2 = '/home/adrisanj/informe_practicas/outputs_ichthyop/roms3d_ichthyop-run202112271645.nc'

nc_2 = netCDF4.Dataset(archive_2)
lon_ich = nc_2.variables['lon'][:]
lat_ich = nc_2.variables['lat'][:]
z_ich = nc_2.variables['depth'][:]
time_ich = nc_2.variables['time'][:]

# --------------------------------------------------------------------------+

fig = plt.figure(figsize = (10,10))
map = Basemap(llcrnrlon = minlon, llcrnrlat = minlat, urcrnrlon = maxlon, urcrnrlat = maxlat, resolution = 'f',  projection = 'merc', lat_0 = minlat, lon_0 = minlon)

Lon_od,Lat_od=map(lon_od,lat_od)
Lon_ich,Lat_ich=map(lon_ich,lat_ich)

plt.text(np.mean(Lon_od[:,0]),np.mean(Lat_od[:,0]),'Lanzamento',fontweight='bold')

for i in range(len(time_od)):
    plt.plot(np.mean(Lon_od[:,i]), np.mean(Lat_od[:,i]), color = 'r', marker = '.', linewidth = 0)
    plt.plot(np.mean(Lon_ich[i,:]), np.mean(Lat_ich[i,:]), color = 'b', marker = '.', linewidth = 0)


plt.text(np.mean(Lon_od[:,-1]),np.mean(Lat_od[:,-1]),'OD',fontweight = 'bold')
plt.text(np.mean(Lon_ich[-1,:]),np.mean(Lat_ich[-1,:]),'Ich',fontweight = 'bold')

# --------------------------------------------------------------------------+ 
   
map.fillcontinents(color = 'grey')
parallels = np.arange(minlat, maxlat, 0.5)
meridians = np.arange(minlon, maxlon, 0.5)
map.drawparallels(parallels, labels = [1,0,0,0], fontsize = 14)
map.drawmeridians(meridians, labels = [0,0,0,1], fontsize = 14)
namefig = 'Lanzamientos.jpg'


plt.show()

# --------------------------------------------------------------------------+

fintime=[]
for t in time_ich:
    fintime.append(initime+datetime.timedelta(t/86400.))

mean_ich = []
mean_od = []

for i in range(0,len(z_ich[:,0])):
    mean_ich.append(np.mean(z_ich[i,:]))
    
for i in range(0,len(z_od[0,:])):
    mean_od.append(np.mean(z_od[:,i]))
    
plt.plot(fintime, mean_od, color = 'r', label = 'OpenDrift')
plt.plot(fintime, mean_ich, color = 'b', label = 'Ihcthyop')
plt.title('Profundidad media vs tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Profundidad (m)')
plt.grid()
plt.show()
