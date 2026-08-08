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

//! t21 bind view: per-context bound stream_id lane (lstn_sid_o is
//! N_SINKS_P*64 wide -> VlWide, two 32-bit words per lane)
static uint64_t sidv(int k) {
    return ((uint64_t)dut->lstn_sid_o[2*k+1] << 32) | dut->lstn_sid_o[2*k];
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
static const uint64_t CT2_EID= 0x680500FFFE0000BBULL;   // foreign controller
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

// byte 16 [7:3] = valid_time (2 s units); vt 3 = the historical 0x1F field.
// available_index (wire 50-53) defaults to a MONOTONIC counter — Milan
// 5.6.4.5.2 step 2 wipes availability on a non-increasing index, so a
// repeated constant would undo the discovery the caller just set up.
// gm (wire 54-61) / dom (wire 62) feed the 5.6.4.5.1 step 1 gate.
static uint32_t g_avidx = 0;
static std::vector<uint8_t> adp(uint8_t msg, uint64_t eid, uint8_t vt = 3,
                                uint64_t gm = 0, uint8_t dom = 0,
                                uint32_t aidx = 0xFFFFFFFF) {
    if (aidx == 0xFFFFFFFF) aidx = ++g_avidx;
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0x02,0x00,0x00,0x00,0x00,0x01,
                              0x22,0xF0, 0xFA};
    f.push_back(msg & 0xF);
    f.push_back((uint8_t)(vt << 3)); f.push_back(56);
    put_be(f, eid, 8);
    while (f.size() < 50) f.push_back(0);
    put_be(f, aidx, 4);
    put_be(f, gm, 8);
    f.push_back(dom);
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
// tk_avail[312] active[313] state[316:314] adp_vt[321:317] seq[337:322]
// last_avail[369:338]
// (adp_vt + seq + last_avail joined at the struct MSBs across the 0x0035/
// B2h rounds, 317 -> 338 -> 370 bits, so every pre-existing offset above
// is unchanged — the [N10]/[B2c]/[B2h] pins below hold the map)
static uint32_t ctxw[12];

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
static uint64_t c_advt()   { return cbits(317, 5); }
static uint64_t c_seq()    { return cbits(322, 16); }
static uint64_t c_lastav() { return cbits(338, 32); }

// request/grant read of one context record
static bool tbl_read(int idx) {
    dut->tbl_idx_i = idx;
    dut->tbl_req_i = 1;
    for (int c = 0; c < 100; c++) {
        tick();
        dut->eval();
        if (dut->tbl_gnt_o) {
            for (int w = 0; w < 12; w++) ctxw[w] = dut->tbl_ctx_o[w];
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
    dut->locked_i = 0; dut->lock_ctlr_i = 0;
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
    printf("\n[L] locked-entity law (Milan 5.5.3.5 step 1; Tables 5.31/35)\n");
    // While the AECP entity lock is held, BIND_RX/UNBIND_RX from any other
    // controller answers CONTROLLER_NOT_AUTHORIZED with a FULL command
    // echo and changes nothing; GET_RX_STATE clauses have no lock step, so
    // reads pass; the locking controller itself is never refused.
    {
        const uint8_t dmL[6] = {0x91,0xE0,0xF0,0x00,0xAB,0xCD};
        const uint64_t SJL   = 0x1357246813572468ULL;
        long pcL = dut->probe_count_o;
        dut->locked_i = 1; dut->lock_ctlr_i = CT_EID;
        // foreign BIND: refused 16, every named field = command echo
        feed(acmp(6, 0, SJL, CT2_EID, T1_EID, US_EID, 0x0001, 0, dmL,
                  0x150, 0x000A, 0xABC));
        auto r = wait_frame();
        ck("[L] foreign BIND refused CONTROLLER_NOT_AUTHORIZED",
           r_sta(r), 16);
        ck("[L] refusal msg BIND_RESP", r_msg(r), 7);
        ckh("[L] refusal ctlr echo", r_be(r, 26, 8), CT2_EID);
        ckh("[L] refusal talker echo", r_be(r, 34, 8), T1_EID);
        ck("[L] refusal tuid echo", (long)r_be(r, 50, 2), 1);
        ckh("[L] refusal stream_id echo", r_be(r, 18, 8), SJL);
        ckh("[L] refusal dmac echo", r_be(r, 54, 6), 0x91E0F000ABCDULL);
        ck("[L] refusal flags echo", (long)r_be(r, 64, 2), 0x000A);
        ck("[L] refusal vlan echo", (long)r_be(r, 66, 2), 0xABC);
        ck("[L] refusal count echo", (long)r_be(r, 60, 2), 0);
        ck("[L] refusal seq echo", (long)r_be(r, 62, 2), 0x150);
        tbl_read(0);
        ck("[L] record untouched", (long)c_state(), 0);
        ck("[L] no probe launched", dut->probe_count_o, pcL);
        // foreign UNBIND: refused 16
        feed(acmp(8, 0, 0, CT2_EID, 0, US_EID, 0, 0, nullptr, 0x151, 0, 0));
        r = wait_frame();
        ck("[L] foreign UNBIND refused 16", r_sta(r), 16);
        ck("[L] refusal msg UNBIND_RESP", r_msg(r), 9);
        // foreign GET: exempt (no lock step in any RCV_GET_RX_STATE clause)
        feed(acmp(10, 0, 0, CT2_EID, 0, US_EID, 0, 0, nullptr, 0x152, 0, 0));
        r = wait_frame();
        ck("[L] foreign GET_RX_STATE exempt (SUCCESS)", r_sta(r), 0);
        // the LOCKING controller binds through the lock
        feed(acmp(6, 0, 0, CT_EID, T1_EID, US_EID, 0, 0, nullptr,
                  0x153, 0, 0));
        r = wait_frame();
        ck("[L] locking controller BIND SUCCESS", r_sta(r), 0);
        (void)wait_frame();                        // its PROBE_TX
        tbl_read(0);
        ck("[L] locking controller's bind took", (long)c_state(), 3);
        // foreign GET on the bound sink still exempt
        feed(acmp(10, 0, 0, CT2_EID, 0, US_EID, 0, 0, nullptr, 0x154, 0, 0));
        r = wait_frame();
        ck("[L] foreign GET on bound sink exempt", r_sta(r), 0);
        ck("[L] ...and served (count 1)", (long)r_be(r, 60, 2), 1);
        // unlock releases: the foreign UNBIND now succeeds
        dut->locked_i = 0; dut->lock_ctlr_i = 0;
        feed(acmp(8, 0, 0, CT2_EID, T1_EID, US_EID, 0, 0, nullptr,
                  0x155, 0, 0));
        r = wait_frame();
        ck("[L] unlock releases: foreign UNBIND SUCCESS", r_sta(r), 0);
        tbl_read(0);
        ck("[L] unbound again", (long)c_state(), 0);
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
    long pc_n2  = dut->probe_count_o;
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
    // t21 bind view (the datapath's lwSRP listener-row provisioner input):
    // a record-only bind raises bound and exposes the bound sid, LIVE
    ck("[N2] ctx1 bind view: BOUND", (dut->lstn_bound_o >> 1) & 1, 1);
    ckh("[N2] ctx1 bind view: the bound sid", sidv(1), S1E);
    ck("[N2] ctx0 bind view: bound too (probing is bound)",
       dut->lstn_bound_o & 1, 1);
    ck("[N2] ctx1 no probe SM: no new probe", dut->probe_count_o, pc_n2);
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
    // answer ctx2's probe -> settles; ctx0's NO_RESP keeps running. The
    // response must echo ctx2's probe fields incl. sequence_id (5.5.3.5.18)
    {
        const uint8_t dmS[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x22};
        feed(acmp(1, 0, S2E, CT_EID, T2_EID, US_EID, 0, 2, dmS,
                  (uint16_t)seq_p2, 0, 2));
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
    //! the resend is a DUPLICATE of probe #1 (5.5.3.5.16): same seq
    ck("[N3] resend reuses ctx0's sequence_id", (long)r_be(pr, 62, 2),
       seq_p0);
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
    // same talker with STREAMING_WAIT toggled: Milan 5.5.3.5.43 step 2 =
    // refresh ctlr + STREAMING_WAIT in place, still no teardown/re-probe
    feed(acmp(6, 0, 0, CT_EID, T2_EID, US_EID, 0, 2, nullptr, 0x310, 0x0008, 0));
    r = wait_frame();
    ck("[N4] rebind-same(SW=1) SUCCESS", r_sta(r), 0);
    ck("[N4] SW-toggle: still no new probe", dut->probe_count_o, pc);
    ck("[N4] SW-toggle: ctx2 still active", (dut->stream_active_o >> 2) & 1, 1);
    tbl_read(2);
    ck("[N4] SW-toggle: state undisturbed", (long)c_state(), 6);
    ck("[N4] stored SW refreshed (step 2)", (long)(c_flags() & 0x8), 0x8);
    // different talker -> SUCCESS + teardown/re-probe (Milan rebind,
    // 5.5.3.5.43 steps 3..12 - NOT 1722.1's LISTENER_EXCLUSIVE refusal)
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
    ck("[N4] status cleared (5.5.3.5.43 step 11)", (long)c_status(), 0);
    ckh("[N4] stale T2 dmac cleared (5.5.2.6 step 1)", c_dmac(), 0);
    ck("[N4] stale T2 vlan cleared", (long)c_vlan(), 0);
    ck("[N4] fresh-bind flags (SW back to cmd's 0)", (long)c_flags(), 0);
    // Table 5.37: a PROBING state's GET reports FC 1, the saved SW and
    // REGISTERING_FAILED 0 — even with the TalkerFailed registrar HIGH
    // (RF is a Table 5.39 / SETTLED_RSV_OK field only)
    dut->ta_failed_i = (1 << 2);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 2, nullptr, 0x302, 0, 0));
    r = wait_frame();
    ck("[N4] probing GET flags FC only, RF=0 (Tab 5.37)",
       (long)r_be(r, 64, 2), 0x0002);
    dut->ta_failed_i = 0;
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x303, 0, 0));
    r = wait_frame();
    ck("[N4] ctx0 (RETRY) GET flags FC only", (long)r_be(r, 64, 2), 0x0002);

    // settle ctx2 on T3 for the following sections (probe-seq echoed)
    feed(acmp(1, 0, 0x0200000000040000ULL, CT_EID, T3_EID, US_EID, 0, 2,
              nullptr, (uint16_t)r_be(p3, 62, 2), 0, 2));
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
    //! Table 5.38: the settled stream_id is the RECORD's, not the echo of
    //! the command's zeros
    ckh("[N5] uid1 stream_id (record, Table 5.38)", r_be(r, 18, 8), S1E);
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
    //! 5.5.3.5.39/.45 "Stop the ADP Discovery SM": the availability view
    //! clears with the record — nothing for a future bind to inherit
    ck("[N6] ctx1 tk_avail cleared", (long)cbits(312, 1), 0);
    ck("[N6] ctx1 adp_age cleared", (long)cbits(298, 7), 0);
    // t21 bind view: the unbind drops bound and zeroes the sid lane, so
    // the downstream lwSRP listener-row provisioner withdraws its row
    ck("[N6] ctx1 bind view: bound CLEARED", (dut->lstn_bound_o >> 1) & 1, 0);
    ckh("[N6] ctx1 bind view: sid cleared", sidv(1), 0);
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
    printf("\n[N7] per-context SRP edges: the COMBINED attribute law\n");
    // Table 5.29: EVT_TK_REGISTERED/_UNREGISTERED are single edges of the
    // combined (Advertise | Failed) registration. Advertise <-> Failed
    // flips while registered are NO event (Table 5.30 marks them "x"), so
    // a settled sink RIDES them out in RSV_OK — the old per-attribute
    // edges invented an RSV_OK -> NO_RSV arc here.
    dut->ta_registered_i = (1 << 2);
    run(8);
    tbl_read(2);
    ck("[N7] ctx2 SETTLED_RSV_OK", (long)c_state(), 7);
    ck("[N7] ctx2 declares (bit 2)", (dut->lstn_declare_o >> 2) & 1, 1);
    tbl_read(0);
    ck("[N7] ctx0 unaffected by ctx2's registrar", (long)c_state(), 5);
    dut->ta_failed_i = (1 << 2);        // TF rise, TA held: no event
    run(8);
    tbl_read(2);
    ck("[N7] TF-rise while settled STAYS RSV_OK", (long)c_state(), 7);
    dut->ta_registered_i = 0;           // TA fall, TF holds: no event
    run(8);
    tbl_read(2);
    ck("[N7] TA-fall with TF held: still RSV_OK", (long)c_state(), 7);
    dut->ta_registered_i = (1 << 2);    // TA back: still registered
    run(8);
    dut->ta_failed_i = 0;               // TF away: still registered
    run(8);
    tbl_read(2);
    ck("[N7] never unregistered: RSV_OK held", (long)c_state(), 7);
    ck("[N7] ctx2 still active through the flips",
       (dut->stream_active_o >> 2) & 1, 1);

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
    ck("[N9] probe seq CLEARED", (long)c_seq(), 0);
    ck("[N9] adp valid_time CLEARED", (long)c_advt(), 0);
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
                  dmR, (uint16_t)r_be(p9, 62, 2), 0, 2));
    }
    tbl_read(0);
    ck("[N9] settled after the probe response", (long)c_state(), 6);
    ckh("[N9] sid re-learned from the probe", c_sid(), 0x1234432112344321ULL);
    ckh("[N9] dmac re-learned", c_dmac(), 0x91E0F000FE99ULL);
    ck("[N9] sink active", dut->stream_active_o & 1, 1);

    // ---------------------------------------------------------------- //
    printf("\n[B1] MSRPDU-ordering race: attribute flips must never wedge\n");
    // THE WEDGE (gh #54 B1b): switch relays the TalkerFailed JoinIn in an
    // EARLIER sweep pass than the TalkerAdvertise leave. The old RTL's
    // invented fail_rise arc landed RSV_OK -> NO_RSV with tmr=0; NO_RSV's
    // only exits are a fresh TA rise or an ARMED timer, so the sink sat
    // disarmed forever (recovery only by UNBIND / full TA cycle). Combined-
    // attribute edges (Table 5.29/5.30) ride the flips out in RSV_OK and
    // leave on the true unregistration, with the ladder ADVANCING.
    {
        dut->ta_registered_i |= 1;              // TA rise: NO_RSV -> RSV_OK
        run(8);
        tbl_read(0);
        ck("[B1] TA rise: RSV_OK", (long)c_state(), 7);
        dut->ta_failed_i |= 1;                  // TF JoinIn first...
        run(8);
        tbl_read(0);
        ck("[B1] TF-rise while settled: STAYS RSV_OK", (long)c_state(), 7);
        dut->ta_registered_i &= ~1u;            // ...then the TA leave
        run(8);
        tbl_read(0);
        ck("[B1] TA leave with TF held: STAYS RSV_OK", (long)c_state(), 7);
        dut->ta_failed_i &= ~1u;                // TF leave: NOW unregistered
        run(8);
        tbl_read(0);
        ck("[B1] combined fall exits settled (no wedge)", (long)c_state(), 2);
        ck("[B1] deactivated", dut->stream_active_o & 1, 0);
        ck("[B1] declare withdrawn", dut->lstn_declare_o & 1, 0);
        //! 5.5.3.5.48 step 1 + 5.3.8.9: the FULL SRP-parameter clear on
        //! the way out — sid included, and the bind-view sid lane (the
        //! datapath provisioner's |sid want-guard input) follows it
        ckh("[B1] dmac cleared on exit", c_dmac(), 0);
        ck("[B1] vlan cleared on exit", (long)c_vlan(), 0);
        ckh("[B1] sid zeroed on exit (5.3.8.9)", c_sid(), 0);
        ckh("[B1] bind-view sid lane zeroed with it", sidv(0), 0);
        long pcw = dut->probe_count_o;
        auto pw = wait_frame(1100 * MS);        // the ladder ADVANCES
        ck("[B1] re-probe emitted (ladder alive)", pw.size(), 70);
        ck("[B1] re-probe is ctx0's", (long)r_be(pw, 52, 2), 0);
        ck("[B1] probe_count advanced", (long)dut->probe_count_o - pcw, 1);

        // ---- TF-ALONE promotion (Table 5.29 "either ... or") ----------
        // settle again, then a TalkerFailed registration ALONE promotes to
        // RSV_OK (flags report FC | saved SW | REGISTERING_FAILED) and no
        // probe churn follows for 12 s (the NO_TK timer was cleared).
        {
            const uint8_t dmW[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x9A};
            feed(acmp(1, 0, 0x1234432112344321ULL, CT_EID, T2_EID, US_EID,
                      5, 0, dmW, (uint16_t)r_be(pw, 62, 2), 0, 2));
        }
        tbl_read(0);
        ck("[B1] re-settled NO_RSV", (long)c_state(), 6);
        dut->ta_failed_i |= 1;                  // TF-alone rise
        run(8);
        tbl_read(0);
        ck("[B1] TF-alone PROMOTES to RSV_OK (Tab 5.29)", (long)c_state(), 7);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x700, 0, 0));
        r = wait_frame();
        ck("[B1] flags FC|SW|REGISTERING_FAILED (Tab 5.39)",
           (long)r_be(r, 64, 2), 0x004A);
        auto quiet = wait_frame(12000 * MS);
        ck("[B1] no probe churn for 12 s", quiet.size(), 0);
        tbl_read(0);
        ck("[B1] still RSV_OK after 12 s", (long)c_state(), 7);
        dut->ta_failed_i &= ~1u;                // true unregistration
        run(8);
        auto pz = wait_frame(1100 * MS);        // DELAY -> probe (drain)
        ck("[B1] exit re-probes", pz.size(), 70);
        feed(acmp(8, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x701, 0, 0));
        (void)wait_frame();                     // UNBIND_RESP
        tbl_read(0);
        ck("[B1] ctx0 parked UNBOUND", (long)c_state(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[N10] probe-response accept vs arrival phase (ax-rv32-g return"
           " leg)\n");
    // THE SILICON SHAPE, 2026-08-05: the peer answered EVERY probe within
    // 1.4 ms with a flawless PROBE_TX_RESPONSE (sid == its entity id, a MAAP
    // dmac, vlan 2), yet ACMPL_STATE took MINUTES of 500 ms retries to reach
    // probing=COMPLETED - most responses were lost somewhere between capture
    // and accept.  This sweeps the response's arrival phase against the
    // sweep engine / classify pipeline, one bind-probe-respond cycle per
    // phase, and demands the accept at EVERY phase.  A phase that loses the
    // response is the race, reproduced.
    {
        const uint8_t dmP[6] = {0x91,0xE0,0xF0,0x00,0xBE,0xC6};
        const uint64_t PEER = 0x3CC0C60102030000ULL;   // sid == talker EID
        const uint64_t PW0C = 0x6805CAFFFE95B2D1ULL;   // the real controller
        int lost = 0;
        for (int ph = 0; ph <= 24; ph++) {
            // clean slate for ctx2 (SM-enabled, sid-explicit)
            feed(acmp(8, 0, 0, PW0C, PEER, US_EID, 0, 2, nullptr,
                      0x200+ph, 0, 0));                 // DISCONNECT_RX
            wait_frame();                               // unbind response
            run(20);
            feed(acmp(6, 0, 0, PW0C, PEER, US_EID, 0, 2, nullptr,
                      0x300+ph, 2, 0));                 // BIND_RX
            wait_frame();                               // bind response
            auto pr = wait_frame();                     // the PROBE_TX
            uint16_t pseq = (uint16_t)r_be(pr, 62, 2);
            run(ph);                                    // the swept phase
            feed(acmp(1, 0, PEER, PW0C, PEER, US_EID, 0, 2, dmP,
                      pseq, 2, 2));                     // the real answer
            run(6);
            tbl_read(2);
            bool ok = (c_state() == 6) && (c_probing() == 3) &&
                      (c_sid() == PEER) && (c_dmac() == 0x91E0F000BEC6ULL);
            if (!ok) {
                lost++;
                printf("  [phase %2d] LOST: state=%ld probing=%ld sid=%llx\n",
                       ph, (long)c_state(), (long)c_probing(),
                       (unsigned long long)c_sid());
            }
        }
        ck("[N10] the accept survives every arrival phase", lost, 0);

        // ---- 5.5.3.5.18 step 1 mismatch leg: wrong sequence_id ---------
        // (wrong-talker is pinned in sim_main [G]; this is the seq term)
        feed(acmp(8, 0, 0, PW0C, PEER, US_EID, 0, 2, nullptr, 0x3F0, 0, 0));
        wait_frame();
        run(20);
        feed(acmp(6, 0, 0, PW0C, PEER, US_EID, 0, 2, nullptr, 0x3F1, 2, 0));
        wait_frame();                               // bind response
        auto pm = wait_frame();                     // the PROBE_TX
        uint16_t mseq = (uint16_t)r_be(pm, 62, 2);
        tbl_read(2);
        //! the record carries the OUTSTANDING probe's id (offset-map proof
        //! for the grown struct: seq sits at bits 337:322)
        ck("[N10] record seq = the emitted probe's", (long)c_seq(),
           (long)mseq);
        feed(acmp(1, 0, PEER, PW0C, PEER, US_EID, 0, 2, dmP,
                  (uint16_t)(mseq ^ 0x5A5A), 2, 2));
        run(6);
        tbl_read(2);
        ck("[N10] wrong-seq response IGNORED (5.5.3.5.18 s1)",
           (long)c_state(), 3);
        feed(acmp(1, 0, PEER, PW0C, PEER, US_EID, 0, 2, dmP, mseq, 2, 2));
        run(6);
        tbl_read(2);
        ck("[N10] right-seq response accepted", (long)c_state(), 6);
        ck("[N10] probing COMPLETED", (long)c_probing(), 3);
    }

    // ---------------------------------------------------------------- //
    printf("\n[B2c] unbind clears the availability view (no stale ladder)\n");
    // gh #55 B2c: the unbind arm PRESERVED tk_avail/adp_age, so an unbound
    // record kept aging and the NEXT bind (possibly a different talker)
    // inherited a stale "discovered" view — its RETRY expiry then re-drew
    // the fast DELAY ladder against a talker nobody has seen (phantom
    // re-probes). Both unbind branches now clear the whole record.
    {
        const uint64_t PEER = 0x3CC0C60102030000ULL;
        const uint64_t PW0C = 0x6805CAFFFE95B2D1ULL;
        // X (= PEER, ctx2's bound talker after [N10]) becomes ADP-visible
        feed(adp(0, PEER));
        run(8);
        tbl_read(2);
        ck("[B2c] X visible on the bound record", (long)cbits(312, 1), 1);
        //! the ADPDU's valid_time landed in the record (adp_vt at 321:317)
        ck("[B2c] valid_time latched (vt=3)", (long)c_advt(), 3);
        // unbind: the availability view goes with the record
        feed(acmp(8, 0, 0, PW0C, PEER, US_EID, 0, 2, nullptr, 0x800, 0, 0));
        auto r8 = wait_frame();
        ck("[B2c] UNBIND SUCCESS", r_sta(r8), 0);
        tbl_read(2);
        ck("[B2c] record UNBOUND", (long)c_state(), 0);
        ck("[B2c] tk_avail cleared with it", (long)cbits(312, 1), 0);
        ck("[B2c] adp_age cleared with it", (long)cbits(298, 7), 0);
        ck("[B2c] valid_time cleared with it", (long)c_advt(), 0);
        // rebind to Y (T3, NEVER ADP-visible): the fresh bind must start
        // at "talker has not been discovered" (5.5.3.5.6 step 6)
        feed(acmp(6, 0, 0, CT_EID, T3_EID, US_EID, 0, 2, nullptr,
                  0x801, 0, 0));
        (void)wait_frame();                       // BIND_RESP
        (void)wait_frame();                       // probe #1
        tbl_read(2);
        ck("[B2c] rebind-Y inherits NO availability", (long)cbits(312, 1), 0);
        (void)wait_frame(250 * MS);               // probe #2 (dup resend)
        run(250 * MS);                            // -> PRB_W_RETRY
        tbl_read(2);
        ck("[B2c] ladder timed out to RETRY", (long)c_state(), 5);
        run(4100 * MS);                           // RETRY expiry
        tbl_read(2);
        ck("[B2c] RETRY expiry parks PASSIVE (Y undiscovered)",
           (long)c_state(), 1);
        auto rq = wait_frame(1200 * MS);
        ck("[B2c] ...and stays SILENT (no phantom re-probe)", rq.size(), 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[B1a] NO_TK lapse zeroes the SRP params; contexts isolated\n");
    // gh #54 B1a: 5.5.3.5.36 step 1 "Clear the SRP parameters and stop
    // SRP" — after 10 s of talker silence the sink must not keep declaring
    // with stale dmac/vlan. A neighbouring settled context keeps ITS
    // parameters untouched (the isolation half).
    {
        // ctx2 (in PRB_W_AVAIL on T3 after [B2c]): make T3 visible, settle
        // it with real params, promote to RSV_OK (immune to NO_TK)
        dut->ta_registered_i &= ~(1u << 2);       // arm a FRESH edge later
        run(8);
        feed(adp(0, T3_EID));
        run(8);
        auto p2b = wait_frame(1100 * MS);         // DELAY -> probe
        ck("[B1a] ctx2 re-probes T3", p2b.size(), 70);
        {
            const uint8_t dmI2[6] = {0x91,0xE0,0xF0,0x00,0x66,0x22};
            feed(acmp(1, 0, 0x5151515151515151ULL, CT_EID, T3_EID, US_EID,
                      0, 2, dmI2, (uint16_t)r_be(p2b, 62, 2), 0, 6));
        }
        tbl_read(2);
        ck("[B1a] ctx2 settled", (long)c_state(), 6);
        dut->ta_registered_i |= (1u << 2);
        run(8);
        tbl_read(2);
        ck("[B1a] ctx2 RSV_OK (no NO_TK)", (long)c_state(), 7);

        // ctx0: bind to T1 (not ADP-visible, no registrar) and settle with
        // NONZERO params -> its NO_TK runs the full 10 s
        feed(acmp(6, 0, 0, CT_EID, T1_EID, US_EID, 0, 0, nullptr,
                  0x810, 0, 0));
        (void)wait_frame();                       // BIND_RESP
        auto p0b = wait_frame();                  // probe
        {
            const uint8_t dmI0[6] = {0x91,0xE0,0xF0,0x00,0x66,0x00};
            feed(acmp(1, 0, T1_SID, CT_EID, T1_EID, US_EID, 0, 0, dmI0,
                      (uint16_t)r_be(p0b, 62, 2), 0, 5));
        }
        tbl_read(0);
        ck("[B1a] ctx0 settled with params", (long)c_state(), 6);
        ckh("[B1a] ctx0 dmac learned", c_dmac(), 0x91E0F0006600ULL);
        ck("[B1a] ctx0 active", dut->stream_active_o & 1, 1);

        run(10100 * MS);                          // the NO_TK lapse
        tbl_read(0);
        ck("[B1a] ctx0 lapsed to PRB_W_AVAIL", (long)c_state(), 1);
        ckh("[B1a] ctx0 dmac zeroed (5.5.3.5.36 s1)", c_dmac(), 0);
        ck("[B1a] ctx0 vlan zeroed", (long)c_vlan(), 0);
        ckh("[B1a] ctx0 sid zeroed (5.3.8.9)", c_sid(), 0);
        ckh("[B1a] ctx0 bind-view sid lane zeroed (want guard)", sidv(0), 0);
        ck("[B1a] ctx0 deactivated", dut->stream_active_o & 1, 0);
        ck("[B1a] ctx0 declare withdrawn", dut->lstn_declare_o & 1, 0);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x811, 0, 0));
        auto rg = wait_frame();
        ck("[B1a] GET count still 1 (bound)", (long)r_be(rg, 60, 2), 1);
        ckh("[B1a] GET bytes 54-59 zero after lapse", r_be(rg, 54, 6), 0);
        ck("[B1a] GET vlan zero after lapse", (long)r_be(rg, 66, 2), 0);
        ckh("[B1a] GET stream_id zero after lapse (5.3.8.9)",
            r_be(rg, 18, 8), 0);
        // isolation: ctx2 rode the 10 s out untouched
        tbl_read(2);
        ck("[B1a] ctx2 still RSV_OK", (long)c_state(), 7);
        ckh("[B1a] ctx2 dmac intact", c_dmac(), 0x91E0F0006622ULL);
        ck("[B1a] ctx2 still active", (dut->stream_active_o >> 2) & 1, 1);
        ck("[B1a] ctx2 still declares", (dut->lstn_declare_o >> 2) & 1, 1);
    }

    // ---------------------------------------------------------------- //
    printf("\n[B2h] ADP watch law: gm/domain gate + available_index\n");
    // Milan 5.6.4.5.1 step 1 (gm/domain must match the committed view or
    // the ENTITY_AVAILABLE is ignored), 5.6.4.5.2 step 2 (non-increasing
    // available_index = talker restart = EVT_TK_DEPARTED, index noted so
    // the next increasing ADPDU re-discovers), 5.6.4.5.3 (DEPARTING has no
    // gm step). interface_index is deliberately unchecked in RTL: single-
    // AVB-interface platform. ctx0 sits in PRB_W_AVAIL bound to T1 after
    // [B1a] — exactly the discovery-wait state the gate protects.
    {
        const uint64_t GM = 0x001B21FFFE0A0B0CULL;
        tbl_read(0);
        ck("[B2h] precondition: ctx0 PRB_W_AVAIL", (long)c_state(), 1);
        ck("[B2h] precondition: tk_avail 0", (long)cbits(312, 1), 0);
        dut->gm_id_i = GM; dut->gm_domain_i = 5;
        // wrong grandmaster: ignored entirely (no discovery, no note)
        feed(adp(0, T1_EID, 3, 0x0102030405060708ULL, 5, 30));
        run(8);
        tbl_read(0);
        ck("[B2h] wrong-gm AVAILABLE ignored (5.6.4.5.1 s1)",
           (long)cbits(312, 1), 0);
        ck("[B2h] ...state unmoved", (long)c_state(), 1);
        ck("[B2h] ...index not noted", (long)c_lastav(), 0);
        // right gm, wrong domain: same verdict
        feed(adp(0, T1_EID, 3, GM, 6, 31));
        run(8);
        tbl_read(0);
        ck("[B2h] wrong-domain AVAILABLE ignored", (long)cbits(312, 1), 0);
        // matching pair: discovered, index noted at its struct offset
        feed(adp(0, T1_EID, 3, GM, 5, 32));
        run(8);
        tbl_read(0);
        ck("[B2h] matching AVAILABLE discovers", (long)cbits(312, 1), 1);
        ck("[B2h] EVT_TK_DISCOVERED -> PRB_W_DELAY", (long)c_state(), 2);
        ck("[B2h] available_index noted (last_avail at 369:338)",
           (long)c_lastav(), 32);
        ck("[B2h] adp_age reset with it", (long)cbits(298, 7), 0);
        // non-increasing index while discovered: EVT_TK_DEPARTED — the
        // DELAY arc consumes adp_dep back to PRB_W_AVAIL
        feed(adp(0, T1_EID, 3, GM, 5, 32));
        run(8);
        tbl_read(0);
        ck("[B2h] repeated index wipes availability (5.6.4.5.2 s2)",
           (long)cbits(312, 1), 0);
        ck("[B2h] EVT_TK_DEPARTED -> PRB_W_AVAIL", (long)c_state(), 1);
        ck("[B2h] index still noted (step 3)", (long)c_lastav(), 32);
        // the restarted talker's next ADPDU increases again: re-discovered
        feed(adp(0, T1_EID, 3, GM, 5, 33));
        run(8);
        tbl_read(0);
        ck("[B2h] increasing index re-discovers", (long)cbits(312, 1), 1);
        ck("[B2h] ...and re-enters the ladder", (long)c_state(), 2);
        ck("[B2h] note advances", (long)c_lastav(), 33);
        // strictly-lower index (deeper regression) wipes as well
        feed(adp(0, T1_EID, 3, GM, 5, 31));
        run(8);
        tbl_read(0);
        ck("[B2h] lower index wipes too", (long)cbits(312, 1), 0);
        ck("[B2h] lower index noted", (long)c_lastav(), 31);
        // DEPARTING is never gm-gated (5.6.4.5.3 names no gm step)
        feed(adp(0, T1_EID, 3, GM, 5, 40));
        run(8);
        tbl_read(0);
        ck("[B2h] re-discovered for the departing leg",
           (long)cbits(312, 1), 1);
        feed(adp(1, T1_EID, 3, 0xDEADDEADDEADDEADULL, 9, 41));
        run(8);
        tbl_read(0);
        ck("[B2h] wrong-gm DEPARTING still departs (5.6.4.5.3)",
           (long)cbits(312, 1), 0);
        // all-zero committed pair = no gPTP commitment yet: gate stands
        // down (bring-up / saved-state fast-connect must not deadlock)
        dut->gm_id_i = 0; dut->gm_domain_i = 0;
        feed(adp(0, T1_EID, 3, 0x5555666677778888ULL, 7, 42));
        run(8);
        tbl_read(0);
        ck("[B2h] zero committed pair: gate off (bring-up escape)",
           (long)cbits(312, 1), 1);
        ck("[B2h] escape notes the index too", (long)c_lastav(), 42);
    }

    printf("\nKL_acmp_lstn_ctx N=4: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
