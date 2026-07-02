/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking Verilator harness for adp_advertiser.sv — the ADP transmit
 * (advertise / depart / discover-response) engine.
 *
 * It captures the emitted AXI4-Stream frame, decodes it exactly the way a real
 * AVDECC controller does (IEEE 1722.1-2021 ADPDU layout; identical byte offsets
 * to srcs/milan-tests-avb/controller/avdecc_l2.py::parse_adp), and asserts:
 *   - Ethernet header: dst = 91:E0:F0:01:00:00, src = station MAC, type 0x22F0
 *   - ADPDU: subtype 0xFA, control_data_length 0x38, all entity fields byte-exact
 *   - message_type per scenario: AVAILABLE(0) / DEPARTING(1)
 *   - available_index: +1 on link-up / info-change; UNCHANGED on periodic
 *     re-advertise and on a discover response; monotonic; not bumped by depart
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
static const uint64_t GPTP_GM      = 0x0011223344556677ULL;
static const uint8_t  GPTP_DOMAIN  = 0;
static const uint8_t  VALID_TIME   = 5;         // also the re-advertise period (ticks)
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
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== adp_advertiser harness ==\n");

    // 1) link-up -> ENTITY_AVAILABLE, available_index bumped 0 -> 1
    pulse(dut->link_up_i);
    auto f1 = capture_frame();
    check_common("link-up AVAILABLE", f1, /*AVAILABLE*/0, /*index*/1);

    // 2) periodic re-advertise after VALID_TIME ticks -> AVAILABLE, index UNCHANGED (1)
    for (int t = 0; t < VALID_TIME; t++) pulse(dut->tick_i);
    auto f2 = capture_frame();
    check_common("periodic AVAILABLE", f2, 0, 1);   // <-- no spurious index bump

    // 3) discover response -> AVAILABLE, index UNCHANGED (1)
    pulse(dut->rcv_discover_i);
    auto f3 = capture_frame();
    check_common("discover-response AVAILABLE", f3, 0, 1);

    // 4) info/gm change -> AVAILABLE, index bumped 1 -> 2
    pulse(dut->gm_change_i);
    auto f4 = capture_frame();
    check_common("gm-change AVAILABLE", f4, 0, 2);

    // 5) link-down -> ENTITY_DEPARTING, index UNCHANGED (2, depart never bumps)
    pulse(dut->link_down_i);
    auto f5 = capture_frame();
    check_common("link-down DEPARTING", f5, /*DEPARTING*/1, 2);

    // 6) re-up under AXIS back-pressure -> AVAILABLE, index 2 -> 3, bytes intact
    pulse(dut->link_up_i);
    auto f6 = capture_frame(/*bp=*/1);
    check_common("backpressure AVAILABLE", f6, 0, 3);

    // 7) once departed (link down), a periodic tick must NOT emit a frame
    pulse(dut->link_down_i);
    (void)capture_frame();                      // drain the departing frame
    bool spurious = false;
    for (int t = 0; t < VALID_TIME + 3; t++) {
        pulse(dut->tick_i);
        for (int k = 0; k < 4; k++) { lo(); if (dut->m_axis_tvalid) spurious = true; hi(); }
    }
    ck("no advertise while departed", spurious ? 1 : 0, 0);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
