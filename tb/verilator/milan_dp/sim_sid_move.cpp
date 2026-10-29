// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Protocol processor #202 recovery: through the whole datapath, at
// compressed time.
//
// After a MAAP conflict the processor withdraws each declaring source,
// re-allocates at once and, at the grant, moves the source to a new Stream ID
// (IEEE 802.1Q-2018 35.2.2.8 gaps only a re-declaration of the same StreamID;
// Milan v1.2 Table 5.3, 5.3.7.5, lets the PAAD take another one). It publishes
// each source's current ID on src_stream_id_o. A listener binds through
// PROBE_TX and registers for the ID the answer names, so the stream frames
// (IEEE 1722-2016 4.4.4.8, the AVTP stream_id) and a STREAM_OUTPUT's
// GET_STREAM_INFO stream_id (IEEE 1722.1-2021 7.4.16.2, "the current id of
// the stream") must name the same ID, before the move and after it.
//
// Two elaborations run it, both on the shared compressed millisecond grid
// (the processor's millisecond and KL_maap's millisecond both MS_CYC_TB
// cycles):
//   the 1x1 shipping shape, endstation_ax7101_1x1_tdm8: AAF talker 0 and the
//                CRF Media Clock Output (source uid 1) stream;
//   the 8x8 shape, endstation_ax7101_8x8: AAF talkers 0 and 1 stream, and
//                talker 1's unique ID is named explicitly in its TCTX record
//                (uid 1, equal to the derived one), the software override
//                the framer used to let outrank the processor.
// GRADED_MASK_TB names the source uids a leg streams and grades;
// NAMED_UID_TALKER_TB the AAF talker whose TCTX uid it names (-1: none).
// Phases:
//   boot:   identity, the firmware boot values, the named talker's TCTX uid.
//   bind:   the graded sources probed; MAAP claims a block and grants; the
//           switch declares Listener Ready for the ID each PROBE_TX answer
//           names; each source streams. The wire, PROBE_TX, GET_STREAM_INFO
//           selector 2, the Talker Advertise and src_stream_id_o agree.
//   move:   a peer ANNOUNCEs the claimed block from a lower MAC (IEEE
//           1722-2016 B.3.6.4 compare_MAC: this station re-addresses). Every
//           declaring source withdraws, takes a new Stream ID at its grant and
//           declares it at once; the listener re-probes and binds to it.
//   after:  for each source: a new ID with the old upper 48 bits, declared
//           under 2 s after the conflict; the wire, PROBE_TX, GET_STREAM_INFO,
//           the Talker Advertise and src_stream_id_o all name it; no frame
//           carries the withdrawn ID after its withdrawal; the named TCTX uid
//           is still held and does not reach the wire.

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <filesystem>
#include <functional>
#include <map>
#include <string>
#include <vector>

#ifndef MS_CYC_TB
#error "MS_CYC_TB must be the processor and KL_maap millisecond, in cycles"
#endif
#ifndef SOURCES_TB
#error "SOURCES_TB must be the talker source count (the AAF talkers plus the CRF output)"
#endif
#ifndef GRADED_MASK_TB
#error "GRADED_MASK_TB must name the source uids this leg streams and grades"
#endif
#ifndef NAMED_UID_TALKER_TB
#error "NAMED_UID_TALKER_TB must name the AAF talker whose TCTX uid is set (-1: none)"
#endif
#ifndef SHAPE8_TB
#error "SHAPE8_TB must say which shape this leg elaborates (1: endstation_ax7101_8x8)"
#endif

namespace {

constexpr uint64_t kMsCyc = MS_CYC_TB;
//! the end-station config whose AEM image the elaborated shape ships
#if SHAPE8_TB
constexpr char kAemiCfg[] = "endstation_ax7101_8x8";
#else
constexpr char kAemiCfg[] = "endstation_ax7101_1x1_tdm8";
#endif
constexpr uint64_t kNever = ~0ull;
constexpr uint64_t ms(uint64_t n) { return n * kMsCyc; }

//! A captured AVTP stream PDU.
struct StreamPdu {
    uint64_t cyc = 0;
    int subtype = 0;
    uint64_t sid = 0;
    uint64_t da = 0;
};

//! What the DUT declared for one Talker Advertise value (802.1Q 35.2.2.8).
struct TaSeen {
    uint64_t first_join = kNever;   // first New / JoinIn / JoinMt
    uint64_t last_leave = kNever;   // latest Lv
};

//! One source's listener and the switch port in front of it.
struct Peer {
    bool want = false;
    int status = -1;                // last PROBE_TX answer
    uint64_t answered_sid = 0;      // stream_id of the last SUCCESS answer
    uint64_t answered_da = 0;
    uint64_t answered_at = kNever;
    uint64_t ready_sid = 0;         // the switch's Listener Ready, 0 = none
    long probes = 0;
};

class SidMoveHarness {
 public:
    int run();

 private:
    Vmilan_datapath* dut = nullptr;
    long checks = 0;
    long fails = 0;
    uint64_t cyc = 0;

    static constexpr uint64_t kTestEid = 0x001BC50CAC000001ull;
    static constexpr uint32_t kStaMacLo = 0x00000002u;   // 02:00:00:00
    static constexpr uint32_t kStaMacHi = 0x00000100u;   // 00:01
    static constexpr uint64_t kStaMac = 0x020000000001ull;
    static constexpr uint64_t kCtlrMac = 0x021122334455ull;
    static constexpr uint64_t kCtlrEid = 0xC0FFEE00DEADBEEFull;
    //! a peer whose MAC wins compare_MAC (B.3.6.4: octet-reversed, lower wins)
    static constexpr uint64_t kPeerMac = 0x020000000000ull;
    static constexpr int kSources = SOURCES_TB;
    static constexpr int kUidCrf = kSources - 1;     // CRF_TUID_C = N_STREAMS
    static constexpr uint32_t kGraded = GRADED_MASK_TB;
    static constexpr int kNamed = NAMED_UID_TALKER_TB;
    std::vector<int> graded;
    static constexpr uint64_t kMaapPoolBase = 0x91E0F0000000ull;

