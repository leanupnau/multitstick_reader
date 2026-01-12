import numpy as np
import pandas as pd
import xarray as xr
import glob
import re


def apply_temperature_calibration(ds, T_diff):
    """
    Apply per-stick, per-depth temperature calibration.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset containing T_deg(stick_num, z, datetime)
    T_diff : xarray.DataArray
        Calibration offsets with dims (stick_num, z)

    Returns
    -------
    xarray.Dataset
        Calibrated dataset with T_raw, T_diff, and calibrated T_deg
    """
    if "T_deg" not in ds:
        raise ValueError("Dataset does not contain 'T_deg'")

    if not set(ds.stick_num.values).issubset(set(T_diff.stick_num.values)):
        raise ValueError("stick_num mismatch between data and calibration")

    if not np.allclose(ds.z.values, T_diff.z.values):
        raise ValueError("z-coordinates do not match calibration table")

    ds = ds.copy()
    ds["T_raw"] = ds["T_deg"]
    ds["T_diff"] = T_diff
    ds["T_deg"] = ds["T_raw"] - ds["T_diff"]

    ds["T_deg"].attrs.update({
        "calibrated": True,
        "calibration": "Subtracted T_diff(stick_num, z)",
        "units": "degC",
    })

    return ds


# ---- Calibration table (visible & compact) -------------------------

T_diff = xr.DataArray(
    data=np.array([
        [ 0.01688127,  0.04002413,  0.09416699,  0.20345270,  0.10845270,  0.13288127,  0.11530985,  0.16573842],
        [ 0.21075705,  0.01467009,  0.14032227,  0.04901792,  0.11017734, -0.01489512,  0.05655415,  0.04075705],
        [ 0.17162662,  0.18032227,  0.17162662,  0.05858314,  0.11945270,  0.11930778,  0.77162662,  0.09003241],
        [-0.03402556,  0.11640922,  0.11438024,  0.04249618,  0.04611937,  0.16553966,  0.02945270,  0.06162662],
        [ 0.10829328,  0.11742372, -0.01054730,  0.08800343,  0.16206140,  0.11640922,  0.04075705,  0.04336575],
    ]),
    dims=("stick_num", "z"),
    coords={
        "stick_num": [0, 1, 2, 3, 4],
        "z": [0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14],
    },
    name="T_diff",
)

#-------Read Data -------------------------

def read_multistick_data(file_path_pattern):
    """
    Read multi-stick log files, validate format, apply calibration,
    and return an xarray Dataset.

    Parameters
    ----------
    file_path_pattern : str
        Glob pattern for log files (e.g. 'multistick*.log')

    Returns
    -------
    xarray.Dataset
        Dataset with dimensions (stick_num, z, datetime)
    """
    ...
    ds_multisticks = apply_temperature_calibration(ds_multisticks, T_diff)
    return ds_multisticks
