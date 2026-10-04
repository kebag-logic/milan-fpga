#!/usr/bin/env bash
# Scratch (never committed): the four Vivado calibration anchors, one at a time,
# each holding the host's shared Vivado lock (run_vivado.sh takes it).
set -u
S=$VALIDATION_STORAGE/649-a527
for n in "$@"; do
  d=$S/sweep/vivado/$n
  cp $LANES/649-resmap/syn/resmap/datapath_ooc.tcl "$d/"
  sha256sum "$d/datapath_ooc.tcl" > "$d/tcl.sha256"
  echo "$(date -Is) start $n"
  $S/bin/run_vivado.sh "$d" datapath_ooc.tcl ooc.log "$d/point.txt"
  echo "$(date -Is) done $n rc=$(cat "$d/ooc.log.rc")"
done
echo "$(date -Is) chain complete"
