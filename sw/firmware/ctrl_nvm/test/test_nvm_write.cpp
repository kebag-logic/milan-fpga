// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_write.cpp - the write path of the saved-state store (#665 lanes F1
// and FT; GoogleTest): the append and its atomicity rules
// (docs/design/SAVED_STATE_FORMAT_32X32.md section 4, #823 decisions 3 to 7;
// docs/design/SAVED_STATE_FASTCONNECT.md section 7;
// SAVED_STATE_MATERIALIZATION.md section 15.1 DR2b, DR2c and DR5), the
// writer held while a slot's authority is unknown, the time base, the
// command-master waits, the power cut at every write step and the service
// bound. The journal's own rules (replay, compaction, the erase suspend, the
// save bound) are test_nvm_journal.cpp; the round trip against the recorded
// vectors is test_nvm_vector.cpp.
//
// One test per check of the hand-rolled suite this replaced
// (nvm_checks_write.py until #665 FT), under the check's own name. Every slot
// is compared whole with the bytes scripts/nvm_klj3.py assembles for the same
// records: a base container, then its deltas. A save appends a delta to the
// authoritative slot; a failed one leaves its segment torn, and the retry is a
// compaction into the other slot, the base at the old sequence and the save's
// records after it as a delta.

#include <gtest/gtest.h>

#include <array>
#include <cstdlib>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

namespace nvm_test {
namespace {

//! The port's no-progress bound on one wait (LS_POLL_MAX); a drain reads once more.
constexpr long long kPollMax = 4096;

std::string num(long long v) { return std::to_string(v); }

//! The last record of the shape with a new payload.
std::pair<unsigned, Bytes> one_change(unsigned seed) {
    const unsigned rid = rids().back();
    return {rid, value(rid, seed)};
}

std::vector<std::string> concat(std::vector<std::string> a, const std::vector<std::string>& b) {
    a.insert(a.end(), b.begin(), b.end());
    return a;
}

std::vector<long long> gaps(const std::vector<std::uint64_t>& at) {
    std::vector<long long> out;
    for (std::size_t k = 1; k < at.size(); ++k) {
        out.push_back(static_cast<long long>(at[k]) - static_cast<long long>(at[k - 1]));
    }
    return out;
}

bool all_at_least(const std::vector<long long>& v, long long floor) {
    for (const long long x : v) {
        if (x < floor) {
            return false;
        }
    }
    return true;
}

// A console commit on a blank board writes slot A with the all-erased
// container at sequence 1, byte for byte as nvm_klj3.py writes it, one
// program per page and no erase: the background check found the slot blank.
TEST_P(NvmBoth, first_commit_bytes) {
    Files f;
    const Result r = go(port(), f, {"--blank", "--boot", "--commit", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 1 && r.at("auth") == 0 && r.at("erases") == 0 &&
                r.at("programs") == pages() && r.at("compactions") == 1 && r.at("appends") == 0 &&
                r.at("log_end") == fx().num("log_start"))
        << "first commit: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("erased@1"))) << "the first container differs from nvm_klj3.py's";
    if (port() == Port::Litespi) {
        EXPECT_TRUE(r.at("ls_se") == 0 && r.at("ls_pp") == pages() && r.at("ls_wren") == r.at("ls_pp"))
            << "LiteSPI command sequence: " << r.text();
    }
}

//! The pages of the deltas a slot recipe's log holds.
long long log_pages(const std::string& recipe) {
    return (static_cast<long long>(fx().blob(recipe).size()) - fx().num("log_start")) / 256;
}

// A change to the first record of every group is appended to the
// authoritative slot as one delta at the next sequence, byte for byte as
// nvm_klj3.py writes it behind the base, which is untouched; nothing is
// erased; and a boot from the result applies exactly the changed values (the
// round trip).
TEST_P(NvmBoth, change_commit_bytes) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    std::vector<std::string> words = {"--slot-b", "g.bin", "--boot", "--protect-auth"};
    for (const auto& [rid, payload] : fx().payloads("changed5c_firsts")) {
        words.insert(words.end(), {"--set", set_word(rid, payload)});
    }
    words.insert(words.end(), {"--until-idle", "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"});
    Result r = go(port(), f, words);
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 6 && r.at("auth") == 1 && r.at("stale") == 0 && r.at("dirty") == 0 &&
                r.at("pending") == 0 && r.at("appends") == 1 && r.at("erases") == 0 &&
                r.at("programs") == log_pages("golden@5+changed5c@6") &&
                r.at("log_end") == fx().num("log_start") + 256 * log_pages("golden@5+changed5c@6"))
        << "change commit: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["b.bin"], fx().blob("golden@5+changed5c@6")))
        << "the authoritative slot differs from nvm_klj3.py's base and delta for the same records";
    EXPECT_TRUE(f.blobs["a.bin"] == padded(Bytes{})) << "the other slot was written";
    if (port() == Port::Litespi) {
        EXPECT_TRUE(r.at("ls_se") == 0 && r.at("ls_pp") == log_pages("golden@5+changed5c@6"))
            << "LiteSPI command sequence: " << r.text();
    }
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("auth") == 1 && r.at("seq") == 6 && r.at("deltas") == 1) << "boot after the commit: " << r.text();
    expect_state(f, "st", fx().payloads("changed5c"));
}

// #823 decision 4: a change is appended after the 150 ms first-dirty window
// and not before, and a second change inside the window does not extend it.
void debounce_window(Port port) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const auto [rid, new1] = one_change(1);
    const Bytes new2 = one_change(2).second;
    const std::vector<std::string> one = {"--slot-b", "g.bin", "--boot", "--set", set_word(rid, new1)};
    Result r = go(port, f, concat(one, {"--run-ms", num(kWindowMs - 10)}));
    EXPECT_EQ(r.at("programs"), 0) << "a program inside the first-dirty window: " << r.at("programs");
    r = go(port, f, concat(one, {"--run-ms", num(kWindowMs - 10), "--run-ms", "30"}));
    EXPECT_EQ(r.at("programs"), 1) << "no delta 20 ms after the window: " << r.at("programs");
    r = go(port, f, concat(one, {"--run-ms", num(kWindowMs / 2), "--set", set_word(rid, new2), "--run-ms",
                                 num(kWindowMs / 2 + 20)}));
    EXPECT_EQ(r.at("programs"), 1) << "a second change extended the first-dirty window";
}

