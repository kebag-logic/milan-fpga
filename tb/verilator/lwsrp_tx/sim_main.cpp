/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_lwsrp_tx.sv — the lwSRP applicant transmit
 * engine (docs/LWSRP_FPGA_ARCHITECTURE.md §3; byte contract extracted from
 * pipewire module-avb mrp.c/msrp.c/mvrp.c 2026-07-14).
 *
 * Frames are decoded the way the reference bridge-side parser walks them:
 * version octet, then messages terminated by the 0x0000 message-list EndMark,
 * vectors terminated by their own EndMark (AttributeListLength is written on
 * MSRP but never trusted for framing — mrp.c parses purely by endmarks).
 *
 * Contract under test:
 *  - enable rising edge -> prompt declare: MSRP {Domain NEW} + MVRP {VID NEW},
 *    zero-padded to 60 B; every field byte-exact.
 *  - join tick -> refresh pair, JOININ everywhere.
 *  - talker enable -> MSRP gains TalkerAdvertise (NEW, then JOININ); frame is
 *    exactly 64 B; StreamID = {station_mac, uid}; PriorityAndRank = 0x70;
 *    AttributeListLength 9 (Domain) / 30 (TalkerAdvertise).
 *  - our LeaveAll turn -> BOTH next PDUs carry LeaveAllEvent (vector header
 *    0x2001), one pair only.
 *  - received LeaveAll -> prompt re-declare (JOININ, no LeaveAllEvent).
 *  - talker disable -> one TalkerAdvertise LV (Domain stays JOININ), then the
 *    talker message disappears; talker_declared_o tracks the wire.
 *  - engine disable -> Domain LV + MVRP VID LV, then silence on join ticks.
 *  - back-pressure toggling mid-frame keeps frames byte-exact.
 */

#include "VKL_lwsrp_tx.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_lwsrp_tx* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-44s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t STATION  = 0x020000000002ULL;   // arty :02
static const uint16_t UID      = 0;
static const uint64_t DMAC     = 0x91E0F000FE02ULL;
static const uint16_t VID      = 2;
static const uint16_t MAXFRM   = 224;
static const uint16_t IVFRM    = 1;
static const uint32_t LATENCY  = 500000;

// MRP AttributeEvent three-pack octets (single value: e*36)
static const uint8_t EV_NEW = 0 * 36, EV_JOININ = 1 * 36, EV_LV = 5 * 36;

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }
static void pulse(uint8_t& sig) { sig = 1; step(); sig = 0; step(); }
// MRP quiescence (2026-07-19): the applicant refreshes every 5th JoinTime.
// After enable (or a previous fire) jdiv sits at 1: four ticks are silent,
// the fifth fires. prime4() spends the silent ones.
static void prime4() { for (int i = 0; i < 4; i++) pulse(dut->join_tick_i); }

// capture one TX frame (little lane), optional toggling back-pressure
static std::vector<uint8_t> collect(int bp = 0, int maxc = 6000) {
    std::vector<uint8_t> b;
    int phase = 0;
    for (int c = 0; c < maxc; c++) {
        int rdy = bp ? (phase++ & 1) : 1;
        dut->m_axis_tready = rdy;
        lo();
        if (dut->m_axis_tvalid && rdy) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
            bool last = dut->m_axis_tlast;
            hi();
            if (last) { dut->m_axis_tready = 1; return b; }
        } else {
            hi();
        }
    }
    dut->m_axis_tready = 1;
    return b;
}

static void expect_silence(const char* what, int cyc = 80) {
    bool any = false;
    for (int c = 0; c < cyc; c++) { lo(); if (dut->m_axis_tvalid) any = true; hi(); }
    ck(what, any ? 1 : 0, 0);
}

