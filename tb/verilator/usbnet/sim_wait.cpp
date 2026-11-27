// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Bound a network control frame's wait through the real mailbox byte input.
#include "Vusbnet_mailbox_wrap.h"
#include "verilated.h"
#include <algorithm>
#include <cstdio>
#include <vector>

using Bytes = std::vector<unsigned char>;
static Bytes frame(unsigned length, unsigned subtype = 0xfb)
{
    Bytes b(length, 0);
    const unsigned char mac[] = {2, 0x4b, 0x4c, 0, 1, 1};
    std::copy(mac, mac + 6, b.begin());
    b[6] = 0x0a; b[12] = 0x22; b[13] = 0xf0; b[14] = subtype;
    return b;
}
int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    unsigned worst = 0;
    unsigned failures = 0;
    unsigned cases = 0;
    unsigned accepted = 0;
    unsigned full = 0;
    unsigned rate = 0;
    // The mailbox never consumes a host record while this fixture runs.
    // Later repetitions therefore exercise full rings and empty buckets too.
    for (unsigned length : {60u, 61u, 1514u, 1515u}) {
        Vusbnet_mailbox_wrap d;
        auto tick = [&] { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); };
        d.rst_ni = 0; tick(); tick(); d.rst_ni = 1;
        for (unsigned repeat = 0; repeat < 20; ++repeat) {
            const auto local = frame(length);
            const auto net = frame(70, 0xfc);
            unsigned off = 0;
            unsigned netoff = 0;
            unsigned start = 0;
            unsigned first = 0;
            unsigned local_done = 0;
            bool requested = false;
            bool taken = false;
            for (unsigned cycle = 1; cycle <= 10000 && netoff < net.size(); ++cycle) {
                d.clk_i = 0;
                // Two local copies: a waiting network frame must beat the second.
                d.s_active_i = off < 2 * length;
                d.s_valid_i = off < 2 * length;
                d.s_data_i = 0; d.s_keep_i = 0; d.s_last_i = 0;
                if (d.s_valid_i) {
                    const unsigned index = off % length;
                    const unsigned count = std::min(8u, length - index);
                    for (unsigned j = 0; j < count; ++j) {
                        d.s_data_i |= uint64_t(local[index + j]) << (8 * j);
                        d.s_keep_i |= 1u << j;
                    }
                    d.s_last_i = index + count == length;
                    off += count;
                }
                d.net_valid_i = requested;
                d.net_data_i = net[netoff]; d.net_last_i = netoff + 1 == net.size();
                d.eval();
                if (d.net_valid_i && d.net_ready_o) {
                    if (!taken) { first = cycle; taken = true; }
                    ++netoff;
                }
                if (!requested && d.m_valid_o && d.m_ready_o) {
                    requested = true; start = cycle + 1;
                }
                if (!taken && d.m_valid_o && d.m_ready_o && d.m_last_o) ++local_done;
                d.clk_i = 1; d.eval();
            }
            const unsigned wait = taken ? first - start : 10000;
            worst = std::max(worst, wait); ++cases;
            // Two clocks per byte plus sixteen for header/verdict transitions.
            if (!taken || netoff != net.size() || local_done != 1 || wait > 2 * 1515 + 16) {
                std::printf("FAIL %s:%d: mailbox local wait bound length=%u repeat=%u wait=%u local=%u\n",
                            __FILE__, __LINE__, length, repeat, wait, local_done);
                ++failures;
            }
            d.s_valid_i = 0; d.s_active_i = 0; d.net_valid_i = 0;
            for (unsigned n = 0; n < 4000; ++n) tick();
        }
        // Channel two is AECP; the local frame exercises its real admission.
        accepted += d.passed_o[1] & 65535;
        full += d.dropped_o[1] & 65535;
        rate += d.rate_dropped_o[1] & 65535;
        d.final();
    }
    ++cases;
    if (!accepted || !full || !rate) {
        std::printf("FAIL %s:%d: mailbox fixture must exercise acceptance, full rings and empty buckets\n",
                    __FILE__, __LINE__);
        ++failures;
    }
    std::printf("AECP local copies: accepted %u, full/size drops %u, rate drops %u\n", accepted, full, rate);
    std::printf("MAILBOX LOCAL WAIT: worst %u system cycles, %.4f us at 80 MHz; bound 3046 cycles, 38.075 us\n",
                worst, worst / 80.0);
    std::printf("%u checks: %u PASS, %u FAIL\n", cases, cases - failures, failures);
    return failures != 0;
}
