#!/usr/bin/env bash
# Disposable probe: count, across the FULL default pp_top suite, (a) cycles where a
# name write is presented but the store is not ready (a held NAME_WR), (b) accepted
# non-name store writes, (c) exported pulses. (a)=(b)=0 makes mutants M02-M04 and
# M12 observationally equivalent under the dispatched microcode.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); export PATH=$PK/tools:$PATH
T=$PK/scratch/probe; rm -rf $T; mkdir -p $T/tb
cp -r $PK/scratch/head/hdl $T/; cp -r $PK/scratch/head/tb/common $PK/scratch/head/tb/pp_top $T/tb/
rm -rf $T/tb/pp_top/obj_dir
python3 - "$T/hdl/aecp/KL_aecp_desc_store.sv" <<'P'
import sys
p = sys.argv[1]; s = open(p).read()
anchor = "  assign name_wr_o = take_wr_w && st_name_i;"
assert s.count(anchor) == 1
probe = anchor + """
  // REVIEWER PROBE (disposable)
  longint unsigned prb_held_r, prb_nonname_r, prb_pulse_r, prb_req_r;
  initial begin prb_held_r = 0; prb_nonname_r = 0; prb_pulse_r = 0; prb_req_r = 0; end
  always_ff @(posedge clk_i) begin : prb
    if (st_req_i && st_we_i && st_name_i && !st_ready_o) prb_held_r <= prb_held_r + 1;
    if (st_req_i && st_we_i && st_name_i) prb_req_r <= prb_req_r + 1;
    if (take_wr_w && !st_name_i) prb_nonname_r <= prb_nonname_r + 1;
    if (name_wr_o) prb_pulse_r <= prb_pulse_r + 1;
  end
  final $display("PROBE held_name_write_cycles=%0d name_write_request_cycles=%0d accepted_nonname_writes=%0d name_wr_pulses=%0d",
                 prb_held_r, prb_req_r, prb_nonname_r, prb_pulse_r);
"""
open(p, "w").write(s.replace(anchor, probe))
P
cd $T/tb/pp_top && make gsi-build > $PK/receipts/06-probe-build.log 2>&1; echo "build rc=$?"
./obj_dir/Vpp_top_sim > $PK/receipts/06-probe-full.log 2>&1; echo "full default run rc=$?"
grep -E '^PROBE|\[build default' $PK/receipts/06-probe-full.log
rm -rf $T/tb/pp_top/obj_dir
