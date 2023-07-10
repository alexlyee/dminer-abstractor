####################### ERA5

from datetime import datetime
import xarray as xr
import numpy as np

def preprocess_era5_data(variable:str, interpolate=1.25, get_from='./', save_to='./'):
    '''
        loads data from {get_from}data.nc, 
        interpolates at 1.25 degrees by default, 
        converts temp to celsius, 
        and saves dataframe as
        long | lat | time | var

        variable can be: '2m_temperature'
    '''
    # load netCDF file
    data = xr.open_dataset(f'{get_from}data.nc')

    # handle missing values
    df = data.to_dataframe()
    df.loc[10,'t2m'] = None
    missing = df.shape[0] - df['t2m'].count()
    print(f'{missing} missing values found in {get_from}data.nc.')
    if missing:
        df.fillna('NA', inplace=True)
        print('\treplaced with "NA"')

    if interpolate:
        # Create a new coordinate grid
        new_lon = np.arange(0, 360, interpolate)
        new_lat = np.arange(-90, 90, interpolate)

        # Interpolate the data to the new grid
        data_interp = data.interp(longitude=new_lon, latitude=new_lat, method='linear')

        # Convert to dataframe
        df = data_interp.to_dataframe()
    else:
        df = data.to_dataframe()

    # Reset the index to make Lat, Lon, and Time columns
    df = df.reset_index()

    # Convert tmp to celsius
    if variable == '2m_temperature':
        df['t2m'] = df['t2m'] - 273.15

    # Save dataframe as csv
    df.to_csv(f'{save_to}data.csv', index=False)

    print(f"dataframe {variable} saved as csv with columns:\t{', '.join(df.columns)}")
    return True

def check_ipcc_tmp(df):
    pass


################### IPCC

def preprocess_ipcc_data(variable:str, interpolate=1.25, get_from='./', save_to='./'):
    pass

################### GSOD

def preprocess_gsod_data(variable:str, interpolate=1.25, get_from='./', save_to='./'):
    pass

############## GENERAL