    static constexpr uint16_t A_ID = 0x000;
    static constexpr uint16_t A_MAC_ALO = 0x108;
    static constexpr uint16_t A_MAC_AHI = 0x10C;
    static constexpr uint16_t A_ADP_EIDLO = 0x604;
    static constexpr uint16_t A_ADP_EIDHI = 0x608;
    static constexpr uint16_t A_ADP_TALKER = 0x618;
    static constexpr uint16_t A_AAF_CTRL = 0x654;
    static constexpr uint16_t A_LWSRP_CTRL = 0x680;
    static constexpr uint16_t A_MAAP_CTRL = 0x6CC;
    static constexpr uint16_t A_MAAP_STAT0 = 0x6D0;
    static constexpr uint16_t A_MAAP_STAT1 = 0x6D4;
    static constexpr uint16_t A_CRFT_CTRL = 0x750;
    static constexpr uint16_t A_STRM_SEL = 0x800;
    static constexpr uint16_t A_STRMW_CTRL = 0x810;
    static constexpr uint16_t A_STRMW_DMAC_HI = 0x820;
    static constexpr uint16_t A_PP_CTRL = 0x920;

    // ---- the AECP response memory: every AECP answer is assembled in it (the
    // sim_nxn model, ported in shape from tb/verilator/pp_shadow). wr_ready goes
    // LOW while a commit is owed, so wr_done never meets the ready that took
    // the write (KL_aecp_resp_buf's flush arm needs exactly that).
    static constexpr uint32_t RESP_BASE  = 0x20100000u;   // PP_RESP_BASE_P default
    static constexpr uint32_t RESP_BYTES = 592u;          // 16 + PP_DESC_LINE_BYTES_P
    uint8_t  rmem[RESP_BYTES] = {};
    bool     rm_busy  = false;
    uint32_t rm_cur   = 0;
    int      rm_left  = 0;
    bool     rm_wpend = false;
    uint32_t rm_waddr = 0;
    uint64_t rm_wdata = 0;
    uint32_t rm_wstrb = 0;
    uint64_t rmem_beat(uint32_t byte_addr) const;
    void rmem_drive();
    void rmem_edge();

    // ---- the AEM descriptor memory (the sim_nxn model): AECP is held from
    // reset until the D3 walk has proven this image, so GET_STREAM_INFO needs
    // it. One outstanding burst, in order, the first beat DESC_MISS_CYC late,
    // a one-clock bubble every DESC_GAP_EVERY beats.
    static constexpr uint32_t DESC_BASE = 0x20000000u;   // PP_DESC_BASE_P default
    static constexpr int DESC_MISS_CYC  = 142;
    static constexpr int DESC_GAP_EVERY = 4;
    std::vector<uint8_t> desc_img;
    bool     dm_busy = false;
    uint32_t dm_cur  = 0;
    int      dm_left = 0;
    int      dm_wait = 0;
    int      dm_run  = 0;
    uint64_t desc_beat(uint32_t byte_addr) const;
    void dmem_drive();
    void dmem_edge();
    bool load_the_image(std::string* why);
    void start_the_restore_walk();

    std::deque<std::vector<uint8_t>> rx_q;
    size_t rx_beat = 0;
    int rx_gap = 0;
    std::vector<uint8_t> tx_cur;
    std::vector<StreamPdu> pdus;
    std::map<uint64_t, TaSeen> ta;          // per declared stream_id
    std::map<uint16_t, std::vector<uint8_t>> aecp_resp;   // by sequence_id
    std::multimap<uint64_t, std::function<void()>> sched;
    Peer peer[kSources];
    long dut_malformed = 0;
    uint16_t aecp_seq = 0x2020;
    size_t aecp_seen = 0;

    void lo();
    void hi();
    void step() { lo(); hi(); }
    void run_until(uint64_t t) { while (cyc < t) step(); }
    double t_ms(uint64_t c) const { return static_cast<double>(c) / static_cast<double>(kMsCyc); }
    void run_schedule();
    void rx_drive();
    void rx_edge();
    void observe();
    void tx_frame_done();
    void axi_write(uint16_t a, uint32_t d);
    uint32_t axi_read(uint16_t a);
    void do_reset();

    static void put_be(std::vector<uint8_t>& f, size_t off, uint64_t v, int n);
    static uint64_t get_be(const std::vector<uint8_t>& f, size_t off, int n);
    static std::vector<uint8_t> msrp_frame(const std::vector<uint8_t>& payload);
    std::vector<uint8_t> probe_tx(int uid);
    static std::vector<uint8_t> listener_msg(uint64_t sid, int ev, int decl);
    static std::vector<uint8_t> domain_msg();
    static std::vector<uint8_t> maap_announce(uint64_t src, uint16_t off, uint16_t cnt);
    std::vector<uint8_t> gsi_cmd(int ix, uint16_t seq);
    void on_mrpdu(const std::vector<uint8_t>& f);
    void on_acmp(const std::vector<uint8_t>& f);
    void on_aecp(const std::vector<uint8_t>& f);
    void on_stream_pdu(const std::vector<uint8_t>& f, size_t avtp);

    void at(uint64_t when, std::function<void()> fn) { sched.emplace(when, std::move(fn)); }
    void probe(int uid);
    void bridge_ready(int uid, uint64_t sid);
    void bridge_withdraw(int uid);

    void ck(const char* what, uint64_t got, uint64_t exp);
    void ck_true(const char* what, bool cond);
    uint64_t published(int s) const;
    uint64_t gsi_stream_id(int ix);
    uint64_t named_uid() const;
    uint64_t block_base() { return kMaapPoolBase | (axi_read(A_MAAP_STAT0) & 0xFFFFu); }
    int source_of_da(uint64_t da, uint64_t base) const;
    void grade_agreement(const char* phase, uint64_t base, uint64_t from);

