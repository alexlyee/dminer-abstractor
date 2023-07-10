from data_preprocessor import preprocess_era5_data, preprocess_ipcc_data, preprocess_gsod_data
from data_downloader import download_era5_data, download_ipcc_data, download_gsod_data
from data_validation import *
import os
from datetime import datetime, timezone

class WeatherData:
    '''
    This struct is intended to abstract the processes of data_downloader and data_preprocessor for various DMiner data sources.
    Simply initialize, call download, and call preprocessing, which will also validate itself.

    Accepts source "ERA5" ([read more here](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)) or number 1, 
    "IPCC Global Climate Model (GCM) Output" ([read more here](https://ipcc-data.org/sim/gcm_monthly/)) or number 2, 
    "Global Surface Summary of the Day - GSOD" ([read more here]()) or number 3.

    If data for this is known an exclusive fp will be made to it in self.data, and likewise for preprocessed_data.

    Currently only handling data_type='tmp'
    '''
    SOURCES = {
        "ERA5": 1,
        "IPCC Global Climate Model (GCM) Output": 2,
        "Global Surface Summary of the Day - GSOD": 3
    }
    TYPE_MAP = {
        "tmp": {
            1: "2m_temperature",
            2: "NA",
            3: "NA"
        }
    }
    DEFAULT_TYPE_MAP = {
        1: [
            
        ]
    }
    DATE_MAP = {
        1: (datetime(1979, 1, 1, tzinfo=timezone.utc), datetime(2015, 1, 1, tzinfo=timezone.utc)), # like GSOD, data continues to present, but we have decided to train model on data until 2015-01-01 00:00.
        2: (datetime(1979, 1, 1, tzinfo=timezone.utc), datetime(2100, 1, 1, tzinfo=timezone.utc)),
        3: (datetime(1979, 1, 1, tzinfo=timezone.utc), datetime(2023, 1, 1, tzinfo=timezone.utc)) # GSOD records actually begin in 1929.
    }

    def __init__(self, source, data_type:str, start_date:datetime=None, end_date:datetime=None, force=False, verbose=False):
        '''
        Source implies date ranges (see DATE_MAP), overriding dates is possible, but support has been deprecated since 2023-07-01.
        '''
        if isinstance(source, int): 
            assert 1 <= source <= 3, "Invalid source number"
            self.source = source
        else:
            assert source in self.SOURCES, "Invalid source name"
            self.source = self.SOURCES[source] # self.source will be a number

        assert data_type == "tmp", "Incorrect data type"
        self.data_type = data_type

        # date mapping to presumed values for our experiments if not overridden in parameters
        if not (not start_date and end_date): print("WARNING:\tend_date provided but not start_date --is this intentional?")
        self.start_date = start_date if isinstance(start_date, datetime) else self.DATE_MAP[data_type][0]
        self.end_date = end_date if isinstance(end_date, datetime) else self.DATE_MAP[data_type][1]
        if self.end_date == self.start_date: print(f'asking for weather data from source {source}?... weird')
        assert not (end_date and self.end_date < self.start_date), "End date not after start date"

        assert isinstance(force, bool), "Force not bool"
        self.force = force

        self.downloaded = False
        self.preprocessed = False
    
        self._time = f"from {self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}" if self.end_date else f"at {self.start_date}"
        self._str = f'WeatherData source {source}, type {data_type}, {self._time}'
        self._downloadat = f'./downloads/{self.source}/{data_type}/{self._time}/'
        self._preprocessat = f'./preprocessed/{self.source}/{data_type}/{self._time}/'
        self._downloadpatterns = {
            1: self._downloadat + "data.nc",
            2: self._downloadat + "data...", # need updating
            3: self._downloadat + "data..." # need updating
        }
        self._preprocesspatterns = {
            1: self._preprocessat + "data.csv",
            2: self._preprocessat + "data...", # need updating
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

        if self.source == 1: 
            self.downloaded = download_era5_data(self.TYPE_MAP[self.data_type][self.source], 
                self.start_date, self.end_date, self._downloadat)
        elif self.source == 2: 
            self.downloaded = download_ipcc_data(self.TYPE_MAP[self.data_type][self.source], 
                self.start_date, self.end_date, self._downloadat)
        elif self.source == 3: 
            self.downloaded = download_gsod_data(self.TYPE_MAP[self.data_type][self.source], 
                self.start_date, self.end_date, self._downloadat)
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
        
        if self.source == 1: 
            self.preprocessed = preprocess_era5_data(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        elif self.source == 2: 
            self.preprocessed = preprocess_ipcc_data(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        elif self.source == 3: 
            self.preprocessed = preprocess_gsod_data(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        else: assert False, "unexpected source in downloader"
    
    def validate(self, verbose=True):
        'verbose if not nonetype will override self.verbose value in the context of this function.'

        if self.source == 1: 
            self.preprocessed = validate_preprocessed_era5(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        elif self.source == 2: 
            self.preprocessed = preprocess_ipcc_data(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        elif self.source == 3: 
            self.preprocessed = preprocess_gsod_data(self.TYPE_MAP[self.data_type][self.source], 
                1.25, self._downloadat, self._preprocessat)
        else: assert False, "unexpected source in downloader"
