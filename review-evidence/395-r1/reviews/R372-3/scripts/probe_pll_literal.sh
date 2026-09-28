#!/bin/sh
# Mutation probe: restore a literal AX7101 PLL speed grade and confirm the
# standalone timing-grade entry now fails; then restore the exact head bytes.
# Usage: probe_pll_literal.sh <clone> <litex-python>
set -u
C=$1; LP=$2
F=sw/litex/milan_soc.py
cd "$C" || exit 2
grep -n 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)\[1\]))' "$F" || exit 3
sed -i 's|S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)\[1\]))|S7PLL(speedgrade=-2)|' "$F"
grep -n 'S7PLL(speedgrade=-2)' "$F"
timeout 600 python3 -B sw/builder/test_timing_grade.py "$LP"
echo "mutant_rc=$?"
git checkout -- "$F"
git diff --quiet && echo "restored=clean"
timeout 600 python3 -B sw/builder/test_timing_grade.py "$LP" >/dev/null 2>&1
echo "restored_rc=$?"
