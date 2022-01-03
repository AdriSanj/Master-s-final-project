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
run = 2
particle_size = 0.1

if run == 1:
    minlon = -9.4
    maxlon = -8.6
    minlat = 41.4
    maxlat = 42.2
    initime = datetime.datetime(2009,1,1)
elif run == 2:
    # For all particles run
    minlon = -13
    maxlon = -1
    minlat = 37
    maxlat = 46.5
    initime = datetime.datetime(2006,1,1)

# --------------------------------------------------------------------------+

# Dont touch unless specified by the archive
#initime = datetime.datetime(1900,1,1)		# For Ichthyop comparisions
#initime = datetime.datetime(2013,5,1)
#initime = datetime.datetime(2009,1,1)   # Example
#initime = datetime.datetime(2006,1,1)    # Eco
# --------------------------------------------------------------------------+

archive = '/home/adrisanj/informe_practicas/outputs_ichthyop/roms3d_ichthyop-run202112311950.nc'

nc = netCDF4.Dataset(archive)
lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]
z = nc.variables['depth'][:]
time = nc.variables['time'][:]



# --------------------------------------------------------------------------+

fig = plt.figure(figsize = (10,10))
map = Basemap(llcrnrlon = minlon, llcrnrlat = minlat, urcrnrlon = maxlon, urcrnrlat = maxlat, resolution = 'f',  projection = 'merc', lat_0 = minlat, lon_0 = minlon)

Lon,Lat=map(lon,lat)

plt.plot(Lon, Lat, color = 'r', marker = '.', linewidth = 0, markersize = particle_size)
if run == 1:
    plt.text(np.mean(Lon[0,:]),np.mean(Lat[0,:]),'Lanzamento',fontweight='bold')
	
# --------------------------------------------------------------------------+ 
   
map.fillcontinents(color = 'grey')
parallels = np.arange(minlat, maxlat, 0.5)
meridians = np.arange(minlon, maxlon, 0.5)
if run == 1:
    map.drawparallels(parallels, labels = [1,0,0,0], fontsize = 14)
    map.drawmeridians(meridians, labels = [0,0,0,1], fontsize = 14)
elif run == 2:
    map.drawparallels(parallels, labels = [1,0,0,0], fontsize = 5)
    map.drawmeridians(meridians, labels = [0,0,0,1], fontsize = 5)
namefig = 'Lanzamientos.jpg'


plt.show()

if run == 1:
    fintime=[]
    for t in time:
        fintime.append(initime+datetime.timedelta(t/86400.))

    for i in range(0,10):
        plt.plot(fintime, z[:,i])
        plt.title('Profundidad vs tiempo')
        plt.xlabel('Tiempo')
        plt.ylabel('Profundidad (m)')
        plt.grid()
    plt.show()
elif run == 2:
# First run of the ecological model
    fig = plt.figure(figsize = (10,10))
    map = Basemap(llcrnrlon = minlon, llcrnrlat = minlat, urcrnrlon = maxlon, urcrnrlat = maxlat, resolution = 'f',  projection = 'merc', lat_0 = minlat, lon_0 = minlon)
    plt.plot(Lon[0,:], Lat[0,:], color = 'r', marker = '.', linewidth = 0, markersize = particle_size)
    map.fillcontinents(color = 'grey')
    parallels = np.arange(minlat, maxlat, 0.5)
    meridians = np.arange(minlon, maxlon, 0.5)
    map.drawparallels(parallels, labels = [1,0,0,0], fontsize = 5)
    map.drawmeridians(meridians, labels = [0,0,0,1], fontsize = 5)
    plt.show()
