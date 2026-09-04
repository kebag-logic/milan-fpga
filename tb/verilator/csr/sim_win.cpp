/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * P11 indexed per-stream CSR window at N_LISTENERS_P=4 / N_TALKERS_P=4
 * (docs/fpga/FPGA_DESIGN.md section 2) against MODELED lane-K engines:
 *   - LCTX/TCTX context-RAM port-B model (2-stage registered pipeline, the
 *     T2 contract) serving the slow window reads (CTRL/FMT listener side,
 *     CTRL/DMAC extra talker contexts)
 *   - SNAP atomicity: a free-running event pump increments ALL counter words
 *     of the model every cycle and freezes ONLY while snap_req && snap_ok
 *     (the engine-arbitrated burst). The latched {STATE, CNT0..9, PDUS}
 *     block must be ONE coherent epoch while events keep flowing before,
 *     between and after snaps.
 *   - lwSRP ctx master protocol: poll row map (dir=0 -> idx, dir=1 ->
 *     N_LISTENERS_P-1+idx), one-deep provisioning write (CTRL commit carries
 *     the staged SID/DMAC), hold-until-gnt, status readback into 0x85C
 *   - ACMP tbl master protocol: continuous poll, 317-bit ctx latch on gnt,
 *     SID/DMAC/STATE field extraction (offsets locked against acmp_pkg)
 *   - LCTX/TCTX CFG write bundles (window word -> engine word address map)
 *   - out-of-range index rule at N=4 (idx >= 4: reads 0, writes ignored)
 */

#include "../../common/verilator_harness.hpp"
#include "Vmilan_csr.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>

//! Cycle bound on every AXI4-Lite handshake wait: large enough that a healthy
//! DUT never reaches it, small enough that a wedged one still exits.
constexpr int kAxiGuard = 2048;
//! Poll bound on a SNAP arm: how many reads wait for the busy bit to clear.
constexpr int kSnapPollGuard = 64;

constexpr uint32_t A_STRM_SEL   = 0x800;
constexpr uint32_t A_STRM_SNAP  = 0x804;
constexpr uint32_t A_SW_CTRL    = 0x810;
constexpr uint32_t A_SW_SID_LO  = 0x814;
constexpr uint32_t A_SW_SID_HI  = 0x818;
constexpr uint32_t A_SW_DMAC_LO = 0x81C;
constexpr uint32_t A_SW_DMAC_HI = 0x820;
constexpr uint32_t A_SW_FMT_LO  = 0x824;
constexpr uint32_t A_SW_FMT_HI  = 0x828;
constexpr uint32_t A_SW_STATE   = 0x82C;
constexpr uint32_t A_SW_CNT0    = 0x830;
constexpr uint32_t A_SW_PDUS    = 0x858;
constexpr uint32_t A_SW_SRP     = 0x85C;

constexpr uint32_t A_CH_CTRL = 0x900;
constexpr uint32_t A_CH_SEL  = 0x904;
constexpr uint32_t A_CH_WORD = 0x908;
constexpr uint32_t A_CH_SNAP = 0x910;
constexpr uint32_t A_CH_LOOP = 0x914;
constexpr uint32_t POISON = 0xDEADDEADu;

namespace {

//! The window scenario: the Verilated model, the counters, the modelled
//! lane-K engines and the chmap map RAMs all belong to one object, so no
//! function below reads state a reader has to hunt for at file scope (I.2).
class CsrWindowHarness {
 public:
  int run();

 private:
  void ck(const char* what, uint64_t got, uint64_t exp);
  void set_ctx_bits(int lo, int width, uint64_t v);
  void model_pre_edge();
  void chmap_model_pre_edge();
  void posedge();
  void axi_write(uint32_t a, uint32_t d);
  uint32_t axi_read(uint32_t a);
  void snap_and_wait();
  uint32_t chmap_snap(uint32_t sel);

  void slow_window_reads_via_the_port_b_model();
  void cfg_write_bundles_reach_the_engine_words();
  void snap_block_is_one_coherent_epoch();
  void out_of_range_snap_wipes_the_cnt_block();
  void lwsrp_ctx_master_maps_provisions_and_reports();
  void acmp_tbl_master_latches_and_extracts();
  void adp_shape_is_read_only_and_comes_from_the_config();
  void out_of_range_index_reads_zero_and_ignores_writes();
  void chmap_map_ram_readback();
  void chmap_unarmed_state_is_poison_not_zero();
  void chmap_program_capture_channel_five();
  uint32_t chmap_slot_is_mapped_and_fed();
  uint32_t chmap_slot_is_mapped_but_never_fed(uint32_t v);
  void chmap_slot_is_not_in_the_map(uint32_t v2);
  void chmap_render_side_declares_no_mask();
  void chmap_declared_but_silent_port_poisons(uint32_t v2);
  void chmap_recovers_after_the_timeout();

  const milan::tb::Model<Vmilan_csr> model;
  Vmilan_csr* dut = model.get();
  long checks = 0;
  long fails = 0;

