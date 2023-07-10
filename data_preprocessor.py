####################### ERA5

from datetime import datetime
import xarray as xr
import numpy as np
from typing import Union

def preprocess_era5_data(variables: Union[str, list], transform=None, interpolate=1.25, get_from='./', save_to='./', verbose:bool=False) -> bool:
    '''
        loads data from {get_from}data.nc, 
        interpolates at 1.25 degrees by default, 
        converts temp to celsius, 
        and saves dataframe as
        long | lat | time | [variable | s...]

        variables can include: 't2m'

        transform if not nonetype (str or list thereof) will transform variable name/s to something else.

        averages daily data to a single value at 00:00
    '''
    # for some reason era5 downloads to a variable with a different name than the one they ask for.

    # load netCDF file
    data = xr.open_dataset(f'{get_from}data.nc')
    if verbose: print(data, 'ERA5 data opened for preprocessing.')

    # handle missing values
    df = data.to_dataframe()
    for var in variables:
        df.loc[10,var] = np.nan
        missing = df.shape[0] - df[var].count()
        if verbose: print(f'{missing} missing values found in {var} of {get_from}data.nc.')
        if missing:
            df[var].fillna(method='bfill', inplace=True)  # you can choose your appropriate method to handle NaNs
            if verbose: print(f'\tMissing values in {var} replaced using backward fill')

    if verbose:
        print(df.index.unique())
        print("Number of unique timestamps: ", len(df.index.unique()))
        print("Total number of entries: ", len(df))

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
    
    # preprocess standard variables
    for v in variables:
        if v in df:
            if v == 't2m': # convert kelvin to celsius
                df[v] = df[v] - 273.15
            else: print(f'variable {v} lacking preprocessing in {get_from}data.nc')
        else: assert False, f'expected variable {v} not found in {get_from}data.nc'

    # Reset the index to make Lat, Lon, and Time columns
    df = df.reset_index()

    # Count number of rows with NaN values
    nan_rows = df.isnull().any(axis=1).sum()
    if verbose: print(f"Dropping {nan_rows} rows due to NaN values.")
    # Drop rows with NaN values
    df = df.dropna(how='any')

    # Print dataframe before resampling
    if verbose: print("\nDataframe before resampling:\n", df.head())

    # Average to daily values
    df.set_index('time', inplace=True)
    df.index = df.index.to_period('D')  # Convert the timestamp to daily period
    df = df.groupby(['latitude', 'longitude', df.index]).mean() 

    # Reset the index for 'time' to be timestamp again
    df.reset_index(inplace=True)
    df['time'] = df['time'].dt.to_timestamp()

    # Print dataframe after resampling
    if verbose: print("\nDataframe after resampling:\n", df.head())

    # Transform variable names
    if isinstance(transform, str): transform = [transform]
    if isinstance(transform, list):
        assert len(transform) == len(variables), 'incorrect transform list passed into era5 preprocessing'
        for original, new in zip(variables, transform):
            df.rename(columns={original: new}, inplace=True)

    # Save dataframe as csv
    df.to_csv(f'{save_to}data.csv', index=False)

    if verbose: print(f"preprocessed era5 data with columns {', '.join(df.columns)}\n{data}")
    return True

################### GCM

def preprocess_gcm_data(variable:str, interpolate=1.25, get_from='./', save_to='./', verbose:bool=False) -> bool:
    return True

################### GSOD

def preprocess_gsod_data(variable:str, interpolate=1.25, get_from='./', save_to='./', verbose:bool=False) -> bool:
    return True

############## GENERAL
