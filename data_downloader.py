####################### ERA5

import cdsapi
from datetime import datetime

def download_era5_data(variable, start_date:datetime, end_date:datetime, save_to='./') -> bool:
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
    assert start_date.time() <= end_date.time(), f"ERA5 data for {variable} has end_date with time before start_date"
    hour_list = [f'{hour:02d}:00' for hour in range(start_date.hour, end_date.hour + 1, 6)]
        # they don't like 0:00 :(

    c = cdsapi.Client()

    request_params = {
        'product_type': 'reanalysis',
        'variable': variable,
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

def download_gcm_data(variable, start_date:datetime, end_date:datetime, save_to='./') -> bool:
    return True

################### GSOD

def download_gsod_data(variable, start_date:datetime, end_date:datetime, save_to='./') -> bool:
    return True