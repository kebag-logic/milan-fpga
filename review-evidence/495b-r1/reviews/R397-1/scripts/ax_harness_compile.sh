#!/bin/bash
# Focused compile probe of the changed AX 1x1 gPTP harness (not a run):
# emit the Verilated C++ for the exact ax1x1gptp command (no --build),
# then syntax-check sim_ax1x1gptp.cpp against it at the derived clock, at
# a planted 50000001 Hz (the static_assert must fire) and with no define
# (the #error must fire). Usage: ax_harness_compile.sh <probe-tree> <mdir>
set -u
T=$1; M=$2
cd "$T/tb/verilator/milan_dp"
make -s -n -B ax1x1gptp VERILATOR_JOBS=4 > "$M.dry" || exit 2
sed -n 1,5p "$M.dry" | bash -e || { echo "generators failed"; exit 2; }
cmd=$(sed -n '6,/sim_ax1x1gptp.cpp/p' "$M.dry" | sed 's/\\$//' | tr '\n' ' ')
cmd=${cmd/--build -j 4/}
cmd=${cmd/--Mdir obj_ax1x1gptp/--Mdir $M}
verilator --version
start=$(date +%s)
eval "$cmd" > "$M.verilator.log" 2>&1; rc=$?
echo "verilator C++ emission rc=$rc elapsed=$(( $(date +%s)-start ))s"; [ $rc -eq 0 ] || { tail -20 "$M.verilator.log"; exit 1; }
root=$(verilator --getenv VERILATOR_ROOT)
inc="-I$M -I$root/include -I$root/include/vltstd -I../../common -I../.."
for d in "-DMILAN_CLK_HZ_TB=50000000" "-DMILAN_CLK_HZ_TB=50000001" ""; do
  g++ -std=c++20 -fsyntax-only -Wall -Wextra $d $inc sim_ax1x1gptp.cpp > "$M.gxx.log" 2>&1; rc=$?
  echo "g++ -fsyntax-only [${d:-no define}] rc=$rc | $(grep -m1 -E 'error' "$M.gxx.log" | cut -c1-220)"
done
