// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The production attachment, with independent source and destination clocks.
#include "Vled_attachment.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    milan::tb::Model<Vled_attachment> model;
    auto &d = *model;
    unsigned checks = 0;
    unsigned failures = 0;
    auto check = [&](bool ok, const char *name) {
        ++checks;
        if (!ok) {
            ++failures;
            std::printf("FAIL %s:%d: %s\n", __FILE__, __LINE__, name);
        }
    };
    auto source = [&] { d.milan_clk = 0; d.eval(); d.milan_clk = 1; d.eval(); };
    auto dest = [&] { d.sys_clk = 0; d.eval(); d.sys_clk = 1; d.eval(); };
    d.link = 0; d.usb = 0; d.activity = 0;
    d.sys_rst = 1; d.milan_rst = 1; source(); dest(); dest();
    d.sys_rst = 0; d.milan_rst = 0;
    for (unsigned bits = 0; bits < 64; ++bits) {
        const auto old = d.state;
        d.input_locked = bits & 1;
        d.output_open = (bits >> 1) & 1;
        d.clock_internal = (bits >> 2) & 1;
        d.clock_stream = (bits >> 3) & 1;
        d.source_locked = (bits >> 4) & 1;
        d.clock_locked = (bits >> 5) & 1;
        dest(); dest(); dest();
        check(d.state == old, "datapath predicates wait for the source clock");
        source(); dest();
        check(d.state == old, "two destination stages precede display");
        dest();
        unsigned expected = (bits & 3) ? 4 : 0;
        if (bits & 4) expected |= 8;
        else if ((bits & 32) && (!(bits & 8) || (bits & 16))) expected |= 8;
        check(d.state == expected, "production LED attachment truth table");
        check(!(d.led0_r || d.led0_b || d.led1_r || d.led1_b ||
                d.led2_r || d.led2_b || d.led3_r || d.led3_b), "only green is connected");
    }
    d.link = 1; d.usb = 1; dest();
    check((d.state & 3) == 3, "link and USB status do not wait for the datapath clock");
    d.milan_rst = 1; source(); dest(); dest();
    check((d.state & 12) == 0, "source reset crosses into the display");
    std::printf("%u checks: %u PASS, %u FAIL\n", checks, checks - failures, failures);
    return failures != 0;
}
