/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Self-checking harness for KL_acmp_responder.sv — the Milan v1.2 talker-side
 * ACMP PROBE_TX activation state machine (docs/design/MILAN_TALKER_SM.md;
 * reference: pipewire module-avb acmp-cmds-resps/acmp-milan-v12.c).
 *
 * Frames are built exactly as a controller would (byte-identical offsets to
 * the pipewire struct avb_packet_acmp) and fed through the little-lane RX
 * tap; responses are decoded from the little-lane TX AXIS.
 *
 * Contract under test:
 *  - CONNECT_TX_COMMAND == Milan PROBE_TX: SUCCESS + LIVE stream params
 *    (stream_id = {station_mac, uid} — must match the AVTP header), count=0,
 *    FAST_CONNECT|STREAMING_WAIT cleared (SRP_REG_FAILED preserved), arms
 *    the 15 s window (talker_active_o).
 *  - DISCONNECT_TX: always SUCCESS, ZEROED stream fields, flags ECHOED,
 *    NO state change (stays armed).
 *  - GET_TX_STATE: SUCCESS + LIVE params, count=0, all three flags cleared.
 *  - unique_id != 0 -> TALKER_UNKNOWN_ID with full echo.
 *  - GET_TX_CONNECTION -> NOT_SUPPORTED (Milan §5.5.4.4).
 *  - 15-tick expiry drops the arm unless listener_observed_i holds it.
 *  - foreign talker / response-typed messages ignored; back-pressure exact.
 */

#include "VKL_acmp_responder.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static VKL_acmp_responder* dut;
static long checks = 0, fails = 0;

static void ck(const char* what, uint64_t got, uint64_t exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-38s got=0x%llx exp=0x%llx\n", what,
               (unsigned long long)got, (unsigned long long)exp);
    }
}

static const uint64_t ENTITY_ID  = 0x020000FFFE000001ULL;
static const uint64_t CTRL_ID    = 0x6805CA95B2D10055ULL;
static const uint64_t STATION    = 0x020000FFFE01ULL;      // 48-bit
static const uint64_t AAF_DMAC   = 0x91E0F000FE01ULL;      // CSR reset default
static const uint16_t AAF_VID    = 2;
static const uint64_t LIVE_SID   = (STATION << 16);        // {mac, uid=0}

static void lo() { dut->clk_i = 0; dut->eval(); }
static void hi() { dut->clk_i = 1; dut->eval(); }
static void step() { lo(); hi(); }
static void tick() { dut->tick_1s_i = 1; step(); dut->tick_1s_i = 0; step(); }

static void put_be(std::vector<uint8_t>& b, uint64_t v, int n) {
    for (int i = n - 1; i >= 0; i--) b.push_back((v >> (8 * i)) & 0xFF);
}

// 70-byte ACMP command frame
static std::vector<uint8_t> acmp_cmd(int msg, uint64_t talker, uint16_t tuid,
                                     uint16_t seq, uint16_t flags = 0) {
    std::vector<uint8_t> b;
    put_be(b, 0x91E0F0010000ULL, 6);          // dst = ACMP multicast
    put_be(b, CTRL_ID >> 16, 6);              // src (any controller MAC)
    put_be(b, 0x22F0, 2);
    b.push_back(0xFC);                        // subtype
    b.push_back(msg & 0x0F);                  // sv=0/ver=0/msg
    put_be(b, 44, 2);                         // status=0 + cdl=44
    put_be(b, 0x1122334455667788ULL, 8);      // stream_id (controller junk)
    put_be(b, CTRL_ID, 8);
    put_be(b, talker, 8);
    put_be(b, 0xAABBCCDDEEFF0011ULL, 8);      // listener_entity_id
    put_be(b, tuid, 2);
    put_be(b, 7, 2);                          // listener_unique_id (echo test)
    put_be(b, 0x0EDC10000001ULL, 6);          // stream_dest_mac (junk)
    put_be(b, 3, 2);                          // connection_count (junk)
    put_be(b, seq, 2);
    put_be(b, flags, 2);
    put_be(b, 42, 2);                         // stream_vlan_id (junk)
    put_be(b, 0xBEEF, 2);                     // reserved (echo test)
    return b;
}

// drive the RX tap, little lane
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
    step();   // registered tap: flush the last beat
}

