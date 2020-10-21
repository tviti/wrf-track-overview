#!/usr/bin/env python
from netCDF4 import Dataset
import numpy as np
import argparse
import wrf
import sys

parser = argparse.ArgumentParser(description="Dump argmin(pressure) from a wrfout file, to stdout")
parser.add_argument('wrfout')
parser.add_argument('--start', default=None, type=str)

args = parser.parse_args()

ncfile = Dataset(args.wrfout)

press = wrf.getvar(ncfile, "slp", timeidx=wrf.ALL_TIMES)

if args.start is not None:
    press = press[press["Time"] >= np.datetime64(args.start), :, :]

locs = press.argmin(dim=["south_north", "west_east"])
xlong = press["XLONG"].data[locs["south_north"], locs["west_east"]]
xlat = press["XLAT"].data[locs["south_north"], locs["west_east"]]

for (lon, lat) in zip(xlong, xlat):
    sys.stdout.write("{lon} {lat}\n".format(lat=lat, lon=lon))
