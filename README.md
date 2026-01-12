# Multistick Temperature Reader

Reads multi-stick temperature log files and returns a calibrated
xarray Dataset with dimensions:

- stick_num
- z
- datetime

Calibration offsets are stored explicitly in the code and embedded
in the output dataset for full reproducibility.

## Installation

Requires:
- numpy
- pandas
- xarray

## Usage

```python
from multistick_reader import read_multistick_data

ds = read_multistick_data("multistick*.log")
print(ds)
