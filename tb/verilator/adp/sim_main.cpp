/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for adp_advertiser.sv — the ADP transmit
 * (advertise / depart / discover-response) engine.
 *
 * It captures the emitted AXI4-Stream frame, decodes it exactly the way a real
 * AVDECC controller does (IEEE 1722.1-2021 ADPDU layout; identical byte offsets
 * to srcs/the-private-test-repo/controller/avdecc_l2.py::parse_adp), and asserts:
 *   - Ethernet header: dst = 91:E0:F0:01:00:00, src = station MAC, type 0x22F0
 *   - ADPDU: subtype 0xFA, control_data_length 0x38, all entity fields byte-exact
 *   - message_type per scenario: AVAILABLE(0) / DEPARTING(1)
 *   - available_index: +1 on EVERY transmitted ADPDU: link-up, periodic
 *     re-advertise, discover response and depart (every ADPDU send bumps)
 *   - the periodic advertise timer fires after valid_time ticks
 *   - byte-for-byte integrity of the frame under AXIS back-pressure
 *
 * Exit 0 = pass, non-zero = fail.  (Verifies FR-DISC-01..04.)
 */

#include "Vadp_advertiser.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vadp_advertiser* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-30s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

// ---- entity model under test (distinctive values so byte errors are visible) ----
static const uint64_t ENTITY_ID    = 0xDEAD00BEEF00FEEDULL;
static const uint64_t MODEL_ID     = 0x001BC5FFFE000101ULL;
static const uint32_t ENT_CAPS     = 0x0000C588u;
static const uint16_t TALK_SRC     = 8, TALK_CAP = 0x0001;
static const uint16_t LIST_SNK     = 8, LIST_CAP = 0x0001;
static const uint32_t CTRL_CAPS    = 0x00000000u;
// mutable: case 14 re-provisions them for the GM-change scenario (ADP-9)
static uint64_t GPTP_GM      = 0x0011223344556677ULL;
static uint8_t  GPTP_DOMAIN  = 0;
static const uint8_t  VALID_TIME   = 5;
//! The re-advertise period is NOT valid_time: Milan v1.2 Table 5.50 makes
//! TMR_ADVERTISE "a timer with a fixed value of 5 seconds" and IEEE
//! 1722.1-2021 Figure 6-2 makes it MAX(1, valid_time/2) SECONDS, and the
//! engine takes the faster of the two = MIN(5, MAX(1, valid_time/2)).
static const int      ADV_PERIOD   = (VALID_TIME / 2) < 1 ? 1
                                   : ((VALID_TIME / 2) > 5 ? 5 : (VALID_TIME / 2));
static const uint64_t STATION_MAC  = 0x001BC5AABBCCULL;
static const uint16_t CUR_CFG = 0, IDENT_CTRL = 0, IFACE_IDX = 0;
static const uint64_t ASSOC_ID = 0;

static void apply_static_fields() {
    dut->station_mac_i                 = STATION_MAC;
    dut->valid_time_i                  = VALID_TIME;
    dut->entity_id_i                   = ENTITY_ID;
    dut->entity_model_id_i             = MODEL_ID;
    dut->entity_capabilities_i         = ENT_CAPS;
    dut->talker_stream_sources_i       = TALK_SRC;
    dut->talker_capabilities_i         = TALK_CAP;
    dut->listener_stream_sinks_i       = LIST_SNK;
    dut->listener_capabilities_i       = LIST_CAP;
    dut->controller_capabilities_i     = CTRL_CAPS;
    dut->gptp_grandmaster_id_i         = GPTP_GM;
    dut->gptp_domain_number_i          = GPTP_DOMAIN;
    dut->current_configuration_index_i = CUR_CFG;
    dut->identify_control_index_i      = IDENT_CTRL;
    dut->interface_index_i             = IFACE_IDX;
    dut->association_id_i              = ASSOC_ID;
}

