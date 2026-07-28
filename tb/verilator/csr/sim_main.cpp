/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for milan_csr.sv (AXI4-Lite TSN CSR block).
 * Drives an AXI4-Lite master BFM and checks the register map in
 * docs/reference/REGISTER_MAP.md: reset values, RW behaviour, W1C IRQ, command strobes,
 * stats snapshot, and the config output wiring. Exit 0 = pass.
 */

#include "Vmilan_csr.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>

// Register offsets (mirror docs/reference/REGISTER_MAP.md)
enum {
  A_ID=0x000, A_VERSION=0x004, A_CAP=0x008, A_SCRATCH=0x00C,
  A_IRQ_STATUS=0x010, A_IRQ_MASK=0x014, A_IRQ_RAW=0x018,
  A_MAC_CTRL=0x100, A_MAC_IFG=0x104, A_MAC_ALO=0x108, A_MAC_AHI=0x10C,
  A_MAC_STATUS=0x110, A_MC_LO=0x114, A_MC_HI=0x118, A_PHY_RST=0x11C,
  A_STATS_CTRL=0x200, A_STATS_CAP=0x204, A_STAT0=0x210, A_STAT8=0x230,
  A_CLS_CTRL=0x300, A_CLS_MAP=0x308, A_CLS_TCQ=0x310,
  A_CBS0_IDLE=0x400, A_CBS0_CTRL=0x40C, A_CBS1_IDLE=0x420, A_CBS2_CTRL=0x44C,
  A_CBS3_IDLE=0x460, A_CBS3_CTRL=0x46C, A_CBS4_IDLE=0x480, A_CBS4_CTRL=0x48C,
  A_CBS_PAST_END=0x4A0,
  A_PTP_CTRL=0x500, A_PTP_INCR=0x504, A_PTP_TWLO=0x510, A_PTP_TWHI=0x514,
  A_PTP_CMD=0x520, A_PTP_TRLO=0x530, A_PTP_TRHI=0x534,
  A_ADP_CTRL=0x600, A_ADP_EIDLO=0x604, A_ADP_EIDHI=0x608, A_ADP_ECAPS=0x614,
  A_ADP_TALK=0x618, A_ADP_LIST=0x61C,
  A_ADP_GMLO=0x624, A_ADP_GMHI=0x628, A_ADP_DOMAIN=0x62C,
  A_ADP_IDX0=0x630, A_ADP_CMD=0x640, A_ADP_STATUS=0x644,
  A_TCAM_CTRL=0x700, A_TCAM_KLO=0x704, A_TCAM_KHI=0x708, A_TCAM_MLO=0x70C,
  A_TCAM_MHI=0x710, A_TCAM_ACT=0x714, A_TCAM_CMD=0x718,
};

static Vmilan_csr* dut;
static long fails = 0, checks = 0;

// sticky captures of single-cycle strobe outputs
static bool seen_ptp_load, seen_ptp_adjust, seen_ptp_snap;
static bool seen_stats_snap, seen_stats_reset;
static bool seen_adp_adv, seen_adp_dep;
static bool seen_i2spb_clru, seen_i2spb_clro;
static bool seen_clkv_wr, seen_clkv_disc;
// TCAM entry-write capture (o_tcam_wr_en is a 1-cycle strobe)
static bool     seen_tcam_wr;
static uint32_t tcam_wr_index, tcam_wr_valid, tcam_wr_action;
static uint64_t tcam_wr_key, tcam_wr_mask;

static void posedge() {
  dut->aclk = 1; dut->eval();
  seen_ptp_load    |= dut->o_ptp_cmd_load;
  seen_ptp_adjust  |= dut->o_ptp_cmd_adjust;
  seen_ptp_snap    |= dut->o_ptp_cmd_snapshot;
  seen_stats_snap  |= dut->o_stats_snapshot;
  seen_stats_reset |= dut->o_stats_reset;
  seen_adp_adv     |= dut->o_adp_advertise_p;
  seen_adp_dep     |= dut->o_adp_depart_p;
  seen_i2spb_clru  |= dut->o_i2spb_clr_under;
  seen_i2spb_clro  |= dut->o_i2spb_clr_over;
  seen_clkv_wr     |= dut->o_clkv_wr_p;
  seen_clkv_disc   |= dut->o_clkv_disc_p;
  if (dut->o_tcam_wr_en) {          // latch the committed entry
    seen_tcam_wr = true;
    tcam_wr_index = dut->o_tcam_wr_index; tcam_wr_valid = dut->o_tcam_wr_valid;
    tcam_wr_key = dut->o_tcam_wr_key; tcam_wr_mask = dut->o_tcam_wr_mask;
    tcam_wr_action = dut->o_tcam_wr_action;
  }
  dut->aclk = 0; dut->eval();
}

