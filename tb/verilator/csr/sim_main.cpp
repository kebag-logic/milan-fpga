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
  for (int g = 0; g < 64; ++g) {
    dut->eval();
    bool acc = dut->s_axi_awready && dut->s_axi_wready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
  for (int g = 0; g < 64; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; posedge(); }
  posedge();                       // consume bvalid (bready=1)
  dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint32_t a) {
  dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
  for (int g = 0; g < 64; ++g) {
    dut->eval();
    bool acc = dut->s_axi_arready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t v = 0;
  for (int g = 0; g < 64; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } posedge(); }
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
  for (int k = 0; k < 9; ++k) dut->i_stats[k] = 0;
  for (int i = 0; i < 5; ++i) posedge();
  dut->aresetn = 1; posedge();

  printf("== milan_csr AXI4-Lite CSR verification ==\n");

  printf("-- identification / capabilities --\n");
  ck("ID",            axi_read(A_ID),      0x4D494C4E);
  ck("VERSION",       axi_read(A_VERSION), 0x00010003);
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

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  dut->final();
  delete dut;
  return fails ? 1 : 0;
}
