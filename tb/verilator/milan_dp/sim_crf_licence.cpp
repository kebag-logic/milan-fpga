// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// obj_crflic: issue #530 on the flashed shape, at compressed time.
//
// The #117 Run B silicon run bound a reference listener to the DUT's CRF
// Stream Output through the bench AVB switch and recorded two defects:
//
//   1. THE BOUND TALKER ENDED ITS OWN BURSTS. The switch scopes a received
//      LeaveAll per attribute type (802.1Q-2014 10.7.5.20 NOTE). The DUT's
//      LeaveAll MRPDU flagged only its first message (the Domain), so the
//      switch never re-declared its Listener after it, and the processor
//      re-aged the Listener registration at every flagged VectorHeader of the
//      switch's own LeaveAll MRPDU. Once the 15 s PROBE_TX window had passed
//      (Milan v1.2 4.3.3.1) the DA gate closed, the DUT sent a Talker
//      Advertise Leave and stopped. The processor fixed both halves at pin
//      09f9bf38 (its issue 106).
//   2. EMISSION BEGAN BEFORE A RESERVATION EXISTED. The fabric licence read
//      the processor's raw admission verdict, which rises at DECLARE_TALKER,
//      instead of its ACTIVE (declaring Talker Advertise, a Listener Ready or
//      Ready Failed registered, admitted: Milan v1.2 5.3.7.3).
//
// This leg elaborates milan_datapath at endstation_ax7101_1x1_tdm8, where the
// CRF Media Clock Output is source uid 1, with the processor's millisecond and
// KL_maap's millisecond both compressed to MS_CYC_TB cycles (the pp_shadow
// recipe), and plays the two Run B peers:
//
//   * THE LISTENER probes a source, retries 4 s after a TALKER_DEST_MAC_FAIL
//     (3) answer and re-probes 0.5 s after the DUT's Talker Advertise Leave.
//   * THE SWITCH PORT declares Listener Ready 40 ms after the listener's
//     successful probe; re-declares, 2 ms after a DUT LeaveAll, only the
//     attribute types that LeaveAll flags; sends its own LeaveAll 9.99 s after
//     each DUT LeaveAll in the capture's layout (Listener JoinMt first, then
//     Domain, then LeaveAll-only Talker Advertise and Talker Failed vectors);
//     and withdraws its Listener 2 ms after a Talker Advertise Leave.
//
// Every level below is sampled on every cycle, so an edge between two CSR
// reads cannot be missed. Phases:
//   [BOOT] identity, the firmware boot values, the MAAP claim.
//   [A]    Run B's opening: the first probes are refused, MAAP grants, the DUT
//          declares Talker Advertise and is admitted, and no Listener Ready
//          exists yet. Nothing may be emitted (item 2).
//   [B]    the switch's first Listener Ready opens the licence on the cycle
//          ACTIVE rises, never before; the CRF PDUs are class A.
//   [B2]   the AAF closing edge: a withdrawn Listener closes the AAF gate on
//          the cycle ACTIVE falls, while the talker still declares.
//   [C]    item 1: 76 s bound across the Run B LeaveAll exchange, the probe
//          window long closed. No self-Leave, no licence drop.
//   [D]    a registered Asking Failed licenses nothing; Ready Failed does.
//   [E]    the unbind: the licence closes when the Listener registration
//          ends, not when the probe window does (the Run B last burst).
//   [F]    item 3: FRAMES_TX counts observation intervals, not PDUs, and
//          restarts at STREAM_START (Milan v1.2 5.3.7.7 Table 5.4).
//   [G]    #551: real admission refuses a re-declaration while a wire Listener
//          Ready lands inside the optimistic window. No licence, counter edge,
//          interval-counter reset or PDU. Both sources and round phases run.
//   [H]    the matching admitted cases stream; measure ACTIVE-to-licence delay.

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <functional>
#include <map>
#include <vector>

#ifndef MS_CYC_TB
#error "MS_CYC_TB must be the processor and KL_maap millisecond, in cycles"
#endif
#ifndef DIAG_TICK_MS_TB
#error "DIAG_TICK_MS_TB must be the Table 5.4 observation interval, in ms"
#endif

namespace {

constexpr uint64_t kMsCyc = MS_CYC_TB;
constexpr uint64_t kDiagTickMs = DIAG_TICK_MS_TB;
constexpr uint64_t kNever = ~0ull;

constexpr uint64_t ms(uint64_t n) { return n * kMsCyc; }

//! One level of the design, sampled every cycle: its edges and when they came.
struct Level {
    bool v = false;
    long rises = 0;
    long falls = 0;
    uint64_t first_rise = kNever;
    uint64_t last_rise = kNever;
    uint64_t last_fall = kNever;
    void sample(bool now, uint64_t cyc) {
        if (now && !v) {
            rises++;
            last_rise = cyc;
            if (first_rise == kNever) first_rise = cyc;
        }
        if (!now && v) {
            falls++;
            last_fall = cyc;
        }
        v = now;
    }
};

//! One VectorAttribute of a decoded MRPDU (802.1Q 10.8.1.2).
struct MrpVector {
    int leave_all = 0;
    int n = 0;
    std::vector<uint8_t> first_value;
    std::vector<int> events;       // ThreePackedEvents, one per value
    std::vector<int> declarations; // FourPackedEvents (Listener only)
};

struct MrpMessage {
    int type = 0;
    int attr_len = 0;
    std::vector<MrpVector> vectors;
};

//! A captured AVTP stream PDU.
struct StreamPdu {
    uint64_t cyc = 0;
    bool tagged = false;
    int pcp = -1;
    int vid = -1;
    uint64_t sid = 0;
    uint64_t da = 0;
};

//! One source's side of the two scripted peers, and what the DUT did to it.
struct Peer {
    bool listener_on = false;      // the listener wants the stream
    bool listener_bound = false;
    int probe_status = -1;         // last CONNECT_TX_RESPONSE status
    int first_status = -1;
    uint64_t last_probe = kNever;
    long probes = 0;
    int bridge_decl = 0;           // the switch's Listener declaration, 0 = none
    uint64_t first_ready = kNever;
    long dut_ta_leave = 0;
    uint64_t ta_on_wire = kNever;
};

class CrfLicenceHarness {
 public:
    int run();

 private:
    Vmilan_datapath* dut = nullptr;
    long checks = 0;
    long fails = 0;
    uint64_t cyc = 0;

    // ---- identities (wire order) -------------------------------------------
    static constexpr uint64_t kTestEid = 0x001BC50CAC000001ull;
    static constexpr uint32_t kStaMacLo = 0x00000002u;   // 02:00:00:00
    static constexpr uint32_t kStaMacHi = 0x00000100u;   // 00:01
    //! {station MAC, talker_unique_id}: what the processor declares and the
    //! Run B capture carried for the CRF output (uid 1)
    static constexpr uint64_t kSidBase = 0x0200000000010000ull;
    static constexpr int kUidAaf = 0;
    static constexpr int kUidCrf = 1;
    static constexpr int kSources = 2;
    static constexpr uint64_t kMaapPoolBase = 0x91E0F0000000ull;

