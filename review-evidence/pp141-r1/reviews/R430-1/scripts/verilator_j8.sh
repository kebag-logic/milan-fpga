#!/bin/sh
# Verilator wrapper that caps the C++ build parallelism at 8 jobs: every
# "-j 0" / "-j N" pair handed to Verilator becomes "-j ${VJOBS:-8}".
# REAL_VERILATOR names the Verilator 5.050 entry point to call.
: "${REAL_VERILATOR:?set REAL_VERILATOR to the Verilator 5.050 binary}"
out=""
skip=0
for a in "$@"; do
  if [ "$skip" = 1 ]; then skip=0; set -- "$@" "${VJOBS:-8}"; shift; continue; fi
  if [ "$a" = "-j" ]; then skip=1; set -- "$@" "-j"; shift; continue; fi
  set -- "$@" "$a"; shift
done
exec "$REAL_VERILATOR" "$@"