    void boot();
    void phase_a();
    void phase_move();
};

// ============================================================================
//  clocking: the peers act first, then the inputs settle, then the model
// ============================================================================
void SidMoveHarness::lo() {
    run_schedule();
    rx_drive();
    rmem_drive();
    dmem_drive();
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0;
    dut->eval();
    rmem_edge();
    dmem_edge();
    observe();
    rx_edge();
}

uint64_t SidMoveHarness::desc_beat(uint32_t byte_addr) const {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {                 // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - DESC_BASE + static_cast<uint32_t>(i);
        v = (v << 8) | static_cast<uint64_t>((off < desc_img.size()) ? desc_img[off] : 0);
    }
    return v;
}

void SidMoveHarness::dmem_drive() {
    const bool answering = !desc_img.empty();
    const bool beat = answering && dm_busy && (dm_wait == 0);
    dut->i_desc_mem_req_ready = (answering && !dm_busy) ? 1 : 0;
    dut->i_desc_mem_rsp_valid = beat ? 1 : 0;
    dut->i_desc_mem_rsp_data  = beat ? desc_beat(dm_cur) : 0;
    dut->i_desc_mem_rsp_last  = (beat && dm_left == 1) ? 1 : 0;
    dut->i_desc_mem_rsp_err   = 0;
}

void SidMoveHarness::dmem_edge() {
    if (desc_img.empty()) return;
    if (!dm_busy) {
        if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
            dm_cur  = dut->o_desc_mem_req_addr;
            dm_left = static_cast<int>(dut->o_desc_mem_req_beats);
            dm_busy = (dm_left > 0);
            dm_wait = DESC_MISS_CYC;
            dm_run  = 0;
        }
    } else if (dm_wait > 0) {
        dm_wait--;
    } else if (dut->o_desc_mem_rsp_ready) {
        dm_cur += 8;
        if (--dm_left <= 0) dm_busy = false;
        else if (++dm_run == DESC_GAP_EVERY) { dm_run = 0; dm_wait = 1; }
    }
}

//! The image the build ships, regenerated the way sim_nxn does it: the
//! end-station builder's overlay packed by avdecc/gen_aemi_image.py.
bool SidMoveHarness::load_the_image(std::string* why) {
    const char* scratch = getenv("TMPDIR");
    if (!scratch || !*scratch) scratch = "/tmp";
    std::string tmpl = std::string(scratch) + "/milan_sidmove_XXXXXX";
    std::vector<char> buf(tmpl.begin(), tmpl.end());
    buf.push_back('\0');
    const char* made = mkdtemp(buf.data());
    if (!made) { *why = "cannot create the image scratch directory"; return false; }
    const std::string dir(made);
    const std::string cfg(kAemiCfg);
    const std::string log = dir + "/generator.log";
    const std::string bld = dir + "/builder";
    const std::string bin = dir + "/image.bin";
    const std::string cmd1 = "python3 ../../../sw/builder/endstation_builder.py ../../../configs/"
                             + cfg + ".yaml -o '" + bld + "' > '" + log + "' 2>&1";
    const std::string cmd2 = "python3 ../../../avdecc/gen_aemi_image.py --overlay '" + bld + "/"
                             + cfg + "/aem_overlay.json' -o '" + bin + "' --json '" + dir
                             + "/image.json' --line-bytes 576 > '" + log + "' 2>&1";
    if (system(cmd1.c_str()) != 0) { *why = "endstation_builder.py failed: " + log; return false; }
    if (system(cmd2.c_str()) != 0) { *why = "gen_aemi_image.py failed: " + log; return false; }
    FILE* fh = fopen(bin.c_str(), "rb");
    if (!fh) { *why = "the generator wrote no image"; return false; }
    uint8_t chunk[4096];
    size_t n;
    while ((n = fread(chunk, 1, sizeof chunk, fh)) > 0) desc_img.insert(desc_img.end(), chunk, chunk + n);
    fclose(fh);
    std::error_code ec;
    std::filesystem::remove_all(dir, ec);
    return !desc_img.empty();
}

//! The boot restore walk as the firmware starts it (PP_CTRL[1]) once the image
//! is in place: with no NVM media the backend answers blank and the walk ends
//! COMPLETE (sim_nxn start_the_boot_restore_walk), which releases AECP.
void SidMoveHarness::start_the_restore_walk() {
    constexpr uint16_t A_PP_STAT = 0x924;
    constexpr uint32_t kDone = 1u << 2;
    constexpr uint32_t kClosed = 1u << 16;
    axi_write(A_PP_CTRL, axi_read(A_PP_CTRL) | 0x2u);
    uint32_t st = 0;
    for (int r = 0; r < 4000 && !(st & (kDone | kClosed)); r++) {
        for (int c = 0; c < 64; c++) step();
        st = axi_read(A_PP_STAT);
    }
    ck("[BOOT] PP_STAT the restore walk sequenced (done 1, CLOSED 0)", st & (kDone | kClosed), kDone);
}

uint64_t SidMoveHarness::rmem_beat(uint32_t byte_addr) const {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {                 // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - RESP_BASE + static_cast<uint32_t>(i);
        v = (v << 8) | static_cast<uint64_t>((off < RESP_BYTES) ? rmem[off] : 0);
    }
    return v;
}

void SidMoveHarness::rmem_drive() {
    dut->i_resp_mem_req_ready = rm_busy ? 0 : 1;
    dut->i_resp_mem_rsp_valid = rm_busy ? 1 : 0;
    dut->i_resp_mem_rsp_data  = rm_busy ? rmem_beat(rm_cur) : 0;
    dut->i_resp_mem_rsp_last  = (rm_busy && rm_left == 1) ? 1 : 0;
    dut->i_resp_mem_rsp_err   = 0;
    dut->i_resp_mem_wr_ready  = rm_wpend ? 0 : 1;
    dut->i_resp_mem_wr_done   = rm_wpend ? 1 : 0;
    dut->i_resp_mem_wr_err    = 0;
}

