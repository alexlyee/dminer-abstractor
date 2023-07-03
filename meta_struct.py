from data_merger import *
from data_plotter import *
from ingest_struct import WeatherData
import string
import random

class WorkingData:
    '''
    This struct is intended to abstract the process of data_merger and data_plotter.

    Expects a preprocessed WeatherData or a list thereof.

    You may set a contant UID value for WorkingData to proceed assuming it has prepared its data before. 
    Use with CAUTION though, as this obviously may be unpredictable.
    '''
    def __init__(self, data, UID=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16)), merged=False, prepared=False):
        # here we really need to enforce that it's in a list form for future logic to work, and we need to ensure that each element in the list is WeatherData.
        if isinstance(data, WeatherData): data = [data]
        assert all([e.preprocessed_data for e in data]), "WeatherData is not fully preprocessed" # assuming list is all weatherdata
        self.data = data

        self.UID = UID
        self.merged = merged
        self.prepared = prepared
        self.df = None
        self._folder = f"./working/{self.UID}/"

    # I realize it would be very complicated to handle the force=False case here because there's no reliable way of 
    # knowing if WeatherData's files were modified since last initilization. Thus, that will have to wait.

    def merger(self, technique="saveall"):
        '''
        This function may be needed in the case where data needs to be merged someday; currently data_merger.py is empty
        Saves to "./working/{self.UID}/"
        technique:
          - saveall: merge into standardized form without losing any data (warning: duplicates)
          - combine: average values of the same type 
        '''
        if not len(self.data) > 1: return False
        # it is okay to leave this empty for now.
        self.merged = True

    def prepare(self, technique="combine"):
        'Saves to "./working/{self.UID}/"'
        if not self.merged: 
            if not len(self.data) > 1: self.merger(technique)
            else: standardize(self.data[0], self._folder)
        assert revalidate(self.data[0], self._folder), "merged data failing revalidation"
        self.prepared = True
        
    def plot(self, techniques="all"):
        '''
        Attempts to plot "./working/{self.UID}/data.csv"

        '''
        # 
        pass

def standardize(data, alternateLocation=None):
    '''
    By default, this will simply standardize the WeatherData for our plotting functions in-place, appending "_standardized" before .csv
    '''
    # ...currently there is only one state we worry about.
    assert revalidate, f"data of type {data.source} failing standardization."

def revalidate(data, alternateLocation=None):
    'Double-checks for expected values from standardized data'
    # ...currently there is only one state we worry about.
    return True