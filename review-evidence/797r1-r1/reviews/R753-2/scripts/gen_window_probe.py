#!/usr/bin/env python3
"""Generate a Verilator harness that drives milan_csr over AXI-Lite and prints
per-word observations. Usage: gen_oracle.py <repo-root> <out.cpp>"""
import re, sys
root, out = sys.argv[1], sys.argv[2]
text = open(f"{root}/hdl/common/csr/milan_csr.sv", encoding="utf-8").read()
text = re.sub(r"//.*", "", text)
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
hdr = text[text.index("module milan_csr"):]
hdr = hdr[:hdr.index(");\n")]
decl = re.findall(r"\binput\s+wire\s*(\[[^\]]+\])?\s*(\w+)", hdr)
ports = [n for _, n in decl]
def width(rng):
    if not rng:
        return 1
    hi = rng.strip()[1:-1].split(":")[0].replace("N_LISTENERS_P", "1").replace("ADDR_WIDTH", "16")
    return eval(hi) + 1
widths = {n: width(r) for r, n in decl}
# Handshake inputs held at fixed values; everything else follows the pattern.
FIXED = {"aclk": None, "aresetn": None, "s_axi_awaddr": None, "s_axi_awvalid": None, "s_axi_wdata": None,
         "s_axi_wstrb": None, "s_axi_wvalid": None, "s_axi_bready": None, "s_axi_araddr": None,
         "s_axi_arvalid": None, "s_axi_rready": None,
         "i_lctx_rd_valid": 1, "i_tctx_rd_valid": 1, "i_lctx_snap_ok": 1, "i_tctx_snap_ok": 1,
         "i_lctx_wr_rdy": 1, "i_tctx_wr_rdy": 1, "i_acmp_tbl_gnt": 0, "i_srp_ctx_gnt": 0,
         "i_srp_ctx_stolen": 0, "i_pp_ack": 0, "i_pp_err": 0, "i_mac_reinit": 0, "i_ptp_tod_valid": 0,
         "i_evt_link_change": 0, "i_evt_rmon_rollover": 0, "i_adp_disc_seen_p": 0, "i_acmp_rest_ack": 0,
         "i_chmap_rd_valid": 0}
lines = ['#include "Vmilan_csr.h"', '#include "verilated.h"', '#include <cstdio>', '#include <cstdint>', '#include <cstring>',
 'static Vmilan_csr* t; static uint64_t ticks=0;',
 'template<class T> static void setv(T& v,int on){ v = on ? (T)~(T)0 : (T)0; }',
 'template<std::size_t N> static void setv(VlWide<N>& v,int on){ for(std::size_t i=0;i<N;i++) v[i]= on?0xFFFFFFFFu:0u; }',
 'static void pattern(int on){']
for p in ports:
    if p in FIXED:
        continue
    w = widths[p]
    if w > 64:
        lines.append(f'  setv(t->{p},on);')
    else:
        mask = (1 << w) - 1
        lines.append(f'  t->{p} = on ? {mask:#x}ULL : 0;')
lines.append('}')
lines.append('static void fixed(){')
for p, v in FIXED.items():
    if v is not None:
        lines.append(f'  t->{p}={v};')
lines.append('}')

lines.append(r'''
static void tick(){ t->aclk=0; t->eval(); t->aclk=1; t->eval(); t->aclk=0; t->eval(); }
static void reset_dut(){ t->aresetn=0; t->s_axi_awvalid=0; t->s_axi_wvalid=0; t->s_axi_arvalid=0; t->s_axi_bready=1; t->s_axi_rready=0;
  for(int i=0;i<8;i++) tick(); t->aresetn=1; for(int i=0;i<530;i++) tick(); }
static uint32_t rd(uint32_t a){ t->s_axi_araddr=a; t->s_axi_arvalid=1; t->s_axi_rready=0; int g=0;
  t->eval(); while(!t->s_axi_arready){ tick(); t->eval(); if(++g>2000) return 0xBAD0BAD0u; }
  tick(); t->s_axi_arvalid=0; t->eval(); g=0; while(!t->s_axi_rvalid){ tick(); t->eval(); if(++g>2000) return 0xBAD1BAD1u; }
  uint32_t v=t->s_axi_rdata; t->s_axi_rready=1; t->eval(); tick(); t->s_axi_rready=0; t->eval(); tick(); return v; }
static void wr(uint32_t a,uint32_t d){ t->s_axi_awaddr=a; t->s_axi_wdata=d; t->s_axi_wstrb=0xF; t->s_axi_awvalid=1; t->s_axi_wvalid=1; t->s_axi_bready=1; int g=0;
  t->eval(); while(!t->s_axi_awready){ tick(); t->eval(); if(++g>2000) break; }
  tick(); t->s_axi_awvalid=0; t->s_axi_wvalid=0; t->eval(); for(int i=0;i<4;i++) tick(); }
int main(int argc,char**argv){ Verilated::commandArgs(argc,argv); t=new Vmilan_csr; fixed(); pattern(0); reset_dut();
  t->i_lctx_rd_data=0x11111111u; t->i_tctx_rd_data=0x22222222u; t->i_lwsrp_status=0x33333333u; t->i_aaf_frames=0;
  wr(0x654,1);
  struct {const char* n; uint32_t sel;} cases[]={{"listener idx0",0x000},{"talker idx0",0x100},{"listener idx1 (no stream)",0x001},{"talker idx1 (no stream)",0x101},{"listener idx0 row bit",0x200}};
  for(auto& c:cases){ wr(0x800,c.sel); for(int i=0;i<8;i++) tick();
    printf("%-28s STRM_SEL=%03x STRMW_CTRL(0x810)=%08x STRMW_SRP(0x85C)=%08x\n",c.n,c.sel,rd(0x810),rd(0x85C)); }
  /* MAC_IFG stored width */
  wr(0x7D8,0x554E4C4Bu); wr(0x104,0xABCDEF12u); for(int i=0;i<40;i++) tick();
  printf("MAC_IFG wrote abcdef12 reads %08x o_mac_ifg=%02x\n",rd(0x104),(unsigned)t->o_mac_ifg);
  delete t; return 0; }
''')
open(out, "w").write("\n".join(lines) + "\n")
