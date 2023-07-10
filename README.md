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

### ingest_struct

is a class designed to automate the downloading and preprocessing of our data from the three sources.

see code for example usage.

### meta_struct

is a class designed to automate working with our preprocessed data.

currently only capable of plotting things in various ways.

see code for example usage.