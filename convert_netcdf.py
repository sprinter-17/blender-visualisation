import netCDF4 as nc
import numpy as np

ds = nc.Dataset("data/net_dt01_proc000.nc", "r", format='NETCDF4')


sample_count = len(ds.dimensions['No_of_samples'])
bead_count = len(ds.dimensions['NBeads'])
data = ds['configuration']

for sample in range(0,sample_count):
    for bead in range(0, bead_count):
        location = data[bead,:,sample,0]
        for dim in range(0, 3):
            print(location[dim], end=" ")
    print()

ds.close()
