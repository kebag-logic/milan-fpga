#!/usr/bin/env python3
"""Add observational boot-boundary and CSR probes to a disposable harness copy."""
import argparse, json, os, shutil, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("packet",type=Path);p.add_argument("--verilator",required=True);a=p.parse_args()
src=a.source.resolve();packet=a.packet.resolve();suite=src/"tb/verilator/r491_probe"
suite.mkdir(exist_ok=True)
for name in ("Makefile","sim_nxn.cpp","gen_nvm_window.py","dynmap_probes.vlt"):
 shutil.copyfile(src/"tb/verilator/milan_dp"/name,suite/name)
cpp=(suite/"sim_nxn.cpp").read_text()
def change(old,new):
 global cpp
 assert cpp.count(old)==1,old
 cpp=cpp.replace(old,new)
change("bool audio_held = false;",r'''bool audio_held = false;
    bool r491_watch_ram = false;
    bool r491_was_window = false;
    bool r491_timing = false;
    long r491_ram_edges = 0, r491_ram_bad = 0, r491_overlap = 0;
    long r491_drains = 0, r491_drain_cyc = 0, r491_max_drain = 0;
    void r491_edge() {
        auto& r = *dut->rootp;
        if (!dut->axis_resetn) {
            r491_was_window = true; r491_timing = false; return;
        }
        const bool window = r.milan_datapath__DOT__amap_boot_r;
        const bool busy = r.milan_datapath__DOT__amap_boot_busy_w;
        if (r491_timing) ++r491_drain_cyc;
        if (r491_was_window && !window) {
            r491_timing = true; r491_drain_cyc = 0;
        }
        if (r491_timing && !busy) {
            ++r491_drains;
            r491_max_drain = std::max(r491_max_drain,r491_drain_cyc);
            r491_timing = false;
        }
        r491_was_window = window;
        if (busy && r.milan_datapath__DOT__pp_amap_edit_req_w
                 && r.milan_datapath__DOT__pp_amap_edit_phase_w == 5)
            ++r491_overlap;
        if (!r491_watch_ram) return;
        ++r491_ram_edges;
        if (r.milan_datapath__DOT__amap_in_store_r != 0x8786858483828180ULL
            || r.milan_datapath__DOT__amap_out_owner_v_r != 0xff)
            ++r491_ram_bad;
        for (unsigned c=0;c<8;++c) {
            if (r.milan_datapath__DOT__chan_map_render__DOT__map_r[c+2] != (0x80u|c))
                ++r491_ram_bad;
            if (r.milan_datapath__DOT__chan_map_capture__DOT__map_r[c]
                != (0x1200u | ((c&1u)<<11) | (c>>1))) ++r491_ram_bad;
        }
    }
    void r491_held_csr() {
        for(int i=0;i<64;++i) step();
        ck("[R491 probe] boot writer held before restore",dut->rootp->milan_datapath__DOT__amap_boot_busy_w,1);
        r491_watch_ram=true;
        axi_write(0x900,1);
        for(unsigned side=0;side<2;++side) for(unsigned k=0;k<8;++k) {
            axi_write(0x904,(side<<8)|k); axi_write(0x908,0);
        }
        axi_write(0x900,0);
        for(int i=0;i<16;++i) step();
        r491_watch_ram=false;
        ck("[R491 probe] held CSR attempted writes leave both stores and RAMs unchanged on every sampled edge",r491_ram_bad,0);
        ck("[R491 probe] CSR monitor sampled over 64 active edges",r491_ram_edges>64,1);
    }
    void r491_released_csr() {
        ck("[R491 probe] final sweep and drain ended",dut->rootp->milan_datapath__DOT__amap_boot_busy_w,0);
        axi_write(0x900,1); axi_write(0x904,0); axi_write(0x908,0);
        for(int i=0;i<64;++i) step();
        ck("[R491 probe] post-release CSR removal persists in the protocol map",get_audio_map_page0(0x000e,0).nmappings,3);
        ck("[R491 probe] post-release CSR removal persists in the render RAM",dynmap_ram_rd(2)&0xff,0);
        axi_write(0x900,0);
        ck("[R491 probe] controller ADD after release restores the removed identity",identity_edit(0x002c,0x000e,0,0,0,0),0);
        ck("[R491 probe] post-release controller edit persists",get_audio_map_page0(0x000e,0).nmappings,4);
    }
    void r491_final() {
        ck("[R491 probe] two real restore terminals drained",r491_drains,2);
        ck("[R491 probe] 8-key final sweep drains in nine clocks",r491_max_drain,9);
        ck("[R491 probe] no controller phase-5 beat overlaps the boot writer",r491_overlap,0);
    }''')
change("dut->clk_audio_i = audio_held ? 0 : 1; dut->eval(); }","dut->clk_audio_i = audio_held ? 0 : 1; dut->eval(); r491_edge(); }")
change("        dynmap_stage_an_output_row_in_the_window(fout, in_n, out_n);","        r491_held_csr();\n        dynmap_stage_an_output_row_in_the_window(fout, in_n, out_n);")
change('        dynmap_set_input_channels(fin, 8, 0, "restored 4->8");','        r491_released_csr();\n        dynmap_set_input_channels(fin, 8, 0, "restored 4->8");')
change('        grade_identity_page("restored 4->8 SPI 0", 0x000E, 0, 4);','        grade_identity_page("restored 4->8 SPI 0", 0x000E, 0, 4);\n        r491_final();')
(suite/"sim_nxn.cpp").write_text(cpp)
env=os.environ.copy();env["TMPDIR"]=str(packet/"scratch");env["VERILATOR_JOBS"]="2";env["MAKEFLAGS"]="--no-print-directory -j16"
obj=packet/"scratch/boot-probe-obj"
commands=[("boot-probe-build",["make","--no-print-directory","-j16","dynmap-build",f"VERILATOR={a.verilator}","VERILATOR_JOBS=2",f"DYNMAP_MDIR={obj}"]),
          ("boot-probe-run",[str(obj/"Vmilan_dp_dynmap")])]
for tag,cmd in commands:
 with (packet/"receipts"/(tag+".log")).open("w") as log:
  log.write("COMMAND "+json.dumps(cmd)+"\n");log.flush()
  rc=subprocess.run(cmd,cwd=suite,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=580).returncode
 (packet/"receipts"/(tag+".rc")).write_text(str(rc)+"\n")
 print(tag,rc,flush=True)
 if rc:raise SystemExit(rc)
