# dminer-abstractor

## context

ERA5 and GCM (IPCC) data are used to predict GSOD data. All years of ERA5 are used to train the model (epoch -> 2015), 
and extra years of GSOD (2015-2018) are used to test the validity of the model.
GCM (IPCC) is a benchmark scientific model of expected world temperatures at a low-resolution that includes many factors.
the goal is essentially to upscale the resolution of the GCM using modern machine-learning techniques.

a part of the works of [the DMiner lab at MSU](https://www.egr.msu.edu/~ptan/dminer/).

---

## this repo

contains code to automate the downloading, preprocessing, and plotting functions of this research endeavor.
it is designed in a semi-modular fashion to allow for future extensibility.

was unfifnished as of August 2023 due to miscommunications (see summary for more)

### ingest_struct

is a class designed to automate the downloading and preprocessing of our data from the three sources.

see code for example usage.

### meta_struct

is a class designed to automate working with our preprocessed data.

currently only capable of plotting things in various ways.

see code for example usage.

---

## getting set up

Have [miniconda](https://docs.conda.io/en/latest/miniconda.html)/[anaconda](https://www.anaconda.com/download/) set up.

VS Code should automatically detect your conda environments. If it doesn't, you might need to set the path to your conda executable in the settings (either by editing the settings.json file directly or through the UI).

To change the Python interpreter for a particular file or project in VS Code:

    Click on the Python version in the bottom-left corner of the status bar, or use the Python:Select Interpreter command from the Command Palette (Ctrl+Shift+P).
    You should see your conda environment in the list of interpreters that VS Code detects automatically.

```py
conda update -n base -c defaults conda
conda env create -f environment.yml
conda init
    # may be needed, afterwards restart terminal
conda activate dminer
pip install cdsapi
    # cdsapi only available on pip
    # restart vscode and select dminer interpreter
```