#!/bin/bash
# R843-3-F2's verification: R843-3's mixed-point probe (record_classes_mixed_probe.py, unchanged) over a harness
# directory. Its first case, 8x8/1if complete beside 1x1/1if's answering-ports leg alone with its accepted
# SET_CONFIGURATION dropped, the completeness map built as main() builds it, must be refused by name at 1x1/1if: both
# findings in that case's own lines. Prints the probe's output; exit 0 only when both are there.
# usage: mixed_probe_gate.sh HARNESS_DIR
set -u
out=$(python3 -I "$(dirname "$0")/record_classes_mixed_probe.py" "$1") || exit 2
echo "$out"
first=$(printf '%s\n' "$out" | sed -n '/^mixed pass/,/^the same pass/p')
printf '%s\n' "$first" | grep -qF 'the pass runs no arm A leg at 1x1/1if' || { echo 'MISSING: no arm A leg at 1x1/1if'; exit 1; }
printf '%s\n' "$first" | grep -qF "the pass is missing arm B's SET_CONFIGURATION: no answering-ports leg at 1x1/1if" || { echo "MISSING: arm B's SET_CONFIGURATION at 1x1/1if"; exit 1; }
echo 'RESULT: PASS: the mixed-point pass is refused by name at 1x1/1if'