void SidMoveHarness::rmem_edge() {
    if (!rm_busy) {
        if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
            rm_cur  = dut->o_resp_mem_req_addr;
            rm_left = static_cast<int>(dut->o_resp_mem_req_beats);
            rm_busy = (rm_left > 0);
        }
    } else if (dut->o_resp_mem_rsp_ready) {
        rm_cur += 8;
        if (--rm_left <= 0) rm_busy = false;
    }
    if (rm_wpend) {
        for (int i = 0; i < 8; i++) {
            if (rm_wstrb & (1u << i)) {
                const uint32_t k = rm_waddr - RESP_BASE + static_cast<uint32_t>(i);
                if (k < RESP_BYTES) rmem[k] = static_cast<uint8_t>(rm_wdata >> (56 - 8 * i));
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

void SidMoveHarness::hi() {
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1;
    dut->eval();
    cyc++;
}

void SidMoveHarness::run_schedule() {
    while (!sched.empty() && sched.begin()->first <= cyc) {
        const std::function<void()> fn = sched.begin()->second;
        sched.erase(sched.begin());
        fn();
    }
}

//! Frames are fed LITTLE-LANE (tdata[7:0] = first wire byte), the RX tap's
//! convention, with a short gap between frames.
void SidMoveHarness::rx_drive() {
    if (rx_q.empty() || rx_gap > 0) {
        dut->s_axis_mac_rx_tvalid = 0;
        dut->s_axis_mac_rx_tlast = 0;
        return;
    }
    const std::vector<uint8_t>& f = rx_q.front();
    const size_t beats = (f.size() + 7) / 8;
    uint64_t d = 0;
    uint8_t k = 0;
    for (size_t i = 0; i < 8; i++) {
        const size_t o = rx_beat * 8 + i;
        if (o < f.size()) {
            d |= static_cast<uint64_t>(f[o]) << (8 * i);
            k = static_cast<uint8_t>(k | (1u << i));
        }
    }
    dut->s_axis_mac_rx_tdata = d;
    dut->s_axis_mac_rx_tkeep = k;
    dut->s_axis_mac_rx_tvalid = 1;
    dut->s_axis_mac_rx_tlast = (rx_beat + 1 == beats) ? 1 : 0;
}

void SidMoveHarness::rx_edge() {
    if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) {
        rx_beat++;
        if (rx_beat * 8 >= rx_q.front().size()) {
            rx_q.pop_front();
            rx_beat = 0;
            rx_gap = 16;
        }
    } else if (rx_gap > 0) {
        rx_gap--;
    }
}

void SidMoveHarness::observe() {
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
        const uint8_t keep = static_cast<uint8_t>(dut->m_axis_mac_tx_tkeep);
        const uint64_t d = dut->m_axis_mac_tx_tdata;
        for (int l = 0; l < 8; l++)
            if ((keep >> l) & 1) tx_cur.push_back(static_cast<uint8_t>(d >> (8 * l)));
        if (dut->m_axis_mac_tx_tlast) {
            tx_frame_done();
            tx_cur.clear();
        }
    }
}

// ============================================================================
//  the AXI4-Lite BFM (the datapath suite's protocol and timing)
// ============================================================================
void SidMoveHarness::axi_write(uint16_t a, uint32_t d) {
    constexpr int kGuard = 2048;
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < kGuard; g++) {
        lo();
        const bool acc = dut->s_axi_awready && dut->s_axi_wready;
        hi();
        if (acc) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < kGuard; g++) {
        lo();
        const bool bv = dut->s_axi_bvalid;
        hi();
        if (bv) break;
    }
    dut->s_axi_bready = 0;
}

uint32_t SidMoveHarness::axi_read(uint16_t a) {
    constexpr int kGuard = 2048;
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < kGuard; g++) {
        lo();
        const bool acc = dut->s_axi_arready;
        hi();
        if (acc) break;
    }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < kGuard; g++) {
        lo();
        const bool rv = dut->s_axi_rvalid;
        if (rv) d = dut->s_axi_rdata;
        hi();
        if (rv) break;
    }
    dut->s_axi_rready = 0;
    return d;
}

void SidMoveHarness::do_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0; dut->s_axi_arvalid = 0;
    dut->s_axi_bready = 0; dut->s_axi_rready = 0;
    dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 16; i++) step();
}

// ============================================================================
//  frames (wire order, byte 0 = the first destination-address octet)
// ============================================================================
void SidMoveHarness::put_be(std::vector<uint8_t>& f, size_t off, uint64_t v, int n) {
    for (int i = 0; i < n; i++)
        f[off + static_cast<size_t>(i)] = static_cast<uint8_t>(v >> (8 * (n - 1 - i)));
}

uint64_t SidMoveHarness::get_be(const std::vector<uint8_t>& f, size_t off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | f[off + static_cast<size_t>(i)];
    return v;
}

//! An MRPDU from the switch port to the Nearest Bridge group, EtherType MSRP.
std::vector<uint8_t> SidMoveHarness::msrp_frame(const std::vector<uint8_t>& payload) {
    std::vector<uint8_t> f(14, 0);
    put_be(f, 0, 0x0180C200000Eull, 6);
    put_be(f, 6, 0x020B2100000Eull, 6);
    put_be(f, 12, 0x22EA, 2);
    f.push_back(0x00);
    f.insert(f.end(), payload.begin(), payload.end());
    f.push_back(0x00);
    f.push_back(0x00);
    if (f.size() < 60) f.resize(60, 0);
    return f;
}

