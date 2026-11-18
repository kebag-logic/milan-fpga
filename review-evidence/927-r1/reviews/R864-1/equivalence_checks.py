#!/usr/bin/env python3
"""Compare changed modules to base RTL using the existing self-checking stimuli."""
import argparse,os,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("repo",type=Path);p.add_argument("packet",type=Path);a=p.parse_args();a.repo=a.repo.resolve();a.packet=a.packet.resolve()
w=a.packet/"scratch"/"equivalence";w.mkdir(parents=True,exist_ok=True)
os.environ["VERILATOR_JOBS"]="3"
def git(path): return subprocess.check_output(["git","show","70f4056f:"+path],cwd=a.repo,text=True)
def run(cmd,cwd):
 print("COMMAND",*cmd,flush=True); subprocess.run(cmd,cwd=cwd,check=True)
for name,path,suite,target,var in [
 ("KL_mbx_dma","hdl/milan/mailbox/KL_mbx_dma.sv","mbx","run-dma","DMA_RTL"),
 ("KL_aaf_clock_meter","hdl/ieee1722/crf/KL_aaf_clock_meter.sv","aaf_clock_meter","cases","METER_RTL")]:
 src=(a.repo/path).read_text(); base=git(path).replace("module "+name,"module "+name+"_base",1)
 if name=="KL_mbx_dma": base=base.replace("endmodule : KL_mbx_dma","endmodule : KL_mbx_dma_base")
 header=src[src.index("module "+name):src.index("\n);",src.index("module "+name))+3]
 header=re.sub(r"//[^\n]*", "", header)
 ports=re.findall(r"^\s*(input|output)\s+(?:wire|logic)\s*(signed\s*)?(\[[^\n]+?\])?\s*(\w+)\s*[,\n]",header,re.M)
 assert len(ports)>20
 decl=[];conn=[];outputs=[]
 for direction,signed,width,n in ports:
  if direction=="output":
   decl.append(f"wire {signed}{width} review_base_{n};"); conn.append(f".{n}(review_base_{n})"); outputs.append(n)
  else: conn.append(f".{n}({n})")
 params=".ID_W_P(ID_W_P)" if name=="KL_mbx_dma" else ".CLK_FREQ_HZ_P(CLK_FREQ_HZ_P), .N_LISTENERS_P(N_LISTENERS_P)"
 extra="\n"+"\n".join(decl)+f"\n{name}_base #({params}) review_base ("+", ".join(conn)+");\n"
 extra+="always @(negedge clk_i) if (rst_n) begin\n"
 for n in outputs: extra+=f"  if ({n} !== review_base_{n}) $fatal(1, \"BASE DIFFERENCE {name} {n}\");\n"
 if name=="KL_mbx_dma": extra+="  if (ring_addr_r !== (base_r + MBX_ADDR_W_C\x27(index_r & mask_r))) $fatal(1, \"RING INVARIANT\");\n"
 else: extra+="  if (grp_ref_r !== (review_base.grp_ts0_r + 32\x27(review_base.grp_off_r))) $fatal(1, \"GROUP INVARIANT\");\n"
 extra+="end\n"
 changed=src.replace("endmodule",extra+"endmodule",1)
 f=w/(name+"_miter.sv");f.write_text(base+"\n"+changed)
 val=str(f)
 if name=="KL_mbx_dma": val=str(a.repo/"hdl/milan/mailbox/KL_mbx_pkg.sv")+" "+val
 run(["make","-j16",target,f"{var}={val}"],a.repo/"tb/verilator"/suite)
 print("BASE CYCLE COMPARISON PASS",name,"outputs",len(outputs),flush=True)
# FIFO equivalence at two deployed width/depth classes and independent clocks.
base=git("hdl/common/cdc_pair_fifo.sv").replace("module cdc_pair_fifo","module cdc_pair_fifo_base",1)
(w/"fifo_base.sv").write_text(base)
top="""module fifo_compare;
logic wc=0, rc=0, wr=0, rr=0, wen=0, ren=0;
logic [191:0] data=0;
always #5 wc=~wc;
always #7 rc=~rc;
"""
for k,width,depth in [(0,192,2),(1,48,4)]:
 for mode in range(3):
  top+=f"wire f{k}_{mode},e{k}_{mode}; wire [{width-1}:0] d{k}_{mode};\n"
  mod="cdc_pair_fifo_base" if mode==0 else "cdc_pair_fifo"
  param=f".WIDTH({width}), .LOG2D({depth})"+(f", .DIST_RAM_P({mode-1})" if mode else "")
  top+=f"{mod} #({param}) u{k}_{mode} (.wclk_i(wc), .rclk_i(rc), .wrst_n(wr), .rrst_n(rr), .wen_i(wen), .ren_i(ren), .wdata_i(data[{width-1}:0]), .wfull_o(f{k}_{mode}), .rempty_o(e{k}_{mode}), .rdata_o(d{k}_{mode}));\n"
 top+=f"always @(negedge wc or negedge rc) if (wr && rr) begin\n"
 for mode in [1,2]: top+=f"if ({{f{k}_0,e{k}_0,d{k}_0}} !== {{f{k}_{mode},e{k}_{mode},d{k}_{mode}}}) $fatal(1,\"FIFO DIFFERENCE shape {k} mode {mode}\");\n"
 top+="end\n"
top+="""integer n; logic [31:0] rng=32'h9270864;
initial begin
 #101; wr=1; rr=1;
 for(n=0;n<200000;n=n+1) begin
  #2; rng={rng[30:0],rng[31]^rng[21]^rng[1]^rng[0]};
  wen=(n%1000<700) ? rng[0]:0; ren=(n%1000>200) ? rng[1]:0;
  data={rng,~rng,rng^32'h12345678,rng+32'd1,rng+32'd2,rng+32'd3};
  wr=(n%17011>=30); rr=(n%19001>=40);
 end
 $display("FIFO BASE/DEFAULT/DISTRIBUTED EQUIVALENCE PASS: 200000 steps, widths 192/48, depths 4/16, 5:7 clocks, full/empty/stalls/reset"); $finish;
end
endmodule
"""
(w/"fifo_compare.sv").write_text(top)
run([os.environ["VERILATOR"],"--binary","--timing","-j","3","-Wno-fatal","--top-module","fifo_compare","--Mdir",str(w/"fifo_obj"),str(w/"fifo_base.sv"),str(a.repo/"hdl/common/cdc_pair_fifo.sv"),str(w/"fifo_compare.sv")],w)
run([str(w/"fifo_obj/Vfifo_compare")],w)
