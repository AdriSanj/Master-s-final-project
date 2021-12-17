#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: adrian sanjurjo garcia
"""

# Basic imports for executing OpenDrift.
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_ROMS_native
from datetime import datetime, timedelta
import dateutil.parser

# For reading a .txt of initial positions if we want.
import pandas as pd

# Necessary for calculate the time 
import time

start = time.time()

# Initial coordinates if we dont input a .txt file.
#longitude = -9
#latitude = 42

# Radius for uniform dispersion around source [meters]
R = 500.0


# Set number of floats 
N = 1000

# Time period of the simulation

start_time = datetime(2021, 12, 18)  
end_time = datetime(2021, 12, 21)



# Reading of the .txt file

names = ['lon', 'lat', 'dep']
#df = pd.read_csv('all_particles_OD.txt', sep = ' ', names = names)
df = pd.read_csv('all_particles_OD.txt', sep = ' ', names = names)

lon = df['lon']       
lat = df['lat']
z = df['dep']



""" Model initialization """

model = OceanDrift(loglevel = 0)

""" Add readers """
# Ocean data


phys = reader_ROMS_native.Reader('/cesga/NWIberia_mercator_bio_nov2006_his.nc')

# Adding readers
model.add_reader(phys)

object_type = 1 # PIW-1 Person-in-water (PIW), unknown state (mean values)


""" Seed elements """
model.seed_elements(lon = lon,
                lat = lat,
                number = N,
                #radius = R,
                #radius_type = "uniform",
                time = start_time,
                z = z      # comment if dont want depth
                #object_type=object_type
                )

# Para evitar el beaching
#model.set_config('general:coastline_action', 'previous')

model.set_config('drift:advection_scheme', 'runge-kutta')
model.set_config('drift:vertical_advection', True)
model.set_config('drift:horizontal_diffusivity', 10)
#model.set_config('drift:verticaldiffusivity_Sundby1983', 10, -10)

# vertical mixing 
model.set_config('drift:vertical_mixing', True)
model.set_config('vertical_mixing:diffusivitymodel', 'environment')
timestep_vm = 10     # segundos
model.set_config('vertical_mixing:timestep', timestep_vm)

""" Model run """

# para pruebas, timestepdelta 30
print('starting model run')
model.run(end_time = end_time, 
        time_step = timedelta(minutes = 30), 
        time_step_output = timedelta(minutes = 30), 
        outfile = filename,
        export_variables = ["trajectory", 
                            "time", 
                            "status",
                            "age_seconds",
                            "lon", 
                            "lat",
                            "z"]       
        )


print('finished model run')

# Exports the final time in which the program was executed.
end = time.time()
print('time of execution')
print(end-start)

f = open("tiempo.txt", "w")
f.write(str(end-start))
f.close() 
