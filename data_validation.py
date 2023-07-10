from datetime import datetime

# it may not be a bad idea to impliment validation for the downloaded data.

##### general

def check_unique_dates(df, verbose=True):
    num_unique_dates = df['time'].nunique()
    num_total_dates = len(df)
    if num_unique_dates != num_total_dates: print("Warning: Dates are not unique.")
    else: print("Dates are unique.")

def check_complete_dates(df, delta=1, verbose=True):
    '''
    `delta` is the number of hours that are expected between each time. 
    Warns if there is an unexpected datetime or lack thereof
    '''
    # code

def check_missing_values(df, verbose=True):
    if df.isnull().sum().sum() > 0: print("Warning: There are missing values.")
    else: print("No missing values detected.")

def check_lat_lon_range(df, verbose=True):
    if df['latitude'].min() < -90 or df['latitude'].max() > 90: print("Warning: Latitude out of range.")
    if df['longitude'].min() < 0 or df['longitude'].max() > 360: print("Warning: Longitude out of range.")

############# ERA5

import pandas as pd
import numpy as np
from typing import Union

# it is worth noting that this ERA5 data will naturally produce many redundant values at 90 degrees and -90 degrees latitude.
# I will not delete it because I'm not sure if that is ultimately desired behavior.

def validate_preprocessed_era5(variables: Union[str, list], verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:
    '''
    loads data from {get_from}data.nc

    validates that era5 data is in form time | latitude | longitude | [variable | s ...]
    as such variables is expected to be an str or list thereof
    
    if being verbose, will warn when any variable passed in is not of expected form (i.e. it will not be tested)
    also warns if any number of NAs are found

    ensures that all expected fields are in latitude (-90 -> 90) longitude (0 -> 360-interpolation) grid based on interpolation (degrees). 

    ensures that exactly one exists for each point + day; one value per day.
    '''
    # Load dataframe
    df = pd.read_csv(f'{get_from}data.csv')

    # Check columns
    if isinstance(variables, list): expected_columns = ['time', 'latitude', 'longitude'] + variables
    else: expected_columns = ['time', 'latitude', 'longitude', variables]

    if not all(col in df.columns for col in expected_columns):
        if verbose: print("Columns of the data do not match the expected structure.")
        return False

    # Check for NAs
    if df.isna().sum().any():
        if verbose: print("Data contains NA values.")
        return False

    # Create grid of expected latitudes and longitudes
    expected_lats = np.arange(-90, 90, interpolation)
    expected_lons = np.arange(0, 360, interpolation)
    
    # Check if all expected latitudes and longitudes are present
    if not all(lat in df['latitude'].unique() for lat in expected_lats):
        if verbose: print("Some latitudes are missing from the data.")
        return False

    if not all(lon in df['longitude'].unique() for lon in expected_lons):
        if verbose: print("Some longitudes are missing from the data.")
        return False

    # Check for duplicate entries for the same day + lat + lon
    if df.duplicated(['time', 'latitude', 'longitude']).sum() > 0:
        if verbose: print("Duplicate entries found for the same day and location.")
        return False

    # Create expected dates
    expected_dates = pd.date_range(start_date, end_date)
    
    # Check if all expected dates are present
    if not all(date.strftime('%Y-%m-%d') in df['time'].unique() for date in expected_dates):
        if verbose: print("Some dates are missing from the data.")
        return False

    return True





############# GSM

def validate_preprocessed_gcm(variable, verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:

    return True


############# GSOD

def validate_preprocessed_gsod(variable, verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:

    return True
