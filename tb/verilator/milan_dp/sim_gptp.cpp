// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The GPTP_PLANE_EN_P=1 elaboration smoke (issue #114): the option-ON
// datapath builds, and the plane's boot Pdelay_Req emerges at the REAL
// MAC boundary through the real merge chain (gptp_ctl_mux -> adp_tx_mux)
// with NOTHING driven but clocks and resets -- the plane's own timer
// cadence is the stimulus. It then plays one peer through the real wide
// RX tap, establishes a nonzero committed publication bank, and grades
// that bank byte-exactly in GET_AVB_INFO / GET_AS_PATH responses at the
// real MAC boundary. A selected Sync then proves CLOCK_DOMAIN lock/unlock,
// descriptor-specific GET_COUNTERS dirty notifications, and the shared AAF /
// CRF tu wire. The donor's own suites remain the deep state-machine oracle;
// THIS leg pins every integration seam in the real datapath.
//
// MILAN_CLK_FREQ_HZ=2 MHz for this leg so the 1200 ms boot cadence
// fires within a runnable window; the ucode hex is generated for the
// same clock (see the Makefile rule).

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <algorithm>
#include <filesystem>
#include <string>
#include <vector>
#include <unistd.h>
#include <verilated.h>
#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"

#ifndef PP_MS_CYC_TB
#error "Makefile must couple PP_MS_CYC_TB to GPP_TIM_DIV_MS_P"
#endif

constexpr uint64_t PEER_CID = 0x0080E1FFFE112233ull;
constexpr uint64_t GMID = 0x00AACCFFFE010203ull;
constexpr uint64_t GMID_EMPTY = 0x00AACCFFFE010204ull;
constexpr uint64_t PATH_B1 = 0x001122FFFE000011ull;
constexpr uint64_t PATH_B2 = 0x001122FFFE000022ull;
constexpr uint64_t PATH_B2_NEW = 0x445566FFFE000033ull;
constexpr uint64_t PATH_B3 = 0x001122FFFE000044ull;
constexpr uint64_t PATH_B4 = 0x001122FFFE000055ull;
constexpr uint64_t PATH_B5 = 0x001122FFFE000066ull;
constexpr uint64_t PATH_B6 = 0x001122FFFE000077ull;
constexpr uint32_t PEER_CQ = 0xF8FE436A;

//! Fabric cycles in one PROCESSOR millisecond. The Makefile derives it from
//! the same variable that sets -GPP_TIM_DIV_MS_P, so the two cannot drift;
//! the #error above refuses a build that forgot to pass it.
constexpr uint64_t kPpMsCyc = PP_MS_CYC_TB;

namespace {

//! The whole option-ON gPTP plane leg: the model's memory faces, the peer
//! model, the frame log and the counted verdicts in one scope rather than at
//! file scope (I.2).
class GptpPlaneHarness {
 public:
  int run();

 private:
  int checks = 0;
  int fails = 0;
  void expect(const char *what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
      fails++;
      printf("FAIL %-30s got %016llx exp %016llx\n", what,
             static_cast<unsigned long long>(got), static_cast<unsigned long long>(exp));
    }
  }

  struct Frame {
    std::vector<uint8_t> b;
    void u8(uint8_t v) { b.push_back(v); }
    void u16(uint16_t v) { u8(v >> 8); u8(v & 0xFF); }
    void u32(uint32_t v) { u16(v >> 16); u16(v & 0xFFFF); }
    void u48(uint64_t v) { u16((v >> 32) & 0xFFFF); u32(v & 0xFFFFFFFF); }
    void u64(uint64_t v) { u32(v >> 32); u32(v & 0xFFFFFFFF); }
    void ts(uint64_t ns) { u48(ns / 1000000000ull); u32(ns % 1000000000ull); }
  };

  Frame ptp(uint8_t mtype, uint16_t seq, uint64_t corr,
                   uint16_t flags, uint16_t body_len,
                   uint64_t src = PEER_CID) {
    Frame f;
    f.u48(0x0180C200000Eull);
    f.u48(0x0080E1112233ull);
    f.u16(0x88F7);
    f.u8(0x10 | mtype); f.u8(0x02);
    f.u16(34 + body_len);
    f.u8(0); f.u8(0);
    f.u16(flags);
    f.u64(corr);
    f.u32(0);
    f.u64(src); f.u16(1);
    f.u16(seq);
    f.u8(0x05); f.u8(0x7F);
    return f;
  }

  //! The shortest legal 802.1AS Follow_Up includes the 32-byte organization
  //! extension TLV after preciseOriginTimestamp. The selected peer's one Sync
  //! pair is enough for the engine to publish sync-ok; omitting the TLV would
  //! exercise only the parser's malformed-frame rejection.
  Frame follow_up(uint16_t seq, uint64_t origin_ns) {
    Frame f = ptp(0x8, seq, 0, 0x0008, 42);
    f.ts(origin_ns);
    f.u16(0x0003); f.u16(28);
    f.u8(0x00); f.u8(0x80); f.u8(0xC2);
    f.u8(0x00); f.u8(0x00); f.u8(0x01);
    f.u32(0);
    f.u16(0);
    f.u64(0); f.u32(0);
    f.u32(0);
    return f;
  }

  // The protocol processor assembles every AECP response through this memory
  // face. Model one ordered, always-answering store; the gPTP commands do not
  // touch descriptor memory.
  static constexpr uint32_t RESP_BASE = 0x20100000u;
  static constexpr uint32_t RESP_BYTES = 592u;
  uint8_t rmem[RESP_BYTES];
  bool rm_busy = false;
  bool rm_wpend = false;
  uint32_t rm_cur = 0;
  uint32_t rm_waddr = 0;
  uint32_t rm_wstrb = 0;
  uint64_t rm_wdata = 0;
  int rm_left = 0;

  uint64_t rmem_beat(uint32_t addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {
      const uint32_t off = addr - RESP_BASE + static_cast<uint32_t>(i);
      v = (v << 8) | static_cast<uint64_t>((off < RESP_BYTES) ? rmem[off] : 0);
    }
    return v;
  }

  void rmem_drive(Vmilan_datapath *dut) {
    dut->i_resp_mem_req_ready = rm_busy ? 0 : 1;
    dut->i_resp_mem_rsp_valid = rm_busy ? 1 : 0;
    dut->i_resp_mem_rsp_data = rm_busy ? rmem_beat(rm_cur) : 0;
    dut->i_resp_mem_rsp_last = (rm_busy && rm_left == 1) ? 1 : 0;
    dut->i_resp_mem_rsp_err = 0;
    dut->i_resp_mem_wr_ready = rm_wpend ? 0 : 1;
    dut->i_resp_mem_wr_done = rm_wpend ? 1 : 0;
    dut->i_resp_mem_wr_err = 0;
  }

