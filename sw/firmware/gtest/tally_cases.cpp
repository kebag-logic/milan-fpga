// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tally_cases.cpp - the planted cases of the tally listener's self-test
// (tally_selftest.py). One binary; each run selects one case with
// --gtest_filter, and every case but Pass must leave a log that
// scripts/suite_tally.py reads as a failure.

#include <gtest/gtest.h>
#include <unistd.h>

#include <csignal>
#include <cstdlib>
#include <stdexcept>

#include "fw_gtest.hpp"

FW_TALLY_LABEL("firmware tally listener (planted cases)");

namespace {

// Not a constant the compiler can see through, so a planted case cannot be
// folded away.
volatile int planted_one = 1;

}  // namespace

TEST(Pass, One) {
    EXPECT_EQ(planted_one, 1);
}

TEST(Fail, Expect) {
    EXPECT_EQ(planted_one, 2) << "a planted failing assertion";
}

TEST(Crash, Segv) {
    static_cast<void>(std::raise(SIGSEGV));
}

TEST(Crash, Abort) {
    std::abort();
}

TEST(Exit, Zero) {
    std::exit(0);
}

TEST(Exit, Immediate) {
    _exit(0);
}

TEST(Skip, Silent) {
    GTEST_SKIP() << "a planted skip";
}

TEST(Throw, Uncaught) {
    throw std::runtime_error("a planted exception");
}

TEST(Disabled, DISABLED_NeverRuns) {
    EXPECT_EQ(planted_one, 1);
}

class SetUpFails : public ::testing::Test {
 protected:
    static void SetUpTestSuite() { ADD_FAILURE() << "a planted failure in a suite's set-up"; }
};

TEST_F(SetUpFails, Body) {
    EXPECT_EQ(planted_one, 1);
}
