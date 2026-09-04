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
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <array>
#include <vector>
#include <set>

namespace {

struct Res;   // defined below, next to run_frame()

// The whole harness: the model handle, the tally and every phase that drives
// them, so no file-scope mutable state is left for a reader to hunt for.
class DatapathHarness {
 public:
    int run();

 private:
    void ck(const char* what, long got, long exp);
    void lo();
    void hi();
    void step();
    void set_cbs(bool shaped, uint32_t slope, int32_t hicr, int32_t locr);
    std::vector<uint64_t> vlan_frame(int pcp, uint8_t marker);
    Res run_frame(const std::vector<uint64_t>& beats, int cycles);
    void do_reset();
    void config_classifier();
    void unshaped_strict_priority_passes_byte_exact();
    void shaped_cbs_path_passes_byte_exact();
    void burst_across_queues_all_delivered();

    Vdatapath_wrap* dut = nullptr;
    long checks = 0;
    long fails = 0;
};

void DatapathHarness::ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-32s got=%ld exp=%ld\n", what, got, exp);
    }
}

void DatapathHarness::lo() { dut->clk = 0; dut->eval(); }
void DatapathHarness::hi() { dut->clk = 1; dut->eval(); }
void DatapathHarness::step() { lo(); hi(); }

constexpr int NQ = 5;    // ethernet_packet_pkg::NUMBER_OF_QUEUES (802.1Q order)

// Frame geometry of the injected VLAN frame (see vlan_frame() below).
constexpr int kFrameBytes    = 64;               // one full 802.1Q test frame
constexpr int kFrameBeats    = kFrameBytes / 8;  // 8 bytes per 64-bit AXIS beat
constexpr int kMacBytes      = 6;                // one MAC address
constexpr int kPayloadOffset = 18;               // DA+SA+TPID+TCI+EtherType

// Cycle budgets: how long run_frame() is given to push one frame through the
// whole classifier -> FIFO -> shaper chain and drain it again.
constexpr int kFrameCycles       = 300;  // unshaped / burst
constexpr int kShapedFrameCycles = 500;  // shaped: the CBS credit path is slower
constexpr int kResetCycles       = 8;    // resetn held low
constexpr int kPostResetCycles   = 4;    // settle after resetn release
constexpr int kCbsSettleCycles   = 8;    // settle after the CBS config changes
constexpr int kBurstFrames       = 12;   // back-to-back burst length

// "Generous credit": a shaped run that must not starve, so the frames still
// egress byte-exact and only the CBS *path* is exercised, not its limits.
constexpr uint32_t kIdleSlopeBps  = 300000000u;
constexpr int32_t  kHiCreditBytes = 1000000;
constexpr int32_t  kLoCreditBytes = -1000000;

void DatapathHarness::set_cbs(bool shaped, uint32_t slope, int32_t hicr,
                              int32_t locr) {
    dut->cbs_shaped_i = shaped ? ((1u << NQ) - 1) : 0x0;
    for (int q = 0; q < NQ; q++) {
        dut->cbs_idle_slope_bps_i[q] = slope;
        dut->cbs_hi_credit_bytes_i[q]  = static_cast<uint32_t>(hicr);
        dut->cbs_lo_credit_bytes_i[q]  = static_cast<uint32_t>(locr);
    }
}

// build an 8-beat (64-byte) VLAN frame, PCP in the TCI, payload tagged by marker
std::vector<uint64_t> DatapathHarness::vlan_frame(int pcp, uint8_t marker) {
    uint8_t b[kFrameBytes];
    memset(b, 0, sizeof b);
    const std::array<uint8_t, kMacBytes> dst = {0x00,0x11,0x22,0x33,0x44,0x55};
    const std::array<uint8_t, kMacBytes> src = {0x66,0x77,0x88,0x99,0xAA,0xBB};
    for (int i = 0; i < kMacBytes; i++) { b[i] = dst[i]; b[kMacBytes+i] = src[i]; }
    b[12] = 0x81; b[13] = 0x00;                        // VLAN TPID 0x8100
    b[14] = static_cast<uint8_t>((pcp & 7) << 5);      // TCI: PCP in [7:5]
    b[15] = 0x01;                                      // ... VID low
    b[16] = 0x08; b[17] = 0x00;                        // inner EtherType (IPv4)
    for (int i = kPayloadOffset; i < kFrameBytes; i++) b[i] = static_cast<uint8_t>(marker ^ i);
    std::vector<uint64_t> beats;
    for (int bt = 0; bt < kFrameBeats; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++) v |= static_cast<uint64_t>(b[bt*8+j]) << (8*(7-j)); // big-endian
        beats.push_back(v);
    }
    return beats;
}

struct Res { std::vector<uint64_t> data; std::vector<uint8_t> keep; int dest = -1; bool got = false; };

// stream one frame in while draining the output; run for `cycles`
Res DatapathHarness::run_frame(const std::vector<uint64_t>& beats, int cycles) {
    Res r;
    size_t bi = 0;
    for (int c = 0; c < cycles; c++) {
        bool have = bi < beats.size();
        dut->s_tdata  = have ? beats[bi] : 0;
        dut->s_tkeep  = have ? 0xFF : 0x00;
        dut->s_tlast  = have ? (bi == beats.size()-1) : 0;
        dut->s_tvalid = have;
        dut->m_tready = 1;
        lo();
        if (dut->m_tvalid && dut->m_tready) {
            r.data.push_back(dut->m_tdata);
            r.keep.push_back(dut->m_tkeep);
            r.dest = dut->m_tdest;
            r.got = true;
        }
        bool sacc = have && dut->s_tvalid && dut->s_tready;
        hi();
        if (sacc) bi++;
    }
    dut->s_tvalid = 0;
    step();
    return r;
}