//! Milan PROBE_TX = IEEE 1722.1 CONNECT_TX_COMMAND aimed at our source `uid`.
std::vector<uint8_t> SidMoveHarness::probe_tx(int uid) {
    std::vector<uint8_t> f(70, 0);
    put_be(f, 0, 0x91E0F0010000ull, 6);
    put_be(f, 6, kCtlrMac, 6);
    put_be(f, 12, 0x22F0, 2);
    f[14] = 0xFC;                                  // ACMP
    f[15] = 0x00;                                  // CONNECT_TX_COMMAND
    f[17] = 44;                                    // control_data_length
    put_be(f, 26, kCtlrEid, 8);                    // @12 controller_entity_id
    put_be(f, 34, kTestEid, 8);                    // @20 talker_entity_id
    put_be(f, 42, 0x2222222222222222ull, 8);       // @28 listener_entity_id
    put_be(f, 50, static_cast<uint64_t>(uid), 2);  // @36 talker_unique_id
    put_be(f, 62, static_cast<uint64_t>(peer[uid].probes + 1), 2);   // @48 sequence_id
    return f;
}

//! One Listener message, one value (802.1Q 35.2.2.7): event `ev` (0 New,
//! 5 Lv), declaration `decl` (2 Ready).
std::vector<uint8_t> SidMoveHarness::listener_msg(uint64_t sid, int ev, int decl) {
    std::vector<uint8_t> m(18, 0);
    m[0] = 3;
    m[1] = 8;
    put_be(m, 2, 14, 2);
    put_be(m, 4, 1u, 2);
    put_be(m, 6, sid, 8);
    m[14] = static_cast<uint8_t>(ev * 36);
    m[15] = static_cast<uint8_t>(decl << 6);
    return m;
}

//! The switch's Domain: NumberOfValues 2 from {SRclassID 5, priority 2, VID
//! 2}, so class A {6, 3, 2} is value 1 (the message a Milan switch sends).
std::vector<uint8_t> SidMoveHarness::domain_msg() {
    std::vector<uint8_t> m(13, 0);
    m[0] = 4;
    m[1] = 4;
    put_be(m, 2, 9, 2);
    put_be(m, 4, 2u, 2);
    m[6] = 5; m[7] = 2; put_be(m, 8, 2, 2);
    m[10] = static_cast<uint8_t>(1 * 36 + 1 * 6);
    return m;
}

//! A MAAP ANNOUNCE (IEEE 1722-2016 Figure B.1, B.3.6.7) from `src` claiming
//! pool offsets [off, off + cnt): message_type 3, maap_version 1, cdl 16.
std::vector<uint8_t> SidMoveHarness::maap_announce(uint64_t src, uint16_t off, uint16_t cnt) {
    std::vector<uint8_t> f(60, 0);
    put_be(f, 0, 0x91E0F000FF00ull, 6);
    put_be(f, 6, src, 6);
    put_be(f, 12, 0x22F0, 2);
    f[14] = 0xFE;
    f[15] = 0x03;
    f[16] = 0x08;
    f[17] = 16;
    put_be(f, 26, kMaapPoolBase | off, 6);
    put_be(f, 32, cnt, 2);
    return f;
}

//! AEM GET_STREAM_INFO (command_type 0x000F) for STREAM_OUTPUT `ix` (IEEE
//! 1722.1-2021 7.4.16.1: descriptor_type 0x0006, descriptor_index).
std::vector<uint8_t> SidMoveHarness::gsi_cmd(int ix, uint16_t seq) {
    std::vector<uint8_t> f(60, 0);
    put_be(f, 0, kStaMac, 6);
    put_be(f, 6, kCtlrMac, 6);
    put_be(f, 12, 0x22F0, 2);
    f[14] = 0xFB;                                  // AECP, AEM_COMMAND
    f[15] = 0x00;
    put_be(f, 16, 12 + 4, 2);                      // control_data_length
    put_be(f, 18, kTestEid, 8);                    // target_entity_id
    put_be(f, 26, kCtlrEid, 8);                    // controller_entity_id
    put_be(f, 34, seq, 2);
    put_be(f, 36, 0x000F, 2);
    put_be(f, 38, 0x0006, 2);
    put_be(f, 40, static_cast<uint64_t>(ix), 2);
    return f;
}

// ============================================================================
//  what the DUT sends, and how the peers answer it
// ============================================================================
void SidMoveHarness::tx_frame_done() {
    const std::vector<uint8_t>& f = tx_cur;
    if (f.size() < 18) return;
    const uint64_t et = get_be(f, 12, 2);
    if (et == 0x22EA) {
        on_mrpdu(f);
    } else if (et == 0x8100 && f.size() >= 30 && get_be(f, 16, 2) == 0x22F0) {
        on_stream_pdu(f, 18);
    } else if (et == 0x22F0 && f[14] == 0xFC) {
        on_acmp(f);
    } else if (et == 0x22F0 && f[14] == 0xFB) {
        on_aecp(f);
    } else if (et == 0x22F0 && f.size() >= 26 && f[14] != 0xFE && f[14] != 0xFA) {
        on_stream_pdu(f, 14);
    }
}

void SidMoveHarness::on_stream_pdu(const std::vector<uint8_t>& f, size_t avtp) {
    const int subtype = f[avtp];
    if (subtype != 0x04 && subtype != 0x02) return;   // CRF, AAF
    StreamPdu p;
    p.cyc = cyc;
    p.subtype = subtype;
    p.sid = get_be(f, avtp + 4, 8);
    p.da = get_be(f, 0, 6);
    pdus.push_back(p);
}

