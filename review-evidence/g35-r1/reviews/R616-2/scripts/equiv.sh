#!/bin/sh
# Reviewer equivalence probe: base vs head KL_gptp_rx_parser.
#   tied: rx_err_i forced 0 in both (must prove every cell)
#   free: rx_err_i a shared free input (must leave bad_r unproven: non-vacuity)
# usage: equiv.sh <base-tree> <head-tree> <work-dir>
set -eu
base=$1; head=$2; w=$3
mkdir -p "$w"
for t in base head; do
  eval root=\$$t
  sv2v "$root/hdl/ucpu/gptp_ucpu_pkg.sv" "$root/hdl/wire/KL_gptp_rx_parser.sv" \
    | sed "s/\bmodule KL_gptp_rx_parser\b/module parser_$t/" > "$w/parser_$t.v"
done
for mode in tied free; do
  if [ $mode = tied ]; then ERR="1'b0"; PORT=""; else ERR="rx_err_i"; PORT="input wire rx_err_i,"; fi
  for t in base head; do
    cat > "$w/wrap_${t}_$mode.v" <<EOF
module wrap_$t ( input wire clk_i, input wire rst_n, input wire rx_valid_i,
  input wire [7:0] rx_data_i, input wire rx_sof_i, input wire rx_eof_i, $PORT
  input wire [63:0] local_clock_id_i, input wire local_clock_valid_i,
  output wire bank_we_o, output wire [4:0] bank_addr_o, output wire [63:0] bank_wdata_o,
  output wire ev_valid_o, output wire [7:0] ev_code_o, output wire [15:0] ev_seq_o,
  output wire [15:0] drop_cnt_o );
  parser_$t u (.clk_i(clk_i), .rst_n(rst_n), .rx_valid_i(rx_valid_i), .rx_data_i(rx_data_i),
    .rx_sof_i(rx_sof_i), .rx_eof_i(rx_eof_i), .rx_err_i($ERR),
    .local_clock_id_i(local_clock_id_i), .local_clock_valid_i(local_clock_valid_i),
    .bank_we_o(bank_we_o), .bank_addr_o(bank_addr_o), .bank_wdata_o(bank_wdata_o),
    .ev_valid_o(ev_valid_o), .ev_code_o(ev_code_o), .ev_seq_o(ev_seq_o), .drop_cnt_o(drop_cnt_o));
endmodule
EOF
  done
  cat > "$w/equiv_$mode.ys" <<EOF
read_verilog -sv $w/parser_base.v $w/wrap_base_$mode.v
read_verilog -sv $w/parser_head.v $w/wrap_head_$mode.v
proc; opt_clean
flatten wrap_base wrap_head
rename wrap_base gold
rename wrap_head gate
async2sync
equiv_make gold gate equiv
hierarchy -top equiv
equiv_simple -seq 5
equiv_induct -seq 5
equiv_status -assert
EOF
  set +e
  yosys -q -l "$w/equiv_$mode.log" -s "$w/equiv_$mode.ys" >/dev/null 2>&1
  echo "$mode rc=$?"
  set -e
  grep -E "Of those cells|Unproven|Found .* unproven" "$w/equiv_$mode.log" || true
done