// A change the running capture takes leaves no window behind it, so the next
// change gets its own full window: a change to the last record, and one to the
// very record the capture examines next; a change the capture has passed opens
// one of its own.
TEST_P(NvmBoth, debounce) {
    debounce_window(port());
    Files f = fx().files({{"g.bin", "golden@5"}});
    const unsigned rid = rids().back();
    const unsigned first = rids().front();
    // the capture has latched nothing yet: it takes a change to the last
    // record, and one to the first, the record it examines next
    for (const unsigned taken : {rid, first}) {
        const Result r = go(port(), f,
                         {"--slot-b", "g.bin", "--boot", "--set-pattern", "1", "--until-phase", num(NVM_P_CAPTURE),
                          "--set", set_word(taken, value(taken, 1)), "--until-idle", "--run-ms", "5000", "--mark",
                          "--set", set_word(taken, value(taken, 2)), "--until-idle"});
        EXPECT_TRUE(r.at("ok") >= 2 && in(after_mark(r), kWindowMs * kMs, (kWindowMs + 50) * kMs))
            << "a change after a commit that took one mid-capture (record 0x" << std::hex << taken << std::dec
            << "): its program " << after_mark(r) << " us after it, want 150 to 200 ms: " << r.text();
    }
    // the capture is over: a change now waits for a window of its own
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--boot", "--set", set_word(rid, one_change(1).second), "--until-phase",
                      num(NVM_P_SEAL), "--until-phase", num(NVM_P_IDLE), "--mark", "--set",
                      set_word(first, value(first, 9)), "--until-idle"});
    EXPECT_TRUE(r.at("ok") == 2 && in(after_mark(r), kWindowMs * kMs, (kWindowMs + 50) * kMs))
        << "a change after the capture: its program " << after_mark(r) << " us after it, want 150 to 200 ms: "
        << r.text();
}

// #823 decision 6: the open bits carry their count. Two changes to one record
// and one to another open two records; the capture moves both into flight,
// and the verified commit closes them, each count following its bits.
TEST_P(NvmBoth, open_count) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const unsigned a = rids().front();
    const unsigned b = rids().back();
    const std::vector<std::string> marks = {"--slot-b", "g.bin", "--boot", "--set", set_word(a, value(a, 1)),
                                            "--set", set_word(a, value(a, 2)), "--set", set_word(b, value(b, 3))};
    Result r = go(port(), f, marks);
    EXPECT_TRUE(r.at("n_dirty") == 2 && r.at("n_inflight") == 0 && r.at("dirty") == 1 && r.at("pending") == 0)
        << "two records changed, one twice: " << r.text();
    std::vector<std::string> words = marks;
    words.insert(words.end(), {"--until-phase", num(NVM_P_SEAL)});
    r = go(port(), f, words);
    EXPECT_TRUE(r.at("n_dirty") == 0 && r.at("n_inflight") == 2 && r.at("dirty") == 0 && r.at("pending") == 1)
        << "both captured: " << r.text();
    words = marks;
    words.insert(words.end(), {"--until-idle"});
    r = go(port(), f, words);
    EXPECT_TRUE(r.at("ok") == 1 && r.at("n_dirty") == 0 && r.at("n_inflight") == 0 && r.at("dirty") == 0 &&
                r.at("pending") == 0)
        << "committed: " << r.text();
}

// DR2b: a change that leaves every persisted value as the verified slot holds
// it writes nothing.
TEST_P(NvmBoth, unchanged_no_erase) {
    const unsigned rid = rids().back();
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--boot", "--set", set_word(rid, fx().payloads("golden").at(rid)),
                      "--until-idle"});
    EXPECT_TRUE(r.at("erases") == 0 && r.at("programs") == 0 && r.at("skipped") == 1 && r.at("ok") == 0 &&
                r.at("dirty") == 0 && r.at("pending") == 0)
        << "unchanged value: " << r.text();
}

// DR2b only suppresses what a VERIFIED slot holds: after a failed delta, the
// retry, a compaction, writes the value again although the stage already
// carries it, and appends it behind the new base.
TEST_P(NvmBoth, failed_commit_not_skipped) {
    const auto [rid, new3] = one_change(3);
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:1", "--set", set_word(rid, new3),
                      "--until-quiet", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("failed") == 1 && r.at("ok") == 2 && r.at("compactions") == 1 && r.at("appends") == 1 &&
                r.at("last") == NVM_VD_OK && r.at("skipped") == 0 && r.at("auth") == 0 && r.at("seq") == 6)
        << "retry after a failed attempt: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("one3@5+one3@6"))) << "the retried change is not in the slot";
}

// DR2c: a delta whose program or read-back fails names its verdict, keeps
// the change in flight, marks the claim stale and leaves the segment torn;
// the retries, compactions into the other slot, fail too, at most three
// attempts in all, each at least 1,000 ms after the one before, and then the
// set is abandoned and recorded. The authoritative slot's base is untouched. A
// program that never ends leaves the device busy: nothing is read until it
// answers, so the compaction never starts and the one attempt stands.
TEST_P(NvmBoth, media_failures) {
    struct Failure {
        const char* mode;
        long long verdict;
        bool hang;
    };
    static constexpr Failure kFailures[] = {{"program-hang", NVM_VD_PROGRAM, true},
                                            {"program-drop", NVM_VD_VERIFY, false},
                                            {"program-flip", NVM_VD_VERIFY, false}};
    const auto [rid, new4] = one_change(4);
    for (const Failure& fail : kFailures) {
        Files f = fx().files({{"g.bin", "golden@5"}});
        const Result r = go(port(), f,
                         {"--slot-b", "g.bin", "--boot", "--protect-auth", "--fault", std::string(fail.mode) + ":99999",
                          "--set", set_word(rid, new4), "--run-ms", "20000", "--dump-slot-b", "b.bin"});
        const long long attempts = fail.hang ? 1 : 3;
        EXPECT_TRUE(r.at("failed") == attempts && r.at("exhausted") == (fail.hang ? 0 : 1) &&
                    r.at("first") == fail.verdict && r.at("last") == fail.verdict && r.at("stale") == 1 &&
                    r.at("dirty") == 0 && r.at("pending") == 1 && r.at("ok") == 0 && r.at("torn") == 1 &&
                    r.at("abandoned") == (fail.hang ? 0 : 1) && r.at("abandoned_vd") == (fail.hang ? 0 : fail.verdict))
            << fail.mode << ": " << r.text();
        EXPECT_TRUE(prefix_holds(f.blobs["b.bin"], fx().blob("golden@5")))
            << fail.mode << ": the authoritative slot's base changed";
        EXPECT_TRUE(r.fail_at.size() == static_cast<std::size_t>(attempts) && all_at_least(gaps(r.fail_at), 1000000))
            << fail.mode << ": " << r.fail_at.size() << " attempts, want " << attempts << " at least 1,000 ms apart";
    }
}

