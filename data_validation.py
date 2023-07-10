

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

def validate_preprocessed_era5(variable, interpolation=1.25, ):
    pass




############# GSM




############# GSOD


