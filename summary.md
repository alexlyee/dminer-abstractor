
> This was a place where I (along with the readme) tried to figure out what we really were trying to achieve. It took until the 6th week for the information needed to understand that we in fact only would ever care about one date range to be revealed, which rendered most of my programming up until that point useless to the dminer lab. :(
    > There was a distinct impression before then that abstracting the downloading and preprocessing process was maximally needed.
    > In hindsight, although I asked consistently for more information at meetings, and occasionally via. email, it would have been best if I more strongly said "no, I can't work on this without knowing the full scope of the work." I understand now how easy it is to forget how little another knows or can readily infer about your project, and the importance of insisting on being provided complete contextual information for freelance programming work.
        > I've done a lot of odd programming jobs before, so I know this, but I think it was my first time in a situation where I really had to say "no, this isn't enough information at all." again, despite being pressed for time.

Newer summaries are pasted above. Older ones are kept in case information is lost betwixt summaries. Three dividers will indicate that the below summaries were incorporated in a deliberate way into the above one.

---

The WeatherData class is responsible for handling a single data source and data type.

Multiple WeatherData instances, each representing a different data source/type, are passed into WorkingData in meta_struct.py.

WorkingData will be responsible for calling the download(), preprocess(), and validate() methods on each WeatherData instance it contains.

The verbose parameter for WeatherData methods already defaults to False, so no change needed there.

For now, we are focused only on daily resolution data. So preprocess() logic for monthly averaging is not needed at this time.

main.py should demonstrate creating multiple WeatherData instances and passing them together into a WorkingData instance.

---

The goal of this project is to create a modular framework for downloading, preprocessing, verifying and visualizing weather data from three different sources - ERA5, GCM and GSOD.

The core components are:

    ingest_struct.py - Defines the WeatherData class to abstract data downloading and processing. Currently supports ERA5.

    meta_struct.py - Defines the WorkingData class to handle merging datasets and machine learning in the future.

    main.py - Entry point that imports and utilizes other modules. Constantly evolving.

    data_validation.py - Validates downloaded data. Only ERA5 validation implemented currently.

    data_preprocessor.py - Preprocesses data. Only ERA5 preprocessing implemented currently.

    data_plotter.py - Will handle data visualization. Placeholder functions currently.

    data_merger.py - Expected to merge datasets in the future. Currently empty.

    data_downloader.py - Downloads data. Only ERA5 download implemented currently.

The framework is setup but only ERA5 workflow is fully implemented end-to-end for now. Workflows for GCM, GSOD, merging, ML etc. remain as future development tasks.

---

The project's objective is to abstract the process of downloading, preprocessing, verifying, and visualizing weather data from three different sources, namely the "NCEP/DOE Reanalysis II", "IPCC Global Climate Model Output", and "Global Surface Summary of the Day – GSOD". The project is designed to be modular to facilitate future expansion, such as integrating machine learning models. It comprises the following eight Python files:

1. `ingest_struct.py`: This file defines the `WeatherData` class which is used to manage weather data. The class supports downloading, preprocessing, and validating data from three different sources (ERA5, GCM, and GSOD). The source is determined by a parameter provided during class initialization.

2. `meta_struct.py`: This file defines the `WorkingData` class which serves as a wrapper for `WeatherData` objects. The class supports merging multiple datasets and preparing data for further analysis. However, as of the current version, it appears that the `merger` method doesn't merge the data, but it is expected to handle this in the future. The `WorkingData` class is also expected to handle machine learning operations on the datasets in the future.

3. `main.py`: This file is the entry point of the program. For the purposes of this application, main.py will be constantly changing. For example, it may create an instance of the `WeatherData` class, download the data, preprocesses it, and validate it.

4. `data_validation.py`: This file contains functions for validating the preprocessed data from ERA5, GCM, and GSOD sources. It checks for unique dates, complete dates, missing values, and latitude and longitude range. However, only the validation function for ERA5 data is currently implemented.

5. `data_preprocessor.py`: This file contains functions for preprocessing data from ERA5, GCM, and GSOD sources. The preprocessing steps for ERA5 data include handling missing values, interpolating the data, and converting temperatures from Kelvin to Celsius. For GCM and GSOD data, the preprocessing functions are currently placeholders and return `True`.

6. `data_plotter.py`: This file contains functions for plotting spatial frequency maps and time series data. However, the plotting functions are currently placeholders.

7. `data_merger.py`: This file is currently empty, but it is expected to contain functions for merging data in the future.

8. `data_downloader.py`: This file contains functions for downloading weather data from ERA5, GCM, and GSOD sources. However, only the function for downloading ERA5 data is currently implemented. The functions for GCM and GSOD data are placeholders and return `True`. 

In summary, this program is a framework for downloading, preprocessing, validating, and potentially merging and analyzing weather data from three different sources. However, as of the current version, only the workflows for ERA5 data are fully implemented. The workflows for GCM and GSOD data, data merging, and machine learning operations are planned for future development.