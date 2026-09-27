#!/usr/bin/env bash
# Bound the logic cone of the #602 RTL edit: synth_xilinx -flatten of
# KL_media_clock_restart plus the exact restart expression, with and without
# the PHC re-base OR term, at N contexts. usage: cone_synth.sh TREE OUTDIR
set -euo pipefail
TREE="$(cd "$1" && pwd)"; OUT="$2"; mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
ENG="$TREE/hdl/ieee1722/avtp/KL_media_clock_restart.sv"
for n in 2 9; do for v in before after; do
  if [ "$v" = before ]; then EXPR="(sel & ((lk_q & ~locked) | mr_tog)) | (adj | load)";
  else EXPR="sel & ((lk_q & ~locked) | mr_tog)"; fi
  W="$OUT/w_${v}_$n.sv"
  cat > "$W" <<SV
\`default_nettype none
module cone_w (input wire clk, input wire rst_n, input wire sel, input wire lk_q,
  input wire locked, input wire mr_tog, input wire adj, input wire load,
  input wire [15:0] src, input wire [$n-1:0] strm, input wire fp,
  input wire [3:0] fidx, input wire fmr, output logic [$n-1:0] mr);
  wire rq = $EXPR;
  KL_media_clock_restart #(.N_TALKERS_P($n)) u (.clk_i(clk), .rst_n(rst_n),
    .restart_p_i(rq), .clk_src_i(src), .streaming_i(strm), .frame_p_i(fp),
    .frame_idx_i(fidx), .frame_mr_i(fmr), .mr_o(mr));
endmodule
SV
  sv2v --top=cone_w "$ENG" "$W" > "$OUT/w_${v}_$n.v"
  yosys -q -p "read_verilog $OUT/w_${v}_$n.v; synth_xilinx -family xc7 -top cone_w -flatten; tee -o $OUT/stat_${v}_$n.txt stat" > "$OUT/yosys_${v}_$n.log" 2>&1
  L=$(awk '/LUT[1-6]$/{s+=$1} END{print s+0}' "$OUT/stat_${v}_$n.txt")
  F=$(awk '/FD[CPRS]E$/{s+=$1} END{print s+0}' "$OUT/stat_${v}_$n.txt")
  echo "N=$n $v LUT=$L FF=$F"
done; done
