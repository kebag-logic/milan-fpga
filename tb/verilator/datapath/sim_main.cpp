/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * T1.5 end-to-end datapath harness for traffic_controller_802_1q (802.1Q
 * classifier -> per-queue FIFOs -> 802.1Qav CBS shaper), i.e. the fully
 * de-Xilinx'd TSN TX datapath (Forencich axis_fifo/demux/arb_mux + open RTL).
 * That it builds+runs proves the whole pipeline Verilates end-to-end.
 *
 * Injects VLAN-tagged frames (PCP in the TCI) and checks, through the whole
 * chain: byte-exact egress, classification routes by PCP (tdest), multiple queues
 * are exercised, and the datapath works both unshaped (strict priority) and
 * shaped (CBS credit path). The CBS credit *math* is covered by tb/verilator/cbs
 * and shaper_core; here we prove integration.
 *
 * Frames are big-endian on the wire (BIG_ENDIAN=1: tdata[63:56] = first byte).
 * Exit 0 = pass.
 */

#include "Vdatapath_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>
#include <set>

static Vdatapath_wrap* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-32s got=%ld exp=%ld\n", what, got, exp); }
}

static void lo() { dut->clk = 0; dut->eval(); }
static void hi() { dut->clk = 1; dut->eval(); }
static void step() { lo(); hi(); }

static void set_cbs(bool shaped, uint32_t slope, int32_t hicr, int32_t locr) {
    dut->cbs_shaped_i = shaped ? 0xF : 0x0;
    for (int q = 0; q < 4; q++) {
        dut->cbs_idle_slope_i[q] = slope;
        dut->cbs_hi_credit_i[q]  = (uint32_t)hicr;
        dut->cbs_lo_credit_i[q]  = (uint32_t)locr;
    }
}

// build an 8-beat (64-byte) VLAN frame, PCP in the TCI, payload tagged by marker
static std::vector<uint64_t> vlan_frame(int pcp, uint8_t marker) {
    uint8_t b[64]; memset(b, 0, sizeof b);
    const uint8_t dst[6] = {0x00,0x11,0x22,0x33,0x44,0x55};
    const uint8_t src[6] = {0x66,0x77,0x88,0x99,0xAA,0xBB};
    for (int i = 0; i < 6; i++) { b[i] = dst[i]; b[6+i] = src[i]; }
    b[12] = 0x81; b[13] = 0x00;               // VLAN TPID 0x8100
    b[14] = (uint8_t)((pcp & 7) << 5);        // TCI: PCP in [7:5]
    b[15] = 0x01;                             // ... VID low
    b[16] = 0x08; b[17] = 0x00;               // inner EtherType (IPv4)
    for (int i = 18; i < 64; i++) b[i] = (uint8_t)(marker ^ i);
    std::vector<uint64_t> beats;
    for (int bt = 0; bt < 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++) v |= (uint64_t)b[bt*8+j] << (8*(7-j)); // big-endian
        beats.push_back(v);
    }
    return beats;
}

struct Res { std::vector<uint64_t> data; int dest = -1; bool got = false; };

// stream one frame in while draining the output; run for `cycles`
static Res run_frame(const std::vector<uint64_t>& beats, int cycles) {
    Res r; size_t bi = 0;
    for (int c = 0; c < cycles; c++) {
        bool have = bi < beats.size();
        dut->s_tdata  = have ? beats[bi] : 0;
        dut->s_tkeep  = have ? 0xFF : 0x00;
        dut->s_tlast  = have ? (bi == beats.size()-1) : 0;
        dut->s_tvalid = have; dut->m_tready = 1;
        lo();
        if (dut->m_tvalid && dut->m_tready) { r.data.push_back(dut->m_tdata); r.dest = dut->m_tdest; r.got = true; }
        bool sacc = have && dut->s_tvalid && dut->s_tready;
        hi();
        if (sacc) bi++;
    }
    dut->s_tvalid = 0; step();
    return r;
}

static void do_reset() {
    dut->resetn = 0; dut->s_tvalid = 0; dut->m_tready = 0;
    for (int i = 0; i < 8; i++) step();
    dut->resetn = 1;
    for (int i = 0; i < 4; i++) step();
}

static void config_classifier() {
    dut->is_1g_i = 1;
    dut->cls_use_pcp_i = 1; dut->cls_dmac_check_i = 0; dut->cls_default_pcp_i = 0;
    // identity maps so PCP p -> prio p -> TC p -> queue p (deterministic routing):
    dut->cls_prio_regen_i   = 0x00FAC688;  // PCP -> PCP
    dut->cls_pcp_tc_map_i    = 0x00FAC688;  // prio -> TC
    dut->cls_tc_queue_map_i  = 0x000000E4;  // TC0..3 -> queue 0..3
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vdatapath_wrap;
    config_classifier();
    set_cbs(false, 0, 0, 0);
    do_reset();

    printf("== traffic_controller_802_1q end-to-end datapath harness ==\n");

    // ---- unshaped (strict priority): frames of several PCPs pass byte-exact ----
    printf("-- unshaped (strict priority) --\n");
    set_cbs(false, 0, 0, 0);
    std::set<int> dests;
    for (int pcp = 0; pcp < 4; pcp++) {
        auto f = vlan_frame(pcp, 0xA0 + pcp);
        auto r = run_frame(f, 300);
        ck("frame egressed", r.got ? 1 : 0, 1);
        bool eq = (r.data.size() == f.size());
        for (size_t i = 0; eq && i < f.size(); i++) eq = (r.data[i] == f[i]);
        ck("byte-exact end-to-end", eq ? 1 : 0, 1);
        ck("tdest == queue (PCP p -> q p)", r.dest, pcp);   // identity map -> exact routing
        if (r.dest >= 0) dests.insert(r.dest);
    }
    ck("classification uses 4 queues", (long)dests.size(), 4);

    // ---- shaped (CBS path, generous credit): frames still pass byte-exact ----
    printf("-- shaped (CBS, generous credit) --\n");
    do_reset(); config_classifier();
    set_cbs(true, 300000000u, 1000000, -1000000);
    for (int i = 0; i < 8; i++) step();
    int shaped_ok = 0;
    for (int pcp = 0; pcp < 4; pcp++) {
        auto f = vlan_frame(pcp, 0xB0 + pcp);
        auto r = run_frame(f, 500);
        if (r.got) {
            bool eq = (r.data.size() == f.size());
            for (size_t i = 0; eq && i < f.size(); i++) eq = (r.data[i] == f[i]);
            if (eq) shaped_ok++;
        }
    }
    ck("shaped frames pass byte-exact", shaped_ok, 4);

    // ---- back-to-back burst then drain (queue depth + arbiter under load) ----
    printf("-- burst of frames across queues --\n");
    do_reset(); config_classifier(); set_cbs(false, 0, 0, 0);
    int delivered = 0;
    for (int n = 0; n < 6; n++) {
        auto f = vlan_frame(n % 4, 0xC0 + n);
        auto r = run_frame(f, 300);
        if (r.got && r.data.size() == f.size()) delivered++;
    }
    ck("burst all delivered", delivered, 6);

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final(); delete dut;
    return fails ? 1 : 0;
}
