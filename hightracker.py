### import the things
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cmocean
import os
import math
import seaborn as sns

data_path  = '/media/peter/Storage/data/'

def low_pass_weights(window, cutoff):
    """Calculate weights for a low pass Lanczos filter.

    Args:

    window: int
        The length of the filter window.

    cutoff: float
        The cutoff frequency in inverse time steps.

    """
    order = ((window - 1) // 2 ) + 1
    nwts = 2 * order + 1
    w = np.zeros([nwts])
    n = nwts // 2
    w[n] = 2 * cutoff
    k = np.arange(1., n)
    sigma = np.sin(np.pi * k / n) * n / (np.pi * k)
    firstfactor = np.sin(2. * np.pi * cutoff * k) / (np.pi * k)
    w[n-1:0:-1] = firstfactor * sigma
    w[n+1:-1] = firstfactor * sigma
    return w[1:-1]

wgts = low_pass_weights(41, 1/10)
weight = xr.DataArray(list(wgts), dims=['window'])


x =xr.open_dataset(str(data_path)+'NOAA/z_day_noaa_20thC-reanalysis_2000.nc')
x = x.rename({'level':'plev'})
x = x.rename({'hgt':'zg'})
#x = x.rename({'longitude':'lon'})
#x = x.rename({'latitude':'lat'})
x = x.sel(plev=500.0)
x = x.sel(lat=slice(-85,-15))
x = x.assign_coords(lon=(((x.lon + 180) % 360) - 180))
x = x.sortby(x.lon)
x = x.sel(lon=slice(-50,32))
x['zg'] = x.zg.rolling(time=41, center=True).construct('window').dot(weight)
x = x.where(x.time==x.time[20:-21])


x['maxi'] = x.zg.copy()
for i in range(len(x.time)):
    x.maxi[i] = x.zg[i].where((x.zg[i]==np.max(x.zg[i])))

east=[]
west=[]
north=[]
south=[]
for i in range(len(x.time)):
    ids =  np.argwhere(~np.isnan(x.maxi[i].values))
    latsid = [item[0] for item in ids]
    lonsid = [item[1] for item in ids]
    west.append(x.lon.values[np.min(lonsid)])
    east.append(x.lon.values[np.max(lonsid)])
    north.append(x.lat.values[np.min(latsid)])
    south.append(x.lat.values[np.max(latsid)])

results = pd.DataFrame({'time':x.time.values,'North':north,'South':south,'East':east,'West':west})

results.to_csv('../HIGH_OUT/high_out.csv')
x.to_zarr('../HIGH_OUT/high_out.zarr')
