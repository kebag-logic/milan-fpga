#!/bin/sh
# Acquisition sweep: does an engagement's transient drop NCO ticks?
# The slow plan's transient carries the marker LATER than the target (it
# crosses the next tick from an upper-side target); the fast feed's carries
# it EARLIER (it crosses the previous tick from a lower-side target).
# Usage: run_acq_sweep.sh <probe_loop-binary> <out-file>
set -eu
B=${1:?binary}; O=${2:?out}
{
  for s in 1 2 3 4; do for j in 0 1; do
    for l in 0 2056 2060 2064 2067 2070 2075 2080 2082 2083; do echo "acq slow $l $j $s"; done
    for l in 0 2 4 8 12 16 20 24 28; do echo "acq fast $l $j $s"; done
  done; done
} | xargs -P 8 -L 1 "$B" | sort -k2,2 -k4,4 -k3,3n > "$O"
