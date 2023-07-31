import os
import requests
from datetime import datetime as dt
from pprint import pprint

from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'foobar').lower()

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

    except Exception as e:
        print(str(e))
        sys.exit(1)

# Check if 

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

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
