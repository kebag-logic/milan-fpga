// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// fw_gtest_main.cpp - main() of every firmware test binary: GoogleTest and
// GoogleMock, with the tally listener of fw_gtest.hpp.
//
// The tally is the binary's verdict as scripts/suite_tally.py reads it, so
// it must never look like agreement when a test did not finish. Three ways
// out of a run are handled:
//
//   * the run ends: the listener prints the tally, every failed, skipped or
//     disabled test counted, and each failure outside a test (the program's,
//     or a test suite's set-up or tear-down) counted once;
//   * a fatal signal (SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGABRT): the handler
//     prints a [FAIL] line naming the test it was in and a tally with that
//     test counted as failed, then dies of the same signal;
//   * exit() before the run ended: an atexit handler does the same, so a
//     test that calls exit(0) still leaves a failing tally behind.
//
// The handler and the atexit path print with write(2) only, from state the
// listener stores outside them: they run where stdio may not be called.
// stdout is unbuffered so GoogleTest's own lines and these keep their order.

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <unistd.h>

#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>

#include "fw_gtest.hpp"

namespace {

// What the crash and early-exit paths print. It has static storage because a
// signal handler can reach nothing else; only the listener writes it.
struct TallyState {
    char label[160];
    char test[256];          // the test running now, empty between tests
    unsigned long checks;    // tests ended
    unsigned long failures;  // tests ended failed or skipped
    bool reported;           // the tally has been printed
};

TallyState state;

void put(const char* text) {
    const ssize_t written = write(STDOUT_FILENO, text, std::strlen(text));
    static_cast<void>(written);  // nothing else can be done about a lost line here
}

void put_number(unsigned long value) {
    char digits[24];
    std::size_t at = sizeof digits - 1u;
    digits[at] = '\0';
    do {
        digits[--at] = static_cast<char>('0' + value % 10u);
        value /= 10u;
    } while (value != 0u && at > 0u);
    put(&digits[at]);
}

void put_tally(unsigned long checks, unsigned long failures) {
    put("== ");
    put(state.label);
    put(": checks: ");
    put_number(checks);
    put("   failures: ");
    put_number(failures);
    put(" ==\n");
    put(failures == 0u ? "RESULT: PASS\n" : "RESULT: FAIL\n");
    state.reported = true;
}

const char* current_test() {
    return state.test[0] != '\0' ? state.test : "(program)";
}

// The run did not end: the test it was in fails, and the tally says so.
void report_unfinished(const char* how) {
    put("  [FAIL] ");
    put(current_test());
    put(how);
    put_tally(state.checks + 1u, state.failures + 1u);
}

extern "C" void on_fatal_signal(int sig) {
    if (!state.reported) {
        put("\n");
        put("  [FAIL] ");
        put(current_test());
        put(": crashed on signal ");
        put_number(static_cast<unsigned long>(sig));
        put("\n");
        put_tally(state.checks + 1u, state.failures + 1u);
    }
    static_cast<void>(std::signal(sig, SIG_DFL));
    static_cast<void>(std::raise(sig));
}

extern "C" void on_exit_early() {
    if (!state.reported) {
        report_unfinished(": the program ended before its tests did\n");
    }
}

// The last line of a failure's message: the test's own words when it gave
// any (EXPECT_...() << "..."), else GoogleTest's last line of the values.
const char* last_line(const char* message, std::size_t* length) {
    const char* end = message + std::strlen(message);
    while (end > message && end[-1] == '\n') {
        --end;
    }
    const char* start = end;
    while (start > message && start[-1] != '\n') {
        --start;
    }
    *length = static_cast<std::size_t>(end - start);
    return start;
}

// A disabled test runs nothing and would otherwise pass in silence: each one
// the filter selects is named and counted as a failure.
unsigned long report_disabled(const ::testing::UnitTest& unit) {
    unsigned long disabled = 0;
    for (int k = 0; k < unit.total_test_suite_count(); ++k) {
        const ::testing::TestSuite* suite = unit.GetTestSuite(k);
        for (int t = 0; t < suite->total_test_count(); ++t) {
            const ::testing::TestInfo* info = suite->GetTestInfo(t);
            const bool named_disabled =
                std::strncmp(suite->name(), "DISABLED_", 9) == 0 || std::strncmp(info->name(), "DISABLED_", 9) == 0;
            if (named_disabled && info->is_reportable() && !info->should_run()) {
                std::printf("  [FAIL] %s.%s: disabled, so it runs nothing\n", suite->name(), info->name());
                disabled++;
            }
        }
    }
    return disabled;
}

class TallyListener final : public ::testing::EmptyTestEventListener {
 public:
    void OnTestStart(const ::testing::TestInfo& info) override {
        std::snprintf(state.test, sizeof state.test, "%s.%s", info.test_suite_name(), info.name());
    }

    void OnTestPartResult(const ::testing::TestPartResult& part) override {
        if (part.passed()) {
            return;
        }
        std::size_t length = 0;
        const char* line = last_line(part.message(), &length);
        std::printf("  [FAIL] %s: %s%.*s\n", current_test(), part.skipped() ? "skipped: " : "",
                    static_cast<int>(length), line);
    }

    void OnTestEnd(const ::testing::TestInfo& info) override {
        state.checks++;
        if (info.result()->Failed() || info.result()->Skipped()) {
            state.failures++;
        }
        state.test[0] = '\0';
    }

    void OnTestProgramEnd(const ::testing::UnitTest& unit) override {
        unsigned long failures = state.failures;
        if (unit.ad_hoc_test_result().Failed()) {
            std::printf("  [FAIL] (program): a failure outside every test\n");
            failures++;
        }
        for (int k = 0; k < unit.total_test_suite_count(); ++k) {
            const ::testing::TestSuite* suite = unit.GetTestSuite(k);
            if (suite->ad_hoc_test_result().Failed()) {
                std::printf("  [FAIL] %s: a failure in its set-up or tear-down\n", suite->name());
                failures++;
            }
        }
        failures += report_disabled(unit);
        put_tally(state.checks, failures);
    }
};

}  // namespace

int main(int argc, char** argv) {
    static_cast<void>(std::setvbuf(stdout, nullptr, _IONBF, 0));
    std::snprintf(state.label, sizeof state.label, "%s", fw_test::tally_label());
    ::testing::InitGoogleMock(&argc, argv);
    // GoogleTest takes ownership of an appended listener (its documented API).
    ::testing::UnitTest::GetInstance()->listeners().Append(new TallyListener);
    for (const int sig : {SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGABRT}) {
        static_cast<void>(std::signal(sig, on_fatal_signal));
    }
    static_cast<void>(std::atexit(on_exit_early));
    return RUN_ALL_TESTS();
}
