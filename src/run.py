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
from json2args.logger import logger

from helper import flatt


# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'dem_downloader').lower()

kwargs = get_parameter(typed=True)

if toolname == 'dem_downloader':
    logger.info("#TOOL START - dem_downloader")
    logger.debug(f"kwargs: {kwargs}")

    if kwargs.longitude is None or kwargs.latitude is None:
        raise ValueError("longitude and latitude are required parameters")
    
    # Download and save to out folder (30m tile)
    url = os.environ.get('DEM_URL', 'https://prism-dem-open.copernicus.eu/pd-desk-open-access/prismDownload/COP-DEM_GLO-30-DGED__2022_1/')
    
    #Adding leading zeros for URL compatibility (Refer Copernicus Documentation)
    long = str(kwargs.longitude).zfill(3)
    lat = str(kwargs.latitude).zfill(2)
    file = f"Copernicus_DSM_10_{kwargs.lat_direction}{lat}_00_{kwargs.long_direction}{long}_00.tar"
    file_url = url + file

    logger.debug(f"Downloading file: {file} from: {file_url}")

    t1  = time.time()
    try:
        zname = os.path.join(kwargs.output_dir, file)
        with open(zname, 'wb') as f:
            res = requests.get(file_url, stream=True)
            total = int(res.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            for data in res.iter_content(block_size):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total)
                sys.stdout.write('\r[{}{}] {:.1f}%'.format('=' * done, ' ' * (50 - done), downloaded * 100 / total))
                sys.stdout.flush()
            sys.stdout.write('\n')
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        sys.exit(1)
    
    t2 = time.time()
    logger.info(f"Done writing after {t2 - t1:.1f} seconds.")

    if kwargs.unzip:
        # open file
        file = tarfile.open(zname)
        # extracting file
        file.extractall(kwargs.output_dir)
        file.close() 
        t3 = time.time()   
        logger.info(f"Finished unzipping after {t3 - t2:.1f} seconds.")
    else:
        logger.info("#TOOL END - dem_downloader")
        sys.exit(0)

    if kwargs.flatten:
        flatt(kwargs.output_dir, kwargs.output_dir)      
        t4 = time.time() 
        logger.info(f"Finished flattening after {t4 - t3:.1f} seconds.")
    else:
        logger.info("#TOOL END - dem_downloader")
        sys.exit(0)

    if kwargs.tidyup:
        os.remove(zname)

    logger.info("#TOOL END - dem_downloader")
    sys.exit(0)

# In any other case, it was not clear which tool to run
else:
    raise AttributeError(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")