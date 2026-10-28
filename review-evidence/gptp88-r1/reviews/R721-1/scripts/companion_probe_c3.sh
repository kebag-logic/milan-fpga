#!/bin/bash
# Probe C3: the datapath Table 5.22 AS_PATH comparator ignores entry 0. usage: <parent> <outdir>
set -u
src="$1"; out="$2"; work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
d="$work/c3"; cp -a "$src" "$d"
python3 -I - "$d/hdl/milan/milan_datapath.sv" <<'PY'
import sys; p = sys.argv[1]; t = open(p).read()
o = "                    && ((asp_live_head_w != gsi_asp_head_q_r)\n"
n = "                    && ((1'b0)\n"
assert t.count(o) == 1, t.count(o); open(p, "w").write(t.replace(o, n))
PY
( cd "$d" && make -C tb/verilator/milan_dp gptp ) > "$out/C3-milan_dp-gptp.log" 2>&1
echo "C3 datapath AS_PATH comparator ignores entry 0: milan_dp gptp rc=$? $(grep -E '^[0-9]+ checks:' "$out/C3-milan_dp-gptp.log" | tail -1)" >> "$out/summary.txt"
grep -E '^FAIL' "$out/C3-milan_dp-gptp.log" >> "$out/summary.txt"
