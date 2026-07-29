/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_lwsrp_top.sv — the whole lwSRP engine
 * (timers + applicant TX + RX chain + bandwidth gate) driven end-to-end:
 * bridge PDUs in through the monitor tap, MRPDUs out through the AXIS
 * master, reservation outputs sampled cycle-accurately.
 *
 * CLK_FREQ_HZ_P is scaled to 10 kHz so real MRP time runs fast:
 * 1 kHz tick = 10 cycles, JoinTime = 2 000 cycles, LeaveTime = 6 000,
 * LeaveAllTime = 100 000.
 *
 * Contract under test (docs/LWSRP_FPGA_ARCHITECTURE.md §3/§6):
 *  - enable -> prompt declare pair, then a pair per JoinTime (timer cadence
 *    measured over >= 2 periods — bench rule 7), MSRP carries TalkerAdvertise
 *    while the talker is enabled.
 *  - Listener Ready in -> reservation ACTIVE: slope_en rises FIRST, the
 *    stream gate opens HOLD cycles later; idleSlope is byte-exact TSpec math;
 *    listener_ready_o exported (the ACMP listener_observed hook).
 *  - teardown (leave-timer expiry): gate closes FIRST, slope releases after.
 *  - 75 % refusal: an over-budget TSpec on a live reservation tears down
 *    (gate-first) and reports over_limit.
 *  - received LeaveAll -> prompt re-declare + registration ages out unless
 *    the listener re-registers; our own LeaveAll turn fires within the
 *    LeaveAllTime.
 *  - domain mismatch kills the reservation; heal restores it.
 *  - MILAN v1.2 5.3.7.3, the licence to stream, term by term: the gate is
 *    SHUT with no Listener registration and with Listener AskingFailed, and
 *    OPEN on Listener Ready AND on Listener Ready FAILED (the clause names
 *    both) - while the Talker attribute stays declared throughout, because
 *    5.3.7.2 makes that unconditional. Added 2026-07-28 after both boards
 *    were measured streaming SR-class-A-tagged AAF with no Listener at all.
 */

