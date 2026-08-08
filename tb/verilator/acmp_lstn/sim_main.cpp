/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for KL_acmp_listener (Milan v1.2 listener
 * SM, pipewire acmp-milan-v12.c contract). Runs at a 10 kHz scaled clock so
 * the 200 ms / 4 s / 10 s timers are simulable. Exit 0 = all pass.
 */

#include "VKL_acmp_listener.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static VKL_acmp_listener* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-46s = %ld\n", what, got); }
}
static void ckh(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-46s got=%llx exp=%llx\n", what,
                              (unsigned long long)got, (unsigned long long)exp); }
    else            { printf("  [ ok ] %-46s = %llx\n", what, (unsigned long long)got); }
}

// KNOWN-GAP pin (see the [G] section). Records a behaviour a clause REQUIRES
// and this RTL does not implement yet. It counts as a check and PASSES while
// the value is still the non-conformant one we measured, so the suite stays
// green and honest; it FAILS THE SUITE the moment the value moves - to the
// conformant value (the gap closed: promote the gap() to a ck()) or to
// anything else (a regression). A gap can therefore never be forgotten and can
// never be closed silently.
static long gapsn = 0;
static void gap(const char* what, long got, long cur, long req,
                const char* clause) {
    checks++;
    if (got == cur) {
        gapsn++;
        printf("  [ GAP ] %-46s = %ld   (%s requires %ld)\n",
               what, got, clause, req);
    } else if (got == req) {
        fails++;
        printf("  [GAP CLOSED] %-39s got=%ld - now conformant with %s:\n"
               "               promote this gap() to a ck() and drop the pin\n",
               what, got, clause);
    } else {
        fails++;
        printf("  [FAIL] %-46s got=%ld exp %ld (gap) or %ld (fixed)\n",
               what, got, cur, req);
    }
}

// partial response frame currently being assembled (survives across helpers)
static std::vector<uint8_t> partial;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}

// advance one clock, harvesting any active output beat first
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

static void run(int n) {
    for (int i = 0; i < n; i++) tick_collect(nullptr);
}

// wait for the next complete output frame (empty = none within budget)
static std::vector<uint8_t> wait_frame(int budget = 4000) {
    std::vector<uint8_t> f;
    for (int c = 0; c < budget; c++)
        if (tick_collect(&f)) return f;
    return {};
}

// ------------------------------------------------------------------ identity
static const uint64_t US_EID  = 0x020000FFFE000003ULL;  // this listener
static const uint8_t  US_MAC[6] = {0x02,0x00,0x00,0x00,0x00,0x03};
static const uint64_t TK_EID  = 0x020000FFFE000001ULL;  // bound talker
static const uint64_t TK2_EID = 0x020000FFFE000002ULL;
static const uint64_t CT_EID  = 0x680500FFFE0000AAULL;  // controller
static const uint64_t CT2_EID = 0x680500FFFE0000BBULL;  // rebinding controller
static const uint64_t TK_SID  = 0x0200000000010000ULL;  // {talker MAC, uid 0}

static void put_be(std::vector<uint8_t>& v, uint64_t x, int n) {
    for (int i = n-1; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}

// 70-byte ACMP frame
static std::vector<uint8_t> acmp(uint8_t msg, uint8_t status,
                                 uint64_t sid, uint64_t ctlr, uint64_t talker,
                                 uint64_t lstnr, uint16_t tuid, uint16_t luid,
                                 const uint8_t* dmac, uint16_t seq,
                                 uint16_t flags, uint16_t vlan) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0xAA,0xBB,0xCC,0x00,0x00,0x01,
                              0x22,0xF0, 0xFC};
    f.push_back(msg & 0xF);
    f.push_back((status << 3) | 0);          // status | cdl_hi (cdl=44)
    f.push_back(44);
    put_be(f, sid, 8);
    put_be(f, ctlr, 8);
    put_be(f, talker, 8);
    put_be(f, lstnr, 8);
    put_be(f, tuid, 2);
    put_be(f, luid, 2);
    for (int i = 0; i < 6; i++) f.push_back(dmac ? dmac[i] : 0);
    put_be(f, 0, 2);                          // connection_count
    put_be(f, seq, 2);
    put_be(f, flags, 2);
    put_be(f, vlan, 2);
    put_be(f, 0, 2);                          // reserved
    return f;
}

// minimal ADP frame (>= 26 bytes classified; padded to 82). Byte 16 [7:3]
// is valid_time in 2 s units (1722.1 6.2.2.5) — the RTL ages the talker
// out after vt x 2 seconds, so the tests pass an explicit vt (default 3
// = the historical 0x1F byte's field value = a 6 s horizon).
static std::vector<uint8_t> adp(uint8_t msg, uint64_t eid, uint8_t vt = 3) {
    std::vector<uint8_t> f = {0x91,0xE0,0xF0,0x01,0x00,0x00,
                              0x02,0x00,0x00,0x00,0x00,0x01,
                              0x22,0xF0, 0xFA};
    f.push_back(msg & 0xF);
    f.push_back((uint8_t)(vt << 3)); f.push_back(56);   // valid_time | cdl
    put_be(f, eid, 8);                         // entity_id at wire byte 18
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
    // classification cycle
    tick_collect(nullptr);
    tick_collect(nullptr);
}

// response accessors (wire bytes)
static int r_msg(const std::vector<uint8_t>& b){ return b.size()>15 ? b[15]&0xF : -1; }
static int r_sta(const std::vector<uint8_t>& b){ return b.size()>16 ? b[16]>>3 : -1; }
static uint64_t r_be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0;
    for (int i = 0; i < n; i++)
        v = (v << 8) | ((size_t)(off+i) < b.size() ? b[off+i] : 0);
    return v;
}

