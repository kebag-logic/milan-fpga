"""Wire the real parent allocator adapter into the real donor talker for an isolated experiment.
Usage: python3 run_first_probe.py PARENT_CHECKOUT BUILD_DIRECTORY
No tracked source file is changed. All generated/build files stay in scratch.
"""
from pathlib import Path
import re,subprocess,sys
parent,build=map(lambda p:Path(p).resolve(),sys.argv[1:])
pp=parent/'protocol-processor';out=Path(__file__).resolve().parent
build.mkdir(parents=True,exist_ok=True)
s=(pp/'hdl/acmp/KL_acmp_talker.sv').read_text()
# Keep the upstream testbench ports. Only the allocator inputs consumed by the
# core are rewired; the original external input pins become unused in this harness.
end=re.search(r'\n\);',s).end()
head,body=s[:end],s[end:]
head=head.replace('input  wire', 'input wire block_valid_i,\n    input  wire',1)
inputs={'maap_req_ready_i':'shim_ready_w','maap_rsp_valid_i':'shim_rsp_w','maap_rsp_ok_i':'shim_ok_w','maap_rsp_da_i':'shim_da_w','maap_conflict_valid_i':'shim_conflict_w','maap_conflict_src_i':'shim_src_w'}
for a,b in inputs.items():body=re.sub(r'\b'+a+r'\b',b,body)
shim="""
  wire shim_ready_w,shim_rsp_w,shim_ok_w,shim_conflict_w;
  wire [47:0] shim_da_w;
  wire [SRC_W_C-1:0] shim_src_w;
  KL_pp_maap_shim #(.N_SRC_P(N_STREAM_OUT_P)) allocator_adapter (
    .clk_i(clk_i),.rst_n(rst_n),.blk_addr_i(48'h91e0f0006817),
    .blk_valid_i(block_valid_i),.blk_count_i(8'd2),
    .req_valid_i(maap_req_valid_o),.req_ready_o(shim_ready_w),
    .req_release_i(maap_req_release_o),.req_src_i(maap_req_src_o),
    .rsp_valid_o(shim_rsp_w),.rsp_ok_o(shim_ok_w),.rsp_da_o(shim_da_w),
    .conflict_valid_o(shim_conflict_w),.conflict_src_o(shim_src_w),
    .conflict_ack_i(maap_conflict_ack_o)
  );
"""
(build/'KL_acmp_talker_probe.sv').write_text(head+shim+body)
cmd=['verilator','--cc','--exe','--build','-j','4','--top-module','KL_acmp_talker','-Wno-fatal','--Mdir',str(build/'obj'),'-CFLAGS',f'-std=c++17 -O2 -I{pp}/tb',str(pp/'hdl/common/pp_pkg.sv'),str(pp/'hdl/srp/srp_pkg.sv'),str(parent/'hdl/milan/KL_pp_maap_shim.sv'),str(build/'KL_acmp_talker_probe.sv'),str(out/'reproduce_first_probe.cpp'),'-o','first_probe']
with (build/'build.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=600)
if r.returncode:print((build/'build.log').read_text()[-7000:]);raise SystemExit(r.returncode)
r=subprocess.run([str(build/'obj/first_probe')],capture_output=True,text=True,timeout=180)
print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
(out/'first-probe-results.txt').write_text(r.stdout+r.stderr)
raise SystemExit(r.returncode)
