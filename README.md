# pyDRtest:
## _Data reduction test module_

This is a test module that can perform data reduction in several ways.

## Features

- Can perfrom data reduction on arrays
- Select from several data reduction methods
- Tested with an .abf file using pyabf module


## Installation

```sh
pip install drtest
```

## Usage
Importing:
```sh
import drtest as dr
```
Use the DataAnalysis class for some xdata, ydata:
```sh
da = dr.DataAnalysis(xdata, ydata)
```
Perform data reduction with different methods:
```sh
xdec, ydec = da.data_reduction(method='decimate', reduction_factor=4)
xavr, yavr = da.data_reduction(method='average', reduction_factor=4)
xmin, ymin = da.data_reduction(method='min', reduction_factor=4)
xmax, ymax = da.data_reduction(method='max', reduction_factor=4)
xminmax, yminmax = da.data_reduction(method='min/max', reduction_factor=4)
```