    // ---- the CSR window ----------------------------------------------------
    static constexpr uint16_t A_ID = 0x000;
    static constexpr uint16_t A_MAC_ALO = 0x108;
    static constexpr uint16_t A_MAC_AHI = 0x10C;
    static constexpr uint16_t A_ADP_EIDLO = 0x604;
    static constexpr uint16_t A_ADP_EIDHI = 0x608;
    static constexpr uint16_t A_AAF_CTRL = 0x654;
    static constexpr uint16_t A_LWSRP_CTRL = 0x680;
    static constexpr uint16_t A_LWSRP_STATUS = 0x694;
    static constexpr uint16_t A_MAAP_CTRL = 0x6CC;
    static constexpr uint16_t A_MAAP_STAT0 = 0x6D0;
    static constexpr uint16_t A_MAAP_STAT1 = 0x6D4;
    static constexpr uint16_t A_CRFT_CTRL = 0x750;
    static constexpr uint16_t A_CRFT_COUNT = 0x764;
    static constexpr uint16_t A_PP_CTRL = 0x920;

    // ---- the per-cycle record ----------------------------------------------
    Level licence;                 // crft_emit_en_w
    Level active[kSources];        // the processor's ACTIVE
    Level admitted[kSources];      // the processor's raw sr_admitted
    Level declaring[kSources];     // the ACMP DA gate
    Level ta_declared[kSources];   // SRP Talker Advertise self-declared
    Level aaf_gate;                // aaf_stream_en_w[0]
    long licence_ne_active = 0;    // cycles CRF differs from ACTIVE AND real grant
    long aaf_without_active = 0;   // cycles AAF opens without ACTIVE AND real grant
    std::array<uint64_t, kSources> listener_event{kNever, kNever};
    bool corner_phase = false;

    // ---- the MAC ports -----------------------------------------------------
    std::deque<std::vector<uint8_t>> rx_q;
    size_t rx_beat = 0;
    int rx_gap = 0;
    std::vector<uint8_t> tx_cur;
    std::vector<StreamPdu> crf_pdus;
    std::vector<StreamPdu> aaf_pdus;

    // ---- the scripted peers -------------------------------------------------
    std::multimap<uint64_t, std::function<void()>> sched;
    Peer peer[kSources];                           // per source uid
    uint64_t bridge_la_gen = 0;
    long bridge_la = 0;
    long dut_la = 0;
    long dut_la_not_all_types = 0;
    int dut_la_last_mask = 0;
    long timeline_lines = 0;
    long dut_malformed = 0;
    uint64_t maap_off = 0;

    // ---- clocking ----------------------------------------------------------
    void lo();
    void hi();
    void step() { lo(); hi(); }
    void run_until(uint64_t t) { while (cyc < t) step(); }
    double t_ms(uint64_t c) const { return static_cast<double>(c) / static_cast<double>(kMsCyc); }

    void run_schedule();
    void rx_drive();
    void rx_edge();
    void observe();
    void sample_levels();
    void tx_frame_done();

    void axi_write(uint16_t a, uint32_t d);
    uint32_t axi_read(uint16_t a);
    void do_reset();

    // ---- frames ------------------------------------------------------------
    static void put_be(std::vector<uint8_t>& f, size_t off, uint64_t v, int n);
    static uint64_t get_be(const std::vector<uint8_t>& f, size_t off, int n);
    static std::vector<uint8_t> msrp_frame(const std::vector<uint8_t>& payload);
    std::vector<uint8_t> probe_tx(int uid);
    static std::vector<uint8_t> listener_msg(uint64_t sid, int la, int ev, int decl);
    static std::vector<uint8_t> domain_msg(int la, int ev);
    static std::vector<uint8_t> leave_all_only_msg(int type, int attr_len);
    std::vector<uint8_t> bridge_leave_all();
    static bool parse_mrpdu(const std::vector<uint8_t>& f, std::vector<MrpMessage>& out);
    void on_mrpdu(const std::vector<uint8_t>& f);
    void on_dut_leave_all(int mask);
    void on_dut_talker_event(int uid, int ev);
    void on_acmp(const std::vector<uint8_t>& f);
    void on_stream_pdu(const std::vector<uint8_t>& f, size_t avtp, bool tagged);

    // ---- the peers' actions ------------------------------------------------
    void at(uint64_t when, std::function<void()> fn) { sched.emplace(when, std::move(fn)); }
    void probe(int uid);
    void bridge_declare(int uid, int ev, int decl);
    void bridge_withdraw(int uid);
    void bridge_send_leave_all(uint64_t gen);
    void note(const char* what, int uid, long value);
    void note_edge(const char* what, const Level& was, bool now);

    // ---- grading -----------------------------------------------------------
    void ck(const char* what, uint64_t got, uint64_t exp);
    void ck_true(const char* what, bool cond);
    static uint64_t sid_of(int uid) { return kSidBase + static_cast<uint64_t>(uid); }
    long pdus_after(const std::vector<StreamPdu>& v, uint64_t from, uint64_t to) const;
    uint64_t max_gap(const std::vector<StreamPdu>& v, uint64_t from, uint64_t to) const;
    enum class Ctr { kStreamStart, kStreamStop, kFramesTx };
    uint32_t diag(Ctr which, int idx) const;
    unsigned lstn_reg(int uid) const;

