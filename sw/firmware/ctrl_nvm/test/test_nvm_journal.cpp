// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_journal.cpp - the split placement's append-only journal (#823
// decisions 3, 4, 5 and 7; docs/design/SAVED_STATE_FORMAT_32X32.md section 4
// and its test plan T7 to T13; GoogleTest): the boot's replay of a slot's
// log, the torn segment and the compaction it forces, the compaction itself
// with a save landing in it and a power cut at every page of it, the
// background erase of the other slot and its suspend, the reserve and the
// full log, and the append's deadline. The save bound at the 32x32 bound
// shape is test_nvm_bound.cpp.
//
// Every slot loaded or compared is scripts/nvm_klj3.py's (klj3_delta,
// klj3_slot) through the fixture, and every restored state is what its
// klj3_slot_decode leaves.

#include <gtest/gtest.h>

#include <algorithm>
#include <string>
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

//! The last record, and the first, each with a new payload.
unsigned last_id() { return rids().back(); }
unsigned first_id() { return rids().front(); }

// T7: a slot's log is replayed in order behind its base: the last closing
// delta that holds a record gives its value, and the slot's sequence is that
// delta's.
TEST_P(NvmBoth, append_order) {
    Files f = fx().files({{"s.bin", "golden@5+one3@6+one6@7"}});
    const Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("auth") == 1 && r.at("seq") == 7 && r.at("deltas") == 2 &&
                r.at("torn") == 0 && r.at("log_end") == fx().num("log_start") + 512)
        << "two deltas: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6+one6@7"), "two deltas: ");
    Files g = fx().files({{"s.bin", "golden@5+one3@6+first9@7"}});
    const Result q = go(port(), g, {"--slot-b", "s.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(q.at("seq") == 7 && q.at("deltas") == 2) << "deltas of two records: " << q.text();
    expect_state(g, "st", fx().payloads("golden@5+one3@6+first9@7"), "deltas of two records: ");
}

// T8: a delta that does not close is torn: the walk stops before it, so the
// slot is its base and the deltas before. Here only its CRC-32 refuses it, a
// pad byte flipped. Rule 3: the next write is then a compaction, and nothing
// appends behind the torn segment.
TEST_P(NvmBoth, torn_delta) {
    Files f = fx().files({{"s.bin", "torn_pad"}});
    Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("seq") == 6 && r.at("deltas") == 1 && r.at("torn") == 1 &&
                r.at("log_end") == fx().num("log_start") + 256)
        << "a torn delta: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6"), "a torn delta: ");
    r = go(port(), f,
           {"--slot-b", "s.bin", "--boot", "--protect-auth", "--set", set_word(first_id(), value(first_id(), 9)),
            "--until-quiet", "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("appends") == 1 && r.at("auth") == 0 && r.at("seq") == 7 &&
                r.at("torn") == 0 && r.at("failed") == 0)
        << "the write after a torn boot: " << r.text();
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("auth") == 0 && r.at("seq") == 7) << "the boot after it: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6+first9@7"), "the boot after it: ");
}

// A delta whose sequence is not above the one before it is stale: torn.
TEST_P(NvmBoth, stale_delta) {
    Files f = fx().files({{"s.bin", "golden@5+one3@5"}});
    const Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("seq") == 5 && r.at("deltas") == 0 && r.at("torn") == 1) << "a stale delta: " << r.text();
    expect_state(f, "st", fx().payloads("golden"), "a stale delta: ");
}