  void rmem_edge(Vmilan_datapath *dut) {
    if (!rm_busy) {
      if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
        rm_cur = dut->o_resp_mem_req_addr;
        rm_left = static_cast<int>(dut->o_resp_mem_req_beats);
        rm_busy = rm_left > 0;
      }
    } else if (dut->o_resp_mem_rsp_ready) {
      rm_cur += 8;
      if (--rm_left <= 0) rm_busy = false;
    }
    if (rm_wpend) {
      for (int i = 0; i < 8; i++) {
        if (rm_wstrb & (1u << i)) {
          const uint32_t off = rm_waddr - RESP_BASE + static_cast<uint32_t>(i);
          if (off < RESP_BYTES)
            rmem[off] = static_cast<uint8_t>(rm_wdata >> (56 - 8 * i));
        }
      }
      rm_wpend = false;
    } else if (dut->o_resp_mem_wr_valid && dut->i_resp_mem_wr_ready) {
      rm_waddr = dut->o_resp_mem_wr_addr;
      rm_wdata = dut->o_resp_mem_wr_data;
      rm_wstrb = dut->o_resp_mem_wr_strb;
      rm_wpend = true;
    }
  }

  static constexpr uint32_t DESC_BASE = 0x20000000u;
  std::vector<uint8_t> desc_img;
  bool dm_busy = false;
  uint32_t dm_cur = 0;
  int dm_left = 0;
  int dm_wait = 0;
  int dm_run = 0;

  struct AemiTemps {
    std::string outdir;
    std::string image;
    std::string log;
    bool keep_log = false;
    ~AemiTemps() {
      std::error_code ec;
      std::filesystem::remove_all(outdir, ec);
      std::filesystem::remove(image, ec);
      if (!keep_log) std::filesystem::remove(log, ec);
    }
    bool fail(const char *step) {
      keep_log = true;
      fprintf(stderr, "shipping AEM %s failed; log retained at %s\n",
              step, log.c_str());
      return false;
    }
  };

  bool load_shipping_aemi() {
    const int pid = static_cast<int>(getpid());
    const std::string tmp = std::filesystem::temp_directory_path().string();
    AemiTemps files{
        tmp + "/milan_gptp_bld_" + std::to_string(pid),
        tmp + "/milan_gptp_aemi_" + std::to_string(pid) + ".bin",
        tmp + "/milan_gptp_aemi_" + std::to_string(pid) + ".log"};
    char overlay[512];
    char cmd[1536];
    snprintf(cmd, sizeof cmd,
             "python3 ../../../sw/builder/endstation_builder.py "
             "../../../configs/endstation_ax7101_1x1_tdm8.yaml -o %s "
             "> %s 2>&1", files.outdir.c_str(), files.log.c_str());
    if (system(cmd) != 0) return files.fail("builder");
    snprintf(overlay, sizeof overlay,
             "%s/endstation_ax7101_1x1_tdm8/aem_overlay.json",
             files.outdir.c_str());
    snprintf(cmd, sizeof cmd,
             "python3 ../../../avdecc/gen_aemi_image.py --overlay %s "
             "--line-bytes 576 -o %s >> %s 2>&1", overlay,
             files.image.c_str(), files.log.c_str());
    if (system(cmd) != 0) return files.fail("image generation");
    FILE *fp = fopen(files.image.c_str(), "rb");
    if (!fp) return files.fail("image read");
    desc_img.clear();
    uint8_t buf[4096];
    for (;;) {
      const size_t n = fread(buf, 1, sizeof buf, fp);
      desc_img.insert(desc_img.end(), buf, buf + n);
      if (n < sizeof buf) break;
    }
    fclose(fp);
    if (desc_img.empty()) return files.fail("image read (empty)");
    return true;
  }

  uint64_t desc_beat(uint32_t addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {
      const uint32_t off = addr - DESC_BASE + static_cast<uint32_t>(i);
      v = (v << 8) | static_cast<uint64_t>((off < desc_img.size()) ? desc_img[off] : 0);
    }
    return v;
  }

  void dmem_drive(Vmilan_datapath *dut) {
    const bool beat = dm_busy && dm_wait == 0;
    dut->i_desc_mem_req_ready = dm_busy ? 0 : 1;
    dut->i_desc_mem_rsp_valid = beat ? 1 : 0;
    dut->i_desc_mem_rsp_data = beat ? desc_beat(dm_cur) : 0;
    dut->i_desc_mem_rsp_last = (beat && dm_left == 1) ? 1 : 0;
    dut->i_desc_mem_rsp_err = 0;
  }

  void dmem_edge(Vmilan_datapath *dut) {
    if (!dm_busy) {
      if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
        dm_cur = dut->o_desc_mem_req_addr;
        dm_left = static_cast<int>(dut->o_desc_mem_req_beats);
        dm_busy = dm_left > 0;
        dm_wait = 12;                 // a real, non-zero first-beat latency
        dm_run = 0;
      }
    } else if (dm_wait > 0) {
      dm_wait--;
    } else if (dut->o_desc_mem_rsp_ready) {
      dm_cur += 8;
      if (--dm_left <= 0) dm_busy = false;
      else if (++dm_run == 4) { dm_run = 0; dm_wait = 1; }
    }
  }

  std::vector<std::vector<uint8_t>> tx_frames;
  std::vector<uint64_t> tx_sof_ns;
  std::vector<uint8_t> tx_cur;
  bool tx_open = false;
  uint64_t sim_cyc = 0;
  bool pp_ctr_avb_seen = false;
  bool pp_ctr_ckd_seen = false;

  struct CycleFires {
    bool rx = false;
    bool axi_wr = false;
    bool axi_b = false;
    bool axi_ar = false;
    bool axi_r = false;
    uint32_t axi_rdata = 0;
  };

  CycleFires tick(Vmilan_datapath *dut) {
    dut->axis_clk = 0; dut->gtx_clk = 0;
    dut->clk_audio_i = 0; dut->clk_tdm_i = 0;
    rmem_drive(dut); dmem_drive(dut); dut->eval();
    CycleFires fire;
    fire.rx = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
    fire.axi_wr = dut->s_axi_awvalid && dut->s_axi_awready
               && dut->s_axi_wvalid && dut->s_axi_wready;
    fire.axi_b = dut->s_axi_bvalid && dut->s_axi_bready;
    fire.axi_ar = dut->s_axi_arvalid && dut->s_axi_arready;
    fire.axi_r = dut->s_axi_rvalid && dut->s_axi_rready;
    fire.axi_rdata = dut->s_axi_rdata;
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
      if (!tx_open) {
        tx_sof_ns.push_back(sim_cyc * 8);
        tx_open = true;
      }
      const uint64_t d = dut->m_axis_mac_tx_tdata;
      for (int i = 0; i < 8; i++)
        if ((dut->m_axis_mac_tx_tkeep >> i) & 1)
          tx_cur.push_back((d >> (8 * i)) & 0xFF);
      if (dut->m_axis_mac_tx_tlast) {
        tx_frames.push_back(tx_cur);
        tx_cur.clear();
        tx_open = false;
      }
    }
    if (dut->rootp->milan_datapath__DOT__pp_ctr_evt_valid_w) {
      const unsigned type =
          dut->rootp->milan_datapath__DOT__pp_ctr_evt_type_w;
      const unsigned index =
          dut->rootp->milan_datapath__DOT__pp_ctr_evt_index_w;
      if (type == 0x0009 && index == 0) pp_ctr_avb_seen = true;
      if (type == 0x0024 && index == 0) pp_ctr_ckd_seen = true;
    }
    rmem_edge(dut); dmem_edge(dut);
    dut->axis_clk = 1; dut->gtx_clk = 1;
    dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->eval();
    sim_cyc++;
    return fire;
  }

  void axi_write(Vmilan_datapath *dut, uint16_t addr, uint32_t data) {
    dut->s_axi_awaddr = addr; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = data; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int n = 0; n < 2048; n++) {
      if (tick(dut).axi_wr) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int n = 0; n < 2048; n++) {
      if (tick(dut).axi_b) break;
    }
    dut->s_axi_bready = 0;
  }

  uint32_t axi_read(Vmilan_datapath *dut, uint16_t addr) {
    dut->s_axi_araddr = addr; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int n = 0; n < 2048; n++) {
      if (tick(dut).axi_ar) break;
    }
    dut->s_axi_arvalid = 0;
    uint32_t data = 0;
    for (int n = 0; n < 2048; n++) {
      const CycleFires fire = tick(dut);
      if (fire.axi_r) { data = fire.axi_rdata; break; }
    }
    dut->s_axi_rready = 0;
    return data;
  }

  void run(Vmilan_datapath *dut, uint64_t n) {
    while (n--) tick(dut);
  }

  void send_wide(Vmilan_datapath *dut,
                        const std::vector<uint8_t> &bytes) {
    for (size_t off = 0; off < bytes.size(); off += 8) {
      uint64_t data = 0;
      uint8_t keep = 0;
      for (size_t i = 0; i < 8 && off + i < bytes.size(); i++) {
        data |= static_cast<uint64_t>(bytes[off + i]) << (8 * i);
        keep |= static_cast<uint8_t>(1u << i);
      }
      dut->s_axis_mac_rx_tdata = data;
      dut->s_axis_mac_rx_tkeep = keep;
      dut->s_axis_mac_rx_tvalid = 1;
      dut->s_axis_mac_rx_tlast = off + 8 >= bytes.size();
      while (!tick(dut).rx) {}
    }
    dut->s_axis_mac_rx_tvalid = 0;
    dut->s_axis_mac_rx_tlast = 0;
  }

  void send_sync_pair(Vmilan_datapath *dut, uint16_t seq) {
    const uint32_t phc_lo = axi_read(dut, 0x530);
    const uint64_t origin = (static_cast<uint64_t>(axi_read(dut, 0x534)) << 32) | phc_lo;
    Frame sync = ptp(0x0, seq, 0, 0x0208, 10);
    sync.ts(0);
    send_wide(dut, sync.b);
    run(dut, 1000);
    Frame fu = follow_up(seq, origin);
    send_wide(dut, fu.b);
  }

  bool await_fabric_lock(Vmilan_datapath *dut, unsigned polls = 350) {
    for (unsigned n = 0; n < polls; n++) {
      run_peer(dut, 1000);
      const uint32_t stat = axi_read(dut, 0x77C);
      if (((stat >> 1) & 1) && !(stat & 1)) return true;
    }
    return false;
  }

  size_t pd_scan = 0;
  int pd_answers = 0;
  int64_t pd_target = 600;
  int64_t pd_expect = 0;
  void service_pdelay(Vmilan_datapath *dut) {
    while (pd_scan < tx_frames.size()) {
      const size_t req_ix = pd_scan++;
      const std::vector<uint8_t> req = tx_frames[req_ix];
      if (req.size() < 54 || req[12] != 0x88 || req[13] != 0xF7
          || (req[14] & 0xF) != 0x2)
        continue;
      const uint16_t seq = static_cast<uint16_t>((req[44] << 8) | req[45]);
      const uint64_t t1 = tx_sof_ns[req_ix];
      run(dut, 300);
      const uint64_t now = sim_cyc * 8;
      const uint64_t t2 = 5000000ull + now;
      const int64_t residence = static_cast<int64_t>(now - t1) - 2 * pd_target;
      const uint64_t t3 = t2 + static_cast<uint64_t>(residence);
      const uint64_t t4_est = (sim_cyc + 1) * 8;
      pd_expect = (static_cast<int64_t>(t4_est - t1) - residence) / 2;
      Frame resp = ptp(0x3, seq, 0, 0x0200, 20);
      resp.ts(t2);
      for (int i = 0; i < 10; i++) resp.u8(req[34 + i]);
      send_wide(dut, resp.b);
      run(dut, 16);
      Frame fup = ptp(0xA, seq, 0, 0x0000, 20);
      fup.ts(t3);
      for (int i = 0; i < 10; i++) fup.u8(req[34 + i]);
      send_wide(dut, fup.b);
      run(dut, 32);
      pd_answers++;
    }
  }

  void run_peer(Vmilan_datapath *dut, uint64_t n) {
    for (uint64_t i = 0; i < n; i++) {
      tick(dut);
      if ((i & 255) == 0) service_pdelay(dut);
    }
    service_pdelay(dut);
  }

  void announce(Vmilan_datapath *dut, uint16_t seq,
                       const std::vector<uint64_t> &path,
                       uint64_t gmid = GMID, uint64_t src = PEER_CID,
                       uint8_t priority1 = 100) {
    //! A fixed Announce may carry no PathTrace suffix; that selected shape must
    //! reach the parent as raw count zero. A present TLV remains complete and
    //! identity-aligned, with its count bound to stepsRemoved+1.
    const uint16_t tlv = path.empty() ? 0
                                      : static_cast<uint16_t>(4 + 8 * path.size());
    Frame a = ptp(0xB, seq, 0, 0x0008, static_cast<uint16_t>(30 + tlv), src);
    for (int i = 0; i < 10; i++) a.u8(0);
    a.u16(0xFFC4); a.u8(0);
    a.u8(priority1); a.u32(PEER_CQ); a.u8(248);
    a.u64(gmid);
    a.u16(path.empty() ? 0 : static_cast<uint16_t>(path.size() - 1)); a.u8(0xA0);
    if (!path.empty()) {
      a.u16(0x0008); a.u16(static_cast<uint16_t>(8 * path.size()));
      for (uint64_t hop : path) a.u64(hop);
    }
    send_wide(dut, a.b);
  }

  std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t seq,
                                           const std::vector<uint8_t> &pl) {
    const size_t flen = std::max<size_t>(60, 38 + pl.size());
    std::vector<uint8_t> f(flen, 0);
    const uint8_t src[6] = {
        0x68,0x05,0xCA,0x95,0xB2,0xD1};
    memcpy(f.data() + 6, src, 6);
    f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
    const uint16_t cdl = static_cast<uint16_t>(12 + pl.size());
    f[16] = static_cast<uint8_t>((cdl >> 8) & 7); f[17] = static_cast<uint8_t>(cdl);
    const uint8_t target[8] = {
        0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
    const uint8_t controller[8] = {
        0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
    memcpy(f.data() + 18, target, 8);
    memcpy(f.data() + 26, controller, 8);
    f[34] = static_cast<uint8_t>(seq >> 8); f[35] = static_cast<uint8_t>(seq);
    f[36] = static_cast<uint8_t>((cmd >> 8) & 0x7F); f[37] = static_cast<uint8_t>(cmd);
    std::copy(pl.begin(), pl.end(), f.begin() + 38);
    return f;
  }

  size_t aecp_scan = 0;
  std::vector<uint8_t> await_aecp(Vmilan_datapath *dut, uint16_t seq,
                                         uint16_t cmd, int max_cycles = 200000) {
    for (int cyc = 0; cyc < max_cycles; cyc++) {
      while (aecp_scan < tx_frames.size()) {
        std::vector<uint8_t> f = tx_frames[aecp_scan++];
        if (f.size() > 37 && f[12] == 0x22 && f[13] == 0xF0
            && f[14] == 0xFB && (f[15] & 0xF) == 1
            && ((static_cast<unsigned>(f[34]) << 8) | f[35]) == seq
            && (((static_cast<unsigned>(f[36]) & 0x7F) << 8) | f[37]) == cmd)
          return f;
      }
      tick(dut);
    }
    return {};
  }

  std::vector<uint8_t> aecp_xact(Vmilan_datapath *dut, uint16_t cmd,
                                        uint16_t seq,
                                        const std::vector<uint8_t> &pl) {
    const std::vector<uint8_t> req = aecp_request(cmd, seq, pl);
    send_wide(dut, req);
    run(dut, 40);
    return await_aecp(dut, seq, cmd);
  }

  uint64_t be64(const std::vector<uint8_t> &f, size_t off) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) v = (v << 8) | f[off + i];
    return v;
  }

  uint32_t be32(const std::vector<uint8_t> &f, size_t off) {
    uint32_t v = 0;
    for (int i = 0; i < 4; i++) v = (v << 8) | f[off + i];
    return v;
  }

  std::vector<uint8_t> get_counters(Vmilan_datapath *dut,
                                           uint16_t seq, uint16_t type) {
    return aecp_xact(dut, 0x0029, seq,
                     {static_cast<uint8_t>(type >> 8), static_cast<uint8_t>(type), 0x00, 0x00});
  }

  uint32_t counter_word(const std::vector<uint8_t> &f, unsigned word) {
    if (f.size() < 174 || word > 32) return 0xDEADBEEFu;
    const size_t off = word == 32 ? 42u : 46u + 4u * word;
    return be32(f, off);
  }

  int aecp_status(const std::vector<uint8_t> &f) {
    return f.size() > 16 ? (f[16] >> 3) & 0x1F : -1;
  }

  bool unsolicited_cmd(const std::vector<uint8_t> &f, uint16_t cmd) {
    return f.size() > 37 && f[12] == 0x22 && f[13] == 0xF0
        && f[14] == 0xFB && (f[15] & 0xF) == 1 && (f[36] & 0x80)
        && (((static_cast<unsigned>(f[36]) & 0x7F) << 8) | f[37]) == cmd;
  }

  unsigned unsolicited_count(size_t first, uint16_t cmd) {
    unsigned n = 0;
    for (size_t i = first; i < tx_frames.size(); i++)
      if (unsolicited_cmd(tx_frames[i], cmd)) n++;
    return n;
  }

  //! Return an owned copy. tx_frames keeps growing while the following
  //! solicited comparison is built, so retaining a pointer or reference into
  //! the vector would be invalidated by a reallocation before it is graded.
  std::vector<uint8_t> last_unsolicited(size_t first, uint16_t cmd) {
    std::vector<uint8_t> last;
    for (size_t i = first; i < tx_frames.size(); i++)
      if (unsolicited_cmd(tx_frames[i], cmd)) last = tx_frames[i];
    return last;
  }

  bool unsolicited_desc(const std::vector<uint8_t> &f, uint16_t cmd,
                               uint16_t type) {
    return unsolicited_cmd(f, cmd) && f.size() >= 42
        && ((static_cast<unsigned>(f[38]) << 8) | f[39]) == type
        && f[40] == 0 && f[41] == 0;
  }

  unsigned unsolicited_desc_count(size_t first, uint16_t type) {
    unsigned n = 0;
    for (size_t i = first; i < tx_frames.size(); i++)
      if (unsolicited_desc(tx_frames[i], 0x0029, type)) n++;
    return n;
  }

  std::vector<uint8_t> last_unsolicited_desc(size_t first,
                                                    uint16_t type) {
    std::vector<uint8_t> last;
    for (size_t i = first; i < tx_frames.size(); i++)
      if (unsolicited_desc(tx_frames[i], 0x0029, type)) last = tx_frames[i];
    return last;
  }

  bool same_from(const std::vector<uint8_t> &a,
                        const std::vector<uint8_t> &b, size_t off) {
    return a.size() == b.size() && a.size() > off
        && std::equal(a.begin() + off, a.end(), b.begin() + off);
  }

  bool await_unsolicited_desc_count(Vmilan_datapath *dut, size_t first,
                                           uint16_t type, unsigned want,
                                           uint64_t max_cycles) {
    for (uint64_t elapsed = 0; elapsed < max_cycles; elapsed += 100) {
      if (unsolicited_desc_count(first, type) >= want) return true;
      run_peer(dut, 100);
    }
    return unsolicited_desc_count(first, type) >= want;
  }

  struct MediaTuSeen {
    bool aaf = false;
    bool crf = false;
  };

  //! Observe the real MAC-bound AAF and CRF headers. Looking for an exact bit,
  //! rather than merely sampling the first completion, tolerates a frame that
  //! was already in flight at a verdict edge without weakening the wiring test:
  //! a disconnected/stuck tu input can never satisfy both the certain and
  //! uncertain calls made below.
  MediaTuSeen await_media_tu(Vmilan_datapath *dut, size_t first,
                                    unsigned want_tu, uint64_t max_cycles) {
    MediaTuSeen seen;
    size_t scan = first;
    for (uint64_t n = 0; n < max_cycles && !(seen.aaf && seen.crf); n++) {
      while (scan < tx_frames.size()) {
        const std::vector<uint8_t> &f = tx_frames[scan++];
        if (f.size() > 21 && f[12] == 0x81 && f[13] == 0x00
            && f[16] == 0x22 && f[17] == 0xF0 && f[18] == 0x02
            && (f[21] & 1) == want_tu)
          seen.aaf = true;
        if (f.size() > 15 && f[12] == 0x22 && f[13] == 0xF0
            && f[14] == 0x04 && (f[15] & 1) == want_tu)
          seen.crf = true;
        if (f.size() > 19 && f[12] == 0x81 && f[13] == 0x00
            && f[16] == 0x22 && f[17] == 0xF0 && f[18] == 0x04
            && (f[19] & 1) == want_tu)
          seen.crf = true;
      }
      tick(dut);
      if ((n & 255) == 0) service_pdelay(dut);
    }
    service_pdelay(dut);
    return seen;
  }

  void bring_the_plane_out_of_reset(Vmilan_datapath *dut) {
    dut->axis_resetn = 0;
    dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_mac_rx_tvalid = 0;
    dut->s_axis_mac_rx_tlast = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 2;
    dut->i_link_up = 1;
    dut->i_full_duplex = 1;
    dut->i_mac_events = 0;
    dut->i2s_sdout_i = 0;
    dut->tdm_bclk_i = 0;
    dut->tdm_fsync_i = 0;
    dut->tdm_data_i = 0;
    dut->i_mmcm_locked = 1;
    for (int i = 0; i < 16; i++) tick(dut);
    dut->axis_resetn = 1;
    dut->gtx_resetn = 1;
  }

  // Match the generated product identity. AECP targets the entity id, while
  // the descriptor image supplies the same identity to the processor store.
  void prove_the_retired_publication_writes_are_inert(Vmilan_datapath *dut) {
    axi_write(dut, 0x608, 0x020000FF);
    axi_write(dut, 0x604, 0xFE000001);
    axi_write(dut, 0x504, 8u << 24);       // 8.0 ns; matches sim_cyc model

    // The option is omitted from this elaboration: these are assertions about
    // the RTL default.  Before any peer answers, the engine's committed bank is
    // zero. Retained legacy addresses remain mapped for ABI stability, but every
    // write is inert and cannot manufacture a publication or healthy CLKV claim.
    expect("default-on VERSION", axi_read(dut, 0x004), 0x00020057);
    axi_write(dut, 0x624, 0x55667788); axi_write(dut, 0x628, 0x11223344);
    axi_write(dut, 0x6E4, 1234);
    axi_write(dut, 0x730, 0xDDEEFF00); axi_write(dut, 0x734, 0x99AABBCC);
    axi_write(dut, 0x778, 0x00000085); // maximal retired sync/asCapable fields
    // The nonzero compatibility domain write: the engine speaks only domain 0
    // (802.1AS 8.1), so this 5 must never surface on the CSR readback, the
    // GET_AVB_INFO gather below, or the MAC-bound Pdelay_Req scanned below.
    axi_write(dut, 0x62C, 5);
    expect("fabric GM low overrides SW", axi_read(dut, 0x624), 0);
    expect("fabric GM high overrides SW", axi_read(dut, 0x628), 0);
    expect("fabric pdelay overrides SW", axi_read(dut, 0x6E4), 0);
    expect("fabric parent low overrides SW", axi_read(dut, 0x730), 0);
    expect("fabric parent high overrides SW", axi_read(dut, 0x734), 0);
    expect("fabric domain overrides SW (engine owns domain 0)",
           axi_read(dut, 0x62C), 0);
    uint32_t clkv = axi_read(dut, 0x77C);
    expect("legacy write cannot clear tu", clkv & 1, 1);
    expect("legacy sync claim is inert", (clkv >> 1) & 1, 0);
    expect("compatibility CLKV fields read zero", (clkv >> 2) & 0x3FFF, 0);
    expect("legacy asCapable claim is inert", (clkv >> 16) & 1, 0);
  }

  // A_TXARB_DIAG is a public ABI, not a comment about implementation names.
  // Exercise the real default-only gptp_ctl_mux and prove its three verdicts
  // reach lane 4.  The counter preloads below shorten a 2^16 watchdog wait;
  // adp_tx/sim_super is the behavioral source-abandonment oracle, while this
  // white-box stimulus proves the parent integration's bit mapping.
  void prove_the_gptp_merge_verdicts_reach_lane_four(Vmilan_datapath *dut) {
    dut->m_axis_mac_tx_tready = 0;
    bool gptp_presented = false;
    for (uint64_t n = 0; n < 12000000ull && !gptp_presented; n++) {
      tick(dut);
      gptp_presented = dut->m_axis_mac_tx_tvalid
          && ((dut->m_axis_mac_tx_tdata & 0x0000FFFFFFFFFFFFull)
              == 0x00000E0000C28001ull);
    }
    expect("gPTP SOF presented at MAC", gptp_presented, 1);
    dut->m_axis_mac_tx_tready = 1;
    tick(dut);                         // accept beat 0 and acquire lane-4 lock
    dut->m_axis_mac_tx_tready = 0;
    uint32_t txdiag = axi_read(dut, 0x784);
    expect("TXARB_DIAG presence tag", txdiag >> 24, 0xA7);
    expect("gPTP merge lock is lane 4", (txdiag >> 4) & 1, 1);
    expect("TXARB lanes 7:5 structural zero", txdiag & 0x00E0E0E0u, 0);

    // The byte-to-wide gPTP gearbox may take several clocks to assemble beat 1.
    // Expiring the watchdog in that inter-beat gap is correctly an abandoned-
    // source verdict, not a downstream stall. Wait until the real held source is
    // presenting its next beat while the MAC still refuses it, then shorten only
    // the watchdog interval.
    auto *root = dut->rootp;
    for (int n = 0; n < 64 &&
         !root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__src_tvalid_w;
         n++) tick(dut);
    expect("stalled gPTP source remains valid",
           root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__src_tvalid_w,
           1);
    root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__to_cnt_r
        = 1u << 16;
    tick(dut);                         // held-valid refusal -> stall pulse
    tick(dut);                         // CSR sticky samples the pulse
    txdiag = axi_read(dut, 0x784);
    expect("gPTP merge stall sticky is lane 4", (txdiag >> 20) & 1, 1);
    expect("TXARB reserved lanes stay zero after stall",
           txdiag & 0x00E0E0E0u, 0);

    dut->m_axis_mac_tx_tready = 1;
    run(dut, 128);                     // drain the real Pdelay frame
    while (dut->m_axis_mac_tx_tvalid) tick(dut);
    root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__locked_r = 1;
    root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__sel_r = 1;
    root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__flush_r = 0;
    root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__to_cnt_r
        = 1u << 16;
    dut->eval();
    expect("abort preload selects an absent gPTP source",
           root->milan_datapath__DOT__g_gptp_plane__DOT__gptp_ctl_mux__DOT__src_tvalid_w,
           0);
    tick(dut);                         // selected gPTP source absent -> abort
    tick(dut);                         // injected close accepted + CSR samples
    txdiag = axi_read(dut, 0x784);
    expect("gPTP merge abort sticky is lane 4", (txdiag >> 12) & 1, 1);
    expect("TXARB reserved lanes stay zero after abort",
           txdiag & 0x00E0E0E0u, 0);
  }

  // scan the MAC boundary for the plane's boot Pdelay_Req: an 0x88F7
  // frame whose transportSpecific|msgType byte is 0x12
  void prove_the_boot_pdelay_req_reaches_the_mac(Vmilan_datapath *dut) {
    bool seen_pdreq = false;
    bool seen_ann = false;
    int pdreq_domain = -1;
    size_t boot_scan = tx_frames.size();
    for (uint64_t n = 0; n < 12000000ull; n++) {
      tick(dut);
      while (boot_scan < tx_frames.size()) {
        const std::vector<uint8_t> &frame = tx_frames[boot_scan++];
        if (frame.size() > 14 && frame[12] == 0x88 && frame[13] == 0xF7) {
          if (frame[14] == 0x12) {
            seen_pdreq = true;
            if (frame.size() > 18 && pdreq_domain < 0)
              pdreq_domain = frame[18];   // PTP header domainNumber
          }
          if (frame[14] == 0x1B) seen_ann = true;
        }
      }
    }
    expect("the plane's Pdelay_Req reaches the MAC", seen_pdreq, 1);
    // The compatibility write of 5 to 0x62C above must not reach the wire: the
    // engine-owned domain is the one the MAC-bound frame speaks.
    expect("MAC-bound Pdelay_Req speaks the engine domain", pdreq_domain, 0);
    // no peer ever answers, so asCapable never rises: the announce
    // receipt timeout expires inside the scan window but the becgate
    // must HOLD -- an Announce here would mean an ungated become-master
    expect("no Announce without asCapable", seen_ann, 0);
  }

  // Ignore requests accumulated during the deliberately unanswered phase.
  // Two fresh fabric-timestamped exchanges raise asCapable; the peer then
  // announces a nonzero GM and parent which the engine publishes atomically.
  void answer_pdelay_until_ascapable_and_grade_the_delay(Vmilan_datapath *dut) {
    pd_scan = tx_frames.size();
    for (uint64_t n = 0; n < 10000000ull && pd_answers < 3; n++) {
      tick(dut);
      if ((n & 255) == 0) service_pdelay(dut);
    }
    service_pdelay(dut);
    expect("three fresh Pdelay exchanges answered", pd_answers >= 3, 1);
    run(dut, 10000);
    const uint32_t pdelay = axi_read(dut, 0x6E4);
    expect("fabric publication pdelay is nonzero", pdelay != 0, 1);
    expect("fabric pdelay matches peer timing",
           static_cast<int64_t>(static_cast<int32_t>(pdelay)) >= pd_expect - 32
           && static_cast<int64_t>(static_cast<int32_t>(pdelay)) <= pd_expect + 32, 1);
    expect("fabric asCapable reached the CSR", (axi_read(dut, 0x77C) >> 16) & 1, 1);

    // Drive a legal small negative symmetric-delay result. The donor keeps the
    // signed value for acceptance, but every parent public consumer is unsigned:
    // CSR and the byte-exact GET_AVB_INFO field must see zero, not 0xffff_ffxx.
    const int positive_answers = pd_answers;
    pd_target = -40;
    for (uint64_t n = 0; n < 10000000ull && pd_answers == positive_answers; n++) {
      tick(dut);
      if ((n & 255) == 0) service_pdelay(dut);
    }
    service_pdelay(dut);
    expect("negative Pdelay exchange answered", pd_answers > positive_answers, 1);
    run(dut, 10000);
    expect("negative Pdelay model reached signed noise", pd_expect < 0, 1);
    expect("negative Pdelay clamps in the public CSR", axi_read(dut, 0x6E4), 0);
    expect("negative Pdelay retains asCapable",
           (axi_read(dut, 0x77C) >> 16) & 1, 1);
  }

  void publish_the_peer_announce_into_the_live_bank(Vmilan_datapath *dut) {
    const std::vector<uint64_t> path_a = {GMID, PATH_B1, PATH_B2, PEER_CID};
    announce(dut, 0x7001, path_a);
    uint64_t gm = 0;
    for (int n = 0; n < 32 && gm != GMID; n++) {
      run(dut, 1000);
      gm = (static_cast<uint64_t>(axi_read(dut, 0x628)) << 32) | axi_read(dut, 0x624);
    }
    const uint64_t parent = (static_cast<uint64_t>(axi_read(dut, 0x734)) << 32)
                          | axi_read(dut, 0x730);
    expect("peer-driven GM reached live CSR", gm, GMID);
    expect("peer-driven parent reached live CSR", parent, PEER_CID);
    const uint32_t asp_live_a = axi_read(dut, 0x7E4);
    expect("fabric live AS_PATH count is four", asp_live_a & 0xF, 4);
    expect("fabric live AS_PATH generation advanced",
           ((asp_live_a >> 4) & 0xF) != 0, 1);

    // 0x7DC/0x7E0 remain mapped but are inert in product mode too. There is no
    // parallel writable mirror beside the engine-owned state.
    axi_write(dut, 0x7DC, 0x01234567u);
    axi_write(dut, 0x7E0, 0xDEADBEEFu);
    expect("fabric mode ASP stage LO is inert",
           axi_read(dut, 0x7DC), 0u);
    expect("fabric mode ASP stage HI is inert",
           axi_read(dut, 0x7E0), 0u);
    axi_write(dut, 0x7E4, 0xC0000107u);
    expect("software publish cannot move live fabric 0x7E4",
           axi_read(dut, 0x7E4), asp_live_a);
  }

  // The same nonzero committed bank must traverse the processor's gather
  // face and the real AECP response buffer onto the shared MAC wire.
  void grade_the_committed_bank_on_the_aecp_wire(Vmilan_datapath *dut) {
    aecp_scan = tx_frames.size();
    std::vector<uint8_t> avb = aecp_xact(
        dut, 0x0027, 0x7101, {0x00, 0x09, 0x00, 0x00});
    expect("GET_AVB_INFO response length", avb.size(), 62);
    expect("GET_AVB_INFO SUCCESS", aecp_status(avb), 0);
    expect("GET_AVB_INFO cdl", avb.size() >= 18
           ? (((static_cast<unsigned>(avb[16]) & 7) << 8) | avb[17]) : 0, 36);
    expect("GET_AVB_INFO descriptor", avb.size() >= 42
           ? be32(avb, 38) : 0, 0x00090000u);
    expect("GET_AVB_INFO nonzero GM", avb.size() >= 50
           ? be64(avb, 42) : 0, GMID);
    expect("GET_AVB_INFO byte-exact negative-delay clamp", avb.size() >= 54
           ? be32(avb, 50) : ~0u, 0);
    expect("GET_AVB_INFO domain/flags/map", avb.size() >= 58
           ? be32(avb, 54) : 0, 0x00170001u);
    expect("GET_AVB_INFO exact class mapping", avb.size() >= 62
           ? be32(avb, 58) : 0, 0x06030002u);

    std::vector<uint8_t> path = aecp_xact(
        dut, 0x0028, 0x7102, {0x00, 0x00, 0x00, 0x00});
    expect("GET_AS_PATH full-tail wire length", path.size(), 74);
    expect("GET_AS_PATH SUCCESS", aecp_status(path), 0);
    expect("GET_AS_PATH cdl", path.size() >= 18
           ? (((static_cast<unsigned>(path[16]) & 7) << 8) | path[17]) : 0, 48);
    expect("GET_AS_PATH count four", path.size() >= 42
           ? be32(path, 38) : 0, 4);
    expect("GET_AS_PATH ordered GM", path.size() >= 50
           ? be64(path, 42) : 0, GMID);
    expect("GET_AS_PATH ordered bridge one", path.size() >= 58
           ? be64(path, 50) : 0, PATH_B1);
    expect("GET_AS_PATH ordered bridge two", path.size() >= 66
           ? be64(path, 58) : 0, PATH_B2);
    expect("GET_AS_PATH ordered parent", path.size() >= 74
           ? be64(path, 66) : 0, PEER_CID);
  }

  // Both product talkers consume the same fabric-owner CLKV verdict. Before
  // any valid Sync/Follow_Up pair, keep streaming but stamp uncertainty on
  // the actual MAC-bound AAF and CRF headers.
  void prove_uncertainty_stamps_both_media_wires(Vmilan_datapath *dut) {
    axi_write(dut, 0x654, 0x00020003u);  // AAF enable + admission bypass, VID 2
    axi_write(dut, 0x754, 0x00010001u);
    axi_write(dut, 0x758, 0x02000000u);
    axi_write(dut, 0x75C, 0xF0002A07u);
    axi_write(dut, 0x760, 0x000091E0u);
    axi_write(dut, 0x750, 1u);           // CRF Media Clock Output enable
    const size_t unsync_media_first = tx_frames.size();
    const MediaTuSeen unsync_media =
        await_media_tu(dut, unsync_media_first, 1, 200000);
    expect("unsynchronised fabric verdict is tu", axi_read(dut, 0x77C) & 1, 1);
    expect("fabric tu reaches AAF before Sync", unsync_media.aaf, 1);
    expect("fabric tu reaches CRF before Sync", unsync_media.crf, 1);
  }

  // Register this controller, then refresh the selected parent twice. A
  // tail-only change with stable GM/parent must advance the complete served
  // generation and emit exactly one Table 5.22 GET_AS_PATH push; replaying
  // the identical selected tuple must do neither. The changed push body must
  // equal the solicited response that follows it.
  void prove_a_registered_controller_sees_no_retired_dirt(Vmilan_datapath *dut) {
    std::vector<uint8_t> reg = aecp_xact(
        dut, 0x0024, 0x7103, {0x00, 0x00, 0x00, 0x00});
    expect("REGISTER_UNSOLICITED_NOTIFICATION SUCCESS", aecp_status(reg), 0);
    run(dut, 200000);

    // Repeat the retired-publication attack with a controller registered.
    // Merely preserving public readback is insufficient: an inert address must
    // also leave both counter families and every Table 5.22 dirty input quiet.
    const std::vector<uint8_t> inert_avb_before =
        get_counters(dut, 0x7120, 0x0009);
    const std::vector<uint8_t> inert_ckd_before =
        get_counters(dut, 0x7121, 0x0024);
    const size_t inert_first = tx_frames.size();
    pp_ctr_avb_seen = false;
    pp_ctr_ckd_seen = false;
    axi_write(dut, 0x624, 0xFFFFFFFFu);
    axi_write(dut, 0x628, 0xFFFFFFFFu);
    axi_write(dut, 0x62C, 0xFFFFFFFFu);
    axi_write(dut, 0x6E4, 0xFFFFFFFFu);
    axi_write(dut, 0x730, 0xFFFFFFFFu);
    axi_write(dut, 0x734, 0xFFFFFFFFu);
    axi_write(dut, 0x778, 0xFFFFFFFFu);
    axi_write(dut, 0x7DC, 0xFFFFFFFFu);
    axi_write(dut, 0x7E0, 0xFFFFFFFFu);
    axi_write(dut, 0x7E4, 0xFFFFFFFFu);
    run_peer(dut, 20000);
    expect("retired writes do not dirty AVB counters", pp_ctr_avb_seen, 0);
    expect("retired writes do not dirty CLOCK counters", pp_ctr_ckd_seen, 0);
    expect("retired writes emit no GET_AVB_INFO push",
           unsolicited_count(inert_first, 0x0027), 0);
    expect("retired writes emit no GET_AS_PATH push",
           unsolicited_count(inert_first, 0x0028), 0);
    expect("retired writes emit no GET_COUNTERS push",
           unsolicited_count(inert_first, 0x0029), 0);
    const std::vector<uint8_t> inert_avb_after =
        get_counters(dut, 0x7122, 0x0009);
    const std::vector<uint8_t> inert_ckd_after =
        get_counters(dut, 0x7123, 0x0024);
    expect("retired writes leave AVB counters unchanged",
           same_from(inert_avb_before, inert_avb_after, 38), 1);
    expect("retired writes leave CLOCK counters unchanged",
           same_from(inert_ckd_before, inert_ckd_after, 38), 1);
  }

  // Exercise the per-descriptor one-second limiter through the real product
  // event path. LINK_DOWN emits immediately. LINK_UP follows within one
  // compressed processor second, must remain dirty without a second push,
  // then must be released exactly once when that descriptor's limiter opens.
  void prove_the_per_descriptor_one_second_limiter(Vmilan_datapath *dut) {
    const std::vector<uint8_t> rate_avb_before =
        get_counters(dut, 0x7124, 0x0009);
    const size_t rate_first = tx_frames.size();
    pp_ctr_avb_seen = false;
    axi_write(dut, 0x71C, 0u);
    for (unsigned n = 0; n < 200 && !pp_ctr_avb_seen; n++) run_peer(dut, 100);
    const uint64_t down_evt_cyc = sim_cyc;
    expect("LINK_DOWN reaches AVB counter descriptor arbiter",
           pp_ctr_avb_seen, 1);
    const bool down_emitted =
        await_unsolicited_desc_count(dut, rate_first, 0x0009, 1, 50000);
    expect("LINK_DOWN emits first AVB GET_COUNTERS push", down_emitted, 1);
    expect("first AVB limiter window contains one push",
           unsolicited_desc_count(rate_first, 0x0009), 1);
    const std::vector<uint8_t> down_push =
        last_unsolicited_desc(rate_first, 0x0009);
    const std::vector<uint8_t> rate_avb_down =
        get_counters(dut, 0x7125, 0x0009);
    expect("LINK_DOWN increments AVB counter",
           counter_word(rate_avb_down, 1) - counter_word(rate_avb_before, 1), 1);
    expect("LINK_DOWN leaves LINK_UP stable",
           counter_word(rate_avb_down, 0) - counter_word(rate_avb_before, 0), 0);
    expect("LINK_DOWN push body equals solicited counters",
           same_from(down_push, rate_avb_down, 38), 1);

    pp_ctr_avb_seen = false;
    axi_write(dut, 0x71C, 1u);
    for (unsigned n = 0; n < 200 && !pp_ctr_avb_seen; n++) run_peer(dut, 100);
    const uint64_t up_evt_cyc = sim_cyc;
    expect("LINK_UP reaches AVB counter descriptor arbiter", pp_ctr_avb_seen, 1);
    expect("LINK_UP event is inside first one-second limiter window",
           (up_evt_cyc - down_evt_cyc) < 1000ull * kPpMsCyc, 1);
    run_peer(dut, 200ull * kPpMsCyc);
    expect("within-window LINK_UP push is suppressed",
           unsolicited_desc_count(rate_first, 0x0009), 1);
    const bool up_released =
        await_unsolicited_desc_count(dut, rate_first, 0x0009, 2,
                                     1200ull * kPpMsCyc);
    expect("pending LINK_UP releases when AVB limiter opens", up_released, 1);
    expect("pending LINK_UP releases exactly one second push",
           unsolicited_desc_count(rate_first, 0x0009), 2);
    const std::vector<uint8_t> up_push =
        last_unsolicited_desc(rate_first, 0x0009);
    const std::vector<uint8_t> rate_avb_after =
        get_counters(dut, 0x7126, 0x0009);
    expect("released LINK_UP increments AVB counter",
           counter_word(rate_avb_after, 0) - counter_word(rate_avb_before, 0), 1);
    expect("released state retains one LINK_DOWN",
           counter_word(rate_avb_after, 1) - counter_word(rate_avb_before, 1), 1);
    expect("released LINK_UP push body equals solicited counters",
           same_from(up_push, rate_avb_after, 38), 1);
  }

  // One selected-peer Sync/Follow_Up raises the fabric sync publication.
  // The resulting tu 1->0 edge must increment CLOCK_DOMAIN.LOCKED, traverse
  // ctr_ckd_dirty_w and the descriptor arbiter, and arrive as a GET_COUNTERS
  // notification. The same verdict must clear tu on both media wire formats.
  void prove_the_sync_lock_reaches_the_clock_domain_counters(Vmilan_datapath *dut) {
    std::vector<uint8_t> ckd_before = get_counters(dut, 0x7110, 0x0024);
    expect("pre-Sync CLOCK_DOMAIN counters SUCCESS", aecp_status(ckd_before), 0);
    expect("CLOCK_DOMAIN counters_valid", counter_word(ckd_before, 32), 3);
    const uint32_t lock_before = counter_word(ckd_before, 0);
    const uint32_t unlock_before = counter_word(ckd_before, 1);
    pp_ctr_ckd_seen = false;
    const size_t sync_first = tx_frames.size();
    send_sync_pair(dut, 0x7200);
    const bool fabric_locked = await_fabric_lock(dut);
    expect("fabric Sync reaches CLKV sync-ok", (axi_read(dut, 0x77C) >> 1) & 1,
           1);
    expect("fabric Sync clears CLKV tu after hold", fabric_locked, 1);
    const size_t locked_media_first = tx_frames.size();
    const MediaTuSeen locked_media =
        await_media_tu(dut, locked_media_first, 0, 100000);
    expect("fabric certainty reaches AAF tu", locked_media.aaf, 1);
    expect("fabric certainty reaches CRF tu", locked_media.crf, 1);
    run_peer(dut, 100000);
    expect("CLKV lock edge reaches counter descriptor arbiter",
           pp_ctr_ckd_seen, 1);
    expect("CLKV lock emits one CLOCK_DOMAIN GET_COUNTERS push",
           unsolicited_desc_count(sync_first, 0x0024), 1);
    const std::vector<uint8_t> lock_push =
        last_unsolicited_desc(sync_first, 0x0024);
    std::vector<uint8_t> ckd_locked = get_counters(dut, 0x7111, 0x0024);
    expect("fabric lock increments CLOCK_DOMAIN.LOCKED",
           counter_word(ckd_locked, 0) - lock_before, 1);
    expect("fabric lock leaves CLOCK_DOMAIN.UNLOCKED stable",
           counter_word(ckd_locked, 1) - unlock_before, 0);
    expect("CLOCK_DOMAIN push body equals solicited counters",
           same_from(lock_push, ckd_locked, 38), 1);
  }

  // Let the locally compressed per-descriptor notification limiter reopen
  // before the later GM switch, without exceeding syncReceiptTimeout. Pdelay
  // service keeps the selected peer capable throughout.
  unsigned prove_the_path_trace_refresh_generations(Vmilan_datapath *dut) {
    run_peer(dut, 150000);
    const size_t changed_first = tx_frames.size();
    const unsigned gen_a = (axi_read(dut, 0x7E4) >> 4) & 0xF;
    const std::vector<uint64_t> path_b =
        {GMID, PATH_B1, PATH_B2_NEW, PEER_CID};
    announce(dut, 0x7002, path_b);
    unsigned gen_b = gen_a;
    for (int n = 0; n < 64 && gen_b == gen_a; n++) {
      run(dut, 1000);
      gen_b = (axi_read(dut, 0x7E4) >> 4) & 0xF;
    }
    expect("tail-only parent refresh advances generation", gen_b,
           (gen_a + 1) & 0xF);
    expect("tail-only refresh leaves GM stable",
           (static_cast<uint64_t>(axi_read(dut, 0x628)) << 32) | axi_read(dut, 0x624), GMID);
    expect("tail-only refresh leaves parent stable",
           (static_cast<uint64_t>(axi_read(dut, 0x734)) << 32) | axi_read(dut, 0x730),
           PEER_CID);
    run(dut, 200000);
    expect("tail-only refresh emits one GET_AS_PATH push",
           unsolicited_count(changed_first, 0x0028), 1);
    const std::vector<uint8_t> changed_push =
        last_unsolicited(changed_first, 0x0028);
    std::vector<uint8_t> path_new = aecp_xact(
        dut, 0x0028, 0x7104, {0x00, 0x00, 0x00, 0x00});
    expect("tail-only refresh reaches solicited path",
           path_new.size() >= 74 ? be64(path_new, 58) : 0, PATH_B2_NEW);
    expect("changed push body equals current solicited path",
           same_from(changed_push, path_new, 38), 1);

    const size_t identical_first = tx_frames.size();
    announce(dut, 0x7003, path_b);
    run(dut, 200000);
    expect("identical parent refresh keeps generation",
           (axi_read(dut, 0x7E4) >> 4) & 0xF, gen_b);
    expect("identical parent refresh emits no false AS_PATH push",
           unsolicited_count(identical_first, 0x0028), 0);

    // A selected fixed Announce without PathTrace is not #227's software
    // count-zero alias. Product fabric mode serves the actual empty sequence,
    // advances once on present<->absent, and sends exactly that zero-count body.
    const size_t absent_first = tx_frames.size();
    announce(dut, 0x7004, {});
    uint32_t asp_empty = axi_read(dut, 0x7E4);
    for (int n = 0; n < 64 && (asp_empty & 0xF) != 0; n++) {
      run(dut, 1000);
      asp_empty = axi_read(dut, 0x7E4);
    }
    expect("TLV-less fabric publication preserves raw count zero",
           asp_empty & 0xF, 0);
    expect("present to absent advances fabric path generation once",
           (asp_empty >> 4) & 0xF, (gen_b + 1) & 0xF);
    expect("TLV-less selection retains scalar GM",
           (static_cast<uint64_t>(axi_read(dut, 0x628)) << 32) | axi_read(dut, 0x624), GMID);
    run(dut, 200000);
    expect("present to absent emits one GET_AS_PATH push",
           unsolicited_count(absent_first, 0x0028), 1);
    const std::vector<uint8_t> absent_push =
        last_unsolicited(absent_first, 0x0028);
    std::vector<uint8_t> path_empty = aecp_xact(
        dut, 0x0028, 0x7105, {0x00, 0x00, 0x00, 0x00});
    expect("TLV-less GET_AS_PATH minimum-Ethernet wire length",
           path_empty.size(), 60);
    expect("TLV-less GET_AS_PATH SUCCESS", aecp_status(path_empty), 0);
    expect("TLV-less GET_AS_PATH cdl", path_empty.size() >= 18
           ? (((static_cast<unsigned>(path_empty[16]) & 7) << 8) | path_empty[17]) : 0, 16);
    expect("TLV-less GET_AS_PATH serves count zero", path_empty.size() >= 42
           ? be32(path_empty, 38) : ~0u, 0);
    expect("absent push body equals solicited empty response",
           same_from(absent_push, path_empty, 38), 1);

    const size_t absent_same_first = tx_frames.size();
    const unsigned gen_empty = (asp_empty >> 4) & 0xF;
    announce(dut, 0x7005, {});
    run(dut, 200000);
    expect("identical absent refresh keeps fabric path generation",
           (axi_read(dut, 0x7E4) >> 4) & 0xF, gen_empty);
    expect("identical absent refresh emits no AS_PATH push",
           unsolicited_count(absent_same_first, 0x0028), 0);
    return gen_empty;
  }

  // The PathTrace cases above intentionally take longer than one Sync receipt
  // window. Re-establish the selected peer immediately before the GM-switch
  // proof, then reopen the compressed counter-notification limiter while the
  // domain is still locked.
  void prove_the_gm_switch_drives_both_counter_families(Vmilan_datapath *dut,
                                                         unsigned gen_empty) {
    send_sync_pair(dut, 0x7201);
    expect("pre-switch fabric domain is locked", await_fabric_lock(dut), 1);
    run_peer(dut, 150000);

    // The scalar GM remains live independently of PathTrace. Switching between
    // two selected TLV-less masters drives AVB_INFO and GPTP_GM_CHANGED, but the
    // served AS_PATH is empty on both sides and therefore stays silent. It also
    // drives the product counter families: AVB_INTERFACE records the GM change,
    // while the discontinuity makes the previously locked CLOCK_DOMAIN unlock.
    const std::vector<uint8_t> avb_ctr_before =
        get_counters(dut, 0x7112, 0x0009);
    const std::vector<uint8_t> ckd_ctr_before =
        get_counters(dut, 0x7113, 0x0024);
    expect("AVB_INTERFACE counters_valid", counter_word(avb_ctr_before, 32),
           0x23);
    pp_ctr_avb_seen = false;
    pp_ctr_ckd_seen = false;
    const size_t empty_gm_first = tx_frames.size();
    const unsigned long gmchg_before =
        dut->rootp->milan_datapath__DOT__ctr_gmchg_r;
    announce(dut, 0x7006, {}, GMID_EMPTY, GMID_EMPTY, 90);
    uint64_t empty_gm = 0;
    for (int n = 0; n < 64 && empty_gm != GMID_EMPTY; n++) {
      run(dut, 1000);
      empty_gm = (static_cast<uint64_t>(axi_read(dut, 0x628)) << 32)
               | axi_read(dut, 0x624);
    }
    expect("TLV-less better Announce changes scalar GM", empty_gm, GMID_EMPTY);
    expect("absent GM switch retains raw-empty count", axi_read(dut, 0x7E4) & 0xF,
           0);
    expect("absent GM switch spends no path generation",
           (axi_read(dut, 0x7E4) >> 4) & 0xF, gen_empty);
    expect("fabric GM switch asserts CLKV tu hold", axi_read(dut, 0x77C) & 1, 1);
    const MediaTuSeen switch_media =
        await_media_tu(dut, empty_gm_first, 1, 90000);
    expect("GM-switch tu reaches AAF wire", switch_media.aaf, 1);
    expect("GM-switch tu reaches CRF wire", switch_media.crf, 1);
    run_peer(dut, 5000);
    expect("GM switch reaches AVB counter descriptor arbiter",
           pp_ctr_avb_seen, 1);
    expect("GM-switch tu reaches CLOCK_DOMAIN descriptor arbiter",
           pp_ctr_ckd_seen, 1);
    expect("GM switch emits one AVB_INTERFACE GET_COUNTERS push",
           unsolicited_desc_count(empty_gm_first, 0x0009), 1);
    expect("GM-switch tu emits one CLOCK_DOMAIN GET_COUNTERS push",
           unsolicited_desc_count(empty_gm_first, 0x0024), 1);
    const std::vector<uint8_t> avb_ctr_push =
        last_unsolicited_desc(empty_gm_first, 0x0009);
    const std::vector<uint8_t> ckd_ctr_push =
        last_unsolicited_desc(empty_gm_first, 0x0024);
    const std::vector<uint8_t> avb_ctr_after =
        get_counters(dut, 0x7114, 0x0009);
    const std::vector<uint8_t> ckd_ctr_after =
        get_counters(dut, 0x7115, 0x0024);
    expect("GET_COUNTERS records fabric GPTP_GM_CHANGED",
           counter_word(avb_ctr_after, 5) - counter_word(avb_ctr_before, 5), 1);
    expect("GET_COUNTERS records GM-switch CLOCK_DOMAIN.UNLOCKED",
           counter_word(ckd_ctr_after, 1) - counter_word(ckd_ctr_before, 1), 1);
    expect("GM-switch hold has not relocked CLOCK_DOMAIN early",
           counter_word(ckd_ctr_after, 0) - counter_word(ckd_ctr_before, 0), 0);
    expect("AVB counter push body equals solicited counters",
           same_from(avb_ctr_push, avb_ctr_after, 38), 1);
    expect("CLOCK_DOMAIN push body equals solicited counters",
           same_from(ckd_ctr_push, ckd_ctr_after, 38), 1);
    run(dut, 200000);
    expect("absent GM switch emits no false GET_AS_PATH push",
           unsolicited_count(empty_gm_first, 0x0028), 0);
    expect("absent GM switch still emits one GET_AVB_INFO push",
           unsolicited_count(empty_gm_first, 0x0027), 1);
    expect("absent GM switch still increments GPTP_GM_CHANGED",
           dut->rootp->milan_datapath__DOT__ctr_gmchg_r - gmchg_before, 1);
  }

  // Explicit `[GM]` is distinct from absent. Snapshot a one-entry response,
  // withdraw it after the first-count capture, and require the in-flight wire
  // answer to remain wholly old while live state and the following read are
  // wholly new. These checks kill fabric min-one and torn-response mutations.
  uint32_t prove_explicit_and_withdrawn_path_trace_coherence(
        Vmilan_datapath *dut, unsigned gen_empty) {
    const std::vector<uint64_t> one_path = {GMID_EMPTY};
    const size_t one_first = tx_frames.size();
    announce(dut, 0x7007, one_path, GMID_EMPTY, GMID_EMPTY, 90);
    uint32_t asp_one = axi_read(dut, 0x7E4);
    for (int n = 0; n < 64 && (asp_one & 0xF) != 1; n++) {
      run(dut, 1000);
      asp_one = axi_read(dut, 0x7E4);
    }
    expect("explicit one-entry fabric PathTrace serves count one",
           asp_one & 0xF, 1);
    expect("absent to explicit GM advances generation once",
           (asp_one >> 4) & 0xF, (gen_empty + 1) & 0xF);
    run(dut, 200000);
    expect("absent to explicit GM emits one AS_PATH push",
           unsolicited_count(one_first, 0x0028), 1);
    std::vector<uint8_t> path_one = aecp_xact(
        dut, 0x0028, 0x7106, {0x00, 0x00, 0x00, 0x00});
    expect("explicit one-entry GET_AS_PATH minimum-Ethernet wire length",
           path_one.size(), 60);
    expect("explicit one-entry GET_AS_PATH cdl", path_one.size() >= 18
           ? (((static_cast<unsigned>(path_one[16]) & 7) << 8) | path_one[17]) : 0, 24);
    expect("explicit one-entry GET_AS_PATH count", path_one.size() >= 42
           ? be32(path_one, 38) : 0, 1);
    expect("explicit one-entry GET_AS_PATH head", path_one.size() >= 50
           ? be64(path_one, 42) : 0, GMID_EMPTY);

    const uint16_t cut_seq = 0x7107;
    const std::vector<uint8_t> cut_req = aecp_request(
        0x0028, cut_seq, {0x00, 0x00, 0x00, 0x00});
    send_wide(dut, cut_req);
    bool cut_capture = false;
    for (int n = 0; n < 200000 && !cut_capture; n++) {
      tick(dut);
      cut_capture = dut->rootp->milan_datapath__DOT__asp_resp_capture_w;
    }
    expect("in-flight fabric response reached first-count snapshot",
           cut_capture, 1);
    const size_t withdraw_first = tx_frames.size();
    const unsigned gen_one = (asp_one >> 4) & 0xF;
    //! Hold the already-captured response behind the real MAC boundary while
    //! the independent gPTP plane commits the withdrawal. Releasing it afterward
    //! makes old-response/new-live coherence observable rather than a timing
    //! inference from a response that happened to leave first.
    dut->m_axis_mac_tx_tready = 0;
    announce(dut, 0x7008, {}, GMID_EMPTY, GMID_EMPTY, 90);
    bool withdrew_before_old_wire = false;
    for (int n = 0; n < 200000 && !withdrew_before_old_wire; n++) {
      tick(dut);
      withdrew_before_old_wire =
          dut->rootp->milan_datapath__DOT__gptp_pub_path_count_w == 0;
    }
    expect("withdrawal commits before captured old response leaves wire",
           withdrew_before_old_wire, 1);
    dut->m_axis_mac_tx_tready = 1;
    std::vector<uint8_t> cut_old = await_aecp(dut, cut_seq, 0x0028);
    expect("in-flight response remains wholly old count one",
           cut_old.size() >= 50 ? be32(cut_old, 38) : 0, 1);
    expect("in-flight response remains wholly old GM",
           cut_old.size() >= 50 ? be64(cut_old, 42) : 0, GMID_EMPTY);
    uint32_t asp_withdrawn = axi_read(dut, 0x7E4);
    for (int n = 0; n < 64 && (asp_withdrawn & 0xF) != 0; n++) {
      run(dut, 1000);
      asp_withdrawn = axi_read(dut, 0x7E4);
    }
    expect("explicit GM withdrawal restores raw-empty count",
           asp_withdrawn & 0xF, 0);
    expect("explicit GM withdrawal advances generation once",
           (asp_withdrawn >> 4) & 0xF, (gen_one + 1) & 0xF);
    run(dut, 200000);
    expect("explicit GM withdrawal emits one AS_PATH push",
           unsolicited_count(withdraw_first, 0x0028), 1);
    const std::vector<uint8_t> withdraw_push =
        last_unsolicited(withdraw_first, 0x0028);
    std::vector<uint8_t> cut_new = aecp_xact(
        dut, 0x0028, 0x7108, {0x00, 0x00, 0x00, 0x00});
    expect("post-cut response is wholly new count zero",
           cut_new.size() >= 42 ? be32(cut_new, 38) : ~0u, 0);
    expect("withdrawal push body equals post-cut solicited response",
           same_from(withdraw_push, cut_new, 38), 1);
    return asp_withdrawn;
  }

  // Drive the complete fixed parent ABI through the response gather and wire
  // formatter. Shortening any wrapper, CSR, snapshot or ordinal loop to the
  // smaller smoke-test path must lose the final identity and fail here.
  void prove_the_maximum_bounded_path_trace(Vmilan_datapath *dut,
                                             uint32_t asp_withdrawn) {
    const size_t max_first = tx_frames.size();
    const unsigned gen_withdrawn = (asp_withdrawn >> 4) & 0xF;
    const std::vector<uint64_t> path_max = {
        GMID_EMPTY, PATH_B1, PATH_B2, PATH_B3,
        PATH_B4, PATH_B5, PATH_B6, PEER_CID};
    announce(dut, 0x7009, path_max, GMID_EMPTY, PEER_CID, 80);
    uint32_t asp_max = axi_read(dut, 0x7E4);
    for (int n = 0; n < 64 && (asp_max & 0xF) != 8; n++) {
      run(dut, 1000);
      asp_max = axi_read(dut, 0x7E4);
    }
    expect("maximum bounded fabric PathTrace serves count eight", asp_max & 0xF,
           8);
    expect("empty to maximum path advances generation once",
           (asp_max >> 4) & 0xF, (gen_withdrawn + 1) & 0xF);
    run(dut, 200000);
    expect("maximum path emits one GET_AS_PATH push",
           unsolicited_count(max_first, 0x0028), 1);
    expect("maximum path emits no false GET_AVB_INFO push",
           unsolicited_count(max_first, 0x0027), 0);
    const std::vector<uint8_t> max_push =
        last_unsolicited(max_first, 0x0028);
    std::vector<uint8_t> path_max_wire = aecp_xact(
        dut, 0x0028, 0x7109, {0x00, 0x00, 0x00, 0x00});
    expect("maximum GET_AS_PATH wire length", path_max_wire.size(), 106);
    expect("maximum GET_AS_PATH cdl", path_max_wire.size() >= 18
           ? (((static_cast<unsigned>(path_max_wire[16]) & 7) << 8) | path_max_wire[17]) : 0,
           80);
    expect("maximum GET_AS_PATH count", path_max_wire.size() >= 42
           ? be32(path_max_wire, 38) : 0, 8);
    expect("maximum GET_AS_PATH final identity", path_max_wire.size() >= 106
           ? be64(path_max_wire, 98) : 0, PEER_CID);
    expect("maximum push body equals solicited path",
           same_from(max_push, path_max_wire, 38), 1);
  }

  // ---- issue #207: the three drop counters through the real CSR route ----
  // Each counter moves through its own refusing stage, injected at the MAC
  // RX seam and read at 0x7E8/0x7EC over the same AXI path software uses.
  void prove_the_three_drop_counters_through_the_csr(Vmilan_datapath *dut) {
    auto *root = dut->rootp;
    {
      // a) the parser refuses a foreign-domain Sync: only [15:0] of 0x7E8
      //    moves (gPTP is domain 0; the donor parser drops the header).
      uint32_t w0 = axi_read(dut, 0x7E8);
      uint32_t e0 = axi_read(dut, 0x7EC);
      Frame fd = ptp(0x0, 0x5107, 0, 0x0208, 10);
      fd.ts(0);
      fd.b[18] = 5;                       // domainNumber, frame byte 14+4
      send_wide(dut, fd.b);
      run(dut, 3000);
      uint32_t w1 = axi_read(dut, 0x7E8);
      uint32_t e1 = axi_read(dut, 0x7EC);
      expect("foreign domain moves the parser count",
             static_cast<uint16_t>((w1 & 0xFFFF) - (w0 & 0xFFFF)) >= 1, 1);
      expect("foreign domain leaves the tap count", w1 >> 16, w0 >> 16);
      expect("foreign domain leaves the event count", e1, e0);

      // b) a full queue refuses the next accepted frame's event: only 0x7EC
      //    moves. The four-deep level is held full around exactly one valid
      //    Sync - the same poke-the-corner idiom as the merge-stall arms -
      //    while a first Sync keeps the uCPU inside its handler so nothing
      //    pops a forced entry. The level is restored to the true wp-rp
      //    afterwards; the refused frame's bank stays held, which nothing
      //    after this arm asserts on.
      auto *eng = &root->milan_datapath__DOT__g_gptp_plane__DOT__u_gptp_shadow__DOT__u_engine__DOT__evq_lvl_r;
      Frame s1 = ptp(0x0, 0x5108, 0, 0x0208, 10);
      s1.ts(0);
      send_wide(dut, s1.b);
      run(dut, 40);                       // the handler is now holding the uCPU
      *eng = 4; dut->eval();              // queue reads full; pushes refused
      Frame s2 = ptp(0x0, 0x5109, 0, 0x0208, 10);
      s2.ts(0);
      send_wide(dut, s2.b);
      run(dut, 400);                      // s2's event arrives against full
      uint32_t w2 = axi_read(dut, 0x7E8);
      uint32_t e2 = axi_read(dut, 0x7EC);
      expect("a full queue moves only the event count",
             static_cast<uint16_t>(e2 - e1) >= 1, 1);
      expect("the full-queue refusal leaves the parser count",
             w2 & 0xFFFF, w1 & 0xFFFF);
      expect("the full-queue refusal leaves the tap count", w2 >> 16, w1 >> 16);
      // The restore is exact only if no pop fired inside the window; a pop
      // needs the uCPU idle, which s1's still-running handler forbids, and
      // an early pop would fail the full-queue expect above loudly. The one
      // green-but-poisoned residue (a pop after the refusal, before this
      // line) is benign only because this is the file's last arm - keep it
      // last, or gate the restore on dbg_busy_o.
      *eng = static_cast<uint8_t>((root->milan_datapath__DOT__g_gptp_plane__DOT__u_gptp_shadow__DOT__u_engine__DOT__evq_wp_r
              - root->milan_datapath__DOT__g_gptp_plane__DOT__u_gptp_shadow__DOT__u_engine__DOT__evq_rp_r) & 3);
      dut->eval();
      run(dut, 4000);                     // drain the real backlog

      // c) a back-to-back burst overruns the 2 KB tap FIFO: the shed frames
      //    are counted at 0x7E8[31:16] and, having never reached the parser,
      //    cannot move [15:0]. Forty 130-octet Syncs are ~5.6 KB against a
      //    2 KB FIFO drained byte-serially. Delivered frames may pile
      //    events; the event counter is deliberately unasserted here.
      for (int k = 0; k < 40; k++) {
        Frame sy = ptp(0x0, static_cast<uint16_t>(0x6000 + k), 0, 0x0208, 96);
        sy.ts(0);
        for (int i = 0; i < 86; i++) sy.u8(static_cast<uint8_t>(i));
        send_wide(dut, sy.b);
      }
      run(dut, 6000);
      uint32_t w3 = axi_read(dut, 0x7E8);
      expect("a burst moves the tap count", static_cast<uint16_t>((w3 >> 16) - (w2 >> 16)) >= 1, 1);
      expect("shed frames never reach the parser count",
             w3 & 0xFFFF, w2 & 0xFFFF);
    }
  }

  int report() const {
    printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }
};

