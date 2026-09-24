#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R276-6 reviewer probe: is_fresh() of both gmstep positive legs inside a
# parent make recipe, under a given GNU make, for the head's runner and for
# the a21cd358 runner (the control: it must report stale under make 4.3).
# Usage: repro_freshness_r276.sh <tree copy> <dir holding the make to test> <verilator>
# Builds obj_gmstep and obj_dir in the tree copy first if they are missing.
set -euo pipefail
TREE=$(cd "$1" && pwd); MAKEDIR=$(cd "$2" && pwd); VL=$3
HERE_S=$(cd "$(dirname "$0")" && pwd)
DP=$TREE/tb/verilator/milan_dp
export PATH="$MAKEDIR:$PATH"
make --version | head -1
if [ ! -x "$DP/obj_gmstep/Vmilan_dp_gmstep" ]; then
  make -s -C "$DP" gmstep-build VERILATOR="$VL" VERILATOR_JOBS=8 >/dev/null
fi
if [ ! -x "$DP/obj_dir/Vmilan_dp_sim" ]; then
  make -s -C "$DP" option-off-build VERILATOR="$VL" VERILATOR_JOBS=8 >/dev/null
fi
OLD=$(mktemp -d)/gmstep_mutants_a21cd358.py
git -C "$TREE" show a21cd3585abdd3cdf4ac5774a048361a66fed043:tb/verilator/milan_dp/gmstep_mutants.py > "$OLD"
rc_head=0; rc_old=0
make -C "$DP" -f Makefile -f "$HERE_S/fresh_probe.mk" fresh-probe \
  PROBE_PY="$HERE_S/fresh_probe.py" RUNNER="$DP/gmstep_mutants.py" LABEL=head || rc_head=$?
make -C "$DP" -f Makefile -f "$HERE_S/fresh_probe.mk" fresh-probe \
  PROBE_PY="$HERE_S/fresh_probe.py" RUNNER="$OLD" LABEL=a21cd358 || rc_old=$?
echo "RESULT head_all_fresh=$([ $rc_head = 0 ] && echo yes || echo no) a21cd358_all_fresh=$([ $rc_old = 0 ] && echo yes || echo no)"
