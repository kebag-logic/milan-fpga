#!/bin/sh
# Usage: ab_integration.sh <clone> <label> <makefile> <outdir>
# Builds the real-datapath MAAP integration exactly as mutants.py's sub-make does
# (make -s -C <suite> -f <makefile> build), under the inherited MAKEFLAGS=w the
# hosted runner hands a `make -C` recipe, then runs the built harness.
set -u
C=$1; L=$2; F=$3; OUT=$4
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
MD=$OUT/../scratch/ab-$L; rm -rf "$MD"
LOG=$OUT/ab-$L.log
{
  echo "label=$L makefile=$F head=$(git -C "$C" rev-parse HEAD) MAKEFLAGS=w"
  env MAKEFLAGS=w make -s -C "$C/tb/verilator/maap" -f "$F" build DP_MDIR="$MD" \
     MAAP_RTL="$C/hdl/ieee1722/maap/KL_maap.sv" VERILATOR="$V" VERILATOR_JOBS=8
  b=$?; echo "build-rc=$b"
  if [ $b -eq 0 ]; then (cd "$MD" && ./maap_integration); echo "run-rc=$?"; fi
} > "$LOG" 2>&1
grep -E 'build-rc|run-rc' "$LOG" | tr '\n' ' ' > "$OUT/ab-$L.rc"
