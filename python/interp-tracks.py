#!/usr/bin/env python

# Interpolate a set of hurricane tracks that were manually spliced together from
# both hurdat2 and Table 1 of Phadke et. al. 2003. This really isn't going to be
# re-usable, since it was written specifically to upsample a dataset that was
# constructed by hand, and is included solely for posterity (lest the source of
# the 15m upsampled tracks be someday forgotten).

from scipy import interpolate
import pandas as pd
import numpy as np

tracks_name = "../data/tracks.txt"

tracks = pd.read_csv(tracks_name, sep=",", comment="#", index_col="UTC")

tracks.index = pd.to_datetime(tracks.index)
tracks.columns = [col.strip() for col in tracks.columns]  # Strip white space
tracks["src"] = tracks["src"].apply(str.strip)
tracks[["V_max", "p_min"]] = tracks[["V_max", "p_min"]].astype(float)

# Convert V_max from knots to m/s
tracks["V_max"] = tracks["V_max"]*0.51444

# # Remove duplicate entries. Keep Phadke track, and take V & p from hurdat.
i_dupes = tracks.index.duplicated(keep=False)
i_hurdat = tracks["src"] == "hurdat2"
i_phadke = tracks["src"] == "phadke"
tracks.loc[i_dupes & i_phadke, ["V_max", "p_min"]] = tracks[i_dupes & i_hurdat][["V_max", "p_min"]]
tracks = tracks[~(i_dupes & i_hurdat)]

# # Interpolate across the holes in V and p
tracks[["V_max", "p_min"]] = tracks[["V_max", "p_min"]].interpolate(method="spline", order=3)

tracks.index = tracks.index.rename("time")

# Interpolate the tracks to 15 minutes, then save to a text file so we can also
# inspect them using an interactive tool.
tracks_15m = tracks.resample('900S').asfreq()
tracks_15m = tracks_15m.interpolate('time')

tracks_15m[["lon", "lat"]].to_csv('../data/tracks_15m.txt', header=False, index=False, sep=" ")