int GptpPlaneHarness::run() {
  expect("shipping AEM image generated", load_shipping_aemi(), 1);
  const milan::tb::Model<Vmilan_datapath> model;
  Vmilan_datapath *const dut = model.get();

  bring_the_plane_out_of_reset(dut);
  prove_the_retired_publication_writes_are_inert(dut);
  prove_the_gptp_merge_verdicts_reach_lane_four(dut);
  prove_the_boot_pdelay_req_reaches_the_mac(dut);
  answer_pdelay_until_ascapable_and_grade_the_delay(dut);
  publish_the_peer_announce_into_the_live_bank(dut);
  grade_the_committed_bank_on_the_aecp_wire(dut);
  prove_uncertainty_stamps_both_media_wires(dut);
  prove_a_registered_controller_sees_no_retired_dirt(dut);
  prove_the_per_descriptor_one_second_limiter(dut);
  prove_the_sync_lock_reaches_the_clock_domain_counters(dut);
  const unsigned gen_empty = prove_the_path_trace_refresh_generations(dut);
  prove_the_gm_switch_drives_both_counter_families(dut, gen_empty);
  const uint32_t asp_withdrawn =
      prove_explicit_and_withdrawn_path_trace_coherence(dut, gen_empty);
  prove_the_maximum_bounded_path_trace(dut, asp_withdrawn);
  prove_the_three_drop_counters_through_the_csr(dut);

  return report();
}

}  // namespace

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  GptpPlaneHarness harness;
  return harness.run();
}
