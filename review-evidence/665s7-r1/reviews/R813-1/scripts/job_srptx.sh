#!/bin/sh
# make srptx (the three scenarios, graded), then the srptx-plants recipe on its captures
set -u
cd "$1"
make -j3 srptx; rc=$?
echo "make srptx rc=$rc"
python3 -B srptx_plants.py obj_srptx; rc2=$?
echo "srptx_plants rc=$rc2"
[ $rc -eq 0 ] && [ $rc2 -eq 0 ]