  // ----------------------------------------------------------------- models
  uint32_t lctx[8][32] = {};        // {s[2:0], word[4:0]}
  uint32_t tctx[8][16] = {};        // {t[2:0], word[3:0]}
  // port-B registered pipelines
  uint32_t l_q1 = 0;
  uint32_t l_q2 = 0;
  uint32_t t_q1 = 0;
  uint32_t t_q2 = 0;
  // rd_valid pipelines (P12 contract)
  int      l_ev1 = 0;
  int      l_ev2 = 0;
  int      t_ev1 = 0;
  int      t_ev2 = 0;
  // snap_ok grant delay counters
  int      l_ok_cnt = 0;
  int      t_ok_cnt = 0;
  bool     pump_on = false;
  uint32_t evt = 0;                       // coherent event epoch

  // lwSRP ctx port model (grant one cycle after req, KL_lwsrp_ctx style) +
  // sticky capture of the last WRITE command's payload
  int      srp_gnt_next = 0;
  bool     srp_saw_wr = false;
  uint32_t srp_wr_idx = 0;
  uint32_t srp_wr_valid = 0;
  uint32_t srp_wr_dir = 0;
  uint64_t srp_wr_sid = 0;
  uint64_t srp_wr_dmac = 0;
  uint32_t srp_seen_idx_rd = 0;           // last polled (we=0) row index

  // ACMP tbl model
  int      acmp_gnt_next = 0;

  // ------------------------------------------------------------------ chmap
  //  Model of the two channel-map RAMs behind the 0x910/0x914 readback port.
  //  This executable is built with -GCHMAP_RDBK_P=3, i.e. "both read ports are
  //  wired", which is what the milan_datapath patch does.
  //
  //  Shapes are the REAL ones, not convenient ones:
  //    - the CSR's 16-bit §5 word is COMPOSED/SLICED on the way into each RAM
  //      exactly as milan_datapath wires it (CHANNEL_MAP_64.md §5 "as wired
  //      today"): render keeps its 8-bit slice, capture composes the 13-bit
  //      PER-CHANNEL entry {en, half, src, idxh, idx} (0x0027), so a
  //      round-trip test proves the transport, not a tautology;
  //    - the capture RAM answers one clock after a held map_rd_en_i, the
  //      registered read port KL_chan_map_capture actually has;
  //    - the capture readback word is the per-channel view
  //      {1'b0, loop_fed[14], loop_mapped[13], entry[12:0]}. loop_fed is a
  //      property only the FABRIC can know (has any audio ever reached this
  //      channel?) - here it is a TB-owned flag, which is the point: the CSR
  //      must transport it, never synthesise it.
  uint16_t cmap_ram[64] = {};                 // 13-bit per-CHANNEL entries
  uint8_t  rmap_ram[64] = {};                 // 8-bit render entries
  bool     cmap_fed[64] = {};                 // fabric's "ever fed" observation
  bool     chmap_answer = true;               // false = declared but silent
  int      chmap_v_q = 0;                     // registered read-port pipeline
  uint32_t chmap_d_q = 0;

  // sticky captures of the CFG write bundles
  bool     seen_lctx_wr = false;
  bool     seen_tctx_wr = false;
  uint32_t lctx_wr_addr = 0;
  uint32_t lctx_wr_data = 0;
  uint32_t tctx_wr_addr = 0;
  uint32_t tctx_wr_data = 0;
};

void CsrWindowHarness::ck(const char* what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("  [FAIL] %-44s got=0x%llx exp=0x%llx\n", what,
           static_cast<unsigned long long>(got),
           static_cast<unsigned long long>(exp));
  } else {
    printf("  [ok]   %-44s = 0x%llx\n", what,
           static_cast<unsigned long long>(got));
  }
}

void CsrWindowHarness::set_ctx_bits(int lo, int width, uint64_t v) {
  for (int i = 0; i < width; i++) {
    int b = lo + i;
    if ((v >> i) & 1) dut->i_acmp_tbl_ctx[b >> 5] |=  (1u << (b & 31));
    else              dut->i_acmp_tbl_ctx[b >> 5] &= ~(1u << (b & 31));
  }
}

