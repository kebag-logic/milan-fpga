#!/usr/bin/env python3
"""Generate a Verilator harness that sweeps the stream window's selection and
state over milan_csr and prints each read beside the state that decides it.
Usage: gen_read_table_sim.py <repo-root> <out.cpp>"""
import re
import sys

root, out = sys.argv[1], sys.argv[2]
text = open(f"{root}/hdl/common/csr/milan_csr.sv", encoding="utf-8").read()
text = re.sub(r"//.*", "", text)
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
hdr = text[text.index("module milan_csr"):]
hdr = hdr[:hdr.index(");\n")]
ports = re.findall(r"\binput\s+wire\s*(?:\[[^\]]+\])?\s*(\w+)", hdr)
wide = {"i_acmp_tbl_ctx"}
FIXED = {"aclk", "aresetn", "s_axi_awaddr", "s_axi_awvalid", "s_axi_wdata", "s_axi_wstrb", "s_axi_wvalid",
         "s_axi_bready", "s_axi_araddr", "s_axi_arvalid", "s_axi_rready"}
HIGH = {"i_lctx_rd_valid", "i_tctx_rd_valid", "i_lctx_wr_rdy", "i_tctx_wr_rdy", "i_lctx_snap_ok", "i_tctx_snap_ok"}
init = []
for p in ports:
    if p in FIXED:
        continue
    if p in wide:
        init.append(f"  for (int i = 0; i < 10; i++) t->{p}[i] = 0xA5000000u + i;")
    else:
        init.append(f"  setv(t->{p}, {1 if p in HIGH else 0});")
body = "\n".join(init)
code = r'''#include "Vmilan_csr.h"
#include "Vmilan_csr___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
static Vmilan_csr* t;
template <class T> static void setv(T& v, int on) { v = on; }
template <std::size_t N> static void setv(VlWide<N>& v, int on) { for (std::size_t i = 0; i < N; i++) v[i] = on; }
static void tick() { t->aclk = 0; t->eval(); t->aclk = 1; t->eval(); t->aclk = 0; t->eval(); }
static void ticks(int n) { for (int i = 0; i < n; i++) tick(); }
static uint32_t rd(uint32_t a) {
  t->s_axi_araddr = a; t->s_axi_arvalid = 1; t->s_axi_rready = 0; int g = 0; t->eval();
  while (!t->s_axi_arready) { tick(); t->eval(); if (++g > 2000) return 0xBAD0BAD0u; }
  tick(); t->s_axi_arvalid = 0; t->eval(); g = 0;
  while (!t->s_axi_rvalid) { tick(); t->eval(); if (++g > 2000) return 0xBAD1BAD1u; }
  uint32_t v = t->s_axi_rdata; t->s_axi_rready = 1; t->eval(); tick(); t->s_axi_rready = 0; t->eval(); tick(); return v;
}
static void wr(uint32_t a, uint32_t d) {
  t->s_axi_awaddr = a; t->s_axi_wdata = d; t->s_axi_wstrb = 0xF; t->s_axi_awvalid = 1; t->s_axi_wvalid = 1;
  t->s_axi_bready = 1; int g = 0; t->eval();
  while (!t->s_axi_awready) { tick(); t->eval(); if (++g > 2000) break; }
  tick(); t->s_axi_awvalid = 0; t->s_axi_wvalid = 0; t->eval(); ticks(4);
}
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv); t = new Vmilan_csr;
  t->s_axi_awvalid = 0; t->s_axi_wvalid = 0; t->s_axi_arvalid = 0; t->s_axi_bready = 1; t->s_axi_rready = 0;
@INIT@
  t->i_lctx_rd_data = 0x11111111u; t->i_tctx_rd_data = 0x22222222u; t->i_lwsrp_status = 0x33333333u;
  t->i_srp_ctx_rd_stat = 0x4444u; t->i_srp_ctx_rd_sid = 0x5555555566666666ULL;
  t->aresetn = 0; ticks(8); t->aresetn = 1; ticks(530);
  wr(0x654, 1); wr(0x658, 0x12345678u); wr(0x65C, 0x0000ABCDu);
  static const uint32_t words[] = {0x810, 0x814, 0x818, 0x81C, 0x820, 0x824, 0x828, 0x85C, 0x860, 0x864, 0x868, 0x86C};
  auto* r = t->rootp;
  printf("addr value exists snap dir idx ls0 acmp srp sid dmac ctlr flags tuid mac sel\n");
  for (int lsn0 = 0; lsn0 < 2; lsn0++) for (int dir = 0; dir < 2; dir++) for (int idx = 0; idx < 3; idx++)
  for (int ga = 0; ga < 2; ga++) for (int gs = 0; gs < 2; gs++) for (int snap = 0; snap < 2; snap++) {
    t->i_acmp_tbl_gnt = 0; t->i_srp_ctx_gnt = 0; t->i_lctx_snap_ok = 1; t->i_tctx_snap_ok = 1; ticks(2);
    uint32_t sel = (lsn0 << 9) | (dir << 8) | idx;
    wr(0x800, sel); ticks(8);
    t->i_acmp_tbl_gnt = ga; t->i_srp_ctx_gnt = gs; ticks(8);
    t->i_acmp_tbl_gnt = 0; t->i_srp_ctx_gnt = 0; ticks(2);
    if (snap) { t->i_lctx_snap_ok = 0; t->i_tctx_snap_ok = 0; wr(0x804, 1); ticks(8); }
    for (uint32_t a : words) {
      uint32_t v = rd(a); t->eval();
      printf("%x %08x %d %d %d %d %d %d %d %016llx %012llx %016llx %04x %04x %012llx %03x\n", a, v,
             (int)r->milan_csr__DOT__win_in_range_w, (int)r->milan_csr__DOT__snap_busy_r,
             (int)r->milan_csr__DOT__strm_dir_r, (int)r->milan_csr__DOT__strm_idx_r,
             (int)r->milan_csr__DOT__srp_idx0_ls_w, (int)r->milan_csr__DOT__acmp_fresh_r,
             (int)r->milan_csr__DOT__srp_fresh_r,
             (unsigned long long)r->milan_csr__DOT__acmp_sid_q_r, (unsigned long long)r->milan_csr__DOT__acmp_dmac_q_r,
             (unsigned long long)r->milan_csr__DOT__acmp_ctlr_q_r, (unsigned)r->milan_csr__DOT__acmp_flags_q_r,
             (unsigned)r->milan_csr__DOT__acmp_tuid_q_r, (unsigned long long)r->milan_csr__DOT__mac_wire_w, sel);
    }
    t->i_lctx_snap_ok = 1; t->i_tctx_snap_ok = 1; int g = 0;
    while (r->milan_csr__DOT__snap_busy_r && ++g < 4000) tick();
    ticks(4);
  }
  delete t; return 0;
}
'''
open(out, "w", encoding="utf-8").write(code.replace("@INIT@", body))