//! CONNECT_TX_RESPONSE: status at wire byte 16 [7:3], stream_id @4 (18..25),
//! talker_unique_id @36 (50..51), stream_dest_mac @40 (54..59).
void SidMoveHarness::on_acmp(const std::vector<uint8_t>& f) {
    if ((f[15] & 0x0F) != 1 || f.size() < 70) return;
    const uint64_t uid64 = get_be(f, 50, 2);
    if (uid64 >= static_cast<uint64_t>(kSources)) return;
    const int uid = static_cast<int>(uid64);
    Peer& p = peer[uid];
    p.status = f[16] >> 3;
    printf("  [t] %11.2f ms  PROBE_TX answered, uid %d, status %d, stream_id %016llx\n",
           t_ms(cyc), uid, p.status, static_cast<unsigned long long>(get_be(f, 18, 8)));
    if (p.status == 0) {
        p.answered_sid = get_be(f, 18, 8);
        p.answered_da = get_be(f, 54, 6);
        p.answered_at = cyc;
        if (p.want && p.ready_sid != p.answered_sid) {
            const uint64_t sid = p.answered_sid;
            at(cyc + ms(40), [this, uid, sid] { if (peer[uid].want) bridge_ready(uid, sid); });
        }
    } else if (p.status == 3 && p.want) {
        at(cyc + ms(500), [this, uid] { if (peer[uid].want) probe(uid); });
    }
}

void SidMoveHarness::on_aecp(const std::vector<uint8_t>& f) {
    aecp_seen++;
    if (f.size() < 42 || (f[15] & 0x0F) != 1 || (f[36] & 0x80) != 0) return;
    aecp_resp[static_cast<uint16_t>(get_be(f, 34, 2))] = f;
}

//! Every Talker Advertise value (type 1), vector value k naming FirstValue's
//! stream_id + k (802.1Q 35.2.2.8): its events, and the peers' answer to a
//! withdrawal of the ID a listener is bound to.
void SidMoveHarness::on_mrpdu(const std::vector<uint8_t>& f) {
    size_t off = 15;
    while (off + 2 <= f.size() && !(f[off] == 0 && f[off + 1] == 0)) {
        if (off + 4 > f.size()) { dut_malformed++; return; }
        const int type = f[off];
        const int alen = f[off + 1];
        size_t p = off + 4;
        const size_t end = p + get_be(f, off + 2, 2);
        if (end > f.size()) { dut_malformed++; return; }
        while (p + 2 <= end && !(f[p] == 0 && f[p + 1] == 0)) {
            const int n = static_cast<int>(get_be(f, p, 2) & 0x1FFFu);
            p += 2;
            if (p + static_cast<size_t>(alen) > end) { dut_malformed++; return; }
            const uint64_t sid0 = (type == 1 && alen >= 8) ? get_be(f, p, 8) : 0;
            p += static_cast<size_t>(alen);
            std::vector<int> ev;
            for (int k = 0; k < (n + 2) / 3 && p < end; k++, p++) {
                const int b = f[p];
                ev.push_back(b / 36); ev.push_back((b / 6) % 6); ev.push_back(b % 6);
            }
            if (type == 3) p += static_cast<size_t>((n + 3) / 4);
            if (type != 1) continue;
            for (int k = 0; k < n && k < static_cast<int>(ev.size()); k++) {
                const uint64_t sid = sid0 + static_cast<uint64_t>(k);
                TaSeen& t = ta[sid];
                if (ev[static_cast<size_t>(k)] == 5) {
                    t.last_leave = cyc;
                    for (int s = 0; s < kSources; s++) {
                        if (peer[s].want && peer[s].ready_sid == sid) {
                            at(cyc + ms(2), [this, s] { bridge_withdraw(s); });
                            at(cyc + ms(500), [this, s] { if (peer[s].want) probe(s); });
                        }
                    }
                } else if (t.first_join == kNever) {
                    t.first_join = cyc;
                    printf("  [t] %11.2f ms  Talker Advertise first on the wire for %016llx (event %d)\n",
                           t_ms(cyc), static_cast<unsigned long long>(sid), ev[static_cast<size_t>(k)]);
                }
            }
        }
        off = end;
    }
}

void SidMoveHarness::probe(int uid) {
    peer[uid].probes++;
    rx_q.push_back(probe_tx(uid));
}

void SidMoveHarness::bridge_ready(int uid, uint64_t sid) {
    peer[uid].ready_sid = sid;
    rx_q.push_back(msrp_frame(listener_msg(sid, 0, 2)));
    printf("  [t] %11.2f ms  switch declares Listener Ready, uid %d, stream_id %016llx\n",
           t_ms(cyc), uid, static_cast<unsigned long long>(sid));
}

void SidMoveHarness::bridge_withdraw(int uid) {
    if (peer[uid].ready_sid == 0) return;
    rx_q.push_back(msrp_frame(listener_msg(peer[uid].ready_sid, 5, 2)));
    peer[uid].ready_sid = 0;
}

// ============================================================================
//  grading
// ============================================================================
void SidMoveHarness::ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    const bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-70s got=%016llx exp=%016llx\n", ok ? "PASS" : "FAIL", what,
           static_cast<unsigned long long>(got), static_cast<unsigned long long>(exp));
}

void SidMoveHarness::ck_true(const char* what, bool cond) {
    checks++;
    if (!cond) fails++;
    printf("  [%s] %s\n", cond ? "PASS" : "FAIL", what);
}

//! src_stream_id_o slice `s`, as the datapath names it (pp_cd_src_stream_id_w)
uint64_t SidMoveHarness::published(int s) const {
    const auto& w = dut->rootp->milan_datapath__DOT__pp_cd_src_stream_id_w;
    return (static_cast<uint64_t>(w[2 * s + 1]) << 32) | w[2 * s];
}

