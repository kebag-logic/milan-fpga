#!/bin/sh
# reviewer wrapper: pinned Verilator 5.050 with build parallelism capped at 2 (4 concurrent builds = 8 jobs)
args=""
for a in "$@"; do :; done
out=""
prev=""
set -- "$@"
n=$#
i=0
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=2; fi
  set -- "$@" "$a"
  prev="$a"
done
shift $n
exec $VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator "$@"