// Every rule of a delta, each broken alone, its CRC-32 resealed: the delta is
// torn, and the slot is its base and the deltas before it, as
// klj3_slot_decode reads the same bytes.
TEST_P(NvmBoth, delta_refusals) {
    const std::vector<long long>& before = fx().list("delta_case_deltas");
    for (std::size_t n = 0; n < before.size(); ++n) {
        const std::string label = fx().text("delta_case_label/" + num(static_cast<long long>(n)));
        Files f = fx().files({{"s.bin", "delta_case/" + num(static_cast<long long>(n))}});
        const Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--dump-state", "st"});
        EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("auth") == 1 && r.at("torn") == 1 &&
                    r.at("deltas") == before[n] && r.at("seq") == 5 + before[n] &&
                    r.at("log_end") == fx().num("log_start") + 256 * before[n])
            << label << ": " << r.text();
        if (before[n] == 0) {
            expect_state(f, "st", fx().payloads("golden"), label + ": ");
        }
    }
    // IMG_LEN past the slot's room, its records and trailer closing in the
    // bytes the other slot starts with: the delta is refused all the same
    Files f = fx().files({{"a.bin", "delta_spill/a"}, {"b.bin", "delta_spill/b"}});
    const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("auth") == 0 && r.at("torn") == 1 &&
                r.at("deltas") == fx().num("delta_spill_deltas"))
        << "IMG_LEN past the slot's room, closing in the other slot: " << r.text();
}

// A read the port fails in a walk of the log, at a delta's header, a record's
// header, its payload or the trailer, is a media fault: that walk is
// discarded and the two after it stand. A read that fails in the chosen
// slot's replay is read again.
TEST_F(NvmModel, replay_read_faults) {
    const long long b = fx().num("journal_b") + fx().num("log_start");
    for (const long long at : {b, b + 44, b + 55, b + 116}) {
        Files f = fx().files({{"s.bin", "golden@5+one3@6"}});
        Result r = go(port(), f, {"--slot-b", "s.bin", "--boot-fault", "read-fail-at:1:0:" + num(at), "--boot",
                                  "--dump-state", "st"});
        EXPECT_TRUE(r.at("seq") == 6 && r.at("deltas") == 1 && r.at("read_faults") == 1 && r.at("unread") == 0)
            << "a walk's read failing at " << at << ": " << r.text();
        expect_state(f, "st", fx().payloads("golden@5+one3@6"), "a walk's read failing: ");
        r = go(port(), f, {"--slot-b", "s.bin", "--boot-fault", "read-fail-at:1:2:" + num(at), "--boot",
                           "--dump-state", "st"});
        EXPECT_TRUE(r.at("seq") == 6 && r.at("deltas") == 1 && r.at("read_faults") == 1 && r.at("unread") == 0)
            << "a replay's read failing at " << at << ": " << r.text();
        expect_state(f, "st", fx().payloads("golden@5+one3@6"), "a replay's read failing: ");
    }
}

// A walk of the log ends on bytes a misread could make, so it stands only on
// two walks that return the same bytes: one misread walk is outvoted, three
// that disagree leave the slot UNREAD and the writer HELD. The chosen slot's
// replay is judged again: a misread there is read again.
TEST_F(NvmModel, replay_reads) {
    const std::string at = num(fx().num("journal_b") + fx().num("log_start") + 55);
    Files f = fx().files({{"s.bin", "golden@5+one3@6"}});
    Result r = go(port(), f, {"--slot-b", "s.bin", "--boot-fault", "read-vary-at:1:0:" + at, "--boot", "--dump-state",
                              "st"});
    EXPECT_TRUE(r.at("seq") == 6 && r.at("deltas") == 1 && r.at("torn") == 0 && r.at("read_faults") == 1 &&
                r.at("unread") == 0)
        << "one misread walk: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6"), "one misread walk: ");
    r = go(port(), f, {"--slot-b", "s.bin", "--boot-fault", "read-vary-at:3:0:" + at, "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("unread") == 2 && r.at("phase") == NVM_P_HELD && r.at("terminal") == NVM_T_BLANK)
        << "three walks that disagree: " << r.text();
    r = go(port(), f, {"--slot-b", "s.bin", "--boot-fault", "read-flip-at:1:2:" + at, "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("seq") == 6 && r.at("deltas") == 1 && r.at("read_faults") == 1 && r.at("unread") == 0)
        << "a misread replay: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6"), "a misread replay: ");
}

// A console commit compacts: the stage as a base into the other slot, at the
// authoritative slot's sequence, byte for byte as nvm_klj3.py writes it; then
// the old slot is erased in the background, and a boot finds the new one.
TEST_P(NvmBoth, compaction_bytes) {
    Files f = fx().files({{"s.bin", "golden@5+one3@6"}});
    Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--protect-auth", "--commit", "--dump-slot-a", "a.bin",
                              "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("ok") == 1 && r.at("auth") == 0 && r.at("seq") == 6 &&
                r.at("log_end") == fx().num("log_start") && r.at("erases") == 1)
        << "the compaction: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("one3@6"))) << "the base differs from nvm_klj3.py's";
    EXPECT_TRUE(f.blobs["b.bin"] == padded(Bytes{})) << "the old slot was not erased";
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("auth") == 0 && r.at("seq") == 6 && r.at("deltas") == 0) << "the boot after it: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6"), "the boot after it: ");
}

