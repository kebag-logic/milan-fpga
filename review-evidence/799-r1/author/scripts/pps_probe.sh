#!/usr/bin/env bash
# #799 / #790: the pp_shadow [GSI] group against a planted processor, in a scratch clone at <rev> (never the lane,
# never pushed). The clone's protocol-processor checkout gets the pass-through of processor #206's settled gate
# (`if (!gsi_settled_w) begin` -> `if (1'b0) begin`, exactly one site), then pp_shadow's base leg is built and run.
# The planted run must fail, and its failures must be [GSI] lines of the stale case.
# usage: pps_probe.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692; C=$X/clone-ppsprobe-${rev:0:8}; O=$X/r/ppsprobe-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
P=$C/protocol-processor
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || { echo "processor toplevel mismatch" > "$O/verdict.txt"; exit 2; }
git -C "$P" remote get-url origin > "$O/processor-origin.txt"
git -C "$P" rev-parse HEAD > "$O/processor-head.txt"
python3 - "$P/hdl/top/protocol_processor_top.sv" > "$O/plant.txt" <<'PY' || exit 2
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
old = "      if (!gsi_settled_w) begin"
assert s.count(old) == 1, s.count(old)
p.write_text(s.replace(old, "      if (1'b0) begin"))
print("planted: '" + old.strip() + "' -> 'if (1'b0) begin' (1 site)")
PY
git -C "$P" diff > "$O/plant.diff"
source "$D/env.sh"
cd "$C/tb/verilator/pp_shadow" || exit 2
make -j8 build-base > "$O/build.log" 2>&1; echo "build rc=$?" > "$O/rc.txt"
make exec-base > "$O/run.log" 2>&1; echo "run rc=$?" >> "$O/rc.txt"
grep -E '^\s*\[FAIL\]' "$O/run.log" > "$O/fail-lines.txt"
tail -2 "$O/run.log" >> "$O/rc.txt"
git -C "$P" checkout -- hdl/top/protocol_processor_top.sv
git -C "$P" status --porcelain > "$O/processor-status-after.txt"
echo PROBE-DONE >> "$O/rc.txt"