static void clear_events() {
    dut->link_up_i = dut->link_down_i = dut->shutdown_i = 0;
    dut->gm_change_i = dut->info_changed_i = dut->rcv_discover_i = dut->tick_i = 0;
}
// link_level_i is a LEVEL (gates the dormancy self-re-arm); the pulses above
// stay the event interface. The TB keeps the level consistent with the pulses.

// two-phase clock; sample the sink during the low phase (stable, pre-edge)
static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

// Capture one frame, optionally applying a back-pressure pattern on tready.
// bp==0 -> tready always 1; bp==1 -> tready toggles (stress the handshake).
static std::vector<uint8_t> capture_frame(int bp = 0, int maxc = 400) {
    std::vector<uint8_t> b;
    bool started = false;
    int  phase = 0;
    for (int c = 0; c < maxc; c++) {
        int ready = bp ? (phase++ & 1) : 1;      // toggle when back-pressuring
        dut->m_axis_tready = ready;
        lo();                                     // outputs now reflect this beat
        if (dut->m_axis_tvalid && ready) {        // this beat is accepted at the edge
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
            started = true;
            bool last = dut->m_axis_tlast;
            hi();
            if (last) return b;
        } else {
            hi();
            if (started && !dut->m_axis_tvalid) return b;   // safety
        }
    }
    return b;
}

static void pulse(CData& sig) { sig = 1; step(); sig = 0; }   // 1-cycle event

// big-endian field readers over the captured wire bytes
static uint64_t be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | b[off + i]; return v;
}