//! GET_STREAM_INFO(STREAM_OUTPUT ix): the stream_id field (frame 54..61,
//! after descriptor_type, descriptor_index, stream_info_flags and
//! stream_format), or ~0 when no SUCCESS answer came.
uint64_t SidMoveHarness::gsi_stream_id(int ix) {
    for (int attempt = 0; attempt < 20; attempt++) {
        const uint16_t seq = aecp_seq++;
        rx_q.push_back(gsi_cmd(ix, seq));
        const uint64_t until = cyc + ms(50);
        while (cyc < until && aecp_resp.count(seq) == 0) step();
        const auto it = aecp_resp.find(seq);
        if (it == aecp_resp.end()) continue;
        const std::vector<uint8_t> r = it->second;
        aecp_resp.erase(it);
        if (r.size() >= 62 && (r[16] >> 3) == 0 && get_be(r, 36, 2) == 0x000F
            && get_be(r, 38, 2) == 0x0006 && get_be(r, 40, 2) == static_cast<uint64_t>(ix))
            return get_be(r, 54, 8);
        printf("  [i]    GET_STREAM_INFO(STREAM_OUTPUT %d) answered status %d, command %04llx, "
               "descriptor %04llx:%llu, %zu bytes\n", ix, r[16] >> 3,
               static_cast<unsigned long long>(get_be(r, 36, 2)),
               static_cast<unsigned long long>(r.size() >= 40 ? get_be(r, 38, 2) : 0),
               static_cast<unsigned long long>(r.size() >= 42 ? get_be(r, 40, 2) : 0), r.size());
        run_until(cyc + ms(20));
    }
    printf("  [i]    GET_STREAM_INFO(STREAM_OUTPUT %d): no SUCCESS answer in 20 tries "
           "(%zu AECP responses seen)\n", ix, aecp_seen);
    return ~0ull;
}

//! AAF talker t's PDUs go to block base + t and the CRF output's to base + its
//! uid (KL_pp_maap_shim; milan_datapath acmp_src_dmac_w), so a PDU's source
//! is named by its address, not by the stream_id under test.
int SidMoveHarness::source_of_da(uint64_t da, uint64_t base) const {
    if (da < base || da >= base + static_cast<uint64_t>(kSources)) return -1;
    return static_cast<int>(da - base);
}

//! Each streamed source: PROBE_TX, src_stream_id_o, GET_STREAM_INFO selector
//! 2, the Talker Advertise and every PDU sent to its address since `from`
//! name one stream_id.
void SidMoveHarness::grade_agreement(const char* phase, uint64_t base, uint64_t from) {
    for (const int s : graded) {
        char w[160];
        printf("  -- source uid %d (%s)%s\n", s, s == kUidCrf ? "CRF Media Clock Output" : "AAF",
               s == kNamed ? ", its TCTX uid named" : "");
        const uint64_t pub = published(s);
        snprintf(w, sizeof w, "%s: PROBE_TX answers SUCCESS", phase);
        ck(w, static_cast<uint64_t>(peer[s].status), 0);
        snprintf(w, sizeof w, "%s: PROBE_TX's stream_id is src_stream_id_o", phase);
        ck(w, peer[s].answered_sid, pub);
        snprintf(w, sizeof w, "%s: PROBE_TX's stream_dest_mac is the block address", phase);
        ck(w, peer[s].answered_da, base + static_cast<uint64_t>(s));
        snprintf(w, sizeof w, "%s: GET_STREAM_INFO selector 2 is src_stream_id_o", phase);
        ck(w, gsi_stream_id(s), pub);
        snprintf(w, sizeof w, "%s: the Talker Advertise declares src_stream_id_o", phase);
        ck_true(w, ta.count(pub) != 0 && ta[pub].first_join != kNever);
        long n = 0;
        long other = 0;
        uint64_t odd = 0;
        for (const StreamPdu& p : pdus) {
            if (p.cyc < from || source_of_da(p.da, base) != s) continue;
            if (p.subtype != (s == kUidCrf ? 0x04 : 0x02)) continue;
            n++;
            if (p.sid != pub) { other++; odd = p.sid; }
        }
        snprintf(w, sizeof w, "%s: the source's stream PDUs are on the wire (%ld)", phase, n);
        ck_true(w, n >= 3);
        snprintf(w, sizeof w, "%s: every one carries src_stream_id_o (else %016llx)", phase,
                 static_cast<unsigned long long>(odd));
        ck(w, static_cast<uint64_t>(other), 0);
    }
}

