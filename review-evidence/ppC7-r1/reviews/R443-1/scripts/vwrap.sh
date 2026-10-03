#!/bin/sh
# Verilator wrapper: pinned 5.050, with "-j 0" bounded to $VJ jobs (default 4)
PIN=${PIN_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
VJ=${VJ:-4}
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$VJ"; fi
  set -- "$@" "$a"; prev="$a"
done
shift $n
exec "$PIN" "$@"
