# Master-s-final-project

This are the codes used for my master thesis.

The files larvalfish_ieo.py and oceandrift_ieo.py must be copypasted to the folder "models" in OpenDrift so they can be used. 
Both of them are recursive, so you cannot use oceandrift_ieo.py by default like the oceandrift.py file included in OpenDrift, 
so its only for use the larvalfish_ieo.py. This file is a modification of the original larvalfish.py that models the growth
and buyoyancy of the cod, which in this case is for the growth of the sardine, describing the egg stage and the two larval
stages of this one (Yolk-Sac and Feeding Larvae), but discarding the case of the larval movement, only using the movement of the sea water obtained by the
netcdf files. 

For the use of this class, in an initial script of OpenDrift, must write the model "larvalfish_ieo" and choose the variables
you want to export for the representation. The file oceandrift_ieo.py is like the original oceandrift.py but with a few 
modifications, including a new function that obtains the first parameters of temperature and salinity of the ROMS ecological
model (doesn't work with a ROMS without a biological part) in the first timestep, necessary for the egg development, and a few
new if conditionals for the use of this function. 
