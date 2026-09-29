#!/usr/bin/env python3
"""Plant a disposable monitor in a copy's KL_pp_nvm_mgr_arb: count, over a whole
run, every cycle an abort meets a strobe or a WRITE, and print the counts from a
final block (one line per arbiter instance). The arbiter's logic is unchanged.
Usage: instrument_arb.py <tree>"""
import sys, pathlib
f = pathlib.Path(sys.argv[1]) / "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"
s = f.read_text()
anchor = "  assign dbg_drain_o = drain_r;\n"
assert s.count(anchor) == 1
mon = anchor + """
  // ---- reviewer monitor (disposable copy only) ----
  longint unsigned r_iss0_ab0_rd, r_iss0_ab0_wr, r_iss1_ab1_rd, r_iss1_ab1_wr, r_iss0_ab1,
                   r_iss1_ab0, r_ab0_idle, r_ab1_idle, r_ab_wr_owned, r_ab0_owned_rd,
                   r_ab1_owned_rd, r_iss0, r_iss1;
  initial begin
    r_iss0_ab0_rd = 0; r_iss0_ab0_wr = 0; r_iss1_ab1_rd = 0; r_iss1_ab1_wr = 0;
    r_iss0_ab1 = 0; r_iss1_ab0 = 0; r_ab0_idle = 0; r_ab1_idle = 0; r_ab_wr_owned = 0;
    r_ab0_owned_rd = 0; r_ab1_owned_rd = 0; r_iss0 = 0; r_iss1 = 0;
  end
  always_ff @(posedge clk_i) if (rst_n) begin
    if (iss0_w) r_iss0 <= r_iss0 + 1;
    if (iss1_w) r_iss1 <= r_iss1 + 1;
    if (iss0_w && !m0_we_i && m0_abort_i) r_iss0_ab0_rd <= r_iss0_ab0_rd + 1;
    if (iss0_w &&  m0_we_i && m0_abort_i) r_iss0_ab0_wr <= r_iss0_ab0_wr + 1;
    if (iss1_w && !m1_we_i && m1_abort_i) r_iss1_ab1_rd <= r_iss1_ab1_rd + 1;
    if (iss1_w &&  m1_we_i && m1_abort_i) r_iss1_ab1_wr <= r_iss1_ab1_wr + 1;
    if (iss0_w && m1_abort_i) r_iss0_ab1 <= r_iss0_ab1 + 1;
    if (iss1_w && m0_abort_i) r_iss1_ab0 <= r_iss1_ab0 + 1;
    if (m0_abort_i && (own_r != O_M0) && !iss0_w) r_ab0_idle <= r_ab0_idle + 1;
    if (m1_abort_i && (own_r != O_M1) && !iss1_w) r_ab1_idle <= r_ab1_idle + 1;
    if (((own_r == O_M0) && we_r && m0_abort_i) || ((own_r == O_M1) && we_r && m1_abort_i))
      r_ab_wr_owned <= r_ab_wr_owned + 1;
    if ((own_r == O_M0) && !we_r && m0_abort_i) r_ab0_owned_rd <= r_ab0_owned_rd + 1;
    if ((own_r == O_M1) && !we_r && m1_abort_i) r_ab1_owned_rd <= r_ab1_owned_rd + 1;
  end
  final $display("ARBMON %m: iss0 %0d iss1 %0d | issue-cycle arms: m0 READ+abort %0d, m1 READ+abort %0d | abort with a WRITE strobe: m0 %0d m1 %0d | cross: m0 strobe + m1 abort %0d, m1 grant + m0 abort %0d | abort with nothing owned or strobed: m0 %0d m1 %0d | abort while a WRITE is owned %0d | owned-READ aborts: m0 %0d m1 %0d",
                 r_iss0, r_iss1, r_iss0_ab0_rd, r_iss1_ab1_rd, r_iss0_ab0_wr, r_iss1_ab1_wr,
                 r_iss0_ab1, r_iss1_ab0, r_ab0_idle, r_ab1_idle, r_ab_wr_owned, r_ab0_owned_rd,
                 r_ab1_owned_rd);
"""
f.write_text(s.replace(anchor, mon))
print("instrumented", f)
