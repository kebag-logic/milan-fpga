#!/bin/sh
# R417-2 probe: remove KL_aecp_engine's gen_g_line_step guard in a scratch
# copy of the head and run the bench's own line guards. Expected: the 580
# case is no longer refused, so line_guards.py fails "line guard 580".
# Usage: probe_line_step_guard.sh <head-export> <scratch-dir> <verilator>
set -u
SRC=$1; WORK=$2; VL=$3
rm -rf "$WORK"; mkdir -p "$WORK"
cp -a "$SRC/hdl" "$SRC/tb" "$WORK/"
python3 - "$WORK/hdl/aecp/KL_aecp_engine.sv" <<'PY'
import sys, re
p = sys.argv[1]; s = open(p).read()
old = re.search(r"  if \(\(LINE_BYTES_P % 8\) != 0\) begin : gen_g_line_step\n.*?\n  end\n", s, re.S)
assert old, "guard not found"
s = s.replace(old.group(0), "")
open(p, "w").write(s)
print("planted: gen_g_line_step removed")
PY
cd "$WORK/tb/pp_top" && make line-guards VERILATOR="$VL"
echo "line-guards rc=$?"
