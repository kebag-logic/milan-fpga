#!/bin/bash
# Reviewer wrapper: forwards to the issue-502 pinned 5.050 wrapper, capping build parallelism at 2.
args=(); prev=""
for a in "$@"; do
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then args+=("2"); else args+=("$a"); fi
  prev="$a"
done
exec $VALIDATION_STORAGE/502-manager-r1/pinned-tool-bin/verilator "${args[@]}"
