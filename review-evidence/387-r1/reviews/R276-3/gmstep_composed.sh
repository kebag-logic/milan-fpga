#!/usr/bin/env bash
# Build the #387 gmstep leg on the composed tree and run it at several feed
# delays. Usage: gmstep_composed.sh <clone> <verilator> <outdir> <mdir> [DP_SRC] [delays...]
# DP_SRC empty = the tree's own milan_datapath.sv.
set -u
clone=${1:?}; vl=${2:?}; out=${3:?}; mdir=${4:?}; dp=${5:-}; shift 5 || shift $#
delays=${*:-0 12}
mkdir -p "$out"
cd "$clone/tb/verilator/milan_dp" || exit 2
extra=()
[ -n "$dp" ] && extra=(DP_SRC="$dp")
make gmstep-build VERILATOR="$vl" VERILATOR_JOBS=8 GMSTEP_MDIR="$mdir" "${extra[@]}" \
  > "$out/build.log" 2>&1
echo "build exit=$?" | tee -a "$out/summary.txt"
for d in $delays; do
  "$mdir/Vmilan_dp_gmstep" "$mdir/aemi.bin" "$d" > "$out/delay-$d.log" 2>&1
  rc=$?
  line=$(grep -E 'checks|FAIL' "$out/delay-$d.log" | tail -1)
  echo "delay=$d exit=$rc :: $line" | tee -a "$out/summary.txt"
done
