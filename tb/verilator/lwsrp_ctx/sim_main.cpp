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

static std::vector<uint8_t> golden_legacy_msrp(bool talker, int dom_ev,
                                               int tk_ev, int lva) {
    std::vector<uint8_t> f;
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
    std::vector<uint8_t> f;
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
    std::vector<uint8_t> body;
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
    out.push_back((uint8_t)m.type);
    out.push_back((uint8_t)m.len);
    if (m.msrp) put_be(out, body.size(), 2);
    out.insert(out.end(), body.begin(), body.end());
    return out;
}

static std::vector<uint8_t> bframe(const std::vector<Msg>& msgs) {
    std::vector<uint8_t> f;
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
    std::vector<uint8_t> v; put_be(v, sid, 8); return v;
}
static std::vector<uint8_t> fv_talker(uint64_t sid) {
    std::vector<uint8_t> v; put_be(v, sid, 8);
    for (int i = 0; i < 17; i++) v.push_back(0xA0 + i);
    return v;
}
static std::vector<uint8_t> fv_tfail(uint64_t sid, uint8_t code) {
    auto v = fv_talker(sid);
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

// ---- context provisioning port -------------------------------------------
static void ctx_write(int idx, int valid, int dir, uint64_t sid,
                      uint64_t dmac = 0, uint8_t pr = 0x70,
                      uint16_t maxf = 0, uint16_t ivf = 0, uint32_t lat = 0) {
    dut->ctx_req_i = 1; dut->ctx_we_i = 1; dut->ctx_idx_i = idx;
    dut->ctx_valid_i = valid; dut->ctx_dir_i = dir; dut->ctx_sid_i = sid;
    dut->ctx_dmac_i = dmac; dut->ctx_prio_rank_i = pr;
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

    // 8) ONE bridge TalkerAdvertise vector covering BOTH listener rows
    //    (CRF at k=0, row 3 at k=2; k=1 is nobody)
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
        run(6600);
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

    ck("final: no RX drops", dut->rx_drops_o, 0);
    ck("final: ctx MRPDUs were sent", dut->ctx_tx_count_o > 0, 1);

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
