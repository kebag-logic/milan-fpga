#!/bin/sh
# reviewer wrapper: the pinned Verilator 5.050, with any "-j 0" capped at "-j 8"
R=~/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"; prev="$a"
done
shift $n
exec env VERILATOR_ROOT=$R/usr/share/verilator $R/usr/bin/verilator "$@"