// ============================================================================
//  boot: identity, the firmware boot values, the named talker's TCTX uid
// ============================================================================
void SidMoveHarness::boot() {
    printf("[BOOT] identity, the firmware boot values, the named talker's TCTX uid\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4Eu);
    ck("ADP_TALKER[15:0] talker_stream_sources is this leg's source count",
       axi_read(A_ADP_TALKER) & 0xFFFFu, kSources);
    axi_write(A_MAC_ALO, kStaMacLo);
    axi_write(A_MAC_AHI, kStaMacHi);
    axi_write(A_ADP_EIDLO, static_cast<uint32_t>(kTestEid & 0xFFFFFFFFu));
    axi_write(A_ADP_EIDHI, static_cast<uint32_t>(kTestEid >> 32));
    axi_write(A_AAF_CTRL, 0x00020001u);    // AAF talker 0 on, bypass CLEAR, VID 2
    if (kNamed > 0) {
        // the talker's TCTX record through the P11 window: w0 {en, chans 8},
        // and w2 {UID, DMAC_HI 0}, a non-zero uid naming the derived one
        axi_write(A_STRM_SEL, (1u << 8) | static_cast<uint32_t>(kNamed));
        axi_write(A_STRMW_CTRL, 1u | (8u << 1));
        axi_write(A_STRMW_DMAC_HI, static_cast<uint32_t>(kNamed) << 16);
    }
    axi_write(A_LWSRP_CTRL, 0x13u);        // SRP policing: engine + talker on
    axi_write(A_MAAP_CTRL, (static_cast<uint32_t>(kSources) << 8) | 1u);
    axi_write(A_CRFT_CTRL, 0x3u);          // CRF output on, class A
    axi_write(A_PP_CTRL, 0x1u);            // entity enable
    std::string why;
    const bool img = load_the_image(&why);
    if (!img) printf("  [i]    %s\n", why.c_str());
    ck("[BOOT] the shape's AEM image was generated and is served", img ? 1u : 0u, 1);
    start_the_restore_walk();
    rx_q.push_back(msrp_frame(domain_msg()));
    run_until(cyc + ms(20));
    ck("KL_maap is probing, no block claimed yet", axi_read(A_MAAP_STAT1) & 7u, 1);
}

//! the named talker's TCTX uid as the framer holds it (read at its CFG fetch)
uint64_t SidMoveHarness::named_uid() const {
    return dut->rootp->milan_datapath__DOT__aaf_packetizer__DOT__euid_r;
}

// ============================================================================
//  bind: the graded sources bind and stream under their configured IDs
// ============================================================================
void SidMoveHarness::phase_a() {
    printf("[A] the listener probes, MAAP grants, the switch declares Listener Ready "
           "for the answered ID, and each source streams\n");
    const uint64_t t0 = cyc;
    for (const int s : graded) {
        peer[s].want = true;
        probe(s);
    }
    run_until(t0 + ms(8000));
    const uint64_t base = block_base();
    ck("KL_maap reached ANNOUNCE (a block of one address per source)",
       (axi_read(A_MAAP_STAT1) >> 2) & 1u, 1);
    for (const int s : graded) {
        char w[96];
        snprintf(w, sizeof w, "[A] src_stream_id_o[%d] is the configured {MAC, uid}", s);
        ck(w, published(s), (kStaMac << 16) | static_cast<uint64_t>(s));
    }
    if (kNamed > 0) ck("[A] the named talker's TCTX uid is held by the framer",
                       named_uid(), static_cast<uint64_t>(kNamed));
    // the CRF grid runs off clk_audio, uncompressed, so its PDUs are sparse on
    // this grid: grade every PDU from half a second after the last binding
    uint64_t from = t0;
    for (const int s : graded)
        if (peer[s].answered_at != kNever && peer[s].answered_at > from) from = peer[s].answered_at;
    grade_agreement("[A]", base, from + ms(500));
}

// ============================================================================
//  move: a peer takes the block; every declaring source moves
// ============================================================================
void SidMoveHarness::phase_move() {
    printf("[MOVE] a peer ANNOUNCEs the claimed block from a lower MAC: KL_maap "
           "re-addresses, each declaring source withdraws and moves\n");
    const uint64_t base1 = block_base();
    uint64_t old_sid[kSources] = {};
    for (const int s : graded) old_sid[s] = published(s);
    // the listener's periodic probes keep T-SRP-DAFRESH alive across the walk
    for (const int s : graded) probe(s);
    run_until(cyc + ms(200));
    const uint64_t tc = cyc;
    rx_q.push_back(maap_announce(kPeerMac, static_cast<uint16_t>(base1 & 0xFFFFu),
                                 static_cast<uint16_t>(kSources)));
    run_until(tc + ms(9000));
    const uint64_t base2 = block_base();
    ck_true("KL_maap claimed another block", base2 != base1);
    ck("KL_maap is in ANNOUNCE again", (axi_read(A_MAAP_STAT1) >> 2) & 1u, 1);
    printf("[AFTER] each source's new Stream ID, everywhere it is named\n");
    bool distinct = true;
    for (size_t a = 0; a < graded.size(); a++)
        for (size_t b = a + 1; b < graded.size(); b++)
            if (published(graded[a]) == published(graded[b])) distinct = false;
    for (const int s : graded) {
        char w[160];
        const uint64_t pub = published(s);
        printf("  -- source uid %d: %016llx -> %016llx\n", s,
               static_cast<unsigned long long>(old_sid[s]), static_cast<unsigned long long>(pub));
        ck_true("[AFTER] the source moved to a new Stream ID", pub != old_sid[s]);
        ck("[AFTER] the new ID keeps the upper 48 bits", pub >> 16, old_sid[s] >> 16);
        const TaSeen& was = ta[old_sid[s]];
        ck_true("[AFTER] the withdrawn ID's Talker Advertise left after the conflict",
                was.last_leave != kNever && was.last_leave > tc);
        const uint64_t joined = ta.count(pub) ? ta[pub].first_join : kNever;
        snprintf(w, sizeof w, "[AFTER] conflict to the new ID's declaration under 2 s (%.0f ms)",
                 joined == kNever ? -1.0 : t_ms(joined - tc));
        ck_true(w, joined != kNever && joined > tc && joined - tc < ms(2000));
        long late = 0;
        for (const StreamPdu& p : pdus)
            if (p.sid == old_sid[s] && was.last_leave != kNever && p.cyc > was.last_leave + ms(50))
                late++;
        snprintf(w, sizeof w, "[AFTER] no PDU carries the withdrawn ID 50 ms after its Leave (%ld)", late);
        ck(w, static_cast<uint64_t>(late), 0);
    }
    ck_true("[AFTER] the graded sources' current IDs are distinct", distinct);
    if (kNamed > 0) ck("[AFTER] the named talker's TCTX uid is still held, unchanged",
                       named_uid(), static_cast<uint64_t>(kNamed));
    uint64_t from = tc;
    for (const int s : graded)
        if (peer[s].answered_at != kNever && peer[s].answered_at > from) from = peer[s].answered_at;
    grade_agreement("[AFTER]", base2, from + ms(500));
}

int SidMoveHarness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();
    for (int s = 0; s < kSources; s++)
        if ((kGraded >> s) & 1u) graded.push_back(s);
    printf("=== processor #202 Stream ID move, %d talker sources (graded mask 0x%x), "
           "1 ms = %llu cycles ===\n", kSources, kGraded, static_cast<unsigned long long>(kMsCyc));
    do_reset();
    boot();
    phase_a();
    phase_move();
    printf("[INV] over the whole run\n");
    ck("no malformed DUT MRPDU", static_cast<uint64_t>(dut_malformed), 0);
    printf("--------------------------------------------------------------\n");
    printf("simulated %.2f ms (%llu cycles)\n", t_ms(cyc), static_cast<unsigned long long>(cyc));
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    SidMoveHarness harness;
    return harness.run();
}
