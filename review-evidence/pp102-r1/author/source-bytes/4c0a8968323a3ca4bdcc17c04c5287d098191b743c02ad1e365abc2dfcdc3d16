#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run every Verilator suite under tb/ (glob — never a hand-kept list).
# Exit = number of failing suites; exit 90 if any PASSing suite's tally line
# is unreadable (a suite whose check count cannot be read is unproven).

# Strict mode, and it does NOT disarm the sweep. This script's job is to run
# every suite and count the red ones, so each status it is built to survive was
# checked against `set -e`: a failing suite is read by an `if`, and the two
# `[ ... ] && exit` verdicts at the bottom are AND-OR lists - errexit acts on
# neither. The one expected failure `pipefail` WOULD have turned into a crash
# mid-sweep is the tally read, and that line now says so.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1   # every path below is relative to the repo root
fails=0; unreadable=0; total=0

# The uPC map is written down twice (gen_ucode.py's entry points and the
# engine's UPC_*_C localparams) and a mismatch does NOT fail to elaborate: the
# uCPU starts in the ROM fill and answers a well-formed response carrying
# garbage. Gate it before any suite runs, because every suite would pass.
if ! python3 scripts/check_upc_map.py; then
  echo "FAIL check_upc_map (the engine dispatches where no program lives)"
  exit 1
fi

for d in tb/*/; do
  [ -f "$d/Makefile" ] || continue
  name=$(basename "$d")
  log=$(mktemp)
  if (cd "$d" && make) >"$log" 2>&1; then
    # A suite that passed with no tally line is the UNREADABLE verdict below,
    # not a crash: under `pipefail` the empty `grep` is a failing pipeline, so
    # its status is consumed here and the emptiness of $tally is what is read.
    tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1) || tally=""
    if [ -z "$tally" ]; then
      echo "UNREADABLE $name (passed but no tally line)"; unreadable=1
    else
      n=${tally%% *}; total=$((total + n))
      echo "PASS $name ($tally)"
    fi
  else
    echo "FAIL $name"; tail -5 "$log" | sed 's/^/    /'; fails=$((fails + 1))
  fi
  rm -f "$log"
done
echo "suites: $total checks total, $fails failing"
[ "$fails" -gt 0 ] && exit "$fails"
[ "$unreadable" -gt 0 ] && exit 90
exit 0
