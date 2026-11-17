#!/bin/bash
# Adapted for the round 13 head: the head states 75 ms at 8x8/1if, so the plant replaces 75u (the reviewer's copy, r843_tx_plant_probe.sh, replaces 70u). Nothing else differs.
# Reviewer probe: plant 8x8/1if's CTRL_LOOP_TX_MS at 60 ms (under its 69.84 ms tx row by every source, and under the
# 61 ms that would keep the hold-off's ceil(TX/10) term at 7 cs) in a disposable export of the head, and run the
# graders that hold THE SHAPES' figures. usage: tx_plant_probe.sh CLONE WORKDIR
set -u
C=$(readlink -f "$1"); W=$2
rm -rf "$W"; mkdir -p "$W"; git -C "$C" archive HEAD | tar -x -C "$W"
for s in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  rmdir "$W/$s" 2>/dev/null; ln -s "$C/$s" "$W/$s"; done
cd "$W" || exit 3
python3 - <<'PY'
p = 'sw/firmware/ctrl/loop/ctrl_loop.h'
s = open(p).read()
a = s.index('#elif CTRL_LOOP_SHAPE(1u, 9u, 9u)'); b = s.index('#elif', a + 5)
assert s[a:b].count('#define CTRL_LOOP_TX_MS 75u') == 1
open(p, 'w').write(s[:a] + s[a:b].replace('#define CTRL_LOOP_TX_MS 75u', '#define CTRL_LOOP_TX_MS 60u') + s[b:])
PY
echo "# planted: $(grep -n 'CTRL_LOOP_TX_MS 60u' sw/firmware/ctrl/loop/ctrl_loop.h)"
B=tb/verilator/ctrl_service_budget
for c in "shape_costs.py --check" "flip_grade.py --check --point 8x8/1if" "flip_grade.py --check" "load_grade.py --check" "rows_tiers.py --selftest"; do
  out=$(python3 -B $B/$c 2>&1); rc=$?
  echo "$c rc=$rc: $(printf '%s\n' "$out" | grep -E 'RESULT|planted controls|OVER .*TX' | tail -2 | tr '\n' ' ')"
done
grep -n "REPORTED = \|rowed = \|row_findings(ROOT, rowed" $B/flip_grade.py