static uint64_t be(const std::vector<uint8_t>& b, size_t off, int n) {
    uint64_t v = 0;
    if (off + n > b.size()) return ~0ULL;   // clean mismatch, never UB
    for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

// ---- bridge-style checks on one MSRP PDU -------------------------------
// talker_ev < 0 : expect NO TalkerAdvertise message.
static void check_msrp(const char* tag, const std::vector<uint8_t>& f,
                       int domain_ev, int talker_ev, int lva) {
    char w[96];
    const uint16_t vech = (lva ? 0x2000 : 0x0000) | 1;
    const bool talker = talker_ev >= 0;
    snprintf(w, sizeof w, "%s: frame length", tag);
    ck(w, f.size(), talker ? 64 : 60);
    if (f.size() < 30) return;
    snprintf(w, sizeof w, "%s: dst MAC", tag);
    ck(w, be(f, 0, 6), 0x0180C200000EULL);
    snprintf(w, sizeof w, "%s: src MAC", tag);
    ck(w, be(f, 6, 6), STATION);
    snprintf(w, sizeof w, "%s: ethertype", tag);
    ck(w, be(f, 12, 2), 0x22EA);
    snprintf(w, sizeof w, "%s: protocol version", tag);
    ck(w, f[14], 0);
    // Message 1: Domain
    snprintf(w, sizeof w, "%s: domain attr type/len", tag);
    ck(w, be(f, 15, 2), 0x0404);
    snprintf(w, sizeof w, "%s: domain AttributeListLength", tag);
    ck(w, be(f, 17, 2), 9);
    snprintf(w, sizeof w, "%s: domain vector header", tag);
    ck(w, be(f, 19, 2), vech);
    snprintf(w, sizeof w, "%s: domain class/prio/vid", tag);
    ck(w, be(f, 21, 4), 0x06030000ULL | VID);
    snprintf(w, sizeof w, "%s: domain event octet", tag);
    ck(w, f[25], (uint8_t)domain_ev);
    snprintf(w, sizeof w, "%s: domain vector EndMark", tag);
    ck(w, be(f, 26, 2), 0);
    if (!talker) {
        snprintf(w, sizeof w, "%s: message-list EndMark", tag);
        ck(w, be(f, 28, 2), 0);
        snprintf(w, sizeof w, "%s: padding zero", tag);
        ck(w, be(f, 30, 8) | be(f, 52, 8), 0);
        return;
    }
    // Message 2: TalkerAdvertise
    snprintf(w, sizeof w, "%s: talker attr type/len", tag);
    ck(w, be(f, 28, 2), 0x0119);
    snprintf(w, sizeof w, "%s: talker AttributeListLength", tag);
    ck(w, be(f, 30, 2), 30);
    snprintf(w, sizeof w, "%s: talker vector header", tag);
    ck(w, be(f, 32, 2), vech);
    snprintf(w, sizeof w, "%s: StreamID {mac,uid}", tag);
    ck(w, be(f, 34, 8), (STATION << 16) | UID);
    snprintf(w, sizeof w, "%s: stream dest MAC", tag);
    ck(w, be(f, 42, 6), DMAC);
    snprintf(w, sizeof w, "%s: DataFrameParameters VID", tag);
    ck(w, be(f, 48, 2), VID);
    snprintf(w, sizeof w, "%s: TSpec MaxFrameSize", tag);
    ck(w, be(f, 50, 2), MAXFRM);
    snprintf(w, sizeof w, "%s: TSpec MaxIntervalFrames", tag);
    ck(w, be(f, 52, 2), IVFRM);
    snprintf(w, sizeof w, "%s: PriorityAndRank", tag);
    ck(w, f[54], 0x70);
    snprintf(w, sizeof w, "%s: AccumulatedLatency", tag);
    ck(w, be(f, 55, 4), LATENCY);
    snprintf(w, sizeof w, "%s: talker event octet", tag);
    ck(w, f[59], (uint8_t)talker_ev);
    snprintf(w, sizeof w, "%s: talker vector EndMark", tag);
    ck(w, be(f, 60, 2), 0);
    snprintf(w, sizeof w, "%s: message-list EndMark", tag);
    ck(w, be(f, 62, 2), 0);
}

// ---- bridge-style checks on one MVRP PDU -------------------------------
static void check_mvrp(const char* tag, const std::vector<uint8_t>& f,
                       int vid_ev, int lva) {
    char w[96];
    const uint16_t vech = (lva ? 0x2000 : 0x0000) | 1;
    snprintf(w, sizeof w, "%s: frame length", tag);
    ck(w, f.size(), 60);
    if (f.size() < 26) return;
    snprintf(w, sizeof w, "%s: dst MAC", tag);
    ck(w, be(f, 0, 6), 0x0180C2000021ULL);
    snprintf(w, sizeof w, "%s: src MAC", tag);
    ck(w, be(f, 6, 6), STATION);
    snprintf(w, sizeof w, "%s: ethertype", tag);
    ck(w, be(f, 12, 2), 0x88F5);
    snprintf(w, sizeof w, "%s: protocol version", tag);
    ck(w, f[14], 0);
    snprintf(w, sizeof w, "%s: vid attr type/len (no listlen)", tag);
    ck(w, be(f, 15, 2), 0x0102);
    snprintf(w, sizeof w, "%s: vector header", tag);
    ck(w, be(f, 17, 2), vech);
    snprintf(w, sizeof w, "%s: VID FirstValue", tag);
    ck(w, be(f, 19, 2), VID);
    snprintf(w, sizeof w, "%s: event octet", tag);
    ck(w, f[21], (uint8_t)vid_ev);
    snprintf(w, sizeof w, "%s: vector EndMark", tag);
    ck(w, be(f, 22, 2), 0);
    snprintf(w, sizeof w, "%s: message-list EndMark", tag);
    ck(w, be(f, 24, 2), 0);
    snprintf(w, sizeof w, "%s: padding zero", tag);
    ck(w, be(f, 26, 8) | be(f, 52, 8), 0);
}

// ---- Listener-message checks (position depends on TalkerAdvertise) -----
static const uint64_t LSID = 0x0200000000010000ULL;   // bound talker stream
static void check_lstn_msg(const char* tag, const std::vector<uint8_t>& f,
                           size_t lb, int lstn_ev, int decl, int lva) {
    char w[96];
    const uint16_t vech = (lva ? 0x2000 : 0x0000) | 1;
    snprintf(w, sizeof w, "%s: lstn attr type/len", tag);
    ck(w, be(f, lb, 2), 0x0308);
    snprintf(w, sizeof w, "%s: lstn AttributeListLength", tag);
    ck(w, be(f, lb+2, 2), 14);
    snprintf(w, sizeof w, "%s: lstn vector header", tag);
    ck(w, be(f, lb+4, 2), vech);
    snprintf(w, sizeof w, "%s: lstn StreamID (bound)", tag);
    ck(w, be(f, lb+6, 8), LSID);
    snprintf(w, sizeof w, "%s: lstn event octet", tag);
    ck(w, f[lb+14], (uint8_t)lstn_ev);
    snprintf(w, sizeof w, "%s: lstn 4-packed declaration", tag);
    ck(w, f[lb+15], (uint8_t)(decl << 6));
    snprintf(w, sizeof w, "%s: lstn vector EndMark", tag);
    ck(w, be(f, lb+16, 2), 0);
    snprintf(w, sizeof w, "%s: message-list EndMark", tag);
    ck(w, be(f, lb+18, 2), 0);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_tx;

    dut->rst_n = 0; dut->enable_i = 0; dut->talker_en_i = 0;
    dut->join_tick_i = 0; dut->leaveall_tick_i = 0; dut->rx_leaveall_i = 0;
    dut->m_axis_tready = 1;
    dut->station_mac_i = STATION; dut->unique_id_i = UID;
    dut->dest_mac_i = DMAC; dut->vid_i = VID;
    dut->max_frame_i = MAXFRM; dut->interval_frames_i = IVFRM;
    dut->latency_i = LATENCY;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== KL_lwsrp_tx harness (lwSRP applicant TX) ==\n");

    // 0) disabled: silence, nothing declared
    expect_silence("disabled: silent");
    ck("disabled: not declared", dut->talker_declared_o, 0);
    dut->join_tick_i = 1; step(); dut->join_tick_i = 0;
    expect_silence("disabled: join tick ignored");

    // 1) enable (talker off) -> prompt NEW declare pair, padded to 60 B
    dut->enable_i = 1; step(); step();
    // fast state acquisition (2026-07-19): the enable pair carries LeaveAll
    // so the bridge re-declares its registrations to us within a join-time
    check_msrp("declare", collect(), EV_NEW, -1, 1);
    check_mvrp("declare", collect(), EV_NEW, 1);
    ck("declare: talker not declared", dut->talker_declared_o, 0);
    expect_silence("declare: one pair only");
    ck("declare: tx_count", dut->tx_count_o, 2);

    // 2) join tick -> JOININ refresh pair
    prime4(); pulse(dut->join_tick_i);
    check_msrp("refresh", collect(), EV_JOININ, -1, 0);
    check_mvrp("refresh", collect(), EV_JOININ, 0);

    // 3) talker enable -> prompt MSRP with TalkerAdvertise NEW (64 B)
    dut->talker_en_i = 1; step(); step();
    check_msrp("talker-new", collect(), EV_JOININ, EV_NEW, 0);
    ck("talker-new: declared", dut->talker_declared_o, 1);
    expect_silence("talker-new: single frame");

    //    ...then JOININ on the next tick, with back-pressure
    prime4(); pulse(dut->join_tick_i);
    check_msrp("talker-refresh (bp)", collect(1), EV_JOININ, EV_JOININ, 0);
    check_mvrp("talker-refresh (bp)", collect(1), EV_JOININ, 0);

    // 4) our LeaveAll turn -> exactly one pair with LeaveAllEvent set
    pulse(dut->leaveall_tick_i);
    check_msrp("leaveall-turn", collect(), EV_JOININ, EV_JOININ, 1);
    check_mvrp("leaveall-turn", collect(), EV_JOININ, 1);
    prime4(); pulse(dut->join_tick_i);
    check_msrp("post-leaveall", collect(), EV_JOININ, EV_JOININ, 0);
    check_mvrp("post-leaveall", collect(), EV_JOININ, 0);

    // 5) received LeaveAll -> prompt re-declare (JOININ, no LeaveAllEvent)
    pulse(dut->rx_leaveall_i);
    check_msrp("rx-leaveall redeclare", collect(), EV_JOININ, EV_JOININ, 0);
    check_mvrp("rx-leaveall redeclare", collect(), EV_JOININ, 0);

    // 6) talker disable -> one LV for the talker attr, domain stays JOININ
    dut->talker_en_i = 0; step(); step();
    check_msrp("talker-lv", collect(), EV_JOININ, EV_LV, 0);
    ck("talker-lv: not declared", dut->talker_declared_o, 0);
    prime4(); pulse(dut->join_tick_i);
    check_msrp("post-talker-lv", collect(), EV_JOININ, -1, 0);
    check_mvrp("post-talker-lv", collect(), EV_JOININ, 0);

    // 7) re-enable the talker: NEW again (fresh declare after withdraw)
    dut->talker_en_i = 1; step(); step();
    check_msrp("talker-renew", collect(), EV_JOININ, EV_NEW, 0);

    // 8) engine disable -> Domain LV + talker LV, MVRP LV, then silence
    dut->enable_i = 0; dut->talker_en_i = 0; step(); step();
    check_msrp("engine-lv", collect(), EV_LV, EV_LV, 0);
    check_mvrp("engine-lv", collect(), EV_LV, 0);
    ck("engine-lv: not declared", dut->talker_declared_o, 0);
    dut->join_tick_i = 1; step(); dut->join_tick_i = 0;
    expect_silence("disabled again: join tick ignored");

    // 9) re-enable: fresh NEW pair again (state fully re-armed)
    dut->enable_i = 1; step(); step();
    check_msrp("re-declare", collect(), EV_NEW, -1, 1);
    check_mvrp("re-declare", collect(), EV_NEW, 1);

    // 10) listener declare (Ready): prompt MSRP with the Listener message
    //     after Domain (talker off -> 60-byte padded frame, lstn at 28)
    dut->lstn_sid_i = LSID; dut->lstn_ready_i = 1;
    dut->lstn_declare_i = 1; step(); step();
    {
        auto f = collect();
        ck("lstn-new: frame length", f.size(), 60);
        // a NEW binding fires the fast-join LeaveAll pair
        check_lstn_msg("lstn-new", f, 28, EV_NEW, 2 /*READY*/, 1);
        ck("lstn-new: declared", dut->lstn_declared_o, 1);
        (void)collect();   // the MVRP half of the fast-join pair
    }
    prime4(); pulse(dut->join_tick_i);
    check_lstn_msg("lstn-refresh", collect(), 28, EV_JOININ, 2, 0);
    (void)collect();   // the MVRP half of the refresh pair

    // 11) Ready -> AskingFailed re-declares promptly with the new 4-pack
    dut->lstn_ready_i = 0; step(); step();
    check_lstn_msg("lstn-askfail", collect(), 28, EV_JOININ, 1, 0);
    dut->lstn_ready_i = 1; step(); step();
    (void)collect();   // back-to-Ready re-declare

    // 12) talker on too: the 82-byte 3-message MSRP (Domain+TA+Listener)
    dut->talker_en_i = 1; step(); step();
    {
        auto f = collect();
        ck("triple: frame length", f.size(), 82);
        check_lstn_msg("triple", f, 62, EV_JOININ, 2, 0);
        ck("triple: talker StreamID", be(f, 34, 8), (STATION << 16) | UID);
        ck("triple: talker event NEW", f[59], EV_NEW);
    }

    // 13) listener withdraw: LV frame (domain JOININ, no talker msg), then
    //     the next refresh has no Listener message (64-byte talker frame)
    dut->lstn_declare_i = 0; step(); step();
    {
        auto f = collect();
        ck("lstn-lv: frame length", f.size(), 60);
        check_lstn_msg("lstn-lv", f, 28, EV_LV, 2, 0);
        ck("lstn-lv: not declared", dut->lstn_declared_o, 0);
    }
    prime4(); pulse(dut->join_tick_i);
    check_msrp("post-lstn-lv", collect(), EV_JOININ, EV_JOININ, 0);
    (void)collect();   // MVRP half

    // 14) engine disable with talker+listener declared: 82-byte all-LV
    dut->lstn_declare_i = 1; step(); step();
    (void)collect();   // listener re-declare
    dut->enable_i = 0; dut->talker_en_i = 0; dut->lstn_declare_i = 0;
    step(); step();
    {
        auto f = collect();
        ck("engine-lv3: frame length", f.size(), 82);
        ck("engine-lv3: domain LV", f[25], EV_LV);
        ck("engine-lv3: talker LV", f[59], EV_LV);
        check_lstn_msg("engine-lv3", f, 62, EV_LV, 2, 0);
    }
    (void)collect();   // MVRP LV

    printf("== %ld checks, %ld failures ==\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
