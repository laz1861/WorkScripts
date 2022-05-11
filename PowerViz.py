# -*- coding: utf-8 -*-
#Import the power data

#from shapely.geometry import Polygon
from shapely import wkt
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

pow_data = pd.read_csv('Output8.csv', parse_dates=True)
pow_data.set_index('name', inplace=True)
pow_data=pow_data.transpose()

mpl.rcParams['figure.subplot.left']=0
mpl.rcParams['figure.subplot.right']=1
mpl.rcParams['figure.subplot.bottom']=0
mpl.rcParams['figure.subplot.top']=1

#plot_data = gpd.geoseries(pow_data)


p = gpd.GeoDataFrame(pow_data[:5][:])
p['geometry']= p['geometry'].apply(wkt.loads)

#for ind in range(1,p.shape[1]-1):
for ind in range(1,97):
    p.iloc[:,ind]=p.iloc[:,ind].astype(float)
    p.plot(column=p.columns[ind], figsize=(19.20, 13.30),cmap='inferno', edgecolor="white", linewidth=10, vmin=0.45, vmax=1)
    plt.annotate(text = p.columns[ind], xy=(600,1260),color='black',size=40)
    plt.annotate(text = str(pow_data.iloc[5,ind]) + "MW", xy=(600,1200),color='black',size=40)
    #p.plot(figsize=(48.85, 33.84),cmap='Reds', edgecolor="white", linewidth=10)
    plt.margins(0)
    plt.axis([0, 1920, 0, 1330])
    plt.axis('off')
    plt.grid(True)
    plt.savefig('feeder' + str(ind).zfill(7) + '.png', format='png', dpi=100, pad_inches=0, transparent=True)
    plt.close()
    
