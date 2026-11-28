// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_window.cpp - the first-dirty windows (DR2a), the binding class's
// own (#1009): Milan v1.2 5.5.3.5.3 saves the binding parameters before the
// BIND_RX_RESPONSE is sent, and 5.3.8.3 counts a stream input's started/stopped
// state with them, so a change of a binding record is captured 100 ms after
// the first such change; every other record keeps 1,000 ms. A window is not
// restarted, a save captures everything dirty, and a binding change the save in
// flight cannot take opens the next window. Every save writes the container
// whole, so each window's end is read off its save's erase.

#include <cstdint>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

namespace nvm_test {
namespace {

std::string num(long long v) { return std::to_string(v); }

std::vector<std::string> concat(std::vector<std::string> a, const std::vector<std::string>& b) {
    a.insert(a.end(), b.begin(), b.end());
    return a;
}

const std::vector<std::string> kTwin = {"--slot-a", "a5.bin", "--slot-b", "b6.bin"};
const std::vector<std::string> kDump = {"--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"};
Files twin() { return fx().files({{"a5.bin", "golden@5"}, {"b6.bin", "golden@6"}}); }

std::vector<unsigned> bindings() {
    std::vector<unsigned> out;
    for (const long long id : fx().list("binding_ids")) {
        out.push_back(static_cast<unsigned>(id));
    }
    return out;
}

//! Each class's window, as the time from the change to its save's erase, which follows the window by the capture and
//! the seal: at most kAfter at every shape.
constexpr long long kBind = 100 * kMs;
constexpr long long kOther = 1000 * kMs;
constexpr long long kAfter = 20 * kMs;

//! A boot of what the run left in the two slots restores `want`.
void boots_back(Port port, Files& f, const Payloads& want, const std::string& what) {
    const Result b = go(port, f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(b.at("terminal") == NVM_T_COMPLETE) << what << ": " << b.text();
    expect_state(f, "st", want, what);
}

// The window's length is the record's class: every binding record's is 100 ms, and it is 1,000 ms for the first record
// below and the first above their block, the shape's first record and its last.
TEST_P(NvmBoth, binding_window) {
    const std::vector<unsigned> ids = bindings();
    unsigned below = 0;
    unsigned above = 0;
    for (const unsigned rid : rids()) {
        if (rid < ids.front()) {
            below = rid;
        } else if (rid > ids.back() && above == 0u) {
            above = rid;
        }
    }
    std::vector<std::pair<unsigned, long long>> cases;
    for (const unsigned rid : ids) {
        cases.emplace_back(rid, kBind);
    }
    for (const unsigned rid : {rids().front(), below, above, rids().back()}) {
        cases.emplace_back(rid, kOther);
    }
    for (const auto& [rid, window] : cases) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, {"--boot", "--mark", "--set", set_word(rid, value(rid, 7)), "--until-idle"}));
        EXPECT_TRUE(r.at("ok") == 1 && in(after_mark(r, 0), window, window + kAfter))
            << "record " << rid << ": erased " << after_mark(r, 0) << " us after it, want " << window << " to "
            << window + kAfter << ": " << r.text();
    }
}

// The window starts at the class's first change and is not restarted: a second binding change 60 ms into it, and one
// again 30 ms later, are in the same save, at the first one's time; so is a change to the same record.
TEST_P(NvmBoth, binding_window_not_restarted) {
    const std::vector<unsigned> ids = bindings();
    const unsigned rb = ids.front();
    const unsigned rb2 = ids.back();
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--mark", "--set", set_word(rb, value(rb, 7)), "--run-ms", "60",
                                              "--set", set_word(rb2, value(rb2, 7)), "--run-ms", "30", "--set",
                                              set_word(rb, value(rb, 8)), "--until-idle"},
                                             kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && in(after_mark(r, 0), kBind, kBind + kAfter))
        << "erased " << after_mark(r, 0) << " us after the first change: " << r.text();
    boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 8)}, {rb2, value(rb2, 7)}}), "both changes");
}

