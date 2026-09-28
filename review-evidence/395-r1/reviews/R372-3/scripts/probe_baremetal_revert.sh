#!/bin/sh
# Mutation probe: restore the round-2 wording in the record and confirm the
# unchanged bare-metal gate refuses it, then restore the exact head bytes.
# Usage: probe_baremetal_revert.sh <clone>
set -u
C=$1
F=docs/findings/COMMERCIAL_TIMING_395.md
cd "$C" || exit 2
grep -n '^Ethernet-to-system crossings remain' "$F" || exit 3
sed -i 's|^Ethernet-to-system crossings remain|Ethernet/sys crossings remain|' "$F"
grep -n '^Ethernet/sys crossings remain' "$F"
timeout 900 python3 -B scripts/check_baremetal_only.py --check
echo "mutant_rc=$?"
git checkout -- "$F"
git diff --quiet && echo "restored=clean"
