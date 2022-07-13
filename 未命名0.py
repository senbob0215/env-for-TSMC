# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:19:22 2022

@author: 藍鼎鈞
"""

import pygrib as pg
import numpy as np
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
from matplotlib.colors import BoundaryNorm
import datetime
import glob

#%%
file = glob.glob(r'C:\Users\landinjyun\Downloads\M-A0064-*.grb2')
rh_mean = []; ts = []
for j in range(len(file)):
    grbs = pg.open(file[j])
    #for grb in grbs:  
    	#print(grb)
    	#print(grb.keys())
        
    #%%
    data = grbs.select(name='2 metre relative humidity')[0]
    rh = data.values
    time = data.validDate
    time = time - datetime.timedelta(hours=6)
    tt = time.strftime('%Y/%m/%d %HUTC')
    ts.append(time.strftime('%m/%d\n%HUTC'))
    lat, lon = data.latlons()
    
    data = grbs.select(name='2 metre temperature')[0]
    temp = data.values
    
    #%%
    F15Alon, F15Alat = 120.6081972931729, 24.211712178532558
    index = np.where((abs(lon-F15Alon) < 0.05) & (abs(lat-F15Alat) < 0.05))
    rh_mean.append(rh[index[0], index[1]].mean())
    
    #%%
    
    # projection
    fig = plt.figure(figsize=(8, 8), dpi=100)
    
    pro_css = ccrs.PlateCarree() #Set map projection
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=120))
    
    #--------------------------------------------------------------------------
    # SST
    cmap=plt.cm.get_cmap('jet')
    norm = BoundaryNorm(np.arange(50,100,5), ncolors=cmap.N, clip=True)
    sst_contourf = ax.pcolormesh(lon, lat, rh, 
                                 cmap=cmap, 
                                 norm=norm, 
                                 transform=pro_css)
    
    cbar_ax = fig.add_axes([0.155, 0.07, 0.7, 0.015])
    def resize_colobar(event):
        plt.draw()
    
        posn = ax.get_position()
        cbar_ax.set_position([posn.x0 + posn.width, posn.y0,
                              0.04, posn.height])
    fig.canvas.mpl_connect('resize_event', resize_colobar)
    
    cbar = plt.colorbar(sst_contourf, 
                        cax=cbar_ax, 
                        orientation='horizontal', 
                        extend='max',
                        ticks = np.arange(50, 100, 10))
    
    cbar.set_label('Relative Humidity(%)', rotation=0, size=14) #Set colorbar label
    #--------------------------------------------------------------------------
    ax.scatter(120.6081972931729, 24.211712178532558, color='r', edgecolors='k', transform=pro_css)
    ax.scatter(120.61561453796702, 24.21213061888599, color='r', edgecolors='k', transform=pro_css)
     
    #--------------------------------------------------------------------------
    # coastline
    #ax.set_extent([119.5, 121.5, 24, 25], crs=pro_css) #Set figure Domain
    ax.set_extent([119, 124, 21.5, 26], crs=pro_css) #Set figure Domain
    ax.coastlines(resolution='50m', zorder=6) #Draw Coastline & set resolution
    #ax.add_feature(cartopy.feature.LAND, color='#FFE4CA', zorder=5) #Add Land
    #ax.add_feature(cartopy.feature.OCEAN, color='#9D9D9D', zorder=1) #Add Ocean
    
    ax.set_xticks(np.arange(119, 124.5, 0.5), crs=ccrs.PlateCarree()) #Set longitude ticks [initial, end, step]
    ax.set_yticks(np.arange(21.5, 26.5, 0.5), crs=ccrs.PlateCarree()) #Set latitude ticks [initial, end, step]
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                           degree_symbol='',
                                           dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                          degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
    
    ax.tick_params(axis='both',labelsize=14,direction='out') #Set longitude & latitude ticks size
    ax.tick_params(axis = 'both', 
                   which = 'major', 
                   labelsize = 11.5, 
                   direction = 'out', 
                   length = 8, 
                   width = 1,
                   pad = 5)
    ax.tick_params(axis = 'both', 
                   which = 'minor', 
                   labelsize = 24, 
                   direction = 'out', 
                   length = 5, 
                   width = 0.8,
                   pad = 5)
    
    
    # Set title
    ax.grid(ls='--')
    ax.set_title(f'WRF Model Relative Humidity {tt}', size=20, pad=10) #Set figure title
    
#%%
plt.figure()
plt.plot(np.arange(len(file)), rh_mean, '-o')
plt.xticks(np.arange(len(file)), ts)
plt.xlabel('Forcast Time')
plt.ylabel('RH(%)')
plt.yticks(np.arange(50,100,5))
plt.grid(ls='--')
plt.title('F15A Relative Humidity')

#%%