#include "VKL_lwsrp_top.h"
#include "verilated.h"
#if VM_TRACE
#include "verilated_vcd_c.h"
static VerilatedVcdC* tfp = nullptr;
#endif
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
        printf("  [FAIL] %-46s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t STATION = 0x020000000002ULL;
static const uint16_t UID     = 0;
static const uint64_t OUR_SID = (STATION << 16) | UID;
static const uint16_t VID     = 2;
static const uint16_t MAXFRM  = 224;
static const uint32_t LATENCY = 500000;
static const uint64_t BRIDGE  = 0x3CC0C6000001ULL;

enum { EV_NEW = 0, EV_JOININ = 1, EV_IN = 2, EV_JOINMT = 3, EV_MT = 4, EV_LV = 5 };
enum { D_IGN = 0, D_ASKFAIL = 1, D_READY = 2, D_READYFAIL = 3 };

// ---- cycle engine: collects TX frames + records gate/slope transitions ----
static long cyc = 0;
static std::deque<std::vector<uint8_t>> tx_frames;
static std::vector<uint8_t> partial;
struct Trans { long cyc; char sig; int val; };   // sig: 'g'ate, 's'lope
static std::vector<Trans> trans;
static int prev_gate = 0, prev_slope = 0;

//! hostile MAC-arbiter model: scripted tready stalls (incl mid-frame) +
//! the AXIS stability rule — under tvalid && !tready the source must HOLD
//! tvalid/data; a source that drops or mutates mid-stall is exactly the
//! frame-abort class that wedges the shared arb-mux grant forever (the
//! m001a silicon TX wedge hunt, 2026-07-29)
static int hostile_tready = 0;         // 0 = legacy always-ready
static unsigned lfsr = 0xACE1u;
static long axis_viol = 0, frames_started = 0;
static int in_stall = 0; static uint64_t stall_data; static int stall_last, stall_keep;
static void step() {
    if (hostile_tready) {
        lfsr = (lfsr >> 1) ^ (-(lfsr & 1u) & 0xB400u);
        dut->m_axis_tready = ((lfsr & 3u) != 0);   // ~25% stall, bursty
    }
    dut->clk_i = 0; dut->eval();
#if VM_TRACE
    if (tfp && cyc > 125000 && cyc < 136000) tfp->dump((vluint64_t)(2*cyc));
#endif
    // PRE-edge sampling: AXIS stability is judged on the values the sink
    // captures AT this rising edge (post-edge sampling races the legal
    // beat advance on stall-release and yields false violations)
    if (in_stall) {
        if (!dut->m_axis_tvalid ||
            dut->m_axis_tdata != stall_data ||
            (int)dut->m_axis_tlast != stall_last ||
            (int)dut->m_axis_tkeep != stall_keep) {
            if (axis_viol < 4)
                printf("   [viol %ld cyc %ld] tvalid=%d data %016llx->%016llx "
                       "last %d->%d\n",
                       axis_viol, cyc, (int)dut->m_axis_tvalid,
                       (unsigned long long)stall_data,
                       (unsigned long long)dut->m_axis_tdata,
                       stall_last, (int)dut->m_axis_tlast);
            axis_viol++;
        }
    }
    if (dut->m_axis_tvalid && !dut->m_axis_tready) {
        in_stall = 1; stall_data = dut->m_axis_tdata;
        stall_last = dut->m_axis_tlast; stall_keep = dut->m_axis_tkeep;
    } else in_stall = 0;
    bool accept = dut->m_axis_tvalid && dut->m_axis_tready;
    uint64_t adata = dut->m_axis_tdata; int akeep = dut->m_axis_tkeep;
    int alast = dut->m_axis_tlast;
    dut->clk_i = 1; dut->eval();
#if VM_TRACE
    if (tfp && cyc > 125000 && cyc < 136000) tfp->dump((vluint64_t)(2*cyc+1));
#endif
    cyc++;
    if (accept) {
        if (partial.empty()) frames_started++;
        for (int l = 0; l < 8; l++)
            if ((akeep >> l) & 1)
                partial.push_back((adata >> (8 * l)) & 0xFF);
        if (alast) { tx_frames.push_back(partial); partial.clear(); }
    }
    if ((int)dut->stream_gate_o != prev_gate) {
        trans.push_back({cyc, 'g', dut->stream_gate_o});
        prev_gate = dut->stream_gate_o;
    }
    if ((int)dut->slope_en_o != prev_slope) {
        trans.push_back({cyc, 's', dut->slope_en_o});
        prev_slope = dut->slope_en_o;
    }
}
static void run(long n) { for (long i = 0; i < n; i++) step(); }

// ---- bridge-side PDU builders (same encoding as the lwsrp_rx suite) ------
static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

// single-value listener / domain MSRP PDU
static std::vector<uint8_t> bridge_listener(int evt, int decl, int lva = 0) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C200000EULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x22EA, 2);
    f.push_back(0);
    f.push_back(3); f.push_back(8); put_be(f, 14, 2);        // type/len/listlen
    put_be(f, (uint64_t)((lva << 13) | 1), 2);
    put_be(f, OUR_SID, 8);
    f.push_back((uint8_t)(evt * 36));
    f.push_back((uint8_t)(decl * 64));
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

static std::vector<uint8_t> bridge_domain(int cls, int prio, int vid) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C200000EULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x22EA, 2);
    f.push_back(0);
    f.push_back(4); f.push_back(4); put_be(f, 9, 2);
    put_be(f, 1, 2);
    f.push_back(cls); f.push_back(prio); put_be(f, vid, 2);
    f.push_back(EV_JOININ * 36);
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

