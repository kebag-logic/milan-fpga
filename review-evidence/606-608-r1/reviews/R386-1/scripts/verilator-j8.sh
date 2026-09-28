#!/bin/sh
# Same pinned Verilator 5.050 wrapper, with the build parallelism capped at 8.
# Place beside a "verilator" wrapper for the pinned 5.050 build; the receipts invoked it as VERILATOR=<this file>.
out=""
for a in "$@"; do :; done
n=$#; i=0; prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"; prev="$a"; i=$((i+1)); [ $i -eq $n ] && break
done
shift $n
exec "$(dirname "$0")/verilator" "$@"
