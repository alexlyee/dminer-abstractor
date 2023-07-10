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

def validate_preprocessed_era5(variable, verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:
    '''
    loads data from {get_from}data.nc

    validates that era5 data is in form time | latitude | longitude | [variable | s ...]
    
    if being verbose, will warn when any variable passed in is not of expected form (i.e. it will not be tested)
    also warns if any number of NAs are found

    ensures that all expected fields are in latitude (-90 -> 90) longitude (0 -> 360-interpolation) grid based on interpolation (degrees). 

    ensures that exactly one exists for each point + day; one value per day.
    '''

    return True




############# GSM

def validate_preprocessed_gcm(variable, verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:

    return True


############# GSOD

def validate_preprocessed_gsod(variable, verbose:bool, start_date:datetime, end_date:datetime, interpolation:int, get_from='./') -> bool:

    return True
