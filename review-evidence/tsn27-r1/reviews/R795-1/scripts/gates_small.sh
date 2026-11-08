#!/bin/bash
# Focused metadata gates at the exact head (work directories outside the clone).
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/gates-small; W=$SCR/gates-small; mkdir -p "$O" "$W"; : > "$O/rc.txt"
cd "$REPO"
g() { n=$1; shift; python3 "$@" > "$O/$n.log" 2>&1; echo "$n rc $?" >> "$O/rc.txt"; }
g comments scripts/check_comments.py --selftest --work "$W/comments"
g needles scripts/needle_audit.py --selftest
g traceability scripts/traceability.py --selftest --build "$W/registration" --jobs 2
g test-inventory scripts/test_inventory.py --build "$W/registration" --jobs 2
g privacy scripts/check_privacy.py
g license scripts/check_license.py --selftest
g mutation-controls scripts/mutation_selftest.py --work "$W/mutation-controls" --jobs 2
cat "$O/rc.txt"