// single-value MVRP VID PDU (no AttributeListLength field in MVRP)
static std::vector<uint8_t> bridge_mvrp_vid(int evt, int lva = 0) {
    std::vector<uint8_t> f;
    put_be(f, 0x0180C2000021ULL, 6); put_be(f, BRIDGE, 6); put_be(f, 0x88F5, 2);
    f.push_back(0);
    f.push_back(1); f.push_back(2);                          // type/len
    put_be(f, (uint64_t)((lva << 13) | 1), 2);
    put_be(f, VID, 2);
    f.push_back((uint8_t)(evt * 36));
    put_be(f, 0, 2); put_be(f, 0, 2);
    while (f.size() < 60) f.push_back(0);
    return f;
}

// scan the transition recorder for a licence (gate) drop
static bool gate_dropped() {
    for (auto& t : trans)
        if (t.sig == 'g' && t.val == 0) return true;
    return false;
}

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

// ---- TX frame classification ---------------------------------------------
static bool is_msrp(const std::vector<uint8_t>& f) {
    return f.size() >= 14 && f[12] == 0x22 && f[13] == 0xEA;
}
static bool msrp_has_talker(const std::vector<uint8_t>& f) {
    return is_msrp(f) && f.size() >= 30 && f[28] == 0x01;
}
static void drain_tx() { tx_frames.clear(); }