void CsrWindowHarness::model_pre_edge() {
  dut->eval();
  // event pump: every counter word of every stream carries the SAME epoch
  // value; frozen only while the engine has granted a coherent burst
  bool l_frozen = dut->o_lctx_snap_req && dut->i_lctx_snap_ok;
  bool t_frozen = dut->o_tctx_snap_req && dut->i_tctx_snap_ok;
  if (pump_on && !l_frozen && !t_frozen) {
    evt++;
    for (int s = 0; s < 8; s++) {
      for (int w = 16; w <= 25; w++) lctx[s][w] = evt;   // CNT0..9
      lctx[s][11] = evt;                                 // PDUS
      lctx[s][8]  = ((evt & 0xFF) << 14) | (1u << 12);   // wire_chans, locked
      tctx[s][5]  = evt;                                 // talker FRAMES
    }
  }
  // port-B pipelines: present q2, then shift (data valid 2 edges after addr).
  // P12 contract: rd_valid mirrors the data pipeline (valid = rd_en two
  // edges ago) — an always-idle engine model, the P11 timing exactly.
  uint32_t la = dut->o_lctx_rd_addr;
  uint32_t ta = dut->o_tctx_rd_addr;
  dut->i_lctx_rd_data = l_q2;
  l_q2 = l_q1; l_q1 = lctx[(la >> 5) & 7][la & 31];
  dut->i_lctx_rd_valid = l_ev2;
  l_ev2 = l_ev1; l_ev1 = dut->o_lctx_rd_en & 1;
  dut->i_tctx_rd_data = t_q2;
  t_q2 = t_q1; t_q1 = tctx[(ta >> 4) & 7][ta & 15];
  dut->i_tctx_rd_valid = t_ev2;
  t_ev2 = t_ev1; t_ev1 = dut->o_tctx_rd_en & 1;
  // snap_ok: granted 3 cycles into a held request
  l_ok_cnt = dut->o_lctx_snap_req ? l_ok_cnt + 1 : 0;
  t_ok_cnt = dut->o_tctx_snap_req ? t_ok_cnt + 1 : 0;
  dut->i_lctx_snap_ok = (l_ok_cnt >= 3);
  dut->i_tctx_snap_ok = (t_ok_cnt >= 3);
  // lwSRP ctx port: capture the command at its service beat (req && !gnt),
  // grant one cycle later
  dut->i_srp_ctx_gnt = srp_gnt_next;
  dut->eval();
  if (dut->o_srp_ctx_req && !dut->i_srp_ctx_gnt) {
    if (dut->o_srp_ctx_we) {
      srp_saw_wr   = true;
      srp_wr_idx   = dut->o_srp_ctx_idx;
      srp_wr_valid = dut->o_srp_ctx_valid;
      srp_wr_dir   = dut->o_srp_ctx_dir;
      srp_wr_sid   = dut->o_srp_ctx_sid;
      srp_wr_dmac  = dut->o_srp_ctx_dmac;
    } else {
      srp_seen_idx_rd = dut->o_srp_ctx_idx;
    }
    srp_gnt_next = 1;
  } else {
    srp_gnt_next = 0;
  }
  // ACMP tbl port: same grant shape; ctx word is preloaded by the test
  dut->i_acmp_tbl_gnt = acmp_gnt_next;
  dut->eval();
  acmp_gnt_next = (dut->o_acmp_tbl_req && !dut->i_acmp_tbl_gnt) ? 1 : 0;
}

void CsrWindowHarness::chmap_model_pre_edge() {
  dut->i_chmap_rd_valid = chmap_v_q;
  dut->i_chmap_rd_data  = chmap_d_q;
  dut->eval();
  if (dut->o_chmap_rd_en && chmap_answer) {
    int a = dut->o_chmap_rd_addr & 63;
    chmap_v_q = 1;
    if (dut->o_chmap_rd_side)                       // CMAP (capture)
      chmap_d_q = (static_cast<uint32_t>(cmap_fed[a] ? 1 : 0) << 14) |
                  (static_cast<uint32_t>((cmap_ram[a] >> 12) & 1) << 13) |
                  static_cast<uint32_t>(cmap_ram[a] & 0x1FFF);
    else                                            // RMAP (render): no mask
      chmap_d_q = static_cast<uint32_t>(rmap_ram[a]);
  } else {
    chmap_v_q = 0;
  }
}

void CsrWindowHarness::posedge() {
  model_pre_edge();
  chmap_model_pre_edge();
  dut->aclk = 1; dut->eval();
  // the shared map write port, sliced as milan_datapath slices it
  if (dut->o_chmap_wr_en) {
    int a = dut->o_chmap_wr_addr & 63;
    uint32_t d = dut->o_chmap_wr_data;
    if (dut->o_chmap_wr_side)   // capture (0x0027): compose the 13-bit
                                // entry {en, half=WORD[8], src, idxh, idx}
      cmap_ram[a] = static_cast<uint16_t>((((d >> 15) & 1) << 12) |
                                          (((d >>  8) & 1) << 11) |
                                          (((d >> 12) & 7) <<  8) | (d & 0xFF));
    else                        // render:  {en[15], src[12], idx[6:4], idx[2:0]}
      rmap_ram[a] = static_cast<uint8_t>((((d >> 15) & 1) << 7) |
                                         (((d >> 12) & 1) << 6) |
                                         (((d >> 4) & 7) << 3) | (d & 7));
  }
  if (dut->o_lctx_wr_p) {
    seen_lctx_wr = true;
    lctx_wr_addr = dut->o_lctx_wr_addr; lctx_wr_data = dut->o_lctx_wr_data;
  }
  if (dut->o_tctx_wr_p) {
    seen_tctx_wr = true;
    tctx_wr_addr = dut->o_tctx_wr_addr; tctx_wr_data = dut->o_tctx_wr_data;
  }
  dut->aclk = 0; dut->eval();
}

