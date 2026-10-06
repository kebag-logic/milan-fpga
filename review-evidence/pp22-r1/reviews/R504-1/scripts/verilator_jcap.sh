#!/bin/sh
# Verilator ($VERILATOR_REAL; this review pointed it at the pinned 5.050) with
# the suite Makefiles' "--build -j 0" capped to VJOBS (default 4) compile jobs,
# so concurrent suites stay inside a job budget. Every other argument is passed
# through unchanged.
real=${VERILATOR_REAL:-verilator}
n=$#; prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=${VJOBS:-4}; fi
  set -- "$@" "$a"; prev=$a
done
shift "$n"
exec "$real" "$@"
