#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Basic imports for executing OpenDrift.
from opendrift.models.oceandrift import OceanDrift
from opendrift.models.larvalfish_ieo import LarvalFish_sardine
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_ROMS_native
from datetime import datetime, timedelta
import dateutil.parser

# For reading a .txt of initial positions if we want.
import pandas as pd

# Necessary for calculate the time 
import time


start = time.time()


filename = '/home/adrisanj/informe_practicas/outputs_opendrift/OD_eco_sim_NOBEACHING.nc'

""" Set seeding conditions """


    
# Set number of floats 
N = 52746

# Date

start_time = datetime(2006, 11, 8, 20)  
end_time = datetime(2006, 12, 1)  


names = ['lon', 'lat', 'dep']
df = pd.read_csv('all_particles_OD.txt', sep = ' ', names = names)

lon = df['lon']       
lat = df['lat']
z = -1*df['dep']	# Ponerle un -1 en caso de usar el fichero de all particles


""" Model initialization """
model = LarvalFish_sardine(loglevel = 0)

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
                z = z      # comment if dont want profundity
                #object_type=object_type
                )

# Para evitar el beaching
model.set_config('general:coastline_action', 'previous')

model.set_config('drift:advection_scheme', 'runge-kutta')
model.set_config('drift:vertical_advection', True)
model.set_config('drift:horizontal_diffusivity', 10)

# vertical mixing 
model.set_config('drift:vertical_mixing', True)
model.set_config('vertical_mixing:diffusivitymodel', 'environment')
timestep_vm = 10     # segundos
model.set_config('vertical_mixing:timestep', timestep_vm)

""" Model run """

print('starting model run')
model.run(end_time = end_time, 
        time_step = timedelta(minutes = 10), 
        time_step_output = timedelta(minutes = 10), 
        outfile = filename,
        export_variables = ["trajectory", 
                            "time", 
                            "status",
                            "age_seconds",
                            "lon", 
                            "lat",
                            "z",
                            "hatched",     # Borrar en el caso de no usar larvalfish
                            "stage_fraction",
                            "length",
                            "egg_dens",
                            "dens_diff",
                            "zoopl"]       
        )


print('finished model run')

end = time.time()
print('time of execution')
print(end-start)

f = open("tiempo.txt", "w")
f.write(str(end-start))
f.close() 
