#!/bin/sh
# Pinned Verilator 5.050 (same binary as the manager candidate wrapper); rewrites "-j 0" to "-j 8"
# so no build exceeds eight parallel jobs.
VR=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi
  set -- "$@" "$a"; prev="$a"
done
shift $n
exec env VERILATOR_ROOT=$VR/share/verilator $VR/bin/verilator "$@"
