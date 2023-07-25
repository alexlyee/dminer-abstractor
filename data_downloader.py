####################### ERA5

import cdsapi
from datetime import datetime
from typing import Union
import asyncio

def download_era5_data(variables: Union[str, list], start_date:datetime, end_date:datetime, save_to='./') -> bool:
    '''
        downloads data at a single datetime or range thereof of global {variable} to data.nc in {save_to}
        save_to must end in a forward-slash.

        assumes range of times from start_date and end_date. this means end_date CANNOT be earlier in the day than start_date.
        ...well, technically an hour earlier, as the algorithm will not look at minutes, and hence rounds down all times to XX:00.
        ERA5 only has 00:00, 6:00, 12:00, and 18:00. so of those hours in your range, only those are included for the final request.
        That's up to four hours a day of DAILY DATA.

        This is daily data.

        variable must be str or list thereof.

        valid variables for era5 can be found here.
    '''
    assert start_date.time() <= end_date.time(), f"ERA5 data for {variables} has end_date with time before start_date"
    hour_list = [f'{hour:02d}:00' for hour in range(start_date.hour, end_date.hour + 1, 6)]
        # they don't like 0:00 :(

    c = cdsapi.Client()

    request_params = {
        'product_type': 'reanalysis',
        'variable': variables,
        'year': [start_date.year, end_date.year] if end_date else start_date.year,
        'month': [start_date.month, end_date.month] if end_date else start_date.month,
        'day': [start_date.day, end_date.day] if end_date else start_date.day,
        'time': hour_list if len(hour_list) > 1 else hour_list[0],
        'format': 'netcdf',
        # 'area': [lat+1, lon-1, lat-1, lon+1], # North, West, South, East.
    }

    c.retrieve(
        'reanalysis-era5-single-levels',
        request_params,
        f'{save_to}data.nc'
    )

    return True

################### GCM

import pandas as pd
import wget
import requests
import tqdm

def download_gcm_data(variables: Union[str, list], gcm_type:int, start_date:datetime, end_date:datetime, save_to='./') -> bool:
    """Download GCM data from CDS. Will get all 4 values per day.

    Args:
        variables (list): Variables to download
        gcm_type (str): GCM name, either 1 (SSP245 -> MIROC6) or 2 (SSP585 -> UKESM1-0-LL)        
            SSP245 - a scenario with low challenges for mitigation and adaptation
            SSP585 - a scenario with high challenges for mitigation and adaptation
        start_date (datetime): Start date
        end_date (datetime): End date  
        save_to (str): Path to save the data
    """
    # download method informed by professor's 
    # !wget -P /content/drive/MyDrive/P_Misc/Climate-Forecasting/GCM_bc \
        # \ https://download.scidb.cn/download?fileId=61b95de78bba886bd1c5216a&dataSetType=personal&fileName=atm_hist_1993_04.nc4 
        # \ https://download.scidb.cn/download?fileId=61babc7dac0a5211856bc715&dataSetType=personal&fileName=atm_ssp245_2094_08.nc4

    # Determine fileIds based on gcm_type and date range
  
    fileIds = ['61b95de78bba886bd1c5216a', '61babc7dac0a5211856bc715'] 
    
    for fileId in fileIds:
        url = f'https://download.scidb.cn/download?fileId={fileId}&dataSetType=personal'
        # Stream the response to a file on disk
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        filepath = f'{save_to}{fileId}.nc'
        
        progress_bar = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(filepath, 'wb') as f:
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                f.write(data)
            
        progress_bar.close()

    return True
    

    

################### GSOD

def download_gsod_data(variable, start_date:datetime, end_date:datetime, save_to='./') -> bool:
    return True