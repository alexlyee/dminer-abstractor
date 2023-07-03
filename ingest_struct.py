from data_preprocessor import preprocess_ncep_data, preprocess_ipcc_data, preprocess_gsod_data
from data_downloader import download_ncep_data, download_ipcc_data, download_gsod_data
import os
from datetime import datetime

class WeatherData:
    '''
    This struct is intended to abstract the processes of data_downloader and data_preprocessor for various DMiner data sources.
    Simply initialize, call download, and call preprocessing, which will also validate itself.

    Accepts source "NCEP/DOE Reanalysis II" or number 1, 
    "IPCC Global Climate Model Output" or number 2, 
    "Global Surface Summary of the Day - GSOD" or number 3.

    If data for this is known an exclusive fp will be made to it in self.data, and likewise for preprocessed_data.

    end_date can be null.

    Currently only handling data_type="tmp"
    '''
    SOURCES = {
        "NCEP/DOE Reanalysis II": 1,
        "IPCC Global Climate Model Output": 2,
        "Global Surface Summary of the Day - GSOD": 3
    }
    TYPE_MAP = {
        "tmp": {
            1: "NA",
            2: "2m_temperature",
            3: "NA"
        }
    }

    def __init__(self, source, data_type:str, start_date:datetime, end_date:datetime, force=False):
        if isinstance(source, int): 
            assert 1 <= source <= 3, "Invalid source number"
            self.source = source
        else:
            assert source in self.SOURCES, "Invalid source name"
            self.source = self.SOURCES[source] # self.source will be a number

        assert data_type == "tmp", "Incorrect data type"
        self.data_type = self.TYPE_MAP[data_type][self.source]

        assert not (not start_date and end_date), "Lacking start date"
        assert not (end_date and end_date < start_date), "End date not after start date"
        if end_date == start_date: print(f'asking for weather data from source {source}?... weird')
        self.start_date = start_date
        self.end_date = end_date

        assert isinstance(force, bool), "Force not bool"
        self.force = force

        self.downloaded = False
        self.preprocessed = False
    
        self._time = f"from {self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}" if self.end_date else f"at {self.start_date}"
        self._str = f'WeatherData source {source}, type {data_type}, {self._time}'
        self._downloadat = f'./downloads/{self.source}/{data_type}/{self._time}/'
        self._preprocessat = f'./preprocessed/{self.source}/{data_type}/{self._time}/'
        self._downloadpatterns = {
            1: self._downloadat + "data...", # need updating
            2: self._downloadat + "data.nc",
            3: self._downloadat + "data..." # need updating
        }
        self._preprocesspatterns = {
            1: self._preprocessat + "data...", # need updating
            2: self._preprocessat + "data.csv",
            3: self._preprocessat + "data..." # need updating
        }


    def __str__(self) -> str:
        return self._str

    def get_time(self) -> str:
        return self._time

    def download(self):
        '''
        if force is false this function will skip downloading if a download exists in ./downloads/$SOURCE/$DATA_TYPE/$DATE
        
        downloads world data
        '''
        if not os.path.exists(self._downloadat): os.makedirs(self._downloadat) 
        if not self.force and os.path.exists(self._downloadpatterns[self.source]):
            print(f"{self} data already exists. Skipping download.")
            return

        if self.source == 1: self.downloaded = download_ncep_data(self.data_type, self.start_date, self.end_date, self._downloadat)
        elif self.source == 2: self.downloaded = download_ipcc_data(self.data_type, self.start_date, self.end_date, self._downloadat)
        elif self.source == 3: self.downloaded = download_gsod_data(self.data_type, self.start_date, self.end_date, self._downloadat)
        else: assert False, "unexpected source in downloader"

    def preprocess(self, release=True):
        '''
        if force is false this function will skip preprocessing if an export exists in ./preprocessed/$SOURCE/$DATA_TYPE/$DATE

        interpolates globally to 1.25 degrees.
        '''
        if not os.path.exists(self._preprocessat): os.makedirs(self._preprocessat)
        if not self.force and os.path.exists(self._preprocesspatterns[self.source]):
            print(f"{self} data already exists. Skipping preprocessing.")
            return
        
        if self.source == 1: self.preprocessed = preprocess_ncep_data(self.data_type, 1.25, self._downloadat, self._preprocessat)
        elif self.source == 2: self.preprocessed = preprocess_ipcc_data(self.data_type, 1.25, self._downloadat, self._preprocessat)
        elif self.source == 3: self.preprocessed = preprocess_gsod_data(self.data_type, 1.25, self._downloadat, self._preprocessat)
        else: assert False, "unexpected source in downloader"

        self.validate(False)
    
    def validate(self, verbose=True):
        
        pass


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