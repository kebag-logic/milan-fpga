#!/usr/bin/env bash
# Plant each clear-cycle control (from plant.py) into a git-archive copy of the
# candidate and run the committed suites that grade KL_aecp_notify:
# tb/aecp_notify (`make`) and tb/pp_top (`make`, every build and section).
# A control that passes both is not pinned by any committed check.
# Usage: clear_cycle_probe.sh REPO COMMIT CONTROLS_DIR WORK CONTROL...
set -uo pipefail
repo=$1; commit=$2; ctl=$3; work=$4; shift 4
mkdir -p "$work"
for c in "$@"; do
  t="$work/$c"; rm -rf "$t"; mkdir -p "$t"
  git -C "$repo" archive "$commit" | tar -x -C "$t"
  cp "$ctl/$c.sv" "$t/hdl/aecp/KL_aecp_notify.sv"
  for s in aecp_notify pp_top; do
    (cd "$t/tb/$s" && make) >"$work/$c-$s.log" 2>&1
    rc=$?
    tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$work/$c-$s.log" | tail -1)
    echo "$c tb/$s rc=$rc ${tally:-no tally}"
  done
done
