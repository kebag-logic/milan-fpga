/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_acmp_lstn_ctx at N_SINKS_P=4 with MIXED
 * per-context policies (PROBE_SM_EN_P=4'b0101, SID_EXPLICIT_P=4'b0110):
 *   ctx0 = {probe SM, derive sid}   — today's media sink 0
 *   ctx1 = {bind record, explicit}  — today's CRF sink 1
 *   ctx2 = {probe SM, explicit}     — NEW: fast-connect sid on an SM sink
 *   ctx3 = {bind record, derive}    — NEW: derive-policy record sink
 *
 * Proves the shared-SM + context-RAM design: per-uid responder, one timer
 * wheel over simultaneous probe ladders, per-context ADP watch + SRP edges,
 * the context-table request/grant port, and isolation between contexts
 * (disconnect of one leaves the others locked).
 *
 * Traceability (IEEE 1722.1-2021 / AVnu Milan v1.2):
 *   ACMP-2  8.2.1.4   per-uid CONNECT_RX/DISCONNECT_RX/GET_RX_STATE dispatch
 *   ACMP-3  8.2.1.5   LISTENER_UNKNOWN_ID for uid >= N
 *   ACMP-6  8.2.1.8-12 unique_id addressing (per-context routing)
 *   ACMP-10/M-ACMP-2  Table 5.26 timer ladder (shared wheel, scaled clock)
 *   M-ACMP-3 5.5.3    binding SM per context (Tables 5.28-5.30), rebind-same
 *                     vs rebind-different on an OCCUPIED sink
 *   M-ACMP-5 5.5.3.5  GET_RX_STATE per-state payload per uid (Tab 5.34/5.37)
 *   M-ACMP-10 5.5.1.2 explicit fast-connect stream_id per sink policy
 *                     (upgrades the 🟡 "sink-0 ignores the sid field" row:
 *                     the policy is now per-context config)
 */

#include "VKL_acmp_lstn_ctx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_acmp_lstn_ctx* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-52s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%llx exp=%llx\n", what,
                              (unsigned long long)got, (unsigned long long)exp); }
    else            { printf("  [ ok ] %-52s = %llx\n", what, (unsigned long long)got); }
}

static std::vector<uint8_t> partial;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}

static bool tick_collect(std::vector<uint8_t>* done) {
    bool got = false;
    dut->m_axis_tready = 1;
    dut->eval();
    if (dut->m_axis_tvalid) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_tkeep >> l) & 1)
                partial.push_back((dut->m_axis_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_tlast) {
            if (done) *done = partial;
            partial.clear();
            got = true;
        }
    }
    tick();
    return got;
}

static void run(int n) { for (int i = 0; i < n; i++) tick_collect(nullptr); }

static std::vector<uint8_t> wait_frame(int budget = 4000) {
    std::vector<uint8_t> f;
    for (int c = 0; c < budget; c++)
        if (tick_collect(&f)) return f;
    return {};
}

// ------------------------------------------------------------------ identity
static const uint64_t US_EID = 0x020000FFFE000003ULL;
static const uint8_t  US_MAC[6] = {0x02,0x00,0x00,0x00,0x00,0x03};
static const uint64_t CT_EID = 0x680500FFFE0000AAULL;
static const uint64_t T1_EID = 0x020000FFFE000001ULL;   // ctx0's talker
static const uint64_t T2_EID = 0x020000FFFE000002ULL;   // ctx2's talker
static const uint64_t T3_EID = 0x020000FFFE000004ULL;   // ctx3 / rebind
static const uint64_t T1_SID = 0x0200000000010000ULL;   // derive(T1, 0)

