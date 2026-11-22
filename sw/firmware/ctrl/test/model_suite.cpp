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

// The gPTP publication (contract 2.5, REQ-PTP-07): the snapshot the datapath holds is the GPTP_* words of the
// last GPTP_STATE write that moved GEN, as KL_mbx_cdc's committed bank is; tb/verilator/mbx/tb_cdc_pub.sv runs
// the same orderings on the RTL, so the closed loop's model answers as the crossing does (#884).
TEST(MbxModelGptp, TheSnapshotIsTheLastCommitWhole) {
    const auto m = std::make_unique<mbx_model>();
    mbx_model_reset(m.get());
    auto put = [&](std::uint32_t reg, std::uint32_t v) { mbx_model_write(m.get(), MBX_PUB_BASE + reg, v, 0xFu); };
    auto state = [](std::uint32_t gen) { return gen << MBX_GPTP_STATE_GEN_LSB | 1u << MBX_GPTP_STATE_AS_CAPABLE_LSB; };
    auto commit = [&](std::uint64_t gm, std::uint32_t gen) {
        put(MBX_PUB_REG_GPTP_GM_LO, static_cast<std::uint32_t>(gm));
        put(MBX_PUB_REG_GPTP_GM_HI, static_cast<std::uint32_t>(gm >> 32));
        put(MBX_PUB_REG_GPTP_STATE, state(gen));
    };
    auto held = [&](std::uint64_t gm, std::uint32_t gen) {
        mbx_model_pub view{};
        mbx_model_pub_view(m.get(), 0, &view);
        return view.gptp[0] == static_cast<std::uint32_t>(gm) && view.gptp[1] == static_cast<std::uint32_t>(gm >> 32) &&
               view.gptp[2] == state(gen);
    };
    commit(0x1212121212121212ull, 2);
    commit(0x2222222222222222ull, 3);
    put(MBX_PUB_REG_GPTP_GM_LO, 0x33333333u);
    EXPECT_TRUE(held(0x2222222222222222ull, 3)) << "an update begun after a commit reached the snapshot";
    put(MBX_PUB_REG_GPTP_GM_HI, 0x33333333u);
    put(MBX_PUB_REG_GPTP_STATE, state(3) | 1u << MBX_GPTP_STATE_SYNC_OK_LSB);
    EXPECT_TRUE(held(0x2222222222222222ull, 3)) << "a write that left GEN where it was published";
    commit(0xFFull, 0xFFu);
    commit(0x100ull, 0x00u);
    EXPECT_TRUE(held(0x100ull, 0x00u)) << "a commit that wrapped GEN through 0xFF did not publish";
}

}  // namespace
