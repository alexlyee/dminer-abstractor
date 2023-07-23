import pandas as pd
import matplotlib.pyplot as plt
from data_downloader import *
from data_plotter import *
from data_preprocessor import *
from ingest_struct import WeatherData
import asyncio

def main():
    #test = WeatherData(2, "tmp", datetime.strptime('2023-04-02', '%Y-%m-%d'), datetime.strptime('2023-04-30', '%Y-%m-%d'))
    test = WeatherData(2, 2, force=True, verbose=True)
    print(test)
    test.download()
    test.preprocess()
    test.validate()

if __name__ == "__main__":
    main()
