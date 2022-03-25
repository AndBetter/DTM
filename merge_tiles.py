# code that uses gdal to merge tiles of raster mosaic

import numpy as np
import matplotlib.pyplot as plt
import os, glob
from osgeo import gdal
import numpy as np

#limits of merging
lat_global_min=25     #25
lat_global_max=85     #85
long_global_min=-50    #-50
long_global_max=70

long_step=20

longs=np.array(range(long_global_min,long_global_max+long_step,long_step))


#creates list of files in the entire folder
files_to_mosaic = glob.glob('/home/bettand/Desktop/eos/jeodpp/data/base/Elevation/GLOBAL/FABDEM/VER1-0/Data/GeoTIFF/**/*.tif')
files_to_mosaic


for ii in range(len(longs)-1):
    
    lat_min=lat_global_min
    lat_max=lat_global_max
    long_min=longs[ii]
    long_max=longs[ii+1]
    
    print(ii)
    print(f'long_min={long_min}')
    print(f'long_max={long_max}')
    print('working on it...')
    
    files_to_mosaic_selected=[]
    array_latlong=np.array([[0,0],[0,0]])
    #creates a new list with just the tiles falling into the lat-long limits
    for i in range(len(files_to_mosaic)):
        lat_tile=np.int(files_to_mosaic[i][104:106])
        long_tile=np.int(files_to_mosaic[i][107:110])
        
        #add the sign based on direction
        if files_to_mosaic[i][103:104] == 'S':
            lat_tile=-lat_tile
        if files_to_mosaic[i][106:107] == 'W':
            long_tile=-long_tile
        
        if lat_tile >= lat_min and lat_tile < lat_max and long_tile >= long_min and long_tile < long_max:
           files_to_mosaic_selected.append(files_to_mosaic[i]) 
           array_latlong=np.vstack((array_latlong, np.array([lat_tile,long_tile])))
        
        
    
    #creates single string from list of string names
    files_string = " ".join(files_to_mosaic_selected)
    #print(files_string)
    
    #merge
    command = f"gdal_merge.py -co BIGTIFF=YES -co COMPRESS=LZW  -co PREDICTOR=3  -o /eos/jeodpp/home/users/bettand/Data/europe_stripes_{ii}.tif -of gtiff " + files_string
    print(os.popen(command).read())

