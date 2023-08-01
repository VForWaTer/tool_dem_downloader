import os
import requests
import tarfile
import shutil
import glob
import sys
from datetime import datetime as dt
from pprint import pprint
import time

from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

#Function to flatten
def flatt(parentDir,currentDir): # Credit - https://gist.github.com/oatkiller/4429244
            # get all the files in the current dir
            files = os.listdir(currentDir)
            
            for file in files:
                # get the path of the file relative to the dir its in
                # so "./file" or on successive runs: "./dir/file"
                joinedFile = os.path.join(currentDir,file)
                
                if os.path.isdir(joinedFile):
                    # run the dir function on dirs
                    flatt(parentDir,joinedFile)
                else: # its not a dir, its a file,
                    # dont move files in the parent dir into the parent dir =p
                    if parentDir != currentDir:
                        try:
                            # move it to the dir we are flattening into
                            shutil.move(joinedFile,parentDir)
                        except shutil.Error:
                            # use rename to overwrite existing files
                            os.rename(joinedFile,os.path.join(parentDir,file))
                
            
            # if we arent working on the parent dir, delete the now empty dir
            if parentDir != currentDir:
                os.rmdir(currentDir)

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'dem_downloader').lower()

# switch the tool
if toolname == 'foobar':
    # RUN the tool here and create the output in /out
    print('This toolbox does not include any tool. Did you run the template?\n')
    
    # write parameters to STDOUT.log
    pprint(kwargs)

elif toolname == 'dem_downloader':
    # get the parameters
    try:
        provider = kwargs.get('provider', 'COPERNICUS')
        product = kwargs.get('product', 'GLO-30')
        unzip = kwargs.get('unzip', True)
        flatten = kwargs.get('flatten', True)
        long_dir = kwargs.get('long_direction', 'E')
        lat_dir = kwargs.get('lat_direction', 'N' )
        long = kwargs.get('longitude', 9) # Default lat lon for KIT IWG
        lat = kwargs.get('latitude', 50)
        tidy = kwargs.get('tidyup', True)

    except Exception as e:
        print(str(e))
        sys.exit(1)


    # Download and save to out folder (30m tile)
    url = 'https://prism-dem-open.copernicus.eu/pd-desk-open-access/prismDownload/COP-DEM_GLO-30-DGED__2022_1/'
    #Adding leading zeros for URL compatibility (Refer Copernicus Documentation)
    long = str(long).zfill(3)
    lat = str(lat).zfill(2)
    file = 'Copernicus_DSM_10_'+lat_dir+lat+'_00_'+long_dir+long+'_00.tar'

    file_url = url + file

    print(f'Start downloading LAT: {lat} LONG: {long} from: {url}...')
    t1  = time.time()
    res = requests.get(file_url)
    t2 = time.time()
    print(f"Finsihed downloading after {round(t2 - t1, 1)} seconds.\nExtracting...")
    if res.status_code == 200:
        zname = os.path.join('/out', file)
        zfile = open(zname, 'wb')
        zfile.write(res.content)
        zfile.close()
    t3 = time.time()
    print(f"Done writing after {round(t3 - t2, 1)} seconds.")

    if unzip==False:
        # open file
        print(f"Exiting Program")    
        sys.exit(0)

    if unzip:
        # open file
        file = tarfile.open(zname)
        # extracting file
        file.extractall('/out')
        file.close() 
        t4 = time.time()   
        print(f"Finished unzipping after {round(t4 - t3, 1)} seconds.")

    if flatten==False:
     # open file
        print(f"Exiting Program")    
        sys.exit(0)    

    if flatten:
        flatt('/out','/out')      
        t5 = time.time() 
        print(f"Finished flattening after {round(t5 - t4, 1)} seconds.") 

    if tidy:
        os.remove(zname)

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")