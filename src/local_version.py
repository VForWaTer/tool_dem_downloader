import os
import requests
print('Hello')

long_dir = 'E'
lat_dir = 'N'
long = 9
lat = 50

os.chdir(r'u:\02_Software\Github\tool_dem_downloader')
         
# Download and save to out folder (30m tile)
url = 'https://prism-dem-open.copernicus.eu/pd-desk-open-access/prismDownload/COP-DEM_GLO-30-DGED__2022_1/'
#Adding leading zeros for URL compatibility (Refer Copernicus Documentation)
long = str(long).zfill(3)
lat = str(lat).zfill(2)
file = 'Copernicus_DSM_10_'+lat_dir+lat+'_00_'+long_dir+long+'_00.tar'

file_url = url + file

res = requests.get(file_url)
if res.status_code == 200:
    zname = os.path.join('out', file)
    zfile = open(zname, 'wb')
    zfile.write(res.content)
    zfile.close()
    
    

# importing the "tarfile" module
import tarfile
  
# open file
file = tarfile.open(zname)
  
# extracting file
file.extractall('./out')
  
file.close()

#To flatten 
# Credits - https://gist.github.com/oatkiller/4429244
import shutil
import glob

def flatten(parentDir,currentDir):
    # get all the files in the current dir
    files = os.listdir(currentDir)
    
    for file in files:
        # get the path of the file relative to the dir its in
        # so "./file" or on successive runs: "./dir/file"
        joinedFile = os.path.join(currentDir,file)
        
        if os.path.isdir(joinedFile):
            # run the dir function on dirs
            flatten(parentDir,joinedFile)
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

parentDir = r'u:\02_Software\Github\tool_dem_downloader\out'  
currentDir = r'u:\02_Software\Github\tool_dem_downloader\out\Copernicus_DSM_10_N50_00_E009_00'           
flatten(parentDir,currentDir)          

if unzip:
   print('Hello')     