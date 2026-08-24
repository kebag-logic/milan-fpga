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
// real MAC boundary. The donor's own suites remain the deep state-machine
// oracle; THIS leg pins every integration seam in the real datapath.
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
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"

static const uint64_t PEER_CID = 0x0080E1FFFE112233ull;
static const uint64_t GMID = 0x00AACCFFFE010203ull;
static const uint32_t PEER_CQ = 0xF8FE436A;

static int checks = 0, fails = 0;
static void expect(const char *what, uint64_t got, uint64_t exp) {
  checks++;
  if (got != exp) {
    fails++;
    printf("FAIL %-30s got %016llx exp %016llx\n", what,
           (unsigned long long)got, (unsigned long long)exp);
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

static Frame ptp(uint8_t mtype, uint16_t seq, uint64_t corr,
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

// The protocol processor assembles every AECP response through this memory
// face. Model one ordered, always-answering store; the gPTP commands do not
// touch descriptor memory.
static const uint32_t RESP_BASE = 0x20100000u;
static const uint32_t RESP_BYTES = 592u;
static uint8_t rmem[RESP_BYTES];
static bool rm_busy = false, rm_wpend = false;
static uint32_t rm_cur = 0, rm_waddr = 0, rm_wstrb = 0;
static uint64_t rm_wdata = 0;
static int rm_left = 0;

static uint64_t rmem_beat(uint32_t addr) {
  uint64_t v = 0;
  for (int i = 0; i < 8; i++) {
    const uint32_t off = addr - RESP_BASE + (uint32_t)i;
    v = (v << 8) | (uint64_t)((off < RESP_BYTES) ? rmem[off] : 0);
  }
  return v;
}

static void rmem_drive(Vmilan_datapath *dut) {
  dut->i_resp_mem_req_ready = rm_busy ? 0 : 1;
  dut->i_resp_mem_rsp_valid = rm_busy ? 1 : 0;
  dut->i_resp_mem_rsp_data = rm_busy ? rmem_beat(rm_cur) : 0;
  dut->i_resp_mem_rsp_last = (rm_busy && rm_left == 1) ? 1 : 0;
  dut->i_resp_mem_rsp_err = 0;
  dut->i_resp_mem_wr_ready = rm_wpend ? 0 : 1;
  dut->i_resp_mem_wr_done = rm_wpend ? 1 : 0;
  dut->i_resp_mem_wr_err = 0;
}

static void rmem_edge(Vmilan_datapath *dut) {
  if (!rm_busy) {
    if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
      rm_cur = dut->o_resp_mem_req_addr;
      rm_left = (int)dut->o_resp_mem_req_beats;
      rm_busy = rm_left > 0;
    }
  } else if (dut->o_resp_mem_rsp_ready) {
    rm_cur += 8;
    if (--rm_left <= 0) rm_busy = false;
  }
  if (rm_wpend) {
    for (int i = 0; i < 8; i++) {
      if (rm_wstrb & (1u << i)) {
        const uint32_t off = rm_waddr - RESP_BASE + (uint32_t)i;
        if (off < RESP_BYTES)
          rmem[off] = (uint8_t)(rm_wdata >> (56 - 8 * i));
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

static const uint32_t DESC_BASE = 0x20000000u;
static std::vector<uint8_t> desc_img;
static bool dm_busy = false;
static uint32_t dm_cur = 0;
static int dm_left = 0, dm_wait = 0, dm_run = 0;

struct AemiTemps {
  std::string outdir, image, log;
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

static bool load_shipping_aemi() {
  const int pid = (int)getpid();
  const std::string tmp = std::filesystem::temp_directory_path().string();
  AemiTemps files{
      tmp + "/milan_gptp_bld_" + std::to_string(pid),
      tmp + "/milan_gptp_aemi_" + std::to_string(pid) + ".bin",
      tmp + "/milan_gptp_aemi_" + std::to_string(pid) + ".log"};
  char overlay[512], cmd[1536];
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

static uint64_t desc_beat(uint32_t addr) {
  uint64_t v = 0;
  for (int i = 0; i < 8; i++) {
    const uint32_t off = addr - DESC_BASE + (uint32_t)i;
    v = (v << 8) | (uint64_t)((off < desc_img.size()) ? desc_img[off] : 0);
  }
  return v;
}

static void dmem_drive(Vmilan_datapath *dut) {
  const bool beat = dm_busy && dm_wait == 0;
  dut->i_desc_mem_req_ready = dm_busy ? 0 : 1;
  dut->i_desc_mem_rsp_valid = beat ? 1 : 0;
  dut->i_desc_mem_rsp_data = beat ? desc_beat(dm_cur) : 0;
  dut->i_desc_mem_rsp_last = (beat && dm_left == 1) ? 1 : 0;
  dut->i_desc_mem_rsp_err = 0;
}

static void dmem_edge(Vmilan_datapath *dut) {
  if (!dm_busy) {
    if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
      dm_cur = dut->o_desc_mem_req_addr;
      dm_left = (int)dut->o_desc_mem_req_beats;
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

static std::vector<std::vector<uint8_t>> tx_frames;
static std::vector<uint64_t> tx_sof_ns;
static std::vector<uint8_t> tx_cur;
static bool tx_open = false;
static uint64_t sim_cyc = 0;

struct CycleFires {
  bool rx = false;
  bool axi_wr = false;
  bool axi_b = false;
  bool axi_ar = false;
  bool axi_r = false;
  uint32_t axi_rdata = 0;
};

static CycleFires tick(Vmilan_datapath *dut) {
  dut->axis_clk = 0; dut->gtx_clk = 0;
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
  rmem_edge(dut); dmem_edge(dut);
  dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval();
  sim_cyc++;
  return fire;
}

static void axi_write(Vmilan_datapath *dut, uint16_t addr, uint32_t data) {
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

static uint32_t axi_read(Vmilan_datapath *dut, uint16_t addr) {
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

static void run(Vmilan_datapath *dut, uint64_t n) {
  while (n--) tick(dut);
}

static void send_wide(Vmilan_datapath *dut,
                      const std::vector<uint8_t> &bytes) {
  for (size_t off = 0; off < bytes.size(); off += 8) {
    uint64_t data = 0;
    uint8_t keep = 0;
    for (size_t i = 0; i < 8 && off + i < bytes.size(); i++) {
      data |= (uint64_t)bytes[off + i] << (8 * i);
      keep |= (uint8_t)(1u << i);
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

static size_t pd_scan = 0;
static int pd_answers = 0;
static int64_t pd_target = 600;
static int64_t pd_expect = 0;
static void service_pdelay(Vmilan_datapath *dut) {
  while (pd_scan < tx_frames.size()) {
    const size_t req_ix = pd_scan++;
    const std::vector<uint8_t> req = tx_frames[req_ix];
    if (req.size() < 54 || req[12] != 0x88 || req[13] != 0xF7
        || (req[14] & 0xF) != 0x2)
      continue;
    const uint16_t seq = (uint16_t)((req[44] << 8) | req[45]);
    const uint64_t t1 = tx_sof_ns[req_ix];
    run(dut, 300);
    const uint64_t now = sim_cyc * 8;
    const uint64_t t2 = 5000000ull + now;
    const int64_t residence = (int64_t)(now - t1) - 2 * pd_target;
    const uint64_t t3 = t2 + (uint64_t)residence;
    const uint64_t t4_est = (sim_cyc + 1) * 8;
    pd_expect = ((int64_t)(t4_est - t1) - residence) / 2;
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

static void run_peer(Vmilan_datapath *dut, uint64_t n) {
  for (uint64_t i = 0; i < n; i++) {
    tick(dut);
    if ((i & 255) == 0) service_pdelay(dut);
  }
  service_pdelay(dut);
}

static void announce(Vmilan_datapath *dut, uint16_t seq) {
  Frame a = ptp(0xB, seq, 0, 0x0008, 30);
  for (int i = 0; i < 10; i++) a.u8(0);
  a.u16(0xFFC4); a.u8(0);
  a.u8(100); a.u32(PEER_CQ); a.u8(248);
  a.u64(GMID);
  a.u16(0); a.u8(0xA0);
  send_wide(dut, a.b);
}

static std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t seq,
                                         const std::vector<uint8_t> &pl) {
  const size_t flen = std::max<size_t>(60, 38 + pl.size());
  std::vector<uint8_t> f(flen, 0);
  const uint8_t src[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
  memcpy(f.data() + 6, src, 6);
  f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
  const uint16_t cdl = (uint16_t)(12 + pl.size());
  f[16] = (uint8_t)((cdl >> 8) & 7); f[17] = (uint8_t)cdl;
  const uint8_t target[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
  const uint8_t controller[8] = {0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
  memcpy(f.data() + 18, target, 8);
  memcpy(f.data() + 26, controller, 8);
  f[34] = (uint8_t)(seq >> 8); f[35] = (uint8_t)seq;
  f[36] = (uint8_t)((cmd >> 8) & 0x7F); f[37] = (uint8_t)cmd;
  std::copy(pl.begin(), pl.end(), f.begin() + 38);
  return f;
}

static size_t aecp_scan = 0;
static std::vector<uint8_t> await_aecp(Vmilan_datapath *dut, uint16_t seq,
                                       uint16_t cmd, int max_cycles = 200000) {
  for (int cyc = 0; cyc < max_cycles; cyc++) {
    while (aecp_scan < tx_frames.size()) {
      std::vector<uint8_t> f = tx_frames[aecp_scan++];
      if (f.size() > 37 && f[12] == 0x22 && f[13] == 0xF0
          && f[14] == 0xFB && (f[15] & 0xF) == 1
          && (((unsigned)f[34] << 8) | f[35]) == seq
          && ((((unsigned)f[36] & 0x7F) << 8) | f[37]) == cmd)
        return f;
    }
    tick(dut);
  }
  return {};
}

static std::vector<uint8_t> aecp_xact(Vmilan_datapath *dut, uint16_t cmd,
                                      uint16_t seq,
                                      const std::vector<uint8_t> &pl) {
  const std::vector<uint8_t> req = aecp_request(cmd, seq, pl);
  send_wide(dut, req);
  run(dut, 40);
  return await_aecp(dut, seq, cmd);
}

static uint64_t be64(const std::vector<uint8_t> &f, size_t off) {
  uint64_t v = 0;
  for (int i = 0; i < 8; i++) v = (v << 8) | f[off + i];
  return v;
}

static uint32_t be32(const std::vector<uint8_t> &f, size_t off) {
  uint32_t v = 0;
  for (int i = 0; i < 4; i++) v = (v << 8) | f[off + i];
  return v;
}

static int aecp_status(const std::vector<uint8_t> &f) {
  return f.size() > 16 ? (f[16] >> 3) & 0x1F : -1;
}

int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  expect("shipping AEM image generated", load_shipping_aemi(), 1);
  Vmilan_datapath *dut = new Vmilan_datapath;

  dut->axis_resetn = 0;
  dut->gtx_resetn = 0;
  dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
  dut->s_axi_bready = dut->s_axi_rready = 0;
  dut->s_axis_tx_tvalid = 0;
  dut->s_axis_mac_rx_tvalid = 0;
  dut->s_axis_mac_rx_tlast = 0;
  dut->m_axis_rx_tready = 1;
  dut->m_axis_ts_tready = 1;
  dut->m_axis_pcm_tready = 1;
  dut->m_axis_mac_tx_tready = 1;
  dut->i_mac_speed = 2;
  dut->i_link_up = 1;
  dut->i_full_duplex = 1;
  dut->i_mac_events = 0;
  for (int i = 0; i < 16; i++) tick(dut);
  dut->axis_resetn = 1;
  dut->gtx_resetn = 1;

  // Match the generated product identity. AECP targets the entity id, while
  // the descriptor image supplies the same identity to the processor store.
  axi_write(dut, 0x608, 0x020000FF);
  axi_write(dut, 0x604, 0xFE000001);
  axi_write(dut, 0x504, 8u << 24);       // 8.0 ns; matches sim_cyc model

  // The option is omitted from this elaboration: these are assertions about
  // the RTL default.  Before any peer answers, the engine's committed bank is
  // zero. Writes to the old software mirror remain accepted for ABI safety but
  // cannot change any live read or manufacture a healthy CLKV claim.
  expect("default-on VERSION", axi_read(dut, 0x004), 0x00020055);
  axi_write(dut, 0x624, 0x55667788); axi_write(dut, 0x628, 0x11223344);
  axi_write(dut, 0x6E4, 1234);
  axi_write(dut, 0x730, 0xDDEEFF00); axi_write(dut, 0x734, 0x99AABBCC);
  axi_write(dut, 0x778, 0x00000085); // sync + asCapable + live SW lease
  expect("fabric GM low overrides SW", axi_read(dut, 0x624), 0);
  expect("fabric GM high overrides SW", axi_read(dut, 0x628), 0);
  expect("fabric pdelay overrides SW", axi_read(dut, 0x6E4), 0);
  expect("fabric parent low overrides SW", axi_read(dut, 0x730), 0);
  expect("fabric parent high overrides SW", axi_read(dut, 0x734), 0);
  uint32_t clkv = axi_read(dut, 0x77C);
  expect("software lease cannot clear tu", clkv & 1, 1);
  expect("software sync claim hidden", (clkv >> 1) & 1, 0);
  expect("software lease fields hidden", (clkv >> 2) & 0x3FFF, 0);
  expect("software asCapable hidden", (clkv >> 16) & 1, 0);

  // A_TXARB_DIAG is a public ABI, not a comment about implementation names.
  // Exercise the real default-only gptp_ctl_mux and prove its three verdicts
  // reach lane 4.  The counter preloads below shorten a 2^16 watchdog wait;
  // adp_tx/sim_super is the behavioral source-abandonment oracle, while this
  // white-box stimulus proves the parent integration's bit mapping.
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

  // scan the MAC boundary for the plane's boot Pdelay_Req: an 0x88F7
  // frame whose transportSpecific|msgType byte is 0x12
  bool seen_pdreq = false;
  bool seen_ann = false;
  size_t boot_scan = tx_frames.size();
  for (uint64_t n = 0; n < 12000000ull; n++) {
    tick(dut);
    while (boot_scan < tx_frames.size()) {
      const std::vector<uint8_t> &frame = tx_frames[boot_scan++];
      if (frame.size() > 14 && frame[12] == 0x88 && frame[13] == 0xF7) {
        if (frame[14] == 0x12) seen_pdreq = true;
        if (frame[14] == 0x1B) seen_ann = true;
      }
    }
  }
  expect("the plane's Pdelay_Req reaches the MAC", seen_pdreq, 1);
  // no peer ever answers, so asCapable never rises: the announce
  // receipt timeout expires inside the scan window but the becgate
  // must HOLD -- an Announce here would mean an ungated become-master
  expect("no Announce without asCapable", seen_ann, 0);

  // Ignore requests accumulated during the deliberately unanswered phase.
  // Two fresh fabric-timestamped exchanges raise asCapable; the peer then
  // announces a nonzero GM and parent which the engine publishes atomically.
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
         (int64_t)(int32_t)pdelay >= pd_expect - 32
         && (int64_t)(int32_t)pdelay <= pd_expect + 32, 1);
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

  announce(dut, 0x7001);
  uint64_t gm = 0;
  for (int n = 0; n < 32 && gm != GMID; n++) {
    run(dut, 1000);
    gm = ((uint64_t)axi_read(dut, 0x628) << 32) | axi_read(dut, 0x624);
  }
  const uint64_t parent = ((uint64_t)axi_read(dut, 0x734) << 32)
                        | axi_read(dut, 0x730);
  expect("peer-driven GM reached live CSR", gm, GMID);
  expect("peer-driven parent reached live CSR", parent, PEER_CID);

  // The same nonzero committed bank must traverse the processor's gather
  // face and the real AECP response buffer onto the shared MAC wire.
  aecp_scan = tx_frames.size();
  std::vector<uint8_t> avb = aecp_xact(
      dut, 0x0027, 0x7101, {0x00, 0x09, 0x00, 0x00});
  expect("GET_AVB_INFO response length", avb.size(), 62);
  expect("GET_AVB_INFO SUCCESS", aecp_status(avb), 0);
  expect("GET_AVB_INFO cdl", avb.size() >= 18
         ? ((((unsigned)avb[16] & 7) << 8) | avb[17]) : 0, 36);
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
  expect("GET_AS_PATH padded wire length", path.size(), 60);
  expect("GET_AS_PATH SUCCESS", aecp_status(path), 0);
  expect("GET_AS_PATH cdl", path.size() >= 18
         ? ((((unsigned)path[16] & 7) << 8) | path[17]) : 0, 32);
  expect("GET_AS_PATH count two", path.size() >= 42
         ? be32(path, 38) : 0, 2);
  expect("GET_AS_PATH ordered GM", path.size() >= 50
         ? be64(path, 42) : 0, GMID);
  expect("GET_AS_PATH ordered parent", path.size() >= 58
         ? be64(path, 50) : 0, PEER_CID);
  expect("GET_AS_PATH zero Ethernet pad", path.size() >= 60
         ? ((unsigned)path[58] << 8) | path[59] : 1, 0);

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  delete dut;
  return fails ? 1 : 0;
}