void CsrWindowHarness::axi_write(uint32_t a, uint32_t d) {
  dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
  dut->s_axi_wdata  = d; dut->s_axi_wvalid  = 1; dut->s_axi_wstrb = 0xF;
  dut->s_axi_bready = 1;
  for (int g = 0; g < kAxiGuard; ++g) {
    dut->eval();
    bool acc = dut->s_axi_awready && dut->s_axi_wready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
  for (int g = 0; g < kAxiGuard; ++g) {
    dut->eval();
    if (dut->s_axi_bvalid) break;
    posedge();
  }
  posedge();
  dut->s_axi_bready = 0;
}

uint32_t CsrWindowHarness::axi_read(uint32_t a) {
  dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
  for (int g = 0; g < kAxiGuard; ++g) {
    dut->eval();
    bool acc = dut->s_axi_arready;
    posedge();
    if (acc) break;
  }
  dut->s_axi_arvalid = 0;
  uint32_t v = 0;
  for (int g = 0; g < kAxiGuard; ++g) {
    dut->eval();
    if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; }
    posedge();
  }
  posedge();
  dut->s_axi_rready = 0;
  return v;
}

void CsrWindowHarness::snap_and_wait() {
  axi_write(A_STRM_SNAP, 1);
  for (int g = 0; g < kSnapPollGuard; ++g)
    if (axi_read(A_STRM_SNAP) == 0) return;
}

void CsrWindowHarness::slow_window_reads_via_the_port_b_model() {
  printf("-- slow window reads from the LCTX port-B model --\n");
  lctx[2][4] = 0xC0DE0004;   // CTRL
  lctx[2][2] = 0xC0DE0002;   // FMT_LO
  lctx[2][3] = 0xC0DE0003;   // FMT_HI
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  ck("LCTX CTRL (w4) via port B",  axi_read(A_SW_CTRL),   0xC0DE0004);
  ck("LCTX FMT_LO (w2) via port B", axi_read(A_SW_FMT_LO), 0xC0DE0002);
  ck("LCTX FMT_HI (w3) via port B", axi_read(A_SW_FMT_HI), 0xC0DE0003);
  tctx[3][0] = 0xBEEF0000; tctx[3][1] = 0xBEEF0001; tctx[3][2] = 0xBEEF0002;
  axi_write(A_STRM_SEL, 0x103);              // dir=1 idx=3
  ck("TCTX CTRL (w0) via port B",    axi_read(A_SW_CTRL),    0xBEEF0000);
  ck("TCTX DMAC_LO (w1) via port B", axi_read(A_SW_DMAC_LO), 0xBEEF0001);
  ck("TCTX DMAC_HI (w2) via port B", axi_read(A_SW_DMAC_HI), 0xBEEF0002);
}

void CsrWindowHarness::cfg_write_bundles_reach_the_engine_words() {
  printf("-- CFG write bundles: window word -> engine word map --\n");
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  seen_lctx_wr = false;
  axi_write(A_SW_FMT_LO, 0xAB01);
  ck("FMT_LO write pulsed LCTX", seen_lctx_wr, 1);
  ck("LCTX wr addr {s=2,w=2}", lctx_wr_addr, (2u << 5) | 2u);
  ck("LCTX wr data", lctx_wr_data, 0xAB01);
  seen_lctx_wr = false;
  axi_write(A_SW_SID_LO, 0x5511);
  ck("SID_LO write -> LCTX w0", lctx_wr_addr, (2u << 5) | 0u);
  axi_write(A_STRM_SEL, 0x103);              // dir=1 idx=3
  seen_tctx_wr = false;
  axi_write(A_SW_DMAC_HI, 0x91E0);
  ck("DMAC_HI write pulsed TCTX", seen_tctx_wr, 1);
  ck("TCTX wr addr {t=3,w=2}", tctx_wr_addr, (3u << 4) | 2u);
  ck("TCTX wr data", tctx_wr_data, 0x91E0);
}

void CsrWindowHarness::snap_block_is_one_coherent_epoch() {
  printf("-- SNAP atomicity: coherent block while events keep flowing --\n");
  pump_on = true;
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  for (int i = 0; i < 20; ++i) posedge();    // let events flow
  axi_write(A_STRM_SNAP, 1);
  ck("SNAP busy while bursting", axi_read(A_STRM_SNAP) & 1, 1);
  for (int g = 0; g < kSnapPollGuard; ++g) if (axi_read(A_STRM_SNAP) == 0) break;
  uint32_t v1 = axi_read(A_SW_CNT0);
  ck("snap epoch nonzero", v1 != 0, 1);
  bool coh = true;
  for (int k = 0; k < 10; ++k)
    if (axi_read(A_SW_CNT0 + 4*k) != v1) coh = false;
  if (axi_read(A_SW_PDUS) != v1) coh = false;
  ck("CNT0..9 + PDUS one epoch", coh, 1);
  uint32_t st1 = axi_read(A_SW_STATE);
  ck("STATE wire_chans same epoch", (st1 >> 11) & 0xFF, v1 & 0xFF);
  ck("STATE media_locked (m8[12])", (st1 >> 10) & 1, 1);
  // events kept flowing: a later snap latches a LARGER, again-coherent epoch
  for (int i = 0; i < 30; ++i) posedge();
  snap_and_wait();
  uint32_t v2 = axi_read(A_SW_CNT0);
  ck("second snap advanced", v2 > v1, 1);
  coh = true;
  for (int k = 0; k < 10; ++k)
    if (axi_read(A_SW_CNT0 + 4*k) != v2) coh = false;
  if (axi_read(A_SW_PDUS) != v2) coh = false;
  ck("second snap coherent", coh, 1);
  // talker snap: TCTX w5 -> PDUS, CNT block zero
  axi_write(A_STRM_SEL, 0x101);              // dir=1 idx=1
  snap_and_wait();
  uint32_t vt = axi_read(A_SW_PDUS);
  ck("talker PDUS = TCTX w5 epoch", vt != 0 && vt >= v2, 1);
  ck("talker CNT0 poison (not-backed rule 2026-07-26)", axi_read(A_SW_CNT0), 0xDEADDEADu);
}

