#!/bin/sh
# Verilator wrapper: pins the scoped 5.050 and caps build parallelism at $VJOBS
# (default 8) in place of the Makefiles' "-j 0"; every other flag passes through.
VL=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
J=${VJOBS:-8}
n=$#; i=0; prev=
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=$J; fi
  set -- "$@" "$a"; prev=$a
done
shift $n
exec "$VL" "$@"