// scaled-clock timer values (cycles): 1 ms = 10 cycles
static const int MS = 10;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_acmp_listener;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->entity_id_i = US_EID;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|US_MAC[i]; dut->station_mac_i = m; }
    dut->tick_1s_i = 0;
    dut->ta_registered_i = 0; dut->ta_failed_i = 0;
    dut->locked_i = 0; dut->lock_ctlr_i = 0;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== KL_acmp_listener — Milan v1.2 listener SM ==\n");

    // ---------------------------------------------------------------- //
    printf("\n[1] reset + GET_RX_STATE unbound\n");
    ck("[1] state UNBOUND", dut->state_o, 0);
    ck("[1] inactive", dut->stream_active_o, 0);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x100, 0, 0));
    auto r = wait_frame();
    ck("[1] GET_RX_STATE answered", r.size(), 70);
    ck("[1] msg GET_RX_STATE_RESPONSE", r_msg(r), 11);
    ck("[1] SUCCESS", r_sta(r), 0);
    ck("[1] count 0", (long)r_be(r, 60, 2), 0);
    ckh("[1] talker 0", r_be(r, 34, 8), 0);
    ck("[1] flags 0", (long)r_be(r, 64, 2), 0);
    // ECHOED fields: the response FSM overrides only the beats it owns and
    // passes the rest STRAIGHT OUT OF the frame-word buffer (rword_w =
    // fword_r[beat_r]). Nothing pinned that buffer until the 07-27 area
    // round hoisted its write into its own reset-free process to let it
    // infer as distributed RAM - perturbing the RAM's write address left
    // every check in this suite green. sequence_id and the two unique-ids
    // are the echo, and IEEE 1722.1 8.2.2 requires them verbatim.
    ck("[1] sequence_id echoed", (long)r_be(r, 62, 2), 0x100);
    ck("[1] talker_unique_id echoed", (long)r_be(r, 50, 2), 0);
    ck("[1] listener_unique_id echoed", (long)r_be(r, 52, 2), 0);
    ck("[1] control_data_length echoed", (long)r_be(r, 17, 1), 44);

    // sink 1 (CRF): valid but ALWAYS unbound (la_avdecc fatal-enumeration
    // field report: UNKNOWN_ID for an advertised sink is inconsistent)
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[1b] sink1 GET_RX_STATE SUCCESS", r_sta(r), 0);
    ck("[1b] sink1 count 0", (long)r_be(r, 60, 2), 0);
    ckh("[1b] sink1 talker 0", r_be(r, 34, 8), 0);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 2, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[1b] sink2 UNKNOWN_ID", r_sta(r), 1);

    // ---------------------------------------------------------------- //
    printf("\n[2] BIND_RX -> response + probe, PRB_W_RESP\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x101,
              0x0002 /*FAST_CONNECT requested*/, 0));
    r = wait_frame();
    ck("[2] BIND_RESP", r_msg(r), 7);
    ck("[2] SUCCESS", r_sta(r), 0);
    ck("[2] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[2] stream_id zero", r_be(r, 18, 8), 0);
    ckh("[2] dmac zero", r_be(r, 54, 6), 0);
    ck("[2] FAST_CONNECT cleared", (long)r_be(r, 64, 2), 0);
    ck("[2] vlan zero", (long)r_be(r, 66, 2), 0);
    auto p = wait_frame();
    ck("[2] PROBE_TX follows", p.size(), 70);
    ck("[2] probe msg CONNECT_TX_COMMAND", r_msg(p), 0);
    ckh("[2] probe controller", r_be(p, 26, 8), CT_EID);
    ckh("[2] probe talker", r_be(p, 34, 8), TK_EID);
    ckh("[2] probe listener us", r_be(p, 42, 8), US_EID);
    ck("[2] probe seq 0", (long)r_be(p, 62, 2), 0);
    ckh("[2] probe stream_id 0", r_be(p, 18, 8), 0);
    ck("[2] state PRB_W_RESP", dut->state_o, 3);
    ckh("[2] bound sid derived", dut->bound_sid_o, TK_SID);
    ck("[2] probing ACTIVE", dut->probing_o, 2);
    ck("[2] probe_count 1", dut->probe_count_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[2b] sink1 stays unbound-shaped while sink0 is mid-ladder\n");
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x100, 0, 0));
    r = wait_frame();
    ck("[2b] sink1 SUCCESS", r_sta(r), 0);
    ck("[2b] sink1 count 0", (long)r_be(r, 60, 2), 0);
    ckh("[2b] sink1 talker 0 (sink0 state masked)", r_be(r, 34, 8), 0);
    ck("[2b] sink1 flags 0", (long)r_be(r, 64, 2), 0);

    printf("\n[3] GET_RX_STATE while probing: Table 5.37 flags\n");
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x102, 0, 0));
    r = wait_frame();
    ck("[3] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[3] talker bound", r_be(r, 34, 8), TK_EID);
    //! Table 5.37: FAST_CONNECT = 1 in every bound state, STREAMING_WAIT =
    //! the SAVED binding flag ([2] bound with SW 0), REGISTERING_FAILED = 0
    ck("[3] flags FC|saved-SW (Table 5.37)", (long)r_be(r, 64, 2), 0x0002);
    ckh("[3] dest_mac zeroed", r_be(r, 54, 6), 0);
    ck("[3] state unchanged", dut->state_o, 3);
    //! a DIFFERENT sequence_id than [1], so the echo cannot be a constant
    ck("[3] sequence_id echoed", (long)r_be(r, 62, 2), 0x102);

    // ---------------------------------------------------------------- //
    printf("\n[4] probe response SUCCESS -> SETTLED_NO_RSV\n");
    {
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x01};
        feed(acmp(1, 0, TK_SID, CT_EID, TK_EID, US_EID, 0, 0, dm, 0, 0, 2));
    }
    ck("[4] state SETTLED_NO_RSV", dut->state_o, 6);
    ck("[4] active", dut->stream_active_o, 1);
    ck("[4] declares Listener attr", dut->lstn_declare_o, 1);
    ckh("[4] sid authoritative", dut->bound_sid_o, TK_SID);
    ck("[4] vlan 2", dut->stream_vlan_o, 2);
    ckh("[4] dmac captured", dut->stream_dmac_o, 0x91E0F000FE01ULL);
    ck("[4] probing COMPLETED", dut->probing_o, 3);
    //! a DUPLICATE of the accepted response is a no-op: 5.5.3.5.18 fires
    //! only in PRB_W_RESP/RESP2, and the sink has left them
    {
        const uint8_t dm2[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x77};
        feed(acmp(1, 0, 0xDEAD00000000BEEFULL, CT_EID, TK_EID, US_EID,
                  0, 0, dm2, 0, 0, 7));
        ck("[4] duplicate response: state held", dut->state_o, 6);
        ckh("[4] duplicate response: sid held", dut->bound_sid_o, TK_SID);
        ckh("[4] duplicate response: dmac held", dut->stream_dmac_o,
            0x91E0F000FE01ULL);
    }

    // ---------------------------------------------------------------- //
    printf("\n[5] TalkerAdvertise registered -> SETTLED_RSV_OK\n");
    dut->ta_registered_i = 1;
    run(4);
    ck("[5] state SETTLED_RSV_OK", dut->state_o, 7);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x103, 0, 0));
    r = wait_frame();
    //! Table 5.39: FC 1, saved SW 0, RF 0 (Talker ADVERTISE registered)
    ck("[5] settled flags FC only (Table 5.39)", (long)r_be(r, 64, 2),
       0x0002);
    ck("[5] count 1", (long)r_be(r, 60, 2), 1);
    ckh("[5] dest_mac echoes the learned MAAP addr", r_be(r, 54, 6),
        0x91E0F000FE01ull);

    // ---------------------------------------------------------------- //
    printf("\n[6] Advertise<->Failed flips while settled: STAYS RSV_OK\n");
    // Table 5.29: EVT_TK_REGISTERED/_UNREGISTERED are edges of the COMBINED
    // Talker attribute ("either Talker Advertise or Talker Failed"); Table
    // 5.30 marks every other SRP row in SETTLED_RSV_OK "x". A TalkerFailed
    // RISE while the Advertise is registered is therefore NO event — the
    // old RTL invented an RSV_OK -> NO_RSV arc here (pipewire REF-BUG),
    // whose tmr=0 landing disarmed the wheel = the ordering-race wedge.
    dut->ta_failed_i = 1;              // TF rise, TA still registered
    run(4);
    ck("[6] TF-rise while settled STAYS RSV_OK", dut->state_o, 7);
    dut->ta_registered_i = 0;          // TA falls, TF still holds
    run(4);
    ck("[6] TA-fall with TF held: still RSV_OK", dut->state_o, 7);
    ck("[6] still active", dut->stream_active_o, 1);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x10A, 0, 0));
    r = wait_frame();
    //! Table 5.39 REGISTERING_FAILED: 1 while the registered attribute is
    //! a Talker FAILED (FC 1, saved SW 0)
    ck("[6] flags FC|RF while TalkerFailed registered",
       (long)r_be(r, 64, 2), 0x0042);
    dut->ta_registered_i = 1;          // back to Advertise...
    run(4);
    dut->ta_failed_i = 0;              // ...Failed withdrawn: never a fall
    run(4);
    ck("[6] attribute never unregistered: RSV_OK held", dut->state_o, 7);

    // ---------------------------------------------------------------- //
    printf("\n[7] reservation lost (combined fall) -> PRB_W_AVAIL + SRP clear\n");
    dut->ta_registered_i = 0;
    run(4);
    ck("[7] state PRB_W_AVAIL", dut->state_o, 1);
    ck("[7] deactivated", dut->stream_active_o, 0);
    ck("[7] declare withdrawn", dut->lstn_declare_o, 0);
    ck("[7] probing PASSIVE", dut->probing_o, 1);
    //! 5.5.3.5.48 step 1 "Clear the SRP parameters": dmac/vlan zeroed; the
    //! record sid deliberately survives (lwSRP row key — see the RTL note)
    ckh("[7] stale dmac cleared (5.5.3.5.48 s1)", dut->stream_dmac_o, 0);
    ck("[7] stale vlan cleared", dut->stream_vlan_o, 0);
    ckh("[7] sid preserved (row key)", dut->bound_sid_o, TK_SID);

    // ---------------------------------------------------------------- //
    printf("\n[8] ADP AVAILABLE -> DELAY -> probe ladder to RETRY\n");
    feed(adp(0, TK_EID));
    run(4);
    ck("[8] tk_avail", dut->tk_avail_o, 1);
    ck("[8] state PRB_W_DELAY", dut->state_o, 2);
    // random delay <= 1024 ms; wait up to 1100 ms for the probe
    p = wait_frame(1100 * MS);
    ck("[8] probe sent after delay", p.size(), 70);
    ck("[8] state PRB_W_RESP", dut->state_o, 3);
    // no answer: 200 ms -> resend (RESP2). 5.5.3.5.16 step 1: the resend
    // is a DUPLICATE of the first probe — same sequence_id, same bytes —
    // never a fresh draw.
    {
        auto p1st = p;
        p = wait_frame(250 * MS);
        ck("[8] probe resent", p.size(), 70);
        ck("[8] state PRB_W_RESP2", dut->state_o, 4);
        ck("[8] resend reuses the sequence_id (5.5.3.5.16)",
           (long)r_be(p, 62, 2), (long)r_be(p1st, 62, 2));
        ck("[8] resend is a byte-exact duplicate", p == p1st ? 1 : 0, 1);
    }
    // no answer again: 200 ms -> RETRY with LISTENER_TALKER_TIMEOUT
    run(250 * MS);
    ck("[8] state PRB_W_RETRY", dut->state_o, 5);
    ck("[8] status LISTENER_TALKER_TIMEOUT", dut->acmp_status_o, 7);

    // ---------------------------------------------------------------- //
    printf("\n[9] RETRY expiry (talker visible) -> DELAY -> probe -> error resp\n");
    p = wait_frame(4200 * MS + 1100 * MS);   // 4 s retry + <=1.024 s delay
    ck("[9] re-probe emitted", p.size(), 70);
    ck("[9] state PRB_W_RESP", dut->state_o, 3);
    // talker answers with TALKER_NO_BANDWIDTH (5) — the response must echo
    // the probe's sequence_id to be accepted (5.5.3.5.18 step 1)
    feed(acmp(1, 5, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr,
              (uint16_t)r_be(p, 62, 2), 0, 0));
    ck("[9] state PRB_W_RETRY", dut->state_o, 5);
    ck("[9] status stored (5)", dut->acmp_status_o, 5);

    // ---------------------------------------------------------------- //
    printf("\n[10] ADP DEPARTING in RETRY -> PRB_W_AVAIL\n");
    feed(adp(1, TK_EID));
    run(4);
    ck("[10] tk_avail dropped", dut->tk_avail_o, 0);
    ck("[10] state PRB_W_AVAIL", dut->state_o, 1);

    // ---------------------------------------------------------------- //
    printf("\n[11] rebind-same = response only; rebind-different = re-probe\n");
    long pc = dut->probe_count_o;
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x104, 0, 0));
    r = wait_frame();
    ck("[11] rebind-same BIND_RESP", r_msg(r), 7);
    ck("[11] state stays PRB_W_AVAIL", dut->state_o, 1);
    ck("[11] no new probe", dut->probe_count_o, pc);
    // stale ACMP status from [9] (TALKER_NO_BANDWIDTH) still shows here:
    // the rebind-same fast path must not touch it (5.5.3.5.43 step 2)
    ck("[11] stale status survives rebind-same", dut->acmp_status_o, 5);
    feed(acmp(6, 0, 0, CT_EID, TK2_EID, US_EID, 0, 0, nullptr, 0x105, 0, 0));
    r = wait_frame();
    ck("[11] rebind-diff BIND_RESP", r_msg(r), 7);
    p = wait_frame();
    ck("[11] probe to new talker", p.size(), 70);
    ckh("[11] probe talker T2", r_be(p, 34, 8), TK2_EID);
    ck("[11] state PRB_W_RESP", dut->state_o, 3);
    ckh("[11] bound talker T2", dut->bound_talker_o, TK2_EID);
    ck("[11] stale status cleared (5.5.3.5.43 step 11)", dut->acmp_status_o, 0);

    // ---------------------------------------------------------------- //
    printf("\n[12] settle on T2 then UNBIND_RX -> UNBOUND\n");
    {
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x02};
        feed(acmp(1, 0, 0x0200000000020000ULL, CT_EID, TK2_EID, US_EID, 0, 0,
                  dm, (uint16_t)r_be(p, 62, 2), 0, 2));
    }
    ck("[12] settled", dut->state_o, 6);
    feed(acmp(8, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x106, 0x0008, 0));
    r = wait_frame();
    ck("[12] UNBIND_RESP", r_msg(r), 9);
    ck("[12] SUCCESS", r_sta(r), 0);
    ckh("[12] talker zeroed", r_be(r, 34, 8), 0);
    ck("[12] count 0", (long)r_be(r, 60, 2), 0);
    ck("[12] SW cleared", (long)r_be(r, 64, 2), 0);
    ck("[12] state UNBOUND", dut->state_o, 0);
    ck("[12] inactive", dut->stream_active_o, 0);
    ck("[12] probing DISABLED", dut->probing_o, 0);
    ckh("[12] binding cleared", dut->bound_talker_o, 0);

    // ---------------------------------------------------------------- //
    printf("\n[13] bad listener_unique_id + foreign frames\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 5, nullptr, 0x107, 0, 0));
    r = wait_frame();
    ck("[13] BIND luid=5 LISTENER_UNKNOWN_ID", r_sta(r), 1);
    ck("[13] state UNBOUND still", dut->state_o, 0);
    feed(acmp(6, 0, 0, CT_EID, TK_EID, 0x1111222233334444ULL, 0, 0,
              nullptr, 0x108, 0, 0));
    r = wait_frame(600);
    ck("[13] foreign listener ignored", r.size(), 0);

    // ---------------------------------------------------------------- //
    printf("\n[L] AECP lock gates BIND/UNBIND through the wrapper (B2a)\n");
    // Milan 5.5.3.5 step 1 of every BIND/UNBIND clause: while locked, a
    // foreign controller's state-changing command answers CONTROLLER_NOT_
    // AUTHORIZED (Table 5.31 = full command echo) and changes NOTHING.
    // The full echo/exemption matrix is pinned in sim_ctx [L]; this leg
    // pins the wrapper pass-through the datapath instance rides.
    {
        long pcl = dut->probe_count_o;
        dut->locked_i = 1; dut->lock_ctlr_i = CT_EID;
        feed(acmp(6, 0, 0, CT2_EID, TK_EID, US_EID, 0, 0, nullptr,
                  0x140, 0, 0));
        r = wait_frame();
        ck("[L] foreign BIND refused (16)", r_sta(r), 16);
        ck("[L] refusal is a BIND_RESP", r_msg(r), 7);
        ckh("[L] refusal echoes the command talker", r_be(r, 34, 8), TK_EID);
        ck("[L] record untouched (UNBOUND)", dut->state_o, 0);
        ck("[L] no probe launched", dut->probe_count_o, pcl);
        dut->locked_i = 0; dut->lock_ctlr_i = 0;
    }

    // ---------------------------------------------------------------- //
    printf("\n[14] NO_TK lapse in SETTLED_NO_RSV: 5.5.3.5.36 SRP clear\n");
    feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x109, 0, 0));
    (void)wait_frame();                              // BIND_RESP
    p = wait_frame();                                // the PROBE_TX
    {   //! settle with NONZERO SRP params so the lapse-zeroing is visible
        const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x01};
        feed(acmp(1, 0, TK_SID, CT_EID, TK_EID, US_EID, 0, 0, dm,
                  (uint16_t)r_be(p, 62, 2), 0, 2));
    }
    ck("[14] settled", dut->state_o, 6);
    ckh("[14] dmac learned", dut->stream_dmac_o, 0x91E0F000FE01ULL);
    //! invalid-uid refusal must not leak this BOUND record (Table 5.27 =
    //! command echo for every named field; the old path read ctx-0)
    {
        feed(acmp(10, 0, 0x1122334455667788ULL, CT_EID,
                  0x5544332211009988ULL, US_EID, 0x7777, 5, nullptr,
                  0x141, 0x1234, 0x333));
        r = wait_frame();
        ck("[14] uid5 GET refused UNKNOWN_ID", r_sta(r), 1);
        ckh("[14] refusal talker = command echo (no ctx-0 leak)",
            r_be(r, 34, 8), 0x5544332211009988ULL);
        ck("[14] refusal tuid = command echo", (long)r_be(r, 50, 2), 0x7777);
        ckh("[14] refusal stream_id = command echo", r_be(r, 18, 8),
            0x1122334455667788ULL);
        ck("[14] refusal count = command echo", (long)r_be(r, 60, 2), 0);
        ck("[14] refusal flags = command echo", (long)r_be(r, 64, 2), 0x1234);
        ck("[14] refusal vlan = command echo", (long)r_be(r, 66, 2), 0x333);
    }
    run(10100 * MS);                                  // 10 s NO_TK
    ck("[14] state PRB_W_AVAIL", dut->state_o, 1);
    ck("[14] probing PASSIVE", dut->probing_o, 1);
    //! 5.5.3.5.36 step 1: SRP params cleared + sink closed on the lapse
    ck("[14] deactivated on lapse", dut->stream_active_o, 0);
    ck("[14] declare withdrawn on lapse", dut->lstn_declare_o, 0);
    ckh("[14] dmac zeroed on lapse", dut->stream_dmac_o, 0);
    ck("[14] vlan zeroed on lapse", dut->stream_vlan_o, 0);
    ckh("[14] sid preserved (row key)", dut->bound_sid_o, TK_SID);
    feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x142, 0, 0));
    r = wait_frame();
    ck("[14] GET count still 1 (bound)", (long)r_be(r, 60, 2), 1);
    ckh("[14] GET talker still bound", r_be(r, 34, 8), TK_EID);
    ckh("[14] GET bytes 54-59 zero after lapse", r_be(r, 54, 6), 0);
    ck("[14] GET vlan zero after lapse", (long)r_be(r, 66, 2), 0);

    // ---------------------------------------------------------------- //
    printf("\n[15] ADP availability age-out follows valid_time x 2 s\n");
    // 1722.1 6.2.2.5: the availability horizon is the ADPDU's OWN
    // valid_time (2 s units) — not a fixed constant. The talker stays
    // visible through vt x 2 seconds and drops on the tick after.
    {
        auto sec = [&](int n) {
            for (int s = 0; s < n; s++) {
                dut->tick_1s_i = 1; tick_collect(nullptr);
                dut->tick_1s_i = 0; run(3);
            }
        };
        feed(adp(0, TK_EID, 3));                    // vt 3 => 6 s
        run(4);
        ck("[15] visible again (vt=3)", dut->tk_avail_o, 1);
        sec(6);
        ck("[15] still visible through 6 s", dut->tk_avail_o, 1);
        sec(1);
        ck("[15] aged out after vt=3 horizon", dut->tk_avail_o, 0);

        feed(adp(0, TK_EID, 15));                   // vt 15 => 30 s
        run(4);
        ck("[15] refreshed (vt=15)", dut->tk_avail_o, 1);
        sec(30);
        ck("[15] still visible through 30 s", dut->tk_avail_o, 1);
        sec(1);
        ck("[15] aged out after vt=15 horizon", dut->tk_avail_o, 0);

        //! vt = 0 clamps to 4 s (LSM_ADP_AGE_MIN_S_C): neither immortal
        //! nor dead-on-arrival
        feed(adp(0, TK_EID, 0));
        run(4);
        ck("[15] refreshed (vt=0)", dut->tk_avail_o, 1);
        sec(4);
        ck("[15] vt=0 clamp holds 4 s", dut->tk_avail_o, 1);
        sec(1);
        ck("[15] vt=0 aged out at the clamp", dut->tk_avail_o, 0);
    }

    printf("\n======================================================================\n");

    // ---------------------------------------------------------------- //
    printf("\n[W] TX-grant watchdog: wedged arbiter must not deafen the SM\n");
    {
        uint16_t cc0 = dut->cmd_count_o;
        // raw feed with tready HELD LOW (feed()/tick_collect force it high)
        auto f = acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x900, 0, 0);
        dut->m_axis_tready = 0;
        for (size_t off = 0; off < f.size(); off += 8) {
            uint64_t d = 0; uint8_t keep = 0;
            for (int l = 0; l < 8; l++)
                if (off + l < f.size()) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
            dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
            dut->rx_tkeep_i = keep; dut->rx_tlast_i = (off + 8 >= f.size());
            tick();
        }
        dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
        tick(); tick(); tick();
        ck("[W] command accepted", dut->cmd_count_o, (long)(cc0 + 1));
        // walker now sits in RESPOND_S; run past the 2^20-cycle watchdog
        for (int i = 0; i < (1 << 20) + 200; i++) tick();
        ck("[W] wedge counted", dut->tx_wedge_cnt_o, 1);
        dut->m_axis_tready = 1;
        for (int i = 0; i < 10; i++) tick();
        // the listener must be alive again: next command accepted + answered
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x901, 0, 0));
        auto rw = wait_frame();
        ck("[W] next GET_RX_STATE answered", rw.size(), 70);
        ck("[W] cmd_count advanced", dut->cmd_count_o, (long)(cc0 + 2));
    }


    // ---------------------------------------------------------------- //
    printf("\n[Z] zero-gap frames: command right behind another frame\n");
    // Silicon RX FIFOs compress inter-frame gaps under DMA stalls; a
    // command draining gaplessly behind an AAF frame must still be
    // accepted (task #29). EXPECTED TO FAIL until the always-armed
    // capture lands - kept as the repro.
    {
        uint16_t cc0 = dut->cmd_count_o;
        // 88-byte AAF-ish frame (foreign dst/subtype: walker must ignore)
        std::vector<uint8_t> aaf(88, 0);
        const uint8_t ad[6]={0x91,0xE0,0xF0,0x00,0xFE,0x01};
        for (int i=0;i<6;i++) aaf[i]=ad[i];
        aaf[12]=0x22; aaf[13]=0xF0; aaf[14]=0x02; aaf[15]=0x81;
        auto cmd = acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0xA01, 0, 0);
        // drive both frames back-to-back with ZERO idle beats
        auto drive = [&](const std::vector<uint8_t>& f, bool hold_after) {
            for (size_t off = 0; off < f.size(); off += 8) {
                uint64_t d = 0; uint8_t keep = 0;
                for (int l = 0; l < 8; l++)
                    if (off + l < f.size()) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
                dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
                dut->rx_tkeep_i = keep; dut->rx_tlast_i = (off + 8 >= f.size());
                tick();
            }
            if (!hold_after) { dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; }
        };
        drive(aaf, true);          // tlast beat, then IMMEDIATELY...
        drive(cmd, false);         // ...the command, no idle cycle
        for (int i = 0; i < 30; i++) tick_collect(nullptr);
        ck("[Z] zero-gap command accepted", dut->cmd_count_o, (long)(cc0 + 1));
    }

    // ---------------------------------------------------------------- //
    printf("\n[S1] sink-1 bind: full probe ladder, response is the authority\n");
    // TASK #64. Sink 1 used to be a RECORD-ONLY bind (no probe SM, no MSRP
    // attach): it parked in SETTLED_NO_RSV and its lwSRP listener row was
    // registered against a stream_id the record COPIED from the command or
    // GUESSED from {talker EID, tuid}. Milan v1.2 5.5.3.2 defines the state
    // table per SINK and 5.5.3.5.3 step 5 requires a PROBE_TX_COMMAND on
    // RCV_BIND_RX_CMD for whichever sink listener_unique_id names, so every
    // context now runs the ladder. The fast-connect stream_id (5.5.1.2) is
    // still honoured on a non-zero sink, but only as the PROVISIONAL value:
    // 5.5.3.5.18 step 4 makes the PROBE_TX_RESPONSE the source of the real
    // stream_id / stream_dest_mac / stream_vlan_id and the trigger for
    // "initiate SRP reservation", and this section pins that ordering.
    {
        // sink0 state as [Z] left it: the S1 record must not disturb it
        long st0 = dut->state_o, act0 = dut->stream_active_o;
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x1FF, 0, 0));
        auto r = wait_frame();
        long cnt0 = (long)r_be(r, 60, 2);
        long pc0  = dut->probe_count_o;

        // fast-connect bind: command carries the stream_id + dest_mac
        const uint8_t cdm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x08};
        feed(acmp(6, 0, 0x020000000001000BULL, CT_EID, TK_EID, US_EID,
                  0x000B, 1, cdm, 0x200, 0, 0));
        r = wait_frame();
        ck("[S1] BIND_RESP", r_msg(r), 7);
        ck("[S1] SUCCESS", r_sta(r), 0);
        ck("[S1] count 1", (long)r_be(r, 60, 2), 1);
        //! Table 5.32 pins stream_dest_mac 0 on a BIND success — the
        //! fast-connect command's NONZERO dest_mac must NOT echo back
        ckh("[S1] BIND_RESP dmac pinned 0 (Table 5.32)", r_be(r, 54, 6), 0);
        ck("[S1] s1_bound_o", dut->s1_bound_o, 1);
        ckh("[S1] s1_sid = command sid (provisional)", dut->s1_sid_o,
            0x020000000001000BULL);
        // 5.5.2.6 step 1 / Table 5.33: the SRP parameters are CLEARED at bind
        // and re-learned from the probe response. The command's dest_mac is
        // not a source of truth for them - it never was for sink 0.
        ckh("[S1] s1_dmac cleared at bind (5.5.2.6 s1)", dut->s1_dmac_o, 0);
        ck("[S1] sink0 SM untouched", dut->state_o, st0);
        ck("[S1] sink0 activity untouched", dut->stream_active_o, act0);

        // ...and the probe follows the response (5.5.3.5.3 steps 3 then 5)
        auto p1 = wait_frame();
        ck("[S1] sink1 PROBE_TX emitted", p1.size(), 70);
        ck("[S1] probe is CONNECT_TX_COMMAND", r_msg(p1), 0);
        ck("[S1] probe listener_unique_id 1 (Table 5.33)",
           (long)r_be(p1, 52, 2), 1);
        ckh("[S1] probe talker = bound talker", r_be(p1, 34, 8), TK_EID);
        ck("[S1] probe talker_unique_id = binding", (long)r_be(p1, 50, 2),
           0x000B);
        ck("[S1] probe_count advanced", (long)dut->probe_count_o - pc0, 1);
        ck("[S1] sink1 state PRB_W_RESP", dut->s1_bound_o, 1);

        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x201, 0, 0));
        r = wait_frame();
        ck("[S1] state SUCCESS", r_sta(r), 0);
        ck("[S1] state count 1", (long)r_be(r, 60, 2), 1);
        ckh("[S1] state talker", r_be(r, 34, 8), TK_EID);
        ck("[S1] state tuid", (long)r_be(r, 50, 2), 0x000B);
        ckh("[S1] state dmac 0 while probing", r_be(r, 54, 6), 0);
        ck("[S1] state flags FC|saved-SW while probing (Tab 5.37)",
           (long)r_be(r, 64, 2), 0x0002);

        // THE BITE (5.5.3.5.18 step 4): the talker answers with a stream_id
        // that is NEITHER the command's fast-connect sid NOR the {EID,tuid}
        // derivation. What the sink keeps - and therefore what the lwSRP
        // listener row is registered against - must be the RESPONSE's.
        {
            const uint8_t rdm[6] = {0x91,0xE0,0xF0,0x00,0x5B,0x77};
            feed(acmp(1, 0, 0xAABBCCDDEEFF0077ULL, CT_EID, TK_EID, US_EID,
                      0x000B, 1, rdm, (uint16_t)r_be(p1, 62, 2), 0, 3));
            ckh("[S1] sid from the RESPONSE, not the guess", dut->s1_sid_o,
                0xAABBCCDDEEFF0077ULL);
            ckh("[S1] dmac from the RESPONSE", dut->s1_dmac_o,
                0x91E0F0005B77ULL);
            feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x207, 0, 0));
            r = wait_frame();
            ckh("[S1] settled state dmac from the response", r_be(r, 54, 6),
                0x91E0F0005B77ULL);
            ck("[S1] settled flags FC|saved-SW (Table 5.38)",
               (long)r_be(r, 64, 2), 0x0002);
            ck("[S1] settled state count 1", (long)r_be(r, 60, 2), 1);
        }

        // zero-sid rebind to a different tuid falls back to the {talker
        // EID(FFFE-squeezed), tuid} derivation as the PROVISIONAL value...
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0x0001, 1, nullptr,
                  0x202, 0, 0));
        r = wait_frame();
        ck("[S1] zero-sid rebind SUCCESS", r_sta(r), 0);
        ckh("[S1] fallback sid {eid,tuid}", dut->s1_sid_o,
            0x0200000000010001ULL);
        ckh("[S1] rebind clears the stale response dmac", dut->s1_dmac_o, 0);
        p1 = wait_frame();
        ck("[S1] rebind re-probes (5.5.3.5.43 step 8)", p1.size(), 70);
        ck("[S1] re-probe luid still 1", (long)r_be(p1, 52, 2), 1);

        // sink0 GET_RX_STATE remains independent (whatever [Z] left)
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x203, 0, 0));
        r = wait_frame();
        ck("[S1] sink0 state count unchanged", (long)r_be(r, 60, 2), cnt0);

        // unbind clears the record (and stops the ladder)
        feed(acmp(8, 0, 0, CT_EID, TK_EID, US_EID, 0, 1, nullptr, 0x204, 0, 0));
        r = wait_frame();
        ck("[S1] UNBIND_RESP", r_msg(r), 9);
        ck("[S1] UNBIND SUCCESS", r_sta(r), 0);
        //! Table 5.36 pins talker_unique_id 0 on success — the OLD tuid
        //! (0x0001 here, the record is pre-unbind at response time) must
        //! not be emitted
        ck("[S1] unbind tuid pinned 0 (Table 5.36)", (long)r_be(r, 50, 2), 0);
        ckh("[S1] unbind talker pinned 0", r_be(r, 34, 8), 0);
        ck("[S1] s1 cleared", dut->s1_bound_o, 0);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x205, 0, 0));
        r = wait_frame();
        ck("[S1] post-unbind count 0", (long)r_be(r, 60, 2), 0);
        ckh("[S1] post-unbind talker 0", r_be(r, 34, 8), 0);

        // uid >= 2 still LISTENER_UNKNOWN_ID
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 2, nullptr, 0x206, 0, 0));
        r = wait_frame();
        ck("[S1] uid2 bind UNKNOWN_ID", r_sta(r), 1);
        ck("[S1] uid2 left s1 alone", dut->s1_bound_o, 0);
    }

    // ---------------------------------------------------------------- //
    printf("\n[R] Milan 5.5.3.5.43: CONNECT_RX while bound + STREAMING\n");
    // The 07-29 silicon finding: a listener bound to talker X and streaming
    // is asked to CONNECT_RX talker Y. 1722.1-2021 8.2.2.6 alone would
    // refuse with LISTENER_EXCLUSIVE (8.2.4.2.2 listenerIsConnected); Milan
    // v1.2 5.5.3.5.43 OVERRIDES that for a PAAD-AE: same talker = refresh
    // ctlr/STREAMING_WAIT only (step 2), different talker = implicit rebind
    // (steps 3..12: teardown + SUCCESS + fresh probe ladder), and the sink
    // never passes through UNBOUND (so the [M-5.3.8.10] not-bound->bound
    // counter reset stays silent).
    {
        // deterministic baseline: unbind (kills every pending sink-0 timer),
        // drain any stray ladder frame from the earlier sections, fresh bind
        // to X, settle via the probe response (the reference device's probe
        // flow itself is pinned by [8]/[9]/[14]/[15])
        feed(acmp(8, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x2FE, 0, 0));
        (void)wait_frame();                       // UNBIND_RESP
        run(12000);                               // > max 1024 ms DELAY draw
        ck("[R] baseline UNBOUND", dut->state_o, 0);
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x2FF, 0, 0));
        r = wait_frame();
        ck("[R] bind BIND_RESP", r_msg(r), 7);
        p = wait_frame();
        ck("[R] bind probe emitted", p.size(), 70);
        const uint8_t dmx[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x01};
        feed(acmp(1, 0, TK_SID, CT_EID, TK_EID, US_EID, 0, 0, dmx,
                  (uint16_t)r_be(p, 62, 2), 0, 2));
        ck("[R] settled on X", dut->state_o, 6);
        dut->ta_registered_i = 1;
        run(4);
        ck("[R] STREAMING on X (SETTLED_RSV_OK)", dut->state_o, 7);
        ck("[R] active", dut->stream_active_o, 1);

        // (a) same talker, STREAMING_WAIT toggled, new controller: step 2 =
        // parameter refresh ONLY - the stream must NOT be interrupted
        long pcr = dut->probe_count_o;
        feed(acmp(6, 0, 0, CT2_EID, TK_EID, US_EID, 0, 0, nullptr, 0x300,
                  0x0008, 0));
        r = wait_frame();
        ck("[R] rebind-same(SW=1) SUCCESS", r_sta(r), 0);
        ck("[R] stream not interrupted (RSV_OK)", dut->state_o, 7);
        ck("[R] still active", dut->stream_active_o, 1);
        ck("[R] no re-probe (step 2 'exit')", dut->probe_count_o, pcr);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x301, 0, 0));
        r = wait_frame();
        //! RSV_OK flags: FC 1 + the REFRESHED saved SW (Table 5.39)
        ck("[R] stored STREAMING_WAIT refreshed", (long)r_be(r, 64, 2),
           0x000A);

        // (b) THE FINDING: different talker while streaming -> implicit
        // rebind, never LISTENER_EXCLUSIVE, never an UNBOUND excursion
        dut->ta_registered_i = 0;      // Y's TA not on the wire yet
        bool saw_unbound = false;
        {
            auto f = acmp(6, 0, 0, CT2_EID, TK2_EID, US_EID, 0, 0, nullptr,
                          0x302, 0, 0);
            int n = f.size();
            for (int off = 0; off < n; off += 8) {
                uint64_t d = 0; uint8_t keep = 0;
                for (int l = 0; l < 8; l++)
                    if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
                dut->rx_tvalid_i = 1; dut->rx_tdata_i = d;
                dut->rx_tkeep_i = keep; dut->rx_tlast_i = (off + 8 >= n);
                if (dut->state_o == 0) saw_unbound = true;
                tick_collect(nullptr);
            }
            dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
            for (int i = 0; i < 6; i++) {
                if (dut->state_o == 0) saw_unbound = true;
                tick_collect(nullptr);
            }
        }
        r = wait_frame();
        ck("[R] rebind-diff SUCCESS (not LISTENER_EXCLUSIVE)", r_sta(r), 0);
        ck("[R] msg BIND_RESP", r_msg(r), 7);
        ck("[R] no UNBOUND excursion (no counter reset)", saw_unbound, 0);
        p = wait_frame();
        ck("[R] fresh probe to Y", p.size(), 70);
        ckh("[R] probe talker Y", r_be(p, 34, 8), TK2_EID);
        ckh("[R] probe ctlr = rebinding controller", r_be(p, 26, 8), CT2_EID);
        ck("[R] state PRB_W_RESP", dut->state_o, 3);
        ck("[R] X released: inactive", dut->stream_active_o, 0);
        ck("[R] Listener attr withdrawn", dut->lstn_declare_o, 0);
        ckh("[R] bound talker now Y", dut->bound_talker_o, TK2_EID);
        ckh("[R] stale X dmac cleared (5.5.2.6 step 1)", dut->stream_dmac_o, 0);
        ck("[R] stale X vlan cleared", dut->stream_vlan_o, 0);
        ckh("[R] sid re-derived for Y", dut->bound_sid_o,
            0x0200000000020000ULL);

        // (c) Y answers -> the sink settles and streams on Y
        const uint8_t dmy[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x02};
        feed(acmp(1, 0, 0x0200000000020000ULL, CT2_EID, TK2_EID, US_EID,
                  0, 0, dmy, (uint16_t)r_be(p, 62, 2), 0, 2));
        ck("[R] settled on Y", dut->state_o, 6);
        dut->ta_registered_i = 1;
        run(4);
        ck("[R] STREAMING on Y (RSV_OK)", dut->state_o, 7);
        ck("[R] active on Y", dut->stream_active_o, 1);
        ckh("[R] Y dmac learned", dut->stream_dmac_o, 0x91E0F000FE02ULL);
        dut->ta_registered_i = 0;
    }

    // ---------------------------------------------------------------- //
    printf("\n[G] Milan v1.2 5.5.3 conformance pins (task #64 closures)\n");
    // CLAUSE-FIRST NOTE, 2026-08-03. Two things reported as defects after the
    // test-device bring-up are in fact CONFORMANT for a Milan PAAD-AE and must
    // NOT be "fixed":
    //   * BIND_RX_RESPONSE carrying stream_id 00:00:00:00:00:00:00:00 is
    //     MANDATORY - Milan v1.2 Table 5.32 ("BIND_RX_RESPONSE fields on
    //     success") pins stream_id, stream_dest_mac and stream_vlan_id to
    //     zero. Checks [2] above already assert exactly that.
    //   * Answering the controller BEFORE probing the talker is the specified
    //     order - 5.5.3.5.3 sends the BIND_RX_RESPONSE at step 3 and the
    //     PROBE_TX_COMMAND at step 5. Milan does NOT use the plain
    //     1722.1-2021 8.2.2.5 flow where CONNECT_RX_RESPONSE waits for the
    //     CONNECT_TX_RESPONSE (Milan renames those messages to BIND_RX_* and
    //     PROBE_TX_* and redefines the machine around them).
    // What WAS non-conformant is pinned below - closed by task #64 and the
    // #54/#55 response-law round (the former OPEN 3/OPEN 4 gap() pins are
    // hard ck()s now). The gap() mechanism itself stays available.
    {
        // ---- CLOSED 1: every sink owns a probe state machine -----------
        // Was: KL_acmp_listener.sv SM_EN_MAP_C = N_SINKS_P'(1), i.e.
        // PROBE_SM_EN_P = ...0001, so every sink except 0 took the
        // record-only branch, parked in LSM_SETTLED_NO_RSV and never emitted
        // a PROBE_TX_COMMAND - seven AAF sinks plus CRF on the 8x8 shape.
        // Milan 5.5.3.5.3 step 5 requires one on RCV_BIND_RX_CMD for the sink
        // listener_unique_id names, and 5.5.3.5.18 step 4 makes the
        // PROBE_TX_RESPONSE the only source of the talker's real stream_id /
        // stream_dest_mac / stream_vlan_id and the trigger for "initiate SRP
        // reservation". A record-only sink instead registered its lwSRP
        // listener row (d2739b1b) against a sid DERIVED from {talker EID,
        // tuid} - right only when the talker derives the same way.
        // SM_EN_MAP_C is now all-ones; [S1] above pins the response-is-the-
        // authority half, this pins the probe-per-sink half.
        long pc0 = dut->probe_count_o;
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0x000B, 1, nullptr,
                  0x301, 0, 0));
        r = wait_frame();
        ck("[G] sink1 BIND_RESP", r_msg(r), 7);
        ck("[G] sink1 BIND SUCCESS", r_sta(r), 0);
        ck("[G] sink1 bound", dut->s1_bound_o, 1);
        auto p1 = wait_frame();
        ck("[G] sink1 probes the talker", (long)dut->probe_count_o - pc0, 1);
        ck("[G] sink1 probe on the wire", p1.size(), 70);
        //! msg type FIRST: a BIND_RX_RESPONSE to sink 1 also echoes
        //! listener_unique_id 1, so the index check alone can be satisfied by
        //! the wrong frame entirely
        ck("[G] sink1 probe is CONNECT_TX_COMMAND", r_msg(p1), 0);
        ck("[G] sink1 probe carries its own sink index",
           (long)r_be(p1, 52, 2), 1);
        // ...and it is a LADDER, not one shot: 200 ms with no answer resends
        // (1722.1 Table 8-1 TMR_NO_RESP as Milan 5.5.3.5.3 step 7 sets it)
        p1 = wait_frame(260 * MS);
        ck("[G] sink1 resends at TMR_NO_RESP", p1.size(), 70);
        ck("[G] resend is a CONNECT_TX_COMMAND", r_msg(p1), 0);
        ck("[G] resend is still sink 1's", (long)r_be(p1, 52, 2), 1);
        // park it again so its ladder cannot interleave with sink 0 below
        feed(acmp(8, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x304, 0, 0));
        (void)wait_frame();
        ck("[G] sink1 unbound again", dut->s1_bound_o, 0);

        // ---- CLOSED 2: PROBE_TX_COMMAND forces FAST_CONNECT ------------
        // Was: KL_acmp_lstn_ctx.sv
        //   w_probe_flags = cur_r.flags & ~(STREAMING_WAIT | SRP_REG_FAILED)
        // FAST_CONNECT was not in that mask, so the probe reproduced whatever
        // the controller put in the BIND_RX_COMMAND. Milan Table 5.33
        // ("PROBE_TX_COMMAND fields on success") states FAST_CONNECT as the
        // literal 1, not as a copied binding parameter. Rebind sink 0
        // (settled on Y after [R]) to X to draw a fresh probe.
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0, 0, nullptr, 0x302,
                  0x0000 /*controller did NOT request FAST_CONNECT*/, 0));
        r = wait_frame();
        ck("[G] sink0 rebind SUCCESS", r_sta(r), 0);
        p = wait_frame();
        ck("[G] fresh probe emitted", p.size(), 70);
        ck("[G] probe is CONNECT_TX_COMMAND", r_msg(p), 0);
        ck("[G] probe connection_count 0 (Table 5.33)", (long)r_be(p, 60, 2), 0);
        ckh("[G] probe stream_id 0 (Table 5.33)", r_be(p, 18, 8), 0);
        ck("[G] probe FAST_CONNECT set (Table 5.33)", (long)r_be(p, 64, 2),
           0x0002);

        // ...and the flags word is still DERIVED from the record, not a
        // constant: bind asking for STREAMING_WAIT, which Table 5.33 states
        // as the literal 0, and the probe must carry FAST_CONNECT alone. A
        // "fix" that echoed the flags would show 0x000A here; one that
        // hardcoded 0x0002 everywhere would still pass this, which is why
        // [3]/[R] pin the STREAMING_WAIT the RECORD keeps.
        feed(acmp(6, 0, 0, CT_EID, TK2_EID, US_EID, 0, 0, nullptr, 0x303,
                  0x0008 /*controller DID request STREAMING_WAIT*/, 0));
        r = wait_frame();
        ck("[G] sink0 rebind to Y SUCCESS", r_sta(r), 0);
        ck("[G] BIND_RESP echoes STREAMING_WAIT (Table 5.32)",
           (long)r_be(r, 64, 2), 0x0008);
        p = wait_frame();
        ck("[G] probe FAST_CONNECT 1, STREAMING_WAIT 0", (long)r_be(p, 64, 2),
           0x0002);
        feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 0, nullptr, 0x305, 0, 0));
        r = wait_frame();
        //! probing-state GET: FC 1 + the record's STREAMING_WAIT (Tab 5.37)
        ck("[G] record still holds STREAMING_WAIT", (long)r_be(r, 64, 2),
           0x000A);

        // ---- CLOSED 3 (was OPEN): probe-response matching --------------
        // 5.5.3.5.18 step 1: "Check that the controller_entity_id,
        // talker_entity_id, talker_unique_id and sequence_id fields match
        // the fields of the PROBE_TX_COMMAND message that has been sent.
        // If not, ignore the message and exit." A CONNECT_TX_RESPONSE from
        // the WRONG talker used to settle the sink on that talker's stream
        // parameters. Pin: answer sink 0's outstanding probe as TALKER Z —
        // ignored — then as the REAL talker with the probe's own
        // sequence_id — accepted (the positive control also quiets sink
        // 0's ladder for the section below).
        long st_before = dut->state_o;
        feed(acmp(1, 0, 0x1234567890ABCDEFULL, CT_EID,
                  0x020000FFFE0000EEULL /*never bound*/, US_EID, 0, 0,
                  nullptr, 0x77, 0, 5));
        ck("[G] mismatched probe response ignored (5.5.3.5.18 s1)",
           dut->state_o, st_before);
        {
            const uint8_t gdx[6] = {0x91,0xE0,0xF0,0x00,0xFE,0x02};
            feed(acmp(1, 0, 0x0200000000020000ULL, CT_EID, TK2_EID, US_EID,
                      0, 0, gdx, (uint16_t)r_be(p, 62, 2), 0, 2));
            ck("[G] matching response accepted (positive control)",
               dut->state_o, 6);
        }

        // ---- CLOSED 4 (was OPEN): settled GET serves the SRP params ----
        // Table 5.38: stream_id / stream_dest_mac / stream_vlan_id are
        // "copied from the STREAM_INPUT's SRP parameters". The old
        // w_str_echo kept the RECEIVED frame's bytes for stream_id (18-25)
        // and stream_vlan_id (66-67), so a controller sending the usual
        // zeros read its own zeros back for a settled sink. Pinned on a
        // sink SETTLED on parameters the command does not contain.
        feed(acmp(6, 0, 0, CT_EID, TK_EID, US_EID, 0x000B, 1, nullptr,
                  0x306, 0, 0));
        (void)wait_frame();               // BIND_RESP
        p1 = wait_frame();                // PROBE_TX (its seq keys the match)
        {
            const uint8_t gdm[6] = {0x91,0xE0,0xF0,0x00,0x5B,0x88};
            feed(acmp(1, 0, 0xAABBCCDDEEFF0088ULL, CT_EID, TK_EID, US_EID,
                      0x000B, 1, gdm, (uint16_t)r_be(p1, 62, 2), 0, 4));
            ckh("[G] sink1 settled on the response sid", dut->s1_sid_o,
                0xAABBCCDDEEFF0088ULL);
            //! command carries stream_id 0 / vlan 0, record carries ...0088 / 4
            feed(acmp(10, 0, 0, CT_EID, 0, US_EID, 0, 1, nullptr, 0x307, 0, 0));
            r = wait_frame();
            ckh("[G] state dmac is the record's (Table 5.38)", r_be(r, 54, 6),
                0x91E0F0005B88ULL);
            ckh("[G] state stream_id is the record's (Table 5.38)",
                r_be(r, 18, 8), 0xAABBCCDDEEFF0088ULL);
            ck("[G] state stream_vlan_id is the record's (Table 5.38)",
               (long)r_be(r, 66, 2), 4);
        }
    }

    printf("KL_acmp_listener: %ld checks, %ld failures, %ld known gaps\n",
           checks, fails, gapsn);
    delete dut;
    return fails ? 1 : 0;
}
