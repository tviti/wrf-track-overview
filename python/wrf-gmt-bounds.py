#!/usr/bin/env python
import xarray as xr
import numpy as np
import argparse
import sys

parser = argparse.ArgumentParser(description="Dump wrfout bounds to stdout")
parser.add_argument('wrfout')

args = parser.parse_args()

ds = xr.open_dataset(args.wrfout)

bottom = np.array((ds["XLONG"][0, 0, :], ds["XLAT"][0, 0, :]))
right = np.array((ds["XLONG"][0, :, -1], ds["XLAT"][0, :, -1]))
top = np.array((ds["XLONG"][0, -1, ::-1], ds["XLAT"][0, -1, ::-1]))
left = np.array((ds["XLONG"][0, ::-1, 0], ds["XLAT"][0, ::-1, 0]))

bounds = np.hstack((bottom, right, top, left))

np.savetxt(sys.stdout, bounds.T)
