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
# Credits - https://amitd.co/code/python/flatten-a-directory
import shutil
def flatten(directory):
    for dirpath, _, filenames in os.walk(directory, topdown=False):
        for filename in filenames:
            i = 0
            source = os.path.join(dirpath, filename)
            target = os.path.join(directory, filename)

            while os.path.exists(target):
                i += 1
                file_parts = os.path.splitext(os.path.basename(filename))

                target = os.path.join(
                    directory,
                    file_parts[0] + "_" + str(i) + file_parts[1],
                )

            shutil.move(source, target)

            print("Moved ", source, " to ", target)

        if dirpath != directory:
            os.rmdir(dirpath)

            print("Deleted ", dirpath)
            
            
            