// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Real AECP commands select the descriptor; the fabric predicate consumes its
// decoded source kind and explicit media levels. This is a seam test, not a
// processor-to-datapath bus simulation or a measurement of media acquisition.
// clock_commands.py appends this to the unchanged AECP fixture translation unit.
#include "VKL_status_led_truth.h"

struct FabricClock : Core {
    VKL_status_led_truth leds;
    void edge() { leds.clk_i = 0; leds.eval(); leds.clk_i = 1; leds.eval(); }
    unsigned source(unsigned kind) {
        for (const auto &d : descriptors)
            if (d.configuration == a.configuration && d.type == 10 && get(d.value + 72, 2) == kind)
                return d.index;
        ADD_FAILURE() << "declared clock source missing";
        return 0;
    }
    void select(unsigned index, bool flow, bool locked) {
        auto body = target(36, 0, 8); put(body, 4, index, 2);
        ask(22, body);
        ASSERT_FALSE(sent.empty());
        ASSERT_EQ(sent.back().second[16] >> 3, 0u) << "SET_CLOCK_SOURCE succeeds";
        ASSERT_EQ(get(desc(36).value + 70, 2), index) << "selection reaches the descriptor";
        const auto kind = get(desc(10, index).value + 72, 2);
        leds.clock_internal_i = kind == 0;
        leds.clock_stream_i = kind == 2;
        leds.source_locked_i = flow;
        leds.clock_locked_i = locked;
        leds.input_locked_i = flow;
        leds.output_open_i = 0;
        leds.rst_ni = 0; edge(); leds.rst_ni = 1; edge();
    }
};
TEST_F(FabricClock, Internal)
{
    select(source(0), false, false);
    EXPECT_TRUE(leds.clock_o) << "internal selection lights LD3 without any lock";
}
TEST_F(FabricClock, Flowing)
{
    select(source(2), true, true);
    EXPECT_TRUE(leds.clock_o) << "flowing selected stream with media lock lights LD3";
    select(source(2), true, false);
    EXPECT_FALSE(leds.clock_o) << "flow without media clock lock leaves LD3 dark";
}
TEST_F(FabricClock, Stopped)
{
    select(source(2), false, true);
    EXPECT_FALSE(leds.clock_o) << "stopped selected stream leaves LD3 dark";
    leds.input_locked_i = 1; edge();
    EXPECT_TRUE(leds.stream_o) << "another receiving input lights LD2";
    EXPECT_FALSE(leds.clock_o) << "another input cannot satisfy the selected source";
}
TEST_F(FabricClock, External)
{
    const auto index = source(0);
    put(desc(10, index).value + 72, 1, 2);
    select(index, false, false);
    EXPECT_FALSE(leds.clock_o) << "external source requires clock lock";
    select(index, false, true);
    EXPECT_TRUE(leds.clock_o) << "locked external source needs no input stream";
}
