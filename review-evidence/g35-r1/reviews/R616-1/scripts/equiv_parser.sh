#!/bin/sh
# Focused base/head parser identity probe (not the parent bank).
# usage: equiv_parser.sh <base-tree> <head-tree> <workdir> <receipt-dir>
# 1. sv2v each parser (with its package), rename the module.
# 2. Yosys equivalence base vs head, rx_err_i tied 0 (expect all proven)
#    and left free (expect bad_r unproven: the proof is not vacuous).
# 3. Wrapper with rx_err_i tied 0, flatten; opt; opt_clean; write_verilog
#    -noattr: compare the two netlists as text, and their stat.
# 4. gen_gptp_ucode.py output at base and head (ROM image identity).
set -u
base=$1 head=$2 w=$3 out=$4
mkdir -p "$w" "$out"
for t in base head; do
  eval src=\$$t
  sv2v "$src/hdl/ucpu/gptp_ucpu_pkg.sv" "$src/hdl/wire/KL_gptp_rx_parser.sv" \
    | sed "s/^module KL_gptp_rx_parser/module parser_$t/" > "$w/$t.v"
  for mode in tied free; do
    if [ $mode = tied ]; then e="1'b0"; port=""; else e="rx_err_i"; port="input wire rx_err_i,"; fi
    cat > "$w/wrap_${t}_$mode.v" <<EOF
module w_${t}_$mode (input wire clk_i, input wire rst_n, input wire rx_valid_i,
  input wire [7:0] rx_data_i, input wire rx_sof_i, input wire rx_eof_i, $port
  input wire [63:0] local_clock_id_i, input wire local_clock_valid_i,
  output wire bank_we_o, output wire [4:0] bank_addr_o, output wire [63:0] bank_wdata_o,
  output wire ev_valid_o, output wire [7:0] ev_code_o, output wire [15:0] ev_seq_o,
  output wire [15:0] drop_cnt_o);
  parser_$t u (.clk_i(clk_i), .rst_n(rst_n), .rx_valid_i(rx_valid_i), .rx_data_i(rx_data_i),
    .rx_sof_i(rx_sof_i), .rx_eof_i(rx_eof_i), .rx_err_i($e),
    .local_clock_id_i(local_clock_id_i), .local_clock_valid_i(local_clock_valid_i),
    .bank_we_o(bank_we_o), .bank_addr_o(bank_addr_o), .bank_wdata_o(bank_wdata_o),
    .ev_valid_o(ev_valid_o), .ev_code_o(ev_code_o), .ev_seq_o(ev_seq_o), .drop_cnt_o(drop_cnt_o));
endmodule
EOF
  done
done
cd "$w"
for mode in tied free; do
  yosys -p "read_verilog base.v head.v wrap_base_$mode.v wrap_head_$mode.v; hierarchy -check; proc; flatten; opt_clean; async2sync; equiv_make w_base_$mode w_head_$mode eq; hierarchy -top eq; equiv_simple -seq 2; equiv_induct -seq 2; equiv_status" \
    > "$out/equiv_$mode.log" 2>&1
  echo $? > "$out/equiv_$mode.rc"
  grep -E "Of those cells|Unproven" "$out/equiv_$mode.log" > "$out/equiv_$mode.summary"
done
for t in base head; do
  yosys -q -p "read_verilog $t.v wrap_${t}_tied.v; hierarchy -check -top w_${t}_tied; proc; flatten; opt; opt_clean; rename w_${t}_tied w_tied; rename -enumerate; tee -q -o $out/flat_tied_$t.stat stat; write_verilog -noattr $out/flat_tied_$t.v" \
    > "$out/flat_tied_$t.log" 2>&1
  echo $? > "$out/flat_tied_$t.rc"
  yosys -q -p "read_verilog $t.v; hierarchy -check -top parser_$t; proc; opt_clean; tee -q -o $out/hier_free_$t.stat stat" > "$out/hier_free_$t.log" 2>&1
done
if cmp -s "$out/flat_tied_base.v" "$out/flat_tied_head.v"; then echo IDENTICAL; else echo DIFFERENT; fi > "$out/flat_tied_compare.txt"
diff "$out/flat_tied_base.stat" "$out/flat_tied_head.stat" > "$out/flat_tied_stat.diff"; echo "stat diff rc=$?" >> "$out/flat_tied_compare.txt"
grep -E "Number of cells|cells$" "$out/hier_free_base.stat" "$out/hier_free_head.stat" > "$out/hier_free_cells.txt"
diff "$out/hier_free_base.stat" "$out/hier_free_head.stat" > "$out/hier_free_stat.diff"
for t in base head; do
  eval src=\$$t
  python3 "$src/hdl/ucode/gen_gptp_ucode.py" -o "$w/gptp_ucode_$t.hex" > /dev/null 2>&1; echo "$t gen rc=$?"
  (cd "$w" && sha256sum "gptp_ucode_$t.hex")
done > "$out/rom.txt" 2>&1
