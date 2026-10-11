#!/bin/sh
# pass-through to the pinned 5.050 wrapper; caps the build's -j 0 at 4 jobs
args=""
prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=4; fi
  prev="$a"
  set -- "$@" "$a"
done
shift $(( $# / 2 ))
exec $VALIDATION_TOOLS/pinned-verilator-5.050/verilator "$@"