// Rule 8: a log with less than its reserve left compacts with no change.
TEST_P(NvmBoth, compaction_reserve) {
    Files f = fx().files({{"s.bin", "below_reserve"}});
    const Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--protect-auth", "--until-quiet",
                                    "--dump-state", "st"});
    const long long seq = 5 + fx().num("below_reserve_deltas");
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("auth") == 0 && r.at("seq") == seq &&
                r.at("log_end") == fx().num("log_start") && r.at("appends") == 0)
        << "a log below its reserve: " << r.text();
}

// Rule 5: a compaction yields to a save between pages. The save, made once
// three of the base's slowed pages are written, is appended to the old slot
// within its window and two pages; then its delta is copied behind the new
// base, page for page, before the authority moves, and a boot finds it.
TEST_P(NvmBoth, compaction_yields) {
    Files f = fx().files({{"s.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "s.bin", "--boot", "--protect-auth", "--times", "20:20000", "--until-bg",
                      num(NVM_B_READY), "--commit-try", "--until-programs", "3", "--mark", "--set",
                      set_word(last_id(), value(last_id(), 3)), "--until-ok", "2", "--dump-slot-a", "a.bin",
                      "--dump-slot-b", "b.bin", "--until-quiet"});
    const long long took = r.ok_at.empty() || r.marks.empty() ? -1 : static_cast<long long>(r.ok_at[0] - r.marks[0]);
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("appends") == 1 && r.at("auth") == 0 && r.at("seq") == 6 &&
                in(took, kWindowMs * kMs, (kWindowMs + 70) * kMs))
        << "a save inside a compaction, verified " << took << " us after it: " << r.text();
    const Bytes& a = f.blobs["a.bin"];
    const Bytes& b = f.blobs["b.bin"];
    const auto start = static_cast<std::ptrdiff_t>(fx().num("log_start"));
    EXPECT_TRUE(a.size() == b.size() && std::equal(b.begin() + start, b.begin() + start + 256, a.begin() + start))
        << "the old slot's delta is not copied behind the new base";
    Files g = fx().files({});
    g.blobs["a.bin"] = a;
    g.blobs["b.bin"] = b;
    const Result q = go(port(), g, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(q.at("seq") == 6) << "the boot after the move: " << q.text();
    expect_state(g, "st", fx().payloads("golden@5+one3@6"), "the boot after the move: ");
    // the new slot alone: its base at the old slot's sequence, and the copied
    // delta above it closing behind it
    Files h = fx().files({});
    h.blobs["a.bin"] = a;
    const Result n = go(port(), h, {"--slot-a", "a.bin", "--boot"});
    EXPECT_TRUE(n.at("auth") == 0 && n.at("seq") == 6 && n.at("deltas") == 1 && n.at("torn") == 0)
        << "the new slot alone: " << n.text();
}

// A record a base's page cuts is taken whole, as it was when the page was:
// the record that runs past the first page boundary it crosses is changed
// and saved at once (the console) between that page and the next, and the
// base still holds its old value, every frame closing; the save goes to the
// old slot and is copied behind the base, so a boot of the new slot alone
// finds the new value.
TEST_P(NvmBoth, compaction_carry) {
    const std::vector<long long>& offs = fx().list("offs");
    const std::vector<unsigned> ids = rids();
    std::size_t cut = ids.size();
    for (std::size_t k = 0; k < ids.size() && cut == ids.size(); ++k) {
        const long long start = 40 + offs[k];
        const long long end = start + fx().num("rec_hdr") + plen(ids[k]);
        if (start / 256 != (end - 1) / 256) {
            cut = k;
        }
    }
    ASSERT_LT(cut, ids.size()) << "no record of the shape crosses a page of the base";
    const unsigned rid = ids[cut];
    const long long page = (40 + offs[cut]) / 256;
    Files f = fx().files({{"s.bin", "golden@5"}});
    Result r = go(port(), f,
                  {"--slot-b", "s.bin", "--boot", "--protect-auth", "--times", "20:20000", "--until-bg",
                   num(NVM_B_READY), "--commit-try", "--until-programs", num(page + 1), "--until-phase",
                   num(NVM_P_IDLE), "--set", set_word(rid, value(rid, 7)), "--commit-try", "--until-quiet",
                   "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("appends") == 1 && r.at("auth") == 0 && r.at("failed") == 0)
        << "a save between the pages of a cut record: " << r.text();
    const Bytes& golden = fx().blob("golden@5");
    EXPECT_TRUE(f.blobs["a.bin"].size() >= golden.size() &&
                std::equal(golden.begin(), golden.end(), f.blobs["a.bin"].begin()))
        << "the base does not hold every record as it was when its page was written";
    Files g;
    g.blobs["a.bin"] = f.blobs["a.bin"];
    r = go(port(), g, {"--slot-a", "a.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("vd_a") == NVM_VD_OK && r.at("deltas") == 1)
        << "the new slot alone: " << r.text();
    expect_state(g, "st", with(fx().payloads("golden"), {{rid, value(rid, 7)}}), "the new slot alone: ");
}

// A compaction that fails leaves part of a base behind: the other slot is
// prepared again, its written block erased, and the retry writes the base.
TEST_P(NvmBoth, compaction_failure_reprepares) {
    Files f = fx().files({{"s.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "s.bin", "--boot", "--protect-auth", "--until-bg", num(NVM_B_READY),
                                    "--fault", "program-flip:1", "--commit", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("failed") == 1 && r.at("compactions") == 1 && r.at("auth") == 0 && r.at("erases") >= 2)
        << "a failed compaction: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("golden@5"))) << "the retried base differs";
}

// With no authoritative slot, a record latched behind the first base's front
// keeps its value out of that base: it is appended behind it once the base
// holds the authority, and a boot finds it.
TEST_P(NvmBoth, first_base_behind) {
    Files f;
    Result r = go(port(), f,
               {"--blank", "--boot", "--times", "20:20000", "--until-bg", num(NVM_B_READY), "--commit-try",
                "--until-programs", "3", "--set", set_word(first_id(), value(first_id(), 9)), "--until-quiet",
                "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("appends") == 1 && r.at("auth") == 0 && r.at("seq") == 2 &&
                r.at("pending") == 0)
        << "a change behind the first base: " << r.text();
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("seq") == 2 && r.at("deltas") == 1) << "the boot after it: " << r.text();
    expect_state(f, "st", {{first_id(), value(first_id(), 9)}}, "the boot after it: ");
}

// T9: a power cut inside every media effect of a compaction a save lands in
// (the base's pages, the old slot's delta, the copy behind the base and the
// old slot's erase, at 0, 1/256, 1/2 and 255/256 of each): the board boots
// the old values or the new ones exactly, the new ones whenever the save had
// been reported, never touching the authoritative slot's closed bytes, and
// recovers.
TEST_P(NvmBoth, torn_compaction) {
    Files f = fx().files({{"o.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "o.bin", "--powercut-compaction"});
    const auto pc = [&r](const char* key) { return r.powercut.count(key) != 0u ? r.powercut.at(key) : -1; };
    EXPECT_TRUE(pc("effects") >= pages() + 2 && pc("cases") == 4 * pc("effects") && pc("bad") == 0 && pc("new") >= 1 &&
                pc("reported") >= 1 && pc("old") + pc("new") == pc("cases"))
        << "power cut in a compaction: effects " << pc("effects") << ", cases " << pc("cases") << ", old " << pc("old")
        << ", new " << pc("new") << ", reported " << pc("reported") << ", bad " << pc("bad");
}

//! Slot B golden, slot A written so the background preparation erases it,
//! for 3 s, and the change after the erase starts.
std::vector<std::string> erase_running(Files* f, const std::string& times = "3000:1000") {
    *f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    return {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--protect-auth", "--times", times,
            "--until-bg", num(NVM_B_ERASE_WAIT), "--mark", "--set", set_word(last_id(), value(last_id(), 3))};
}

// A compaction whose copy of the old slot's log cannot be read fails
// VD_VERIFY: the other slot is prepared again and the next compaction moves
// the authority, the save's delta copied.
TEST_F(NvmModel, compaction_copy_read) {
    Files f = fx().files({{"s.bin", "golden@5"}});
    const std::string at = num(fx().num("journal_b") + fx().num("log_start") + 8);
    const Result r = go(port(), f,
                     {"--slot-b", "s.bin", "--boot", "--protect-auth", "--times", "20:20000", "--until-bg",
                      num(NVM_B_READY), "--commit-try", "--until-programs", "3", "--fault", "read-fail-at:1:1:" + at,
                      "--set", set_word(last_id(), value(last_id(), 3)), "--until-quiet", "--dump-state", "st"});
    EXPECT_TRUE(r.at("failed") == 1 && r.at("last") == NVM_VD_OK && r.at("compactions") == 1 && r.at("appends") == 1 &&
                r.at("auth") == 0 && r.at("seq") == 6 && r.at("prep_failed") == 0)
        << "a copy read failing: " << r.text();
    expect_state(f, "st", fx().payloads("golden@5+one3@6"), "a copy read failing: ");
}

// T10: a save during the background erase suspends it, programs and reads
// back, and resumes it: it is verified within its window and a page, not
// after the erase, and the erase then runs its time out. The suspend is
// timed, well inside the room the bound leaves it, and none is slow.
TEST_P(NvmBoth, erase_suspended) {
    Files f;
    const Result r = go(port(), f, concat(erase_running(&f), {"--until-idle", "--clock", "--until-quiet"}));
    const long long took = r.ok_at.empty() || r.marks.empty() ? -1 : static_cast<long long>(r.ok_at[0] - r.marks[0]);
    EXPECT_TRUE(r.at("ok") == 1 && in(took, kWindowMs * kMs, (kWindowMs + 20) * kMs) && r.at("suspends") == 1 &&
                r.at("fm_suspends") == 1 && r.at("fm_resumes") == 1 && r.at("suspend_slow") == 0 &&
                r.at("suspend_us_max") >= 15 && r.at("suspend_us_max") < 1000 && r.at("bg") == NVM_B_READY &&
                r.at("prep_failed") == 0)
        << "a save in the erase, verified " << took << " us after the change: " << r.text();
    if (port() == Port::Litespi) {
        EXPECT_TRUE(r.at("ls_pes") == 1 && r.at("ls_per") == 1) << "LiteSPI suspend and resume: " << r.text();
    }
}

// A save that finds the erase ended by the time it programs suspends
// nothing: a 151 ms erase starting with the change ends while a capture of
// every record runs.
TEST_P(NvmBoth, erase_ended_before_suspend) {
    Files f = fx().files({{"g.bin", "golden@5"}, {"o.bin", "golden@3"}});
    const Result r = go(port(), f, {"--slot-a", "o.bin", "--slot-b", "g.bin", "--boot", "--times", "151:1000",
                                    "--until-bg", num(NVM_B_ERASE_WAIT), "--set-pattern", "6", "--until-quiet"});
    EXPECT_TRUE(r.at("appends") >= 1 && r.at("failed") == 0 && r.at("fm_suspends") == 0 && r.at("suspends") == 0 &&
                r.at("bg") == NVM_B_READY)
        << "an erase ended before the first program: " << r.text();
}

// The suspend's own command failing on the command master: the status read
// before it (an RX stall) or the PES byte (a TX stall after the status
// read's four), fails the save VD_ERASE without tearing the log, and the
// retry commits.
TEST_F(NvmLitespi, suspend_master_stall) {
    for (const char* stall : {"rx:1:0:0", "tx:1:4:0"}) {
        Files f;
        Result r = go(port(), f,
                      concat(erase_running(&f), {"--until-phase", num(NVM_P_SUSPEND), "--ls-stall", stall, "--run-ms",
                                                 "50"}),
                      {"ls_short"});
        EXPECT_TRUE(r.at("failed") == 1 && r.at("first") == NVM_VD_ERASE && r.at("torn") == 0 && r.at("ok") == 0)
            << "a stalled suspend, " << stall << ": " << r.text();
        r = go(port(), f,
               concat(erase_running(&f), {"--until-phase", num(NVM_P_SUSPEND), "--ls-stall", stall, "--until-idle"}),
               {"ls_short"});
        EXPECT_TRUE(r.at("failed") == 1 && r.at("ok") == 1 && r.at("appends") == 1)
            << "the retry after a stalled suspend, " << stall << ": " << r.text();
    }
}

// Assumption A3: the writer times every suspend and counts one that took
// longer than the room the bound leaves it (95.29 ms); the save still
// commits. A suspend the device ignores fails the save VD_ERASE at its
// deadline without tearing the log, and the retry commits once the device
// answers; a suspend that takes effect after that is resumed.
TEST_P(NvmBoth, suspend_slow) {
    Files f;
    Result r = go(port(), f, concat(erase_running(&f), {"--fault", "suspend-slow:1:0:120000", "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("suspends") == 1 && r.at("suspend_slow") == 1 &&
                r.at("suspend_us_max") >= 120000 && r.at("failed") == 0)
        << "a slow suspend: " << r.text();
    r = go(port(), f, concat(erase_running(&f), {"--fault", "suspend-ignored:1", "--run-ms", "900"}));
    EXPECT_TRUE(r.at("ok") == 0 && r.at("failed") == 1 && r.at("first") == NVM_VD_ERASE && r.at("torn") == 0 &&
                r.fail_at.size() == 1u && !r.marks.empty() &&
                in(static_cast<long long>(r.fail_at[0] - r.marks[0]), (kWindowMs + kAppendTimeoutMs) * kMs,
                   (kWindowMs + kAppendTimeoutMs + 5) * kMs))
        << "an ignored suspend: " << r.text();
    r = go(port(), f, concat(erase_running(&f), {"--fault", "suspend-ignored:1", "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 1 && r.at("appends") == 1 && r.at("suspended") == 0)
        << "the retry after an ignored suspend: " << r.text();
    // a suspend that takes effect after the save gave up on it is resumed
    // once the device answers, and the erase runs out
    r = go(port(), f, concat(erase_running(&f), {"--fault", "suspend-slow:1:0:600000", "--until-quiet"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 1 && r.at("suspended") == 0 &&
                r.at("fm_resumes") == r.at("fm_suspends") && r.at("bg") == NVM_B_READY)
        << "a suspend that took effect late: " << r.text();
}

// A save that fails while it holds the erase suspended leaves it suspended
// only until the device answers: the erase is resumed, runs out, and the
// preparation completes; the save is retried by a compaction.
TEST_P(NvmBoth, erase_resumed_after_failure) {
    Files f;
    const Result r = go(port(), f, concat(erase_running(&f), {"--fault", "program-drop:1", "--until-quiet"}));
    EXPECT_TRUE(r.at("failed") == 1 && r.at("fm_suspends") >= 1 &&
                r.at("fm_resumes") == r.at("fm_suspends") && r.at("suspended") == 0 && r.at("bg") == NVM_B_READY &&
                r.at("ok") == 2 && r.at("prep_failed") == 0)
        << "a failed save in a suspended erase: " << r.text();
}

// The erase's deadline counts the time it ran, not the time a save held it
// suspended: a 3.4 s erase suspended for a slowed delta runs past 3.5 s of
// wall time and does not fail.
TEST_P(NvmBoth, erase_time_excludes_suspend) {
    Files f;
    std::vector<std::string> words = erase_running(&f, "3400:40000");
    for (const auto& [rid, payload] : fx().payloads("changed5c_firsts")) {
        words.insert(words.end(), {"--set", set_word(rid, payload)});
    }
    words.insert(words.end(), {"--until-quiet"});
    const Result r = go(port(), f, words);
    EXPECT_TRUE(r.at("prep_failed") == 0 && r.at("bg") == NVM_B_READY && r.at("suspends") >= 1 &&
                r.at("appends") == 1 && r.at("failed") == 0 && r.at("now_ms") > 3500 + 100)
        << "an erase suspended past its deadline in wall time: " << r.text();
}

// T12: a log with no room left takes no delta: the save is published pending,
// never dropped, and a compaction carries it once the other slot is
// prepared; a boot then finds it.
TEST_P(NvmBoth, reserve_exhausted) {
    Files f;
    f = fx().files({{"s.bin", "log_full"}, {"o.bin", "golden@3"}});
    const std::vector<std::string> head = {"--slot-a", "o.bin", "--slot-b", "s.bin", "--boot", "--protect-auth",
                                           "--times", "3000:1000", "--set", set_word(first_id(), value(first_id(), 9))};
    Result r = go(port(), f, concat(head, {"--run-ms", "1000"}));
    EXPECT_TRUE(r.at("log_end") == fx().num("slot_bytes") && r.at("pending") == 1 && r.at("n_inflight") == 1 &&
                r.at("ok") == 0 && r.at("appends") == 0 && r.at("failed") == 0)
        << "a full log: " << r.text();
    r = go(port(), f, concat(head, {"--until-quiet", "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"}));
    EXPECT_TRUE(r.at("compactions") == 1 && r.at("appends") == 1 && r.at("pending") == 0 && r.at("auth") == 0)
        << "the compaction after it: " << r.text();
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("auth") == 0 && r.at("seq") == 6 + fx().num("log_full_deltas")) << "the boot: " << r.text();
}

// A1: a burst larger than one segment drains as successive deltas, each at
// most NVM_SEG_PAGES pages, with no new window between them.
TEST_P(NvmBoth, burst_deltas) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--set-pattern", "4", "--until-idle"});
    EXPECT_TRUE(r.at("appends") == fx().num("pattern_deltas") && r.at("pending") == 0 && r.at("seg_max") == fx().num("seg_max") &&
                r.at("log_start") == fx().num("log_start") && r.at("reserve") == fx().num("reserve"))
        << "every record changed: " << r.text();
}

// T13, decision 7: an append that is not read back within T-NVM-COMMIT-TIMEOUT,
// 500 ms from the save falling due, fails VD_PROGRAM and leaves its segment
// torn: a delta of every record, each page 49 ms (inside one page's wait).
TEST_P(NvmBoth, append_deadline) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--times", "20:49000", "--mark",
                                    "--set-pattern", "5", "--run-ms", "900"});
    EXPECT_TRUE(r.at("failed") == 1 && r.at("first") == NVM_VD_PROGRAM && r.at("torn") == 1 && r.at("appends") == 0 &&
                r.fail_at.size() == 1u && !r.marks.empty() &&
                in(static_cast<long long>(r.fail_at[0] - r.marks[0]), (kWindowMs + kAppendTimeoutMs) * kMs,
                   (kWindowMs + kAppendTimeoutMs + 5) * kMs))
        << "a slow append: " << r.text();
}

}  // namespace
}  // namespace nvm_test
