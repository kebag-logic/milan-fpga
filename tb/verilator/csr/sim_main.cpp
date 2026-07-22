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
  A_STATS_CTRL=0x200, A_STAT0=0x210, A_STAT8=0x230,
  A_CLS_CTRL=0x300, A_CLS_MAP=0x308, A_CLS_TCQ=0x310,
  A_CBS0_IDLE=0x400, A_CBS0_CTRL=0x40C, A_CBS1_IDLE=0x420, A_CBS2_CTRL=0x44C,
  A_CBS3_CTRL=0x46C,
  A_PTP_CTRL=0x500, A_PTP_INCR=0x504, A_PTP_TWLO=0x510, A_PTP_TWHI=0x514,
  A_PTP_CMD=0x520, A_PTP_TRLO=0x530, A_PTP_TRHI=0x534,
  A_ADP_CTRL=0x600, A_ADP_EIDLO=0x604, A_ADP_EIDHI=0x608, A_ADP_ECAPS=0x614,
  A_ADP_TALK=0x618, A_ADP_GMLO=0x624, A_ADP_GMHI=0x628, A_ADP_DOMAIN=0x62C,
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
  // P12 no-engine ties (see the milan_csr port contract): rd_valid/wr_rdy
  // tied 1 reproduce the P11 fixed 4-cycle window timing with rd_data=0
  dut->i_lctx_rd_valid = 1; dut->i_tctx_rd_valid = 1;
  dut->i_lctx_wr_rdy = 1;   dut->i_tctx_wr_rdy = 1;
  for (int k = 0; k < 9; ++k) dut->i_stats[k] = 0;
  for (int i = 0; i < 5; ++i) posedge();
  dut->aresetn = 1; posedge();

  printf("== milan_csr AXI4-Lite CSR verification ==\n");

  printf("-- identification / capabilities --\n");
  ck("ID",            axi_read(A_ID),      0x4D494C4E);
  ck("VERSION",       axi_read(A_VERSION), 0x00010009);
  uint32_t cap = axi_read(A_CAP);
  ck("CAP.num_queues", cap & 0xF, 4);
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
  ck("CLS_CTRL(reset)",  axi_read(A_CLS_CTRL), 0x1);
  ck("CLS_MAP(reset)",   axi_read(A_CLS_MAP),  0x00FAC688);
  ck("CLS_TCQ(reset)",   axi_read(A_CLS_TCQ),  0x000000E4);
  ck("PTP_CTRL(reset)",  axi_read(A_PTP_CTRL), 0x1);
  ck("PTP_INCR(reset)",  axi_read(A_PTP_INCR), 0x08000000);
  ck("CBS0_IDLE(reset)", axi_read(A_CBS0_IDLE), 300000000u);
  // ALL queues unshaped at reset: BE lands on q0 via the default class map, and CBS
  // must never pace best-effort (REQ-CBS-02) — software opts SR queues in. The old
  // 4'b0011 default shaped q0 and capped BE TX at ~250 Mbit/s on silicon.
  ck("CBS0_EN(reset)",   axi_read(A_CBS0_CTRL) & 1, 0);   // unshaped (was 1 pre-fix)
  ck("CBS2_EN(reset)",   axi_read(A_CBS2_CTRL) & 1, 0);   // unshaped
  ck("CBS3_EN(reset)",   axi_read(A_CBS3_CTRL) & 1, 0);

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
  axi_write(A_ADP_TALK, 0x00010008);     // talker_caps=0x0001, sources=8
  dut->eval();
  ck("o_adp_talker_sources", dut->o_adp_talker_sources, 8);
  ck("o_adp_talker_caps",    dut->o_adp_talker_caps, 0x0001);
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
  ck("LWSRP_CTRL(reset q=3)", axi_read(0x680), 0x0000000C);
  ck("LWSRP_VID(reset 2)", axi_read(0x684), 2);
  ck("LWSRP_DMAC_LO(reset)", axi_read(0x688), 0xF000FE01u);
  ck("LWSRP_DMAC_HI(reset)", axi_read(0x68C), 0x91E0);
  ck("LWSRP_TSPEC(reset {1,224})", axi_read(0x690), 0x000100E0);
  axi_write(0x680, 0x7);                 // enable + talker, queue 1
  dut->eval();
  ck("o_lwsrp_enable",    dut->o_lwsrp_enable, 1);
  ck("o_lwsrp_talker_en", dut->o_lwsrp_talker_en, 1);
  ck("o_lwsrp_qidx",      dut->o_lwsrp_qidx, 1);
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
  ck("talker CNT0 zero", axi_read(A_SW_CNT0), 0);
  // events after the snap do NOT move the latched block (snapshot semantics)
  dut->i_aaf_frames = 0xCAFE0099;
  ck("PDUS frozen until next SNAP", axi_read(A_SW_PDUS), 0xCAFE0001);

  printf("-- window idx0 dir=listener: Table 7-157 flat aliases --\n");
  axi_write(A_STRM_SEL, 0x00000000);            // dir=0 (listener), idx=0
  dut->i_avtprx_stat = 0x05040301;              // {intr=5, unlocked=4, locked=3, ..., locked=1}
  dut->i_avtprx_err  = 0x00070203;              // {seqmm=7, unsupp=2, tu=3}
  dut->i_avtprx_frx  = 123456;
  dut->i_pcmrx_cnt   = 0x00020064;              // {drops=2, pdus=100}
  dut->i_acmpl_state = (7u << 8) | (2u << 13) | 6u;  // status=7, probing=2, state=6
  dut->i_lwsrp_status = 0x00000155;
  axi_write(A_STRM_SNAP, 1);
  for (int i = 0; i < 8; ++i) posedge();
  ck("CNT0 MEDIA_LOCKED",        axi_read(A_SW_CNT0 + 0*4), 3);
  ck("CNT1 MEDIA_UNLOCKED",      axi_read(A_SW_CNT0 + 1*4), 4);
  ck("CNT2 STREAM_INTERRUPTED",  axi_read(A_SW_CNT0 + 2*4), 5);
  ck("CNT3 SEQ_NUM_MISMATCH",    axi_read(A_SW_CNT0 + 3*4), 7);
  ck("CNT4 MEDIA_RESET (0)",     axi_read(A_SW_CNT0 + 4*4), 0);
  ck("CNT5 TIMESTAMP_UNCERTAIN", axi_read(A_SW_CNT0 + 5*4), 3);
  ck("CNT6 UNSUPPORTED_FORMAT",  axi_read(A_SW_CNT0 + 6*4), 2);
  ck("CNT7 LATE_TS (0)",         axi_read(A_SW_CNT0 + 7*4), 0);
  ck("CNT8 EARLY_TS (0)",        axi_read(A_SW_CNT0 + 8*4), 0);
  ck("CNT9 FRAMES_RX = 0x6BC",   axi_read(A_SW_CNT0 + 9*4), 123456);
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

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  dut->final();
  delete dut;
  return fails ? 1 : 0;
}