static void put_be(std::vector<uint8_t>& v, uint64_t x, int n) {
    for (int i = n-1; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}

static std::vector<uint8_t> acmp(uint8_t msg, uint8_t status,
                                 uint64_t sid, uint64_t ctlr, uint64_t talker,
                                 uint64_t lstnr, uint16_t tuid, uint16_t luid,
                                 const uint8_t* dmac, uint16_t seq,
                                 uint16_t flags, uint16_t vlan) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0xAA,0xBB,0xCC,0x00,0x00,0x01,
                              0x22,0xF0, 0xFC};
    f.push_back(msg & 0xF);
    f.push_back((status << 3) | 0);
    f.push_back(44);
    put_be(f, sid, 8);
    put_be(f, ctlr, 8);
    put_be(f, talker, 8);
    put_be(f, lstnr, 8);
    put_be(f, tuid, 2);
    put_be(f, luid, 2);
    for (int i = 0; i < 6; i++) f.push_back(dmac ? dmac[i] : 0);
    put_be(f, 0, 2);
    put_be(f, seq, 2);
    put_be(f, flags, 2);
    put_be(f, vlan, 2);
    put_be(f, 0, 2);
    return f;
}

static std::vector<uint8_t> adp(uint8_t msg, uint64_t eid) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0x02,0x00,0x00,0x00,0x00,0x01,
                              0x22,0xF0, 0xFA};
    f.push_back(msg & 0xF);
    f.push_back(0x1F); f.push_back(56);
    put_be(f, eid, 8);
    while (f.size() < 82) f.push_back(0);
    return f;
}

static void feed(const std::vector<uint8_t>& f) {
    int n = f.size();
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++)
            if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
        dut->rx_tvalid_i = 1;
        dut->rx_tdata_i  = d;
        dut->rx_tkeep_i  = keep;
        dut->rx_tlast_i  = (off + 8 >= n);
        tick_collect(nullptr);
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
    tick_collect(nullptr);
    tick_collect(nullptr);
}

static int r_msg(const std::vector<uint8_t>& b){ return b.size()>15 ? b[15]&0xF : -1; }
static int r_sta(const std::vector<uint8_t>& b){ return b.size()>16 ? b[16]>>3 : -1; }
static uint64_t r_be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++) v = (v << 8) | b[off+i];
    return v;
}

// ---------------------------------------------------------------- ctx table
// acmp_lstn_ctx_t packed offsets (LSB first): ctlr[63:0] talker[127:64]
// sid[191:128] dmac[239:192] vlan[251:240] flags[267:252] tuid[283:268]
// tmr[297:284] adp_age[304:298] status[309:305] probing[311:310]
// tk_avail[312] active[313] state[316:314]
static uint32_t ctxw[10];

static uint64_t cbits(int lo, int width) {
    uint64_t v = 0;
    for (int i = width - 1; i >= 0; i--) {
        int b = lo + i;
        v = (v << 1) | ((ctxw[b >> 5] >> (b & 31)) & 1);
    }
    return v;
}
static uint64_t c_ctlr()   { return cbits(0, 64); }
static uint64_t c_talker() { return cbits(64, 64); }
static uint64_t c_sid()    { return cbits(128, 64); }
static uint64_t c_dmac()   { return cbits(192, 48); }
static uint64_t c_vlan()   { return cbits(240, 12); }
static uint64_t c_flags()  { return cbits(252, 16); }
static uint64_t c_tuid()   { return cbits(268, 16); }
static uint64_t c_status() { return cbits(305, 5); }
static uint64_t c_probing(){ return cbits(310, 2); }
static uint64_t c_state()  { return cbits(314, 3); }

// request/grant read of one context record
static bool tbl_read(int idx) {
    dut->tbl_idx_i = idx;
    dut->tbl_req_i = 1;
    for (int c = 0; c < 100; c++) {
        tick();
        dut->eval();
        if (dut->tbl_gnt_o) {
            for (int w = 0; w < 10; w++) ctxw[w] = dut->tbl_ctx_o[w];
            dut->tbl_req_i = 0;
            tick();
            return true;
        }
    }
    dut->tbl_req_i = 0;
    return false;
}

