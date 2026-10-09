// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// fw_gtest.hpp - the GoogleTest harness of the bare-metal firmware's host
// tests (#665 lane FT).
//
// Every test binary of sw/firmware links fw_gtest_main.cpp, which installs
// the tally listener and runs every registered test. The listener prints the
// one summary shape scripts/suite_tally.py reads,
//
//     == <label>: checks: N   failures: M ==
//     RESULT: PASS | FAIL
//
// where N is the tests run and M the tests that failed, were skipped, or
// crashed, plus one for a failure outside any test and one per disabled test.
// Each failed assertion also prints a `[FAIL] <Suite.Test>: ...` line, the
// marker suite_tally.py's verdict reads and the planted-defect campaigns
// match a test by.
//
// A test that crashes (a fatal signal) or ends the program early (exit())
// still prints a tally, with the test it was in counted as a failure; one that
// leaves without either (_exit()) prints none, which the reader refuses as
// NOCOUNT. README.md, "The tally", lists the planted cases that prove each.
//
// Each binary names its tally once, in one of its test files:
//
//     FW_TALLY_LABEL("ctrl port, driver and loop (host model)");

#ifndef FW_GTEST_HPP
#define FW_GTEST_HPP

namespace fw_test {

// The label of this binary's tally line; FW_TALLY_LABEL defines it.
const char* tally_label();

}  // namespace fw_test

#define FW_TALLY_LABEL(text)             \
    const char* fw_test::tally_label() { \
        return text;                     \
    }

#endif  // FW_GTEST_HPP