// The background preparation of the other slot (#823 decisions 3 and 5): a
// written block is erased and read again. An erase that leaves a byte written
// fails the preparation VD_ERASE, which starts again 1,000 ms later, three
// times in all, then gives up until reset; the saves append regardless. An
// erase that never ends holds the device: a save cannot suspend it, so it
// fails VD_ERASE at its deadline, without tearing the log, and nothing is
// written while the device stays busy.
TEST_P(NvmBoth, prep_failures) {
    const auto [rid, new4] = one_change(4);
    Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    Result r = go(port(), f,
               {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--protect-auth", "--fault", "erase-stuck:99999",
                "--set", set_word(rid, new4), "--run-ms", "10000"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("appends") == 1 && r.at("failed") == 0 && r.at("prep_failed") == 3 &&
                r.at("prep_vd") == NVM_VD_ERASE && r.at("bg") == NVM_B_FAILED && r.at("erases") == 3 &&
                r.prep_fail_at.size() == 3u && all_at_least(gaps(r.prep_fail_at), 1000000))
        << "erase-stuck: " << r.text();
    r = go(port(), f,
           {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--protect-auth", "--fault", "erase-hang:1", "--set",
            set_word(rid, new4), "--run-ms", "10000"},
           {"while_busy", "ls_refused"});
    EXPECT_TRUE(r.at("ok") == 0 && r.at("failed") == 1 && r.at("first") == NVM_VD_ERASE && r.at("torn") == 0 &&
                r.at("pending") == 1 && r.at("programs") == 0)
        << "erase-hang: " << r.text();
}

// A third attempt that succeeds clears the stale claim; after exhaustion, a
// changed value is a new work set and commits once the media answers. The
// stale claim heals (FASTCONNECT section 9.2), also when the change left
// after the recovering commit set the value it already had and DR2b writes
// nothing; the record of the abandoned set does not heal.
TEST_P(NvmBoth, recovers_after_failure) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const auto [rid, new5] = one_change(5);
    Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:2", "--set", set_word(rid, new5),
                           "--until-quiet"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("failed") == 2 && r.at("stale") == 0 && r.at("last") == NVM_VD_OK &&
                r.at("first") == NVM_VD_OK && r.at("attempts") == 0 && r.at("compactions") == 1 &&
                r.fail_at.size() == 2u && all_at_least(gaps(r.fail_at), 1000000) && !r.ok_at.empty() &&
                r.ok_at[0] >= r.fail_at[1] + 1000000)
        << "third attempt: " << r.text();
    // the delta fails; the retry's compaction and its delta write the value,
    // and the same value is set again while that delta is written, so it is
    // left dirty and DR2b writes nothing for it, and the claim heals
    r = go(port(), f,
           {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:1", "--set", set_word(rid, new5), "--until-programs",
            num(pages() + 2), "--set", set_word(rid, new5), "--until-quiet"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("failed") == 1 && r.at("skipped") == 1 && r.at("stale") == 0 &&
                r.at("dirty") == 0 && r.at("pending") == 0)
        << "a repeated value after recovery: " << r.text();
    r = go(port(), f,
           {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:99999", "--set", set_word(rid, new5), "--run-ms",
            "15000", "--fault", "none:0", "--set", set_word(rid, one_change(6).second), "--until-quiet",
            "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("failed") == 3 && r.at("exhausted") == 0 && r.at("stale") == 0 &&
                r.at("abandoned") == 1 && r.at("abandoned_vd") == NVM_VD_VERIFY)
        << "new work set after exhaustion: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("one6@5+one6@6"))) << "the new work set is not in the slot";
}

// DR2c: an unchanged captured work set gets three attempts in all. A change
// call that leaves the value as it was, made every 5 s for 60 s, buys no
// fourth, and neither does the medium healing; a value that really changes is
// a new set, commits, and leaves the abandoned set's record.
TEST_P(NvmBoth, dr2c_unchanged_set) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const auto [rid, new21] = one_change(21);
    std::vector<std::string> words = {"--slot-b",           "g.bin", "--boot", "--protect-auth", "--fault",
                                      "program-drop:99999", "--set", set_word(rid, new21), "--run-ms", "5000"};
    for (int k = 0; k < 12; ++k) {
        words.insert(words.end(), {"--touch", num(rid), "--run-ms", "5000"});
    }
    words.insert(words.end(), {"--fault", "none:0", "--touch", num(rid), "--run-ms", "3000"});
    Result r = go(port(), f, words);
    EXPECT_TRUE(r.at("failed") == 3 && r.at("ok") == 0 && r.at("exhausted") == 1 && r.at("withheld") == 13 &&
                r.at("abandoned") == 1)
        << "unchanged set held: " << r.text();
    r = go(port(), f,
           {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:99999", "--set", set_word(rid, new21), "--run-ms",
            "5000", "--fault", "none:0", "--set", set_word(rid, value(rid, 22)), "--until-quiet", "--dump-slot-a",
            "a.bin"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("failed") == 3 && r.at("stale") == 0 && r.at("abandoned") == 1 &&
                r.at("abandoned_vd") == NVM_VD_VERIFY)
        << "a changed set after exhaustion: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("one22@5+one22@6"))) << "the changed set is not in the slot";
}

// DR2c binds the console too: a commit asked for inside a failed attempt's
// backoff is refused and the retry still waits 1,000 ms; asked for after the
// set is exhausted, it writes nothing while the set is unchanged, and a
// changed set commits.
TEST_P(NvmBoth, dr2c_console) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const auto [rid, new23] = one_change(23);
    Result r = go(port(), f,
               {"--slot-b", "g.bin", "--boot", "--fault", "program-drop:1", "--set", set_word(rid, new23),
                "--until-phase", num(NVM_P_PROGRAM_WAIT), "--run-ms", "200", "--commit-try", "--run-ms", "300",
                "--commit-try", "--until-quiet"});
    const long long gap = r.fail_at.empty() ? -1 : first_after(r.prog_at, r.fail_at[0]);
    EXPECT_TRUE(r.at("commit_tries") == 2 && r.at("commit_refused") == 2 && r.at("failed") == 1 && r.at("ok") == 2 &&
                in(gap, 1000 * kMs, 1050 * kMs))
        << "console inside the backoff: retry " << gap << " us after the failure: " << r.text();
    std::vector<std::string> words = {"--slot-b",           "g.bin", "--boot", "--protect-auth", "--fault",
                                      "program-drop:99999", "--set", set_word(rid, new23), "--run-ms", "5000"};
    for (int k = 0; k < 5; ++k) {
        words.insert(words.end(), {"--commit-try", "--run-ms", "1500"});
    }
    words.insert(words.end(), {"--fault", "none:0", "--commit-try", "--run-ms", "1500", "--set",
                               set_word(rid, value(rid, 24)), "--commit-try", "--until-quiet"});
    r = go(port(), f, words);
    EXPECT_TRUE(r.at("commit_tries") == 7 && r.at("commit_refused") == 0 && r.at("withheld") == 6 &&
                r.at("failed") == 3 && r.at("ok") == 2 && r.at("abandoned") == 1)
        << "console after exhaustion: " << r.text();
}

