#!/usr/bin/env bash

# Upsample the HURDAT2 + Phadke 2013 mish-mash tracks to 15 min. This was
# originally done while implementing the Phadke 2013 parameteric TC model, and
# is carried forward here just because it looks nicer this way...
cd ./python
./interp-tracks.py
cd ../

#=============================================
# Plot the tracks and WRF domain, using GMT. #
#=============================================

# Dump the NDBC locs to an intermediate file
echo "
-162.00   24.4530 51001
-157.7420 17.0430 51002
-160.6250 19.1750 51003
-152.2550 17.5330 51004
" > ndbc-locs.txt

gmt begin figures/overview pdf # PNG
    gmt set FONT_ANNOT_PRIMARY 6p
    gmt coast -R-180/-130/0/40 -JM3i -Df -Glightbrown -Slightblue -B
    gmt plot ndbc-locs.txt -Si0.25 -Gblack -l"ndbc buoy"
    gmt text ndbc-locs.txt -D0/0.2 -F+f4p,Helvetica
    gmt plot data/tracks_15m.txt -Wthinnest,black -l"HURDAT"

    ./python/get-track.py data/wrfout_d01_1992-09-05_00:00:00 --start 1992-09-09T00:00:00 \
	| gmt plot -Wthinnest,blue -l"WRF-d01a (09-05)"

    ./python/get-track.py data/wrfout_d01_1992-09-09_00:00:00 \
	| gmt plot -Wthinnest,red -l"WRF-d01b (09-09)"

    ./python/wrf-gmt-bounds.py data/wrfout_d01_1992-09-05_00:00:00 \
	| gmt plot -Wthinnest,blue,- -l"d01a"

    ./python/wrf-gmt-bounds.py data/wrfout_d01_1992-09-09_00:00:00 \
	| gmt plot -Wthinnest,red,- -l"d01b"

    gmt legend -DjTR -F+p0.01+gwhite+s1p/-1p/gray50
gmt end

rm -f ndbc-locs.txt