void DatapathHarness::do_reset() {
    dut->resetn = 0;
    dut->s_tvalid = 0;
    dut->m_tready = 0;
    for (int i = 0; i < kResetCycles; i++) step();
    dut->resetn = 1;
    for (int i = 0; i < kPostResetCycles; i++) step();
}

void DatapathHarness::config_classifier() {
    dut->is_1g_i = 1;
    dut->cls_use_pcp_i = 1;
    dut->cls_dmac_check_i = 0;
    dut->cls_default_pcp_i = 0;
    dut->cls_ctrl_class_i = 1;   // CLS_CTRL[2] resets to 1 (REQ-CLS-10)
    // identity maps so PCP p -> prio p -> TC p -> queue p (deterministic routing):
    dut->cls_prio_regen_i   = 0x00FAC688;  // PCP -> PCP
    dut->cls_pcp_tc_map_i    = 0x00FAC688;  // prio -> TC
    // TC t -> queue t for t < NQ (3 bits/entry at NQ=5); TC >= NQ is left at 0
    // so it exercises nothing out of range here (traffic_class_map clamps those
    // to BEST_EFFORT anyway - tb/verilator/cls owns that check).
    uint32_t tcq = 0;
    for (int t = 0; t < NQ; t++) tcq |= static_cast<uint32_t>(t) << (3 * t);
    dut->cls_tc_queue_map_i  = tcq;
}

// ---- unshaped (strict priority): frames of several PCPs pass byte-exact ----
void DatapathHarness::unshaped_strict_priority_passes_byte_exact() {
    printf("-- unshaped (strict priority) --\n");
    set_cbs(false, 0, 0, 0);
    std::set<int> dests;
    for (int pcp = 0; pcp < NQ; pcp++) {
        auto f = vlan_frame(pcp, 0xA0 + pcp);
        auto r = run_frame(f, kFrameCycles);
        ck("frame egressed", r.got ? 1 : 0, 1);
        bool eq = (r.data.size() == f.size());
        for (size_t i = 0; eq && i < f.size(); i++) eq = (r.data[i] == f[i]);
        ck("byte-exact end-to-end", eq ? 1 : 0, 1);
        // egress tkeep must be full (0xFF) on every beat of these full-word frames —
        // guards the AXIS keep the LiteEth last_be handoff depends on (milan_soc MilanMAC).
        bool keep_ok = (r.keep.size() == f.size());
        for (size_t i = 0; keep_ok && i < r.keep.size(); i++) keep_ok = (r.keep[i] == 0xFF);
        ck("egress tkeep = 0xFF (full beats)", keep_ok ? 1 : 0, 1);
        ck("tdest == queue (PCP p -> q p)", r.dest, pcp);   // identity map -> exact routing
        if (r.dest >= 0) dests.insert(r.dest);
    }
    ck("classification uses all 5 queues", static_cast<long>(dests.size()), NQ);
}

// ---- shaped (CBS path, generous credit): frames still pass byte-exact ----
void DatapathHarness::shaped_cbs_path_passes_byte_exact() {
    printf("-- shaped (CBS, generous credit) --\n");
    do_reset();
    config_classifier();
    set_cbs(true, kIdleSlopeBps, kHiCreditBytes, kLoCreditBytes);
    for (int i = 0; i < kCbsSettleCycles; i++) step();
    int shaped_ok = 0;
    for (int pcp = 0; pcp < NQ; pcp++) {
        auto f = vlan_frame(pcp, 0xB0 + pcp);
        auto r = run_frame(f, kShapedFrameCycles);
        if (r.got) {
            bool eq = (r.data.size() == f.size());
            for (size_t i = 0; eq && i < f.size(); i++) eq = (r.data[i] == f[i]);
            if (eq) shaped_ok++;
        }
    }
    ck("shaped frames pass byte-exact", shaped_ok, NQ);
}

// ---- back-to-back burst then drain (queue depth + arbiter under load) ----
void DatapathHarness::burst_across_queues_all_delivered() {
    printf("-- burst of frames across queues --\n");
    do_reset();
    config_classifier();
    set_cbs(false, 0, 0, 0);
    int delivered = 0;
    for (int n = 0; n < kBurstFrames; n++) {
        auto f = vlan_frame(n % NQ, 0xC0 + n);
        auto r = run_frame(f, kFrameCycles);
        if (r.got && r.data.size() == f.size()) delivered++;
    }
    ck("burst all delivered", delivered, kBurstFrames);
}

int DatapathHarness::run() {
    const milan::tb::Model<Vdatapath_wrap> model;
    dut = model.get();
    config_classifier();
    set_cbs(false, 0, 0, 0);
    do_reset();

    printf("== traffic_controller_802_1q end-to-end datapath harness ==\n");

    unshaped_strict_priority_passes_byte_exact();
    shaped_cbs_path_passes_byte_exact();
    burst_across_queues_all_delivered();

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    DatapathHarness harness;
    return harness.run();
}
