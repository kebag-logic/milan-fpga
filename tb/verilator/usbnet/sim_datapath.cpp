// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Check all production LED exports, including nonzero AAF source indices.
#include "Vled_datapath.h"
#include "../../common/verilator_harness.hpp"
#include <cstdio>

#ifndef STREAMS_TB
#define STREAMS_TB 1
#endif
#define CHECK(test, name) do { ++checks; if (!(test)) { ++failures; \
    if (failures < 25) std::printf("FAIL %s:%d %s\n", __FILE__, __LINE__, name); } } while (0)

int main() {
    unsigned checks = 0, failures = 0;
    milan::tb::Model<Vled_datapath> model;
    auto &d = *model;
    auto edge = [&]() { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); };
    d.rst_ni = 0; edge(); d.rst_ni = 1;
    // The checked-in Arty descriptors declare INTERNAL, CRF, then each AAF
    // input. Expectations come from that declaration, never the DUT decode.
    for (unsigned source = 0; source < STREAMS_TB + 3; ++source)
    for (unsigned aaf = 0; aaf < (1u << STREAMS_TB); ++aaf)
    for (unsigned crf = 0; crf != 2; ++crf)
    for (unsigned output = 0; output <= OUTPUTS_TB; ++output)
    for (unsigned uncertain = 0; uncertain != 2; ++uncertain)
    for (unsigned servo = 0; servo != 2; ++servo) {
        d.source_index_i = source; d.aaf_locked_i = aaf;
        d.crf_locked_i = crf; d.output_open_i = output ? 1u << (output - 1) : 0;
        d.clock_uncertain_i = uncertain; d.servo_locked_i = servo;
        edge(); edge();
        const bool internal = source == 0;
        const bool follow = source >= 1 && source <= STREAMS_TB + 1;
        const bool selected = source >= 2 && source <= STREAMS_TB + 1
                            ? (aaf & (1u << (source - 2))) != 0 : crf;
        const bool clock_lock = !uncertain && (!follow || servo);
        CHECK(d.monitor_locked_o == aaf, "monitor exports every input lock");
        CHECK(bool(d.levels_o & 1) == bool(aaf || crf), "LD2 input reduction includes AAF and CRF");
        CHECK(bool(d.levels_o & 2) == bool(output), "LD2 output reduction includes every transmit gate");
        CHECK(bool(d.levels_o & 4) == internal, "LD3 internal source decode");
        CHECK(bool(d.levels_o & 8) == follow, "LD3 stream source decode");
        CHECK(bool(d.levels_o & 16) == selected, "LD3 selected input lock index");
        CHECK(bool(d.levels_o & 32) == clock_lock, "LD3 clock-domain lock predicate");
        CHECK(bool(d.stream_o) == bool(aaf || crf || output), "datapath drives LD2 predicate");
        CHECK(bool(d.clock_o) == (internal || (clock_lock && (!follow || selected))),
              "datapath drives LD3 predicate");
    }
    d.rst_ni = 0; edge();
    CHECK((d.levels_o & 12) == 0, "reset clears stored source decode");
    CHECK(!d.clock_o && !d.stream_o, "reset clears datapath LED predicates");
    std::printf("datapath LEDs: %u checks, %u failures\n", checks, failures);
    return failures ? 1 : 0;
}
