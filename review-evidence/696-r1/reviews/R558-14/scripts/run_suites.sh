#!/bin/bash
# Usage: run_suites.sh <repo> <packet> <job>   (VERILATOR wrapper dir first in PATH)
# Each job writes logs/<job>.log and logs/<job>.rc; build trees go to <packet>/scratch/<job>.
set -u
R=$1; P=$2; J=$3; W=$P/scratch/$J; L=$P/logs/$J
mkdir -p "$W" "$P/scratch/tmp/$J"; export TMPDIR=$P/scratch/tmp/$J VERILATOR=$(command -v verilator)
cd "$R" || exit 9
{
  echo "job=$J head=$(git rev-parse HEAD) verilator=$VERILATOR ($(verilator --version)) start=$(date -Is)"
  case $J in
    maap-all)     make -j16 -C tb/verilator/maap MDIR="$W/unit" VERILATOR="$VERILATOR" all ;;
    integration)  make -j16 -C tb/verilator/maap integration-build DP_MDIR="$W/integration" VERILATOR="$VERILATOR" && (cd "$W/integration" && ./maap_integration) ;;
    coverage)     make -j16 -C tb/verilator/maap coverage COV_MDIR="$W/coverage" VERILATOR="$VERILATOR" ;;
    differential) python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$W/differential" ;;
    *) echo "unknown job"; exit 9 ;;
  esac
  rc=$?; echo "end=$(date -Is) rc=$rc"; exit $rc
} > "$L.log" 2>&1
echo $? > "$L.rc"
