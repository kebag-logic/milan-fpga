// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// #667: grade the first ten PDUs at every enable phase, including rebinds.
// The shipping 1x1 TDM8 packetizer receives the capture-map pair walk.
// IEEE 1722-2016 7.5: each timestamp belongs to its first sample frame.
#include "VKL_aaf_packetizer.h"
#include "../../common/verilator_harness.hpp"
#include "verilated.h"
#include <array>
#include <cstdint>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

namespace {
using Frame = std::vector<uint8_t>;
constexpr uint32_t kTransitNs = 2000000;
constexpr int kTickNs = 20;
constexpr int kPduPeriodNs = 125000;
constexpr unsigned kPdus = 10;
constexpr unsigned kSamplesLimit = 80;

class Startup {
 public:
    explicit Startup(milan::tb::Checker& checks) : check(checks) {}
    void run(uint64_t origin, int phase, int pair_stride, uint64_t idle_ns, bool reset_start,
             bool stalled);

 private:
    void tick();
    void cycles(unsigned count);
    void sample(unsigned index, int enable_cycle = -1);
    void reset();
    void grade(const std::string& label);
    static uint32_t word(const Frame& frame, unsigned offset);

    const milan::tb::Model<VKL_aaf_packetizer> model;
    VKL_aaf_packetizer* dut = model.get();
    milan::tb::Checker& check;
    std::vector<Frame> frames;
    Frame current;
    std::map<unsigned, uint32_t> sample_times;
    uint64_t now_ns = 0;
    unsigned cycle = 0;
    int pair_stride_cyc = 1;
    bool stall = false;
};

void Startup::tick() {
    dut->ptp_ns_i = now_ns;
    // Bounded stalls never approach one sample interval or exhaust a bank.
    dut->m_axis_tready = !stall || cycle % 17 >= 5;
    dut->clk_i = 0;
    dut->eval();
    if (dut->m_axis_tvalid && dut->m_axis_tready) {
        for (unsigned byte = 0; byte < 8; ++byte) {
            if ((dut->m_axis_tkeep >> byte) & 1)
                current.push_back(static_cast<uint8_t>(dut->m_axis_tdata >> (8 * byte)));
        }
        if (dut->m_axis_tlast) {
            frames.push_back(current);
            current.clear();
        }
    }
    dut->clk_i = 1;
    dut->eval();
    now_ns += kTickNs;
    ++cycle;
}

void Startup::cycles(unsigned count) {
    for (unsigned i = 0; i < count; ++i) tick();
}

void Startup::sample(unsigned index, int enable_cycle) {
    // Four pair slots exercise compact, capture-map and physical TDM spacing.
    // A rational 1041/1042/1042-cycle grid gives 48 kHz at 50 MHz.
    const int length = index % 3 == 0 ? 1041 : 1042;
    sample_times[index] = static_cast<uint32_t>(now_ns);
    for (int offset = 0; offset < length; ++offset) {
        if (offset == enable_cycle) {
            dut->rst_n = 1;
            dut->stream_en_i = 1;
        }
        const int slot = offset / pair_stride_cyc;
        dut->pair_valid_i = slot < 4 && offset % pair_stride_cyc == 0;
        dut->pair_slot_i = slot < 4 ? slot : 0;
        // Every channel identifies its source sample and channel position.
        dut->pair_l_i = (index << 4) + 2 * slot;
        dut->pair_r_i = (index << 4) + 2 * slot + 1;
        tick();
    }
    dut->pair_valid_i = 0;
}

void Startup::reset() {
    dut->rst_n = 0;
    dut->stream_en_i = 0;
    dut->pair_valid_i = 0;
    cycles(4);
    dut->rst_n = 1;
    cycles(4);
}

uint32_t Startup::word(const Frame& frame, unsigned offset) {
    uint32_t value = 0;
    for (unsigned byte = 0; byte < 4; ++byte)
        value = (value << 8) | frame.at(offset + byte);
    return value;
}

void Startup::grade(const std::string& label) {
    check.dec((label + " bounded first ten").c_str(), frames.size(), kPdus);
    if (frames.size() != kPdus) return;
    std::array<uint32_t, kPdus> timestamps{};
    for (unsigned pdu = 0; pdu < kPdus; ++pdu) {
        const Frame& frame = frames[pdu];
        check.dec((label + " frame bytes").c_str(), frame.size(), 234);
        if (frame.size() != 234) return;
        timestamps[pdu] = word(frame, 30);
        const unsigned first_sample = word(frame, 42) >> 12;
        const auto first = sample_times.find(first_sample);
        check.dec((label + " first sample exists").c_str(), first != sample_times.end(), true);
        if (first != sample_times.end()) {
            check.dec((label + " sample plus offset").c_str(), timestamps[pdu],
                     static_cast<uint32_t>(first->second + kTransitNs));
        }
        bool payload_ok = true;
        for (unsigned row = 0; row < 6; ++row) {
            for (unsigned channel = 0; channel < 8; ++channel) {
                const uint32_t expected = (((first_sample + row) << 4) + channel) << 8;
                payload_ok &= word(frame, 42 + 4 * (8 * row + channel)) == expected;
            }
        }
        check.dec((label + " complete sample rows").c_str(), payload_ok, true);
        check.dec((label + " valid normal timestamp").c_str(), frame[19] & 1, 1);
        if (pdu != 0)
            check.dec((label + " consecutive sequence").c_str(), frame[20],
                     static_cast<uint8_t>(frames[pdu - 1][20] + 1));
        std::printf("START-PDU %s n=%u seq=%u tv=%u ts=%08x\n", label.c_str(),
                    pdu + 1, frame[20], frame[19] & 1, timestamps[pdu]);
    }
    // Six rational sample periods are exactly 125000 ns, including wrap.
    // Later PDUs independently establish the steady step. No first-PDU skip.
    const int32_t steady = static_cast<int32_t>(timestamps[9] - timestamps[8]);
    check.dec((label + " steady period").c_str(), steady, kPduPeriodNs);
    for (unsigned pdu = 1; pdu < kPdus; ++pdu)
        check.dec((label + " startup step equals steady").c_str(),
                 static_cast<int32_t>(timestamps[pdu] - timestamps[pdu - 1]), steady);
    std::printf("START-SWEEP %s first_step=%d steady=%d tolerance_ns=0\n", label.c_str(),
                static_cast<int32_t>(timestamps[1] - timestamps[0]), steady);
}

void Startup::run(uint64_t origin, int phase, int pair_stride, uint64_t idle_ns,
                  bool reset_start, bool stalled) {
    now_ns = origin;
    pair_stride_cyc = pair_stride;
    dut->dest_mac_i = 0x91e0f0000001ULL;
    dut->station_mac_i = 0x020000000001ULL;
    dut->vlan_vid_i = 2;
    dut->vlan_pcp_i = 3;
    dut->dom_ovr_i = 0;
    dut->transit_ns_i = kTransitNs;
    dut->ts_uncertain_i = 0;
    dut->mr_i = 0;
    dut->tctx_wr_en_i = 0;
    dut->tctx_rd_en_i = 0;
    reset();
    // An arbitrary legal initial sequence exercises modulo-256 wrap.
    dut->tctx_wr_addr_i = 3;
    dut->tctx_wr_data_i = 248;
    dut->tctx_wr_en_i = 1;
    tick();
    dut->tctx_wr_en_i = 0;
    if (idle_ns != 0) {
        dut->stream_en_i = 1;
        for (unsigned index = 0; index < 13; ++index) sample(index);
        // Stop with a partial epoch. A new timestamp must be acquired even
        // though the unreset TCTX retains this previous stream's value.
        if (reset_start) {
            // Keep enable high through reset so its reset assignment is
            // observed independently of the disabled-stream clear.
            dut->rst_n = 0;
            cycles(8);
        }
        else {
            dut->stream_en_i = 0;
            cycles(8);
        }
        // Elide the disabled interval's clocks, advancing only the PHC.
        now_ns += idle_ns;
    }
    frames.clear();
    current.clear();
    sample_times.clear();
    stall = stalled;
    sample(13, phase);
    for (unsigned index = 14; index < kSamplesLimit && frames.size() < kPdus; ++index)
        sample(index);
    const std::string label = "origin=" + std::to_string(origin)
        + " phase=" + std::to_string(phase) + " idle=" + std::to_string(idle_ns)
        + " stride=" + std::to_string(pair_stride_cyc)
        + " reset=" + std::to_string(reset_start) + " stall=" + std::to_string(stalled);
    grade(label);
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"aaf-start"};
    for (uint64_t origin : {uint64_t{0}, uint64_t{1000000000}, uint64_t{0xffe00000}})
        for (int stride : {1, 26, 260})
          for (int phase : {0, 1, stride, stride + 1, 2 * stride,
                            2 * stride + 1, 3 * stride, 3 * stride + 1, 1040})
            for (uint64_t idle : {uint64_t{0}, uint64_t{500000000}, uint64_t{3800000000}})
                for (bool reset : {false, true}) {
                    Startup start(check);
                    start.run(origin, phase, stride, idle, reset, reset);
                }
    return check.report();
}
