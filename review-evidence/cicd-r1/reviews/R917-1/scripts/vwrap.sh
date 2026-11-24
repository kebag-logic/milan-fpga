#!/bin/sh
# Reviewer wrapper around the pinned Verilator: only rewrites a build-parallelism
# argument "-j 0" (all host CPUs) to "-j $VW_JOBS" so concurrent paired runs stay
# inside the reviewer's CPU/memory share. It changes no other argument.
# Usage: VERILATOR=/path/vwrap.sh make ...   (PINNED_VERILATOR names the real wrapper)
PINNED=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
J=${VW_JOBS:-2}
n=$#
i=0
prev=
for a in "$@"; do
  i=$((i + 1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$J; fi
  set -- "$@" "$a"
  prev=$a
done
shift "$n"
exec "$PINNED" "$@"
