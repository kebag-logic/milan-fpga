#!/bin/sh
# Passage and lock sweeps with the probe_loop binary, at most 8 jobs.
# Usage: run_sweeps.sh <probe_loop-binary> <out-dir>
set -eu
B=${1:?binary}; O=${2:?out}
mkdir -p "$O"
{
  for s in 1 2 3 4; do for j in 0 1; do
    for l in 2045 2050 2055 2060 2063 2066 2070 2075; do echo "passage slow $l $j $s"; done
    for l in 8 13 18 20 23 28 33 38; do echo "passage fast $l $j $s"; done
  done; done
} | xargs -P 8 -L 1 "$B" | sort -k2,2 -k4,4n -k3,3n > "$O/passage_sweep.txt"
{
  for s in 1 2; do for dir in slow fast; do
    for l in 0 1 2 3 4 6 8 12 15 16 17 20 2060 2064 2066 2067 2068 2070 2074 2078 2080 2081 2082 2083; do
      echo "lock $dir $l $s"; done; done; done
} | xargs -P 8 -L 1 "$B" | sort -k2,2 -k3,3 > "$O/lock_sweep.txt"
