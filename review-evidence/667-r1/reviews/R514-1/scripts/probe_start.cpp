// Reviewer probe (R514-1, #667): independent generalisation of the startup
// boundary. Compile-time: PCH = pairs per talker sample (chans/2), NT = talkers.
// Talker 0 streams continuously when NT == 2; the talker under test (NT-1)
// is stopped (disable or reset) and restarted at every enable phase in a dense
// set. Expected timestamps are computed from the stimulus PHC at the talker's
// own pair zero plus that talker's own offset; payload identity is graded.
// Mode LONGSTALL holds tready low across more than one sample interval at the
// first PDU (characterisation of the pre-existing overrun path).
#include "VKL_aaf_packetizer.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <string>
#include <vector>

#ifndef PCH
#define PCH 4
#endif
#ifndef NT
#define NT 1
#endif

namespace {
using Frame = std::vector<uint8_t>;
constexpr uint32_t kOff[2] = {2000000u, 1500000u};
constexpr int kTickNs = 20;
constexpr unsigned kPdus = 10;
constexpr unsigned kFrameBytes = 42 + 24 * 2 * PCH;
unsigned long long g_checks = 0, g_fail = 0, g_runs = 0;
std::map<std::string, unsigned long long> g_fail_by;

void chk(const std::string& what, const std::string& label, long long got, long long exp) {
    ++g_checks;
    if (got != exp) {
        ++g_fail;
        ++g_fail_by[what];
        if (g_fail_by[what] <= 3)
            std::printf("[FAIL] %s %s got=%lld exp=%lld\n", label.c_str(), what.c_str(), got, exp);
    }
}

struct Run {
    VKL_aaf_packetizer* dut;
    std::vector<Frame> frames[NT];
    Frame cur;
    std::map<unsigned, uint32_t> st[NT];
    uint64_t now = 0;
    unsigned cyc = 0;
    int stride = 1;
    int stall_mode = 0;      // 0 none, 1 bounded 5/17, 2 long hold at first PDU
    unsigned long long hold_until = 0;
    bool held = false;

    explicit Run(VKL_aaf_packetizer* d) : dut(d) {}

    void tick() {
        dut->ptp_ns_i = now;
        bool rdy = true;
        if (stall_mode == 1) rdy = cyc % 17 >= 5;
        if (stall_mode == 2) {
            if (!held && dut->m_axis_tvalid) { held = true; hold_until = cyc + 1500; }
            rdy = !(held && cyc < hold_until);
        }
        dut->m_axis_tready = rdy;
        dut->clk_i = 0;
        dut->eval();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            for (unsigned b = 0; b < 8; ++b)
                if ((dut->m_axis_tkeep >> b) & 1) cur.push_back(uint8_t(dut->m_axis_tdata >> (8 * b)));
            if (dut->m_axis_tlast) {
                unsigned t = cur.size() >= 30 ? cur[29] : 0;   // derived uid = talker
                if (t < NT) frames[t].push_back(cur);
                cur.clear();
            }
        }
        dut->clk_i = 1;
        dut->eval();
        now += kTickNs;
        ++cyc;
    }
    void sample(unsigned idx, int en_cycle, unsigned tut) {
        const int len = idx % 3 == 0 ? 1041 : 1042;
        for (unsigned t = 0; t < NT; ++t)
            st[t][idx] = uint32_t(now + uint64_t(t) * PCH * stride * kTickNs);
        for (int off = 0; off < len; ++off) {
            if (off == en_cycle) { dut->rst_n = 1; dut->stream_en_i |= (1u << tut); }
            const int slot = off / stride;
            const bool v = slot < NT * PCH && off % stride == 0;
            dut->pair_valid_i = v;
            dut->pair_slot_i = v ? slot : 0;
            dut->pair_l_i = (idx << 4) + 2 * slot;
            dut->pair_r_i = (idx << 4) + 2 * slot + 1;
            tick();
        }
        dut->pair_valid_i = 0;
    }
};

uint32_t w32(const Frame& f, unsigned o) {
    return (uint32_t(f[o]) << 24) | (uint32_t(f[o + 1]) << 16) | (uint32_t(f[o + 2]) << 8) | f[o + 3];
}

