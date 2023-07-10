from data_preprocessor import preprocess_era5_data, preprocess_gcm_data, preprocess_gsod_data
from data_downloader import download_era5_data, download_gcm_data, download_gsod_data
from data_validation import validate_preprocessed_era5, validate_preprocessed_gcm, validate_preprocessed_gsod
import os
from datetime import datetime, timezone
from collections import OrderedDict as odict

def dupless(lst:list) -> bool:
    'returns true if all values in list are unique (i.e. if lst is an ordered set)'
    return lst == list(set(lst))

class WeatherData:
    '''
    This struct is intended to abstract the processes of data_downloader and data_preprocessor for various DMiner data sources.
    Simply initialize, call download, and call preprocessing, which will also validate itself.

    Accepts source "ERA5" ([read more here](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)) or number 1, 
    "IPCC Global Climate Model (GCM) Output" ([read more here](https://ipcc-data.org/sim/gcm_monthly/)) or number 2, 
    "Global Surface Summary of the Day - GSOD" ([read more here](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00516)) or number 3.

    If data for this is known an exclusive fp will be made to it in self.data, and likewise for preprocessed_data.

    This struct was designed from the bottom-up to care for daily, surface-level (often "2M" above) data.

    Currently only handling data_type='tmp'
    '''
    SOURCES = odict({
        'ERA5': 1,
        'IPCC Global Climate Model (GCM) Output': 2,
        'Global Surface Summary of the Day - GSOD': 3
    })
    GCMS = odict({
        'SSP245': 1,
        'SSP585': 2   
    })
    TYPE_MAP = {
        'tmp': { # temperatures are only considered at surface-level for our purposes.
            1: ('2m_temperature', 't2m'),
            2: '?',
            3: '?'
        },
        'percip': {
            3: '?'
        }
    }
    DEFAULT_TYPE_MAP = {
        1: (['2m_temperature'], ['t2m'], ['tmp']), # i'm in chronological order!
    }
    DATE_MAP = {
        1: (datetime(1979, 1, 1, tzinfo=timezone.utc), # like GSOD, data continues to present, but we have decided to train model on data until 2015-01-01 00:00.
            datetime(2015, 1, 1, 23, tzinfo=timezone.utc)), # in effect this will be downloading for all 24 hours of every day, and later averaging all of them.
        2: (datetime(1979, 1, 1, tzinfo=timezone.utc), datetime(2100, 1, 1, 23, tzinfo=timezone.utc)),
        3: (datetime(1979, 1, 1, tzinfo=timezone.utc), datetime(2023, 1, 1, 23, tzinfo=timezone.utc)) # GSOD records actually begin in 1929.
    }

    def __init__(self, source, gcm_type=None, data_types='default', start_date:datetime=None, end_date:datetime=None, force=False, verbose=False):
        '''
        Source implies date ranges (see DATE_MAP), overriding dates is possible, but support has been deprecated since 2023-07-01.

        data_types must be either str of expected types (see TYPE_MAP) or list thereof. 
        alternatively 'default' assumes the values based on what is needed for dminer research.

        if source is GCM (2), gcm_type must be specified: either 'SSP245' (1) or 'SSP585' (2).
        '''
        if isinstance(source, int): 
            assert 1 <= source <= 3, 'Invalid source number'
            self.source = source
        else:
            assert source in self.SOURCES, 'Invalid source name'
            self.source = self.SOURCES[source] # self.source will be a number
        if self.source == 2:
            if gcm_type not in self.GCMS:
                if gcm_type != 1 and gcm_type != 2: assert False, 'GCM type expected, got invalid input'
                else: self.gcm_type = gcm_type
            else: self.gcm_type = self.GCMS[gcm_type]
            
        # date mapping to presumed values for our experiments if not overridden in parameters
        if not start_date and end_date: print('WARNING:\tend_date provided but not start_date --is this intentional?')
        self.start_date = start_date if isinstance(start_date, datetime) else self.DATE_MAP[self.source][0]
        self.end_date = end_date if isinstance(end_date, datetime) else self.DATE_MAP[self.source][1]
        if self.end_date == self.start_date: print(f'asking for weather data from source {source}?... weird')
        assert not (end_date and self.end_date < self.start_date), 'End date not after start date'

        assert isinstance(force, bool), 'Force not bool'
        self.force = force

        assert isinstance(force, bool), 'Verbose not bool'
        self.verbose = verbose

        self.downloaded = False
        self.preprocessed = False
        self.validated = False

        if data_types == 'default': 
            self._downloadingtypenames, self._downloadedtypenames, self.data_types = self.DEFAULT_TYPE_MAP[self.source]
        else:
            if isinstance(data_types, str): data_types = [data_types]
            else: assert dupless(data_types), 'data_types passed in is not unique list'
            self.data_types = data_types
            self._downloadingtypenames = [] # data label name during the downloading process
            self._downloadedtypenames = [] # data label name once downloaded, to be transformed to standard format in preprocessing
            for e in data_types: 
                assert e in self.TYPE_MAP, f"Incorrect data type '{e}'"
                assert self.source in self.TYPE_MAP[e], f"Invalid data type '{e}' for source-type {self.source}"
                dlingname, dlname = self.TYPE_MAP[e][self.source]
                self._downloadingtypenames.append(dlingname)
                self._downloadedtypenames.append(dlname)

        self._timestr = f"from {self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}" if self.end_date else f'at {self.start_date}'
        self._typestr = ', '.join(self.data_types)
        self._str = f'WeatherData source {source}, type(s) {self._typestr}, {self._timestr}'
        self._downloadat = f'./downloads/{self.source}/{self._typestr}/{self._timestr}/'
        self._preprocessat = f'./preprocessed/{self.source}/{self._typestr}/{self._timestr}/'
        self._downloadpatterns = {
            1: self._downloadat + 'data.nc',
            2: self._downloadat + 'data...', # need updating
            3: self._downloadat + 'data...' # need updating
        }
        self._preprocesspatterns = {
            1: self._preprocessat + 'data.csv',
            2: self._preprocessat + 'data...', # need updating
            3: self._preprocessat + 'data...' # need updating
        }

        if verbose: print(f'{self} initialized.')

    def get_time(self) -> str:
        return self._timestr
    
    def get_type(self) -> str:
        return self._typestr
    
    def __str__(self) -> str:
        return self._str

    def download(self):
        '''
        if force is false this function will skip downloading if a download exists in ./downloads/$SOURCE/$DATA_TYPE/$DATE
        
        downloads world data
        '''
        if not os.path.exists(self._downloadat): os.makedirs(self._downloadat) 
        if not self.force and os.path.exists(self._downloadpatterns[self.source]):
            print(f'{self} data already exists. Skipping download.')
            self.downloaded = True
            return

        if self.source == 1: 
            self.downloaded = download_era5_data(self._downloadingtypenames, 
                self.start_date, self.end_date, self._downloadat)
        elif self.source == 2: 
            self.downloaded = download_gcm_data(self._downloadingtypenames, 
                self.start_date, self.end_date, self._downloadat)
        elif self.source == 3: 
            self.downloaded = download_gsod_data(self._downloadingtypenames, 
                self.start_date, self.end_date, self._downloadat)
        else: assert False, 'unexpected source in downloader'

        if not self.downloaded: print(f'{self} reported a failed download')
        elif self.verbose: print(f'{self} reported a successful download')

    def preprocess(self, release=True):
        '''
        if force is false this function will skip preprocessing if an export exists in ./preprocessed/$SOURCE/$DATA_TYPE/$DATE

        interpolates globally to 1.25 degrees.
        '''
        if not os.path.exists(self._preprocessat): os.makedirs(self._preprocessat)
        if not self.force and os.path.exists(self._preprocesspatterns[self.source]):
            print(f'{self} data already exists. Skipping preprocessing.')
            self.preprocessed = True
            return
        
        if self.source == 1: 
            self.preprocessed = preprocess_era5_data(self._downloadedtypenames, self.data_types,
                1.25, self._downloadat, self._preprocessat, self.verbose)
        elif self.source == 2: 
            self.preprocessed = preprocess_gcm_data(self._downloadedtypenames, self.data_types,
                1.25, self._downloadat, self._preprocessat, self.verbose)
        elif self.source == 3: 
            self.preprocessed = preprocess_gsod_data(self._downloadedtypenames, self.data_types,
                1.25, self._downloadat, self._preprocessat, self.verbose)
        else: assert False, 'unexpected source in preprocessor'

        if not self.preprocessed: print(f'{self} reported a failed preprocessing')
        elif self.verbose: print(f"dataframe {self} saved as with columns noted above")
    
    def validate(self, verbose=True):
        '''
        verbose if not nonetype will override self.verbose value in the context of this function.
        
        validates only preprocessed data.
        '''

        if self.source == 1: 
            self.validated = validate_preprocessed_era5(self.data_types,
                verbose if isinstance(verbose, bool) else self.verbose, self.start_date, self.end_date, 1.25, self._preprocessat)
        elif self.source == 2: 
            self.validated = validate_preprocessed_gcm(self.data_types,
                verbose if isinstance(verbose, bool) else self.verbose, self.start_date, self.end_date, 1.25, self._preprocessat)
        elif self.source == 3: 
            self.validated = validate_preprocessed_gsod(self.data_types,
                verbose if isinstance(verbose, bool) else self.verbose, self.start_date, self.end_date, 1.25, self._preprocessat)
        else: assert False, 'unexpected source in validator'

        if not self.preprocessed: print(f'{self} reported a failed validation')
        elif verbose: print(f"{self} passed validation")
