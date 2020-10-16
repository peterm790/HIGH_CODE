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

rsults = pd.read_csv('../HIGH_OUT/high_out.csv')
x = xr.open_zarr('../HIGH_OUT/high_out.zarr').compute()


for i in range(len(x.time)):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.contourf(x.lon,x.lat,x.zg[i],cmap = cmocean.cm.phase, levels = 100, transform = ccrs.PlateCarree(),alpha=1)
    #ax.axhline(y=north[i],color='r', linestyle='dashed')
    ax.axhline(y=south[i],color='r', linestyle='dashed')
    ax.axvline(x=east[i],color='r', linestyle='dashed')
    #ax.axvline(x=west[i],color='r', linestyle='dashed')
    plt.title('South Atlantic High Pressure \n'+str(x.zg[i].time.values))
    ax.gridlines(linewidth=0.5, color='gray', alpha=0.5)
    #ax.set_extent([-40, 50, 10, -45], ccrs.PlateCarree())
    plt.savefig('../HIGH_OUT/demonstration/'+str(i)+'_togif.png')
    plt.close()



    #   cat `ls -v *togif.png` | ffmpeg -framerate 6 -f image2pipe -i - output.mp4