// An out-of-range SNAP must WIPE the latched CNT block: re-selecting an
// IN-RANGE index afterwards, without re-arming, has to read 0 and never
// the previous selection's counters. Parking SEL out of range proves
// nothing on its own - win_in_range_w already returns 0 for that - so the
// read has to happen with SEL back in range, and the block has to hold
// real walk data first (a blank one passes whatever the RTL does).
void CsrWindowHarness::out_of_range_snap_wipes_the_cnt_block() {
  axi_write(A_STRM_SEL, 0x002);              // dir=0 idx=2
  for (int i = 0; i < 20; ++i) posedge();
  snap_and_wait();
  pump_on = false;
  uint32_t v3 = axi_read(A_SW_CNT0);
  ck("re-latched listener CNT block is populated", v3 != 0, 1);
  axi_write(A_STRM_SEL, 0x004);              // idx 4 >= N_LISTENERS_P=4
  snap_and_wait();
  axi_write(A_STRM_SEL, 0x002);              // back in range, NO re-arm
  bool wiped = true;
  for (int k = 0; k < 10; ++k)
    if (axi_read(A_SW_CNT0 + 4*k) != 0) wiped = false;
  ck("out-of-range SNAP wipes the CNT block", wiped, 1);
}

void CsrWindowHarness::lwsrp_ctx_master_maps_provisions_and_reports() {
  printf("-- lwSRP ctx master: row map, provisioning, status readback --\n");
  axi_write(A_STRM_SEL, 0x003);              // dir=0 idx=3 -> poll row 3
  dut->i_srp_ctx_rd_stat = 0x8123;           // engine-held snapshot
  dut->i_srp_ctx_rd_sid  = 0x1122334455667788ULL;
  for (int i = 0; i < 10; ++i) posedge();    // let a poll grant land
  ck("poll row = idx (dir=0)", srp_seen_idx_rd, 3);
  ck("SRP word = {16'0, rd_stat}", axi_read(A_SW_SRP), 0x8123);
  axi_write(A_STRM_SEL, 0x102);              // dir=1 idx=2 -> row 4-1+2 = 5
  for (int i = 0; i < 10; ++i) posedge();
  ck("poll row = N_L-1+idx (dir=1)", srp_seen_idx_rd, 5);
  ck("talker SID_LO = ctx rd_sid", axi_read(A_SW_SID_LO), 0x55667788);
  ck("talker SID_HI = ctx rd_sid", axi_read(A_SW_SID_HI), 0x11223344);
  // provisioning: stage SID/DMAC, commit with CTRL.en=1
  srp_saw_wr = false;
  axi_write(A_SW_SID_LO, 0x0000AAAA);
  axi_write(A_SW_SID_HI, 0x02000000);
  axi_write(A_SW_DMAC_LO, 0xF000FE05);
  axi_write(A_SW_DMAC_HI, 0x000091E0);
  axi_write(A_SW_CTRL, 1);
  for (int i = 0; i < 10; ++i) posedge();
  ck("provision write granted", srp_saw_wr, 1);
  ck("provision row", srp_wr_idx, 5);
  ck("provision valid", srp_wr_valid, 1);
  ck("provision dir (ctx enc: talker=0)", srp_wr_dir, 0);
  ck("provision sid staged", srp_wr_sid, 0x020000000000AAAAULL);
  ck("provision dmac staged", srp_wr_dmac, 0x91E0F000FE05ULL);
  // withdraw: CTRL.en=0 -> valid=0 write to the same row
  srp_saw_wr = false;
  axi_write(A_SW_CTRL, 0);
  for (int i = 0; i < 10; ++i) posedge();
  ck("withdraw granted", srp_saw_wr, 1);
  ck("withdraw valid=0", srp_wr_valid, 0);
  // listener provisioning carries ctx dir=1
  axi_write(A_STRM_SEL, 0x001);              // dir=0 idx=1 -> row 1
  srp_saw_wr = false;
  axi_write(A_SW_CTRL, 1);
  for (int i = 0; i < 10; ++i) posedge();
  ck("listener provision row", srp_wr_idx, 1);
  ck("listener provision dir=1", srp_wr_dir, 1);
}

