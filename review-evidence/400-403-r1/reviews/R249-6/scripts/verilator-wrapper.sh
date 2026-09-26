#!/bin/sh
# Pinned Verilator 5.050 ($PINNED_VERILATOR) with "-j 0" capped at REVIEW_JOBS (default 6) so
# builds stay within the review's parallel-job budget.
jobs=${REVIEW_JOBS:-6}
prev=
for a in "$@"; do
  shift
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$jobs; fi
  set -- "$@" "$a"
  prev=$a
done
exec "${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned Verilator 5.050 executable}" "$@"