int main(int argc, char** argv) {
#if VM_TRACE
    Verilated::traceEverOn(true);
#endif
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_top;
#if VM_TRACE
    tfp = new VerilatedVcdC;
    dut->trace(tfp, 99);
    tfp->open("wedge.vcd");
#endif

    dut->rst_n = 0; dut->enable_i = 0; dut->talker_en_i = 0; dut->is_1g_i = 0;
    dut->station_mac_i = STATION; dut->unique_id_i = UID;
    dut->dest_mac_i = 0x91E0F000FE02ULL; dut->vid_i = VID;
    dut->max_frame_i = MAXFRM; dut->interval_frames_i = 1;
    dut->latency_i = LATENCY;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0;
    dut->rx_tlast_i = 0;
    dut->m_axis_tready = 1;
    for (int i = 0; i < 8; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) step();

    printf("== KL_lwsrp_top harness (whole lwSRP engine, 10 kHz clock) ==\n");

    // 0) quiet while disabled
    run(3000);
    ck("disabled: no TX", tx_frames.size(), 0);
    ck("disabled: gate closed", dut->stream_gate_o, 0);

    // 1) enable + talker: prompt declare pair, then a pair per JoinTime.
    //    Cadence measured over TWO join periods (bench rule 7).
    dut->enable_i = 1; dut->talker_en_i = 1;
    run(3000);   // pair spans the 1024-cycle inter-frame gap (2026-07-19)
    ck("declare: prompt pair", tx_frames.size(), 2);
    ck("declare: MSRP first", tx_frames.size() && is_msrp(tx_frames[0]), 1);
    ck("declare: talker declared", dut->talker_declared_o, 1);
    if (tx_frames.size() >= 2) {
        ck("declare: TalkerAdvertise present", msrp_has_talker(tx_frames[0]), 1);
        ck("declare: MVRP second", is_msrp(tx_frames[1]), 0);
    }
    drain_tx();
    // MRP quiescence (2026-07-19): the applicant refreshes every 5th
    // JoinTime (1 s), not every tick - two periods must stay SILENT...
    run(2 * 2000 + 400);
    ck("quiesce: no re-declare within 2 periods", tx_frames.size(), 0);
    // ...and the 5th tick carries the slow refresh pair
    run(3 * 2000 + 400);
    ck("quiesce: 1-s refresh pair", tx_frames.size(), 2);
    drain_tx();

    // 2) Listener Ready -> reservation ACTIVE, slope-then-gate ordering
    trans.clear();
    feed(bridge_listener(EV_JOININ, D_READY));
    run(400);
    ck("active: listener_ready", dut->listener_ready_o, 1);
    ck("active: reservation", dut->res_active_o, 1);
    ck("active: slope_en", dut->slope_en_o, 1);
    ck("active: gate open", dut->stream_gate_o, 1);
    ck("active: idleSlope = (224+42)*64000", dut->idle_slope_o,
       (uint32_t)((MAXFRM + 42) * 64000));
    ck("active: within 100M budget", dut->over_limit_o, 0);
    // ordering: slope rise recorded before gate rise
    {
        long s_up = -1, g_up = -1;
        for (auto& t : trans) {
            if (t.sig == 's' && t.val == 1 && s_up < 0) s_up = t.cyc;
            if (t.sig == 'g' && t.val == 1 && g_up < 0) g_up = t.cyc;
        }
        ck("active: slope before gate", (s_up > 0 && g_up > s_up) ? 1 : 0, 1);
    }

    // 3) teardown by leave-timer expiry: gate-first ordering
    trans.clear();
    feed(bridge_listener(EV_LV, D_IGN));
    run(6000 + 600);       // LeaveTime + margin
    ck("teardown: deregistered", dut->listener_reg_o, 0);
    ck("teardown: reservation gone", dut->res_active_o, 0);
    ck("teardown: gate closed", dut->stream_gate_o, 0);
    ck("teardown: slope released", dut->slope_en_o, 0);
    {
        long g_dn = -1, s_dn = -1;
        for (auto& t : trans) {
            if (t.sig == 'g' && t.val == 0 && g_dn < 0) g_dn = t.cyc;
            if (t.sig == 's' && t.val == 0 && s_dn < 0) s_dn = t.cyc;
        }
        ck("teardown: gate before slope", (g_dn > 0 && s_dn > g_dn) ? 1 : 0, 1);
    }

    // 4) 75 % refusal on a live reservation (100 Mb/s port): interval x100
    feed(bridge_listener(EV_JOININ, D_READY));
    run(400);
    ck("refusal-setup: active again", dut->res_active_o, 1);
    trans.clear();
    dut->interval_frames_i = 500;   // (224+42)*500*64000 = 8.5 Gb/s >> 75 Mb/s
    run(400);
    ck("refusal: over_limit", dut->over_limit_o, 1);
    ck("refusal: reservation dropped", dut->res_active_o, 0);
    ck("refusal: gate closed", dut->stream_gate_o, 0);
    dut->interval_frames_i = 1;
    run(400);
    ck("refusal-heal: reservation back", dut->res_active_o, 1);

    // 5) received LeaveAll: prompt re-declare; registration must be
    //    refreshed by the listener or it ages out
    drain_tx();
    feed(bridge_listener(EV_MT, D_IGN, /*lva=*/1));
    run(3000);
    ck("rx-leaveall: prompt re-declare pair", tx_frames.size() >= 2 ? 1 : 0, 1);
    run(6200);             // no listener refresh -> ages out
    ck("rx-leaveall: aged out", dut->listener_reg_o, 0);
    ck("rx-leaveall: reservation gone", dut->res_active_o, 0);

    // 6) domain mismatch kills the reservation; heal restores it
    feed(bridge_listener(EV_JOININ, D_READY));
    run(400);
    ck("domain-setup: active", dut->res_active_o, 1);
    feed(bridge_domain(6, 2, VID));
    run(100);
    ck("domain-mismatch: boundary", dut->domain_ok_o, 0);
    ck("domain-mismatch: reservation dropped", dut->res_active_o, 0);
    feed(bridge_domain(6, 3, VID));
    run(100);
    ck("domain-heal: ok", dut->domain_ok_o, 1);
    ck("domain-heal: reservation back", dut->res_active_o, 1);

    // 7) our own LeaveAll turn: within LeaveAllTime the TX pair carries the
    //    LeaveAllEvent in the vector headers (byte 19 of the MSRP PDU)
    drain_tx();
    long deadline = cyc + 110000;
    bool lva_seen = false;
    while (cyc < deadline && !lva_seen) {
        step();
        while (!tx_frames.empty()) {
            auto f = tx_frames.front(); tx_frames.pop_front();
            if (is_msrp(f) && f.size() >= 21 && (f[19] & 0xE0) != 0)
                lva_seen = true;
        }
    }
    ck("leaveall-turn: fired within LeaveAllTime", lva_seen ? 1 : 0, 1);

    // 8) refresh keeps everything alive across the LeaveAll turn
    feed(bridge_listener(EV_JOININ, D_READY));
    run(400);
    ck("final: reservation active", dut->res_active_o, 1);
    ck("final: no drops", dut->rx_drops_o, 0);

    // ===========================================================
    // 9) MILAN v1.2 5.3.7.3 - THE LICENCE TO STREAM, term by term.
    //
    //   "As long as a PAAD is declaring a Talker Advertise attribute and
    //    receiving a Listener Ready or Listener Ready Failed attribute for
    //    a Stream Output, it shall be streaming AVTP packets. This
    //    specification excludes the possibility for a Stream Output to be
    //    stopped (STREAMING_WAIT state shall not be implemented)."
    //
    //   The obligation is CONDITIONAL, and stream_gate_o is the fabric's
    //   expression of the condition. Three registration states are possible
    //   (5.3.7.2: Ready/ReadyFailed, AskingFailed, or none) and only the
    //   first LICENSES streaming - so the gate must distinguish all three,
    //   and READY FAILED must open it just as Ready does. Measured on
    //   silicon 2026-07-28: with a bind up the ALINX read LWSRP_STATUS
    //   0x0000037E (reservation ACTIVE, gate open) and the tap counted
    //   18,012 tagged AAF frames in 6 s; after DISCONNECT_RX the same
    //   register read 0x00000030 and the tap counted ZERO.
    //
    //   Note what is NOT asserted here: that the applicant stops declaring.
    //   5.3.7.2 makes the Talker attribute unconditional ("shall always
    //   declare an MSRP Talker attribute as soon as it has valid SRP
    //   parameters"), so talker_declared_o must stay 1 throughout.
    // ==================================================================
    printf("-- Milan 5.3.7.3 licence to stream --\n");
    {
        // (a) no Listener attribute at all -> no licence
        feed(bridge_listener(EV_LV, D_IGN));
        run(6000 + 600);
        ck("5.3.7.3(a): no Listener attribute -> gate SHUT",
           dut->stream_gate_o, 0);
        ck("5.3.7.3(a): reservation not active", dut->res_active_o, 0);
        ck("5.3.7.2(a): Talker attribute still declared",
           dut->talker_declared_o, 1);

        // (b) Listener ASKING FAILED: registered, but NOT a licence
        feed(bridge_listener(EV_JOININ, D_ASKFAIL));
        run(400);
        ck("5.3.7.3(b): AskingFailed registers", dut->listener_reg_o, 1);
        ck("5.3.7.3(b): AskingFailed is NOT listener_ready",
           dut->listener_ready_o, 0);
        ck("5.3.7.3(b): gate stays SHUT on AskingFailed",
           dut->stream_gate_o, 0);
        ck("5.3.7.3(b): no slope claimed either", dut->slope_en_o, 0);

        // (c) Listener READY FAILED: the clause names it beside Ready, so
        //     it MUST open the gate. This is the leg a "reservation
        //     succeeded" reading of the fabric would get wrong.
        feed(bridge_listener(EV_JOININ, D_READYFAIL));
        run(400);
        ck("5.3.7.3(c): ReadyFailed is listener_ready",
           dut->listener_ready_o, 1);
        ck("5.3.7.3(c): gate OPEN on ReadyFailed", dut->stream_gate_o, 1);

        // (d) back to plain Ready, then withdraw: the licence follows the
        //     registration in both directions (R2 - the check can fail)
        feed(bridge_listener(EV_JOININ, D_READY));
        run(400);
        ck("5.3.7.3(d): gate OPEN on Ready", dut->stream_gate_o, 1);
        feed(bridge_listener(EV_JOININ, D_ASKFAIL));
        run(400);
        ck("5.3.7.3(d): Ready -> AskingFailed SHUTS the gate",
           dut->stream_gate_o, 0);
        ck("5.3.7.2(d): Talker attribute STILL declared",
           dut->talker_declared_o, 1);
    }
    // 10) STREAMING LICENCE vs LeaveAll (802.1Q Table 10-4): an MSRP
    //    LeaveAll puts the registration in leave-pending (LV), it does NOT
    //    flush it - re-declared within LeaveTime, the licence NEVER blinks
    //    (the silicon STREAM_START/STOP flap forensics, 2026-07-29).
    trans.clear();
    feed(bridge_listener(EV_MT, D_IGN, /*lva=*/1));   // pure LeaveAll
    run(3000);                                        // 300 ms into LV
    feed(bridge_listener(EV_JOININ, D_READY));        // bridge re-declares
    run(4000);                                        // past the 600 ms mark
    ck("la-hold: licence never dropped", gate_dropped() ? 1 : 0, 0);
    ck("la-hold: still registered", dut->listener_reg_o, 1);
    ck("la-hold: reservation active", dut->res_active_o, 1);

    // 11) LeaveAll scope is PER MRP APPLICATION (802.1Q 10.7.1/10.7.9: one
    //     Participant per application; a LeaveAll ages that Participant's
    //     registrars only). A bridge MVRP LeaveAll obliges NO MSRP Listener
    //     re-declare, so it must never age the MSRP registration - this is
    //     the licence-flap defect pin (STREAM_START=16/STOP=15 on silicon).
    trans.clear();
    feed(bridge_mvrp_vid(EV_JOININ, /*lva=*/1));
    run(7000);                                        // LeaveTime + margin
    ck("mvrp-la: licence never dropped", gate_dropped() ? 1 : 0, 0);
    ck("mvrp-la: still registered", dut->listener_reg_o, 1);
    ck("mvrp-la: reservation active", dut->res_active_o, 1);

    // 12) negative: an MSRP LeaveAll with NO re-declare within LeaveTime
    //     still deregisters (the Table 10-4 leavetimer! row survived the
    //     application-scope fix)
    feed(bridge_listener(EV_MT, D_IGN, /*lva=*/1));
    run(6600);
    ck("la-neg: aged out at LeaveTime", dut->listener_reg_o, 0);
    ck("la-neg: licence dropped", dut->stream_gate_o, 0);

    printf("\n-- [13] TX-wedge soak: hostile tready + LeaveAll turns + rx\n"
           "   LeaveAlls of BOTH applications at random offsets (m001a wedge\n"
           "   hunt: a frame-abort under stall holds the MAC arb grant) --\n");
    hostile_tready = 1;
    long f0 = (long)tx_frames.size();
    long viol0 = axis_viol;
    long last_frames = f0;
    int live_ok = 1;
    // 12 LeaveAll turns (LEAVEALL 10 s = 100k cycles at the 10 kHz scale),
    // with bridge LeaveAlls of both applications sprinkled mid-turn
    for (int turn = 0; turn < 12; turn++) {
        run(30000);
        if (turn % 3 == 0) feed(bridge_mvrp_vid(EV_JOININ, /*lva=*/1));
        run(30000);
        if (turn % 4 == 1) feed(bridge_listener(EV_JOININ, D_READY, /*lva=*/1));
        run(40000);
        long now_frames = (long)tx_frames.size();
        if (now_frames == last_frames) {   // liveness: JoinTime beats emit
            live_ok = 0;
            printf("   [turn %d] NO frames emitted this whole turn\n", turn);
        }
        last_frames = now_frames;
    }
    ck("[13a] TX liveness across 12 LeaveAll turns", live_ok, 1);
    ck("[13b] frames grew", (long)tx_frames.size() > f0, 1);
    ck("[13c] AXIS stability under stall (no mid-frame abort/mutate)",
       axis_viol - viol0, 0);
    ck("[13d] no partial frame left hanging", partial.empty() ? 1 : 0, 1);
    hostile_tready = 0; dut->m_axis_tready = 1;

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
