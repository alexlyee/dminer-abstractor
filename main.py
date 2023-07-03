import pandas as pd
import matplotlib.pyplot as plt
from data_downloader import *
from data_plotter import *
from data_preprocessor import *
from ingest_struct import WeatherData

def main():
    test = WeatherData(2, "tmp", datetime.strptime('2023-04-02', '%Y-%m-%d'), datetime.strptime('2023-04-30', '%Y-%m-%d'))
    print(test)
    test.download()
    test.preprocess()

"""    variable = '2m_temperature'  # The variable we're interested in
    lat, lon = 0, 90  # The latitude and longitude
    start_date = pd.to_datetime('2023-04-01')  # The start date
    end_date = pd.to_datetime('2023-04-30')  # The end date

    # download_data(variable, lat, lon, start_date)
    download_global_data(variable, start_date)
    preprocess_data(variable, False)
    
    plot_global_data(variable)

    #preprocess_data(variable)
    #plot_global_data(variable)

    months = [('2023-01-01', '2023-01-31'), ('2023-02-01', '2023-02-28')]

    for start_date, end_date in months:
        download_global_data(variable, start_date, end_date)
        preprocess_data(variable, False)
        plot_global_data(variable)"""



if __name__ == "__main__":
    main()
