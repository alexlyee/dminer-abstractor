from data_merger import *
from data_plotter import *
from ingest_struct import WeatherData
import string
import random
from typing import Union
import asyncio

class WorkingData:
    '''
    This struct is intended to abstract the process of data_merger and data_plotter.

    Expects a preprocessed WeatherData or a list thereof.

    You may set a contant UID value for WorkingData to proceed assuming it has prepared its data before. 
    Use with CAUTION though, as this obviously may be unpredictable.
    '''
    def __init__(self, data: Union[WeatherData, list], UID=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))):
        # here we really need to enforce that it's in a list form for future logic to work, and we need to ensure that each element in the list is WeatherData.
        self.merged = isinstance(data, WeatherData)
        if not self.merged: data = [data]
        assert all([e.preprocessed_data for e in data]), "WeatherData is not fully preprocessed" # assuming list is all weatherdata
        self.data = data

        self.prepared = False
        self.UID = UID
        self.df = None
        self._folder = f"./working/{self.UID}/"
        self._datastring = '\n\t' + '\n\t'.join(data)
        self._str = f'WorkingData {self._folder} containing the following data:\n\t{self._datastring}'

    def __str__(self):
        return self._str

    # I realize it would be very complicated to handle the force=False case here because there's no reliable way of 
    # knowing if WeatherData's files were modified since last initilization. Thus, that will have to wait.

    def merger(self, technique="saveall") -> bool:
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

    def prepare(self, technique="combine", force=False) -> bool:
        'Saves to "./working/{self.UID}/". When force is false prepare will skip standardization if already prepared '
        if not len(self.data) > 1: self.merger(technique)
        if self.prepared and not force: self.prepared = self.standardize()
        assert self.validate(), f'working data of type {self} --failing validation.'
        return self.prepared
        
    def plot(self, techniques="all"):
        '''
        Attempts to plot "./working/{self.UID}/data.csv"

        '''
        # 
        pass

    def standardize(self, location:str=None) -> bool:
        '''
        By default, this will simply standardize the WeatherData for our plotting functions in-place, appending "_standardized" before .csv
        This will validate the possible plotting techniques that may be used. location uses self._folder by default
        '''
        if not location: location = self._folder
        # ...currently there is only one state we worry about
        return True

    def validate(self, location:str=None) -> bool:
        'Double-checks for expected values from standardized data'
        if not location: location = self._folder
        # ...currently there is only one state we worry about.
        return True

