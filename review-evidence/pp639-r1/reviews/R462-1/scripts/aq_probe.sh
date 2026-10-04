#!/usr/bin/env bash
# Plant one arm-queue defect in a disposable copy of the head and run tb/pp_top --arm-queue-only.
# usage: aq_probe.sh HEAD_TREE WORK NAME   (NAME in write_refused | wr_wrap_hi)
set -euo pipefail
head=$1; work=$2; name=$3
rm -rf "$work"; mkdir -p "$work/tb"
cp -r "$head/hdl" "$work/hdl"; cp -r "$head/tb/common" "$work/tb/common"; cp -r "$head/tb/pp_top" "$work/tb/pp_top"
rm -rf "$work/tb/pp_top"/obj*
python3 - "$work/hdl/top/protocol_processor_top.sv" "$name" <<'PY'
import sys
p, name = sys.argv[1:3]
edits = {
  "write_refused": ("if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];",
                    "if (armq_in_vld_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];"),
  "wr_wrap_hi": ("assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];",
                 "assign wr_ix_w = (armq_cnt_r[g] >= 3'd3) ? armq_hd_r[g] + 2'd2 : armq_hd_r[g] + armq_cnt_r[g][1:0];"),
}
old, new = edits[name]
s = open(p).read(); assert s.count(old) == 1; open(p, "w").write(s.replace(old, new, 1))
PY
cd "$work/tb/pp_top" && make gsi-build > build.log 2>&1 && ./obj_dir/Vpp_top_sim --arm-queue-only
