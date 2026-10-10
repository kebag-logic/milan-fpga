#!/usr/bin/env bash
# Focused composition suites on a scratch copy of the candidate tree.
# Usage: run_suites.sh <scratch-candidate-copy> <verilator> <out-dir> <maap|render>
# Writes <out-dir>/<suite>.log and <out-dir>/<suite>.rc.
set -u
tree=$1; vl=$2; out=$3; which=$4
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
case "$which" in
  maap)
    # The unit harness, then the real-datapath CSR-to-MAAP build and run.
    ( set -e
      env -u MAKEFLAGS make -C "$tree/tb/verilator/maap" run VERILATOR="$vl" VERILATOR_JOBS=4
      env -u MAKEFLAGS make -C "$tree/tb/verilator/maap" integration-build VERILATOR="$vl" VERILATOR_JOBS=4
      cd "$tree/tb/verilator/maap/obj_integration" && ./maap_integration
    ) >"$out/maap.log" 2>&1
    echo $? >"$out/maap.rc" ;;
  render)
    # The suite dev's #701/#657 changed, built over this PR's KL_maap; outer make serial.
    env -u MAKEFLAGS make -C "$tree/tb/verilator/milan_dp_render" VERILATOR="$vl" VERILATOR_JOBS=4 \
      >"$out/render.log" 2>&1
    echo $? >"$out/render.rc" ;;
esac
