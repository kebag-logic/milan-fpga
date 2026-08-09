/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_lwsrp_top.sv built with N_CTX_P = 4 — the
 * N-attribute context table (docs/MILAN_COMPLIANCE_GAPS.md §3 closure:
 * the 2nd lwSRP listener attribute / CRF reservation, registrar half of
 * roadmap item 5).
 *
 * Cases (all structurally impossible on the old single-pair RTL unless
 * marked GOLDEN):
 *  - GOLDEN N=1 shape: with zero extra rows provisioned the enable declare
 *    pair is BYTE-IDENTICAL to the legacy engine's frames (golden arrays
 *    built from the byte contract the lwsrp_tx suite asserts field-wise).
 *  - CRF-listener row (idx 1): provision via the request/grant port ->
 *    byte-exact Listener MRPDU (NEW, AskingFailed), fast-join LeaveAll
 *    pair from the legacy applicant; bridge TalkerAdvertise -> Ready
 *    four-pack re-declared promptly; TalkerFailed -> failed + code via
 *    the indexed readback.
 *  - Extra talker row (idx 2): full 25-byte TalkerAdvertise FirstValue
 *    from the record RAM (dmac/vid/TSpec/PriorityAndRank/latency).
 *  - Multi-attribute MRPDU packing: one MSRPDU carrying a TalkerAdvertise
 *    message + a 2-vector Listener message (802.1Q §35.2 encoding,
 *    AttributeListLength per message).
 *  - One bridge vector covering MULTIPLE contexts at different +k with
 *    different three-/four-packed positions.
 *  - Add/remove mid-stream: withdraw emits the LV vector, later refreshes
 *    drop the message.
 *  - LeaveAll across contexts: prompt re-declare + per-row leave aging.
 */

#include "VKL_lwsrp_top.h"
#include "VKL_lwsrp_top___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <deque>

static VKL_lwsrp_top* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-52s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t STATION  = 0x020000000002ULL;
static const uint16_t UID      = 0;
static const uint64_t OUR_SID  = (STATION << 16) | UID;
static const uint64_t T2_SID   = OUR_SID + 1;             // extra talker row
static const uint64_t CRF_SID  = 0x0200000000010001ULL;   // AX CRF stream
static const uint64_t L3_SID   = CRF_SID + 2;             // 2nd listener row
static const uint16_t VID      = 2;
static const uint16_t MAXFRM   = 224;
static const uint32_t LATENCY  = 500000;
static const uint64_t DMAC0    = 0x91E0F000FE02ULL;
static const uint64_t DMAC2    = 0x91E0F000FE03ULL;
static const uint64_t BRIDGE   = 0x3CC0C6000001ULL;

enum { EV_NEW = 0, EV_JOININ = 1, EV_IN = 2, EV_JOINMT = 3, EV_MT = 4, EV_LV = 5 };
enum { D_IGN = 0, D_ASKFAIL = 1, D_READY = 2, D_READYFAIL = 3 };

// ---- cycle engine + TX frame collector -----------------------------------
static long cyc = 0;
static std::deque<std::vector<uint8_t>> tx_frames;
static std::vector<uint8_t> partial;

static void step() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    cyc++;
    if (dut->m_axis_tvalid && dut->m_axis_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_tkeep >> l) & 1)
                partial.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
        if (dut->m_axis_tlast) { tx_frames.push_back(partial); partial.clear(); }
    }
}
static void run(long n) { for (long i = 0; i < n; i++) step(); }
//! This TB elaborates KL_lwsrp_top with CLK_FREQ_HZ_P = 10000, so the
//! timers' 1 kHz strobe lands every 10 clocks: CYCLES_PER_MS converts a
//! clause duration into run() cycles. LEAVE_MS mirrors lwsrp_pkg
//! LEAVE_TIME_MS_C (Milan v1.2 Table 4.3). The aging wait below used to be
//! a bare run(6600) - 660 ms, which was LeaveTime + margin only while the
//! package still carried the IEEE 802.1Q 600 ms.
static const int CYCLES_PER_MS = 10;
static const int LEAVE_MS      = 5000;
static void run_ms(long ms) { run(ms * CYCLES_PER_MS); }
static void drain_tx() { tx_frames.clear(); }

// frame classification
static bool is_msrp(const std::vector<uint8_t>& f) {
    return f.size() >= 14 && f[12] == 0x22 && f[13] == 0xEA;
}
static bool is_mvrp(const std::vector<uint8_t>& f) {
    return f.size() >= 14 && f[12] == 0x88 && f[13] == 0xF5;
}
static bool is_legacy_msrp(const std::vector<uint8_t>& f) {
    return is_msrp(f) && f.size() >= 16 && f[15] == 4;    // Domain first
}
static bool is_ext(const std::vector<uint8_t>& f) {      // ctx serializer PDU
    return is_msrp(f) && f.size() >= 16 && (f[15] == 1 || f[15] == 3);
}

// wait until a frame matching pred shows up; only the MATCH is consumed
// (other frames — e.g. the legacy pair racing an ext MRPDU — stay queued)
template <typename P>
static std::vector<uint8_t> wait_frame(P pred, long maxc, const char* what) {
    long deadline = cyc + maxc;
    while (cyc < deadline) {
        for (auto it = tx_frames.begin(); it != tx_frames.end(); ++it) {
            if (pred(*it)) {
                auto f = *it;
                tx_frames.erase(it);
                return f;
            }
        }
        step();
    }
    checks++; fails++;
    printf("  [FAIL] %-52s (no frame within %ld cycles)\n", what, maxc);
    return {};
}

static void cmp_frame(const char* tag, const std::vector<uint8_t>& got,
                      const std::vector<uint8_t>& exp) {
    char w[96];
    snprintf(w, sizeof w, "%s: length", tag);
    ck(w, got.size(), exp.size());
    size_t n = got.size() < exp.size() ? got.size() : exp.size();
    for (size_t i = 0; i < n; i++) {
        if (got[i] != exp[i]) {
            checks++; fails++;
            printf("  [FAIL] %s: byte %zu got=0x%02x exp=0x%02x\n",
                   tag, i, got[i], exp[i]);
            return;
        }
    }
    checks++;   // one aggregated byte-equality check
}

