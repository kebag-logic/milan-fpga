#!/usr/bin/env python3
"""Insert a seam trace into a disposable copy of KL_gptp_gmii_launch.sv.
usage: instrument_seam.py <file> <fault:0|1>"""
import sys
path, fault = sys.argv[1], sys.argv[2] == "1"
text = open(path, encoding="utf-8").read()
probe = '''
  // REVIEW PROBE: seam trace of the first attempted frames after the seal
  integer rv_cyc = 0, rv_frames = 0; logic rv_open = 0;
  always @(posedge eth_clk_i) if (eth_rst_n) begin
    if (gmii_tvalid_i) begin
      if (!rv_open) begin rv_frames = rv_frames + 1; rv_cyc = 0; rv_open = 1; end
      else rv_cyc = rv_cyc + 1;
      if (rv_frames <= 1 && rv_cyc < 28)
        $display("SEAM cyc=%0d v=%b r=%b d=%02x nidx=%0d inf=%b chk=%b cand_r=%b cand_w=%b", rv_cyc, gmii_tvalid_i, gmii_tready_i, gmii_tdata_i, nidx_w, inf_r, chk_w, cand_r, cand_w);
    end else if (close_w) rv_open = 0;
  end
endmodule : KL_gptp_gmii_launch'''
anchor = "endmodule : KL_gptp_gmii_launch"
assert text.count(anchor) == 1
text = text.replace(anchor, probe)
if fault:
    gate = "        if (gmii_tready_i) begin\n"
    assert text.count(gate) == 1
    text = text.replace(gate, "        if (1'b1) begin // REVIEW FAULT: the base observer's one octet per clock\n")
open(path, "w", encoding="utf-8").write(text)
