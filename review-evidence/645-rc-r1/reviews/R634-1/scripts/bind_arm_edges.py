#!/usr/bin/env python3
"""R634-1 edge probe of the settle recentre's bind arm (milan_datapath.sv), two LOOP streams.

Usage: python3 -I bind_arm_edges.py <milan_datapath.sv> <verilator> <workdir>
Extracts the same region settle_control.py extracts, drives it one media tick per edge,
and prints one line per case: EDGE <name>: <observed> (expect <expected>) PASS|FAIL.
"""
import subprocess, sys
from pathlib import Path
dp, sim, work = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
text = dp.read_text()
b = text.index("  localparam int unsigned SRC_SETTLE_ERR_C")
e = text.index("  end : g_settle_recentre", b) + len("  end : g_settle_recentre")
HEADER = """module edge_probe;
logic axis_clk=0, axis_resetn=0;
logic [15:0] media_clk_src_r=0;
logic follow_sel_r=0, mga_engaged_w=0, mcsrv_locked_w=0;
logic signed [15:0] mga_err_w=0;
logic media_tick_p=1;
logic settle_recentre_p_r;
localparam int unsigned MILAN_CLK_FREQ_HZ=6250000;
localparam int unsigned MCSRV_WIN_LOG2_C=9;
localparam int LB_STREAMS_C=2;
logic lb_tap_tvalid_w=0, lb_tap_tlast_w=0;
logic [3:0] lb_tap_tuser_w=0;
logic [LB_STREAMS_C-1:0] strtbl_bind_rise_w=0, strtbl_bind_fall_w=0;
"""
DRIVER = r"""
integer actions=0, fails=0;
task tick; #1; axis_clk=1; #1; if (settle_recentre_p_r) actions++; axis_clk=0; #1; endtask
task rst; axis_resetn=0; tick(); axis_resetn=1; tick(); endtask
task chk(input string name, input integer got, input integer want);
  $display("EDGE %s: %0d (expect %0d) %s", name, got, want, got==want ? "PASS" : "FAIL");
  if (got!=want) fails++;
endtask
task drain; for (integer i=0; i<1100000 && settle_pend_r; i++) tick(); repeat (3000) tick(); endtask
integer a0;
initial begin
  rst(); drain();
  // 1: rise and the first PDU's tlast in one cycle: that beat cannot end a wait not yet set
  a0=actions; strtbl_bind_rise_w=2'b01; lb_tap_tvalid_w=1; lb_tap_tlast_w=1; lb_tap_tuser_w=0; tick();
  strtbl_bind_rise_w=0; lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  chk("same-cycle rise+tlast arms", settle_pend_r, 0);
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  chk("next tlast then arms", settle_pend_r, 1); drain(); chk("one action", actions-a0, 1);
  // 2: stream 1's bind, stream 0's PDU arms nothing; stream 1's PDU arms
  a0=actions; strtbl_bind_rise_w=2'b10; tick(); strtbl_bind_rise_w=0;
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; lb_tap_tuser_w=0; tick();
  chk("other stream's PDU arms", settle_pend_r, 0);
  lb_tap_tuser_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0; lb_tap_tuser_w=0;
  chk("own stream's PDU arms", settle_pend_r, 1); drain(); chk("one action", actions-a0, 1);
  // 3: both streams bound, both first PDUs: two arms, the second restarts the dwell, one action
  a0=actions; strtbl_bind_rise_w=2'b11; tick(); strtbl_bind_rise_w=0;
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; lb_tap_tuser_w=0; tick(); lb_tap_tvalid_w=0;
  repeat (1000) tick();
  lb_tap_tvalid_w=1; lb_tap_tuser_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0; lb_tap_tuser_w=0;
  begin integer t; t=0; while (settle_pend_r && t<5000) begin tick(); t++; end
    chk("ticks from 2nd arm to fire (dwell restarted)", (t>=2047 && t<=2050), 1); end
  repeat (3000) tick(); chk("one action for two binds", actions-a0, 1);
  // 4: a pending source-change arm, then a bind's first PDU: one action, dwell restarted
  a0=actions; media_clk_src_r=1; tick(); media_clk_src_r=1; repeat (500) tick();
  media_clk_src_r=0; tick(); repeat (500) tick();
  strtbl_bind_rise_w=2'b01; tick(); strtbl_bind_rise_w=0;
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  begin integer t; t=0; while (settle_pend_r && t<5000) begin tick(); t++; end
    chk("bind arm restarts a pending dwell (ticks to fire ~2048)", (t>=2047 && t<=2050), 1); end
  repeat (3000) tick(); chk("pending change + bind = one action", actions-a0, 1);
  // 5: fall in the same cycle as the first tlast (documented: an unbind before the first PDU ends the wait)
  a0=actions; strtbl_bind_rise_w=2'b01; tick(); strtbl_bind_rise_w=0;
  strtbl_bind_fall_w=2'b01; lb_tap_tvalid_w=1; lb_tap_tlast_w=1; tick();
  strtbl_bind_fall_w=0; lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  $display("EDGE info: fall in the tlast's own cycle arms: %0d (the capture un-primes on that flush)", settle_pend_r);
  drain();
  // 6: bind under following, switch to INTERNAL before the first PDU: the source change arms; PDU re-arms
  follow_sel_r=1; media_clk_src_r=1; tick(); drain();
  a0=actions; strtbl_bind_rise_w=2'b01; tick(); strtbl_bind_rise_w=0;
  follow_sel_r=0; media_clk_src_r=0; tick(); repeat (100) tick();
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  begin integer t; t=0; while (settle_pend_r && t<5000) begin tick(); t++; end
    chk("bind under following, PDU after the switch to INTERNAL re-arms", (t>=2047 && t<=2050), 1); end
  repeat (3000) tick(); chk("one action", actions-a0, 1);
  // 7: reset while waiting clears the wait
  strtbl_bind_rise_w=2'b01; tick(); strtbl_bind_rise_w=0; rst();
  lb_tap_tvalid_w=1; lb_tap_tlast_w=1; tick(); lb_tap_tvalid_w=0; lb_tap_tlast_w=0;
  chk("reset clears the wait", settle_pend_r, 0);
  $display("EDGE RESULT %s fails=%0d", fails==0 ? "PASS" : "FAIL", fails);
  $finish;
end
endmodule
"""
work.mkdir(parents=True, exist_ok=True)
(work / "edge_probe.sv").write_text(HEADER + text[b:e] + DRIVER)
rc = subprocess.run([sim, "--binary", "--timing", "-j", "8", "-Wno-fatal", "--top-module", "edge_probe",
                     "edge_probe.sv"], cwd=work, capture_output=True, text=True)
if rc.returncode:
    print(rc.stdout[-3000:], rc.stderr[-3000:]); sys.exit(2)
r = subprocess.run([str(work / "obj_dir/Vedge_probe")], cwd=work, capture_output=True, text=True)
print(r.stdout, end=""); sys.exit(r.returncode or ("EDGE RESULT PASS" not in r.stdout))
