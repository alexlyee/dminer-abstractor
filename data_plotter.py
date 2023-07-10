import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def plot_spatial_freq_map(data_dir, variable, start_year, end_year):
    """
    Create a spatial frequency map for a specified variable and time period.

    Parameters:
    - data_dir: The directory where the data file is located.
    - variable: The variable of interest to plot.
    - start_year, end_year: The time period for which to plot the data.
    """
    # Load the data
    df = pd.read_csv(f'{data_dir}/data.csv')
    
    # Filter for the specified time period and variable
    df['time'] = pd.to_datetime(df['time'])
    df = df[(df['time'].dt.year >= start_year) & (df['time'].dt.year <= end_year)]
    
    # Create a pivot table with latitude and longitude as indices
    pivot = df.pivot_table(values=variable, index='latitude', columns='longitude')
    
    # Create the plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.set_global()
    
    plt.contourf(pivot.columns, pivot.index, pivot.values, transform=ccrs.PlateCarree(), cmap='viridis')
    
    plt.title(f'Spatial Frequency of {variable} ({start_year}-{end_year})')
    plt.colorbar(label=variable)
    plt.show()

def plot_data(df1, df2, title1, title2):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
    plt.imshow(df1)
    plt.title(title1)

    plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
    plt.imshow(df2)
    plt.title(title2)

    plt.show()


def plot_data(variable):
    df = pd.read_csv(f'{variable}_data.csv')

    # Assuming we're working with time series data
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # plot data
    df['t2m'].plot()

    plt.show()

def plot_global_data(variable, name='April 2023'):
    # Load data from the csv file
    data = pd.read_csv(f'{variable}_data.csv')

    print(data.shape)

    # cast to 32bit
    data['t2m'] = data['t2m'].astype(np.float32)

    #longitude = np.linspace(-180, 180, 192)
    #latitude = np.linspace(-90, 90, 94)
    #longitude, latitude = np.meshgrid(longitude, latitude)

    # Create a contour plot of the data
    #lon, lat = np.meshgrid(data.longitude.unique(), data.latitude.unique())
    #plt.contourf(longitude, latitude, data.t2m, cmap='jet')
    
        # Pivot data to 2D format suitable for contour plot
    data_2d = data.pivot(index='latitude', columns='longitude', values='t2m')

    # Create a contour plot of the data
    plt.contourf(data_2d.columns, data_2d.index, data_2d.values, cmap='jet')
    plt.colorbar()
    plt.title(f'Monthly Average 2m Temperature for {name}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