// capture one TX frame (little lane), optional toggling back-pressure
static std::vector<uint8_t> collect(int bp = 0, int maxc = 300) {
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

static uint64_t be(const std::vector<uint8_t>& b, int off, int n) {
    uint64_t v = 0; for (int i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

static void expect_silence(const char* what) {
    bool any = false;
    for (int c = 0; c < 60; c++) { lo(); if (dut->m_axis_tvalid) any = true; hi(); }
    ck(what, any ? 1 : 0, 0);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_acmp_responder;

    dut->rst_n = 0; dut->enable_i = 0; dut->m_axis_tready = 1;
    dut->station_mac_i = STATION; dut->entity_id_i = ENTITY_ID;
    dut->aaf_dmac_i = AAF_DMAC; dut->aaf_vid_i = AAF_VID;
    dut->tick_1s_i = 0; dut->listener_observed_i = 0;
    dut->rx_tvalid_i = 0; dut->rx_tdata_i = 0; dut->rx_tkeep_i = 0; dut->rx_tlast_i = 0;
    for (int i = 0; i < 4; i++) step();
    dut->rst_n = 1; dut->enable_i = 1;
    for (int i = 0; i < 2; i++) step();

    printf("== KL_acmp_responder harness (Milan PROBE_TX SM) ==\n");

    ck("idle: not armed", dut->probe_armed_o, 0);
    ck("idle: not active", dut->talker_active_o, 0);

    // 1) GET_TX_STATE, uid 0 -> SUCCESS, count 0, LIVE stream fields,
    //    FAST_CONNECT|STREAMING_WAIT|SRP_REG_FAILED (0x004A) all cleared
    feed(acmp_cmd(4, ENTITY_ID, 0, 0x0101, /*flags*/0x004A));
    auto r = collect();
    ck("frame length 70", r.size(), 70);
    if (r.size() == 70) {
        ck("dst = ACMP multicast", be(r, 0, 6), 0x91E0F0010000ULL);
        ck("src = station MAC", be(r, 6, 6), STATION);
        ck("subtype 0xFC", r[14], 0xFC);
        ck("msg = GET_TX_STATE_RESPONSE(5)", r[15] & 0x0F, 5);
        ck("sv/version = 0", r[15] >> 4, 0);
        ck("status SUCCESS", r[16] >> 3, 0);
        ck("CDL 44", ((r[16] & 7) << 8) | r[17], 44);
        ck("stream_id LIVE {mac,uid}", be(r, 18, 8), LIVE_SID);
        ck("controller echoed", be(r, 26, 8), CTRL_ID);
        ck("talker echoed", be(r, 34, 8), ENTITY_ID);
        ck("listener echoed", be(r, 42, 8), 0xAABBCCDDEEFF0011ULL);
        ck("talker_uid echoed", be(r, 50, 2), 0);
        ck("listener_uid echoed", be(r, 52, 2), 7);
        ck("stream_dest_mac LIVE", be(r, 54, 6), AAF_DMAC);
        ck("connection_count 0", be(r, 60, 2), 0);
        ck("sequence echoed", be(r, 62, 2), 0x0101);
        ck("flags all-three cleared", be(r, 64, 2), 0x0000);
        ck("vlan LIVE", be(r, 66, 2), AAF_VID);
        ck("reserved echoed", be(r, 68, 2), 0xBEEF);
    }
    ck("GET_TX_STATE does not arm", dut->probe_armed_o, 0);

    // 2) GET_TX_STATE, uid 5 -> TALKER_UNKNOWN_ID, body echoed
    feed(acmp_cmd(4, ENTITY_ID, 5, 0x0202));
    r = collect();
    ck("bad-uid frame length", r.size(), 70);
    if (r.size() == 70) {
        ck("bad-uid status TALKER_UNKNOWN_ID", r[16] >> 3, 2);
        ck("bad-uid stream_id echoed", be(r, 18, 8), 0x1122334455667788ULL);
        ck("bad-uid count echoed", be(r, 60, 2), 3);
        ck("bad-uid uid echoed", be(r, 50, 2), 5);
    }

    // 3) GET_TX_CONNECTION -> NOT_SUPPORTED (Milan 5.5.4.4)
    feed(acmp_cmd(12, ENTITY_ID, 0, 0x0303));
    r = collect();
    ck("gtc frame length", r.size(), 70);
    if (r.size() == 70) {
        ck("gtc msg = RESPONSE(13)", r[15] & 0x0F, 13);
        ck("gtc status NOT_SUPPORTED", r[16] >> 3, 31);
        ck("gtc sequence echoed", be(r, 62, 2), 0x0303);
    }

    // 4) PROBE_TX (wire CONNECT_TX, uid 0): SUCCESS + LIVE params + ARMS.
    //    flags 0x004A -> FAST_CONNECT(0x0002)|STREAMING_WAIT(0x0008) cleared,
    //    SRP_REG_FAILED(0x0040) PRESERVED (probe clears only two — reference)
    feed(acmp_cmd(0, ENTITY_ID, 0, 0x0404, /*flags*/0x004A));
    r = collect();
    ck("probe frame length", r.size(), 70);
    if (r.size() == 70) {
        ck("probe msg = CONNECT_TX_RESPONSE(1)", r[15] & 0x0F, 1);
        ck("probe status SUCCESS", r[16] >> 3, 0);
        ck("probe stream_id LIVE", be(r, 18, 8), LIVE_SID);
        ck("probe dest_mac LIVE", be(r, 54, 6), AAF_DMAC);
        ck("probe vlan LIVE", be(r, 66, 2), AAF_VID);
        ck("probe count 0", be(r, 60, 2), 0);
        ck("probe flags keep SRP_REG_FAILED", be(r, 64, 2), 0x0040);
        ck("probe sequence echoed", be(r, 62, 2), 0x0404);
    }
    ck("probe ARMS", dut->probe_armed_o, 1);
    ck("talker_active after probe", dut->talker_active_o, 1);

    // 5) DISCONNECT_TX uid 0: SUCCESS, ZEROED stream fields, flags ECHOED,
    //    NO state change (Milan 5.5.4.2 — not even deactivation)
    feed(acmp_cmd(2, ENTITY_ID, 0, 0x0505, /*flags*/0x004A));
    r = collect();
    ck("disc frame length", r.size(), 70);
    if (r.size() == 70) {
        ck("disc msg = RESPONSE(3)", r[15] & 0x0F, 3);
        ck("disc status SUCCESS", r[16] >> 3, 0);
        ck("disc stream_id zeroed", be(r, 18, 8), 0);
        ck("disc dest_mac zeroed", be(r, 54, 6), 0);
        ck("disc vlan zeroed", be(r, 66, 2), 0);
        ck("disc count 0", be(r, 60, 2), 0);
        ck("disc flags ECHOED", be(r, 64, 2), 0x004A);
    }
    ck("disconnect does NOT disarm", dut->probe_armed_o, 1);

    // 6) PROBE_TX uid 5 -> TALKER_UNKNOWN_ID
    feed(acmp_cmd(0, ENTITY_ID, 5, 0x0606));
    r = collect();
    ck("probe bad-uid status", r.size() == 70 ? (r[16] >> 3) : 0, 2);

    // 7) 15 s window: 14 ticks -> still armed; expiry at 15 -> disarmed
    for (int t = 0; t < 14; t++) tick();
    ck("armed at 14 ticks", dut->probe_armed_o, 1);
    tick();
    ck("disarmed at 15 ticks", dut->probe_armed_o, 0);
    ck("talker_active drops", dut->talker_active_o, 0);

    // 8) a fresh probe re-arms and resets the window
    feed(acmp_cmd(0, ENTITY_ID, 0, 0x0707));
    (void)collect();
    ck("re-armed", dut->probe_armed_o, 1);
    for (int t = 0; t < 14; t++) tick();
    feed(acmp_cmd(0, ENTITY_ID, 0, 0x0808));   // re-arm inside the window
    (void)collect();
    for (int t = 0; t < 14; t++) tick();
    ck("window restarted by mid-window probe", dut->probe_armed_o, 1);

    // 9) listener_observed holds the arm past expiry (SRP registrar rule)
    dut->listener_observed_i = 1;
    for (int t = 0; t < 5; t++) tick();        // cross the 15-tick boundary
    ck("armed held by listener", dut->probe_armed_o, 1);
    ck("active held by listener", dut->talker_active_o, 1);
    dut->listener_observed_i = 0;
    tick();
    ck("disarmed after listener leaves", dut->probe_armed_o, 0);

    // 10) listener_observed ALONE activates (no probe)
    dut->listener_observed_i = 1;
    dut->eval();
    ck("listener alone -> active", dut->talker_active_o, 1);
    dut->listener_observed_i = 0;
    dut->eval();

    // 11) other talker's command -> silence
    feed(acmp_cmd(4, 0xDEADBEEF00000001ULL, 0, 0x0909));
    expect_silence("other-talker command ignored");

    // 12) response-typed message (odd) -> silence
    feed(acmp_cmd(5, ENTITY_ID, 0, 0x0A0A));
    expect_silence("response message ignored");

    // 13) back-pressure: byte-exact under toggling tready
    feed(acmp_cmd(4, ENTITY_ID, 0, 0x0B0B));
    r = collect(/*bp=*/1);
    ck("bp frame length", r.size(), 70);
    if (r.size() == 70) {
        ck("bp status SUCCESS", r[16] >> 3, 0);
        ck("bp sequence echoed", be(r, 62, 2), 0x0B0B);
        ck("bp stream_id LIVE", be(r, 18, 8), LIVE_SID);
        ck("bp count 0", be(r, 60, 2), 0);
    }

    // 14) counters: 9 accepted commands (cases 1-6, the two re-arm probes,
    //     the bp query; the two ignored frames don't count)
    ck("cmd_count", dut->cmd_count_o, 9);
    ck("resp_count", dut->resp_count_o, 9);

    printf("--------------------------------------------------------------\n");
    printf("ACMP Milan talker SM: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