// The earliest end of the open windows starts the capture, which takes everything dirty: a binding change 300 ms into
// another record's window, 60 ms before that window's end, and another record's 50 ms into a binding's.
TEST_P(NvmBoth, earliest_window_takes_everything) {
    const unsigned rb = bindings().front();
    const unsigned other = rids().back();
    for (const auto& [wait, late] : {std::pair<long long, long long>{300, kBind}, {940, 60 * kMs}}) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, concat({"--boot", "--set", set_word(other, value(other, 7)), "--run-ms",
                                                  num(wait), "--mark", "--set", set_word(rb, value(rb, 7)),
                                                  "--until-idle", "--run-ms", "2000"},
                                                 kDump)));
        EXPECT_TRUE(r.at("ok") == 1 && in(after_mark(r, 0), late - 5 * kMs, late + kAfter))
            << "a binding change " << wait << " ms into another window: erased " << after_mark(r, 0)
            << " us after it: " << r.text();
        boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 7)}, {other, value(other, 7)}}),
                   "one save takes both");
    }
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--mark", "--set", set_word(rb, value(rb, 8)), "--run-ms", "50",
                                              "--set", set_word(other, value(other, 8)), "--until-idle", "--run-ms",
                                              "2000"},
                                             kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && in(after_mark(r, 0), kBind, kBind + kAfter))
        << "another record's change inside a binding window: erased " << after_mark(r, 0) << ": " << r.text();
    boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 8)}, {other, value(other, 8)}}),
               "one save takes both, the other way");
}

// After a save, the next binding change opens a window of its own, its full length.
TEST_P(NvmBoth, next_binding_window) {
    const unsigned rb = bindings().front();
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--run-ms", "700",
                                       "--mark", "--set", set_word(rb, value(rb, 8)), "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 2 && in(after_mark(r, 1), kBind, kBind + kAfter))
        << "erased " << after_mark(r, 1) << " us after the second change: " << r.text();
}

// A binding change the save in flight cannot take opens the next window, 100 ms from the change; where the rest of that
// save is longer, the next save starts at the first idle step after it. Any other record's change starts the next save
// at that step whatever the window, as #920 has it, and that save takes a binding change with it.
TEST_P(NvmBoth, binding_change_in_flight_opens_window) {
    const unsigned rb = bindings().front();
    const unsigned rb2 = bindings().back();
    const unsigned other = rids().back();
    const auto flight = [&](const char* times, const std::vector<unsigned>& changes, Files& f) {
        std::vector<std::string> words =
            concat(kTwin, {"--boot", "--times", times, "--set", set_word(rb, value(rb, 7)), "--until-phase",
                           num(NVM_P_SEAL), "--mark"});
        for (const unsigned rid : changes) {
            words = concat(words, {"--set", set_word(rid, value(rid, 7))});
        }
        return go(port(), f, concat(words, concat({"--until-idle"}, kDump)));
    };
    // a short save: its rest ends inside the window
    Files f = twin();
    Result r = flight("1:20", {rb2}, f);
    EXPECT_TRUE(r.at("ok") == 2 && in(after_mark(r, 1), kBind, kBind + kAfter) &&
                static_cast<long long>(r.erases[1] - r.ok_at[0]) > kAfter)
        << "a short save in flight: erased " << after_mark(r, 1) << " us after the change: " << r.text();
    boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 7)}}), "both saves");
    // a long one: its rest outlasts the window
    f = twin();
    r = flight("400:500", {rb2}, f);
    EXPECT_TRUE(r.at("ok") == 2 && after_mark(r, 1) > 400 * kMs &&
                in(static_cast<long long>(r.erases[1] - r.ok_at[0]), 0, kAfter))
        << "a long save in flight: erased " << after_mark(r, 1) << " us after the change: " << r.text();
    boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 7)}}), "both long saves");
    // another record's change with it: the first idle step, whichever came first
    for (const std::vector<unsigned>& changes : {std::vector<unsigned>{other, rb2}, {rb2, other}}) {
        f = twin();
        r = flight("1:20", changes, f);
        EXPECT_TRUE(r.at("ok") == 2 && after_mark(r, 1) < kBind &&
                    in(static_cast<long long>(r.erases[1] - r.ok_at[0]), 0, kAfter))
            << "another record's change in flight too: erased " << after_mark(r, 1) << ": " << r.text();
        boots_back(port(), f,
                   with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 7)}, {other, value(other, 7)}}),
                   "the second save takes both");
    }
}

// A failed attempt's backoff (DR2c) is not shortened by a binding change's window: the retry takes the change.
TEST_P(NvmBoth, binding_change_in_backoff) {
    const unsigned rb = bindings().front();
    const unsigned other = rids().back();
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--fault", "erase-refuse:1", "--set",
                                              set_word(other, value(other, 7)), "--until-phase", num(NVM_P_ERASE),
                                              "--run-ms", "200", "--mark", "--set", set_word(rb, value(rb, 7)),
                                              "--until-idle"},
                                             kDump)),
                        {"ls_refused"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 1 && r.fail_at.size() == 1u && r.ok_at.size() == 1u &&
                r.ok_at[0] - r.fail_at[0] >= static_cast<std::uint64_t>(1000 * kMs))
        << "a binding change 200 ms into a backoff: " << r.text();
    boots_back(port(), f, with(fx().payloads("golden"), {{rb, value(rb, 7)}, {other, value(other, 7)}}),
               "the retry takes both");
}