// With `fault` armed after boot, the first attempt fails with `verdict` and
// nothing commits before the backoff ends; run on, the retry compacts into the
// other slot, the change appended behind its base, and the authoritative slot
// was never touched.
void fails_then_recovers(Port port, const std::string& fault, long long verdict, unsigned seed,
                         const std::vector<std::string>& set = {}) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const auto [rid, change] = one_change(seed);
    std::vector<std::string> head = {"--slot-b", "g.bin", "--boot", "--protect-auth", "--fault", fault};
    head.insert(head.end(), set.begin(), set.end());
    if (set.empty()) {
        head.insert(head.end(), {"--set", set_word(rid, change)});
    }
    Result r = go(port, f, concat(head, {"--run-ms", "1000"}));
    EXPECT_TRUE(r.at("failed") == 1 && r.at("first") == verdict && r.at("ok") == 0)
        << fault << ": want the first failure " << verdict << ": " << r.text();
    r = go(port, f, concat(head, {"--until-quiet", "--dump-slot-a", "a.bin"}));
    EXPECT_TRUE(r.at("failed") == 1 && r.at("ok") == 2 && r.at("auth") == 0 && r.at("seq") == 6)
        << fault << ": no recovery: " << r.text();
    const std::string want = set.empty() ? "one" + num(seed) + "@5+one" + num(seed) + "@6" : "changed5c@5+changed5c@6";
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob(want))) << fault << ": the retried change is not in the slot";
}

//! The words that set the first record of every group as changed5c does.
std::vector<std::string> firsts() {
    std::vector<std::string> out;
    for (const auto& [rid, payload] : fx().payloads("changed5c_firsts")) {
        out.insert(out.end(), {"--set", set_word(rid, payload)});
    }
    return out;
}

// The read-back covers the whole delta to its trailer: a dropped LAST page
// fails the attempt VD_VERIFY, the authority stays, and the retry commits.
TEST_P(NvmBoth, verify_tail) {
    fails_then_recovers(port(), "program-drop:1:" + num(log_pages("golden@5+changed5c@6") - 1), NVM_VD_VERIFY, 25,
                        firsts());
}

// The background check covers the other slot to its last byte: a written
// last byte erases the last block, and an erase that leaves that byte written
// fails the preparation VD_ERASE, before any page is programmed there; the
// next preparation erases it again and finds the slot blank.
TEST_P(NvmBoth, blankcheck_tail) {
    Files f = fx().files({{"g.bin", "golden@5"}, {"t.bin", "tail_written"}});
    const Result r = go(port(), f,
                     {"--slot-a", "t.bin", "--slot-b", "g.bin", "--boot", "--fault",
                      "erase-stuck:1:0:" + num(fx().num("erase_block") - 1), "--until-quiet"});
    const long long last_block = fx().num("journal_a") + fx().num("slot_bytes") - fx().num("erase_block");
    EXPECT_TRUE(r.at("prep_failed") == 1 && r.at("prep_vd") == NVM_VD_ERASE && r.at("bg") == NVM_B_READY &&
                r.at("erases") == 2 && r.erase_at.size() == 2u && r.erase_at[0] == last_block &&
                r.erase_at[1] == last_block && r.at("programs") == 0)
        << "the slot's last byte: " << r.text();
}

// Each failure is named by the step that met it, not a later one: a read
// that fails in the background check is the preparation's VD_ERASE and in a
// delta's read-back VD_VERIFY, never passed over; a program or erase the port
// refuses is VD_PROGRAM or the preparation's VD_ERASE. Each save is retried
// and commits; each preparation starts again and completes.
TEST_F(NvmModel, media_verdicts) {
    const long long a = fx().num("journal_a");
    const long long b = fx().num("journal_b");
    fails_then_recovers(port(), "read-fail-at:1:0:" + num(b + fx().num("log_start") + 8), NVM_VD_VERIFY, 27);
    fails_then_recovers(port(), "program-refuse:1", NVM_VD_PROGRAM, 27);
    const std::pair<std::string, bool> prep[] = {{"read-fail-at:1:0:" + num(a + 300), false},
                                                 {"erase-refuse:1", true}};
    for (const auto& [fault, written] : prep) {
        Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
        std::vector<std::string> words = {"--slot-b", "g.bin"};
        if (written) {
            words.insert(words.end(), {"--slot-a", "o.bin"});
        }
        const Result r = go(port(), f, concat(words, {"--boot", "--fault", fault, "--until-quiet"}));
        EXPECT_TRUE(r.at("prep_failed") == 1 && r.at("prep_vd") == NVM_VD_ERASE && r.at("bg") == NVM_B_READY &&
                    r.at("failed") == 0)
            << fault << ": " << r.text();
    }
}