void CsrWindowHarness::acmp_tbl_master_latches_and_extracts() {
  printf("-- ACMP tbl master: 317-bit ctx latch + field extraction --\n");
  set_ctx_bits(0, 64, 0x680500FFFE0000AAULL);    // ctlr (E2)
  set_ctx_bits(128, 64, 0xAABBCCDD00112233ULL);  // sid
  set_ctx_bits(192, 48, 0x91E0F0004455ULL);      // dmac
  set_ctx_bits(252, 16, 0x0008);                 // flags STREAMING_WAIT (E2)
  set_ctx_bits(268, 16, 0x0005);                 // tuid (E2)
  set_ctx_bits(305, 5, 21);                      // status
  set_ctx_bits(310, 2, 1);                       // probing
  set_ctx_bits(314, 3, 7);                       // state
  axi_write(A_STRM_SEL, 0x001);              // dir=0 idx=1 (re-latch fresh)
  for (int i = 0; i < 10; ++i) posedge();
  ck("acmp SID_LO",  axi_read(A_SW_SID_LO),  0x00112233);
  ck("acmp SID_HI",  axi_read(A_SW_SID_HI),  0xAABBCCDD);
  ck("acmp DMAC_LO", axi_read(A_SW_DMAC_LO), 0xF0004455);
  ck("acmp DMAC_HI", axi_read(A_SW_DMAC_HI), 0x91E0);
  // E2: the remaining persisted binding fields at 0x860/0x864/0x868
  ck("acmp CTLR_LO (E2)", axi_read(0x860), 0xFE0000AA);
  ck("acmp CTLR_HI (E2)", axi_read(0x864), 0x680500FF);
  ck("acmp BIND {flags,tuid} (E2)", axi_read(0x868), 0x00080005);
  ck("window hole 0x86C poison (not-backed rule)", axi_read(0x86C), 0xDEADDEADu);
  axi_write(A_STRM_SEL, 0x101);              // dir=1: listener-only words
  for (int i = 0; i < 10; ++i) posedge();
  ck("talker dir CTLR_LO poison (E2, not-backed rule)", axi_read(0x860), 0xDEADDEADu);
  ck("talker dir BIND poison (E2, not-backed rule)",    axi_read(0x868), 0xDEADDEADu);
  axi_write(A_STRM_SEL, 0x001);              // back to the listener ctx
  for (int i = 0; i < 10; ++i) posedge();
  dut->i_srp_ctx_rd_stat = 0;                // keep the STATE srp9 field 0
  pump_on = true;
  snap_and_wait();
  pump_on = false;
  uint32_t st = axi_read(A_SW_STATE);
  ck("STATE acmp state",   st & 7, 7);
  ck("STATE acmp probing", (st >> 3) & 3, 1);
  ck("STATE acmp status",  (st >> 5) & 31, 21);
}

// A SECOND config's shape: this executable is built with
// +incdir+configs/generated/endstation_arty_4x4, whose generated
// adp_shape_defaults.svh says 5 sources / 5 sinks (4 AAF + the CRF Media
// Clock Output / sink) and sets MEDIA_CLOCK_SOURCE because that config HAS
// a CRF output. sim_main.cpp reads 1/2 with caps 0x4001 off the tracked 1x1
// default. Same RTL, same registers, different end-station config - which
// is what "software-defined" has to mean for a count that hardware owns.
void CsrWindowHarness::adp_shape_is_read_only_and_comes_from_the_config() {
  printf("-- ADP shape is RO and comes from the 4x4 config (5/5) --\n");
  ck("ADP_TALK = {0x4801, 5}", axi_read(0x618), 0x48010005u);
  ck("ADP_LIST = {0x4801, 5}", axi_read(0x61C), 0x48010005u);
  axi_write(0x618, 0x48010001);
  axi_write(0x61C, 0x48010002);
  for (int i = 0; i < 4; ++i) posedge();
  ck("ADP_TALK still 5 after a write", axi_read(0x618), 0x48010005u);
  ck("ADP_LIST still 5 after a write", axi_read(0x61C), 0x48010005u);
}

void CsrWindowHarness::out_of_range_index_reads_zero_and_ignores_writes() {
  printf("-- out-of-range at N=4: idx 4+ reads 0 / writes ignored --\n");
  axi_write(A_STRM_SEL, 0x004);              // dir=0 idx=4: OUT of range
  seen_lctx_wr = false; srp_saw_wr = false;
  axi_write(A_SW_CTRL, 0xFF);
  axi_write(A_SW_SID_LO, 0x1234);
  for (int i = 0; i < 10; ++i) posedge();
  ck("oor CTRL reads 0",   axi_read(A_SW_CTRL), 0);
  ck("oor SID_LO reads 0", axi_read(A_SW_SID_LO), 0);
  ck("oor SRP reads 0",    axi_read(A_SW_SRP), 0);
  ck("oor CTLR_LO reads 0 (E2)", axi_read(0x860), 0);
  ck("oor BIND reads 0 (E2)",    axi_read(0x868), 0);
  ck("oor no LCTX write",  seen_lctx_wr, 0);
  ck("oor no SRP provision", srp_saw_wr, 0);
  ck("oor SEL readback intact", axi_read(A_STRM_SEL), 0x004);
}

