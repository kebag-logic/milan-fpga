#!/bin/sh
# Disposable probe: in a copy of the head tree, delete the default build's
# `run_name_writes(h)` call (the one [[maybe_unused]] now silences if absent)
# and observe which existing gates notice. Usage: 70-drop-call-probe.sh <donor-clone>
# Environment: VERILATOR_BIN_DIR prepended to PATH.
set -u
CLONE=$1
PKT=$(cd "$(dirname "$0")/.." && pwd)
TREE=$PKT/scratch/probe-drop-call
OUT=$PKT/receipts/70-drop-call-probe
rm -rf "$TREE" "$OUT"; mkdir -p "$TREE" "$OUT" "$PKT/scratch/tmp"
export PATH="$VERILATOR_BIN_DIR:$PATH" TMPDIR="$PKT/scratch/tmp"
git -C "$CLONE" archive 83c84b19e09d397ed2eb6f5ace337686ce0ef86b | tar -x -C "$TREE"
F=$TREE/tb/pp_top/sim_main.cpp
grep -c '^  if (!gsi_only) run_name_writes(h);$' "$F" | sed 's/^/call lines before: /' > "$OUT/summary.txt"
sed -i '/^  if (!gsi_only) run_name_writes(h);$/d' "$F"
grep -c 'run_name_writes(h)' "$F" | sed 's/^/call lines after: /' >> "$OUT/summary.txt"
(cd "$TREE/tb/pp_top" && make name-writes) > "$OUT/name-writes.log" 2>&1
echo "make name-writes rc=$?" >> "$OUT/summary.txt"
echo "C++ warnings: $(grep -c 'warning:' "$OUT/name-writes.log")" >> "$OUT/summary.txt"
grep -E '^\[build|^NW:' "$OUT/name-writes.log" >> "$OUT/summary.txt"
python3 "$TREE/tb/pp_top/name_wr_mutant.py" --output "$OUT/mutant" > "$OUT/mutant.stdout" 2>&1
echo "name_wr_mutant.py rc=$?" >> "$OUT/summary.txt"
tail -1 "$OUT/mutant.stdout" >> "$OUT/summary.txt"
sed -i "s#$PKT#<packet>#g; s#$HOME#~#g" "$OUT"/*.log "$OUT"/*.stdout "$OUT"/summary.txt "$OUT"/mutant/*.log 2>/dev/null
cat "$OUT/summary.txt"