// One PHC step of `step` ms inside the first-dirty window, the backoff, an
// erase and a program: no elapsed time moves.
void time_base_step(const std::string& step) {
    const std::vector<std::string> hang = {"while_busy", "ls_refused"};
    const auto [rid, new28] = one_change(28);
    Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    const std::vector<std::string> change = {"--slot-b", "g.bin", "--boot", "--set", set_word(rid, new28)};
    Result r = go(Port::Litespi, f,
               {"--slot-b", "g.bin", "--boot", "--mark", "--set", set_word(rid, new28), "--run-ms", "100",
                "--phc-step", step, "--run-ms", "1000"});
    EXPECT_TRUE(in(after_mark(r), kWindowMs * kMs, (kWindowMs + 50) * kMs))
        << "PHC " << step << " ms in the window: program " << after_mark(r) << " us after the change";
    r = go(Port::Litespi, f,
           concat(change, {"--fault", "program-drop:1", "--run-ms", "400", "--phc-step", step, "--run-ms", "2000"}));
    const long long gap = r.fail_at.empty() ? -1 : first_after(r.prog_at, r.fail_at[0]);
    EXPECT_TRUE(in(gap, 1000 * kMs, 1050 * kMs))
        << "PHC " << step << " ms in the backoff: retry " << gap << " us after the failure";
    r = go(Port::Litespi, f,
           {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--fault", "erase-hang:1", "--run-ms", "1500",
            "--phc-step", step, "--run-ms", "5000"},
           hang);
    const long long erase_took = !r.prep_fail_at.empty() && !r.erases.empty()
                                     ? static_cast<long long>(r.prep_fail_at[0]) - static_cast<long long>(r.erases[0])
                                     : -1;
    EXPECT_TRUE(in(erase_took, 3500 * kMs, 3510 * kMs))
        << "PHC " << step << " ms in an erase: timed out " << erase_took << " us after it, want 3,500 ms";
    r = go(Port::Litespi, f,
           concat(change, {"--fault", "program-hang:1", "--until-phase", num(NVM_P_PROGRAM_WAIT), "--mark", "--run-ms",
                           "20", "--phc-step", step, "--run-ms", "200"}),
           hang);
    const long long program_took = !r.fail_at.empty() && !r.marks.empty()
                                       ? static_cast<long long>(r.fail_at[0]) - static_cast<long long>(r.marks[0])
                                       : -1;
    EXPECT_TRUE(in(program_took, 49 * kMs, 51 * kMs))
        << "PHC " << step << " ms in a program: timed out " << program_took << " us after it, want 50 ms";
}

// The windows and deadlines run on the port's local counter, never the PHC:
// a gPTP step of 60 s either way in the first-dirty window, the backoff, an
// erase and a program changes no elapsed time, and the counter's wrap at the
// shape's own clock (2^32 clocks: 42.9 s at 100 MHz, 51.5 s at 83.333 MHz)
// inside the window does not either. Every time is graded on the model's own
// clock, which no step moves.
TEST_F(NvmLitespi, time_base) {
    time_base_step("-60000");
    time_base_step("60000");
    // model time starts at the boot's power on, and so does the counter
    const long long wrap_us = static_cast<long long>((1ull << 32) * 1000000ull / CONFIG_CLOCK_FREQUENCY);
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--boot", "--run-ms", num(wrap_us / kMs - kWindowMs / 2), "--mark", "--set",
                      set_word(rids().back(), one_change(28).second), "--run-ms", "1500"});
    EXPECT_TRUE(!r.marks.empty() && static_cast<long long>(r.marks[0]) < wrap_us &&
                wrap_us < static_cast<long long>(r.marks[0]) + kWindowMs * kMs)
        << "the window does not hold the counter's wrap at " << wrap_us << " us";
    EXPECT_TRUE(in(after_mark(r), kWindowMs * kMs, (kWindowMs + 50) * kMs))
        << "a window across the counter's wrap: program " << after_mark(r) << " us after the change";
}

// The port keeps time at the shape's own system clock, a whole number of MHz
// or not. The suite is built at the config's sys_clk_hz (83,333,000 Hz at the
// three Arty shapes). The per-call deadline is LS_CALL_US of that clock in
// timer0 clocks, exactly: 166,666 at 83.333 MHz, 200,000 at 100 MHz. Over
// 120 s of service, two counter wraps or more, the port's elapsed time equals
// the model's to 2 us.
TEST_F(NvmLitespi, port_clock) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--clock", "--run-ms", "120000", "--clock"});
    const long long clock_hz = fx().num("clock_hz");
    const long long ticks = kLsCallUs * clock_hz / 1000000;
    EXPECT_TRUE(r.at("clock_hz") == clock_hz && r.at("ls_call_ticks") == ticks)
        << "built at " << r.at("clock_hz") << " Hz with a deadline of " << r.at("ls_call_ticks")
        << " clocks; the config's " << clock_hz << " Hz makes it " << ticks;
    ASSERT_EQ(r.clocks.size(), 2u) << "clock readings: " << r.clocks.size();
    const long long port_us = static_cast<long long>(r.clocks[1].first - r.clocks[0].first);
    const long long model_us = static_cast<long long>(r.clocks[1].second - r.clocks[0].second);
    EXPECT_LE(std::llabs(port_us - model_us), 2)
        << "over " << model_us << " us of model time the port counted " << port_us << " us";
}