    void boot();
    uint64_t phase_a();
    void phase_b(uint64_t t0);
    void phase_b2(uint64_t t0);
    void phase_c(uint64_t t0);
    void phase_d();
    void phase_e();
    void phase_f_after_c(uint64_t t_start);
    void phase_f_after_d(uint64_t t_restart);
    void grade_invariants();
    void stage_declaration(int uid, uint16_t max_frame, bool open);
    uint64_t listener_decode_delay(int uid);
    void phase_real_grant();
    void grant_case(int uid, bool refuse, unsigned round_phase, uint64_t decode_delay);
};

// ============================================================================
//  clocking: the peers act first, then the inputs settle, then the model
// ============================================================================
void CrfLicenceHarness::lo() {
    run_schedule();
    rx_drive();
    dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0;
    dut->eval();
    observe();
    rx_edge();
}

void CrfLicenceHarness::hi() {
    dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1;
    dut->eval();
    cyc++;
}

void CrfLicenceHarness::run_schedule() {
    while (!sched.empty() && sched.begin()->first <= cyc) {
        const std::function<void()> fn = sched.begin()->second;
        sched.erase(sched.begin());
        fn();
    }
}

//! Frames are fed LITTLE-LANE (tdata[7:0] = first wire byte), the RX tap's
//! convention (tb/verilator/pp_shadow states why), with a short gap between.
void CrfLicenceHarness::rx_drive() {
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

void CrfLicenceHarness::rx_edge() {
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

void CrfLicenceHarness::observe() {
    sample_levels();
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

void CrfLicenceHarness::sample_levels() {
    const auto* rp = dut->rootp;
    const unsigned act = rp->milan_datapath__DOT__pp_cd_srp_active_w;
    const unsigned adm = rp->milan_datapath__DOT__pp_cd_srp_sr_admitted_w;
    const unsigned dcl = rp->milan_datapath__DOT__pp_cd_acmp_declaring_w;
    const unsigned tks = rp->milan_datapath__DOT__pp_cd_srp_tk_decl_state_w;
    for (int s = 0; s < kSources; s++) {
        if (s != kUidCrf) active[s].sample((act >> s) & 1u, cyc);
        admitted[s].sample((adm >> s) & 1u, cyc);
        declaring[s].sample((dcl >> s) & 1u, cyc);
        ta_declared[s].sample(((tks >> (2 * s)) & 3u) == 1u, cyc);
    }
    const bool lic = rp->milan_datapath__DOT__crft_emit_en_w & 1u;
    note_edge("CRF licence", licence, lic);
    licence.sample(lic, cyc);
    const bool crf_active = (act >> kUidCrf) & 1u;
    note_edge("ACTIVE", active[kUidCrf], crf_active);
    active[kUidCrf].sample(crf_active, cyc);
    aaf_gate.sample(rp->milan_datapath__DOT__aaf_stream_en_w & 1u, cyc);
    if (lic != (active[kUidCrf].v && admitted[kUidCrf].v)) licence_ne_active++;
    if (aaf_gate.v && !(active[kUidAaf].v && admitted[kUidAaf].v)) aaf_without_active++;
    if (rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_valid_w
        && rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w == 3) {
        for (int s = 0; s < kSources; s++) {
            if (rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_stream_id_w == sid_of(s))
                listener_event[s] = cyc;
        }
    }
}

//! The CRF output's edges go into the timeline, so a run reads like the Run B
//! wire timeline it is compared against.
void CrfLicenceHarness::note_edge(const char* what, const Level& was, bool now) {
    if (now == was.v) return;
    char line[64];
    snprintf(line, sizeof line, "%s %s", what, now ? "RISES" : "FALLS");
    note(line, kUidCrf, -1);
}

// ============================================================================
//  the AXI4-Lite BFM (the milan_dp / pp_shadow protocol and timing)
// ============================================================================
void CrfLicenceHarness::axi_write(uint16_t a, uint32_t d) {
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

uint32_t CrfLicenceHarness::axi_read(uint16_t a) {
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

void CrfLicenceHarness::do_reset() {
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
void CrfLicenceHarness::put_be(std::vector<uint8_t>& f, size_t off, uint64_t v, int n) {
    for (int i = 0; i < n; i++)
        f[off + static_cast<size_t>(i)] = static_cast<uint8_t>(v >> (8 * (n - 1 - i)));
}

uint64_t CrfLicenceHarness::get_be(const std::vector<uint8_t>& f, size_t off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | f[off + static_cast<size_t>(i)];
    return v;
}

//! An MRPDU from the switch port to the Nearest Bridge group, EtherType MSRP:
//! ProtocolVersion 0, the messages, the list EndMark, padded to 60 octets.
std::vector<uint8_t> CrfLicenceHarness::msrp_frame(const std::vector<uint8_t>& payload) {
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

//! Milan PROBE_TX = IEEE 1722.1 CONNECT_TX_COMMAND aimed at our source `uid`
//! (pp_shadow's builder: talker_entity_id at @20 and talker_unique_id at @36
//! are the two fields the talker discriminates on).
std::vector<uint8_t> CrfLicenceHarness::probe_tx(int uid) {
    std::vector<uint8_t> f(70, 0);
    put_be(f, 0, 0x91E0F0010000ull, 6);
    put_be(f, 6, 0x021122334455ull, 6);
    put_be(f, 12, 0x22F0, 2);
    f[14] = 0xFC;                                  // ACMP
    f[15] = 0x00;                                  // CONNECT_TX_COMMAND
    f[17] = 44;                                    // control_data_length
    put_be(f, 18, kTestEid, 8);                    // @4  stream_id
    put_be(f, 26, 0xC0FFEE00DEADBEEFull, 8);       // @12 controller_entity_id
    put_be(f, 34, kTestEid, 8);                    // @20 talker_entity_id
    put_be(f, 42, 0x2222222222222222ull, 8);       // @28 listener_entity_id
    put_be(f, 50, static_cast<uint64_t>(uid), 2);  // @36 talker_unique_id
    put_be(f, 62, static_cast<uint64_t>(peer[uid].probes + 1), 2);   // @48 sequence_id
    return f;
}

//! One Listener message, one value: 802.1Q 35.2.2.7 with event `ev`
//! (0 New, 1 JoinIn, 3 JoinMt, 5 Lv) and declaration `decl` (1 Asking
//! Failed, 2 Ready, 3 Ready Failed). `la` sets the VectorHeader LeaveAllEvent.
std::vector<uint8_t> CrfLicenceHarness::listener_msg(uint64_t sid, int la, int ev, int decl) {
    std::vector<uint8_t> m(18, 0);
    m[0] = 3;
    m[1] = 8;
    put_be(m, 2, 14, 2);                           // 2 + 8 + 1 + 1 + EndMark
    put_be(m, 4, (static_cast<uint64_t>(la) << 13) | 1u, 2);
    put_be(m, 6, sid, 8);
    m[14] = static_cast<uint8_t>(ev * 36);
    m[15] = static_cast<uint8_t>(decl << 6);
    return m;                                      // m[16..17]: the EndMark
}

//! The switch's Domain message as Run B carries it: NumberOfValues 2 from
//! FirstValue {SRclassID 5, priority 2, VID 2}, so class A {6, 3, 2} is value 1.
std::vector<uint8_t> CrfLicenceHarness::domain_msg(int la, int ev) {
    std::vector<uint8_t> m(13, 0);
    m[0] = 4;
    m[1] = 4;
    put_be(m, 2, 9, 2);
    put_be(m, 4, (static_cast<uint64_t>(la) << 13) | 2u, 2);
    m[6] = 5; m[7] = 2; put_be(m, 8, 2, 2);
    m[10] = static_cast<uint8_t>(ev * 36 + ev * 6);
    return m;                                      // m[11..12]: the EndMark
}

//! A LeaveAll-only VectorAttribute: NumberOfValues 0 and a zero FirstValue of
//! the full AttributeLength (802.1Q-2014 10.8.2.8 f), the switch's own bytes.
std::vector<uint8_t> CrfLicenceHarness::leave_all_only_msg(int type, int attr_len) {
    std::vector<uint8_t> m(static_cast<size_t>(4 + 2 + attr_len + 2), 0);
    m[0] = static_cast<uint8_t>(type);
    m[1] = static_cast<uint8_t>(attr_len);
    put_be(m, 2, static_cast<uint64_t>(attr_len + 4), 2);
    put_be(m, 4, 1u << 13, 2);
    return m;
}

//! The switch's own LeaveAll MRPDU in the Run B layout (switch port,
//! 47.029619 s): LeaveAllEvent in every message, Listener first carrying its
//! JoinMt re-declaration, then Domain, then the two Talker types it declares
//! nothing of. Where it declares no Listener, the Listener message is
//! LeaveAll-only too.
std::vector<uint8_t> CrfLicenceHarness::bridge_leave_all() {
    std::vector<uint8_t> p;
    int declared = -1;
    for (int s = 0; s < kSources; s++)
        if (peer[s].bridge_decl != 0 && declared < 0) declared = s;
    const std::vector<uint8_t> lm = (declared >= 0)
        ? listener_msg(sid_of(declared), 1, 3, peer[declared].bridge_decl)
        : leave_all_only_msg(3, 8);
    p.insert(p.end(), lm.begin(), lm.end());
    const std::vector<uint8_t> dm = domain_msg(1, 3);
    p.insert(p.end(), dm.begin(), dm.end());
    const std::vector<uint8_t> ta = leave_all_only_msg(1, 25);
    p.insert(p.end(), ta.begin(), ta.end());
    const std::vector<uint8_t> tf = leave_all_only_msg(2, 34);
    p.insert(p.end(), tf.begin(), tf.end());
    return msrp_frame(p);
}

//! Decode an untagged MRPDU (802.1Q 10.8.1.2): every message, every vector.
//! Returns false on a malformed walk, which the caller counts.
bool CrfLicenceHarness::parse_mrpdu(const std::vector<uint8_t>& f, std::vector<MrpMessage>& out) {
    size_t off = 15;                               // after ProtocolVersion
    while (off + 2 <= f.size() && !(f[off] == 0 && f[off + 1] == 0)) {
        if (off + 4 > f.size()) return false;
        MrpMessage m;
        m.type = f[off];
        m.attr_len = f[off + 1];
        size_t p = off + 4;
        const size_t end = p + get_be(f, off + 2, 2);
        if (end > f.size()) return false;
        while (p + 2 <= end && !(f[p] == 0 && f[p + 1] == 0)) {
            MrpVector v;
            const uint64_t vh = get_be(f, p, 2);
            v.leave_all = static_cast<int>(vh >> 13);
            v.n = static_cast<int>(vh & 0x1FFFu);
            p += 2;
            if (p + static_cast<size_t>(m.attr_len) > end) return false;
            v.first_value.assign(f.begin() + static_cast<long>(p),
                                 f.begin() + static_cast<long>(p) + m.attr_len);
            p += static_cast<size_t>(m.attr_len);
            for (int k = 0; k < (v.n + 2) / 3 && p < end; k++, p++) {
                const int b = f[p];
                v.events.push_back(b / 36);
                v.events.push_back((b / 6) % 6);
                v.events.push_back(b % 6);
            }
            for (int k = 0; m.type == 3 && k < (v.n + 3) / 4 && p < end; k++, p++)
                for (int sh = 6; sh >= 0; sh -= 2) v.declarations.push_back((f[p] >> sh) & 3);
            m.vectors.push_back(v);
        }
        out.push_back(m);
        off = end;
    }
    return true;
}

// ============================================================================
//  what the DUT sends, and how the peers answer it
// ============================================================================
void CrfLicenceHarness::tx_frame_done() {
    const std::vector<uint8_t>& f = tx_cur;
    if (f.size() < 18) return;
    const uint64_t et = get_be(f, 12, 2);
    if (et == 0x22EA) {
        on_mrpdu(f);
    } else if (et == 0x8100 && f.size() >= 30 && get_be(f, 16, 2) == 0x22F0) {
        on_stream_pdu(f, 18, true);
    } else if (et == 0x22F0 && f[14] == 0xFC) {
        on_acmp(f);
    } else if (et == 0x22F0 && f.size() >= 26) {
        on_stream_pdu(f, 14, false);
    }
}

void CrfLicenceHarness::on_stream_pdu(const std::vector<uint8_t>& f, size_t avtp, bool tagged) {
    const int subtype = f[avtp];
    if (subtype != 0x04 && subtype != 0x02) return;   // CRF, AAF
    StreamPdu p;
    p.cyc = cyc;
    p.tagged = tagged;
    if (tagged) {
        p.pcp = f[14] >> 5;
        p.vid = static_cast<int>(get_be(f, 14, 2) & 0xFFFu);
    }
    p.sid = get_be(f, avtp + 4, 8);
    p.da = get_be(f, 0, 6);
    std::vector<StreamPdu>& v = (subtype == 0x04) ? crf_pdus : aaf_pdus;
    if (v.empty()) note(subtype == 0x04 ? "first CRF PDU on the wire" : "first AAF PDU on the wire", -1, -1);
    v.push_back(p);
}

//! CONNECT_TX_RESPONSE (message_type 1): status at wire byte 16 [7:3],
//! talker_unique_id at @36 (wire 50..51).
void CrfLicenceHarness::on_acmp(const std::vector<uint8_t>& f) {
    if ((f[15] & 0x0F) != 1 || f.size() < 70) return;
    const int status = f[16] >> 3;
    const uint64_t uid64 = get_be(f, 50, 2);
    if (uid64 >= kSources) return;
    const int uid = static_cast<int>(uid64);
    peer[uid].probe_status = status;
    if (peer[uid].first_status < 0) peer[uid].first_status = status;
    note("PROBE_TX answered, status", uid, status);
    if (!peer[uid].listener_on) return;
    if (status == 0 && !peer[uid].listener_bound) {
        peer[uid].listener_bound = true;
        at(cyc + ms(40), [this, uid] { if (peer[uid].listener_on) bridge_declare(uid, 0, 2); });
    } else if (status == 3) {
        at(cyc + ms(4000), [this, uid] { if (peer[uid].listener_on) probe(uid); });
    }
}

void CrfLicenceHarness::on_mrpdu(const std::vector<uint8_t>& f) {
    std::vector<MrpMessage> msgs;
    if (!parse_mrpdu(f, msgs)) {
        dut_malformed++;
        note("MALFORMED DUT MRPDU", -1, -1);
        return;
    }
    int mask = 0;
    for (const MrpMessage& m : msgs) {
        for (const MrpVector& v : m.vectors) {
            if (v.leave_all == 1 && m.type >= 1 && m.type <= 4) mask |= 1 << (m.type - 1);
            if (m.type != 1 || v.first_value.size() < 8) continue;
            const uint64_t sid0 = get_be(v.first_value, 0, 8);
            for (int k = 0; k < v.n && k < static_cast<int>(v.events.size()); k++) {
                const uint64_t sid = sid0 + static_cast<uint64_t>(k);   // 802.1Q 35.2.2.8.x +k
                if (sid >= kSidBase && sid < kSidBase + kSources)
                    on_dut_talker_event(static_cast<int>(sid - kSidBase), v.events[static_cast<size_t>(k)]);
            }
        }
    }
    if (mask != 0) on_dut_leave_all(mask);
}

//! The switch scopes a received LeaveAll per attribute type (Run B: 9 of 9
//! DUT LeaveAlls re-declared the Domain, none re-declared the Listener while
//! only the Domain was flagged), and restarts its own leavealltimer on it.
void CrfLicenceHarness::on_dut_leave_all(int mask) {
    dut_la++;
    if (corner_phase) return;
    dut_la_last_mask = mask;
    if (mask != 0xF) dut_la_not_all_types++;
    note("DUT LeaveAll MRPDU, flagged-type mask (bit n = AttributeType n+1)", -1, mask);
    if (mask & 0x4) {
        for (int s = 0; s < kSources; s++)
            if (peer[s].bridge_decl != 0)
                at(cyc + ms(2), [this, s] { if (peer[s].bridge_decl != 0) bridge_declare(s, 1, peer[s].bridge_decl); });
    }
    if (mask & 0x8) at(cyc + ms(1), [this] { rx_q.push_back(msrp_frame(domain_msg(0, 1))); });
    const uint64_t gen = ++bridge_la_gen;
    at(cyc + ms(9990), [this, gen] { bridge_send_leave_all(gen); });
}

void CrfLicenceHarness::on_dut_talker_event(int uid, int ev) {
    if (corner_phase) return;
    if (ev == 5) {
        peer[uid].dut_ta_leave++;
        note("DUT Talker Advertise LEAVE", uid, -1);
        if (peer[uid].bridge_decl != 0) at(cyc + ms(2), [this, uid] { bridge_withdraw(uid); });
        if (peer[uid].listener_on) {
            peer[uid].listener_bound = false;
            at(cyc + ms(500), [this, uid] { if (peer[uid].listener_on) probe(uid); });
        }
    } else if ((ev == 0 || ev == 1 || ev == 3) && peer[uid].ta_on_wire == kNever) {
        peer[uid].ta_on_wire = cyc;
        note("DUT Talker Advertise first on the wire", uid, ev);
    }
}

void CrfLicenceHarness::probe(int uid) {
    rx_q.push_back(probe_tx(uid));
    peer[uid].probes++;
    peer[uid].last_probe = cyc;
    note("listener PROBE_TX", uid, peer[uid].probes);
}

void CrfLicenceHarness::bridge_declare(int uid, int ev, int decl) {
    peer[uid].bridge_decl = decl;
    rx_q.push_back(msrp_frame(listener_msg(sid_of(uid), 0, ev, decl)));
    if ((decl == 2 || decl == 3) && peer[uid].first_ready == kNever) {
        peer[uid].first_ready = cyc;
        note("switch declares the FIRST Listener Ready", uid, -1);
    }
}

void CrfLicenceHarness::bridge_withdraw(int uid) {
    const int decl = (peer[uid].bridge_decl != 0) ? peer[uid].bridge_decl : 2;
    rx_q.push_back(msrp_frame(listener_msg(sid_of(uid), 0, 5, decl)));
    peer[uid].bridge_decl = 0;
    note("switch withdraws its Listener (Lv)", uid, -1);
}

void CrfLicenceHarness::bridge_send_leave_all(uint64_t gen) {
    if (gen != bridge_la_gen) return;              // restarted by a later DUT LeaveAll
    bridge_la++;
    rx_q.push_back(bridge_leave_all());
    note("switch LeaveAll MRPDU (Run B layout)", -1, bridge_la);
}

void CrfLicenceHarness::note(const char* what, int uid, long value) {
    if (timeline_lines >= 400) return;
    timeline_lines++;
    printf("  [t] %11.2f ms  %s", t_ms(cyc), what);
    if (uid >= 0) printf(", uid %d", uid);
    if (value >= 0) printf(" (%ld)", value);
    printf("\n");
}

// ============================================================================
//  grading
// ============================================================================
void CrfLicenceHarness::ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    const bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-66s got=%llu exp=%llu\n", ok ? "PASS" : "FAIL", what,
           static_cast<unsigned long long>(got), static_cast<unsigned long long>(exp));
}

void CrfLicenceHarness::ck_true(const char* what, bool cond) {
    checks++;
    if (!cond) fails++;
    printf("  [%s] %s\n", cond ? "PASS" : "FAIL", what);
}

long CrfLicenceHarness::pdus_after(const std::vector<StreamPdu>& v, uint64_t from, uint64_t to) const {
    long n = 0;
    for (const StreamPdu& p : v)
        if (p.cyc > from && p.cyc <= to) n++;
    return n;
}

uint64_t CrfLicenceHarness::max_gap(const std::vector<StreamPdu>& v, uint64_t from, uint64_t to) const {
    uint64_t prev = kNever;
    uint64_t gap = 0;
    for (const StreamPdu& p : v) {
        if (p.cyc < from || p.cyc > to) continue;
        if (prev != kNever && p.cyc - prev > gap) gap = p.cyc - prev;
        prev = p.cyc;
    }
    return gap;
}

//! Milan Table 5.4 counters of Stream Output `idx`, read where they are kept.
uint32_t CrfLicenceHarness::diag(Ctr which, int idx) const {
    const auto* rp = dut->rootp;
    switch (which) {
        case Ctr::kStreamStart: return rp->milan_datapath__DOT__talker_diag__DOT__start_r[idx];
        case Ctr::kStreamStop:  return rp->milan_datapath__DOT__talker_diag__DOT__stop_r[idx];
        case Ctr::kFramesTx:    return rp->milan_datapath__DOT__talker_diag__DOT__ftx_r[idx];
    }
    return 0;
}

unsigned CrfLicenceHarness::lstn_reg(int uid) const {
    return (dut->rootp->milan_datapath__DOT__pp_cd_srp_lstn_reg_state_w >> (2 * uid)) & 3u;
}

// ============================================================================
//  [BOOT] the identity and the firmware boot values of the #117 image
// ============================================================================
void CrfLicenceHarness::boot() {
    printf("[BOOT] identity, the firmware boot values, the MAAP claim\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4Eu);
    axi_write(A_MAC_ALO, kStaMacLo);
    axi_write(A_MAC_AHI, kStaMacHi);
    axi_write(A_ADP_EIDLO, static_cast<uint32_t>(kTestEid & 0xFFFFFFFFu));
    axi_write(A_ADP_EIDHI, static_cast<uint32_t>(kTestEid >> 32));
    axi_write(A_AAF_CTRL, 0x00020001u);    // AAF talker on, bypass CLEAR, VID 2
    axi_write(A_LWSRP_CTRL, 0x13u);        // SRP policing: engine + talker on
    axi_write(A_MAAP_CTRL, 0x201u);        // MAAP on, two addresses
    axi_write(A_CRFT_CTRL, 0x3u);          // CRF output on, class A
    axi_write(A_PP_CTRL, 0x1u);            // entity enable
    rx_q.push_back(msrp_frame(domain_msg(0, 1)));   // the switch's Domain
    bool announced = false;
    for (int r = 0; r < 400 && !announced; r++) {
        run_until(cyc + ms(20));
        announced = ((axi_read(A_MAAP_STAT1) >> 2) & 1u) != 0;
    }
    ck_true("KL_maap reached ANNOUNCE (a block of two is claimed)", announced);
    maap_off = axi_read(A_MAAP_STAT0) & 0xFFFFu;
    ck("CRFT_CTRL[1:0] reads back the boot value", axi_read(A_CRFT_CTRL) & 3u, 3);
    ck("nothing declares yet, so nothing is licensed", licence.rises, 0);
}

// ============================================================================
//  [A] item 2 reproduced: the Run B opening, with no Listener Ready anywhere
// ============================================================================
uint64_t CrfLicenceHarness::phase_a() {
    printf("[A] the Run B opening: probe refused, MAAP grant, Talker Advertise "
           "declared and admitted, NO Listener Ready - nothing may be emitted\n");
    const uint64_t t0 = cyc;
    peer[kUidCrf].listener_on = true;
    peer[kUidAaf].listener_on = true;
    probe(kUidCrf);
    probe(kUidAaf);
    run_until(t0 + ms(3900));
    for (int s = 0; s < kSources; s++) {
        printf("  -- source uid %d (%s)\n", s, s == kUidCrf ? "CRF Media Clock Output" : "AAF");
        ck("the first PROBE_TX is answered TALKER_DEST_MAC_FAIL (3)", static_cast<uint64_t>(peer[s].first_status), 3);
        ck_true("...and MAAP's grant opens the DA gate after it", declaring[s].first_rise != kNever);
        ck_true("the DUT declares Talker Advertise on the wire", peer[s].ta_on_wire != kNever);
        ck("the processor's RAW admission verdict is up (the pre-#530 gate)", admitted[s].v, 1);
        ck_true("...while no Listener Ready has been declared to the DUT", peer[s].first_ready == kNever);
        ck("ACTIVE never rose", static_cast<uint64_t>(active[s].rises), 0);
    }
    ck("the CRF licence never opened (every cycle sampled)", static_cast<uint64_t>(licence.rises), 0);
    ck("no CRF PDU on the wire", crf_pdus.size(), 0);
    ck("CRFT_COUNT stays 0", axi_read(A_CRFT_COUNT), 0);
    const uint32_t st = axi_read(A_CRFT_CTRL);
    ck("CRFT_CTRL[5] the output is tagged (its Talker Advertise stands)", (st >> 5) & 1u, 1);
    ck("CRFT_CTRL[6] reservation active reads 0", (st >> 6) & 1u, 0);
    ck("CRFT_CTRL[7] emission licensed reads 0", (st >> 7) & 1u, 0);
    ck("the AAF gate never opened", static_cast<uint64_t>(aaf_gate.rises), 0);
    ck("no AAF PDU on the wire", aaf_pdus.size(), 0);
    ck("LWSRP_STATUS[8] stream gate (source 0) reads 0", (axi_read(A_LWSRP_STATUS) >> 8) & 1u, 0);
    if (admitted[kUidCrf].first_rise != kNever)
        printf("  [i]    the raw verdict has stood %.2f ms: the window Run B streamed through\n",
               t_ms(cyc - admitted[kUidCrf].first_rise));
    return t0;
}

// ============================================================================
//  [B] the first Listener Ready: the licence opens with ACTIVE, not before
// ============================================================================
void CrfLicenceHarness::phase_b(uint64_t t0) {
    printf("[B] the listener's retry succeeds and the switch declares Listener Ready\n");
    run_until(t0 + ms(7000));
    for (int s = 0; s < kSources; s++) {
        printf("  -- source uid %d\n", s);
        ck("the retried PROBE_TX is answered SUCCESS", static_cast<uint64_t>(peer[s].probe_status), 0);
        ck_true("the switch's first Listener Ready reached the DUT", peer[s].first_ready != kNever);
        ck_true("ACTIVE rose after it, within 50 ms", active[s].first_rise != kNever
                && active[s].first_rise > peer[s].first_ready
                && active[s].first_rise - peer[s].first_ready <= ms(50));
    }
    ck("the CRF licence opened on the cycle ACTIVE[CRF] rose", licence.first_rise, active[kUidCrf].first_rise);
    ck("the AAF gate opened on the cycle ACTIVE[AAF] rose", aaf_gate.first_rise, active[kUidAaf].first_rise);
    ck_true("CRF PDUs follow the licence (>= 3 in 3 s)",
            !crf_pdus.empty() && crf_pdus.front().cyc > licence.first_rise && crf_pdus.size() >= 3);
    ck_true("AAF PDUs follow the AAF gate",
            !aaf_pdus.empty() && aaf_pdus.front().cyc > aaf_gate.first_rise);
    long class_a = 0;
    for (const StreamPdu& p : crf_pdus)
        if (p.tagged && p.pcp == 3 && p.vid == 2 && p.sid == sid_of(kUidCrf)
            && p.da == (kMaapPoolBase | ((maap_off + kUidCrf) & 0xFFFFu))) class_a++;
    ck("every CRF PDU: C-tag {PCP 3, VID 2}, stream {MAC, uid 1}, the MAAP DA",
       static_cast<uint64_t>(class_a), crf_pdus.size());
    const uint32_t st = axi_read(A_CRFT_CTRL);
    ck("CRFT_CTRL[6] reservation active reads 1", (st >> 6) & 1u, 1);
    ck("CRFT_CTRL[7] emission licensed reads 1", (st >> 7) & 1u, 1);
    ck("LWSRP_STATUS[8] stream gate (source 0) reads 1", (axi_read(A_LWSRP_STATUS) >> 8) & 1u, 1);
}

// ============================================================================
//  [B2] the AAF closing edge: the licence follows ACTIVE down, too
// ============================================================================
void CrfLicenceHarness::phase_b2(uint64_t t0) {
    printf("[B2] the AAF listener unbinds; the switch withdraws that Listener\n");
    peer[kUidAaf].listener_on = false;
    bridge_withdraw(kUidAaf);
    const uint64_t t_lv = cyc;
    run_until(t0 + ms(13500));
    ck_true("ACTIVE[AAF] fell on the Lv, within 50 ms (the registrar goes IN to MT on an rLv)",
            !active[kUidAaf].v && active[kUidAaf].last_fall > t_lv
            && active[kUidAaf].last_fall - t_lv <= ms(50));
    ck("the AAF gate closed on that cycle", aaf_gate.last_fall, active[kUidAaf].last_fall);
    ck("...while the AAF talker still declares Talker Advertise", ta_declared[kUidAaf].v, 1);
    ck("...and its raw verdict still stands (the pre-#530 gate stayed open)", admitted[kUidAaf].v, 1);
    ck("no AAF PDU 20 ms after the gate closed",
       static_cast<uint64_t>(pdus_after(aaf_pdus, aaf_gate.last_fall + ms(20), cyc)), 0);
    ck("the CRF output is untouched", licence.v, 1);
}

// ============================================================================
//  [C] item 1: a bound CRF talker across the Run B LeaveAll exchange
// ============================================================================
void CrfLicenceHarness::phase_c(uint64_t t0) {
    printf("[C] bound, the probe window long closed, across the Run B LeaveAll "
           "exchange: no self-Leave, no licence drop\n");
    const uint64_t t_bound = licence.first_rise;
    const long la0 = dut_la;
    const long bla0 = bridge_la;
    run_until(t0 + ms(80000));
    ck("the DUT sent no Talker Advertise Leave for its bound CRF output",
       static_cast<uint64_t>(peer[kUidCrf].dut_ta_leave), 0);
    ck("ACTIVE[CRF] never fell", static_cast<uint64_t>(active[kUidCrf].falls), 0);
    ck("the CRF licence never fell", static_cast<uint64_t>(licence.falls), 0);
    ck("the CRF DA gate never closed", static_cast<uint64_t>(declaring[kUidCrf].falls), 0);
    ck("the listener never had to re-probe (two probes in all)", static_cast<uint64_t>(peer[kUidCrf].probes), 2);
    ck_true("the registration alone held the DA gate for >= 45 s (probe window + 15 s closed)",
            peer[kUidCrf].last_probe + ms(15000) + ms(45000) <= cyc);
    printf("  [i]    %ld DUT and %ld switch LeaveAll MRPDUs in this phase\n", dut_la - la0, bridge_la - bla0);
    ck_true("the DUT sent >= 4 LeaveAll MRPDUs", dut_la - la0 >= 4);
    ck("every DUT LeaveAll flagged all four MSRP attribute types (802.1Q-2014 10.7.5.20)",
       static_cast<uint64_t>(dut_la_not_all_types), 0);
    ck_true("the switch sent >= 4 of its own, Listener JoinMt first", bridge_la - bla0 >= 4);
    ck("the Listener registration still reads Ready", lstn_reg(kUidCrf), 2);
    const long n = pdus_after(crf_pdus, t_bound, cyc);
    const uint64_t first = crf_pdus.empty() ? 0 : crf_pdus.front().cyc;
    const uint64_t last = crf_pdus.empty() ? 0 : crf_pdus.back().cyc;
    const uint64_t period = (n > 1) ? (last - first) / static_cast<uint64_t>(n - 1) : 0;
    const uint64_t gap = max_gap(crf_pdus, t_bound, cyc);
    printf("  [i]    %ld CRF PDUs, mean period %.2f ms, longest gap %.2f ms\n", n, t_ms(period), t_ms(gap));
    ck_true("the CRF stream never paused (longest gap <= 1.5 mean periods)",
            n > 10 && gap * 2 <= period * 3);
}

// ============================================================================
//  [F] item 3: FRAMES_TX counts observation intervals, not PDUs
// ============================================================================
void CrfLicenceHarness::phase_f_after_c(uint64_t t_start) {
    printf("[F] Stream Output 1's Milan v1.2 5.3.7.7 Table 5.4 counters "
           "(observation interval %llu ms here)\n", static_cast<unsigned long long>(kDiagTickMs));
    const uint64_t intervals = (cyc - t_start) / ms(kDiagTickMs);
    const uint32_t ftx = diag(Ctr::kFramesTx, kUidCrf);
    const long pdus = pdus_after(crf_pdus, t_start, cyc);
    printf("  [i]    %llu intervals since STREAM_START, FRAMES_TX %u, %ld PDUs\n",
           static_cast<unsigned long long>(intervals), ftx, pdus);
    ck("STREAM_START = 1: one start since the bind", diag(Ctr::kStreamStart, kUidCrf), 1);
    ck("STREAM_STOP = 0", diag(Ctr::kStreamStop, kUidCrf), 0);
    ck_true("FRAMES_TX = the intervals elapsed since STREAM_START (+-1)",
            ftx + 1 >= intervals && ftx <= intervals + 1);
    ck_true("...which is far fewer than the PDUs sent (>= 3 per interval here)",
            pdus >= 3 * static_cast<long>(ftx) && ftx > 0);
    ck("CRFT_COUNT (0x764) is the PDU total the wire carried",
       axi_read(A_CRFT_COUNT), crf_pdus.size());
}

void CrfLicenceHarness::phase_f_after_d(uint64_t t_restart) {
    printf("[F] ...and they restart at the next STREAM_START\n");
    const uint64_t intervals = (cyc - t_restart) / ms(kDiagTickMs);
    const uint32_t ftx = diag(Ctr::kFramesTx, kUidCrf);
    ck("STREAM_START = 2", diag(Ctr::kStreamStart, kUidCrf), 2);
    ck("STREAM_STOP = 1", diag(Ctr::kStreamStop, kUidCrf), 1);
    ck_true("FRAMES_TX restarted: it counts only the intervals since the restart (+1)",
            ftx <= intervals + 1);
}

// ============================================================================
//  [D] a registered Asking Failed licenses nothing; Ready Failed does
// ============================================================================
void CrfLicenceHarness::phase_d() {
    printf("[D] the Listener declaration changes: Asking Failed, then Ready Failed\n");
    probe(kUidCrf);                                // a fresh probe window: the DA gate stays open
    run_until(cyc + ms(500));
    bridge_declare(kUidCrf, 1, 1);
    const uint64_t t_af = cyc;
    run_until(t_af + ms(2000));
    ck("Asking Failed registered", lstn_reg(kUidCrf), 1);
    ck_true("ACTIVE fell within 50 ms of it",
            !active[kUidCrf].v && active[kUidCrf].last_fall >= t_af && active[kUidCrf].last_fall - t_af <= ms(50));
    ck("the licence closed on that cycle", licence.last_fall, active[kUidCrf].last_fall);
    ck("...while the talker still declares Talker Advertise", ta_declared[kUidCrf].v, 1);
    ck("...and its raw verdict still stands", admitted[kUidCrf].v, 1);
    ck("no CRF PDU 20 ms after the licence closed",
       static_cast<uint64_t>(pdus_after(crf_pdus, licence.last_fall + ms(20), cyc)), 0);
    bridge_declare(kUidCrf, 1, 3);
    const uint64_t t_rf = cyc;
    run_until(t_rf + ms(2500));
    ck("Ready Failed registered", lstn_reg(kUidCrf), 3);
    ck_true("ACTIVE rose after it", active[kUidCrf].v && active[kUidCrf].last_rise > t_rf);
    ck("the licence reopened on that cycle", licence.last_rise, active[kUidCrf].last_rise);
    ck_true("CRF PDUs resumed", pdus_after(crf_pdus, licence.last_rise, cyc) >= 2);
    phase_f_after_d(licence.last_rise);
}

// ============================================================================
//  [E] the unbind: the licence ends with the registration, not the window
// ============================================================================
void CrfLicenceHarness::phase_e() {
    printf("[E] the CRF listener unbinds inside a fresh probe window\n");
    peer[kUidCrf].listener_on = false;
    bridge_withdraw(kUidCrf);
    const uint64_t t_lv = cyc;
    run_until(t_lv + ms(7000));
    ck_true("the probe window is still open", peer[kUidCrf].last_probe + ms(15000) > cyc);
    ck_true("ACTIVE fell on the Lv, within 50 ms (the registrar goes IN to MT on an rLv)",
            !active[kUidCrf].v && active[kUidCrf].last_fall > t_lv
            && active[kUidCrf].last_fall - t_lv <= ms(50));
    ck("the licence closed on that cycle", licence.last_fall, active[kUidCrf].last_fall);
    ck("...while the talker still declares Talker Advertise", ta_declared[kUidCrf].v, 1);
    ck("...and its raw verdict still stands", admitted[kUidCrf].v, 1);
    ck("no CRF PDU 20 ms after the licence closed",
       static_cast<uint64_t>(pdus_after(crf_pdus, licence.last_fall + ms(20), cyc)), 0);
    const uint32_t st = axi_read(A_CRFT_CTRL);
    ck("CRFT_CTRL[6] reservation active reads 0", (st >> 6) & 1u, 0);
    ck("CRFT_CTRL[7] emission licensed reads 0", (st >> 7) & 1u, 0);
}

//! Verification-only service staging: the same captured tuple that a
//! DECLARE/WITHDRAW_TALKER request leaves in S_GATE. The next real clock
//! performs the declaration and updates the real TSpec admission engine.
//! No result, registrar, optimistic flag, or transmit gate is deposited.
void CrfLicenceHarness::stage_declaration(int uid, uint16_t max_frame, bool open) {
    auto* rp = dut->rootp;
    ck("SRP service is idle before staging", rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__svc_st_r, 0);
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r = static_cast<uint8_t>(uid);
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_sid_r = sid_of(uid);
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_da_r = kMaapPoolBase | ((maap_off + static_cast<uint64_t>(uid)) & 0xFFFFu);
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r = 2;
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mfs_r = max_frame;
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mif_r = 1;
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r = open;
    rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__svc_st_r = 1;
}

//! Measure the real MAC-to-decoder delay with an identical Listener frame.
//! The graded replay asserts this delay again; a changed schedule fails.
uint64_t CrfLicenceHarness::listener_decode_delay(int uid) {
    run_until(cyc + 4096);
    const uint64_t sent = cyc;
    rx_q.push_back(msrp_frame(listener_msg(sid_of(uid), 0, 1, 2)));
    run_until(sent + 4096);
    ck_true("calibration decoded a real Listener frame", listener_event[uid] > sent && listener_event[uid] < cyc);
    return listener_event[uid] - sent;
}

void CrfLicenceHarness::grant_case(int uid, bool refuse, unsigned round_phase, uint64_t decode_delay) {
    printf("[%s] source %d, admission phase %u: %s re-declaration\n",
           refuse ? "G" : "H", uid, round_phase, refuse ? "refused" : "admitted");
    probe(uid);
    run_until(cyc + ms(500));
    // 20000+42 bytes at 8000 intervals/s exceeds even the 1 Gb/s ceiling.
    // Warm the real TSpec pipeline, then withdraw until its grant clears.
    const uint16_t max_frame = refuse ? 20000 : 224;
    stage_declaration(uid, max_frame, true);
    run_until(cyc + 128);
    stage_declaration(uid, max_frame, false);
    run_until(cyc + ms(kDiagTickMs + 100)); // drain frames and close their last interval
    ck("withdrawal cleared the real grant", admitted[uid].v, 0);
    ck("withdrawal closed ACTIVE", active[uid].v, 0);
    ck("the ACMP declaration still stands", declaring[uid].v, 1);

    // Seed nonzero, distinct interval histories: an accidental start cannot
    // pass a reset check by resetting counters that were already zero.
    auto* rp = dut->rootp;
    rp->milan_datapath__DOT__talker_diag__DOT__mreset_r[uid] = 17;
    rp->milan_datapath__DOT__talker_diag__DOT__tuiv_r[uid] = 29;
    rp->milan_datapath__DOT__talker_diag__DOT__ftx_r[uid] = 43;
    const uint32_t starts = diag(Ctr::kStreamStart, uid);
    const uint32_t stops = diag(Ctr::kStreamStop, uid);
    Level& gate = uid == kUidCrf ? licence : aaf_gate;
    const long opens = gate.rises;
    const long active_opens = active[uid].rises;
    const long grants = admitted[uid].rises;
    const auto& pdus = uid == kUidCrf ? crf_pdus : aaf_pdus;
    const size_t pdu_count = pdus.size();
    const uint32_t crf_count = axi_read(A_CRFT_COUNT);
    while (cyc % kSources != round_phase) step();
    const uint64_t sent = cyc;
    rx_q.push_back(msrp_frame(listener_msg(sid_of(uid), 0, 1, 2)));
    run_until(sent + decode_delay - 1);
    stage_declaration(uid, max_frame, true);
    const uint64_t declared = cyc;
    // This step clears the registrar. The next one consumes the real
    // decoded Listener Ready while opt_r is still alive.
    step();
    run_until(cyc + 64);
    ck("Listener replay retained the measured decoder timing", listener_event[uid], sent + decode_delay);
    ck("Listener Ready registered after re-declaration", lstn_reg(uid), 2);
    ck("the optimistic window actually raised ACTIVE", static_cast<uint64_t>(active[uid].rises - active_opens), 1);
    ck_true("ACTIVE rose within three admission rounds", active[uid].last_rise > declared
            && active[uid].last_rise - declared <= 3 * kSources);
    if (refuse) {
        ck("the ceiling refused the re-declaration throughout", static_cast<uint64_t>(admitted[uid].rises - grants), 0);
        ck("the live over-limit bit confirms refusal", (axi_read(A_LWSRP_STATUS) >> 7) & 1u, 1);
        ck("ACTIVE fell after the optimistic window", active[uid].v, 0);
        ck("the declaration became Talker Failed",
           (rp->milan_datapath__DOT__pp_cd_srp_tk_decl_state_w >> (2 * uid)) & 3u, 2);
        run_until(cyc + ms(2500)); // multiple running media periods, including pipeline drain
        ck(uid == kUidCrf ? "refused CRF licence never opened" : "refused AAF gate never opened",
           static_cast<uint64_t>(gate.rises - opens), 0);
        ck("refused re-declaration adds no STREAM_START", diag(Ctr::kStreamStart, uid), starts);
        ck("refused re-declaration adds no STREAM_STOP", diag(Ctr::kStreamStop, uid), stops);
        ck("refused re-declaration preserves MEDIA_RESET", rp->milan_datapath__DOT__talker_diag__DOT__mreset_r[uid], 17);
        ck("refused re-declaration preserves TIMESTAMP_UNCERTAIN", rp->milan_datapath__DOT__talker_diag__DOT__tuiv_r[uid], 29);
        ck("refused re-declaration preserves FRAMES_TX", diag(Ctr::kFramesTx, uid), 43);
        ck("refused re-declaration emits no PDU", pdus.size(), pdu_count);
        if (uid == kUidCrf) ck("refused CRF leaves CRFT_COUNT unchanged", axi_read(A_CRFT_COUNT), crf_count);
    } else {
        ck("admitted re-declaration opens the licence once", static_cast<uint64_t>(gate.rises - opens), 1);
        ck_true("licence waits for both ACTIVE and grant", gate.last_rise >= active[uid].last_rise
                && gate.last_rise >= admitted[uid].last_rise);
        const uint64_t delay = gate.last_rise - active[uid].last_rise;
        printf("  [LATENCY] uid=%d phase=%u ACTIVE=%llu grant=%llu licence=%llu added_cycles=%llu\n",
               uid, round_phase, static_cast<unsigned long long>(active[uid].last_rise),
               static_cast<unsigned long long>(admitted[uid].last_rise),
               static_cast<unsigned long long>(gate.last_rise), static_cast<unsigned long long>(delay));
        ck_true("added start latency fits three admission rounds", delay <= 3 * kSources);
        ck("admitted start resets MEDIA_RESET", rp->milan_datapath__DOT__talker_diag__DOT__mreset_r[uid], 0);
        ck("admitted start resets TIMESTAMP_UNCERTAIN", rp->milan_datapath__DOT__talker_diag__DOT__tuiv_r[uid], 0);
        ck("admitted start resets FRAMES_TX", diag(Ctr::kFramesTx, uid), 0);
        run_until(cyc + ms(2500));
        ck_true("admitted re-declaration still streams", pdus.size() >= pdu_count + 2);
        ck("admitted re-declaration adds one STREAM_START", diag(Ctr::kStreamStart, uid), starts + 1);
        ck("admitted re-declaration adds no STREAM_STOP", diag(Ctr::kStreamStop, uid), stops);
    }
}

void CrfLicenceHarness::phase_real_grant() {
    printf("[G/H] #551: real admission ceiling and both round phases\n");
    corner_phase = true;
    sched.clear();
    for (auto& p : peer) { p.listener_on = false; p.bridge_decl = 0; }
    // Refresh the genuine ACMP/MAAP DA gate; staging SRP does not fake it.
    for (int uid = 0; uid < kSources; uid++) probe(uid);
    run_until(cyc + ms(500));
    sched.clear();
    for (int uid = 0; uid < kSources; uid++) {
        const uint64_t delay = listener_decode_delay(uid);
        ck_true("decoder delay can bracket a declaration", delay > 1 && delay < 4096);
        if (delay <= 1 || delay >= 4096) continue;
        for (unsigned phase = 0; phase < kSources; phase++) {
            grant_case(uid, true, phase, delay);
            grant_case(uid, false, phase, delay);
        }
        stage_declaration(uid, 224, false);
        run_until(cyc + ms(100));
    }
}

void CrfLicenceHarness::grade_invariants() {
    printf("[INV] over the whole run, every cycle\n");
    ck("the CRF licence equals ACTIVE[CRF] AND real grant (config: en, class A, SRP policing)",
       static_cast<uint64_t>(licence_ne_active), 0);
    ck("the AAF gate is never open without ACTIVE[AAF] AND real grant", static_cast<uint64_t>(aaf_without_active), 0);
    ck("no malformed DUT MRPDU", static_cast<uint64_t>(dut_malformed), 0);
}

int CrfLicenceHarness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut = model.get();
    printf("=== obj_crflic: #530 on endstation_ax7101_1x1_tdm8, 1 ms = %llu cycles ===\n",
           static_cast<unsigned long long>(kMsCyc));
    do_reset();
    boot();
    const uint64_t t0 = phase_a();
    phase_b(t0);
    phase_b2(t0);
    phase_c(t0);
    phase_f_after_c(licence.first_rise);
    phase_d();
    phase_e();
    phase_real_grant();
    grade_invariants();
    printf("--------------------------------------------------------------\n");
    printf("simulated %.2f ms (%llu cycles)\n", t_ms(cyc), static_cast<unsigned long long>(cyc));
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    CrfLicenceHarness harness;
    return harness.run();
}
