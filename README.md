# RRTM_LW
Starting from [`RRTM_LW`](http://rtweb.aer.com/rrtm_frame.html), add python scripts to run offline longwave radiative transfer calculations with custom temperature and moisture profiles.

This might with time become more general. To be used with caution as many assumptions are hard coded into the input file setup.

Workflow:
```bash
# we assume rrtm_lw has been compiled as per user instructions.
# define location of executable
rrtm=../rrtm_lw.x
# move into work directory (is called era5 because my input profiles come from ERA5)
cd era5
# the custom profiles for temperature and specific humidity are to be placed into the file tq_profile.nc
# create input file for RRTM_LW
python produce_rrtm_input.py 
# run RRTM_LW
${rrtm}        
# parse output and create netcdf file containing RRTM_LW output
python read_rrtm_output.py
```
