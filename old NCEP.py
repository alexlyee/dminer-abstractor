import os
import requests
import pickle
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def get_nc_files(dir_list):
    """
    Given a list of directories, return a list of all .nc files within them.
    """
    nc_files = []
    for directory in dir_list:
        nc_files.extend([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.nc')])
    
    print(f"Given directories, {len(nc_files)} found.")
    return nc_files

def ingest_nc_files(nc_files, download_dir):
    """
    Given a list of .nc files, return a dictionary mapping each file's path to its data.
    Also tries to re-download any files that cannot be opened.
    """
    all_datasets = {}
    for file in nc_files:
        try:
            data = xr.open_dataset(file).load()
            all_datasets[file] = data
        except Exception as e:
            print(f"Error opening file {file}: {e}")
            # Try to re-download the file
            print(f"Attempting to re-download {file}")
            url = "https://downloads.psl.noaa.gov" + file[len(download_dir):]  # construct the URL from the file path
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Save the content to the file
                with open(file, 'wb') as fp:
                    fp.write(response.content)
                # Try to open the file again
                try:
                    data = xr.open_dataset(file).load()
                    all_datasets[file] = data
                except Exception as e:
                    print(f"Still unable to open file {file} after re-downloading: {e}")
            else:
                print(f"Failed to download {file}. HTTP status code: {response.status_code}")
    print(f"{len(all_datasets)} datasets imported from {len(nc_files)} files.")
    return all_datasets

# Define a list of directories to search for .nc files
dir_list = ['./dl/downloads.psl.noaa.gov/Datasets/ncep.reanalysis2/Dailies/gaussian_grid']

# Get list of all .nc files
nc_files = get_nc_files(dir_list)

# Ingest all .nc files into a dictionary
all_datasets = ingest_nc_files(nc_files, './dl')

# Save the datasets as a pickled file
with open('all_datasets.pickle', 'wb') as f:
    pickle.dump(all_datasets, f)

# Plot an example dataset
example_file = next(iter(all_datasets))
example_data = all_datasets[example_file]
variable_name = next(iter(example_data.data_vars))

example_variable = example_data[variable_name]
last_month_data = example_variable[-1,:,:]

longitude = example_data.lon.values
latitude = example_data.lat.values
longitude, latitude = np.meshgrid(longitude, latitude)

plt.contourf(longitude, latitude, last_month_data, cmap='jet')
plt.colorbar()  # Add a colorbar for reference
plt.title(f'Last month data for variable {variable_name}')  # Set a title for the plot
plt.xlabel('Longitude')  # Label the x-axis
plt.ylabel('Latitude')  # Label the y-axis
plt.show()  # Display the plot
