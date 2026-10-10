#!/bin/sh
# Reviewer probe: throttle the engine's result acceptance in a PRIVATE copy
# (bench-only instrumentation of KL_gptp_engine's txts_ready_o) so the egress
# result queue holds two or more results, then run gptp_tables unmutated and
# with the result RAM written at the head instead of the tail.
# Usage: results_depth_probe.sh <repo> <workdir>   (verilator 5.050 on PATH)
set -u
REPO=$1; W=$2
for v in plain write_at_head; do
  T=$W/$v; rm -rf "$T"; mkdir -p "$T"
  for d in hdl gptp-processor/hdl third_party/verilog-axis/rtl tb/verilator/gptp_tables tb/verilator/gptp_shadow tb/common; do
    mkdir -p "$T/$(dirname $d)"; cp -a "$REPO/$d" "$T/$d"
  done
  rm -rf "$T/tb/verilator/gptp_tables/obj_dir"
  python3 -I - "$T" "$v" <<'PY'
import sys
from pathlib import Path
root, v = Path(sys.argv[1]), sys.argv[2]
eng = root / "gptp-processor/hdl/top/KL_gptp_engine.sv"
t = eng.read_text()
old = "  assign txts_ready_o  = !txts_pend_r && rst_n;"
new = ("  logic [14:0] probe_cnt_r = '0;\n"
       "  always_ff @(posedge clk_i) probe_cnt_r <= probe_cnt_r + 15'd1;\n"
       "  assign txts_ready_o  = !txts_pend_r && rst_n && probe_cnt_r[14];")
assert t.count(old) == 1
eng.write_text(t.replace(old, new, 1))
if v == "write_at_head":
    ret = root / "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
    t = ret.read_text()
    old = "      res_ns_r  [res_tail_w] <= res_ns_w;"
    assert t.count(old) == 1
    ret.write_text(t.replace(old, "      res_ns_r  [res_head_r] <= res_ns_w;", 1))
PY
  (cd "$T/tb/verilator/gptp_tables" && make -s run VERILATOR_JOBS=4 > "$W/$v.log" 2>&1; echo "rc=$?" >> "$W/$v.log") &
done
wait
for v in plain write_at_head; do
  echo "== $v"; grep -E "^results:|^ledger:|results lockstep|== gptp_tables|^rc=" "$W/$v.log"
done
