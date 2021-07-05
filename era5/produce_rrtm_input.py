#!env python
import numpy as np
import xarray as xr

# record 1.2
IATM   = 1
IXSECT = 0
ISCAT  = 0
NUMANGS= 0
IOUT   = 0
ICLD   = 0

# record 1.4
TBOUND = -1.0
IEMIS  = 0
IREFLECT=0
SEMISS = 1.0

# record 3.1 (applicable if IATM=1)
MODEL   = 0
IBMAX   = 0 # use RRTM internal layers for LBL calculations
NOPRNT  = 1  
NMOL    = 2 # to be defined
IPUNCH  = 1
MUNITS  = 1
RE      = 6378.39
#CO2MX   = 330  # replaced with VMOL(2)
#REF_LAT = 15.0 # not used somehow

## data
def RefineVertical(ds,istart):
    # increase vertical resolution
    print('Refining from level {0}'.format(ds.level.values[istart]))
    midlevs = (ds.level.values[istart:]+ds.level.values[istart-1:-1])*0.5
    all_levs = np.sort(list(midlevs)+list(ds.level.values))[::-1]
    ds = ds.interp(level=all_levs)
    #print(ds.level.values)
    return ds

era = xr.open_dataset('tq_profile.nc')#.sel(level=slice(200,1000))
era = era.sel(level=np.sort(era.level)[::-1])
#era = RefineVertical(era,20)
#era = RefineVertical(era,40)
t = era.t.values
q = era.q.values
p = era.level.values

H = 6.5
PS= 1013.15
# record 3.2
HBOUND  = 0.0 # to be defined 
HTOA    = -H*np.log(np.min(p)/PS)    # to be defined

# record 3.3A
AVTRAT = 0.0
TDIFF1 = 0.0
TDIFF2 = 0.0
ALTD1  = 0.0
ALTD2  = 0.0


## record 3.3B
#PBOUND  = HBOUND #1013.15
#PTOA    = HTOA   #PBOUND*np.exp(-HTOA/H)
#PBND    = np.logspace(np.log10(PBOUND),np.log10(PTOA),abs(IBMAX)+2)[1:-1] #to be defined - IBMAX pressure boundaries

# record 3.4
IMMAX   =  len(p)
HMOD    = 'custom profile'

# record 3.5

PBOUND  = PS*np.exp(-HBOUND/H)
PTOA    = PS*np.exp(-HTOA/H)
#PM      = np.logspace(np.log10(PTOA),np.log10(PBOUND),abs(IMMAX)+2)[1:-1][::-1] #to be defined # to be defined - these are input profile pressures
#TM      = 303-7.5*ZM # to be defined
PM      = p
TM      = t
ZM      = -H*np.log(PM/PBOUND)
JCHARP  = 'A' 
JCHART  = 'A'
JCHAR   = ['C','A'] # H2O in g/kg, CO2 in ppmv
#JCHAR   = ['1']*NMOL # predefined model atmosphere

# record 3.6
#VMOL    = [[,330]]*abs(IMMAX) # H2O,CO2to be defined
VMOL    = [[q[k]*1e3,330] for k in range(len(p))]



file = open('INPUT_RRTM','w')
file.write("$ python generated input file\n")

file.write('{0:50}{1:20}{2:13}{3:2}{4:5}{5:5}\n'.format(IATM,IXSECT,ISCAT,NUMANGS,IOUT,ICLD))
file.write('{0:10.3E}{1:2}{2:3}{3:5.3E}\n'.format(TBOUND,IEMIS,IREFLECT,SEMISS))
file.write('{0:5}{1:10}{2:10}{3:5}{4:5}{5:5}{6:10.3f}\n'.format(MODEL,IBMAX,NOPRNT,NMOL,IPUNCH,MUNITS,RE))
## record 3.2
file.write('{0:10.3f}{1:10.3f}\n'.format(HBOUND,HTOA))
## record 3.3A
file.write('{0:10.3f}{1:10.3f}{2:10.3f}{3:10.3f}{4:10.3f}\n'.format(AVTRAT,TDIFF1,TDIFF2,ALTD1,ALTD2))
## record 3.3B
#pbnd_list = ['{:10.3f}'.format(p) for p in PBND]
## format is 8F10.3, so need newline after 8 entries
#n8 = len(pbnd_list) & 8
#for n in range(n8):
#    pbnd_list[n*n8-1] += '\n'
#file.write(''.join(pbnd_list))
## record 3.4
file.write('{0:5}{1}\n'.format(IMMAX,HMOD))
for k in range(abs(IMMAX)):
    lne = '{0:10.3E}{1:10.3E}{2:10.3E}     {3:1}{4:1}   '.format(ZM[k],PM[k],TM[k],JCHARP,JCHART)+''.join(JCHAR)+'\n'
    file.write(lne)
    vmol_list = ['{:10.3E}'.format(VMOL[k][l]) for l in range(NMOL)]
    file.write(''.join(vmol_list)+'\n')

file.write('%')
file.close()
