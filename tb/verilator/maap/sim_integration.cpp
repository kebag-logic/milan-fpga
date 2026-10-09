// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// #696 M4: equal reset/write/enable timing, different programmed MACs.
// Observe complete frames at the real datapath MAC output (B.3.4 NOTE).
#include "Vmilan_datapath.h"
#include "../../common/verilator_harness.hpp"
#include <array>
#include <cstdio>
#include <vector>

namespace {
class SeedHarness {
 public:
    std::vector<unsigned> intervals(unsigned mac_last) {
        dut->axis_resetn = 0;
        dut->gtx_resetn = 0;
        dut->m_axis_mac_tx_tready = 1;
        dut->i_mac_speed = 2;
        dut->i_link_up = 1;
        dut->i_full_duplex = 1;
        for (int i = 0; i < 8; ++i) cycle();
        dut->axis_resetn = 1;
        dut->gtx_resetn = 1;
        for (int i = 0; i < 16; ++i) cycle();
        // Wire MAC 02:00:00:00:00:xx, programmed only after reset.
        if (!write(0x108, 2) || !write(0x10c, mac_last << 8)
            || !write(0x6cc, 0x801)) return {};
        for (unsigned i = 0; i < 25000 && starts.size() < 4; ++i) cycle();
        if (starts.size() != 4 || !frames_ok) return {};
        std::vector<unsigned> result;
        for (unsigned i = 1; i < starts.size(); ++i)
            result.push_back(starts[i] - starts[i - 1]);
        return result;
    }

 private:
    const milan::tb::Model<Vmilan_datapath> model;
    Vmilan_datapath* dut = model.get();
    unsigned now = 0;
    unsigned start = 0;
    bool frames_ok = true;
    std::vector<unsigned char> frame;
    std::vector<unsigned> starts;

    void low() {
        dut->axis_clk = 0; dut->gtx_clk = 0;
        dut->clk_audio_i = 0; dut->clk_tdm_i = 0;
        dut->eval();
    }

    void high() {
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            if (frame.empty()) start = now;
            for (unsigned i = 0; i < 8; ++i)
                if ((dut->m_axis_mac_tx_tkeep >> i) & 1)
                    frame.push_back(dut->m_axis_mac_tx_tdata >> (8 * i));
            if (dut->m_axis_mac_tx_tlast) {
                if (frame.size() >= 16 && frame[14] == 0xfe && frame[15] == 1) {
                    frames_ok &= frame.size() == 60 && frame[17] == 16;
                    starts.push_back(start);
                }
                frame.clear();
            }
        }
        dut->axis_clk = 1; dut->gtx_clk = 1;
        dut->clk_audio_i = 1; dut->clk_tdm_i = 1;
        dut->eval();
        ++now;
    }

    void cycle() { low(); high(); }

    bool write(unsigned address, unsigned value) {
        dut->s_axi_awaddr = address; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = value; dut->s_axi_wstrb = 15;
        dut->s_axi_wvalid = 1; dut->s_axi_bready = 1;
        bool accepted = false;
        for (unsigned i = 0; i < 2048 && !accepted; ++i) {
            low();
            accepted = dut->s_axi_awready && dut->s_axi_wready;
            high();
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        bool response = false;
        for (unsigned i = 0; i < 2048 && !response; ++i) {
            low(); response = dut->s_axi_bvalid; high();
        }
        dut->s_axi_bready = 0;
        return accepted && response;
    }
};
} // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    std::array<std::vector<unsigned>, 2> intervals;
    for (unsigned i = 0; i < intervals.size(); ++i) {
        SeedHarness station;
        intervals[i] = station.intervals(i + 1);
        std::printf("station %u probe intervals:", i);
        for (unsigned value : intervals[i]) std::printf(" %u", value);
        std::puts("");
    }
    bool valid = true;
    for (const auto& station : intervals) {
        valid &= station.size() == 3;
        for (unsigned value : station) valid &= value > 5000 && value < 6000;
    }
    const bool different = valid && intervals[0] != intervals[1];
    std::printf("[%s] M4 datapath: programmed MAC changes probe intervals\n",
                different ? "ok" : "FAIL");
    std::printf("MAAP integration: 1 checks, %u failures\n", different ? 0 : 1);
    return different ? 0 : 1;
}