// E1 bind-restore injection: hold req until the 1-cycle ack, return status
// (0 injected, 1 occupied, 2 bad idx / record-only context, -1 no ack)
static int rest_inject(int idx, uint64_t talker, uint16_t tuid,
                       uint64_t ctlr, uint16_t flags) {
    dut->rest_idx_i    = idx;
    dut->rest_talker_i = talker;
    dut->rest_tuid_i   = tuid;
    dut->rest_ctlr_i   = ctlr;
    dut->rest_flags_i  = flags;
    dut->rest_req_i    = 1;
    int st = -1;
    for (int c = 0; c < 200; c++) {
        tick();
        dut->eval();
        if (dut->rest_ack_o) { st = dut->rest_status_o; break; }
    }
    dut->rest_req_i = 0;
    tick();
    return st;
}

static const int MS = 10;   // scaled clock: 1 ms = 10 cycles

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_acmp_lstn_ctx;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->entity_id_i = US_EID;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|US_MAC[i]; dut->station_mac_i = m; }
    dut->tick_1s_i = 0;
    dut->ta_registered_i = 0; dut->ta_failed_i = 0;
    dut->tbl_req_i = 0; dut->tbl_idx_i = 0;
    dut->rest_req_i = 0; dut->rest_idx_i = 0;
    dut->rest_talker_i = 0; dut->rest_tuid_i = 0;
    dut->rest_ctlr_i = 0; dut->rest_flags_i = 0;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();   // covers the ctx-RAM init walk

    printf("== KL_acmp_lstn_ctx N=4, mixed sid/SM policies ==\n");

    // ---------------------------------------------------------------- //
    printf("\n[N1] GET_RX_STATE per uid after reset; uid>=N refused\n");
    for (int uid = 0; uid < 4; uid++) {
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, uid, nullptr, 0x100+uid, 0, 0));
        auto r = wait_frame();
        ck("[N1] GET answered", r.size(), 70);
        ck("[N1] msg GET_RX_STATE_RESPONSE", r_msg(r), 11);
        ck("[N1] SUCCESS", r_sta(r), 0);
        ck("[N1] count 0", (long)r_be(r, 60, 2), 0);
        ckh("[N1] talker 0", r_be(r, 34, 8), 0);
    }
    {
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 4, nullptr, 0x104, 0, 0));
        auto r = wait_frame();
        ck("[N1] uid4 LISTENER_UNKNOWN_ID (ACMP-3)", r_sta(r), 1);
        feed(acmp(6, 0, 0, CT_EID, T1_EID, US_EID, 0, 5, nullptr, 0x105, 0, 0));
        r = wait_frame();
        ck("[N1] BIND uid5 LISTENER_UNKNOWN_ID", r_sta(r), 1);
        tbl_read(0);
        ck("[N1] ctx0 untouched by refused bind", (long)c_state(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[N2] mixed-policy binds (M-ACMP-10 per-context sid policy)\n");
    const uint8_t dm1[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x01};
    const uint8_t dm2[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
    const uint64_t S1E = 0x1111222233330001ULL;   // explicit sid for ctx1
    const uint64_t S2E = 0x4444555566660002ULL;   // explicit sid for ctx2
    const uint64_t SJ  = 0x7777888899990003ULL;   // junk sid (must be ignored)

    // ctx0 {SM, derive}: explicit sid in the command is IGNORED (today's
    // sink-0 policy, kept by config)
    feed(acmp(6, 0, SJ, CT_EID, T1_EID, US_EID, 0, 0, nullptr, 0x200, 0, 0));
    auto r = wait_frame();
    ck("[N2] ctx0 BIND_RESP", r_msg(r), 7);
    ck("[N2] ctx0 SUCCESS count 1", (long)r_be(r, 60, 2), 1);
    auto p0 = wait_frame();
    ck("[N2] ctx0 PROBE_TX follows", p0.size(), 70);
    ck("[N2] ctx0 probe luid 0", (long)r_be(p0, 52, 2), 0);
    ckh("[N2] ctx0 probe talker T1", r_be(p0, 34, 8), T1_EID);
    long seq_p0 = (long)r_be(p0, 62, 2);
    tbl_read(0);
    ck("[N2] ctx0 state PRB_W_RESP", (long)c_state(), 3);
    ckh("[N2] ctx0 sid DERIVED (junk sid ignored)", c_sid(), T1_SID);

    // ctx1 {record, explicit}: nonzero command sid IS the stream
    feed(acmp(6, 0, S1E, CT_EID, T1_EID, US_EID, 0x000B, 1, dm1, 0x201, 0, 0));
    r = wait_frame();
    ck("[N2] ctx1 BIND_RESP SUCCESS", r_sta(r), 0);
    tbl_read(1);
    ck("[N2] ctx1 parked settled (record)", (long)c_state(), 6);
    ckh("[N2] ctx1 sid EXPLICIT", c_sid(), S1E);
    ckh("[N2] ctx1 dmac from command", c_dmac(), 0x91E0F0002A01ULL);
    ck("[N2] ctx1 no probe SM: no new probe", dut->probe_count_o, 1);
    ck("[N2] ctx1 never activates (no MSRP)",
       (dut->stream_active_o >> 1) & 1, 0);

    // ctx2 {SM, explicit}: fast-connect sid honoured on an SM sink (NEW —
    // the M-ACMP-10 upgrade), probe still runs and stays authoritative
    feed(acmp(6, 0, S2E, CT_EID, T2_EID, US_EID, 0, 2, dm2, 0x202, 0, 0));
    r = wait_frame();
    ck("[N2] ctx2 BIND_RESP SUCCESS", r_sta(r), 0);
    auto p2 = wait_frame();
    ck("[N2] ctx2 PROBE_TX follows", p2.size(), 70);
    ck("[N2] ctx2 probe luid 2 (response routing)", (long)r_be(p2, 52, 2), 2);
    ckh("[N2] ctx2 probe talker T2", r_be(p2, 34, 8), T2_EID);
    long seq_p2 = (long)r_be(p2, 62, 2);
    ck("[N2] shared probe_seq distinct", seq_p2 != seq_p0, 1);
    tbl_read(2);
    ck("[N2] ctx2 state PRB_W_RESP", (long)c_state(), 3);
    ckh("[N2] ctx2 provisional sid EXPLICIT", c_sid(), S2E);

    // ctx3 {record, derive}: explicit sid in the command is ignored
    feed(acmp(6, 0, SJ, CT_EID, T3_EID, US_EID, 0x0007, 3, nullptr, 0x203, 0, 0));
    r = wait_frame();
    ck("[N3] ctx3 BIND_RESP SUCCESS", r_sta(r), 0);
    tbl_read(3);
    ck("[N2] ctx3 parked settled (record)", (long)c_state(), 6);
    ckh("[N2] ctx3 sid DERIVED (policy over payload)", c_sid(),
        0x0200000000040007ULL);   // {T3 mac (FFFE-squeezed), tuid 7}

    // ---------------------------------------------------------------- //
    printf("\n[N3] one timer wheel, two live ladders (M-ACMP-2 Tab 5.26)\n");
    // answer ctx2's probe -> settles; ctx0's NO_RESP keeps running
    {
        const uint8_t dmS[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x22};
        feed(acmp(1, 0, S2E, CT_EID, T2_EID, US_EID, 0, 2, dmS, 0, 0, 2));
    }
    tbl_read(2);
    ck("[N3] ctx2 SETTLED_NO_RSV", (long)c_state(), 6);
    ck("[N3] ctx2 active (bit 2)", (dut->stream_active_o >> 2) & 1, 1);
    ck("[N3] ctx0 not active", dut->stream_active_o & 1, 0);
    // only ctx0 resends at 200 ms (ctx2's timer was cancelled)
    auto pr = wait_frame(250 * MS);
    ck("[N3] exactly ctx0 resends", pr.size(), 70);
    ck("[N3] resend luid 0", (long)r_be(pr, 52, 2), 0);
    ckh("[N3] resend talker T1", r_be(pr, 34, 8), T1_EID);
    pr = wait_frame(250 * MS);
    ck("[N3] no further frame (ctx2 quiet)", pr.size(), 0);
    tbl_read(0);
    ck("[N3] ctx0 PRB_W_RETRY", (long)c_state(), 5);
    ck("[N3] ctx0 status LISTENER_TALKER_TIMEOUT", (long)c_status(), 7);
    tbl_read(2);
    ck("[N3] ctx2 still settled", (long)c_state(), 6);

    // ---------------------------------------------------------------- //
    printf("\n[N4] CONNECT to an OCCUPIED sink (M-ACMP-3 rebind rules)\n");
    long pc = dut->probe_count_o;
    // same talker + matching flags -> SUCCESS response only, no disturbance
    feed(acmp(6, 0, 0, CT_EID, T2_EID, US_EID, 0, 2, nullptr, 0x300, 0, 0));
    r = wait_frame();
    ck("[N4] rebind-same SUCCESS", r_sta(r), 0);
    ck("[N4] no new probe", dut->probe_count_o, pc);
    tbl_read(2);
    ck("[N4] ctx2 state undisturbed", (long)c_state(), 6);
    ck("[N4] ctx2 still active", (dut->stream_active_o >> 2) & 1, 1);
    // different talker -> SUCCESS + teardown/re-probe (Milan rebind)
    feed(acmp(6, 0, 0, CT_EID, T3_EID, US_EID, 0, 2, nullptr, 0x301, 0, 0));
    r = wait_frame();
    ck("[N4] rebind-diff SUCCESS", r_sta(r), 0);
    auto p3 = wait_frame();
    ck("[N4] probe to the new talker", p3.size(), 70);
    ckh("[N4] probe talker T3", r_be(p3, 34, 8), T3_EID);
    ck("[N4] probe luid 2", (long)r_be(p3, 52, 2), 2);
    ck("[N4] deactivated on rebind", (dut->stream_active_o >> 2) & 1, 0);
    tbl_read(2);
    ck("[N4] ctx2 PRB_W_RESP", (long)c_state(), 3);
    ckh("[N4] ctx2 sid re-derived (zero cmd sid)",
        c_sid(), 0x0200000000040000ULL);
    // per-context SRP_REG_FAILED sourcing while probing (ACMP-8)
    dut->ta_failed_i = (1 << 2);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 2, nullptr, 0x302, 0, 0));
    r = wait_frame();
    ck("[N4] GET flags SW|SRP_REG_FAILED (ctx2 srf)", (long)r_be(r, 64, 2), 0x0048);
    dut->ta_failed_i = 0;
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x303, 0, 0));
    r = wait_frame();
    ck("[N4] ctx0 GET flags SW only (srf is per-ctx)", (long)r_be(r, 64, 2), 0x0008);

    // settle ctx2 on T3 for the following sections
    feed(acmp(1, 0, 0x0200000000040000ULL, CT_EID, T3_EID, US_EID, 0, 2,
              nullptr, 1, 0, 2));
    tbl_read(2);
    ck("[N4] ctx2 re-settled on T3", (long)c_state(), 6);

    // ---------------------------------------------------------------- //
    printf("\n[N5] GET_RX_STATE per uid (M-ACMP-5 Table 5.37)\n");
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x400, 0, 0));
    r = wait_frame();
    ckh("[N5] uid0 talker T1", r_be(r, 34, 8), T1_EID);
    ck("[N5] uid0 count 1", (long)r_be(r, 60, 2), 1);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x401, 0, 0));
    r = wait_frame();
    ckh("[N5] uid1 talker T1", r_be(r, 34, 8), T1_EID);
    ck("[N5] uid1 tuid 0xB", (long)r_be(r, 50, 2), 0x000B);
    ckh("[N5] uid1 dmac (record)", r_be(r, 54, 6), 0x91E0F0002A01ULL);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 2, nullptr, 0x402, 0, 0));
    r = wait_frame();
    ckh("[N5] uid2 talker T3", r_be(r, 34, 8), T3_EID);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 3, nullptr, 0x403, 0, 0));
    r = wait_frame();
    ckh("[N5] uid3 talker T3", r_be(r, 34, 8), T3_EID);
    ck("[N5] uid3 tuid 7", (long)r_be(r, 50, 2), 0x0007);

    // ---------------------------------------------------------------- //
    printf("\n[N6] DISCONNECT one context leaves the others locked\n");
    feed(acmp(8, 0, 0, CT_EID, T1_EID, US_EID, 0x000B, 1, nullptr, 0x500, 0, 0));
    r = wait_frame();
    ck("[N6] ctx1 UNBIND_RESP SUCCESS", r_sta(r), 0);
    tbl_read(1);
    ck("[N6] ctx1 unbound", (long)c_state(), 0);
    ckh("[N6] ctx1 record cleared", c_talker(), 0);
    tbl_read(0);
    ck("[N6] ctx0 still bound (RETRY)", (long)c_state(), 5);
    ckh("[N6] ctx0 talker intact", c_talker(), T1_EID);
    tbl_read(2);
    ck("[N6] ctx2 still settled", (long)c_state(), 6);
    tbl_read(3);
    ck("[N6] ctx3 still bound", (long)c_state(), 6);
    ckh("[N6] ctx3 talker intact", c_talker(), T3_EID);
    ck("[N6] ctx2 activity survives the unbind",
       (dut->stream_active_o >> 2) & 1, 1);

    // ---------------------------------------------------------------- //
    printf("\n[N7] per-context SRP edges (M-ACMP-3 registered/failed)\n");
    dut->ta_registered_i = (1 << 2);
    run(8);
    tbl_read(2);
    ck("[N7] ctx2 SETTLED_RSV_OK", (long)c_state(), 7);
    ck("[N7] ctx2 declares (bit 2)", (dut->lstn_declare_o >> 2) & 1, 1);
    tbl_read(0);
    ck("[N7] ctx0 unaffected by ctx2's registrar", (long)c_state(), 5);
    dut->ta_failed_i = (1 << 2);
    run(8);
    tbl_read(2);
    ck("[N7] ctx2 degraded to SETTLED_NO_RSV", (long)c_state(), 6);
    dut->ta_failed_i = 0;
    run(8);
    tbl_read(2);
    ck("[N7] level alone does not re-establish", (long)c_state(), 6);
    // re-registration EDGE re-establishes (single-sink [6] semantics)
    dut->ta_registered_i = 0;
    run(8);
    dut->ta_registered_i = (1 << 2);
    run(8);
    tbl_read(2);
    ck("[N7] ctx2 back to RSV_OK (fresh edge via wheel)", (long)c_state(), 7);

    // ---------------------------------------------------------------- //
    printf("\n[N8] per-context ADP watch (M-ACMP-3 talker discovery)\n");
    // let ctx0's 4 s RETRY lapse -> talker invisible -> PRB_W_AVAIL
    run(4200 * MS);
    tbl_read(0);
    ck("[N8] ctx0 PRB_W_AVAIL after RETRY", (long)c_state(), 1);
    // T1 becomes ADP-visible: ONLY ctx0 reacts (ctx2/ctx3 other talkers)
    feed(adp(0, T1_EID));
    run(8);
    tbl_read(0);
    ck("[N8] ctx0 tk_avail -> PRB_W_DELAY", (long)c_state(), 2);
    tbl_read(2);
    ck("[N8] ctx2 untouched by T1's ADP", (long)c_state(), 7);
    tbl_read(3);
    ck("[N8] ctx3 untouched (record ctx has no watch)", (long)c_state(), 6);
    auto pd = wait_frame(1100 * MS);
    ck("[N8] ctx0 re-probes after the delay", pd.size(), 70);
    ck("[N8] re-probe luid 0", (long)r_be(pd, 52, 2), 0);
    ckh("[N8] re-probe talker T1", r_be(pd, 34, 8), T1_EID);

    // ---------------------------------------------------------------- //
    printf("\n[N9] bind-restore injection (E1, Milan 5.5.3.5.2)\n");
    // free ctx0 first: a controller unbind clears the saved state (5.5.1.3)
    feed(acmp(8, 0, 0, CT_EID, T1_EID, US_EID, 0, 0, nullptr, 0x600, 0, 0));
    r = wait_frame();
    ck("[N9] ctx0 UNBIND SUCCESS", r_sta(r), 0);
    tbl_read(0);
    ck("[N9] ctx0 unbound", (long)c_state(), 0);
    // inject the saved bind: talker T2, tuid 5, ctlr, STREAMING_WAIT flag
    ck("[N9] inject accepted (status 0)",
       rest_inject(0, T2_EID, 0x0005, CT_EID, 0x0008), 0);
    tbl_read(0);
    ck("[N9] state PRB_W_AVAIL (5.5.3.5.2 step 3)", (long)c_state(), 1);
    ck("[N9] probing PASSIVE (step 2)", (long)c_probing(), 1);
    ck("[N9] ACMP status 0 (step 2)", (long)c_status(), 0);
    ckh("[N9] talker loaded", c_talker(), T2_EID);
    ck("[N9] tuid loaded", (long)c_tuid(), 5);
    ckh("[N9] ctlr loaded (5.5.3.5.3)", c_ctlr(), CT_EID);
    ck("[N9] flags STREAMING_WAIT kept", (long)c_flags(), 0x0008);
    ckh("[N9] sid CLEARED (5.5.2.6 step 1)", c_sid(), 0);
    ckh("[N9] dmac CLEARED", c_dmac(), 0);
    ck("[N9] vlan CLEARED", (long)c_vlan(), 0);
    ck("[N9] sink not active", dut->stream_active_o & 1, 0);
    // refusals: occupied context / record-only context / index >= N
    ck("[N9] restore to OCCUPIED refused (1)",
       rest_inject(2, T3_EID, 0, CT_EID, 0), 1);
    tbl_read(2);
    ck("[N9] occupied ctx undisturbed", (long)c_state(), 7);
    ck("[N9] record-only ctx refused (2)",
       rest_inject(1, T3_EID, 0, CT_EID, 0), 2);
    ck("[N9] idx >= N refused (2)",
       rest_inject(9, T3_EID, 0, CT_EID, 0), 2);
    tbl_read(0);
    ck("[N9] refusals left the injected record", (long)c_state(), 1);
    // the talker's ENTITY_AVAILABLE arrives (5.5.1.4: wait for the talker's
    // ADPDU) -> the EXISTING ladder takes over: DELAY -> PROBE_TX
    feed(adp(0, T2_EID));
    run(8);
    tbl_read(0);
    ck("[N9] EVT_TK_DISCOVERED -> PRB_W_DELAY", (long)c_state(), 2);
    auto p9 = wait_frame(1100 * MS);
    ck("[N9] PROBE_TX after the delay", p9.size(), 70);
    ckh("[N9] probe talker = restored talker", r_be(p9, 34, 8), T2_EID);
    ck("[N9] probe tuid = restored tuid", (long)r_be(p9, 50, 2), 5);
    ckh("[N9] probe ctlr = restored ctlr", r_be(p9, 26, 8), CT_EID);
    // the talker's PROBE_TX_RESPONSE completes the bind (SM behaviour):
    // sid/dmac/vlan re-learned from the wire, sink settles
    {
        const uint8_t dmR[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x99};
        feed(acmp(1, 0, 0x1234432112344321ULL, CT_EID, T2_EID, US_EID, 5, 0,
                  dmR, 2, 0, 2));
    }
    tbl_read(0);
    ck("[N9] settled after the probe response", (long)c_state(), 6);
    ckh("[N9] sid re-learned from the probe", c_sid(), 0x1234432112344321ULL);
    ckh("[N9] dmac re-learned", c_dmac(), 0x91E0F000FE99ULL);
    ck("[N9] sink active", dut->stream_active_o & 1, 1);

    printf("\nKL_acmp_lstn_ctx N=4: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