// ---- golden TX builders (the byte contract the lwsrp_tx suite asserts) ---
static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

//! Every golden MRPDU below is padded to at least the 60 B Ethernet minimum,
//! so that is the reserve; the talker shape reaches 64 B and says so.
static const size_t MRPDU_MIN_BYTES = 60;

static std::vector<uint8_t> golden_legacy_msrp(bool talker, int dom_ev,
                                               int tk_ev, int lva) {
    std::vector<uint8_t> f;
    f.reserve(talker ? 64 : MRPDU_MIN_BYTES);
    put_be(f, 0x0180C200000EULL, 6); put_be(f, STATION, 6);
    put_be(f, 0x22EA, 2); f.push_back(0);
    uint16_t vech = (lva ? 0x2000 : 0x0000) | 1;
    f.push_back(4); f.push_back(4); put_be(f, 9, 2);
    put_be(f, vech, 2);
    f.push_back(6); f.push_back(3); put_be(f, VID, 2);
    f.push_back((uint8_t)(dom_ev * 36));
    put_be(f, 0, 2);
    if (talker) {
        f.push_back(1); f.push_back(25); put_be(f, 30, 2);
        put_be(f, vech, 2);
        put_be(f, OUR_SID, 8);
        put_be(f, DMAC0, 6); put_be(f, VID, 2);
        put_be(f, MAXFRM, 2); put_be(f, 1, 2);
        f.push_back(0x70);
        put_be(f, LATENCY, 4);
        f.push_back((uint8_t)(tk_ev * 36));
        put_be(f, 0, 2);
    }
    put_be(f, 0, 2);                       // message-list EndMark
    while (f.size() < (talker ? 64u : 60u)) f.push_back(0);
    return f;
}

