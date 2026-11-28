// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Real AECP commands select the descriptor; the fabric predicate consumes its
// decoded source kind and explicit media levels. This is a seam test, not a
// processor-to-datapath bus simulation or a measurement of media acquisition.
// clock_commands.py appends this to the unchanged AECP fixture translation unit.
#include "VKL_status_led_truth.h"
#include "Vled_datapath.h"
#include "../../common/verilator_harness.hpp"

struct FabricClock : Core {
    milan::tb::Model<VKL_status_led_truth> model;
    VKL_status_led_truth &leds = *model;
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

// A successful SET_CLOCK_SOURCE's stored index feeds the real datapath.
// No source-kind decode occurs in this fixture. Media producers are explicit;
// processor/MMIO transport and lock acquisition are outside this seam.
struct DatapathClock : Core {
    milan::tb::Model<Vled_datapath> model;
    Vled_datapath &d = *model;
    void edge() { d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval(); }
    void settle() { edge(); edge(); }
    void select(unsigned index) {
        auto body = target(36, 0, 8); put(body, 4, index, 2);
        ask(22, body);
        ASSERT_FALSE(sent.empty());
        ASSERT_EQ(sent.back().second[16] >> 3, 0u) << "SET_CLOCK_SOURCE succeeds";
        ASSERT_EQ(get(desc(36).value + 70, 2), index) << "selection reaches the descriptor";
        d.source_index_i = get(desc(36).value + 70, 2);
        d.rst_ni = 0; edge(); d.rst_ni = 1; settle();
    }
};
TEST_F(DatapathClock, Internal)
{
    d.clock_uncertain_i = 1; d.servo_locked_i = 0;
    select(0);
    EXPECT_TRUE(d.clock_o) << "stored internal source lights LD3 without lock";
    EXPECT_FALSE(d.stream_o);
}
TEST_F(DatapathClock, CrfFlowingAndStopped)
{
    d.crf_locked_i = 1; d.clock_uncertain_i = 0; d.servo_locked_i = 1;
    select(1);
    EXPECT_TRUE(d.stream_o); EXPECT_TRUE(d.clock_o);
    d.servo_locked_i = 0; settle();
    EXPECT_FALSE(d.clock_o) << "selected CRF needs recovered media clock";
    d.servo_locked_i = 1; d.crf_locked_i = 0;
    select(1);
    EXPECT_FALSE(d.clock_o) << "stopped selected CRF leaves LD3 dark";
}
TEST_F(DatapathClock, EachAafInput)
{
    for (unsigned input = 0; input != 4; ++input) {
        d.aaf_locked_i = 1u << input; d.crf_locked_i = 0;
        d.clock_uncertain_i = 0; d.servo_locked_i = 1;
        select(2 + input);
        EXPECT_TRUE(d.clock_o) << "selected flowing AAF input lights LD3";
        d.aaf_locked_i = 1u << ((input + 1) % 4);
        settle();
        EXPECT_TRUE(d.stream_o) << "another receiving input lights LD2";
        EXPECT_FALSE(d.clock_o) << "another input cannot satisfy the selected source";
        d.aaf_locked_i = 0;
        select(2 + input);
        EXPECT_FALSE(d.clock_o) << "stopped selected AAF leaves LD3 dark";
    }
}
