#!/bin/sh
# Pinned Verilator 5.050, with the C++ build's "-j 0" capped to "-j ${VL_J:-4}"
# so several builds fit one memory cap. Changes build parallelism only.
VL=${VL_REAL:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
J=${VL_J:-4}
prev=""
for a in "$@"; do
  shift
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$J"; fi
  set -- "$@" "$a"
  prev="$a"
done
exec "$VL" "$@"