static void axi_write(uint32_t a, uint32_t d) {
  dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
  dut->s_axi_wdata  = d; dut->s_axi_wvalid  = 1; dut->s_axi_wstrb = 0xF;
  dut->s_axi_bready = 1;
  for (int g = 0; g < 2048; ++g) {
    dut->eval();
    bool acc = dut->s_axi_awready && dut->s_axi_wready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
  for (int g = 0; g < 2048; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; posedge(); }
  posedge();                       // consume bvalid (bready=1)
  dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint32_t a) {
  dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
  for (int g = 0; g < 2048; ++g) {
    dut->eval();
    bool acc = dut->s_axi_arready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t v = 0;
  for (int g = 0; g < 2048; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } posedge(); }
  posedge();                       // consume rvalid (rready=1)
  dut->s_axi_rready = 0;
  return v;
}

static void ck(const char* what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("  [FAIL] %-26s got=0x%llx exp=0x%llx\n", what,
           (unsigned long long)got, (unsigned long long)exp);
  } else {
    printf("  [ok]   %-26s = 0x%llx\n", what, (unsigned long long)got);
  }
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  dut = new Vmilan_csr;

  // reset
  dut->aresetn = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_bready = 0;
  dut->s_axi_arvalid = dut->s_axi_rready = 0;
  dut->i_evt_tx_ts_ready = dut->i_evt_link_change = dut->i_evt_rmon_rollover = 0;
  dut->i_link_up = 1; dut->i_speed = 2; dut->i_full_duplex = 1;
  dut->i_ptp_tod = 0; dut->i_ptp_tod_valid = 0;
  dut->i_adp_available_index = 0;
  dut->i_mac_reinit = 0;
  dut->i_acmp_rest_ack = 0; dut->i_acmp_rest_status = 0;
  // P12 no-engine ties (see the milan_csr port contract): rd_valid/wr_rdy
  // tied 1 reproduce the P11 fixed 4-cycle window timing with rd_data=0
  dut->i_lctx_rd_valid = 1; dut->i_tctx_rd_valid = 1;
  dut->i_lctx_wr_rdy = 1;   dut->i_tctx_wr_rdy = 1;
  for (int k = 0; k < 9; ++k) dut->i_stats[k] = 0;
  dut->i_stats_cap = 0;
  for (int k = 0; k < 10; ++k) dut->i_avtprx_cnt10[k] = 0;
  for (int i = 0; i < 5; ++i) posedge();
  dut->aresetn = 1; posedge();

  printf("== milan_csr AXI4-Lite CSR verification ==\n");

  printf("-- identification / capabilities --\n");
  ck("ID",            axi_read(A_ID),      0x4D494C4E);
  ck("VERSION",       axi_read(A_VERSION), 0x00010018);
  uint32_t cap = axi_read(A_CAP);
  ck("CAP.num_queues", cap & 0xF, 5);
  ck("CAP.CBS",        (cap >> 8) & 1, 1);
  ck("CAP.PTP",        (cap >> 9) & 1, 1);
  ck("CAP.STATS",      (cap >> 10) & 1, 1);
  ck("CAP.ADP",        (cap >> 12) & 1, 1);
  ck("CAP.TCAM",       (cap >> 13) & 1, 1);
  ck("CAP.ts_width",   (cap >> 16) & 0xFF, 64);

  printf("-- reset values --\n");
  ck("MAC_CTRL(reset)",  axi_read(A_MAC_CTRL), 0x13);
  ck("MAC_IFG(reset)",   axi_read(A_MAC_IFG),  0x0C);
  ck("PHY_RST(reset)",   axi_read(A_PHY_RST),  0x1);
  // CLS_CTRL resets to 0x5: [0] use_pcp = 1, [1] dmac_check = 0 (REQ-CLS-07
  // opt-in), [2] ctrl_class = 1 - the REQ-CLS-10 control fast path ships ON so
  // the CONTROL_CLASS row of EGRESS_QUEUE_MAP.md is true on the wire at reset.
  ck("CLS_CTRL(reset)",  axi_read(A_CLS_CTRL), 0x5);
  ck("o_cls_use_pcp(reset)",    dut->o_cls_use_pcp,    1);
  ck("o_cls_dmac_check(reset)", dut->o_cls_dmac_check, 0);
  ck("o_cls_ctrl_class(reset)", dut->o_cls_ctrl_class, 1);
  ck("CLS_MAP(reset)",   axi_read(A_CLS_MAP),  0x00FAC688);
  // 5-queue map, 3 bits per traffic class: TC0/1 -> q0, TC2 -> q3 (SR-B),
  // TC3 -> q4 (SR-A), TC4/5 -> q1 (control), TC6/7 -> q2 (gPTP). No spare.
  ck("CLS_TCQ(reset)",   axi_read(A_CLS_TCQ),  0x004898C0);
  ck("PTP_CTRL(reset)",  axi_read(A_PTP_CTRL), 0x1);
  ck("PTP_INCR(reset)",  axi_read(A_PTP_INCR), 0x08000000);
  // CBS reset slopes are INDEXED BY QUEUE (q0 = best effort ... q4 = SR-A)
  // and sum to 725 Mb/s, under the 75% REQ-CBS-03 ceiling.
  ck("CBS0_IDLE(reset q0 BE)",  axi_read(A_CBS0_IDLE),  25000000u);
  ck("CBS3_IDLE(reset q3 SR-B)",axi_read(A_CBS3_IDLE), 150000000u);
  ck("CBS4_IDLE(reset q4 SR-A)",axi_read(A_CBS4_IDLE), 450000000u);
  // ALL queues unshaped at reset: BE lands on q0 via the default class map, and CBS
  // must never pace best-effort (REQ-CBS-02) — software opts SR queues in. The old
  // 4'b0011 default shaped q0 and capped BE TX at ~250 Mbit/s on silicon.
  ck("CBS0_EN(reset)",   axi_read(A_CBS0_CTRL) & 1, 0);   // unshaped (was 1 pre-fix)
  ck("CBS2_EN(reset)",   axi_read(A_CBS2_CTRL) & 1, 0);   // unshaped
  ck("CBS3_EN(reset)",   axi_read(A_CBS3_CTRL) & 1, 0);
  ck("CBS4_EN(reset)",   axi_read(A_CBS4_CTRL) & 1, 0);
  // the CBS window now runs 0x400..0x49F (5 queues x 0x20); one past the end
  // must read 0 - a stride/size regression would alias a real queue here, and
  // 0x4A0 is exactly where the SIXTH queue's IDLE register used to live
  ck("CBS window ends at 0x4A0", axi_read(A_CBS_PAST_END), 0);
  // ...and 0x4A0 must be UNMAPPED, not merely zero-at-reset. The read-0 leg
  // above has NO TEETH on its own: leave A_CBS_END spanning six queues and
  // 0x4A0 still reads 0, because the reset-defaults ROM indexes a 5-entry
  // table out of range and yields 0 too (mutation-proven 2026-07-27). A WRITE
  // is what discriminates - inside the window `is_plain_rw` puts the word in
  // the shadow BRAM and it reads back; outside, it goes nowhere.
  axi_write(A_CBS_PAST_END, 0xA5A5A5A5);
  ck("0x4A0 is UNMAPPED (a write must not stick)", axi_read(A_CBS_PAST_END), 0);
  // same test one queue further in, at the last REAL queue, so the check above
  // cannot pass by the window being broken shut instead of correctly sized
  axi_write(A_CBS4_IDLE, 0xA5A5A5A5);
  ck("0x480 IS mapped (q4 IDLE takes the write)", axi_read(A_CBS4_IDLE), 0xA5A5A5A5);
  axi_write(A_CBS4_IDLE, 450000000u);

  // RESET VALUE vs RESET OUTPUT. Readback is served from the shadow BRAM
  // (seeded from the `csr_default` table) while the datapath sees the register
  // file's own reset assignment - two independent literals. If they diverge the
  // classifier/shaper run on one value while software reads another, which no
  // readback-only check can see. Pin them equal for the queue-shaped ones.
  dut->eval();
  ck("o_cls_tc_queue_map == CLS_TCQ readback", dut->o_cls_tc_queue_map,
     axi_read(A_CLS_TCQ));
  ck("o_cbs_idle_slope[0] == CBS0_IDLE readback", dut->o_cbs_idle_slope[0],
     axi_read(A_CBS0_IDLE));
  ck("o_cbs_idle_slope[4] == CBS4_IDLE readback", dut->o_cbs_idle_slope[4],
     axi_read(A_CBS4_IDLE));
  ck("o_cbs_enable == 0 at reset (all five unshaped)", dut->o_cbs_enable, 0);

  // FQTSS bandwidth availability (802.1Q-2018 §34.3.1 / REQ-CBS-03) over the
  // registers SOFTWARE actually reads, not over the RTL package. `deltaBandwidth`
  // caps the reserved share of portTransmitRate at 75 %; the shaper harness
  // (tb/verilator/shaper_core) gates the package tables, this gates the CSR
  // window they are supposed to mirror. A slope table edited past the ceiling
  // is a spec violation that no per-register readback check can see.
  {
    uint64_t sum = 0;
    for (int q = 0; q < 5; q++) sum += axi_read(0x400 + 0x20 * q);
    ck("FQTSS 34.3.1: sum(CBSn_IDLE) <= 75% of 1 Gb/s", sum <= 750000000ull, 1);
    ck("FQTSS 34.3.1: SR A+B <= 75% of 1 Gb/s",
       (uint64_t)axi_read(A_CBS4_IDLE) + axi_read(A_CBS3_IDLE) <= 750000000ull, 1);
    // class A must outrank class B in bandwidth as well as in queue order
    ck("FQTSS: class A slope > class B slope",
       axi_read(A_CBS4_IDLE) > axi_read(A_CBS3_IDLE), 1);
    printf("   [info] reset idleSlope sum = %llu bps (%.1f%% of 1 Gb/s), "
           "SR A+B = %u bps\n", (unsigned long long)sum, sum / 1e7,
           axi_read(A_CBS4_IDLE) + axi_read(A_CBS3_IDLE));
  }

  printf("-- read-only registers reject writes --\n");
  axi_write(A_ID, 0xFFFFFFFF);
  ck("ID stays RO", axi_read(A_ID), 0x4D494C4E);
  ck("MAC_STATUS(link/spd/dup)", axi_read(A_MAC_STATUS), 0xD); // fd=1,spd=2,link=1 -> 1101

  printf("-- RW registers + output wiring --\n");
  axi_write(A_SCRATCH, 0xDEADBEEF);
  ck("SCRATCH rw", axi_read(A_SCRATCH), 0xDEADBEEF);

  axi_write(A_MAC_CTRL, 0x1F);
  ck("MAC_CTRL rw", axi_read(A_MAC_CTRL), 0x1F);
  dut->eval();
  ck("o_mac_promisc",  dut->o_mac_promisc, 1);
  ck("o_mac_allmulti", dut->o_mac_allmulti, 1);
  ck("o_mac_is_1g",    dut->o_mac_is_1g, 1);

  axi_write(A_MAC_ALO, 0x33221100);
  axi_write(A_MAC_AHI, 0x00005544);
  dut->eval();
  ck("o_mac_addr", dut->o_mac_addr, 0x554433221100ULL);

  axi_write(A_CBS1_IDLE, 0x0AABBCCD);
  ck("CBS1_IDLE rw", axi_read(A_CBS1_IDLE), 0x0AABBCCD);
  dut->eval();
  ck("o_cbs_idle_slope[1]", dut->o_cbs_idle_slope[1], 0x0AABBCCD);

  axi_write(A_CBS3_CTRL, 0x1);           // enable queue 3 shaping
  dut->eval();
  ck("o_cbs_enable bit3", (dut->o_cbs_enable >> 3) & 1, 1);
  axi_write(A_CBS3_CTRL, 0x0);

  // the TOP queue is reachable end-to-end (write -> readback -> output)
  axi_write(A_CBS4_IDLE, 0x0C0FFEE0);
  ck("CBS4_IDLE rw", axi_read(A_CBS4_IDLE), 0x0C0FFEE0);
  dut->eval();
  ck("o_cbs_idle_slope[4]", dut->o_cbs_idle_slope[4], 0x0C0FFEE0);
  axi_write(A_CBS4_CTRL, 0x1);           // shape the class-A queue
  dut->eval();
  ck("o_cbs_enable bit4", (dut->o_cbs_enable >> 4) & 1, 1);
  axi_write(A_CBS4_CTRL, 0x0);
  axi_write(A_CBS4_IDLE, 450000000u);

  printf("-- IRQ: event latch, mask, W1C --\n");
  axi_write(A_IRQ_MASK, 0x7);
  dut->i_evt_tx_ts_ready = 1; posedge(); dut->i_evt_tx_ts_ready = 0; posedge();
  ck("IRQ_STATUS[0] set", axi_read(A_IRQ_STATUS) & 1, 1);
  dut->eval();
  ck("o_irq asserted", dut->o_irq, 1);
  axi_write(A_IRQ_STATUS, 0x1);          // W1C bit0
  ck("IRQ_STATUS[0] cleared", axi_read(A_IRQ_STATUS) & 1, 0);
  dut->eval();
  ck("o_irq deasserted", dut->o_irq, 0);
  dut->i_evt_link_change = 1; posedge(); dut->i_evt_link_change = 0; posedge();
  ck("IRQ_STATUS[1] set", (axi_read(A_IRQ_STATUS) >> 1) & 1, 1);
  axi_write(A_IRQ_STATUS, 0x2);

  // Hardware event set must win over a coincident W1C clear (event not lost).
  // With the event held asserted across the W1C ack, the bit stays set.
  dut->i_evt_tx_ts_ready = 1;
  axi_write(A_IRQ_STATUS, 0x1);          // W1C bit0 while the event is asserted
  ck("event beats W1C (bit stays set)", axi_read(A_IRQ_STATUS) & 1, 1);
  dut->i_evt_tx_ts_ready = 0; posedge();
  axi_write(A_IRQ_STATUS, 0x1);          // now the event is gone, W1C clears it
  ck("W1C clears once event deasserts", axi_read(A_IRQ_STATUS) & 1, 0);

  printf("-- PTP command strobes + TOD snapshot --\n");
  seen_ptp_snap = false;
  axi_write(A_PTP_CMD, 0x4);             // snapshot command -> pulses o_ptp_cmd_snapshot
  ck("o_ptp_cmd_snapshot pulsed", seen_ptp_snap, 1);
  ck("PTP_CMD reads 0 (strobe)", axi_read(A_PTP_CMD), 0);
  // PHC returns the snapshot value asynchronously via i_ptp_tod + i_ptp_tod_valid
  dut->i_ptp_tod = 0x1122334455667788ULL; dut->i_ptp_tod_valid = 1;
  posedge();
  dut->i_ptp_tod_valid = 0; dut->i_ptp_tod = 0; posedge();
  ck("PTP_TOD_RD_LO", axi_read(A_PTP_TRLO), 0x55667788);
  ck("PTP_TOD_RD_HI", axi_read(A_PTP_TRHI), 0x11223344);
  seen_ptp_load = false;
  axi_write(A_PTP_CMD, 0x1);             // load (settime apply)
  ck("o_ptp_cmd_load pulsed", seen_ptp_load, 1);

  printf("-- statistics snapshot --\n");
  for (int k = 0; k < 9; ++k) dut->i_stats[k] = 0xAAAA0000u + k;
  dut->eval();
  seen_stats_snap = false;
  axi_write(A_STATS_CTRL, 0x1);          // snapshot latch
  ck("o_stats_snapshot pulsed", seen_stats_snap, 1);
  ck("STAT0 latched", axi_read(A_STAT0), 0xAAAA0000u);
  ck("STAT8 latched", axi_read(A_STAT8), 0xAAAA0008u);
  seen_stats_reset = false;
  axi_write(A_STATS_CTRL, 0x2);          // reset pulse
  ck("o_stats_reset pulsed", seen_stats_reset, 1);

  printf("-- STATS_CAP 0x204 (which STAT lanes are real) --\n");
  // The STAT window's zero used to be ambiguous: "no errors" and "no counter"
  // read identically, which is how a fully tied-off RMON group survived on two
  // boards. 0x204 is a LIVE, read-only capability mask - it must track the
  // input every cycle and never become a writable shadow word.
  dut->i_stats_cap = 0x000001B8;         // lanes 3,4,5,7,8 supported
  dut->eval();
  ck("STATS_CAP reads the live mask", axi_read(A_STATS_CAP), 0x000001B8);
  dut->i_stats_cap = 0x00000108;         // MAC without FCS/preamble checking
  dut->eval();
  ck("STATS_CAP follows the input (no shadow latch)",
     axi_read(A_STATS_CAP), 0x00000108);
  axi_write(A_STATS_CAP, 0xFFFFFFFF);    // RO: a write must not stick
  ck("STATS_CAP is read-only", axi_read(A_STATS_CAP), 0x00000108);
  ck("STATS_CAP survives a snapshot (not a latched word)",
     (axi_write(A_STATS_CTRL, 0x1), axi_read(A_STATS_CAP)), 0x00000108);
  dut->i_stats_cap = 0x000001B8;
  dut->eval();

  printf("-- MAC-reset snapshot invalidate (stale-shadow fix) --\n");
  // A MAC reinit (link guard / LINK_CTRL[1]) restarts the MAC path without
  // an aresetn event here; a pre-reset snapshot must NOT survive it (the
  // 2026-07-19 "CSR plane lies until live counters tick" forensics).
  for (int k = 0; k < 9; ++k) dut->i_stats[k] = 0xBBBB0000u + k;
  dut->eval();
  axi_write(A_STATS_CTRL, 0x1);          // snapshot before the "bounce"
  ck("STAT0 pre-reinit latched", axi_read(A_STAT0), 0xBBBB0000u);
  dut->i_mac_reinit = 1;                 // guard holds the MAC in reset
  for (int i = 0; i < 4; ++i) posedge();
  ck("STAT0 held during reinit", axi_read(A_STAT0), 0xBBBB0000u);
  dut->i_mac_reinit = 0;                 // release = MAC restarted
  for (int i = 0; i < 4; ++i) posedge();
  ck("STAT0 invalidated on release", axi_read(A_STAT0), 0);
  ck("STAT8 invalidated on release", axi_read(A_STAT8), 0);
  axi_write(A_STATS_CTRL, 0x1);          // software re-arms a fresh snapshot
  ck("STAT0 re-armed post-reinit", axi_read(A_STAT0), 0xBBBB0000u);
  // config state is NOT MAC-domain state: it must survive the reinit
  ck("SCRATCH unaffected by reinit", axi_read(A_SCRATCH), 0xDEADBEEF);

  printf("-- ADP advertiser identity/control (FR-DISC-*) --\n");
  ck("ADP_CTRL(reset valid_time=31)", axi_read(A_ADP_CTRL), 0x00001F00);
  axi_write(A_ADP_EIDLO, 0xEF00FEED);
  axi_write(A_ADP_EIDHI, 0xDEAD00BE);
  dut->eval();
  ck("o_adp_entity_id", dut->o_adp_entity_id, 0xDEAD00BEEF00FEEDULL);
  axi_write(A_ADP_ECAPS, 0x0000C588);
  dut->eval();
  ck("o_adp_entity_caps", dut->o_adp_entity_caps, 0x0000C588);
  // ADP SHAPE IS READ-ONLY AND COMES FROM THE CONFIG (VERSION 0x0015).
  // 0x618/0x61C are built from gen/adp_shape_defaults.svh, which
  // sw/builder/endstation_builder.py generates from an end-station config.
  // This executable carries the TRACKED default - endstation_arty_current,
  // 1 AAF listener + 1 AAF talker + a CRF sink and no CRF output - so the
  // entity has 1 STREAM_OUTPUT and 2 STREAM_INPUTs, and talker_capabilities
  // must NOT claim MEDIA_CLOCK_SOURCE. (sim_win.cpp elaborates the 4x4
  // config and reads 5/5; sim_live.cpp the 8x8 and reads 9/9.)
  // Before 0x0015 these were plain RW words resetting to ZERO and the values
  // came from a boot script, which is how the 8x8 board advertised the 1x1
  // shape on silicon (2026-07-27). A write must now change NOTHING.
  ck("ADP_TALK RO = {0x4001, ADP_TALKER_SRC_C=1}",
     axi_read(A_ADP_TALK), 0x40010001u);
  ck("ADP_LIST RO = {0x4801, ADP_LISTENER_SINK_C=2}",
     axi_read(A_ADP_LIST), 0x48010002u);
  ck("o_adp_talker_sources", dut->o_adp_talker_sources, 1);
  ck("o_adp_talker_caps",    dut->o_adp_talker_caps, 0x4001);
  ck("o_adp_listener_sinks", dut->o_adp_listener_sinks, 2);
  ck("o_adp_listener_caps",  dut->o_adp_listener_caps, 0x4801);
  axi_write(A_ADP_TALK, 0x00010008);     // the retired S50milan-style poke
  axi_write(A_ADP_LIST, 0x48010009);
  dut->eval();
  ck("ADP_TALK ignores the write", axi_read(A_ADP_TALK), 0x40010001u);
  ck("ADP_LIST ignores the write", axi_read(A_ADP_LIST), 0x48010002u);
  ck("o_adp_talker_sources unmoved", dut->o_adp_talker_sources, 1);
  ck("o_adp_talker_caps unmoved",    dut->o_adp_talker_caps, 0x4001);
  ck("o_adp_listener_sinks unmoved", dut->o_adp_listener_sinks, 2);
  ck("o_adp_listener_caps unmoved",  dut->o_adp_listener_caps, 0x4801);
  axi_write(A_ADP_GMLO, 0x44556677);
  axi_write(A_ADP_GMHI, 0x00112233);
  dut->eval();
  ck("o_adp_gptp_gm", dut->o_adp_gptp_gm, 0x0011223344556677ULL);
  axi_write(A_ADP_DOMAIN, 0x00000005);
  dut->eval();
  ck("o_adp_gptp_domain", dut->o_adp_gptp_domain, 5);
  axi_write(A_ADP_IDX0, 0x00050002);     // identify_index=5, current_config=2
  dut->eval();
  ck("o_adp_current_config", dut->o_adp_current_config, 2);
  ck("o_adp_identify_index", dut->o_adp_identify_index, 5);
  axi_write(A_ADP_CTRL, (31u << 8) | 1); // enable=1, valid_time=31
  dut->eval();
  ck("o_adp_enable",     dut->o_adp_enable, 1);
  ck("o_adp_valid_time", dut->o_adp_valid_time, 31);
  // available_index is owned by the advertiser; ADP_STATUS reads it back (RO)
  dut->i_adp_available_index = 0x00000007; dut->eval();
  ck("ADP_STATUS avail_index", axi_read(A_ADP_STATUS), 7);
  // W1S command strobes pulse the advertiser triggers
  seen_adp_adv = false;
  axi_write(A_ADP_CMD, 0x1);             // advertise/info-changed
  ck("o_adp_advertise_p pulsed", seen_adp_adv, 1);
  seen_adp_dep = false;
  axi_write(A_ADP_CMD, 0x2);             // depart
  ck("o_adp_depart_p pulsed", seen_adp_dep, 1);
  ck("ADP_CMD reads 0 (strobe)", axi_read(A_ADP_CMD), 0);

  printf("-- lwSRP engine (0x680 group, FR-SRP-*) --\n");
  // class-A queue field is [4:2] (3 bits) and resets to q4 = SR class A
  ck("LWSRP_CTRL(reset q=4)", axi_read(0x680), 0x00000010);
  ck("LWSRP_VID(reset 2)", axi_read(0x684), 2);
  ck("LWSRP_DMAC_LO(reset)", axi_read(0x688), 0xF000FE01u);
  ck("LWSRP_DMAC_HI(reset)", axi_read(0x68C), 0x91E0);
  ck("LWSRP_TSPEC(reset {1,224})", axi_read(0x690), 0x000100E0);
  axi_write(0x680, 0x7);                 // enable + talker, queue 1
  dut->eval();
  ck("o_lwsrp_enable",    dut->o_lwsrp_enable, 1);
  ck("o_lwsrp_talker_en", dut->o_lwsrp_talker_en, 1);
  ck("o_lwsrp_qidx",      dut->o_lwsrp_qidx, 1);
  // the widened field must actually REACH the top queue: bit 4 used to be
  // reserved-0, so a build that kept [3:2] would report qidx 0 here instead of
  // 4. (5..7 are still writable and name no queue - milan_datapath gates the
  // slope MUX on qidx < NUM_QUEUES, which tb/verilator/milan_dp pins.)
  axi_write(0x680, 0x11);                // enable, queue 4
  dut->eval();
  ck("o_lwsrp_qidx q4",   dut->o_lwsrp_qidx, 4);
  axi_write(0x680, 0x7);
  axi_write(0x684, 42);
  axi_write(0x690, 0x000200F0);
  dut->eval();
  ck("o_lwsrp_vid",       dut->o_lwsrp_vid, 42);
  ck("o_lwsrp_max_frame", dut->o_lwsrp_max_frame, 0xF0);
  ck("o_lwsrp_interval",  dut->o_lwsrp_interval, 2);
  axi_write(0x688, 0x00FE0002); axi_write(0x68C, 0x91E0);
  dut->eval();
  ck("o_lwsrp_dest_mac", dut->o_lwsrp_dest_mac, 0x91E000FE0002ULL);
  dut->i_lwsrp_status = 0x0000006C; dut->i_lwsrp_slope = 17024000;
  dut->i_lwsrp_cnt = 0x00050009; dut->eval();
  ck("LWSRP_STATUS RO", axi_read(0x694), 0x0000006C);
  ck("LWSRP_SLOPE RO",  axi_read(0x698), 17024000);
  ck("LWSRP_CNT RO",    axi_read(0x69C), 0x00050009);
  axi_write(0x6A0, 500000);
  dut->eval();
  ck("o_lwsrp_latency", dut->o_lwsrp_latency, 500000);
  ck("CAP.LWSRP bit", (axi_read(0x008) >> 14) & 1, 1);

  printf("-- ACMP listener SM RO group (0x6A4) --\n");
  dut->i_acmpl_state = 0x002F0177; dut->i_acmpl_talker_lo = 0xFE000001;
  dut->i_acmpl_talker_hi = 0x02000000; dut->i_acmpl_cnt = 0x00030002;
  dut->i_acmpl_tuid = 0x00080000; dut->eval();
  ck("ACMPL_STATE RO", axi_read(0x6A4), 0x002F0177);
  ck("ACMPL_TKLO RO",  axi_read(0x6A8), 0xFE000001);
  ck("ACMPL_TKHI RO",  axi_read(0x6AC), 0x02000000);
  ck("ACMPL_CNT RO",   axi_read(0x6B0), 0x00030002);
  ck("ACMPL_TUID RO",  axi_read(0x6B4), 0x00080000);

  printf("-- AVTP RX monitor RO group (0x6B8) --\n");
  dut->i_avtprx_stat = 0x01020301; dut->i_avtprx_frx = 0xDEADBEEF;
  dut->i_avtprx_err = 0x00050702; dut->eval();
  ck("AVTPRX_STAT RO", axi_read(0x6B8), 0x01020301);
  ck("AVTPRX_FRX RO",  axi_read(0x6BC), 0xDEADBEEF);
  ck("AVTPRX_ERR RO",  axi_read(0x6C0), 0x00050702);
  axi_write(0x6BC, 0x12345678);   // RO: write ignored
  ck("AVTPRX_FRX write ignored", axi_read(0x6BC), 0xDEADBEEF);

  printf("-- MAAP group (0x6CC) --\n");
  ck("MAAP_CTRL reset (count=8, en=0)", axi_read(0x6CC), 0x00000800);
  axi_write(0x6CC, 0x12340901);   // seed 0x1234, count 9, en
  dut->eval();
  ck("MAAP_CTRL readback", axi_read(0x6CC), 0x12340901);
  ck("o_maap_enable", dut->o_maap_enable, 1);
  ck("o_maap_count", dut->o_maap_count, 9);
  ck("o_maap_seed_offset", dut->o_maap_seed_offset, 0x1234);
  dut->i_maap_stat0 = 0x01020055; dut->i_maap_stat1 = 0x00000006; dut->eval();
  ck("MAAP_STAT0 RO", axi_read(0x6D0), 0x01020055);
  ck("MAAP_STAT1 RO", axi_read(0x6D4), 0x00000006);
  axi_write(0x6CC, 0x00000800);   // restore reset default
  dut->i_i2spb_stat = 0x00050002; dut->eval();
  ck("I2SPB_STAT RO", axi_read(0x6D8), 0x00050002);

  // I2SPB_STAT W1C halves (gaps 5b): a write with any bit of a half set
  // pulses that rail's clear strobe; the halves are independent and a
  // zero write is inert. Readback stays the live engine value.
  seen_i2spb_clru = seen_i2spb_clro = false;
  axi_write(0x6D8, 0xFFFF0000);          // clear the underrun rail only
  ck("I2SPB W1C under strobe", seen_i2spb_clru, 1);
  ck("I2SPB W1C under only",   seen_i2spb_clro, 0);
  seen_i2spb_clru = seen_i2spb_clro = false;
  axi_write(0x6D8, 0x0000FFFF);          // clear the overrun rail only
  ck("I2SPB W1C over strobe",  seen_i2spb_clro, 1);
  ck("I2SPB W1C over only",    seen_i2spb_clru, 0);
  seen_i2spb_clru = seen_i2spb_clro = false;
  axi_write(0x6D8, 0);                   // zero write clears nothing
  ck("I2SPB W1C zero inert", seen_i2spb_clru || seen_i2spb_clro, 0);
  ck("I2SPB_STAT still live", axi_read(0x6D8), 0x00050002);

  // ---- 0x778 clock validity (the AVTP tu verdict) ----------------------
  // The register that stops us claiming timestamps we cannot prove
  // (docs/findings/REF_LISTENER_TIMESTAMP_SWEEP_0727.md). Reset must be
  // SYNC_OK=0 - a default of 1 would reproduce the defect exactly.
  ck("CLKV_CTRL reset = lease 8, SYNC_OK 0", axi_read(0x778), 0x00000080);
  ck("CLKV_CTRL[0] SYNC_OK resets 0", axi_read(0x778) & 1, 0);
  ck("o_clkv_sync_ok resets 0", dut->o_clkv_sync_ok, 0);
  ck("o_clkv_wdog_q resets 8",  dut->o_clkv_wdog_q, 8);
  seen_clkv_wr = seen_clkv_disc = false;
  axi_write(0x778, 0x00000041);          // SYNC_OK | lease 4
  ck("CLKV_CTRL write pulse",  seen_clkv_wr, 1);
  ck("CLKV_CTRL[1] not set -> no disc", seen_clkv_disc, 0);
  ck("o_clkv_sync_ok",  dut->o_clkv_sync_ok, 1);
  ck("o_clkv_wdog_q",   dut->o_clkv_wdog_q, 4);
  ck("CLKV_CTRL readback", axi_read(0x778), 0x00000041);
  seen_clkv_wr = seen_clkv_disc = false;
  axi_write(0x778, 0x00000043);          // + W1S discontinuity report
  ck("CLKV_CTRL[1] W1S strobe", seen_clkv_disc, 1);
  ck("CLKV_CTRL[1] reads back 0 (self-clearing)", axi_read(0x778) & 2, 0);
  axi_write(0x778, 0x00000000);          // software withdraws the claim
  ck("SYNC_OK clearable", dut->o_clkv_sync_ok, 0);
  ck("lease 0 = never trust", dut->o_clkv_wdog_q, 0);
  dut->i_clkv_stat = 0x0000004D; dut->eval();   // lease 4, hold, no_lease, tu
  ck("CLKV_STAT RO live", axi_read(0x77C), 0x0000004D);
  dut->i_clkv_tucnt = 0x0000002A; dut->eval();
  ck("CLKV_TUCNT RO live", axi_read(0x780), 0x0000002A);
  axi_write(0x77C, 0xFFFFFFFF);          // RO: writes must not stick
  ck("CLKV_STAT stays RO",  axi_read(0x77C), 0x0000004D);
  axi_write(0x780, 0xFFFFFFFF);
  ck("CLKV_TUCNT stays RO", axi_read(0x780), 0x0000002A);
  axi_write(0x778, 0x00000080);          // restore the reset shape

  // link guard: RO status mux + LINK_CTRL[3:2] control outputs
  dut->i_linkg_stat = 0x00070013; dut->eval();
  ck("LINKG_STAT RO", axi_read(0x774), 0x00070013);
  axi_write(0x71C, 0xD);                 // sw_link | dis | freeze (no reinit)
  ck("LINKG dis out",    dut->o_linkg_dis, 1);
  ck("LINKG freeze out", dut->o_linkg_freeze, 1);
  ck("mac_reinit clear", dut->o_mac_reinit, 0);
  axi_write(0x71C, 0x1);                 // restore boot default
  ck("LINKG dis clear",  dut->o_linkg_dis, 0);
  ck("TONE_CTRL reset 0", axi_read(0x6DC), 0);
  axi_write(0x6DC, 1); dut->eval();
  ck("o_tone_enable", dut->o_tone_enable, 1);
  ck("TONE_CTRL readback", axi_read(0x6DC), 1);
  axi_write(0x6DC, 0x5); dut->eval();            // en + att=2 (-12 dB)
  ck("o_tone_att", dut->o_tone_att, 2);
  axi_write(0x6DC, 0);
  dut->i_i2spb_trim = 0xFFF00100; dut->eval();
  ck("I2SPB_TRIM RO", axi_read(0x6E0), 0xFFF00100);
  // gPTP measured propagation delay (user bug 3): daemon-written RW ns
  ck("GPTP_PDELAY reset 0", axi_read(0x6E4), 0);
  axi_write(0x6E4, 0x00021F6A); dut->eval();
  ck("o_gptp_pdelay_ns", dut->o_gptp_pdelay_ns, 0x00021F6A);
  ck("GPTP_PDELAY readback", axi_read(0x6E4), 0x00021F6A);

  printf("-- RX dest-MAC TCAM programming (REQ-MAC-02) --\n");
  ck("TCAM_CTRL(reset default_pass)", axi_read(A_TCAM_CTRL) & 1, 1);
  dut->eval();
  ck("o_tcam_default_pass", dut->o_tcam_default_pass, 1);
  // program one entry: key=91E0F0010000, mask=FFFFFFFFFFFF, action=0x22, index=3, add
  axi_write(A_TCAM_KLO, 0xF0010000);
  axi_write(A_TCAM_KHI, 0x000091E0);
  axi_write(A_TCAM_MLO, 0xFFFFFFFF);
  axi_write(A_TCAM_MHI, 0x0000FFFF);
  axi_write(A_TCAM_ACT, 0x00000022);
  dut->eval();
  ck("o_tcam_wr_key",    dut->o_tcam_wr_key,    0x91E0F0010000ULL);
  ck("o_tcam_wr_mask",   dut->o_tcam_wr_mask,   0xFFFFFFFFFFFFULL);
  ck("o_tcam_wr_action", dut->o_tcam_wr_action, 0x22);
  seen_tcam_wr = false;
  axi_write(A_TCAM_CMD, (1u << 16) | (1u << 8) | 3);   // commit: index=3, valid=1
  ck("o_tcam_wr_en pulsed", seen_tcam_wr, 1);
  ck("committed index",  tcam_wr_index, 3);
  ck("committed valid",  tcam_wr_valid, 1);
  ck("committed key",    tcam_wr_key,   0x91E0F0010000ULL);
  ck("committed action", tcam_wr_action, 0x22);
  ck("TCAM_CMD reads 0 (strobe)", axi_read(A_TCAM_CMD), 0);
  // remove entry 3
  seen_tcam_wr = false;
  axi_write(A_TCAM_CMD, (1u << 16) | (0u << 8) | 3);   // commit: index=3, valid=0 (remove)
  ck("remove commit pulsed", seen_tcam_wr, 1);
  ck("remove valid=0", tcam_wr_valid, 0);

  // ---- CRF talker CSR group (0x750) ----
  axi_write(0x750, 0x1);
  axi_write(0x754, 0x00010001);
  axi_write(0x758, 0x02000000);
  axi_write(0x75C, 0xF0002A07);
  axi_write(0x760, 0x000091E0);
  ck("CRFT_CTRL readback", axi_read(0x750), 1);
  ck("CRFT_SIDLO readback", axi_read(0x754), 0x00010001);
  ck("CRFT_SIDHI readback", axi_read(0x758), 0x02000000);
  ck("CRFT_DMLO readback", axi_read(0x75C), 0xF0002A07);
  ck("CRFT_DMHI readback", axi_read(0x760), 0x000091E0);
  ck("o_crft_en", dut->o_crft_en, 1);
  ck("o_crft_sid", dut->o_crft_sid, 0x0200000000010001ULL);
  ck("o_crft_dest_mac", dut->o_crft_dest_mac, 0x91E0F0002A07ULL);
  dut->i_crft_count = 1234;
  ck("CRFT_COUNT live", axi_read(0x764), 1234);

  printf("-- ACMP bind-restore group (0x7A0, E1) --\n");
  // the acmp-persist feature probe: 0x7A0 write/readback of the pattern
  axi_write(0x7A0, 0xA5C35A3C);
  ck("REST_TKLO probe pattern", axi_read(0x7A0), 0xA5C35A3C);
  axi_write(0x7A0, 0xFE000001);          // talker_entity_id lo
  axi_write(0x7A4, 0x02000000);          // talker_entity_id hi
  axi_write(0x7A8, 0x00020005);          // vlan 2 (informational), tuid 5
  axi_write(0x7AC, 0xFE0000AA);          // controller_entity_id lo
  axi_write(0x7B0, 0x68050000);          // controller_entity_id hi
  ck("REST_TKHI rw", axi_read(0x7A4), 0x02000000);
  ck("REST_META rw", axi_read(0x7A8), 0x00020005);
  ck("REST_CTLO rw", axi_read(0x7AC), 0xFE0000AA);
  ck("REST_CTHI rw", axi_read(0x7B0), 0x68050000);
  ck("REST_CMD idle", axi_read(0x7B4), 0);
  // commit sink 0 with STREAMING_WAIT: req held + staged record on the port
  axi_write(0x7B4, 0x80000000u | (0x0008u << 8) | 0x0);
  dut->eval();
  ck("rest req held", dut->o_acmp_rest_req, 1);
  ck("rest idx", dut->o_acmp_rest_idx, 0);
  ck("rest talker", dut->o_acmp_rest_talker, 0x02000000FE000001ULL);
  ck("rest tuid (META[15:0])", dut->o_acmp_rest_tuid, 5);
  ck("rest ctlr", dut->o_acmp_rest_ctlr, 0x68050000FE0000AAULL);
  ck("rest flags (CMD[23:8])", dut->o_acmp_rest_flags, 0x0008);
  ck("CMD busy readback", axi_read(0x7B4) >> 31, 1);
  // engine ack with status 0 -> done, not busy
  dut->i_acmp_rest_ack = 1; dut->i_acmp_rest_status = 0;
  posedge();
  dut->i_acmp_rest_ack = 0; posedge();
  dut->eval();
  ck("rest req dropped", dut->o_acmp_rest_req, 0);
  uint32_t rcmd = axi_read(0x7B4);
  ck("CMD done", (rcmd >> 30) & 1, 1);
  ck("CMD not busy", (rcmd >> 31) & 1, 0);
  ck("CMD status 0 (injected)", (rcmd >> 8) & 3, 0);
  // a refused commit (engine status 1 = occupied) reads back as done+1
  axi_write(0x7B4, 0x80000000u | 0x0);
  dut->i_acmp_rest_ack = 1; dut->i_acmp_rest_status = 1;
  posedge();
  dut->i_acmp_rest_ack = 0; posedge();
  rcmd = axi_read(0x7B4);
  ck("CMD refused status 1", (rcmd >> 8) & 3, 1);
  ck("CMD done after refusal", (rcmd >> 30) & 1, 1);
  // a write without the commit bit is inert
  axi_write(0x7B4, 0x00000001);
  ck("no-commit write inert", (axi_read(0x7B4) >> 31) & 1, 0);

  // =====================================================================
  // P11 indexed per-stream window, N=1 silicon shape (defaults):
  // SEL/SNAP decode, index-0 hard aliases onto the flat registers, and the
  // defined out-of-range behaviour (reads 0, writes ignored). The lane-K
  // engine inputs stay at their datapath ties (rd_data=0, snap_ok=0 is
  // irrelevant here: index 0 never bursts) — engine-backed words read 0.
  // =====================================================================
  enum {
    A_STRM_SEL=0x800, A_STRM_SNAP=0x804, A_SW_CTRL=0x810,
    A_SW_SID_LO=0x814, A_SW_SID_HI=0x818, A_SW_DMAC_LO=0x81C,
    A_SW_DMAC_HI=0x820, A_SW_FMT_LO=0x824, A_SW_FMT_HI=0x828,
    A_SW_STATE=0x82C, A_SW_CNT0=0x830, A_SW_PDUS=0x858, A_SW_SRP=0x85C,
  };

  printf("-- 0x800 window: SEL decode + out-of-range rule (N=1) --\n");
  ck("SEL reset", axi_read(A_STRM_SEL), 0);
  axi_write(A_STRM_SEL, 0x0000011F);            // dir=1, idx=15 (garbage high bits masked)
  ck("SEL stores {dir,idx} only", axi_read(A_STRM_SEL), 0x0000010F);
  axi_write(A_STRM_SEL, 0x00000001);            // dir=0 (listener), idx=1: OUT of range at N=1
  uint32_t aaf_ctrl_before = axi_read(0x654);
  axi_write(A_SW_CTRL, 0xFFFFFFFF);             // must be ignored
  axi_write(A_SW_SID_LO, 0x11111111);
  ck("oor CTRL reads 0",   axi_read(A_SW_CTRL),   0);
  ck("oor SID_LO reads 0", axi_read(A_SW_SID_LO), 0);
  ck("oor SRP reads 0",    axi_read(A_SW_SRP),    0);
  ck("oor write left AAF_CTRL alone", axi_read(0x654), aaf_ctrl_before);
  axi_write(A_STRM_SNAP, 1);                    // out-of-range snap: zeros, completes
  for (int i = 0; i < 8; ++i) posedge();
  ck("oor SNAP busy clears", axi_read(A_STRM_SNAP), 0);
  ck("oor SNAP CNT0 zero",   axi_read(A_SW_CNT0), 0);

  printf("-- window idx0 dir=talker: hard aliases of the flat AAF regs --\n");
  axi_write(A_STRM_SEL, 0x00000100);            // dir=1 (talker), idx=0
  axi_write(0x654, 0x00020003);                 // AAF_CTRL: en=1, bypass=1, VID=2
  axi_write(0x658, 0xF000FE01);                 // AAF_DMLO
  axi_write(0x65C, 0x000091E0);                 // AAF_DMHI
  ck("win CTRL == AAF_CTRL[0]", axi_read(A_SW_CTRL), 1);
  ck("win DMAC_LO == AAF_DMLO", axi_read(A_SW_DMAC_LO), 0xF000FE01);
  ck("win DMAC_HI == AAF_DMHI[15:0]", axi_read(A_SW_DMAC_HI), 0x000091E0);
  // alias is BIDIRECTIONAL: a window write lands in the flat register (and
  // its shadow readback), CTRL merges bit 0 only — VID/bypass survive
  axi_write(A_SW_CTRL, 0);
  ck("win CTRL wrote AAF_CTRL[0]=0", axi_read(0x654), 0x00020002);
  ck("o_aaf_enable follows", dut->o_aaf_enable, 0);
  axi_write(A_SW_CTRL, 1);
  ck("CTRL merge keeps VID/bypass", axi_read(0x654), 0x00020003);
  axi_write(A_SW_DMAC_LO, 0xF000AB01);
  axi_write(A_SW_DMAC_HI, 0x000091E0);
  ck("win DMAC_LO write -> flat 0x658", axi_read(0x658), 0xF000AB01);
  dut->eval();
  ck("o_aaf_dest_mac follows", dut->o_aaf_dest_mac, 0x91E0F000AB01ULL);
  // talker idx0 stream_id derivation {station_mac(wire order), uid=0}
  // (MAC regs still hold 0x554433221100 from the MAC test above)
  ck("win SID_HI = mac[47:16]", axi_read(A_SW_SID_HI), 0x00112233);
  ck("win SID_LO = {mac[15:0],0}", axi_read(A_SW_SID_LO), 0x44550000);

  printf("-- window idx0 talker SNAP: PDUS/STATE flat latch --\n");
  dut->i_aaf_frames = 0xCAFE0001;
  dut->i_aaf_gate = 1; dut->i_acmp_probe_armed = 1; dut->i_acmp_talker_active = 0;
  dut->i_lwsrp_status = 0x000001FF;             // low 9 bits -> STATE[27:19]
  axi_write(A_STRM_SNAP, 1);
  for (int i = 0; i < 8; ++i) posedge();
  ck("SNAP busy clears", axi_read(A_STRM_SNAP), 0);
  ck("talker PDUS = AAF_FRAMES", axi_read(A_SW_PDUS), 0xCAFE0001);
  // STATE = {4'0, srp9, 15'0, gate, lobs, active, armed}
  ck("talker STATE pack", axi_read(A_SW_STATE), (0x1FFu << 19) | (1u << 3) | 1u);
  ck("talker CNT0 poison (not-backed rule 2026-07-26)", axi_read(A_SW_CNT0), 0xDEADDEADu);
  // events after the snap do NOT move the latched block (snapshot semantics)
  dut->i_aaf_frames = 0xCAFE0099;
  ck("PDUS frozen until next SNAP", axi_read(A_SW_PDUS), 0xCAFE0001);

  printf("-- window idx0 dir=listener: FULL-WIDTH Table 7-157 counters --\n");
  // The window's index-0 CNT words used to be re-derived from the PACKED
  // 0x6B8/0x6C0 views, so they inherited their 8/16-bit truncation - and the
  // flat views' "read the window for the real number" was simply not true
  // anywhere. Since VERSION 0x0013 they come from the monitor's full 32-bit
  // counters, so a count past 0xFF/0xFFFF survives here while the flat view
  // saturates. Drive values BEYOND both ceilings: on the pre-fix RTL these
  // read back as the truncated low bytes and FAIL.
  axi_write(A_STRM_SEL, 0x00000000);            // dir=0 (listener), idx=0
  dut->i_avtprx_stat = 0x05040301;              // packed view (saturating)
  dut->i_avtprx_err  = 0x00070203;              // packed view (saturating)
  dut->i_avtprx_frx  = 123456;
  {                                             // full-width Table 7-157 lanes
    const uint32_t c10[10] = {
      0x00000103u,   // MEDIA_LOCKED        259  (> 8-bit view)
      0x00001204u,   // MEDIA_UNLOCKED     4612
      0x00034005u,   // STREAM_INTERRUPTED
      0x0001C943u,   // SEQ_NUM_MISMATCH 116547 (> 16-bit view: the silicon case)
      0x00000042u,   // MEDIA_RESET             (was hard 0 in the window)
      0x00000903u,   // TIMESTAMP_UNCERTAIN
      0x00002002u,   // UNSUPPORTED_FORMAT
      0x00000077u,   // LATE_TIMESTAMP          (was hard 0 in the window)
      0x00000088u,   // EARLY_TIMESTAMP         (was hard 0 in the window)
      123456u };     // FRAMES_RX
    for (int k = 0; k < 10; ++k) dut->i_avtprx_cnt10[k] = c10[k];
  }
  dut->i_pcmrx_cnt   = 0x00020064;              // {drops=2, pdus=100}
  dut->i_acmpl_state = (7u << 8) | (2u << 13) | 6u;  // status=7, probing=2, state=6
  dut->i_lwsrp_status = 0x00000155;
  axi_write(A_STRM_SNAP, 1);
  for (int i = 0; i < 8; ++i) posedge();
  ck("CNT0 MEDIA_LOCKED",        axi_read(A_SW_CNT0 + 0*4), 0x103);
  ck("CNT1 MEDIA_UNLOCKED",      axi_read(A_SW_CNT0 + 1*4), 0x1204);
  ck("CNT2 STREAM_INTERRUPTED",  axi_read(A_SW_CNT0 + 2*4), 0x34005);
  ck("CNT3 SEQ_NUM_MISMATCH",    axi_read(A_SW_CNT0 + 3*4), 0x1C943);
  ck("CNT4 MEDIA_RESET",         axi_read(A_SW_CNT0 + 4*4), 0x42);
  ck("CNT5 TIMESTAMP_UNCERTAIN", axi_read(A_SW_CNT0 + 5*4), 0x903);
  ck("CNT6 UNSUPPORTED_FORMAT",  axi_read(A_SW_CNT0 + 6*4), 0x2002);
  ck("CNT7 LATE_TS",             axi_read(A_SW_CNT0 + 7*4), 0x77);
  ck("CNT8 EARLY_TS",            axi_read(A_SW_CNT0 + 8*4), 0x88);
  ck("CNT9 FRAMES_RX = 0x6BC",   axi_read(A_SW_CNT0 + 9*4), 123456);
  // the point of the widening: the window keeps what the packed view cannot
  ck("window CNT3 exceeds the 16-bit packed field",
     axi_read(A_SW_CNT0 + 3*4) > 0xFFFF ? 1 : 0, 1);
  ck("PDUS = PCMRX_CNT (0x6C4)", axi_read(A_SW_PDUS), 0x00020064);
  // STATE = {4'0, srp9, wire_chans=0, media_locked, status, probing, state}
  ck("listener STATE pack", axi_read(A_SW_STATE),
     (0x155u << 19) | (1u << 10) | (7u << 5) | (2u << 3) | 6u);
  // flat-vs-window equivalence, the alias axiom made executable:
  ck("win CNT9 == flat 0x6BC", axi_read(A_SW_CNT0 + 9*4), axi_read(0x6BC));
  ck("win PDUS == flat 0x6C4", axi_read(A_SW_PDUS), axi_read(0x6C4));
  ck("win SRP  == flat 0x694", axi_read(A_SW_SRP), axi_read(0x694));
  // listener SID/DMAC come from the ACMP tbl port — tied (gnt=0) here, so
  // they read 0 exactly like today's silicon shape
  ck("listener SID_LO 0 (tbl tied)",  axi_read(A_SW_SID_LO), 0);
  ck("listener DMAC_LO 0 (tbl tied)", axi_read(A_SW_DMAC_LO), 0);
  // engine-backed words (LCTX port B) read 0 at the tie
  ck("listener CTRL 0 (LCTX tied)",   axi_read(A_SW_CTRL), 0);
  ck("listener FMT_LO 0 (LCTX tied)", axi_read(A_SW_FMT_LO), 0);

  // ---- RX parser probe group (APRB 0x8B4-0x8C4) -------------------------
  // 5 packed RO words, same >=0x800 carve-out class as the LTAP group: a
  // missing rd_in_window term makes the whole block read 0 while the fabric
  // counts fine (the 0x8F8 dead-read trap, hit for real on the servo word).
  printf("-- RX parser probe (0x8B4-0x8C4) --\n");
  const uint32_t aprb[5] = {0x00001234u, 0x000000FEu, 0x00020000u,
                            0x02000000u, 0x0008021Au};
  for (int k = 0; k < 5; ++k) dut->i_aprb_regs[k] = aprb[k];
  posedge(); posedge();
  ck("APRB frames parsed 0x8B4", axi_read(0x8B4), aprb[0]);
  ck("APRB frames matched 0x8B8", axi_read(0x8B8), aprb[1]);
  ck("APRB last SID_LO 0x8BC",   axi_read(0x8BC), aprb[2]);
  ck("APRB last SID_HI 0x8C0",   axi_read(0x8C0), aprb[3]);
  ck("APRB info 0x8C4",          axi_read(0x8C4), aprb[4]);
  // live: the words follow their inputs with no arm/strobe needed
  for (int k = 0; k < 5; ++k) dut->i_aprb_regs[k] = 0xA5A50000u + k;
  posedge(); posedge();
  ck("APRB word 0 live",  axi_read(0x8B4), 0xA5A50000u);
  ck("APRB word 4 live",  axi_read(0x8C4), 0xA5A50004u);

  // ---- item-7 playback chain probe (PBK 0x8C8-0x8D0) --------------------
  // 3 packed RO words, same >=0x800 carve-out class as APRB/LTAP above.
  // These are the ONLY fabric-side evidence of the host-ring -> KL_pcm_tx ->
  // render crossbar -> DAC chain (every other playback counter is a migen
  // CSR that exists only inside the LiteX SoC).
  printf("-- playback chain probe (0x8C8-0x8D0) --\n");
  const uint32_t pbk[3] = {0x03C0000Bu, 0x0001D4C0u, 0x000700FFu};
  for (int k = 0; k < 3; ++k) dut->i_pbk_regs[k] = pbk[k];
  posedge(); posedge();
  ck("PBK_STAT 0x8C8",  axi_read(0x8C8), pbk[0]);
  ck("PBK_FEEDS 0x8CC", axi_read(0x8CC), pbk[1]);
  ck("PBK_RAILS 0x8D0", axi_read(0x8D0), pbk[2]);
  // the word above the group is unmapped: reads 0, never a shadow alias
  ck("PBK 0x8D4 unmapped reads 0", axi_read(0x8D4), 0);
  // live: no arm/strobe, the words track their inputs
  for (int k = 0; k < 3; ++k) dut->i_pbk_regs[k] = 0x5A5A0000u + k;
  posedge(); posedge();
  ck("PBK word 0 live", axi_read(0x8C8), 0x5A5A0000u);
  ck("PBK word 2 live", axi_read(0x8D0), 0x5A5A0002u);

  // ---- REQ-MAC-03: is_1g follows the MAC's reported speed ----
  // MAC_CTRL[4] reset is 1, so before this a 100 Mb/s port (Arty MII, i_speed
  // = 01) told every is_1g consumer it was on a gigabit link until software
  // intervened - and is_1g sets the lwSRP bandwidth-gate admission limit
  // (750 vs 75 Mb/s) and the CBS sendSlope denominator. Now it follows
  // i_speed unless MAC_CTRL[5] (speed_manual) is set.
  {
    long f0 = fails;
    axi_write(A_MAC_CTRL, 0x13);                 // the reset value: manual bit clear
    dut->i_speed = 2; dut->eval();               // 1000 Mb/s
    ck("mac03 auto: speed=1000 -> is_1g",  dut->o_mac_is_1g, 1);
    dut->i_speed = 1; dut->eval();               // 100 Mb/s
    ck("mac03 auto: speed=100 -> !is_1g",  dut->o_mac_is_1g, 0);
    dut->i_speed = 0; dut->eval();               // 10 Mb/s
    ck("mac03 auto: speed=10 -> !is_1g",   dut->o_mac_is_1g, 0);
    // MAC_STATUS must report the same speed the rate select is derived from,
    // so software and the datapath cannot disagree about the link
    dut->i_speed = 1; dut->eval();
    ck("mac03 MAC_STATUS speed tracks",     (axi_read(A_MAC_STATUS) >> 1) & 3, 1);

    // manual override restores the old behaviour in BOTH directions
    axi_write(A_MAC_CTRL, 0x33);                 // [5]=manual, [4]=1
    dut->i_speed = 1; dut->eval();
    ck("mac03 manual=1,is_1g=1 beats speed=100", dut->o_mac_is_1g, 1);
    axi_write(A_MAC_CTRL, 0x23);                 // [5]=manual, [4]=0
    dut->i_speed = 2; dut->eval();
    ck("mac03 manual=1,is_1g=0 beats speed=1000", dut->o_mac_is_1g, 0);

    // NEGATIVE: with manual CLEAR, MAC_CTRL[4] must have NO effect at all -
    // otherwise the old wrong-default path is still reachable by accident
    axi_write(A_MAC_CTRL, 0x13);                 // manual clear, [4]=1
    dut->i_speed = 1; dut->eval();
    ck("mac03 auto ignores MAC_CTRL[4]=1",  dut->o_mac_is_1g, 0);
    axi_write(A_MAC_CTRL, 0x03);                 // manual clear, [4]=0
    dut->i_speed = 2; dut->eval();
    ck("mac03 auto ignores MAC_CTRL[4]=0",  dut->o_mac_is_1g, 1);

    // restore the harness defaults for anything that follows
    axi_write(A_MAC_CTRL, 0x13);
    dut->i_speed = 2; dut->eval();
    printf("  [%s] REQ-MAC-03 is_1g follows MAC speed (MAC_CTRL[5] overrides)\n",
           (fails == f0) ? "PASS" : "FAIL");
  }

  // ------------------------------------------------------------------ //
  //  chmap map-RAM readback: THE NEGATIVE CONTROL (CHMAP_RDBK_P = 0)
  //
  //  This executable elaborates milan_csr at its DEFAULT parameters, which
  //  means "no map-RAM readback port is wired in this build" - exactly the
  //  state milan_datapath shipped in (map_rd_en_i = 1'b0, map_rd_data_o
  //  unconnected). The property under test is methodology R5: a capability
  //  the fabric cannot back must read UNSUPPORTED, never 0. The check that
  //  matters here is the one that CAN fail - if the register ever answered
  //  a snapshot on a build with no port, or answered it with a zero map
  //  word, this leg fails while sim_win's positive leg still passes.
  //
  //  ORACLE: the fabric. With no readback port there IS no fabric answer,
  //  so the only honest report is "unsupported", and the data word must
  //  stay poison.
  // ------------------------------------------------------------------ //
  {
    long f0 = fails;
    printf("-- chmap readback NEGATIVE control: no port in this build --\n");
    const uint32_t A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904;
    const uint32_t A_CHMAP_SNAP = 0x910, A_CHMAP_LOOP = 0x914;
    const uint32_t POISON = 0xDEADDEADu;

    // THE TRAP THIS REGISTER EXISTS TO AVOID: the 0x800 window's data words
    // read 0 until their SNAP is armed, which is indistinguishable from a
    // dead block. Un-armed here must be POISON.
    ck("CHMAP_LOOP un-armed is POISON not 0", axi_read(A_CHMAP_LOOP), POISON);
    uint32_t s = axi_read(A_CHMAP_SNAP);
    ck("CHMAP_SNAP tag 0xC5 (feature probe)", (s >> 24) & 0xFF, 0xC5);
    ck("CHMAP_SNAP cap = 0 (port absent)", (s >> 8) & 3, 0);
    ck("CHMAP_SNAP armed = 0 at reset",     (s >> 4) & 1, 0);
    ck("CHMAP_SNAP busy = 0 at reset",       s        & 1, 0);
    ck("CHMAP_SNAP valid = 0 at reset",     (s >> 1) & 1, 0);
    // 0x918 is still reserved: it reads 0, so the 0xC5 tag is what tells a
    // probe that 0x910 EXISTS in this gateware
    ck("0x918 still reserved-reads-0", axi_read(0x918), 0);

    // arm a snapshot with no port behind it
    axi_write(A_CHMAP_CTRL, 1);
    axi_write(A_CHMAP_SEL, 0x105);            // side = capture, index = 5
    bool saw_req = false;
    axi_write(A_CHMAP_SNAP, 1);
    for (int i = 0; i < 40; ++i) { if (dut->o_chmap_rd_en) saw_req = true; posedge(); }
    s = axi_read(A_CHMAP_SNAP);
    ck("refused arm: unsup = 1",  (s >> 3) & 1, 1);
    ck("refused arm: valid = 0",  (s >> 1) & 1, 0);
    ck("refused arm: busy = 0",    s       & 1, 0);
    ck("refused arm: timeout = 0", (s >> 2) & 1, 0);   // refused, not silent
    ck("refused arm: armed = 1",  (s >> 4) & 1, 1);    // the arm WAS seen
    ck("refused arm latched {side,idx}", (s >> 16) & 0x7F, (1u << 6) | 5u);
    ck("no fabric request was issued", saw_req, 0);
    ck("CHMAP_LOOP still POISON after a refused arm",
       axi_read(A_CHMAP_LOOP), POISON);
    axi_write(A_CHMAP_CTRL, 0);
    printf("  [%s] R5: an unwired map-RAM readback reads UNSUPPORTED, not 0\n",
           (fails == f0) ? "PASS" : "FAIL");
  }

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  dut->final();
  delete dut;
  return fails ? 1 : 0;
}