// Every wait on the command master is bounded: two waits of one page program
// slowed by 4,000 status reads each (TX, RX or a drain) still complete; a
// master that stops answering in one wait (TX, RX, or a receive side that
// never drains) fails the call within LS_POLL_MAX reads, chip select
// released, so the step returns, the attempt fails under the step's verdict,
// the authority is untouched and the retry commits; in the background
// preparation's erase, its start or its wait, the preparation fails VD_ERASE
// and starts again; a master that never answers exhausts the set while the
// loop keeps running. The case that slows every wait is port_deadline's.
TEST_F(NvmLitespi, port_stall) {
    const std::vector<std::string> cut = {"ls_short", "while_busy", "ls_refused"};
    Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    const std::vector<std::string> head = {"--slot-b", "g.bin", "--boot", "--protect-auth", "--set",
                                           set_word(rids().back(), one_change(29).second)};
    for (const char* stall : {"tx:2:0:4000", "rx:2:0:4000", "drain:2:0:4000"}) {
        const Result r = go(port(), f, concat(head, {"--until-phase", num(NVM_P_PROGRAM), "--ls-stall", stall,
                                                  "--until-idle"}));
        EXPECT_TRUE(r.at("failed") == 0 && r.at("ok") == 1 && r.at("ls_stalled") == 2 && r.at("ls_max_withheld") == 4000)
            << "slow master " << stall << ": " << r.text();
    }
    for (const char* stall : {"tx:1:10:0", "rx:1:100:0", "drain:1:0:0"}) {
        Result r = go(port(), f,
                   concat(head, {"--until-phase", num(NVM_P_PROGRAM), "--ls-stall", stall, "--run-ms", "100",
                                 "--dump-slot-b", "b.bin"}),
                   cut);
        // the port gives up after LS_POLL_MAX reads; a drain reads once more
        const long long withheld = kPollMax + (std::string(stall).rfind("drain", 0) == 0 ? 1 : 0);
        EXPECT_TRUE(r.at("failed") == 1 && r.at("first") == NVM_VD_PROGRAM && r.at("ls_stalled") == 1 &&
                    r.at("ls_max_withheld") == withheld)
            << "stalled master " << stall << ": " << r.text();
        EXPECT_TRUE(prefix_holds(f.blobs["b.bin"], fx().blob("golden@5"))) << stall << ": the authoritative base changed";
        r = go(port(), f, concat(head, {"--until-phase", num(NVM_P_PROGRAM), "--ls-stall", stall, "--until-quiet"}),
               cut);
        EXPECT_TRUE(r.at("failed") == 1 && r.at("ok") == 2) << stall << ": no recovery: " << r.text();
    }
    const std::pair<std::string, std::vector<std::string>> prep[] = {
        {"tx:1:0:0", {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--ls-stall", "tx:1:0:0"}},
        {"tx:1:1:0", {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--ls-stall", "tx:1:1:0"}},
        {"rx:1:0:0", {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--until-bg", num(NVM_B_ERASE_WAIT),
                      "--ls-stall", "rx:1:0:0"}}};
    for (const auto& [stall, words] : prep) {
        const Result r = go(port(), f, concat(words, {"--until-quiet"}), cut);
        EXPECT_TRUE(r.at("prep_failed") == 1 && r.at("prep_vd") == NVM_VD_ERASE && r.at("ls_stalled") == 1 &&
                    r.at("bg") == NVM_B_READY)
            << "stalled master in the preparation's erase, " << stall << ": " << r.text();
    }
    const Result r = go(port(), f,
                     concat(head, {"--until-phase", num(NVM_P_PROGRAM), "--ls-stall", "tx:99999:0:0", "--run-ms",
                                   "10000", "--dump-slot-b", "b.bin"}),
                     cut);
    EXPECT_TRUE(r.at("failed") == 3 && r.at("exhausted") == 1 && r.at("first") == NVM_VD_PROGRAM &&
                r.at("calls") >= 90000 && r.at("max_call_us") <= kCallBoundUs)
        << "dead master: " << r.text();
    EXPECT_TRUE(prefix_holds(f.blobs["b.bin"], fx().blob("golden@5"))) << "dead master: the authoritative base changed";
}

// No call is still waiting on the master past the port's deadline, LS_CALL_US
// of timer0 time, even when the master keeps progressing inside every wait.
// Ten waits slowed by 4,000 status reads each (1.6 ms in one page program)
// and the call completes. Twelve, the slow part ending just before the
// deadline, and the call completes past it at the ready pace, within
// CALL_BOUND_US. Every wait slowed by 4,000 reads, none of them reaching
// LS_POLL_MAX, and each page program fails at the deadline: the attempt fails
// VD_PROGRAM, the authority is untouched, three attempts are spent and the
// loop keeps running; once the master is well, a changed value commits. Every
// call stays within CALL_BOUND_US of model time.
TEST_F(NvmLitespi, port_deadline) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const unsigned rid = rids().back();
    const std::vector<std::string> head = {"--slot-b", "g.bin", "--boot",        "--protect-auth",
                                           "--set",    set_word(rid, one_change(30).second), "--until-phase",
                                           num(NVM_P_PROGRAM)};
    Result r = go(port(), f, concat(head, {"--ls-stall", "tx:10:0:4000", "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 0 && r.at("ls_stalled") == 10 && 1600 <= r.at("max_call_us") &&
                r.at("max_call_us") < kLsCallUs)
        << "ten slowed waits: " << r.text();
    r = go(port(), f, concat(head, {"--ls-stall", "tx:12:0:4000", "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 0 && r.at("ls_stalled") == 12 && kLsCallUs < r.at("max_call_us") &&
                r.at("max_call_us") <= kCallBoundUs)
        << "twelve slowed waits: " << r.text();
    r = go(port(), f,
           concat(head, {"--ls-stall", "tx:999999:0:4000", "--run-ms", "10000", "--dump-slot-b", "b.bin", "--ls-stall",
                         "none:0", "--set", set_word(rid, value(rid, 31)), "--until-quiet"}),
           {"ls_short"});
    EXPECT_TRUE(r.at("failed") == 3 && r.at("abandoned_vd") == NVM_VD_PROGRAM && r.at("abandoned") == 1 &&
                r.at("ok") == 2 && r.at("ls_max_withheld") == 4000 && kLsCallUs <= r.at("max_call_us") &&
                r.at("max_call_us") <= kCallBoundUs && r.at("calls") >= 50000)
        << "every wait slowed: " << r.text();
    EXPECT_TRUE(prefix_holds(f.blobs["b.bin"], fx().blob("golden@5"))) << "every wait slowed: the authority changed";
}

//! Sequences the generation restart meets differently: a tie with 1, an
//! ordinary one, the half-range point and the wrap.
constexpr std::array<unsigned long long, 4> kAuthSeqs{1, 5, 0x80000000, 0xFFFFFFFF};

std::string hex(unsigned long long v) {
    char buf[24];
    std::snprintf(buf, sizeof buf, "%llx", v);
    return buf;
}

// Slot x valid at seq, the other blank, the case's fault armed at boot (held:
// whether it must hold the writer); a change; then a clean reboot, a change,
// its commit and a clean reboot. The faulted boot's run.
Result authority_case(int x, unsigned long long seq, const std::string& fault, bool held) {
    const std::string set = "changed6" + num(x);
    const Payloads& saved = fx().payloads(set);
    const auto [rid, new32] = one_change(32);
    const Bytes new33 = one_change(33).second;
    const std::string what = std::string("slot ") + "AB"[x] + " at 0x" + hex(seq) + ", " + fault;
    Files f = fx().files({{"x.bin", set + "@" + hex(seq)}});
    std::vector<std::string> words = {x == 0 ? "--slot-a" : "--slot-b", "x.bin", "--boot-fault", fault, "--boot",
                                      "--dump-state", "st0", "--set", set_word(rid, new32), "--until-idle"};
    if (held) {
        words.insert(words.end(), {"--run-ms", "3000", "--commit-try"});
    }
    words.insert(words.end(), {"--dump-slot-a", "a1.bin", "--dump-slot-b", "b1.bin"});
    const Result s = go(Port::Model, f, words);
    if (held) {
        EXPECT_TRUE(s.at("unread") == (1 << x) && s.at("phase") == NVM_P_HELD && s.at("terminal") == NVM_T_BLANK &&
                    s.at(x == 0 ? "vd_a" : "vd_b") == NVM_VD_LEN && s.at("ok") == 0 && s.at("erases") == 0 &&
                    s.at("programs") == 0 && s.at("dirty") == 1 && s.at("commit_refused") == 1)
            << what << ": the writer is not held: " << s.text();
    } else {
        EXPECT_TRUE(s.at("unread") == 0 && s.at("terminal") == NVM_T_COMPLETE && s.at("ok") == 1 &&
                    s.at("auth") == x && static_cast<unsigned long long>(s.at("seq")) == ((seq + 1u) & 0xFFFFFFFFu))
            << what << ": the slot was not read again and applied: " << s.text();
    }
    expect_state(f, "st0", held ? Payloads{} : saved, what + ": at boot: ");
    // whatever the store reported committed, a clean reboot restores
    const Payloads durable = s.at("ok") != 0 ? with(saved, {{rid, new32}}) : saved;
    const unsigned long long want_seq = (seq + (s.at("ok") != 0 ? 1u : 0u)) & 0xFFFFFFFFu;
    Result r = go(Port::Model, f,
               {"--slot-a", "a1.bin", "--slot-b", "b1.bin", "--boot", "--dump-state", "st1", "--set",
                set_word(rid, new33), "--until-idle", "--dump-slot-a", "a2.bin", "--dump-slot-b", "b2.bin"});
    EXPECT_TRUE(static_cast<unsigned long long>(r.at("seq")) == ((want_seq + 1u) & 0xFFFFFFFFu) && r.at("ok") == 1 &&
                r.at("unread") == 0)
        << what << ": the change after a clean reboot: " << r.text();
    expect_state(f, "st1", durable, what + ": clean reboot: ");
    r = go(Port::Model, f, {"--slot-a", "a2.bin", "--slot-b", "b2.bin", "--boot", "--dump-state", "st2"});
    EXPECT_TRUE(static_cast<unsigned long long>(r.at("seq")) == ((want_seq + 1u) & 0xFFFFFFFFu) &&
                r.at("terminal") == NVM_T_COMPLETE)
        << what << ": the reboot after that commit: " << r.text();
    expect_state(f, "st2", with(durable, {{rid, new33}}), what + ": last reboot: ");
    return s;
}

// #665 decision 2: a slot refused by a media read fault leaves the authority
// unknown, so nothing is committed until reset. One slot valid and the other
// blank, both ways round, at sequence 1, 5, 0x80000000 and 0xFFFFFFFF. The
// valid slot's reads failing NVM_READ_TRIES times: the boot is BLANK, the
// writer HELD, a change is reported dirty, nothing is erased or written and
// the console is refused; a clean reboot restores the slot. Two failed reads,
// one read flipping a bit unreported, or one read answering from the blank
// slot (so the valid one reads blank): the slot is read again and applied,
// and the change commits at the next sequence. Either way a later change
// commits and a clean reboot restores it with every other value, and nothing
// reported committed is lost on a clean reboot.
TEST_F(NvmModel, authority_unknown) {
    for (const int x : {0, 1}) {
        // a blank slot stands on two header reads, a valid one on its header
        // and its container; slot A is judged first
        const std::string first = x == 0 ? "0" : "2";
        const std::string body = "0x" + hex((x == 0 ? NVM_SLOT_A : NVM_SLOT_B) + 0x100u);
        for (const unsigned long long seq : kAuthSeqs) {
            const std::pair<std::string, bool> cases[] = {{"read-fail:" + num(kReadTries) + ":" + first, true},
                                                           {"read-fail:" + num(kReadTries - 1) + ":" + first, false},
                                                           {"read-flip-at:1:0:" + body, false},
                                                           {"read-alias:1:" + first, false}};
            for (const auto& [fault, held] : cases) {
                static_cast<void>(authority_case(x, seq, fault, held));
            }
        }
    }
}

// Two reads stand a refusal only when they return the same bytes, never on
// equal verdicts alone (#665 issue comment 5999350068; R501-3's probe, kept as
// a check). One slot valid and the other blank, both ways round, at sequence
// 1, 5, 0x80000000 and 0xFFFFFFFF. The valid slot's first header byte, or its
// byte at offset 0x100 in the body, reads XOR 8 and then XOR 16, so two reads
// refuse it alike on different bytes. It then reads clean, and that read is
// applied, with one media fault counted. Read wrong a third way too (XOR 32),
// no two reads agree: the slot is UNREAD and the writer HELD. Every case goes
// on through a clean reboot, a change, its commit and a clean reboot, and
// nothing reported committed is lost.
TEST_F(NvmModel, read_disagreement) {
    for (const int x : {0, 1}) {
        for (const unsigned long long seq : kAuthSeqs) {
            for (const unsigned where : {0u, 0x100u}) {
                const std::string at = "0x" + hex((x == 0 ? NVM_SLOT_A : NVM_SLOT_B) + where);
                for (const auto& [count, held] : {std::pair<int, bool>{2, false}, std::pair<int, bool>{3, true}}) {
                    const Result s = authority_case(x, seq, "read-vary-at:" + num(count) + ":0:" + at, held);
                    EXPECT_EQ(s.at("read_faults"), count - 1)
                        << "slot " << "AB"[x] << " at 0x" << hex(seq) << ", " << count << " reads wrong at " << at
                        << ": " << s.at("read_faults") << " media faults counted, want " << count - 1;
                }
            }
        }
    }
}

// DR5: with no slot accepted, a blank slot takes the first base before a
// refused one, so a refused image is not erased merely for being refused; it
// is erased in the background once a base elsewhere holds the authority
// (#823 decision 3, rule 6).
TEST_P(NvmBoth, refused_slot_kept) {
    const auto [rid, new7] = one_change(7);
    Files f = fx().files({{"f.bin", "golden@5/foreign"}});
    Result r = go(port(), f,
               {"--slot-a", "f.bin", "--boot", "--set", set_word(rid, new7), "--until-ok", "1", "--dump-slot-a",
                "a.bin", "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_BLANK && r.at("vd_a") == NVM_VD_SHAPE && r.at("auth") == 1 && r.at("ok") == 1 &&
                r.at("erases") == 0)
        << "refused slot A: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("golden@5/foreign"))) << "the refused image was erased";
    EXPECT_TRUE(slot_holds(f.blobs["b.bin"], fx().blob("erased_one7@1")))
        << "slot B is not the container nvm_klj3.py assembles for the change";
    r = go(port(), f, {"--slot-a", "f.bin", "--boot", "--set", set_word(rid, new7), "--until-quiet", "--dump-slot-a",
                       "a.bin"});
    EXPECT_TRUE(r.at("auth") == 1 && r.at("erases") == 1 && f.blobs["a.bin"] == padded(Bytes{}))
        << "the refused image is not erased once slot B holds the authority: " << r.text();
}

// Every service step is bounded and returns: no step touches more than one
// latched record or one 256-byte stretch, no call holds the loop past
// NOMINAL_CALL_US of model time, and the loop keeps running through a 3 s
// background erase (one status poll per call), which every delta suspends.
TEST_P(NvmBoth, service_bound) {
    Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    const Result r = go(port(), f, {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--times", "3000:1000",
                                 "--set-pattern", "1", "--until-quiet"});
    // one latched record: its copy, and its crc16 over the reference's header
    // less the crc16's own two bytes, then the payload
    const long long want = std::max<long long>(NVM_STEP_BYTES, 2 * fx().num("max_plen") + fx().num("rec_hdr") - 2);
    EXPECT_TRUE(r.at("ok") >= 1 && r.at("step_max") == want && want == r.at("step_bound"))
        << "step bytes " << r.at("step_max") << ", want " << want << " (bound " << r.at("step_bound") << ")";
    EXPECT_TRUE(r.at("max_call_us") <= kNominalCallUs && r.at("calls") >= 3000000 / (100 + r.at("max_call_us")) &&
                r.at("max_polls_call") <= 3 &&
                r.at("suspends") >= 1 && r.at("bg") == NVM_B_READY)
        << "the loop did not keep running: " << r.text();
}

// A power cut inside every media effect of a save (a base's pages on blank
// media, a delta's pages behind one slot, and behind two the background
// erase of the older one first, at 0, 1/256, 1/2 and 255/256 of each) and
// during the last read-back: the board boots the old values or the new ones
// exactly, never a mix, never touching the authoritative slot's closed
// bytes, and the next change commits, a torn log by a compaction first.
TEST_P(NvmBoth, powercut) {
    const long long delta = log_pages("golden@5+changed33@6");
    const std::tuple<const char*, std::vector<std::string>, long long> starts[] = {
        {"blank media", {"--blank"}, pages()},
        {"one slot", {"--slot-a", "o.bin"}, delta},
        {"two slots", {"--slot-a", "o.bin", "--slot-b", "n.bin"}, 1 + delta}};
    for (const auto& [label, loads, effects] : starts) {
        Files f = fx().files({{"o.bin", "golden@5"}, {"n.bin", "changed21@6"}});
        const Result r = go(port(), f, concat(loads, {"--powercut"}));
        const auto pc = [&r](const char* key) { return r.powercut.count(key) != 0u ? r.powercut.at(key) : -1; };
        const long long cases = 4 * effects + 1;
        EXPECT_TRUE(pc("effects") == effects && pc("cases") == cases && pc("bad") == 0 && 1 <= pc("new") &&
                    pc("new") <= 2 && pc("old") + pc("new") == cases)
            << "power cut from " << label << ": effects " << pc("effects") << ", cases " << pc("cases") << ", old "
            << pc("old") << ", new " << pc("new") << ", bad " << pc("bad");
    }
}

// The LiteSPI port refuses to program or erase outside the journal, today's
// KLJ2 journal above it included.
TEST_F(NvmLitespi, port_guard) {
    Files f;
    const Result r = go(port(), f, {"--port-guard"});
    EXPECT_EQ(r.guard, 0) << "the port took " << r.guard << " of 6 writes outside the journal";
}

}  // namespace
}  // namespace nvm_test