// A burst of 64 bindings, one every 10 ms over every input, with the part's erase and page times: it converges, the
// last value of each bound, one erase a save, and every save whole.
TEST_P(NvmBoth, burst_of_64_bindings) {
    const std::vector<unsigned> ids = bindings();
    Files f = twin();
    std::vector<std::string> words = concat(kTwin, {"--boot", "--times", "120:500", "--mark"});
    Payloads want = fx().payloads("golden");
    for (unsigned k = 0; k < 64u; ++k) {
        const unsigned rid = ids[k % ids.size()];
        words = concat(words, {"--set", set_word(rid, value(rid, 1u + k)), "--run-ms", "10"});
        want[rid] = value(rid, 1u + k);
    }
    const Result r = go(port(), f, concat(words, concat({"--until-idle", "--run-ms", "3000"}, kDump)));
    EXPECT_TRUE(r.at("dirty") == 0 && r.at("pending") == 0 && r.at("failed") == 0 && r.at("stale") == 0)
        << "the burst converges: " << r.text();
    // 640 ms of changes: the first save starts at its window's end, and each later one after the save before it
    EXPECT_TRUE(in(r.at("ok"), 2, 6) && r.at("erases") == r.at("ok") && r.at("programs") == r.at("ok") * pages() &&
                in(after_mark(r, 0), kBind, kBind + kAfter))
        << "saves of the burst: " << r.at("ok") << ", " << r.text();
    boots_back(port(), f, want, "the burst's last values");
}

// #1009's acceptance, whole commits: the power cut every 10 ms from a binding change to 3 s after it, and inside each
// of its save's media effects, with the part's erase and page times; every cut boots the old binding or the new one,
// never neither and never a mix, always the new one from 800 ms on, and the next change commits.
TEST_P(NvmBoth, swept_cut) {
    Files f = twin();
    const Result r = go(port(), f, concat(kTwin, {"--times", "150:500", "--sweep-gate", "800", "--sweep-cut", "10"}));
    const auto at = [&r](const char* k) { return r.sweep.count(k) != 0u ? r.sweep.at(k) : -1; };
    EXPECT_TRUE(at("bad") == 0 && at("cases") >= 301 && at("old") > 0 && at("new") > 0 && at("saves") == 1 &&
                at("effects") == 1 + pages() && in(at("durable_us"), kBind, 800 * kMs))
        << "cases " << at("cases") << " old " << at("old") << " new " << at("new") << " bad " << at("bad")
        << " effects " << at("effects") << " durable " << at("durable_us") << " us; " << r.text();
    for (const std::string& line : r.fails) {
        ADD_FAILURE() << line;
    }
}

// The same for a binding change that arrives during another record's save, at eight points of it and more, from the
// capture's end to the verify's: the two saves' effects are swept, and every cut from the bound on boots the new
// binding. The bound is the rest of the save in flight and one more (#1009, DR2a).
TEST_P(NvmBoth, swept_cut_in_flight) {
    // phase, ms into it
    const std::vector<std::pair<int, int>> arrivals = {
        {NVM_P_SEAL, 0},       {NVM_P_ERASE, 0},   {NVM_P_ERASE_WAIT, 0}, {NVM_P_ERASE_WAIT, 60},
        {NVM_P_ERASE_WAIT, 140}, {NVM_P_BLANKCHECK, 0}, {NVM_P_PROGRAM, 0},  {NVM_P_PROGRAM_WAIT, 2},
        {NVM_P_VERIFY, 0}};
    const std::string gate = pages() <= 16 ? "450" : "950";
    for (const auto& [phase, ms] : arrivals) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, {"--times", "150:500", "--sweep-flight", num(phase) + ":" + num(ms),
                                           "--sweep-gate", gate, "--sweep-cut", "25"}));
        const auto at = [&r](const char* k) { return r.sweep.count(k) != 0u ? r.sweep.at(k) : -1; };
        EXPECT_TRUE(at("bad") == 0 && at("cases") >= 121 && at("old") > 0 && at("new") > 0 && at("saves") == 2 &&
                    at("effects") == 2 * (1 + pages()))
            << "phase " << phase << " + " << ms << " ms: cases " << at("cases") << " old " << at("old") << " new "
            << at("new") << " bad " << at("bad") << " effects " << at("effects") << " saves " << at("saves")
            << " durable " << at("durable_us") << " us; " << r.text();
        for (const std::string& line : r.fails) {
            ADD_FAILURE() << "phase " << phase << " + " << ms << " ms: " << line;
        }
    }
}

}  // namespace
}  // namespace nvm_test
