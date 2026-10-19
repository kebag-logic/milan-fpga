#!/usr/bin/env python3
"""Exercise the exact extracted adapter at non-power-of-two and edge indices.
Usage: probe-capture.py SOURCE PACKET COMPILER
This isolates capture/holding semantics, not the complete processor.
"""
import concurrent.futures, hashlib, json, os, pathlib, subprocess, sys
src,packet,compiler=map(pathlib.Path,sys.argv[1:]); packet=packet.resolve()
text=(src/"hdl/top/protocol_processor_top.sv").read_text()
start=text.index("  typedef struct packed {",text.index("// ---- SRP service adapter:"))
end=text.index("  // =========================================================================",start)
adapter=text[start:end]
root=packet/"scratch/capture"; root.mkdir(parents=True,exist_ok=True)
logs=packet/"receipts/capture"; logs.mkdir(parents=True,exist_ok=True)
header=r"""
module capture;
parameter N_STREAM_OUT_P=8;
localparam W=(N_STREAM_OUT_P>1)?$clog2(N_STREAM_OUT_P):1;
logic clk_i=0; always #5 clk_i=~clk_i;
logic rst_n=0;
logic [N_STREAM_OUT_P*16-1:0] cfg_tspec_max_frame_i='0;
logic tkr_gate_open_w=0,tkr_gate_close_w=0;
logic [W-1:0] tkr_gate_src_w=0;
logic [63:0] tkr_gate_sid_w=64'h0123456789abcdef;
logic [47:0] tkr_gate_da_w=48'h91e000000001;
logic [11:0] tkr_gate_vlan_w=2;
logic lstn_act_settle_w=0,lstn_act_teardown_w=0;
logic [7:0] lstn_act_sink_w=0;
logic [63:0] lstn_act_settle_sid_w=0;
logic [47:0] lstn_act_settle_da_w=0;
logic [15:0] lstn_act_settle_vlan_w=0;
logic svc_ready_o,svc_valid_i=0;
logic [2:0] svc_op_i=0;
logic [7:0] svc_index_i=0;
logic [63:0] svc_stream_id_i=0;
logic [47:0] svc_da_i=0;
logic [11:0] svc_vid_i=0;
logic [15:0] svc_max_frame_i=16'hfedc;
logic [1:0] svc_lstn_state_i=0;
logic svc_rsp_valid_o;
logic [1:0] svc_rsp_status_o;
logic [31:0] svc_rsp_data_o;
logic srp_req_valid_w,srp_req_ready_w=0,srp_rsp_valid_w=0;
logic [1:0] srp_rsp_status_w=0;
logic [31:0] srp_rsp_data_w=0;
logic [2:0] srp_req_op_w;
logic [7:0] srp_req_index_w;
logic [63:0] srp_req_sid_w;
logic [47:0] srp_req_da_w;
logic [11:0] srp_req_vid_w;
logic [15:0] srp_req_mfs_w;
logic [1:0] srp_req_lstn_w;
"""
footer=r"""
integer checks=0;
task tick; @(posedge clk_i); #1; endtask
task reset;
 @(negedge clk_i); rst_n=0; tkr_gate_open_w=0; tkr_gate_close_w=0; svc_valid_i=0;
 tick();
 if(st_tk_vld_r || inflight_vld_r || srp_req_valid_w) $fatal(1,"reset did not clear adapter");
 checks++; @(negedge clk_i); rst_n=1;
endtask
initial begin
 for(int close_gate=0;close_gate<2;close_gate++) begin
  for(int s=0;s<N_STREAM_OUT_P;s++) begin
   reset();
   for(int k=0;k<N_STREAM_OUT_P;k++) cfg_tspec_max_frame_i[16*k+:16]=16'(16'h8101+257*k);
   tkr_gate_src_w=W'(s); tkr_gate_open_w=!close_gate; tkr_gate_close_w=1'(close_gate);
   tick();
   if(st_tk_r.mfs!==16'(16'h8101+257*s) || st_tk_r.index!==8'(s) || st_tk_r.op!==3'(close_gate))
    $fatal(1,"capture source=%0d close=%0d actual=%h",s,close_gate,st_tk_r.mfs);
   checks++;
   @(negedge clk_i); tkr_gate_open_w=0;tkr_gate_close_w=0;cfg_tspec_max_frame_i='0;
   tick();
   repeat(3) begin
    tick();
    if(!srp_req_valid_w || srp_req_mfs_w!==16'(16'h8101+257*s) || srp_req_index_w!==8'(s))
     $fatal(1,"request changed under backpressure source=%0d",s);
    checks++;
   end
  end
 end
 reset(); svc_valid_i=1; svc_index_i=8'(N_STREAM_OUT_P-1); tick();
 @(negedge clk_i); svc_valid_i=0; svc_max_frame_i=0; tick(); tick();
 if(srp_req_mfs_w!==16'hfedc || srp_req_index_w!==8'(N_STREAM_OUT_P-1)) $fatal(1,"service scalar capture failed");
 checks++;
 $display("CAPTURE PASS N=%0d checks=%0d",N_STREAM_OUT_P,checks); $finish;
end
endmodule
"""
(root/"capture.sv").write_text(header+adapter+footer)
(logs/"extraction.json").write_text(json.dumps({"source":"hdl/top/protocol_processor_top.sv","first_line":text[:start].count("\n")+1,"last_line":text[:end].count("\n"),"sha256":hashlib.sha256(adapter.encode()).hexdigest()},indent=2)+"\n")
def run(n):
 build=[str(compiler),"--binary","--timing","--top-module","capture","-Wno-fatal","-j","2",f"-GN_STREAM_OUT_P={n}","--Mdir",str(root/f"obj{n}"),str(root/"capture.sv")]
 with (logs/f"n{n}.log").open("w") as f:
  f.write(json.dumps(build)+"\n");f.flush()
  rc=subprocess.run(build,stdout=f,stderr=subprocess.STDOUT).returncode
  if rc==0: rc=subprocess.run([str(root/f"obj{n}/Vcapture")],stdout=f,stderr=subprocess.STDOUT).returncode
 (logs/f"n{n}.rc").write_text(str(rc)+"\n");print("capture",n,"rc",rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,[1,3,8,17]))
sys.exit(bool(any(results)))