uint32_t CsrWindowHarness::chmap_snap(uint32_t sel) {
  axi_write(A_CH_SEL, sel);
  axi_write(A_CH_SNAP, 1);
  for (int g = 0; g < kSnapPollGuard; ++g)
    if ((axi_read(A_CH_SNAP) & 1) == 0) break;
  return axi_read(A_CH_LOOP);
}

// un-armed state FIRST: the 0x800 window's "reads 0 until SNAP" trap
// must NOT be reproduced here
void CsrWindowHarness::chmap_unarmed_state_is_poison_not_zero() {
  ck("LOOP un-armed is POISON not 0", axi_read(A_CH_LOOP), POISON);
  uint32_t s = axi_read(A_CH_SNAP);
  ck("SNAP tag 0xC5",           (s >> 24) & 0xFF, 0xC5);
  ck("SNAP cap = 3 (both ports wired)", (s >> 8) & 3, 3);
  ck("SNAP armed = 0 at reset", (s >> 4) & 1, 0);
}

// program capture CHANNEL 5 through the debug write port. 0x9000 =
// EN | I2S_IN | pair 0, L half (CHANNEL_MAP_64.md §5 worked example),
// which the datapath composes into the 13-bit entry 0x1100 (0x0027).
void CsrWindowHarness::chmap_program_capture_channel_five() {
  axi_write(A_CH_CTRL, 1);                    // arm the override
  axi_write(A_CH_SEL, 0x105);                 // side = capture, index = 5
  axi_write(A_CH_WORD, 0x9000);
  for (int i = 0; i < 4; ++i) posedge();
  ck("fabric RAM took the composed entry", cmap_ram[5], 0x1100);
}

// ---- state 1: mapped AND fed -------------------------------------
uint32_t CsrWindowHarness::chmap_slot_is_mapped_and_fed() {
  cmap_fed[5] = true;
  uint32_t v = chmap_snap(0x105);
  ck("S1 read-back-what-was-written", v & 0x1FFF, 0x1100);
  ck("S1 valid",       (v >> 26) & 1, 1);
  ck("S1 mask_valid",  (v >> 27) & 1, 1);
  ck("S1 mapped",      (v >> 16) & 1, 1);
  ck("S1 fed",         (v >> 17) & 1, 1);
  ck("S1 LOOP_SUSPECT",(v >> 18) & 1, 0);
  ck("S1 {side,index} echo", (v >> 19) & 0x7F, (5u << 1) | 1u);
  ck("S1 whole word", v, 0x0C5B7100u);
  return v;
}

// ---- state 2: MAPPED BUT NEVER FED (the defect signature) ---------
//  same map entry, same CSR shadow, same 0x908 readback - the ONLY
//  thing that changed is a fabric observation, and it is now visible.
uint32_t CsrWindowHarness::chmap_slot_is_mapped_but_never_fed(uint32_t v) {
  cmap_fed[5] = false;
  uint32_t v2 = chmap_snap(0x105);
  ck("S2 same entry as S1",   v2 & 0x1FFF, 0x1100);
  ck("S2 mapped",            (v2 >> 16) & 1, 1);
  ck("S2 fed",               (v2 >> 17) & 1, 0);
  ck("S2 LOOP_SUSPECT",      (v2 >> 18) & 1, 1);
  ck("S2 whole word", v2, 0x0C5D3100u);
  ck("S2 differs from S1", v2 != v, 1);
  ck("0x908 shadow CANNOT see it", axi_read(A_CH_WORD), 0x9000);
  return v2;
}

// ---- state 3: the slot is not in the map at all --------------------
void CsrWindowHarness::chmap_slot_is_not_in_the_map(uint32_t v2) {
  uint32_t v3 = chmap_snap(0x106);            // index 6, never written
  ck("S3 entry is 0",        v3 & 0xFFFF, 0);
  ck("S3 mapped",           (v3 >> 16) & 1, 0);
  ck("S3 fed",              (v3 >> 17) & 1, 0);
  ck("S3 LOOP_SUSPECT",     (v3 >> 18) & 1, 0);
  ck("S3 valid (a MEASURED zero)", (v3 >> 26) & 1, 1);
  ck("S3 whole word", v3, 0x0C680000u);
  ck("S3 is not POISON",     v3 != POISON, 1);
  ck("S3 differs from S2",   v3 != v2, 1);
}

// ---- render side: no loopback mask, and it SAYS so -----------------
//  KL_chan_map_render's readback carries the entry only. Reporting
//  mapped=0/fed=0 there would be exactly the structural zero this
//  register exists to kill, so mask_valid goes to 0 and the register
//  map says the EN bit is raw[7] on that side.
void CsrWindowHarness::chmap_render_side_declares_no_mask() {
  rmap_ram[2] = 0x91;                          // EN | AVB | s=2 | c=1
  uint32_t vr = chmap_snap(0x002);             // side = render, index = 2
  ck("R entry from the render RAM", vr & 0xFFFF, 0x0091);
  ck("R valid",       (vr >> 26) & 1, 1);
  ck("R mask_valid = 0 (no mask on this side)", (vr >> 27) & 1, 0);
  ck("R whole word", vr, 0x04200091u);
}

