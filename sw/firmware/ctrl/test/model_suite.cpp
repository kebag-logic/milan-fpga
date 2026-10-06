// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// model_suite.cpp - the mailbox suite's checks (tb/verilator/mbx/suite.hpp),
// the ones the RTL passes through both bus adapters, run on the host model
// (#665 lanes F0 and FT). A difference between the model and the RTL fails
// here or there; the firmware's host tests may then rely on the model.
//
// The suite is written once against a bench and a checker. The RTL benches
// grade it with milan::tb::Checker; here GtestCheck grades the same calls as
// GoogleTest assertions, and each of the suite's groups is a test of its own,
// on a fresh model, in the order Suite::run() runs them.

#include <gtest/gtest.h>

#include <cstdint>
#include <ios>
#include <memory>

#include "fw_gtest.hpp"
#include "model_bench.hpp"
#include "suite.hpp"

FW_TALLY_LABEL("mbx (host model)");

namespace {

//! milan::tb::Checker's three calls as GoogleTest assertions, each named by
//! the suite's own words and returning the verdict as Checker does.
class GtestCheck {
 public:
    bool hex(const char* what, std::uint64_t got, std::uint64_t expected) {
        EXPECT_EQ(got, expected) << std::hex << "got=0x" << got << " exp=0x" << expected << "\n" << what;
        return got == expected;
    }
    bool dec(const char* what, std::uint64_t got, std::uint64_t expected) {
        EXPECT_EQ(got, expected) << what;
        return got == expected;
    }
    bool that(const char* what, bool condition) {
        EXPECT_TRUE(condition) << what;
        return condition;
    }
};

using ModelSuite = mbx_tb::Suite<mbx_tb::ModelBench, GtestCheck>;

class MbxModelGroup : public ::testing::TestWithParam<unsigned> {};

TEST_P(MbxModelGroup, PassesOnTheModel) {
    const auto model = std::make_unique<mbx_model>();
    GtestCheck check;
    mbx_tb::ModelBench bench(model.get());
    ModelSuite suite(bench, check);
    suite.run_group(GetParam());
    EXPECT_EQ(bench.bus_timeouts, 0u) << "no bus access went unanswered";
}

INSTANTIATE_TEST_SUITE_P(Suite, MbxModelGroup, ::testing::Range(0u, ModelSuite::kGroups),
                         [](const ::testing::TestParamInfo<unsigned>& info) {
                             return ModelSuite::kGroupNames[info.param];
                         });

}  // namespace
