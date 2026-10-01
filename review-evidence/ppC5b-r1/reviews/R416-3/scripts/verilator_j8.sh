#!/bin/sh
# Pinned Verilator 5.050 with its build parallelism capped at 8 (the review's
# job limit): rewrites "-j 0" / "-j0" into "-j 8" and execs the pinned binary.
PINNED=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
n=$#; i=0; skip=0
for a in "$@"; do
  i=$((i+1))
  if [ "$skip" = 1 ]; then skip=0; set -- "$@" 8; continue; fi
  case "$a" in
    -j) skip=1; set -- "$@" -j ;;
    -j0) set -- "$@" -j8 ;;
    *) set -- "$@" "$a" ;;
  esac
done
shift $n
exec "$PINNED" "$@"
