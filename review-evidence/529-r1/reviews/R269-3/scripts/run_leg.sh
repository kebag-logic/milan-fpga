#!/usr/bin/env bash
# R269-3: build one milan_dp leg through probe.mk in a disposable tree and run it.
# usage: run_leg.sh <tree> <leg: nxn|nxn8|notify|nxndv|nxn4c> <objdir> <logprefix> [DP_SRC] [NXN_CPP]
# VERILATOR (pinned 5.050) and VERILATOR_JOBS come from the environment.
set -u
tree=$1 leg=$2 mdir=$3 log=$4 dp=${5:-} cpp=${6:-}
: "${VERILATOR:?pinned simulator path required}"
: "${VERILATOR_JOBS:=2}"
cd "$tree/tb/verilator/milan_dp" || exit 90
extra=()
[ -n "$dp" ] && extra+=("DP_SRC=$dp")
[ -n "$cpp" ] && extra+=("NXN_CPP=$cpp")
case $leg in
  nxn) bin=Vmilan_dp_nxn ;;
  nxn8) bin=Vmilan_dp_nxn8 ;;
  notify) bin=Vmilan_dp_notify ;;
  nxndv) bin=Vmilan_dp_nxndv ;;
  nxn4c) bin=Vmilan_dp_nxn4c ;;
  *) echo "unknown leg $leg"; exit 91 ;;
esac
if ! make -f probe.mk "probe-$leg" VERILATOR="$VERILATOR" VERILATOR_JOBS="$VERILATOR_JOBS" \
     MDIR="$mdir" "${extra[@]}" > "$log.build.log" 2>&1; then
  echo "$log BUILD-FAILED"; exit 92
fi
"./$mdir/$bin" > "$log.run.log" 2>&1
rc=$?
tally=$(grep -E '^checks:' "$log.run.log" | tail -1)
echo "$(basename "$log") leg=$leg exit=$rc $tally"
exit 0
