#!/usr/bin/env bash
# usage: probe.sh <copy-dir> <name> <logdir> <make targets...>
# builds and runs milan_dp legs in a disposable copy with the pinned Verilator
set -u
c=$1; n=$2; out=$3; shift 3
V=${VERILATOR_PIN:?set VERILATOR_PIN to the pinned Verilator 5.050 binary}
cd "$c" || exit 2
{ date -u +%FT%TZ; git rev-parse HEAD; git status --short --untracked-files=no; "$V" --version; } > "$out/$n.identity" 2>&1
rc=0
for t in "$@"; do
  make -C tb/verilator/milan_dp "$t" VERILATOR="$V" VERILATOR_JOBS="${VJOBS:-3}" > "$out/$n.$t.log" 2>&1
  r=$?; echo "$t $r" >> "$out/$n.rc"; [ $r -ne 0 ] && rc=$r
done
date -u +%FT%TZ >> "$out/$n.identity"
echo "DONE $rc" >> "$out/$n.rc"
