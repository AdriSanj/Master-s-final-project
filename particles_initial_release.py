import numpy as np
import pyproj
import matplotlib.pyplot as plt
radius_type = 'uniform'


lon = -9
lat = 42
z = 10       # Positive for Ichthyop, negative for OpenDrift    
radius = 500
number = 1000

separation = 'comma'

# --------------------------------------------------------------------------+

lon = lon*np.ones(number)
lat = lat*np.ones(number)

# --------------------------------------------------------------------------+

np.random.seed(0)       # For having the same distribution for all runs

geod = pyproj.Geod(ellps='WGS84')
ones = np.ones(np.sum(number))
if radius_type == 'gaussian':
	x = np.random.randn(np.sum(number))*radius
	y = np.random.randn(np.sum(number))*radius
	az = np.degrees(np.arctan2(x, y))
	dist = np.sqrt(x*x+y*y)
elif radius_type == 'uniform':
	az = np.random.randn(np.sum(number))*360
	dist = np.sqrt(np.random.uniform(0, 1, np.sum(number)))*radius
lon, lat, az = geod.fwd(lon, lat, az, dist, radians = False)

# --------------------------------------------------------------------------+

depth=z*np.ones(len(lon))

namefile='particles.txt'

if separation == 'point':
	DATA = np.column_stack((lon, lat, depth))
elif separation == 'comma':
	Lon = []
	Lat = []
	Depth = []
	for i in range(len(lon)):
		Lon.append(str(lon[i]).replace('.', ','))
		Lat.append(str(lat[i]).replace('.', ','))
		Depth.append(str(depth[i]).replace('.', ','))
	DATA = np.column_stack((Lon, Lat, Depth))

with open(namefile ,'w') as f_handle:
        np.savetxt(f_handle, DATA, delimiter=" ", fmt="%-s")

# --------------------------------------------------------------------------+

plt.plot(lon,lat,'o')
plt.show()