// ---- NEGATIVE CONTROL: declared capable, and silent ----------------
//  CHMAP_RDBK_P is a DECLARATION. The watchdog is what holds it to the
//  wire: a port that never answers must poison the data word, not
//  latch whatever the bus held and not hang busy forever.
void CsrWindowHarness::chmap_declared_but_silent_port_poisons(uint32_t v2) {
  chmap_answer = false;
  axi_write(A_CH_SEL, 0x105);
  axi_write(A_CH_SNAP, 1);
  bool cleared = false;
  for (int g = 0; g < kSnapPollGuard; ++g)
    if ((axi_read(A_CH_SNAP) & 1) == 0) { cleared = true; break; }
  uint32_t st = axi_read(A_CH_SNAP);
  ck("silent port: busy cleared",  cleared, 1);
  ck("silent port: timeout = 1",  (st >> 2) & 1, 1);
  ck("silent port: valid = 0",    (st >> 1) & 1, 0);
  ck("silent port: unsup = 0",    (st >> 3) & 1, 0);   // declared, not absent
  ck("silent port: LOOP is POISON", axi_read(A_CH_LOOP), POISON);
  ck("silent port did NOT keep S2", axi_read(A_CH_LOOP) != v2, 1);
  chmap_answer = true;
}

// recovery: the next snapshot measures again
void CsrWindowHarness::chmap_recovers_after_the_timeout() {
  cmap_fed[5] = true;
  uint32_t v4 = chmap_snap(0x105);
  ck("recovered after timeout", v4, 0x0C5B7100u);
  ck("timeout flag cleared by the new arm", (axi_read(A_CH_SNAP) >> 2) & 1, 0);
  axi_write(A_CH_CTRL, 0);
}

// ------------------------------------------------------------------ //
//  chmap map-RAM readback (CHMAP_SNAP 0x910 / CHMAP_LOOP 0x914)
//
//  ORACLE: the fabric. Everything checked here is a word the modelled map
//  RAM returned on its read port; nothing is reconstructed from what
//  software wrote. That distinction IS the defect: CHMAP_WORD 0x908 reads
//  back milan_csr's own shadow, so before this register a board could not
//  tell a mapped-and-quiet slot from a slot that was never connected -
//  both emit 24'd0.
//
//  THE THREE STATES (the property, methodology R4): on hardware that
//  routes no audio pins the only difference between "working and silent"
//  and "not wired at all" is {loop_mapped, loop_fed}, so the register is
//  only useful if all three are distinguishable through the CSR:
//      mapped=1 fed=1  slot is mapped and audio has reached it
//      mapped=1 fed=0  MAPPED BUT NEVER FED  <- the mis-wired loopback
//      mapped=0        the slot is not in the map at all
// ------------------------------------------------------------------ //
void CsrWindowHarness::chmap_map_ram_readback() {
  long f0 = fails;

  printf("-- chmap map-RAM readback: 0x910 SNAP / 0x914 LOOP --\n");
  chmap_unarmed_state_is_poison_not_zero();
  chmap_program_capture_channel_five();
  const uint32_t v = chmap_slot_is_mapped_and_fed();
  const uint32_t v2 = chmap_slot_is_mapped_but_never_fed(v);
  chmap_slot_is_not_in_the_map(v2);
  chmap_render_side_declares_no_mask();
  chmap_declared_but_silent_port_poisons(v2);
  chmap_recovers_after_the_timeout();
  printf("  [%s] chmap readback: mapped/fed/unmapped are distinguishable,"
         " and a silent port poisons\n", (fails == f0) ? "PASS" : "FAIL");
}

int CsrWindowHarness::run() {
  memset(lctx, 0, sizeof lctx); memset(tctx, 0, sizeof tctx);
  // P12: CFG-word writes are held until the engine's wr_rdy; the model
  // accepts every cycle (arbitration under load is the milan_dp NxN TB's job)
  dut->i_lctx_wr_rdy = 1; dut->i_tctx_wr_rdy = 1;

  dut->aresetn = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_bready = 0;
  dut->s_axi_arvalid = dut->s_axi_rready = 0;
  for (int i = 0; i < 5; ++i) posedge();
  dut->aresetn = 1; posedge();

  printf("== milan_csr P11 window, N=4x4, modeled lane-K engines ==\n");

  slow_window_reads_via_the_port_b_model();
  cfg_write_bundles_reach_the_engine_words();
  snap_block_is_one_coherent_epoch();
  out_of_range_snap_wipes_the_cnt_block();
  lwsrp_ctx_master_maps_provisions_and_reports();
  acmp_tbl_master_latches_and_extracts();
  adp_shape_is_read_only_and_comes_from_the_config();
  out_of_range_index_reads_zero_and_ignores_writes();
  chmap_map_ram_readback();

  printf("--------------------------------------------------------------\n");
  printf("checks: %ld   failures: %ld\n", checks, fails);
  printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  CsrWindowHarness harness;
  return harness.run();
}
