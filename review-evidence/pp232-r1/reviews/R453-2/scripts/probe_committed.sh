#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# probe_committed.sh SRC_TREE CONTROL.sv|none WORK SUITE...
# Copies hdl/, tb/common/ and each named tb/<suite> of SRC_TREE into WORK, plants
# CONTROL.sv as hdl/aecp/KL_aecp_notify.sv (none = the tree's own file), and runs
# `make` in each suite. Prints one line per suite: name rc tally.
set -u
src=$1; ctl=$2; work=$3; shift 3
rm -rf "$work"; mkdir -p "$work/tb"
cp -r "$src/hdl" "$src/scripts" "$work/"
cp -r "$src/tb/common" "$work/tb/"
for s in "$@"; do cp -r "$src/tb/$s" "$work/tb/"; done
[ "$ctl" = none ] || cp "$ctl" "$work/hdl/aecp/KL_aecp_notify.sv"
for s in "$@"; do
  (cd "$work/tb/$s" && make) > "$work/$s.log" 2>&1
  rc=$?
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$work/$s.log" | tail -1)
  echo "$s rc=$rc ${tally:-no-tally}"
  grep -E '^ *FAIL' "$work/$s.log" | head -5 | sed 's/^/    /'
done
