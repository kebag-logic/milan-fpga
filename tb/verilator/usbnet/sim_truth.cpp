// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Exhaust the ruled predicates, including external sources and reset.
#include "VKL_status_led_truth.h"
#include "verilated.h"
#include <cstdio>

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    VKL_status_led_truth d;
    int failures = 0;
    int checks = 0;
    auto check = [&](bool ok, const char *message, unsigned bits) {
        ++checks;
        if (!ok) {
            std::printf("FAIL %s:%d: %s inputs=%02x\n", __FILE__, __LINE__, message, bits);
            ++failures;
        }
    };
    auto tick = [&] { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); };
    // Ascending, descending and discontinuous orders exercise simultaneous changes.
    for (unsigned order = 0; order != 3; ++order) {
        for (unsigned n = 0; n != 64; ++n) {
            const unsigned bits = order == 0 ? n : order == 1 ? 63 - n : (n * 17) % 64;
            d.input_locked_i = bits & 1;
            d.output_open_i = (bits >> 1) & 1;
            d.clock_internal_i = (bits >> 2) & 1;
            d.clock_stream_i = (bits >> 3) & 1;
            d.source_locked_i = (bits >> 4) & 1;
            d.clock_locked_i = (bits >> 5) & 1;
            d.rst_ni = 0; tick();
            check(!d.stream_o && !d.clock_o, "fabric reset clears both predicates", bits);
            d.rst_ni = 1;
            const auto before = d.stream_o | (d.clock_o << 1);
            d.clk_i = 0; d.eval();
            check((d.stream_o | (d.clock_o << 1)) == before,
                  "fabric predicates change only on source clock", bits);
            tick();
            bool expected_stream = false;
            bool expected_clock = false;
            if (bits & 3) expected_stream = true;
            if (bits & 4) expected_clock = true;
            else if (bits & 32) {
                if (!(bits & 8)) expected_clock = true;
                else if (bits & 16) expected_clock = true;
            }
            check(d.stream_o == expected_stream && d.clock_o == expected_clock,
                  "fabric truth table", bits);
        }
    }
    d.final();
    std::printf("%d checks: %d PASS, %d FAIL\n", checks, checks - failures, failures);
    return failures != 0;
}
