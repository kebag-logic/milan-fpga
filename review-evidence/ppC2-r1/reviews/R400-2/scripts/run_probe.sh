#!/bin/sh
# usage: run_probe.sh CLONE REV WORKDIR VERILATOR LOG [MUTANT_PATCH]
# Exports REV from CLONE into WORKDIR, optionally applies a reviewer mutant
# patch, swaps tb/maap/sim_main.cpp for r400_release_probe.cpp and runs it.
set -eu
clone=$1 rev=$2 work=$3 vl=$4 log=$5 patch=${6:-}
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$work"; mkdir -p "$work"
git -C "$clone" archive "$rev" | tar -x -C "$work"
if [ -n "$patch" ]; then (cd "$work" && patch -p1 --quiet < "$patch"); fi
cp "$here/r400_release_probe.cpp" "$work/tb/maap/sim_main.cpp"
set +e
make -C "$work/tb/maap" run VERILATOR="$vl" > "$log" 2>&1
rc=$?
echo "rc=$rc" >> "$log"
exit $rc
