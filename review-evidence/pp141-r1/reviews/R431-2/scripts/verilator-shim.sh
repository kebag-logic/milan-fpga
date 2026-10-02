#!/bin/sh
# Reviewer toolchain shim: forwards to the pinned Verilator 5.050 wrapper and
# rewrites a bare "-j 0" (all host cores) into "-j ${VL_J:-2}" so that several
# campaigns can build concurrently inside the review unit's memory cap.
# No source file is edited; the generated model is otherwise identical.
PINNED=${PINNED_VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
n=$#; i=0; prev=""
for a in "$@"; do
  i=$((i+1))
  if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a="${VL_J:-2}"; fi
  set -- "$@" "$a"; prev="$a"
done
shift "$n"
exec "$PINNED" "$@"
