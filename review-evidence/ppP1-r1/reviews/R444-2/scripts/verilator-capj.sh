#!/bin/sh
# Wrapper around the pinned simulator: rewrites "-j 0" (all cores) to "-j $CAPJ"
# so concurrent builds stay within the reviewer's job cap. Set REAL_VERILATOR.
: "${REAL_VERILATOR:?set REAL_VERILATOR to the pinned simulator}"
: "${CAPJ:=6}"
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="$CAPJ"; fi
  set -- "$@" "$a"; prev="$a"
done
shift "$n"
exec "$REAL_VERILATOR" "$@"