static std::vector<uint8_t> golden_mvrp(int vid_ev, int lva) {
    std::vector<uint8_t> f;
    f.reserve(MRPDU_MIN_BYTES);
    put_be(f, 0x0180C2000021ULL, 6); put_be(f, STATION, 6);
    put_be(f, 0x88F5, 2); f.push_back(0);
    uint16_t vech = (lva ? 0x2000 : 0x0000) | 1;
    f.push_back(1); f.push_back(2);
    put_be(f, vech, 2);
    put_be(f, VID, 2);
    f.push_back((uint8_t)(vid_ev * 36));
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

//! extra-context MRPDU: optional TalkerAdvertise rows + Listener rows
struct ExtT { uint64_t sid; uint64_t dmac; uint16_t maxf, ivf;
              uint8_t pr; uint32_t lat; int ev; };
struct ExtL { uint64_t sid; int ev; int par; };
static std::vector<uint8_t> golden_ext(const std::vector<ExtT>& ts,
                                       const std::vector<ExtL>& ls) {
    // 15 B header, then 4 B + 28 B per talker record and 4 B + 12 B per
    // listener record, then the 2 B message-list EndMark
    size_t want = 15 + 2 + (ts.empty() ? 0 : 6 + 28 * ts.size())
                         + (ls.empty() ? 0 : 6 + 12 * ls.size());
    std::vector<uint8_t> f;
    f.reserve(want < MRPDU_MIN_BYTES ? MRPDU_MIN_BYTES : want);
    put_be(f, 0x0180C200000EULL, 6); put_be(f, STATION, 6);
    put_be(f, 0x22EA, 2); f.push_back(0);
    if (!ts.empty()) {
        f.push_back(1); f.push_back(25);
        put_be(f, ts.size() * 28 + 2, 2);
        for (const auto& t : ts) {
            put_be(f, 1, 2);               // vech: no lva, 1 value
            put_be(f, t.sid, 8);
            put_be(f, t.dmac, 6); put_be(f, VID, 2);
            put_be(f, t.maxf, 2); put_be(f, t.ivf, 2);
            f.push_back(t.pr);
            put_be(f, t.lat, 4);
            f.push_back((uint8_t)(t.ev * 36));
        }
        put_be(f, 0, 2);
    }
    if (!ls.empty()) {
        f.push_back(3); f.push_back(8);
        put_be(f, ls.size() * 12 + 2, 2);
        for (const auto& l : ls) {
            put_be(f, 1, 2);
            put_be(f, l.sid, 8);
            f.push_back((uint8_t)(l.ev * 36));
            f.push_back((uint8_t)(l.par * 64));
        }
        put_be(f, 0, 2);
    }
    put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

// ---- bridge-side PDU builders (the lwsrp_rx suite encoding) --------------
struct Vec {
    int lva = 0;
    int nv  = 1;
    std::vector<uint8_t> fv;
    std::vector<int> evts;
    std::vector<int> pars;
};
struct Msg { int type; int len; bool msrp; std::vector<Vec> vecs; };

static std::vector<uint8_t> encode_msg(const Msg& m) {
    // AttributeList: per vector a 2 B VectorHeader, the FirstValue, ceil(nv/3)
    // three-packed event octets and (listener) ceil(nv/4) four-packed
    // declarations; plus the 2 B vector-list EndMark.
    size_t want = 2;
    for (const auto& v : m.vecs)
        want += 2 + v.fv.size() + (v.nv + 2) / 3 + (v.nv + 3) / 4;
    std::vector<uint8_t> body;
    body.reserve(want);
    for (const auto& v : m.vecs) {
        put_be(body, (uint64_t)((v.lva << 13) | v.nv), 2);
        body.insert(body.end(), v.fv.begin(), v.fv.end());
        int ne = (v.nv + 2) / 3;
        for (int i = 0; i < ne; i++) {
            int e0 = (3*i   < (int)v.evts.size()) ? v.evts[3*i]   : 0;
            int e1 = (3*i+1 < (int)v.evts.size()) ? v.evts[3*i+1] : 0;
            int e2 = (3*i+2 < (int)v.evts.size()) ? v.evts[3*i+2] : 0;
            body.push_back((uint8_t)(e0*36 + e1*6 + e2));
        }
        if (m.msrp && m.type == 3) {
            int np = (v.nv + 3) / 4;
            for (int i = 0; i < np; i++) {
                int p0 = (4*i   < (int)v.pars.size()) ? v.pars[4*i]   : 0;
                int p1 = (4*i+1 < (int)v.pars.size()) ? v.pars[4*i+1] : 0;
                int p2 = (4*i+2 < (int)v.pars.size()) ? v.pars[4*i+2] : 0;
                int p3 = (4*i+3 < (int)v.pars.size()) ? v.pars[4*i+3] : 0;
                body.push_back((uint8_t)(p0*64 + p1*16 + p2*4 + p3));
            }
        }
    }
    put_be(body, 0, 2);
    std::vector<uint8_t> out;
    out.reserve(4 + body.size());       // type + len + AttributeListLength
    out.push_back((uint8_t)m.type);
    out.push_back((uint8_t)m.len);
    if (m.msrp) put_be(out, body.size(), 2);
    out.insert(out.end(), body.begin(), body.end());
    return out;
}

static std::vector<uint8_t> bframe(const std::vector<Msg>& msgs) {
    std::vector<uint8_t> f;
    f.reserve(MRPDU_MIN_BYTES);         // 14 B header + messages, padded here
    put_be(f, 0x0180C200000EULL, 6);
    put_be(f, BRIDGE, 6);
    put_be(f, 0x22EA, 2);
    f.push_back(0);
    for (const auto& m : msgs) {
        auto mb = encode_msg(m);
        f.insert(f.end(), mb.begin(), mb.end());
    }
    put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

static std::vector<uint8_t> fv_listener(uint64_t sid) {
    std::vector<uint8_t> v; v.reserve(8);      // the StreamID, exactly
    put_be(v, sid, 8); return v;
}
static std::vector<uint8_t> fv_talker(uint64_t sid) {
    std::vector<uint8_t> v; v.reserve(25);
    put_be(v, sid, 8);
    for (int i = 0; i < 17; i++) v.push_back(0xA0 + i);
    return v;
}
//! explicit DataFrameParameters (the Table 5.29 three-parameter legs)
static std::vector<uint8_t> fv_talker_dv(uint64_t sid, uint64_t dmac,
                                         uint16_t vlan) {
    std::vector<uint8_t> v; v.reserve(25);
    put_be(v, sid, 8);
    put_be(v, dmac, 6); put_be(v, vlan, 2);          // DFP
    put_be(v, 100, 2);  put_be(v, 1, 2);             // TSpec
    v.push_back(0x70);                               // PriorityAndRank
    put_be(v, 1000, 4);                              // AccumulatedLatency
    return v;                                        // 25 B
}
static std::vector<uint8_t> fv_tfail_dv(uint64_t sid, uint64_t dmac,
                                        uint16_t vlan, uint8_t code) {
    auto v = fv_talker_dv(sid, dmac, vlan);
    v.reserve(34);                      // + 8 B BridgeID + 1 B failure code
    put_be(v, BRIDGE << 16, 8);
    v.push_back(code);
    return v;                                        // 34 B
}
static std::vector<uint8_t> fv_tfail(uint64_t sid, uint8_t code) {
    auto v = fv_talker(sid);
    v.reserve(34);                      // + 8 B BridgeID + 1 B failure code
    put_be(v, BRIDGE << 16, 8);
    v.push_back(code);
    return v;
}
static Msg msg_listener(const Vec& v) { return {3, 8,  true, {v}}; }
static Msg msg_tadv(const Vec& v)     { return {1, 25, true, {v}}; }
static Msg msg_tfail(const Vec& v)    { return {2, 34, true, {v}}; }

static void feed(const std::vector<uint8_t>& f) {
    size_t n = f.size();
    for (size_t off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (int l = 0; l < 8 && off + l < n; l++) {
            d |= (uint64_t)f[off + l] << (8 * l);
            k |= 1 << l;
        }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tlast_i = (off + 8 >= n);
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step();
}

// PARKED-LANE TORTURE (gh #65): a stalled DMA holds tready low mid-frame
// while the producer keeps tvalid on the SAME beat. A tap that samples
// tvalid alone eats every parked cycle as a NEW beat and tears the PDU.
static void feed_parked(const std::vector<uint8_t>& f, int park_beat,
                        int park_cycles) {
    size_t n = f.size();
    int beat = 0;
    for (size_t off = 0; off < n; off += 8, beat++) {
        uint64_t d = 0; uint8_t k = 0;
        for (int l = 0; l < 8 && off + l < n; l++) {
            d |= (uint64_t)f[off + l] << (8 * l);
            k |= 1 << l;
        }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tlast_i = (off + 8 >= n);
        if (beat == park_beat) {
            dut->rx_tready_i = 0;
            for (int i = 0; i < park_cycles; i++) step();
            dut->rx_tready_i = 1;
        }
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step();
}

// ---- context provisioning port -------------------------------------------
static void ctx_write(int idx, int valid, int dir, uint64_t sid,
                      uint64_t dmac = 0, uint8_t pr = 0x70,
                      uint16_t maxf = 0, uint16_t ivf = 0, uint32_t lat = 0,
                      uint16_t vlan = 0) {
    dut->ctx_req_i = 1; dut->ctx_we_i = 1; dut->ctx_idx_i = idx;
    dut->ctx_valid_i = valid; dut->ctx_dir_i = dir; dut->ctx_sid_i = sid;
    dut->ctx_dmac_i = dmac; dut->ctx_vlan_i = vlan; dut->ctx_prio_rank_i = pr;
    dut->ctx_max_frame_i = maxf; dut->ctx_interval_i = ivf;
    dut->ctx_latency_i = lat;
    int guard = 20;
    do { step(); } while (!dut->ctx_gnt_o && guard--);
    ck("ctx port: write granted", dut->ctx_gnt_o, 1);
    dut->ctx_req_i = 0; dut->ctx_we_i = 0;
    step();
}

static uint16_t ctx_read(int idx, uint64_t* sid = nullptr) {
    dut->ctx_req_i = 1; dut->ctx_we_i = 0; dut->ctx_idx_i = idx;
    int guard = 20;
    do { step(); } while (!dut->ctx_gnt_o && guard--);
    ck("ctx port: read granted", dut->ctx_gnt_o, 1);
    uint16_t stat = dut->ctx_rd_stat_o;
    if (sid) *sid = dut->ctx_rd_sid_o;
    dut->ctx_req_i = 0;
    step();
    return stat;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_top;

    dut->rst_n = 0; dut->enable_i = 0; dut->talker_en_i = 0; dut->is_1g_i = 0;
    dut->station_mac_i = STATION; dut->unique_id_i = UID;
    dut->dest_mac_i = DMAC0; dut->vid_i = VID;
    dut->max_frame_i = MAXFRM; dut->interval_frames_i = 1;
    dut->latency_i = LATENCY;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0;
    dut->rx_tlast_i = 0;
    // the tapped lane's consumer is idle-ready; the gh #65 leg parks it
    dut->rx_tready_i = 1;
    dut->m_axis_tready = 1;
    dut->ctx_req_i = 0; dut->ctx_we_i = 0; dut->ctx_idx_i = 0;
    dut->ctx_valid_i = 0; dut->ctx_dir_i = 0; dut->ctx_sid_i = 0;
    dut->ctx_dmac_i = 0; dut->ctx_prio_rank_i = 0;
    dut->ctx_max_frame_i = 0; dut->ctx_interval_i = 0; dut->ctx_latency_i = 0;
    dut->lstn_bound_i = 0; dut->lstn_declare_i = 0; dut->lstn_sid_i = 0;
    for (int i = 0; i < 8; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) step();

    printf("== KL_lwsrp_top N_CTX_P=4 harness (context table) ==\n");

    // 0) disabled: quiet, no rows
    run(3000);
    ck("disabled: no TX", tx_frames.size(), 0);
    ck("disabled: ctx vectors clear", dut->ctx_reg_o | dut->ctx_ready_o |
                                      dut->ctx_failed_o, 0);

    // 1) GOLDEN N=1 shape: enable + talker with ZERO extra rows -> the
    //    declare pair is byte-identical to the legacy engine's frames
    dut->enable_i = 1; dut->talker_en_i = 1;
    run(3000);
    ck("golden: exactly the declare pair", tx_frames.size(), 2);
    if (tx_frames.size() >= 2) {
        cmp_frame("golden: MSRP declare (Domain NEW + TA NEW, lva)",
                  tx_frames[0], golden_legacy_msrp(true, EV_NEW, EV_NEW, 1));
        cmp_frame("golden: MVRP declare (VID NEW, lva)",
                  tx_frames[1], golden_mvrp(EV_NEW, 1));
    }
    drain_tx();

    // 2) provision the CRF-listener row (idx 1) through the req/gnt port
    ctx_write(1, 1, 1, CRF_SID);
    {
        // the shared serializer emits the Listener MRPDU: NEW, AskingFailed
        auto f = wait_frame(is_ext, 3000, "crf: ext MRPDU");
        cmp_frame("crf: Listener NEW/AskingFailed MRPDU", f,
                  golden_ext({}, {{CRF_SID, EV_NEW, D_ASKFAIL}}));
        // the fast-join rule fires the legacy LeaveAll pair too
        auto g = wait_frame(is_legacy_msrp, 3000, "crf: fast-join MSRP");
        ck("crf: fast-join pair carries LeaveAll",
           g.size() >= 21 && (g[19] & 0xE0) != 0, 1);
    }
    drain_tx();

    // 3) bridge TalkerAdvertise covering CRF_SID -> registered + Ready
    //    four-pack re-declared promptly (ready-change rule)
    {
        Vec v; v.fv = fv_talker(CRF_SID); v.evts = {EV_JOININ};
        feed(bframe({msg_tadv(v)}));
        run(200);
        ck("crf: ctx_reg bit1", (dut->ctx_reg_o >> 1) & 1, 1);
        ck("crf: ctx_ready bit1", (dut->ctx_ready_o >> 1) & 1, 1);
        auto f = wait_frame(is_ext, 3000, "crf: Ready re-declare");
        cmp_frame("crf: Listener JOININ/Ready MRPDU", f,
                  golden_ext({}, {{CRF_SID, EV_JOININ, D_READY}}));
    }
    drain_tx();

    // 4) indexed readback: row 1 snapshot + row 0 legacy view
    {
        uint64_t sid = 0;
        uint16_t st = ctx_read(1, &sid);
        ck("rb1: sid", sid, CRF_SID);
        ck("rb1: valid", (st >> 15) & 1, 1);
        ck("rb1: dir listener", (st >> 14) & 1, 1);
        ck("rb1: declared", (st >> 13) & 1, 1);
        ck("rb1: registered", (st >> 12) & 1, 1);
        ck("rb1: ready", (st >> 11) & 1, 1);
        ck("rb1: not failed", (st >> 10) & 1, 0);
        uint16_t st0 = ctx_read(0, &sid);
        ck("rb0: legacy sid", sid, OUR_SID);
        ck("rb0: legacy valid (talker_en)", (st0 >> 15) & 1, 1);
        ck("rb0: legacy declared", (st0 >> 13) & 1, 1);
        ck("rb0: legacy not registered yet", (st0 >> 12) & 1, 0);
    }
    drain_tx();

    // 5) bridge TalkerFailed for the CRF stream -> failed + code readback
    {
        Vec v; v.fv = fv_tfail(CRF_SID, 0x08); v.evts = {EV_JOININ};
        feed(bframe({msg_tfail(v)}));
        run(200);
        ck("crf-tf: ctx_failed bit1", (dut->ctx_failed_o >> 1) & 1, 1);
        uint16_t st = ctx_read(1);
        ck("crf-tf: failed", (st >> 10) & 1, 1);
        ck("crf-tf: code", st & 0xFF, 0x08);
        ck("crf-tf: TA registration intact", (st >> 12) & 1, 1);
    }
    drain_tx();

    // 6) extra talker row (idx 2) + 2nd listener row (idx 3), then the
    //    periodic refresh packs ALL rows into ONE MRPDU:
    //    TalkerAdvertise message (1 vector, full 25-B FirstValue from the
    //    record RAM) + Listener message (2 vectors)
    ctx_write(2, 1, 0, T2_SID, DMAC2, 0x70, 100, 1, 1000);
    ctx_write(3, 1, 1, L3_SID);
    run(4000);       // let the add-frames drain
    drain_tx();
    {
        auto f = wait_frame([](const std::vector<uint8_t>& f) {
            return is_ext(f) && f.size() >= 16 && f[15] == 1;
        }, 14000, "pack: refresh MRPDU");
        cmp_frame("pack: TA + 2-vector Listener in one MRPDU", f,
                  golden_ext({{T2_SID, DMAC2, 100, 1, 0x70, 1000, EV_JOININ}},
                             {{CRF_SID, EV_JOININ, D_READY},
                              {L3_SID, EV_JOININ, D_ASKFAIL}}));
    }
    drain_tx();

    // 7) ONE bridge Listener vector covering the LEGACY talker AND the
    //    extra talker row at different +k with different four-packs
    {
        Vec v; v.nv = 2; v.fv = fv_listener(OUR_SID);
        v.evts = {EV_JOININ, EV_JOININ};
        v.pars = {D_READY, D_READYFAIL};
        feed(bframe({msg_listener(v)}));
        run(200);
        ck("multi: legacy listener ready", dut->listener_ready_o, 1);
        ck("multi: legacy decl Ready", dut->listener_decl_o, D_READY);
        ck("multi: ctx_reg bit2 (talker row)", (dut->ctx_reg_o >> 2) & 1, 1);
        ck("multi: ctx_ready bit2", (dut->ctx_ready_o >> 2) & 1, 1);
        uint16_t st = ctx_read(2);
        ck("multi: row2 decl ReadyFailed", (st >> 8) & 3, D_READYFAIL);
    }
    drain_tx();

    // 7b) REGISTERING_FAILED source (Milan Table 5.47, gh #56 A2):
    //    lstn_ask_fail_o rides the stream_gate index law (L=1 here, so
    //    talker t = ctx row t). ReadyFailed from 7) is NOT AskingFailed;
    //    an AskingFailed four-pack raises the bit — on the ctx row AND on
    //    the legacy row 0 — and Ready drops both. The listener-dir rows
    //    (1 and 3) can never assert: their lanes track the TA, not a
    //    four-pack the bridge declares back at us.
    {
        ck("laf: ReadyFailed is NOT asking-failed", dut->lstn_ask_fail_o, 0);
        Vec v; v.fv = fv_listener(T2_SID);
        v.evts = {EV_JOININ}; v.pars = {D_ASKFAIL};
        feed(bframe({msg_listener(v)}));
        run(200);
        ck("laf: row-2 AskingFailed -> talker-2 bit", dut->lstn_ask_fail_o, 0x4);
        ck("laf: ...and drops out of the ready view",
           (dut->ctx_ready_o >> 2) & 1, 0);
        Vec l0; l0.fv = fv_listener(OUR_SID);
        l0.evts = {EV_JOININ}; l0.pars = {D_ASKFAIL};
        feed(bframe({msg_listener(l0)}));
        run(200);
        ck("laf: legacy row joins at bit 0", dut->lstn_ask_fail_o, 0x5);
        Vec r2; r2.fv = fv_listener(T2_SID);
        r2.evts = {EV_JOININ}; r2.pars = {D_READY};
        feed(bframe({msg_listener(r2)}));
        Vec r0; r0.fv = fv_listener(OUR_SID);
        r0.evts = {EV_JOININ}; r0.pars = {D_READY};
        feed(bframe({msg_listener(r0)}));
        run(200);
        ck("laf: Ready drops both bits", dut->lstn_ask_fail_o, 0);
        ck("laf: row 2 back in the ready view", (dut->ctx_ready_o >> 2) & 1, 1);
    }
    drain_tx();

    // 8) ONE bridge TalkerAdvertise vector covering BOTH listener rows
    //    (CRF at k=0, row 3 at k=2; k=1 is nobody). The k=0 value carries
    //    In — NOT a registering event (802.1Q Table 10-4 has no rIn! row) —
    //    so the pin is per-k decode: the In leaves CRF's EXISTING
    //    registration alone while the k=2 JoinIn registers row 3.
    {
        Vec v; v.nv = 3; v.fv = fv_talker(CRF_SID);
        v.evts = {EV_IN, EV_MT, EV_JOININ};
        feed(bframe({msg_tadv(v)}));
        run(200);
        ck("multi-ta: CRF still registered", (dut->ctx_reg_o >> 1) & 1, 1);
        ck("multi-ta: row3 registered", (dut->ctx_reg_o >> 3) & 1, 1);
        ck("multi-ta: row3 ready", (dut->ctx_ready_o >> 3) & 1, 1);
    }
    run(3000); drain_tx();     // row3 Ready toggle re-declare drains here

    // 9) remove the talker row mid-stream: the withdraw frame carries the
    //    TalkerAdvertise LV vector; later refreshes drop the message
    ctx_write(2, 0, 0, 0);
    {
        auto f = wait_frame([](const std::vector<uint8_t>& f) {
            return is_ext(f) && f.size() >= 16 && f[15] == 1;
        }, 3000, "rm: LV MRPDU");
        cmp_frame("rm: TA LV + Listener rows in the withdraw MRPDU", f,
                  golden_ext({{T2_SID, DMAC2, 100, 1, 0x70, 1000, EV_LV}},
                             {{CRF_SID, EV_JOININ, D_READY},
                              {L3_SID, EV_JOININ, D_READY}}));
        run(10);   // let tx_done clear the on-wire flag before the snapshot
        uint16_t st = ctx_read(2);
        ck("rm: row2 not valid", (st >> 15) & 1, 0);
        ck("rm: row2 not declared", (st >> 13) & 1, 0);
        drain_tx();
        auto g = wait_frame(is_ext, 14000, "rm: next refresh");
        ck("rm: refresh has no TA message", g.size() >= 16 && g[15] == 3, 1);
    }
    drain_tx();

    // 10) LeaveAll across contexts: prompt re-declare, then per-row aging
    {
        Vec v; v.lva = 1; v.fv = fv_listener(OUR_SID);
        v.evts = {EV_MT}; v.pars = {D_IGN};
        feed(bframe({msg_listener(v)}));
        auto f = wait_frame(is_ext, 3000, "la: prompt ext re-declare");
        ck("la: re-declare is the Listener msg",
           f.size() >= 16 && f[15] == 3, 1);
        auto g = wait_frame(is_legacy_msrp, 3000, "la: legacy re-declare");
        ck("la: legacy pair too", g.size() >= 16, 1);
        // both listener rows lose their TA registration after LeaveTime
        run_ms(LEAVE_MS + 200);
        ck("la: CRF registration aged out", (dut->ctx_reg_o >> 1) & 1, 0);
        ck("la: row3 registration aged out", (dut->ctx_reg_o >> 3) & 1, 0);
        ck("la: CRF not ready", (dut->ctx_ready_o >> 1) & 1, 0);
    }
    drain_tx();

    // 11) post-LeaveAll recovery: a fresh TA registers again
    {
        Vec v; v.fv = fv_talker(CRF_SID); v.evts = {EV_JOININ};
        feed(bframe({msg_tadv(v)}));
        run(200);
        ck("recover: CRF registered again", (dut->ctx_reg_o >> 1) & 1, 1);
    }

    // 11b) THE rIn! FIX ON THE CONTEXT ROWS (802.1Q-2018 Table 10-4: the
    //   registering events are rNew!/rJoinIn!/rJoinMt! ONLY — there is no
    //   rIn! registrar row; In means "the sender holds it registered but
    //   is NOT declaring it"). Both directions had In arms until
    //   2026-08-08; both are pinned here.
    {
        // (a) LISTENER direction, In-from-empty — the WORST site: the
        //     registering condition was (jn_w || in_w), so a bare In on
        //     the Talker attribute conjured a Talker registration from MT,
        //     a declaration nobody made. Row 3 aged out in 10) and was
        //     never re-registered.
        ck("in-ctx: row3 starts MT", (dut->ctx_reg_o >> 3) & 1, 0);
        Vec v; v.fv = fv_talker(L3_SID); v.evts = {EV_IN};
        feed(bframe({msg_tadv(v)}));
        run(400);
        ck("in-ctx: In from MT does not register",
           (dut->ctx_reg_o >> 3) & 1, 0);
        ck("in-ctx: not ready either", (dut->ctx_ready_o >> 3) & 1, 0);
        Vec tf; tf.fv = fv_tfail(L3_SID, 0x22); tf.evts = {EV_IN};
        feed(bframe({msg_tfail(tf)}));
        run(400);
        ck("in-ctx: In TF fabricates no failure",
           (dut->ctx_failed_o >> 3) & 1, 0);
        // control: JoinMt on the same lane registers — the negatives above
        // are the event law, not a dead lane
        Vec c; c.fv = fv_talker(L3_SID); c.evts = {EV_JOINMT};
        feed(bframe({msg_tadv(c)}));
        run(400);
        ck("in-ctx: JoinMt control registers", (dut->ctx_reg_o >> 3) & 1, 1);
    }
    run(3000); drain_tx();     // row3 Ready toggle re-declare drains here
    {
        // (b) TALKER direction: In neither refreshes the four-pack nor
        //     cancels the leave counter. Re-provision the talker row,
        //     register the bridge's Listener Ready, LeaveAll, then In-only
        //     "refreshes" carrying a contradicting four-pack — the
        //     registration MUST age out at LeaveTime with the stored
        //     declaration untouched (the old In arm cancelled rleave and
        //     adopted the four-pack, holding the row alive forever).
        ctx_write(2, 1, 0, T2_SID, DMAC2, 0x70, 100, 1, 1000);
        run(400);
        Vec l; l.fv = fv_listener(T2_SID); l.evts = {EV_JOININ};
        l.pars = {D_READY};
        feed(bframe({msg_listener(l)}));
        run(200);
        ck("in-tdir: registered Ready", (dut->ctx_reg_o >> 2) & 1, 1);
        ck("in-tdir: ready", (dut->ctx_ready_o >> 2) & 1, 1);
        Vec la; la.lva = 1; la.fv = fv_listener(T2_SID);
        la.evts = {EV_MT}; la.pars = {D_IGN};
        feed(bframe({msg_listener(la)}));
        run_ms(2000);
        Vec in; in.fv = fv_listener(T2_SID); in.evts = {EV_IN};
        in.pars = {D_ASKFAIL};        // a refresh would flip Ready->AskFail
        feed(bframe({msg_listener(in)}));
        run_ms(2000);
        feed(bframe({msg_listener(in)}));
        run(200);
        ck("in-tdir: still registered inside LeaveTime",
           (dut->ctx_reg_o >> 2) & 1, 1);
        uint16_t st = ctx_read(2);
        ck("in-tdir: In did not refresh the four-pack (decl stays Ready)",
           (st >> 8) & 3, D_READY);
        run_ms(1200);                 // 5200 ms past the LeaveAll
        ck("in-tdir: In never cancels the leave counter -> aged out at "
           "LeaveTime", (dut->ctx_reg_o >> 2) & 1, 0);
        ctx_write(2, 0, 0, 0);
        run(400);
        drain_tx();
    }

    // 12) THE BORROW TERM ON THE CONTEXT LANES. The walker carries three
    //   independent +k matchers: our_sid and the ACMP-bound lsid (both
    //   pinned in the lwsrp_rx suite) and ONE PER CONTEXT ROW - EXT_LANES_P,
    //   which is 14 at the ax7101 8x8 shape and 3 here. The 2026-07-27 area
    //   round rewrote all three from a 64-bit subtract PLUS an independent
    //   magnitude compare into one 65-bit borrow-out subtract, and dropping
    //   the borrow bit from the CONTEXT LANES alone left every check in
    //   lwsrp_rx AND lwsrp_ctx green (mutation-found). This is the only
    //   harness that can provision a row, so it is pinned here.
    //   The alias needs base - sid > 2^64 - 8192, i.e. a SMALL sid: exactly
    //   what a low-numbered or not-yet-provisioned row carries.
    {
        drain_tx();
        ctx_write(2, 1, 1, 5);              // row 2 = listener bound to sid 5
        run(400);
        // base = 2^64-1, nv = 8  ->  (5 - base) mod 2^64 = 6 < 8, so a
        // wrap-blind lane "registers" row 2 off a vector that never covers it
        Vec v; v.nv = 8; v.fv = fv_talker(0xFFFFFFFFFFFFFFFFULL);
        v.evts.assign(8, EV_MT); v.evts[6] = EV_JOININ;
        feed(bframe({msg_tadv(v)}));
        run(400);
        ck("wrap-ctx: base > sid never registers",
           (dut->ctx_reg_o >> 2) & 1, 0);
        // control: the same shape based at 0 is a genuine hit at k = 5, which
        // is what makes the negative above the BORROW term and not a malformed
        // vector or an unprovisioned row
        Vec g; g.nv = 8; g.fv = fv_talker(0);
        g.evts.assign(8, EV_MT); g.evts[5] = EV_JOININ;
        feed(bframe({msg_tadv(g)}));
        run(400);
        ck("wrap-ctx: base <= sid registers", (dut->ctx_reg_o >> 2) & 1, 1);
        ctx_write(2, 0, 0, 0);
        run(400);
        drain_tx();
    }

    // 12) THE PORT CYCLE CONTRACT (2026-08-02 - the datapath's launch-stage
    //   retime leans on it): a write applies on the SERVICE beat, the one
    //   cycle where `ctx_req_i && !ctx_gnt_o`, and on that beat's closing
    //   edge the row identity, row_fresh AND ctx_gnt_o all register
    //   TOGETHER - the walker/serializer can never see a written row
    //   without its fresh mark, or a grant without its write. A held
    //   request is serviced every OTHER cycle (gnt alternates), so two
    //   writes never land on adjacent edges.
    {
        auto* rp = dut->rootp;
        auto lane_sid = [&](int l) -> uint64_t {
            return (uint64_t)rp->KL_lwsrp_top__DOT__ctx__DOT__sid_r[2*l] |
                   ((uint64_t)
                    rp->KL_lwsrp_top__DOT__ctx__DOT__sid_r[2*l + 1] << 32);
        };
        // row 3 (lane 2) known-invalid and quiet
        ctx_write(3, 0, 0, 0);
        run(400);
        drain_tx();
        ck("port: row 3 starts invalid",
           (rp->KL_lwsrp_top__DOT__ctx__DOT__valid_r >> 2) & 1, 0);
        ck("port: row 3 fresh clear",
           (rp->KL_lwsrp_top__DOT__row_fresh_w >> 2) & 1, 0);
        ck("port: gnt idle before the request", dut->ctx_gnt_o, 0);
        // present the write RAW and watch the single service beat close
        dut->ctx_req_i = 1; dut->ctx_we_i = 1; dut->ctx_idx_i = 3;
        dut->ctx_valid_i = 1; dut->ctx_dir_i = 1; dut->ctx_sid_i = L3_SID;
        dut->ctx_dmac_i = 0; dut->ctx_prio_rank_i = 0x70;
        dut->ctx_max_frame_i = MAXFRM; dut->ctx_interval_i = 1;
        dut->ctx_latency_i = LATENCY;
        step();   // the service beat's closing edge: EVERYTHING lands here
        ck("port: row valid ON the service edge",
           (rp->KL_lwsrp_top__DOT__ctx__DOT__valid_r >> 2) & 1, 1);
        ck("port: row_fresh ON the SAME edge",
           (rp->KL_lwsrp_top__DOT__row_fresh_w >> 2) & 1, 1);
        ck("port: sid ON the SAME edge", lane_sid(2) == L3_SID, 1);
        ck("port: gnt ON the SAME edge (answers the write beat)",
           dut->ctx_gnt_o, 1);
        // held request: gnt alternates - a service beat is never adjacent
        // to the previous one
        int adj = 0, svcs = 0, prev_gnt = 1;
        for (int c = 0; c < 6; c++) {
            step();
            if (dut->ctx_gnt_o) { svcs++; if (prev_gnt) adj++; }
            prev_gnt = dut->ctx_gnt_o;
        }
        ck("port: held req services every OTHER cycle", svcs, 3);
        ck("port: two grants never adjacent", adj, 0);
        dut->ctx_req_i = 0; dut->ctx_we_i = 0;
        step(); step();
        ck("port: gnt idle after release", dut->ctx_gnt_o, 0);
        // withdraw + settle so the finals below see the steady shape
        ctx_write(3, 0, 0, 0);
        run(400);
        drain_tx();
    }

    // ================================================================
    // [B1d] Table 5.29 three-parameter registrar match (listener rows)
    //   EVT_TK_REGISTERED requires the Talker attribute to match ALL of
    //   {Stream ID, Stream Destination MAC Address, Stream VLAN ID}; a
    //   mismatch is ignored (5.3.8.9 — the sink re-probes instead).
    //   Before this round the lane hit was sid-range-only: the wrong-vlan
    //   leg below REGISTERED.
    // ================================================================
    {
        const uint64_t M_SID = 0x0200000000010009ULL;
        const uint64_t EXPD  = 0x91E0F000BE55ULL;
        // fresh listener row carrying the EXPECTED pair {EXPD, vlan 2}
        ctx_write(3, 1, 1, M_SID, EXPD, 0x70, 0, 0, 0, 2);
        run(400); drain_tx();
        ck("b1d: row starts unregistered", (dut->ctx_reg_o >> 3) & 1, 0);

        // sid matches, vlan WRONG: never registers (the B1d bite)
        Vec w; w.fv = fv_talker_dv(M_SID, EXPD, 5); w.evts = {EV_JOININ};
        feed(bframe({msg_tadv(w)}));
        run(200);
        ck("b1d: sid-match wrong-vlan TA never registers (Tab 5.29)",
           (dut->ctx_reg_o >> 3) & 1, 0);

        // sid matches, dmac WRONG: same verdict
        Vec d; d.fv = fv_talker_dv(M_SID, EXPD + 1, 2); d.evts = {EV_JOININ};
        feed(bframe({msg_tadv(d)}));
        run(200);
        ck("b1d: wrong-dmac TA never registers",
           (dut->ctx_reg_o >> 3) & 1, 0);

        // all three match: registers (the negative legs are the law, not
        // a parse failure)
        Vec g; g.fv = fv_talker_dv(M_SID, EXPD, 2); g.evts = {EV_JOININ};
        feed(bframe({msg_tadv(g)}));
        run(200);
        ck("b1d: three-parameter match registers",
           (dut->ctx_reg_o >> 3) & 1, 1);
        drain_tx();

        // +k law: 802.1Q 35.2.2.8.1 increments StreamID AND destination_
        // address together through a vector, so a base 2 BELOW with the
        // base dmac 2 below covers our row at k=2 with dmac EXPD exactly
        ctx_write(3, 0, 0, 0); run(100);
        ctx_write(3, 1, 1, M_SID, EXPD, 0x70, 0, 0, 0, 2);
        run(400); drain_tx();
        Vec k; k.nv = 3; k.fv = fv_talker_dv(M_SID - 2, EXPD - 2, 2);
        k.evts = {EV_MT, EV_MT, EV_JOININ};
        feed(bframe({msg_tadv(k)}));
        run(200);
        ck("b1d: +k hit with dmac shifted together registers",
           (dut->ctx_reg_o >> 3) & 1, 1);
        drain_tx();

        // +k negative: the same vector with the base dmac UNshifted is a
        // different stream's DFP at our k (offset 0 != 2) — ignored
        ctx_write(3, 0, 0, 0); run(100);
        ctx_write(3, 1, 1, M_SID, EXPD, 0x70, 0, 0, 0, 2);
        run(400); drain_tx();
        Vec kn; kn.nv = 3; kn.fv = fv_talker_dv(M_SID - 2, EXPD, 2);
        kn.evts = {EV_MT, EV_MT, EV_JOININ};
        feed(bframe({msg_tadv(kn)}));
        run(200);
        ck("b1d: +k hit with unshifted dmac never registers",
           (dut->ctx_reg_o >> 3) & 1, 0);

        // TalkerFailed obeys the same law (Table 5.29: EITHER attribute)
        Vec fw; fw.fv = fv_tfail_dv(M_SID, EXPD, 5, 0x08);
        fw.evts = {EV_JOININ};
        feed(bframe({msg_tfail(fw)}));
        run(200);
        ck("b1d: wrong-vlan TF never registers a failure",
           (dut->ctx_failed_o >> 3) & 1, 0);
        Vec fg; fg.fv = fv_tfail_dv(M_SID, EXPD, 2, 0x08);
        fg.evts = {EV_JOININ};
        feed(bframe({msg_tfail(fg)}));
        run(200);
        ck("b1d: matching TF registers the failure",
           (dut->ctx_failed_o >> 3) & 1, 1);
        {
            uint16_t st = ctx_read(3);
            ck("b1d: failure code via readback", st & 0xFF, 0x08);
        }
        drain_tx();

        // zero expected pair = parameters not learned yet (5.3.8.9): the
        // walker matches sid-only — the lawful window where a talker's TA
        // precedes our probe response (CRF fast-connect, t27 shape)
        ctx_write(3, 0, 0, 0); run(100);
        ctx_write(3, 1, 1, M_SID);                    // pair {0, 0}
        run(400); drain_tx();
        Vec z; z.fv = fv_talker_dv(M_SID, 0x112233445566ULL, 7);
        z.evts = {EV_JOININ};
        feed(bframe({msg_tadv(z)}));
        run(200);
        ck("b1d: zero pair = sid-only match (learn window)",
           (dut->ctx_reg_o >> 3) & 1, 1);
        // withdraw + settle so the finals below see the steady shape
        ctx_write(3, 0, 0, 0);
        run(400);
        drain_tx();
    }

    // ============================================================
    // PARKED-LANE TORTURE (gh #65): a stalled DMA parks a beat with tvalid
    // held. A tap that samples tvalid alone eats every parked cycle as a
    // new beat, tears the PDU, and the context row only registers on the
    // SECOND copy. ONE TalkerAdvertise across a 600-cycle stall must fill
    // the row's status word first-shot.
    // ============================================================
    printf("-- [PARK] parked-lane torture (gh #65) --\n");
    {
        const uint64_t P_SID = 0x0200000000AA0000ULL;
        ctx_write(3, 1, 1, P_SID);            // listener row, fresh sid
        run(400); drain_tx();
        ck("[PARK] pre: row 3 unregistered", (dut->ctx_reg_o >> 3) & 1, 0);

        uint8_t drops_before = dut->rx_drops_o;
        Vec v; v.fv = fv_talker(P_SID); v.evts = {EV_JOININ};
        feed_parked(bframe({msg_tadv(v)}), 3, 600);
        run(400);
        ck("[PARK] row 3 registers first-shot", (dut->ctx_reg_o >> 3) & 1, 1);
        ck("[PARK] row 3 ready first-shot", (dut->ctx_ready_o >> 3) & 1, 1);
        {
            uint64_t sid = 0;
            uint16_t st = ctx_read(3, &sid);
            ck("[PARK] status word: valid", (st >> 15) & 1, 1);
            ck("[PARK] status word: registered", (st >> 12) & 1, 1);
            ck("[PARK] status word: ready", (st >> 11) & 1, 1);
            ck("[PARK] status word: sid intact", sid, P_SID);
        }
        ck("[PARK] the PDU was not torn (no drop)",
           dut->rx_drops_o, drops_before);
        ctx_write(3, 0, 0, 0); run(400); drain_tx();
    }

    ck("final: no RX drops", dut->rx_drops_o, 0);
    ck("final: ctx MRPDUs were sent", dut->ctx_tx_count_o > 0, 1);

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
