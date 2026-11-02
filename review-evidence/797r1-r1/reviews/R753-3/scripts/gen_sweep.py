#!/usr/bin/env python3
"""Generate a Verilator harness sweeping selection and state over milan_csr for
all 17 read tables. Usage: gen_sweep.py <repo-root> <out.cpp> <n_listeners>
Inputs carry distinct constants; state flops are sampled at each read."""
import re, sys
root, out, nl = sys.argv[1], sys.argv[2], int(sys.argv[3])
t = open(f"{root}/hdl/common/csr/milan_csr.sv", encoding="utf-8").read()
t = re.sub(r"//.*", "", t)
t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
h = t[t.index("module milan_csr"):]
h = h[:h.index(");\n")]
ports = re.findall(r"\binput\s+wire\s*(?:\[[^\]]+\])?\s*(\w+)", h)
AXI = {"aclk", "aresetn", "s_axi_awaddr", "s_axi_awvalid", "s_axi_wdata", "s_axi_wstrb", "s_axi_wvalid",
       "s_axi_bready", "s_axi_araddr", "s_axi_arvalid", "s_axi_rready"}
HIGH = {"i_lctx_rd_valid", "i_tctx_rd_valid", "i_lctx_wr_rdy", "i_tctx_wr_rdy", "i_lctx_snap_ok", "i_tctx_snap_ok"}
init = "\n".join(f"  setv(d->{p}, {1 if p in HIGH else 0});" for p in ports if p not in AXI)
code = r'''#include "Vmilan_csr.h"
#include "Vmilan_csr___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
static Vmilan_csr* d;
template <class T> static void setv(T& v, uint32_t x) { v = x; }
template <std::size_t N> static void setv(VlWide<N>& v, uint32_t x) { for (std::size_t i = 0; i < N; i++) v[i] = x; }
static void tick() { d->aclk = 0; d->eval(); d->aclk = 1; d->eval(); d->aclk = 0; d->eval(); }
static void ticks(int n) { while (n--) tick(); }
static uint32_t rd(uint32_t a) {
  d->s_axi_araddr = a; d->s_axi_arvalid = 1; d->s_axi_rready = 0; int g = 0; d->eval();
  while (!d->s_axi_arready) { tick(); if (++g > 3000) return 0xBAD0BAD0u; }
  tick(); d->s_axi_arvalid = 0; d->eval(); g = 0;
  while (!d->s_axi_rvalid) { tick(); if (++g > 3000) return 0xBAD1BAD1u; }
  uint32_t v = d->s_axi_rdata; d->s_axi_rready = 1; d->eval(); tick(); d->s_axi_rready = 0; d->eval(); tick(); return v;
}
static void wr(uint32_t a, uint32_t x) {
  d->s_axi_awaddr = a; d->s_axi_wdata = x; d->s_axi_wstrb = 0xF; d->s_axi_awvalid = 1; d->s_axi_wvalid = 1;
  d->s_axi_bready = 1; int g = 0; d->eval();
  while (!d->s_axi_awready) { tick(); if (++g > 3000) break; }
  tick(); d->s_axi_awvalid = 0; d->s_axi_wvalid = 0; d->eval(); ticks(4);
}
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv); d = new Vmilan_csr;
  d->s_axi_awvalid = 0; d->s_axi_wvalid = 0; d->s_axi_arvalid = 0; d->s_axi_bready = 1; d->s_axi_rready = 0;
@INIT@
  d->i_lctx_rd_data = 0x11111111u; d->i_tctx_rd_data = 0x22222222u; d->i_lwsrp_status = 0x33333333u;
  d->i_srp_ctx_rd_stat = 0x4444u; d->i_srp_ctx_rd_sid = 0x5555555566666666ULL;
  setv(d->i_acmp_tbl_ctx, 0xA5A50000u);
  d->i_render_status = (@NL@ > 1) ? 0x7700000177000000ULL : 0x77000000u;
  d->aresetn = 0; ticks(8); d->aresetn = 1; ticks(600);
  wr(0x654, 1); wr(0x658, 0x12345678u); wr(0x65C, 0x0000ABCDu);
  auto* r = d->rootp;
  /* directed: ADP_CMD reads 0 with its strobe up and after; SEL bit 9 reads 0 */
  fprintf(stderr, "ADP_CMD before write 0x%08x\n", rd(0x640));
  wr(0x640, 3); fprintf(stderr, "ADP_CMD read after write 0x%08x\n", rd(0x640));
  d->s_axi_awaddr = 0x640; d->s_axi_wdata = 3; d->s_axi_wstrb = 0xF; d->s_axi_awvalid = 1; d->s_axi_wvalid = 1; d->eval();
  int pulses = 0;
  for (int i = 0; i < 12; i++) { tick(); if (d->o_adp_advertise_p && d->o_adp_depart_p) pulses++; if (d->s_axi_awready) { d->s_axi_awvalid = 0; d->s_axi_wvalid = 0; } d->eval(); }
  d->s_axi_awvalid = 0; d->s_axi_wvalid = 0; d->eval();
  fprintf(stderr, "ADP_CMD strobe high for %d cycle(s) per write\n", pulses);
  wr(0x800, 0x300); fprintf(stderr, "STRM_SEL written 0x300 reads 0x%08x; STRMW_SRP 0x%08x i_lwsrp_status 0x33333333\n", rd(0x800), rd(0x85C));
  wr(0x800, 0x100); fprintf(stderr, "STRM_SEL written 0x100 reads 0x%08x; STRMW_SRP 0x%08x\n", rd(0x800), rd(0x85C));
  wr(0x800, 0x200); fprintf(stderr, "STRM_SEL written 0x200 reads 0x%08x; STRMW_SRP 0x%08x\n", rd(0x800), rd(0x85C));
  wr(0x800, 0x000); fprintf(stderr, "STRM_SEL written 0x000 reads 0x%08x; STRMW_SRP 0x%08x\n", rd(0x800), rd(0x85C));
  static const uint32_t words[] = {0x810,0x814,0x818,0x81C,0x820,0x824,0x828,0x82C,
    0x830,0x834,0x838,0x83C,0x840,0x844,0x848,0x84C,0x850,0x854,0x858,0x85C,0x860,0x864,0x868,0x86C,0x8DC,0x914};
  static const int idxs[] = {0, 1, 2, 3, 15};
  printf("addr value bit9 ls0 dir idx exists snap acmp srp cm kind shadow sid dmac ctlr flags tuid mac sel\n");
  for (int bit9 = 0; bit9 < 2; bit9++) for (int dir = 0; dir < 2; dir++) for (int idx : idxs)
  for (int ga = 0; ga < 2; ga++) for (int gs = 0; gs < 2; gs++) for (int snap = 0; snap < 2; snap++)
  for (int cm = 0; cm < 2; cm++) for (int kind = 0; kind < 3; kind++) {
    d->i_acmp_tbl_gnt = 0; d->i_srp_ctx_gnt = 0; d->i_lctx_snap_ok = 1; d->i_tctx_snap_ok = 1; ticks(2);
    uint32_t sel = (bit9 << 9) | (dir << 8) | idx;
    wr(0x800, sel); ticks(8);
    d->i_acmp_tbl_gnt = ga; d->i_srp_ctx_gnt = gs; ticks(8);
    d->i_acmp_tbl_gnt = 0; d->i_srp_ctx_gnt = 0; ticks(2);
    if (snap) { d->i_lctx_snap_ok = 0; d->i_tctx_snap_ok = 0; wr(0x804, 1); ticks(8); }
    /* the state this sweep owns and no input reaches: deposited, sampled at the read */
    int forced = 0;
    if (snap && !r->milan_csr__DOT__snap_busy_r) { r->milan_csr__DOT__snap_busy_r = 1; forced = 1; }
    r->milan_csr__DOT__cmrd_valid_r = cm;
    for (int w = 0; w < 12; w++) { r->milan_csr__DOT__snap_kind_r[w] = kind; r->milan_csr__DOT__snap_shadow_r[w] = 0xC0DE0000u + w; }
    d->eval();
    for (uint32_t a : words) {
      uint32_t s0 = (r->milan_csr__DOT__acmp_fresh_r << 2) | (r->milan_csr__DOT__srp_fresh_r << 1) | r->milan_csr__DOT__snap_busy_r;
      uint32_t w = (a >= 0x830 && a < 0x858) ? 1 + (a - 0x830) / 4 : (a == 0x858 ? 11 : 0);
      uint32_t shadow = r->milan_csr__DOT__snap_shadow_r[w];
      uint32_t v = rd(a); d->eval();
      uint32_t s1 = (r->milan_csr__DOT__acmp_fresh_r << 2) | (r->milan_csr__DOT__srp_fresh_r << 1) | r->milan_csr__DOT__snap_busy_r;
      printf("%x %08x %d %d %d %d %d %d %d %d %d %d %08x %016llx %012llx %016llx %04x %04x %012llx %03x%s\n", a, v, bit9,
             (int)r->milan_csr__DOT__srp_idx0_ls_w, (int)r->milan_csr__DOT__strm_dir_r, (int)r->milan_csr__DOT__strm_idx_r,
             (int)r->milan_csr__DOT__win_in_range_w, (s1 & 1), (s1 >> 2) & 1, (s1 >> 1) & 1,
             (int)r->milan_csr__DOT__cmrd_valid_r, kind, shadow,
             (unsigned long long)r->milan_csr__DOT__acmp_sid_q_r, (unsigned long long)r->milan_csr__DOT__acmp_dmac_q_r,
             (unsigned long long)r->milan_csr__DOT__acmp_ctlr_q_r, (unsigned)r->milan_csr__DOT__acmp_flags_q_r,
             (unsigned)r->milan_csr__DOT__acmp_tuid_q_r, (unsigned long long)r->milan_csr__DOT__mac_wire_w, sel,
             s0 == s1 ? "" : " MOVED");
    }
    if (forced) r->milan_csr__DOT__snap_busy_r = 0;
    d->i_lctx_snap_ok = 1; d->i_tctx_snap_ok = 1; int g = 0;
    while (r->milan_csr__DOT__snap_busy_r && ++g < 4000) tick();
    ticks(4);
  }
  delete d; return 0;
}
'''
open(out, "w", encoding="utf-8").write(code.replace("@INIT@", init).replace("@NL@", str(nl)))
