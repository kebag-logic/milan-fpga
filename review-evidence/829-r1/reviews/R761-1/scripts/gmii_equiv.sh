#!/usr/bin/env bash
# gmii_equiv.sh <base tree> <head tree> <work dir>: prove the observer and the ledger at their GMII defaults equal
# the base RTL with ready tied high, and synthesize the observer with the product's registered ready.
# Needs sv2v (SV2V=...) and yosys.
set -u
base=$1 head=$2 w=$3; here=$(cd "$(dirname "$0")" && pwd); mkdir -p "$w"; cd "$w" || exit 3
SV2V=${SV2V:-sv2v}
for side in base head; do
  t=${!side}
  "$SV2V" -w "$side.launch.v" "$t/hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv" "$t/hdl/common/cdc_handshake.sv" "$t/hdl/common/cdc_pulse.sv"
  "$SV2V" -DSYNTHESIS -w "$side.txret.syn.v" "$t/hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
  python3 -I -c "
import re,sys
p=sys.argv[1]; s=open(p).read()
s=re.sub(r'\\\$error\(\"(?:[^\"\\\\\\\\]|\\\\\\\\.)*\"(?:,[^;]*?)?\);',';',s,flags=re.S)
open(p,'w').write(s)" "$side.txret.syn.v"
done
python3 -I -c "
s=open('head.launch.v').read()
s=s.replace('\tgmii_tready_i,\n','',1).replace('input wire gmii_tready_i;','wire gmii_tready_i = 1\'b1;',1)
open('head.launch.tied.v','w').write(s)"
cp "$here/../receipts/yosys/equiv_launch2.ys" "$here/../receipts/yosys/equiv_txret2.ys" .
yosys -q -l equiv_launch2.log equiv_launch2.ys; echo "equiv_launch rc=$?"
yosys -q -l equiv_txret2.log equiv_txret2.ys; echo "equiv_txret rc=$?"
ports="eth_clk_i, eth_rst_n, gmii_tvalid_i, gmii_tdata_i, dp_clk_i, dp_rst_n, rec_valid_o, rec_kind_o, rec_oidx_o, rec_gen_o, rec_type_o, rec_seq_o, rec_delta_o, rec_abort_o, seal_req_i, seal_gen_i, seal_ack_o, dbg_overrun_o"
decl='input eth_clk_i, eth_rst_n, gmii_tvalid_i, dp_clk_i, dp_rst_n, seal_req_i; input [7:0] gmii_tdata_i; output rec_valid_o, rec_kind_o, rec_abort_o, seal_ack_o; output [11:0] rec_oidx_o; output [3:0] rec_gen_o, rec_type_o; output [15:0] rec_seq_o, dbg_overrun_o; output [7:0] rec_delta_o; input [3:0] seal_gen_i;'
inst='KL_gptp_gmii_launch u(.eth_clk_i(eth_clk_i), .eth_rst_n(eth_rst_n), .gmii_tvalid_i(gmii_tvalid_i), .gmii_tready_i(READY), .gmii_tdata_i(gmii_tdata_i), .dp_clk_i(dp_clk_i), .dp_rst_n(dp_rst_n), .rec_valid_o(rec_valid_o), .rec_kind_o(rec_kind_o), .rec_oidx_o(rec_oidx_o), .rec_gen_o(rec_gen_o), .rec_type_o(rec_type_o), .rec_seq_o(rec_seq_o), .rec_delta_o(rec_delta_o), .rec_abort_o(rec_abort_o), .seal_req_i(seal_req_i), .seal_gen_i(seal_gen_i), .seal_ack_o(seal_ack_o), .dbg_overrun_o(dbg_overrun_o));'
echo "module wrap_tied($ports); $decl ${inst/READY/1\'b1} endmodule" > wrap_tied.v
cat > wrap_reg.v <<V
// the product's GMII ready: LiteEthPHYGMIITX's sync assignment, reset to 0 by its own domain
module wrap_reg($ports, phy_rst); $decl input phy_rst; reg ready = 1'b0;
always @(posedge eth_clk_i) if (phy_rst) ready <= 1'b0; else ready <= 1'b1;
${inst/READY/ready} endmodule
V
for shape in "base.launch.v|KL_gptp_gmii_launch|base" "head.launch.v wrap_tied.v|wrap_tied|head_ready_tied_1" "head.launch.v wrap_reg.v|wrap_reg|head_ready_registered"; do
  IFS='|' read -r files top tag <<<"$shape"
  yosys -q -l "synth_$tag.log" -p "read_verilog $files; synth_xilinx -flatten -top $top; tee -o stat_$tag.txt stat -tech xilinx"; echo "synth $tag rc=$?"
done
cat equiv_launch2.status equiv_txret2.status
