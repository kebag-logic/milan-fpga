// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_bound.cpp - the save bound at the bound shape of #823, 32x32/2if
// TDM8 (docs/design/SAVED_STATE_FORMAT_32X32.md section 4, test plan T11 and
// T13; GoogleTest). The store is built at that shape, the flash model at the
// datasheet maxima the page grades (tSE 3 s per block, tPP 5 ms per page)
// with the suspend at its typical 15 us, and every service call is the
// rig's event loop of 100 us. The burst is assumption A1's: the first names
// that fill one delta segment, every one changed at once.
//
// T11: from the change to its delta read back, at most T-NVM-COMMIT-TIMEOUT
// (500 ms) in both worst cases the page models: the save meeting the other
// slot's erase, which it suspends, and meeting a compaction, which it waits
// one page for. T13: the deadline covers twice the worst append, the
// segment itself and the page ahead of it, the window excluded.

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

FW_TALLY_LABEL("ctrl_nvm saved-state store, the save bound at 32x32/2if TDM8");

namespace nvm_test {
namespace {

std::string num(long long v) { return std::to_string(v); }

//! The words that change every name of A1's burst.
std::vector<std::string> burst(std::vector<std::string> words) {
    for (const long long rid : fx().list("burst_ids")) {
        words.insert(words.end(), {"--set", set_word(static_cast<unsigned>(rid), value(static_cast<unsigned>(rid), 5))});
    }
    return words;
}

//! The save's time, from the mark (the change) to its delta read back.
long long took(const Result& r) {
    return r.ok_at.empty() || r.marks.empty() ? -1 : static_cast<long long>(r.ok_at[0] - r.marks[0]);
}

struct Worst {
    long long erase = -1;
    long long compaction = -1;
    long long deadline_ms = -1;     //!< the store's NVM_APPEND_TIMEOUT_MS
};

//! The two worst cases, each run once for every test that grades them.
const Worst& worst() {
    static const Worst w = [] {
        Worst out;
        Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
        std::vector<std::string> words = burst({"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--times",
                                                "3000:5000", "--until-bg", num(NVM_B_ERASE_WAIT), "--mark"});
        words.push_back("--until-idle");
        Result r = go(Port::Model, f, words);
        EXPECT_TRUE(r.at("appends") == 1 && r.at("suspends") == 1 && r.at("failed") == 0 &&
                    r.at("programs") == NVM_SEG_PAGES)
            << "the burst during the erase: " << r.text();
        out.erase = took(r);
        out.deadline_ms = r.at("append_timeout_ms");
        Files g = fx().files({{"g.bin", "golden@5"}});
        words = burst({"--slot-b", "g.bin", "--boot", "--times", "3000:5000", "--until-bg", num(NVM_B_READY),
                       "--commit-try", "--until-programs", "3", "--mark"});
        words.insert(words.end(), {"--until-ok", "1"});
        r = go(Port::Model, g, words);
        EXPECT_TRUE(r.at("appends") == 1 && r.at("compacting") == 1 && r.at("failed") == 0)
            << "the burst during a compaction: " << r.text();
        out.compaction = took(r);
        std::printf("  save bound at 32x32/2if TDM8, change to read back: %lld us during the erase, %lld us during "
                    "a compaction (bound %lld ms)\n",
                    out.erase, out.compaction, kAppendTimeoutMs);
        return out;
    }();
    return w;
}

// T11: the owner's 0.5 s, from the change to durable, in both worst cases.
TEST(NvmBound, save_bound) {
    EXPECT_TRUE(fx().num("n_names") == static_cast<long long>(NVM3_CAP_NAME) && NVM_N_REC == 1108u &&
                fx().list("burst_ids").size() == 96u)
        << "not the bound shape: " << fx().num("n_names") << " names, " << NVM_N_REC << " records, a burst of "
        << fx().list("burst_ids").size() << " names";
    EXPECT_TRUE(in(worst().erase, kWindowMs * kMs, kAppendTimeoutMs * kMs))
        << "the burst during the erase took " << worst().erase << " us from the change";
    EXPECT_TRUE(in(worst().compaction, kWindowMs * kMs, kAppendTimeoutMs * kMs))
        << "the burst during a compaction took " << worst().compaction << " us from the change";
}

// T13: the store's T-NVM-COMMIT-TIMEOUT covers twice the worst append.
TEST(NvmBound, commit_deadline) {
    const long long append = std::max(worst().erase, worst().compaction) - kWindowMs * kMs;
    std::printf("  append at 32x32/2if TDM8, due to read back: %lld us; twice it %lld us, the deadline %lld ms\n",
                append, 2 * append, worst().deadline_ms);
    EXPECT_TRUE(append > 0 && 2 * append <= worst().deadline_ms * kMs)
        << "T-NVM-COMMIT-TIMEOUT " << worst().deadline_ms << " ms does not cover twice the worst append, " << append
        << " us";
}

}  // namespace
}  // namespace nvm_test
