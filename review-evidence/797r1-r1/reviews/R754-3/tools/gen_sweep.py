#!/usr/bin/env python3
"""Generate a Verilator harness that sweeps every selection and window state over
milan_csr and prints each read of every read-table word with its deciding state.
Usage: gen_sweep.py <repo-root> <out.cpp>"""
import re
import sys

root, out = sys.argv[1], sys.argv[2]
text = open(f"{root}/hdl/common/csr/milan_csr.sv", encoding="utf-8").read()
text = re.sub(r"//.*", "", text)
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
hdr = text[text.index("module milan_csr"):]
hdr = hdr[hdr.index(") ("):] if ") (" in hdr else hdr
hdr = hdr[:hdr.index(");\n")]
ports = re.findall(r"\binput\s+wire\s*(?:\[[^\]]+\])?\s*(\w+)", hdr)
AXI = {"aclk", "aresetn", "s_axi_awaddr", "s_axi_awvalid", "s_axi_wdata", "s_axi_wstrb", "s_axi_wvalid",
       "s_axi_bready", "s_axi_araddr", "s_axi_arvalid", "s_axi_rready"}
HIGH = {"i_lctx_rd_valid", "i_tctx_rd_valid", "i_lctx_wr_rdy", "i_tctx_wr_rdy", "i_lctx_snap_ok", "i_tctx_snap_ok"}
init = "\n".join(f"  setv(t->{p}, {1 if p in HIGH else 0});" for p in ports if p not in AXI)
code = r'''#include "Vmilan_csr.h"
#include "Vmilan_csr___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
static Vmilan_csr* t;
template <class T> static void setv(T& v, uint64_t on) { v = on; }
template <std::size_t N> static void setv(VlWide<N>& v, uint64_t on) { for (std::size_t i = 0; i < N; i++) v[i] = (uint32_t)on; }
template <class T> static void word(T& v, int i, uint32_t x) { uint64_t u = v; u &= ~(0xFFFFFFFFull << (i*32)); u |= (uint64_t)x << (i*32); v = u; }
template <std::size_t N> static void word(VlWide<N>& v, int i, uint32_t x) { v[i] = x; }
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
  for (int i = 0; i < 10; i++) t->i_acmp_tbl_ctx[i] = 0xA5000000u + i;
  for (int s = 0; s < N_L; s++) word(t->i_render_status, s, 0x70000000u + s);
  t->aresetn = 0; ticks(8); t->aresetn = 1; ticks(530);
  wr(0x654, 1); wr(0x658, 0x12345678u); wr(0x65C, 0x0000ABCDu);
  auto* r = t->rootp;
  for (int w = 0; w < 12; w++) r->milan_csr__DOT__snap_shadow_r[w] = 0xC0000000u + w;
  r->milan_csr__DOT__cmrd_addr_r = 0x2A; r->milan_csr__DOT__cmrd_side_r = 1; r->milan_csr__DOT__cmrd_data_r = 0x2C5A;
  printf("addr value exists snap dir idx ls0 acmp srp kind cmrd sel "
         "mac sid dmac ctlr flags tuid aafc dmlo dmhi srpidx srpdir\n");
  auto show = [&](uint32_t a, uint32_t v, int kind, uint32_t sel) {
    printf("%x %08x %d %d %d %d %d %d %d %d %d %03x %012llx %016llx %012llx %016llx %04x %04x %08x %08x %08x %d %d\n", a, v,
           (int)r->milan_csr__DOT__win_in_range_w, (int)r->milan_csr__DOT__snap_busy_r,
           (int)r->milan_csr__DOT__strm_dir_r, (int)r->milan_csr__DOT__strm_idx_r,
           (int)r->milan_csr__DOT__srp_idx0_ls_w, (int)r->milan_csr__DOT__acmp_fresh_r,
           (int)r->milan_csr__DOT__srp_fresh_r, kind, (int)r->milan_csr__DOT__cmrd_valid_r, sel,
           (unsigned long long)r->milan_csr__DOT__mac_wire_w, (unsigned long long)r->milan_csr__DOT__acmp_sid_q_r,
           (unsigned long long)r->milan_csr__DOT__acmp_dmac_q_r, (unsigned long long)r->milan_csr__DOT__acmp_ctlr_q_r,
           (unsigned)r->milan_csr__DOT__acmp_flags_q_r, (unsigned)r->milan_csr__DOT__acmp_tuid_q_r,
           (unsigned)r->milan_csr__DOT__aaf_ctrl, (unsigned)r->milan_csr__DOT__aaf_dmlo, (unsigned)r->milan_csr__DOT__aaf_dmhi,
           (int)t->o_srp_ctx_idx, (int)t->o_srp_ctx_dir);
  };
  static const uint32_t words[] = {0x810, 0x814, 0x818, 0x81C, 0x820, 0x824, 0x828, 0x82C, 0x858, 0x85C, 0x860, 0x864, 0x868, 0x86C, 0x8DC};
  for (int lsn0 = 0; lsn0 < 2; lsn0++) for (int dir = 0; dir < 2; dir++) for (int idx = 0; idx < 16; idx++)
  for (int ga = 0; ga < 2; ga++) for (int gs = 0; gs < 2; gs++) for (int snap = 0; snap < 2; snap++) {
    uint32_t sel = (lsn0 << 9) | (dir << 8) | idx;
    t->i_acmp_tbl_gnt = 0; t->i_srp_ctx_gnt = 0; ticks(2);
    wr(0x800, sel); ticks(8);
    t->i_acmp_tbl_gnt = ga; t->i_srp_ctx_gnt = gs; ticks(8);
    t->i_acmp_tbl_gnt = 0; t->i_srp_ctx_gnt = 0; ticks(2);
    r->milan_csr__DOT__snap_busy_r = snap;
    for (uint32_t a : words) { uint32_t v = rd(a); t->eval(); show(a, v, 9, sel); }
    for (int kind = 0; kind < 3; kind++) {
      for (int w = 1; w < 11; w++) r->milan_csr__DOT__snap_kind_r[w] = kind;
      for (uint32_t a = 0x830; a < 0x858; a += 4) { uint32_t v = rd(a); t->eval(); show(a, v, kind, sel); }
    }
    for (int w = 1; w < 11; w++) r->milan_csr__DOT__snap_kind_r[w] = 0;
    for (int cm = 0; cm < 2; cm++) {
      r->milan_csr__DOT__cmrd_valid_r = cm;
      uint32_t v = rd(0x914); t->eval(); show(0x914, v, 9, sel);
    }
    r->milan_csr__DOT__cmrd_valid_r = 0;
    r->milan_csr__DOT__snap_busy_r = 0; ticks(2);
  }
  delete t; return 0;
}
'''
open(out, "w", encoding="utf-8").write(code.replace("@INIT@", init))
