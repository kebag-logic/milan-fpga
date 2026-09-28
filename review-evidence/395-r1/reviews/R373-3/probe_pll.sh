#!/bin/bash
# Planted-fault probe for the standalone timing-grade entry (S2).
# Usage: probe_pll.sh <disposable clone at head> <litex python>
# Control: unmodified standalone entry passes. Fault: the AX7101 PLL speed
# grade restored to the round-1 literal -2; the standalone entry must fail.
set -u
C="$1"; PY="$2"; cd "$C" || exit 2
python3 -B sw/builder/test_timing_grade.py "$PY" >/tmp/pll.$$ 2>&1; echo "control rc=$?"; tail -1 /tmp/pll.$$
sed -i 's/S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)\[1\]))/S7PLL(speedgrade=-2)/' sw/litex/milan_soc.py
echo "planted-lines=$(grep -c 'S7PLL(speedgrade=-2)' sw/litex/milan_soc.py)"
python3 -B sw/builder/test_timing_grade.py "$PY" >/tmp/pll.$$ 2>&1; echo "fault literal-pll rc=$?"; grep -m3 'AssertionError\|speedgrade' /tmp/pll.$$
git checkout -q -- .
echo "final-status: $(git status --porcelain | wc -l) dirty; head: $(git rev-parse HEAD)"
rm -f /tmp/pll.$$
