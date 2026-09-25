#!/bin/sh
# Job-capped Verilator wrapper: rewrites the value after every "-j" to
# $VL_JOBS (default 4) and forwards to the pinned Verilator named by $VL_REAL.
# Used because the csr and pp_shadow recipes hard-code "--build -j 0".
: "${VL_REAL:?set VL_REAL to the pinned verilator}"
jobs="${VL_JOBS:-4}"
n=$#
i=0
after_j=0
while [ "$i" -lt "$n" ]; do
  a="$1"; shift; i=$((i + 1))
  if [ "$after_j" = 1 ]; then a="$jobs"; fi
  after_j=0
  [ "$a" = "-j" ] && after_j=1
  set -- "$@" "$a"
done
exec "$VL_REAL" "$@"
