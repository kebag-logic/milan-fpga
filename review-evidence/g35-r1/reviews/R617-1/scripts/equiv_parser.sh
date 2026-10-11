#!/bin/sh
# Focused parser-only equivalence: base vs head KL_gptp_rx_parser, once with
# rx_err_i tied 0 in both (expected: equivalent) and once with it free
# (expected: not fully proven). Usage: equiv_parser.sh <clone> <base-sha> <work> <out>
set -u
C=$1; B=$2; W=$3; O=$4
mkdir -p "$W" "$O"
git -C "$C" show "$B:hdl/ucpu/gptp_ucpu_pkg.sv" > "$W/pkg_base.sv"
git -C "$C" show "$B:hdl/wire/KL_gptp_rx_parser.sv" > "$W/parser_base.sv"
sv2v "$W/pkg_base.sv" "$W/parser_base.sv" | sed 's/module KL_gptp_rx_parser/module p_gold/' > "$W/gold.v"
sv2v "$C/hdl/ucpu/gptp_ucpu_pkg.sv" "$C/hdl/wire/KL_gptp_rx_parser.sv" | sed 's/module KL_gptp_rx_parser/module p_gate/' > "$W/gate.v"
for m in gold gate; do
cat > "$W/wrap_$m.v" <<V
module t_$m(input clk_i, input rst_n, input rx_valid_i, input [7:0] rx_data_i,
  input rx_sof_i, input rx_eof_i, input rx_err_free, input [63:0] local_clock_id_i,
  input local_clock_valid_i, output bank_we_o, output [4:0] bank_addr_o,
  output [63:0] bank_wdata_o, output ev_valid_o, output [7:0] ev_code_o,
  output [15:0] ev_seq_o, output [15:0] drop_cnt_o);
\`ifdef TIE
  wire e = 1'b0;
\`else
  wire e = rx_err_free;
\`endif
  p_$m u(.clk_i(clk_i), .rst_n(rst_n), .rx_valid_i(rx_valid_i), .rx_data_i(rx_data_i),
    .rx_sof_i(rx_sof_i), .rx_eof_i(rx_eof_i), .rx_err_i(e),
    .local_clock_id_i(local_clock_id_i), .local_clock_valid_i(local_clock_valid_i),
    .bank_we_o(bank_we_o), .bank_addr_o(bank_addr_o), .bank_wdata_o(bank_wdata_o),
    .ev_valid_o(ev_valid_o), .ev_code_o(ev_code_o), .ev_seq_o(ev_seq_o),
    .drop_cnt_o(drop_cnt_o));
endmodule
V
done
for mode in tied free; do
  D=""; [ $mode = tied ] && D="-DTIE"
  yosys -q -l "$O/equiv_$mode.log" -p "
    read_verilog $D $W/gold.v $W/gate.v $W/wrap_gold.v $W/wrap_gate.v
    hierarchy -check; proc; flatten; opt_clean
    equiv_make t_gold t_gate eq
    hierarchy -top eq
    equiv_simple -seq 5
    equiv_induct -seq 5
    equiv_status" > /dev/null 2>&1
  echo $? > "$O/equiv_$mode.rc"
done
grep -h -A3 "Found" "$O"/equiv_*.log