void grade(Run& r, unsigned t, const std::string& label, unsigned need) {
    auto& fr = r.frames[t];
    chk("bounded count", label, fr.size() >= need, 1);
    if (fr.size() < need) return;
    for (unsigned p = 0; p < need; ++p) {
        const Frame& f = fr[p];
        chk("frame bytes", label, f.size(), kFrameBytes);
        if (f.size() != kFrameBytes) return;
        const uint32_t ts = w32(f, 30);
        const unsigned first = (w32(f, 42) >> 8) >> 4;
        auto it = r.st[t].find(first);
        chk("first sample exists", label, it != r.st[t].end(), 1);
        if (it != r.st[t].end()) chk("sample plus own offset", label, ts, uint32_t(it->second + kOff[t]));
        bool ok = true;
        for (unsigned row = 0; row < 6; ++row)
            for (unsigned c = 0; c < 2 * PCH; ++c)
                ok &= w32(f, 42 + 4 * (2 * PCH * row + c)) ==
                      ((((first + row) << 4) + 2 * PCH * t + c) << 8);
        chk("complete rows", label, ok, 1);
        chk("tv", label, f[19] & 1, 1);
        chk("cpf", label, f[36], 2 * PCH);
        if (p) {
            chk("consecutive seq", label, f[20], uint8_t(fr[p - 1][20] + 1));
            // Talker 0 (NT=2) crosses the stimulus' 8-tick stop gap, which
            // legitimately lengthens one sample period; its timestamps are
            // graded exactly by "sample plus own offset" instead.
            if (t == NT - 1)
                chk("step 125000", label, int32_t(ts - w32(fr[p - 1], 30)), 125000);
        }
    }
}

void one(uint64_t origin, int stride, int phase, uint64_t idle, bool reset_start, int stall) {
    VerilatedContext ctx;
    VKL_aaf_packetizer dut(&ctx);
    Run r(&dut);
    r.stride = stride;
    r.now = origin;
    dut.dest_mac_i = 0x91e0f0000001ULL;
    dut.station_mac_i = 0x020000000001ULL;
    dut.vlan_vid_i = 2;
    dut.vlan_pcp_i = 3;
    dut.dom_ovr_i = 0;
#if NT == 1
    dut.transit_ns_i = kOff[0];
#else
    dut.transit_ns_i = (uint64_t(kOff[1]) << 32) | kOff[0];
#endif
    dut.ts_uncertain_i = 0;
    dut.mr_i = 0;
    dut.tctx_wr_en_i = 0;
    dut.tctx_rd_en_i = 0;
    dut.rst_n = 0; dut.stream_en_i = 0; dut.pair_valid_i = 0;
    for (int i = 0; i < 4; ++i) r.tick();
    dut.rst_n = 1;
    for (int i = 0; i < 4; ++i) r.tick();
    const unsigned tut = NT - 1;
    if (NT == 2) dut.stream_en_i = 1;   // talker 0 streams throughout
    unsigned idx = 0;
    if (idle) {
        dut.stream_en_i |= (1u << tut);
        for (; idx < 13; ++idx) r.sample(idx, -1, tut);
        if (reset_start && NT == 1) { dut.rst_n = 0; for (int i = 0; i < 8; ++i) r.tick(); }
        else { dut.stream_en_i &= ~(1u << tut); for (int i = 0; i < 8; ++i) r.tick(); }
        if (NT == 1) r.now += idle;   // PHC jump only where no other talker streams
    }
    // Keep sample-time maps and any frame in flight; only restart counting.
    for (unsigned t = 0; t < NT; ++t) r.frames[t].clear();
    r.stall_mode = stall;
    r.sample(idx++, phase, tut);
    for (; idx < 100 && r.frames[tut].size() < kPdus + 1; ++idx) r.sample(idx, -1, tut);
    const std::string label = "pch=" + std::to_string(PCH) + " nt=" + std::to_string(NT) +
        " origin=" + std::to_string(origin) + " stride=" + std::to_string(stride) +
        " phase=" + std::to_string(phase) + " idle=" + std::to_string(idle) +
        " reset=" + std::to_string(reset_start) + " stall=" + std::to_string(stall);
    grade(r, tut, label, kPdus);
    if (NT == 2) grade(r, 0, label + " [talker0 continuity]", 8);
    ++g_runs;
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const int stall_mode = argc > 1 ? std::atoi(argv[1]) : 0;
    std::vector<int> strides = {1, 26};
    if (NT * PCH * 130 < 1041) strides.push_back(130);
    if (NT * PCH * 260 < 1041) strides.push_back(260);
    for (uint64_t origin : {uint64_t{0}, uint64_t{0xffe00000}})
        for (int stride : strides) {
            std::vector<int> phases;
            const int span = NT * PCH * stride + 2;
            for (int p = 0; p <= span; p += (stride > 26 ? 13 : 1)) phases.push_back(p);
            for (int k = 0; k < NT * PCH; ++k) { phases.push_back(k * stride); phases.push_back(k * stride + 1); }
            phases.push_back(1040);
            for (int phase : phases)
                for (uint64_t idle : {uint64_t{0}, uint64_t{3800000000ULL}})
                    for (bool rs : {false, true}) one(origin, stride, phase, idle, rs, stall_mode);
        }
    std::printf("PROBE pch=%d nt=%d stall=%d runs=%llu checks=%llu failures=%llu\n", PCH, NT,
                stall_mode, g_runs, g_checks, g_fail);
    for (auto& kv : g_fail_by) std::printf("  fail-class %s: %llu\n", kv.first.c_str(), kv.second);
    return g_fail ? 1 : 0;
}
