#!/bin/sh
# Pinned Verilator 5.050 with its --build C++ parallelism capped (default 2),
# so concurrent campaign units stay inside the review unit's memory limit.
# VL_PINNED: path to the pinned verilator; VL_BUILD_JOBS: per-build jobs.
VL_PINNED=${VL_PINNED:-verilator}   # a Verilator 5.050 on PATH by default
J=${VL_BUILD_JOBS:-2}
prev=""
for a in "$@"; do
  shift
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$J"; fi
  set -- "$@" "$a"; prev="$a"
done
exec "$VL_PINNED" "$@"
