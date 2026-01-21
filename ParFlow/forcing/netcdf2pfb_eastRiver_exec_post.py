#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 14:15:14 2021

@author: jpdf
"""

import netCDF4
import numpy as np
import glob
import pandas as pd
import xesmf as xe
import geopandas as gpd
import struct
from datetime import datetime
import multiprocessing as mp
import shapefile

def main():
    varDict = setVars()
    print('Variables set')
    print(varDict['climateDir'])

    # Get all .nc4 files in climate directory and sort them, print the first 2
    # to make sure you have the correct files
    climateFiles = glob.glob(varDict['climateDir']+'*.nc4')
    climateFiles.sort()
    climateFiles = climateFiles[0:2]
    
    # It seems that more than ~30K files don't work for *some reason*, so break it up into chunks of about 25K
    # climateFiles = climateFiles[8:]
    # climateFiles = climateFiles[25000:]
    print(climateFiles[:3],climateFiles[-3:])

    # Call the function to define the regridding process and return grid specification
    regridVars = defineRegridders_correct(climateFiles[0],varDict['climateDir'],varDict['outDir'],
                                  varDict['parflowDir'],varDict['pxy'])
    print('Regridders built')

    # Define the variables for each file's regridding; note that these weights 
    # are calling conservative, but if you changed the regridders you coudl also
    # do bilinear interpolation
    regridStructure = [{'file':f,'outDir':varDict['outDir'],'climVars':varDict['climVars'],
                        'parflowVars':varDict['parflowVars'],'pxy':varDict['pxy'],'pfbPrefix':varDict['pfbPrefix'],
                        'gridIn':regridVars['gridIn'],'gridOut':regridVars['gridOut'],
                        'weights':regridVars['conservative']} for f in climateFiles]

    # Create a multiprocess pool and call it for each individual forcing file
    print('Starting regridding')
    pool = mp.Pool(processes=16)                         # Create a multiprocessing Pool
    pool.map(regridFile, regridStructure)
    print('Done regridding')

    return 
    
def setVars():
    
    # Put in important path data here
    climateDir = '/pscratch/sd/p/pjdf/Projects/EastRiver/runsParflow/forcingData/nldas_wy2015-2021/'   
    outDir = '/pscratch/sd/p/pjdf/Projects/EastRiver/runsParflow/nldas/test/'
    parflowDir = '/global/homes/p/pjdf/Data/EastRiver/GIS/'
    
    # Define the parflow grid variables
    pnx,pny = 170,150    ## Note that it looks to be (170,150) for conservative regridding, (150,170) for bilinear . . ?.
    pnn = pnx*pny
    pdx,pdy = 100.,100.
    px,py = 321547.804, 4322463. 
    pxy = {'pnx':pnx,'pny':pny,'pnn':pnn,'pdx':pdx,'pdy':pdy,'px':px,'py':py}
    
    # Define the variables in the .nc4 files and the associated parflow variable
    climVars = ['Tair','Qair','PSurf','Wind_E','Wind_N','LWdown','SWdown','Rainf']
    parflowVars = ['Temp','SPFH','Press','UGRD','VGRD','DLWR','DSWR','APCP']
    
    # Define the 0 timestep and prefix that will be present in the .nc4 files 
    prefix = 'NLDAS'
    t0 = datetime(2014,10,1)
    
    pfbPrefix = {'prefix':prefix,'t0':t0}
    
    return {'climateDir':climateDir,'outDir':outDir,'parflowDir':parflowDir,'pxy':pxy,
            'climVars':climVars,'parflowVars':parflowVars,'pfbPrefix':pfbPrefix}


def regridFile(varIn):
    # This is the function called in the multiprocessing pool
    
    # First, get the named .nc4 file and read it
    climDataset = netCDF4.Dataset(varIn['file'],'r')
    
    # Calculate the ParFlow hour based on the difference betweeen the date
    # in the file and the t0 time and change it to an integer
    diffTime = datetime.strptime(varIn['file'][-28:-17],'%Y%m%d.%H') - varIn['pfbPrefix']['t0']
    i = int(diffTime.days*24 + diffTime.seconds//3600)
    
    # Define the regrid function for this file
    # Note that this needs to change if doing bilinear rather than conservative
    regrid = xe.Regridder(varIn['gridIn'],varIn['gridOut'],'conservative',reuse_weights=True,filename=varIn['weights'])

    # Call a loop to regrid each variable separately and write a parflow file 
    # with the output 
    for c,p in zip(varIn['climVars'],varIn['parflowVars']):
        climData = np.squeeze(climDataset.variables[c][:])
        # Need to convert units for precip from kg/m^2 (mm/hr) to mm/s
        if c == 'Rainf': climData = climData/3600 
            
        regridData = regrid(np.array(climData))
        
        fileName = varIn['outDir'] + varIn['pfbPrefix']['prefix'] + '.' + p + '.' + str(i).zfill(6) + '.pfb'
        
        write_pfb_1D(regridData,fileName,varIn['pxy']['px'],varIn['pxy']['py'],
                     varIn['pxy']['pnx'],varIn['pxy']['pny'],varIn['pxy']['pdx'],
                     varIn['pxy']['pdy'])

    # Set variables to None to avoid memory leaks
    climDataset,diffTime,regrid,climData,regridData = None, None, None, None, None

    return



def defineRegridders_correct(climateFile,climateDir,outDir,parflowDir,pxy):
    # First, set up the regridder from climate grid to parflow grid

    # Load the NLDAS data and get the latitude, longitude, and shape of the array
    climDataset = netCDF4.Dataset(climateFile,'r')
    climLats = climDataset.variables['lat'][:]  # extract/copy the data
    climLons = climDataset.variables['lon'][:]
    climVar = np.squeeze(climDataset.variables['Tair'][:])

    # Set up 2D array of lat and lon values, calculate pixel corners . . .
    # #Put them into 2D arrays of the correct shapes, and create 
    # # array of "pixel corners" for conservative regridding
    # # Note that the 0.125 is because the NLDAS dataset is 0.25 degree
    climLats = np.array(np.transpose(np.tile(climLats,[np.shape(climVar)[1],1])))
    climLats_b = climLats -(0.125/2)
    climLats_b = np.concatenate([climLats_b,np.array(climLats_b[-1,:]+0.125)[None,:]])
    climLats_b = np.concatenate([climLats_b,np.array(climLats_b[:,-1])[:,None]],axis=1)
    climLons = np.array(np.tile(climLons,(np.shape(climVar)[0],1)))
    climLons_b = climLons -(0.125/2)
    climLons_b = np.concatenate([climLons_b,np.array(climLons_b[-1,:])[None,:]])
    climLons_b = np.concatenate([climLons_b,np.array(climLons_b[:,-1]+0.125)[:,None]],axis=1)


    ### Now do the same for the parflow file
    # First, load the lat and lon values
    # need to build .csv of raster pixel centers and 
    # shapefile that represents each pixel in a multipolygon
    parflowCenters = pd.read_csv(parflowDir + 'demCenters_wgs84.csv')
    parflowGrid = shapefile.Reader(parflowDir + 'demSquares_rectExtent_wgs84.shp')

    # Get just the features from parFlow Grid; each rectange has 5 vertices, with
    # s[0] = s[4], and the numbering starts in th lower left and proceeds clockwise
    # s[0] = [lon0,lat0], so use s[n][0] to get the longitude for node n, and s[n][1] the latitude
    s = parflowGrid.shapes()

    # Reshape the .csv of parflow grid center lats to be the shape of the grid, [pny,pnx]
    parflowLats = np.reshape(parflowCenters['lat'].values,[pxy['pny'],-1])
    
    # Get the upper left corner of each feature to start creating a list of the latitudes of the 
    # corners of all the features
    parflowLats_b = [s[i].points[1][1] for i in range(pxy['pnn'])]

    # Reshape that into the shape of the grid [pny, pnx]
    parflowLats_b = np.reshape(parflowLats_b,[pxy['pny'],-1])

    # Need to add a row on the bottom to get the bottom latitudes,
    # grab [0][1] since it starts counting in the lower left corner
    parflowLats_bottom = [s[i].points[0][1] for i in range(pxy['pnn']-pxy['pnx'],pxy['pnn'])]
    parflowLats_bottom = np.reshape(np.array(parflowLats_bottom),[1,pxy['pnx']])
    parflowLats_b = np.concatenate([parflowLats_b,parflowLats_bottom])
    
    # Then need to add the final right row to the eastmost latitudes
    # Grab [2][1] to get the upper right corner of each feature
    parflowLats_right = [s[i].points[2][1] for i in range(pxy['pnx']-1,pxy['pnn'],pxy['pnx'])]
    # [3][1] is the bottom right corner of the bottom right feature
    parflowLats_right.append(s[pxy['pnn']-1].points[3][1])

    # Then put them all together into a single array
    parflowLats_right = np.reshape(np.array(parflowLats_right),[pxy['pny']+1,1])
    parflowLats_b = np.concatenate([parflowLats_b,parflowLats_right],axis=1)



    # Do exactly the same, but for longitudes, which are held in [n][0] rather than
    # [n][1] of each feature 
    parflowLons = np.reshape(parflowCenters['lon'].values,[pxy['pny'],-1])   
    parflowLons_b = [s[i].points[1][0] for i in range(pxy['pnn'])]
    parflowLons_b = np.reshape(parflowLons_b,[pxy['pny'],-1])
    parflowLons_bottom = [s[i].points[0][0] for i in range(pxy['pnn']-pxy['pnx'],pxy['pnn'])]
    parflowLons_right = [s[i].points[2][0] for i in range(pxy['pnx']-1,pxy['pnn'],pxy['pnx'])]
    parflowLons_right.append(s[pxy['pnn']-1].points[3][0])
    parflowLons_bottom = np.reshape(np.array(parflowLons_bottom),[1,pxy['pnx']])
    parflowLons_b = np.concatenate([parflowLons_b,parflowLons_bottom])
    parflowLons_right = np.reshape(np.array(parflowLons_right),[pxy['pny']+1,1])
    parflowLons_b = np.concatenate([parflowLons_b,parflowLons_right],axis=1)

    
    #Flip upside down to match the usual Parflow setup, starting in the bottom left corner
    parflowLons,parflowLats = np.flipud(parflowLons),np.flipud(parflowLats)
    parflowLons_b,parflowLats_b = np.flipud(parflowLons_b),np.flipud(parflowLats_b)

    
    # Create a regridder between the two
    gridIn = {'lat':climLats, 'lon':climLons, 'lat_b':climLats_b, 'lon_b':climLons_b}
    gridOut = {'lat':parflowLats,'lon':parflowLons, 'lat_b':parflowLats_b,'lon_b':parflowLons_b}

    # bilinearRegridder = xe.Regridder(gridIn, gridOut, "bilinear",filename=outDir + 'regridWeights_bilinear.nc')
    conservativeRegridder = xe.Regridder(gridIn, gridOut, "conservative",filename=outDir + 'regridWeights_conservative.nc')

    return {'bilinear':outDir + 'regridWeights_bilinear.nc','conservative':outDir + 'regridWeights_conservative.nc',
            'gridIn':gridIn,'gridOut':gridOut}




def write_pfb_1D(data,testFile,px,py,pnx,pny,pdx,pdy):
    # Short script to write .pfb files; should be replaced with newer 
    # parflowio code in the future
    fout = open(testFile, 'wb')
    
    fout.write(struct.pack('>3d', px,py,0))
    fout.write(struct.pack('>3i', pnx,pny,1))
    fout.write(struct.pack('>3d', pdx,pdy,1))
    fout.write(struct.pack('>i',1))
    
    fout.write(struct.pack('>3i',0,0,0))
    fout.write(struct.pack('>3i',pnx,pny,1))
    fout.write(struct.pack('>3i',1,1,1))
    for j in range(pny):
        for k in range(pnx):
            fout.write(struct.pack('>d',data[j,k]))
    
    fout.close()
    fout = None
    
    return

if __name__ == '__main__':
    #mp.set_start_method('spawn')
    
    main()
