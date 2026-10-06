#!/usr/bin/env python3
"""Exercise verbatim root settle control with a synthetic media-tick source."""
import os, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
R=Path(os.environ.get("REVIEW_REPO", str(Path.cwd())))
S=P/"scratch/settle-probe"; S.mkdir(exist_ok=True)
src=(R/"hdl/milan/milan_datapath.sv").read_text()
start=src.index("  localparam int unsigned SRC_SETTLE_ERR_C")
end=src.index("  end : g_settle_recentre", start)+len("  end : g_settle_recentre")
body=src[start:end]
header="""module settle_probe;
logic axis_clk=0, axis_resetn=0;
logic [15:0] media_clk_src_r=0;
logic follow_sel_r=0, mga_engaged_w=0, mcsrv_locked_w=0;
logic signed [15:0] mga_err_w=0;
logic media_tick_p=1;
logic settle_recentre_p_r;
localparam int unsigned MILAN_CLK_FREQ_HZ=50000000;
localparam int unsigned MCSRV_WIN_LOG2_C=9;
"""
driver=r"""
task tick;
  #1; axis_clk=1; #1; axis_clk=0; #1;
endtask
task wait_pulse(input integer limit);
  integer n;
  n=0;
  while(!settle_recentre_p_r && n<limit) begin tick(); n++; end
  $display("MEASURE source=%0d follow=%0d engaged=%0d locked=%0d ticks_after_arm=%0d pulse=%0d",media_clk_src_r,follow_sel_r,mga_engaged_w,mcsrv_locked_w,n,settle_recentre_p_r);
  if(!settle_recentre_p_r) $fatal(1,"missing bounded pulse");
endtask
initial begin
  tick(); axis_resetn=1;
  // Prime a followed selection, then switch back to INTERNAL with no feed.
  media_clk_src_r=1; follow_sel_r=1; tick();
  media_clk_src_r=0; follow_sel_r=0; tick();
  wait_pulse(2050);
  if(settle_run_ticks_r!=0 || settle_pend_r) $fatal(1,"not cleared");
  tick();
  media_clk_src_r=2; follow_sel_r=1; mcsrv_locked_w=1; tick();
  wait_pulse(196610);
  tick();
  media_clk_src_r=3; mcsrv_locked_w=0; tick();
  wait_pulse(1048578);
  $finish;
end
endmodule
"""
(S/"settle_probe.sv").write_text(header+body+driver)
V=os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
with (P/"receipts/settle-build.log").open("w") as f:
 rc=subprocess.run([V,"--binary","--timing","-j","2","-Wno-fatal","--top-module","settle_probe","settle_probe.sv"],cwd=S,stdout=f,stderr=subprocess.STDOUT).returncode
(P/"receipts/settle-build.rc").write_text(str(rc)+"\n")
if rc: raise SystemExit(rc)
with (P/"receipts/settle-probe.log").open("w") as f:
 rc=subprocess.run(["obj_dir/Vsettle_probe"],cwd=S,stdout=f,stderr=subprocess.STDOUT).returncode
(P/"receipts/settle-probe.rc").write_text(str(rc)+"\n")
print("settle probe",rc)
