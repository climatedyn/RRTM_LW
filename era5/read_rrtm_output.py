#!env python

import pandas as pd

with open('OUTPUT_RRTM','r') as f:
    lnes = f.readlines()
    indx = lnes.index('\x0c\n')

ds = pd.read_fwf('OUTPUT_RRTM',header=[1,2],nrows=indx-3,widths=[8,13,14,14,14,19],index_col=1).to_xarray()

ds = ds.rename({'index':'level'})
del ds[1]
rname = {}
for var in ds.data_vars:
    rname[var] = var[0].replace(' ','_')
    ds[var].attrs['units'] = var[1]
ds = ds.rename(rname)
outFile = 'rrtm_lw.nc'
ds.to_netcdf('rrtm_lw.nc')
print(outFile)

