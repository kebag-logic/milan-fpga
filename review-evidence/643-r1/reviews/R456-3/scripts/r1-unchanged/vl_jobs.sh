#!/bin/sh
# Pinned Verilator 5.050 with its build parallelism capped: rewrites "-j 0"
# (all cores, from the datapath's print-dp-vflags) to "-j ${VL_JOBS:-8}" so two
# concurrent elaborations stay inside a 16-job budget. Set VL_REAL to the pinned
# verilator launcher.
VL_REAL=${VL_REAL:?set VL_REAL to the pinned verilator}
n=${VL_JOBS:-8}
first=1
for a in "$@"; do
  if [ "$first" = 1 ]; then set --; first=0; fi
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$n; fi
  set -- "$@" "$a"; prev=$a
done
exec "$VL_REAL" "$@"