// Decode + check the invariant Ethernet/ADPDU fields; return message_type & index.
static void check_common(const char* tag, const std::vector<uint8_t>& b,
                         int exp_msg, uint32_t exp_index) {
    printf("-- %s: %zu bytes, msg=%d, avail_index=%u\n", tag, b.size(),
           b.size() >= 16 ? (b[15] & 0x0F) : -1,
           b.size() >= 54 ? (unsigned)be(b, 50, 4) : 0u);
    ck("frame length", b.size(), 82);
    if (b.size() != 82) return;
    ck("dst mac", be(b, 0, 6), 0x91E0F0010000ULL);         // AVDECC ADP multicast
    ck("src mac", be(b, 6, 6), STATION_MAC);
    ck("ethertype", be(b, 12, 2), 0x22F0);
    ck("adp subtype", b[14], 0xFA);
    ck("message_type", b[15] & 0x0F, exp_msg);
    ck("sv/version", b[15] >> 4, 0x00);
    ck("valid_time", b[16] >> 3, VALID_TIME);
    ck("control_data_length", ((b[16] & 0x07) << 8) | b[17], 0x38);
    ck("entity_id", be(b, 18, 8), ENTITY_ID);
    ck("entity_model_id", be(b, 26, 8), MODEL_ID);
    ck("entity_capabilities", be(b, 34, 4), ENT_CAPS);
    ck("talker_stream_sources", be(b, 38, 2), TALK_SRC);
    ck("talker_capabilities", be(b, 40, 2), TALK_CAP);
    ck("listener_stream_sinks", be(b, 42, 2), LIST_SNK);
    ck("listener_capabilities", be(b, 44, 2), LIST_CAP);
    ck("controller_capabilities", be(b, 46, 4), CTRL_CAPS);
    ck("available_index", be(b, 50, 4), exp_index);
    ck("gptp_grandmaster_id", be(b, 54, 8), GPTP_GM);
    ck("gptp_domain_number", b[62], GPTP_DOMAIN);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vadp_advertiser;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    apply_static_fields(); clear_events();
    dut->link_level_i = 1;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== adp_advertiser harness ==\n");

    // Milan v1.2 5.6.3.5.2 "Startup of the PAAD-AE with link status up": an
    // enabled entity whose link is already up advertises BY ITSELF, with no
    // event. That is the first ADPDU of the session (index 1) and it is why
    // every index below is one higher than it was before 2026-07-30. It also
    // counts as a LEVEL arm in rearm_cnt (the STARTUP arm), which is the
    // documented A_ADP_DIAG reading change.
    auto f0 = capture_frame();
    check_common("STARTUP AVAILABLE (level arm, no event)", f0, 0, 1);
    ck("startup arm counted as a level arm", dut->rearm_cnt_o, 1);

    // available_index increments on EVERY transmitted ADPDU (IEEE 1722.1
    // §6.2.1.16 as enforced by la_avdecc/Hive — a repeated index makes the
    // controller treat the entity as offline/online-cycling; the pipewire
    // module-avb reference also bumps on every send).

    // 1) link-up -> ENTITY_AVAILABLE, available_index 0 -> 1
    pulse(dut->link_up_i);
    auto f1 = capture_frame();
    check_common("link-up AVAILABLE", f1, /*AVAILABLE*/0, /*index*/2);

    // 2) periodic re-advertise after VALID_TIME ticks -> AVAILABLE, 1 -> 2
    for (int t = 0; t < ADV_PERIOD; t++) pulse(dut->tick_i);
    auto f2 = capture_frame();
    check_common("periodic AVAILABLE", f2, 0, 3);   // every send bumps

    // 3) discover response -> AVAILABLE, 2 -> 3, but DELAYED (es-2.1): the
    //    entity must NOT answer instantly. Verify no frame for a few cycles,
    //    then the delayed response arrives.
    dut->rcv_discover_i = 1; step(); dut->rcv_discover_i = 0;
    {
        bool early = false;
        for (int c = 0; c < 3; c++) { step(); if (dut->m_axis_tvalid) early = true; }
        ck("discover: no INSTANT response (DELAY state)", early ? 1 : 0, 0);
    }
    auto f3 = capture_frame();
    check_common("discover-response AVAILABLE (delayed)", f3, 0, 4);

    // 3b) COALESCING: a burst of discovers during the delay window yields
    //     ONE response, not one-per-discover.
    for (int i = 0; i < 6; i++) { dut->rcv_discover_i = 1; step(); dut->rcv_discover_i = 0; }
    auto fb = capture_frame();
    check_common("discover burst -> one coalesced response", fb, 0, 5);
    {
        bool extra = false;
        for (int c = 0; c < 60; c++) { step(); if (dut->m_axis_tvalid) extra = true; }
        ck("discover burst: no extra responses after the one", extra ? 1 : 0, 0);
    }

    // 4) info/gm change -> AVAILABLE, 3 -> 4
    pulse(dut->gm_change_i);
    auto f4 = capture_frame();
    check_common("gm-change AVAILABLE", f4, 0, 6);

    // 5) link-down -> ENTITY_DEPARTING, 4 -> 5 (reference bumps on depart too)
    dut->link_level_i = 0;
    pulse(dut->link_down_i);
    auto f5 = capture_frame();
    check_common("link-down DEPARTING", f5, /*DEPARTING*/1, 7);

    // 6) re-up under AXIS back-pressure -> AVAILABLE, 5 -> 6, bytes intact
    dut->link_level_i = 1;
    pulse(dut->link_up_i);
    auto f6 = capture_frame(/*bp=*/1);
    check_common("backpressure AVAILABLE", f6, 0, 8);

    // 7) once departed with the link DOWN, a periodic tick must NOT emit a
    //    frame (and the dormancy self-re-arm must stay gated by link level)
    dut->link_level_i = 0;
    pulse(dut->link_down_i);
    (void)capture_frame();                      // drain the departing frame
    bool spurious = false;
    for (int t = 0; t < VALID_TIME + 3; t++) {
        pulse(dut->tick_i);
        for (int k = 0; k < 4; k++) { lo(); if (dut->m_axis_tvalid) spurious = true; hi(); }
    }
    ck("no advertise while departed", spurious ? 1 : 0, 0);

    // 8) link restored -> AVAILABLE, 7 -> 8 (case 7's depart was index 7)
    dut->link_level_i = 1;
    pulse(dut->link_up_i);
    auto f8 = capture_frame();
    check_common("link-restore AVAILABLE", f8, 0, 10);

    // 9) software depart (ADP_CMD[1]) with the link still UP -> DEPARTING, 9
    pulse(dut->shutdown_i);
    auto f9 = capture_frame();
    check_common("cmd DEPARTING", f9, 1, 11);

    // 10) DORMANCY SELF-RE-ARM (silicon 2026-07-13): enabled + link up but
    //     not available (whatever cleared available_r) -> after 2 ticks the
    //     advertiser re-arms itself and sends ENTITY_AVAILABLE. This is the
    //     bench failure mode: the Arty went dark mid-session and only an
    //     enable-edge poke revived it.
    pulse(dut->tick_i);                         // dormant tick 1: arm watchdog
    pulse(dut->tick_i);                         // dormant tick 2: re-arm fires
    auto f10 = capture_frame();
    check_common("dormancy self-re-arm AVAILABLE", f10, 0, 12);
    //! LEVEL arms are what rearm_cnt counts (it always did - the watchdog was
    //! one): 1 = the 5.6.3.5.2 STARTUP arm, 2 = case 8's link level returning,
    //! 3 = this post-depart heal.
    ck("rearm_cnt after self-heal", dut->rearm_cnt_o, 3);

    // 11) periodic advertising must be fully restored after a self-re-arm
    for (int t = 0; t < ADV_PERIOD; t++) pulse(dut->tick_i);
    auto f11 = capture_frame();
    check_common("periodic after re-arm", f11, 0, 13);

    // 12) DIAG counters: departs taken = case 5 + case 7 + case 9; last
    //     source = shutdown (bit1), not link_down (bit0)
    ck("depart_cnt", dut->depart_cnt_o, 3);
    ck("depart_src == shutdown", dut->depart_src_o, 2);

    // 13) the re-arm is honestly gated by enable_i: depart, disable, ticks ->
    //     silent; re-enable -> self-re-arm resumes advertising
    pulse(dut->shutdown_i);
    auto f13 = capture_frame();
    check_common("cmd DEPARTING pre-disable", f13, 1, 14);
    dut->enable_i = 0;
    bool spurious13 = false;
    for (int t = 0; t < 4; t++) {
        pulse(dut->tick_i);
        for (int k = 0; k < 4; k++) { lo(); if (dut->m_axis_tvalid) spurious13 = true; hi(); }
    }
    ck("no re-arm while disabled", spurious13 ? 1 : 0, 0);
    dut->enable_i = 1;
    pulse(dut->tick_i);
    pulse(dut->tick_i);
    auto f13b = capture_frame();
    check_common("re-arm after re-enable", f13b, 0, 15);
    ck("rearm_cnt after 2nd heal", dut->rearm_cnt_o, 4);

    // 14) GM CHANGE re-advertises the NEW grandmaster (traceability ADP-9 /
    //     M-ADP-2, IEEE 1722.1-2021 6.2.2.16-6.2.2.17 + Milan v1.2 5.6.3.5):
    //     the gPTP daemon rewrites gptp_grandmaster_id/domain (CSRs
    //     0x624/0x628) and pulses gm_change — the very next ADPDU must carry
    //     the NEW GM id + domain (a stale id misleads controllers diagnosing
    //     clock domains) and bump available_index (6.2.2.15). Case 4 above
    //     proved the re-advertise fires; this proves the FIELDS follow.
    //     Silicon note stays: gptp2csr publishes the LOCAL id when
    //     gmPresent=false — the field feed, not this engine.
    GPTP_GM     = 0xFEDCBA9876543210ULL;        // new grandmaster elected
    GPTP_DOMAIN = 3;
    dut->gptp_grandmaster_id_i = GPTP_GM;
    dut->gptp_domain_number_i  = GPTP_DOMAIN;
    pulse(dut->gm_change_i);
    auto f14 = capture_frame();
    check_common("gm-change advertises NEW GM fields", f14, 0, 16);
    // and the next PERIODIC advertise keeps carrying the new GM (no
    // one-shot latch of the old value anywhere in the serializer)
    for (int t = 0; t < ADV_PERIOD; t++) pulse(dut->tick_i);
    auto f14b = capture_frame();
    check_common("periodic after GM change keeps NEW GM", f14b, 0, 17);

    // ================================================================== //
    // 15) ENTITY_DISCOVER RESPONSE + the DIAG group 2 lanes.               //
    //     IEEE 1722.1-2021 6.2.7 Figure 6-5: an ENTITY_DISCOVER whose      //
    //     entity_id is 0 or ours reaches the DISCOVER state and sets       //
    //     needsAdvertise = TRUE; Figure 6-2 then routes that through DELAY //
    //     -> ADVERTISE -> WAITING, where "entityInfo.available_index =     //
    //     entityInfo.available_index + 1". The TARGET TEST is upstream in  //
    //     KL_aecp_ingress (it owns the RX bytes) and is locked in          //
    //     tb/verilator/aecp case 11b; this locks what the engine owes: a   //
    //     DELAYED, index-bumping ENTITY_AVAILABLE, and the A_ADP_DIAG2     //
    //     lanes that make it readable from one CSR read.                   //
    // ================================================================== //
    printf("\n-- [15] discover response + DIAG group 2\n");
    {
        uint32_t sent0 = dut->sent_cnt_o, drx0 = dut->disc_rx_cnt_o;
        ck("state.available before discover", dut->state_o & 1, 1);
        pulse(dut->rcv_discover_i);
        auto f15 = capture_frame();
        check_common("discover response (delayed, index+1)", f15, 0, 18);
        ck("disc_rx_cnt counted the discover", dut->disc_rx_cnt_o, drx0 + 1);
        ck("sent_cnt counted the response",    dut->sent_cnt_o,    sent0 + 1);
        ck("last_msg == ENTITY_AVAILABLE",     dut->last_msg_o,    0);
        ck("state idle after send (nothing busy/pending)", dut->state_o & 0xC, 0);

        // A DEPARTED entity has no Advertise Entity state machine to signal,
        // so a discover must produce NOTHING while the depart HOLD stands.
        // The DIAG still counts the arrival - "asked, and here is why we were
        // silent" is the whole point of the lane.
        pulse(dut->shutdown_i);
        auto f15d = capture_frame();
        check_common("depart before the negative case", f15d, 1, 19);
        ck("last_msg == ENTITY_DEPARTING", dut->last_msg_o, 1);
        ck("state.available == 0 after depart", dut->state_o & 1, 0);
        uint32_t drx1 = dut->disc_rx_cnt_o, sent1 = dut->sent_cnt_o;
        bool answered = false;
        for (int i = 0; i < 4; i++) pulse(dut->rcv_discover_i);
        for (int c = 0; c < 200; c++) { lo(); if (dut->m_axis_tvalid) answered = true; hi(); }
        ck("no discover response while departed", answered ? 1 : 0, 0);
        ck("disc_rx_cnt still witnesses the arrivals", dut->disc_rx_cnt_o, drx1 + 4);
        ck("sent_cnt unchanged while silent", dut->sent_cnt_o, sent1);
        // the depart HOLD expires after REARM_TICKS_C ticks and the LEVEL
        // re-arms us (5.6.3.5.2), which is the state the next case needs
        pulse(dut->tick_i); pulse(dut->tick_i);
        auto f15u = capture_frame();
        check_common("level re-arm after the depart hold", f15u, 0, 20);
    }

    // ================================================================== //
    // 16) DISCOVER STORM - 256 ENTITY_DISCOVERs back to back must not     //
    //     wedge the engine, must not emit one frame per discover, and     //
    //     must keep available_index a strictly +1 sequence (a repeated or //
    //     skipped index is what makes la_avdecc/Hive call an entity       //
    //     incoherent). Also crosses the 8-bit disc_rx_cnt DIAG wrap.      //
    // ================================================================== //
    printf("\n-- [16] discover storm: coalesced, coherent, no wedge\n");
    {
        const int STORM = 256;                  // exactly one 8-bit DIAG wrap
        uint32_t idx = 20, responses = 0;
        uint32_t drx0 = dut->disc_rx_cnt_o, sent0 = dut->sent_cnt_o;
        bool     order_ok = true, shape_ok = true;
        std::vector<uint8_t> cur;
        // ONE inline collector so the discover pulses stay exactly countable:
        // capture_frame() would eat cycles in which no discover is delivered.
        dut->m_axis_tready = 1;
        for (int c = 0; c < 4096; c++) {
            dut->rcv_discover_i = (c < STORM) ? 1 : 0;
            lo();
            bool beat = dut->m_axis_tvalid;
            bool last = dut->m_axis_tlast;
            if (beat)
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_tkeep >> l) & 1)
                        cur.push_back((dut->m_axis_tdata >> (8 * l)) & 0xFF);
            hi();
            if (beat && last) {
                responses++;
                if (cur.size() != 82 || (cur[15] & 0x0F) != 0) shape_ok = false;
                if (cur.size() >= 54 && be(cur, 50, 4) != idx + 1) order_ok = false;
                idx++;
                cur.clear();
            }
        }
        dut->rcv_discover_i = 0;
        printf("   storm: %d discovers -> %u responses, last index %u\n",
               STORM, responses, idx);
        ck("storm: at least one response", responses >= 1, 1);
        ck("storm: COALESCED (fewer responses than discovers)", responses < STORM, 1);
        ck("storm: every response a well-formed AVAILABLE", shape_ok ? 1 : 0, 1);
        ck("storm: available_index strictly +1, never repeated", order_ok ? 1 : 0, 1);
        ck("storm: disc_rx_cnt wrapped exactly once through 256",
           dut->disc_rx_cnt_o, drx0);           // +256 on an 8-bit lane == same value
        ck("storm: sent_cnt tracks the responses",
           dut->sent_cnt_o, (sent0 + responses) & 0xFF);
        ck("storm: engine idle afterwards (no wedge)", dut->state_o & 0xC, 0);
        ck("storm: still available", dut->state_o & 1, 1);
        // the periodic contract must survive the storm
        for (int t = 0; t < ADV_PERIOD; t++) pulse(dut->tick_i);
        auto fp = capture_frame();
        check_common("periodic advertise survives the storm", fp, 0, idx + 1);
    }

    // ================================================================== //
    // 17) COLD BOOT ORDER, tested instead of assumed: reset, arm enable   //
    //     with the link DOWN, then bring the link level up and touch      //
    //     NOTHING else - no link_up pulse, no tick, no CSR write. Milan   //
    //     v1.2 5.6.3.5.2 "Startup of the PAAD-AE with link status up"     //
    //     makes that advertise mandatory, and it is the S50 boot-order    //
    //     claim reduced to RTL: if this passes, flash_verify.sh's devmem  //
    //     toggle is belt-and-braces rather than load-bearing.             //
    // ================================================================== //
    printf("\n-- [17] cold boot: arm before link, advertise with NO event at all\n");
    {
        dut->rst_n = 0; dut->enable_i = 0; clear_events(); dut->link_level_i = 0;
        for (int i = 0; i < 4; i++) step();
        dut->rst_n = 1;
        for (int i = 0; i < 4; i++) step();          // reset released, link down
        dut->enable_i = 1;                            // S50 arms ADP first...
        bool early = false;
        for (int c = 0; c < 60; c++) { lo(); if (dut->m_axis_tvalid) early = true; hi(); }
        ck("no advertise while the link is down", early ? 1 : 0, 0);
        ck("available_index reset to 0 by the reset", dut->available_index_o, 0);
        ck("state.available == 0 with the link down", dut->state_o & 1, 0);
        dut->link_level_i = 1;                        // ...the link comes up LATE
        auto f17 = capture_frame();                   // no pulse, no tick, no write
        check_common("cold-boot AVAILABLE from the LEVEL alone", f17, 0, 1);
        ck("sent_cnt from a cold boot", dut->sent_cnt_o, 1);
        ck("depart_cnt clean on a cold boot", dut->depart_cnt_o, 0);
        ck("state.available == 1 once up", dut->state_o & 1, 1);
    }

    // ================================================================== //
    // 18) LONG-RUN ADVERTISE LOCK - documents PROVEN-GOOD silicon         //
    //     behaviour (2026-07-30 wire capture: ADPDUs at exactly 10.000 s  //
    //     spacing with available_index 2681 -> 2682 -> 2683, i.e. ~7.4 h  //
    //     unbroken) at the CLAUSE period this engine now keeps.           //
    //                                                                     //
    //     CYCLE ARITHMETIC against the real widths and reloads:           //
    //       valid_time_i = 31 = the ADP_CTRL reset value. The period is    //
    //         MIN(5, MAX(1, valid_time/2)) = 5 ticks (Milan Table 5.50's   //
    //         fixed 5 s; 1722.1 Figure 6-2 would allow 15 s here).        //
    //       5400 cycles = 27,000 ticks. tick_i is 1 s in the integration   //
    //         (ADP_TICK_DIV = MILAN_CLK_FREQ_HZ), so this is 7.5 HOURS of  //
    //         silicon wall time - the span the bench capture covered.      //
    //       adv_tick_cnt_r is 5 bits reloading at 5: 5400 laps, so any     //
    //         off-by-one or wrap in the reload compare shows up.          //
    //       sent_cnt_o is 8 bits: 5400 sends = 21 full wraps, proving the  //
    //         DIAG liveness lane keeps counting past 255.                 //
    //       available_index_o is 32 bits and must simply keep going: no    //
    //         reset, no repeat, +1 per ADPDU (6.2.2.15).                   //
    // ================================================================== //
    printf("\n-- [18] long run: 5400 advertise cycles at valid_time 31 (= 7.5 h)\n");
    {
        const int CYCLES = 5400;
        dut->valid_time_i = 31;                  // the ADP_CTRL reset value
        for (int i = 0; i < 2; i++) step();
        uint32_t expect = dut->available_index_o;
        uint32_t frames = 0, gaps = 0, bad = 0;
        for (int cyc = 0; cyc < CYCLES; cyc++) {
            for (int t = 0; t < 5; t++) pulse(dut->tick_i);   // MIN(5, 31/2) = 5
            auto f = capture_frame();
            if (f.size() != 82) { bad++; break; }
            expect++;
            if (be(f, 50, 4) != expect) gaps++;
            if ((f[15] & 0x0F) != 0 || (f[16] >> 3) != 31) bad++;
            frames++;
        }
        printf("   long run: %u frames, last index %u, gaps %u, malformed %u\n",
               frames, expect, gaps, bad);
        ck("long run: 5400 ADPDUs kept coming", frames, CYCLES);
        ck("long run: every frame 82 B AVAILABLE with valid_time 31", bad, 0);
        ck("long run: available_index +1 every frame, never reset", gaps, 0);
        ck("long run: sent_cnt wrapped 21x and still tracks",
           dut->sent_cnt_o, (uint32_t)((1 + CYCLES) & 0xFF));  // +1 = case 17's boot frame
        ck("long run: no departs invented", dut->depart_cnt_o, 0);
        ck("long run: still available at the end", dut->state_o & 1, 1);
        // and still responsive to a discover after 7.5 simulated hours
        pulse(dut->rcv_discover_i);
        auto f18 = capture_frame();
        ck("discover still answered after 7.5 h", f18.size(), 82);
        ck("...and it bumped the index",
           f18.size() >= 54 ? be(f18, 50, 4) : 0, expect + 1);
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
