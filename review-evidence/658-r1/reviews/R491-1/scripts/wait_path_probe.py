#!/usr/bin/env python3
"""Compare an already queued minimum-length edit with the boot wait pin retained/tied low."""
import argparse, concurrent.futures, json, os, shutil, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("packet",type=Path);p.add_argument("--verilator",required=True);p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
src=a.source.resolve();packet=a.packet.resolve();suite=src/"tb/verilator/r491_wait_probe";suite.mkdir(exist_ok=True)
for name in ("Makefile","sim_nxn.cpp","gen_nvm_window.py","dynmap_probes.vlt"):
 shutil.copyfile(src/"tb/verilator/r491_probe"/name,suite/name)
cpp=(suite/"sim_nxn.cpp").read_text()
def change(old,new):
 global cpp
 assert cpp.count(old)==1,old
 cpp=cpp.replace(old,new)
change("bool r491_watch_ram = false;",'''bool r491_watch_ram = false;
    bool r491_early = false;
    long r491_since_terminal = 0, r491_first_begin = -1;
    void r491_queue_edit() {
        r491_early = true; r491_since_terminal = 0; r491_first_begin = -1;
        std::vector<uint8_t> pl(8,0); pl[1]=0x0e;
        auto f=aecp_request(0x002c,0x4910,pl);
        inject(f.data(),f.size(),1200);
        ck("[R491 wait] queued zero-record ADD stays held before restore",r491_first_begin,-1);
    }
    void r491_get_queued_reply() {
        auto r=await_aecp();
        ck("[R491 wait] queued zero-record ADD succeeds",aecp_status(r),0);
        ck("[R491 wait] queued edit reaches phase zero after the nine-clock drain",r491_first_begin>9,1);
        printf("[R491 wait] first phase-zero request at clock %ld after window closes\\n",r491_first_begin);
        r491_early=false;
    }''')
change("const bool busy = r.milan_datapath__DOT__amap_boot_busy_w;",'''const bool busy = r.milan_datapath__DOT__amap_boot_busy_w;
        if (r491_early && !window) {
            if (r491_was_window) r491_since_terminal=0;
            else ++r491_since_terminal;
            if (r491_first_begin<0 && r.milan_datapath__DOT__pp_amap_edit_req_w
                && r.milan_datapath__DOT__pp_amap_edit_phase_w==0)
                r491_first_begin=r491_since_terminal;
        }''')
change("        start_the_boot_restore_walk();\n        const uint32_t st = axi_read(A_PP_STAT);","        r491_queue_edit();\n        start_the_boot_restore_walk();\n        r491_get_queued_reply();\n        const uint32_t st = axi_read(A_PP_STAT);")
(suite/"sim_nxn.cpp").write_text(cpp)
rtl=(src/"hdl/milan/milan_datapath.sv").read_text();old="assign pp_amap_edit_wait_w = amap_boot_busy_w;";assert rtl.count(old)==1
mut=packet/"scratch/wait-low.sv";mut.write_text(rtl.replace(old,"assign pp_amap_edit_wait_w = 1'b0;"))
env=os.environ.copy();env["TMPDIR"]=str(packet/"scratch");env["MAKEFLAGS"]="--no-print-directory -j16";env["VERILATOR_JOBS"]="4"
subprocess.run(["make","--no-print-directory","-j16","ltn_rom.hex","ucode.hex"],cwd=suite,env=env,check=True,stdout=subprocess.DEVNULL)
def case(tag,dp):
 obj=packet/"scratch"/tag
 for suffix,cmd in [("build",["make","--no-print-directory","-j16","dynmap-build",f"VERILATOR={a.verilator}","VERILATOR_JOBS=4",f"DYNMAP_MDIR={obj}",f"DP_SRC={dp}"]),("run",[str(obj/"Vmilan_dp_dynmap")])]:
  with (packet/"receipts"/(tag+"-"+suffix+".log")).open("w") as log:
   log.write("COMMAND "+json.dumps(cmd)+"\n");log.flush()
   rc=subprocess.run(cmd,cwd=suite,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=580).returncode
  (packet/"receipts"/(tag+"-"+suffix+".rc")).write_text(str(rc)+"\n")
  print(tag,suffix,rc,flush=True)
  if rc:return rc
 return 0
assert 1<=a.jobs<=2
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
 results=list(pool.map(lambda x:case(*x),[("queued-head",src/"hdl/milan/milan_datapath.sv"),("queued-wait-low",mut)]))
raise SystemExit(any(results))
