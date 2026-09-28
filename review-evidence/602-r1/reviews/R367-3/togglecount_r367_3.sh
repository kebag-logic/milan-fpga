#!/bin/sh
# R367-3 witness for PR #603 at 6b2ebd1c: counts every talker-0 mr level change
# between the option-off leg's adjtime and its settime baseline, so the level
# comparison the adjtime check uses can be compared with a toggle count.
#
# Usage: togglecount_r367_3.sh <disposable tree copy> <scratch dir> <receipts dir>
# The tree copy is modified by `git apply` of receipts/togglecount_harness.patch
# (seven added harness lines, no RTL change). PATH must name Verilator 5.050.
set -e
T=$1; S=$2; R=$3
PKT=$(cd "$(dirname "$0")" && pwd)
git -C "$T" apply "$PKT/receipts/togglecount_harness.patch"
make -s -C "$T/tb/verilator/milan_dp" option-off-build OPTOFF_MDIR="$S/obj_TC_clean" VERILATOR_JOBS=8
(cd "$T/tb/verilator/milan_dp" && "$S/obj_TC_clean/Vmilan_dp_sim" > "$R/TC_clean.log" 2>&1 || true)
grep -E 'R367-WITNESS|checks, .* failures' "$R/TC_clean.log"
