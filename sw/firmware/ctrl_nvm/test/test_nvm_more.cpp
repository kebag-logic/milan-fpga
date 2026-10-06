// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_more.cpp - store paths the hand-rolled suite left unwalked
// (#665 lane FT, for branch coverage), each graded against the fixture as
// the checks are:
//
//   long_container_reads       a container longer than the stage: each of
//                              its reads failing once, and its CRC not
//                              closing;
//   console_commit_unchanged   the console writes a verified container again
//                              when nothing changed;
//   first_commit_no_blank_slot with no slot accepted and neither blank, the
//                              first commit takes slot A (DR5's other face);
//   nothing_to_save            a change whose owner has nothing to save
//                              leaves the staged bytes as they were;
//   change_unknown_record      a change to a record the shape does not have
//                              marks nothing;
//   capture_window_edges       a change the running capture has passed, or
//                              one after its last latch, opens a window of
//                              its own (DR2a).

#include <gtest/gtest.h>

#include <string>
#include <vector>

#include "nvm_c.hpp"
#include "nvm_suite.hpp"

namespace nvm_test {
namespace {

std::string num(long long v) { return std::to_string(v); }

// The header read, the two streamed reads of the CRC, the trailer and the
// stage: each failing once is a media fault, and the read again judges the
// slot as klj2_decode does. A CRC that does not close is refused VD_CRC.
TEST_F(NvmModel, long_container_reads) {
    for (const int at : {1, 2, 3, 4}) {
        Files f = fx().files({{"l.bin", "long"}});
        const Result r = go(port(), f, {"--slot-a", "l.bin", "--boot-fault", "read-fail:1:" + num(at), "--boot"});
        EXPECT_TRUE(r.at("read_faults") == 1 && r.at("vd_a") == fx().num("long_verdict") && r.at("unread") == 0)
            << "read " << at << " of a container longer than the stage failing once: " << r.text();
    }
    Files f = fx().files({{"l.bin", "long_crc"}});
    const Result r = go(port(), f, {"--slot-a", "l.bin", "--boot"});
    EXPECT_TRUE(r.at("vd_a") == fx().num("long_crc_verdict") && r.at("vd_a") == NVM_VD_CRC && r.at("read_faults") == 0)
        << "a container longer than the stage whose CRC does not close: " << r.text();
}

// A console commit with nothing changed writes the verified container again
// at the next sequence, into the other slot (the console's force).
TEST_P(NvmBoth, console_commit_unchanged) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--commit", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 6 && r.at("auth") == 0 && r.at("skipped") == 0)
        << "console commit of an unchanged container: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("golden@6"))) << "slot A is not the container at sequence 6";
}

// DR5 with no blank slot: neither slot accepted and neither blank, the first
// commit takes slot A, and slot B keeps its refused image.
TEST_P(NvmBoth, first_commit_no_blank_slot) {
    const unsigned rid = rids().back();
    Files f = fx().files({{"a.bin", "golden@9~49"}, {"b.bin", "golden@a~43"}});
    const Result r = go(port(), f,
                        {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--set", set_word(rid, value(rid, 7)),
                         "--until-idle", "--dump-slot-a", "a1.bin", "--dump-slot-b", "b1.bin"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_BLANK && r.at("ok") == 1 && r.at("auth") == 0 && r.at("seq") == 1)
        << "first commit with both slots refused: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a1.bin"], fx().blob("erased_one7@1"))) << "slot A is not the first container";
    EXPECT_TRUE(slot_holds(f.blobs["b1.bin"], fx().blob("golden@a~43"))) << "slot B's refused image was touched";
}

// A change whose owner has nothing valid to save leaves the staged bytes: on
// a blank board the commit writes the all-erased container.
TEST_P(NvmBoth, nothing_to_save) {
    Files f;
    const Result r = go(port(), f,
                        {"--blank", "--boot", "--touch", num(rids().back()), "--until-idle", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 1 && r.at("dirty") == 0 && r.at("pending") == 0)
        << "a change with nothing to save: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("erased@1"))) << "the staged bytes did not stand";
}

// A change to a group past the last, or an index past a group's count, marks
// nothing and starts no window.
TEST_F(NvmModel, change_unknown_record) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                        {"--slot-b", "g.bin", "--boot", "--change", num(NVM_G_COUNT) + ":0", "--change",
                         num(NVM_G_CFG) + ":1", "--run-ms", "3000"});
    EXPECT_TRUE(r.at("dirty") == 0 && r.at("erases") == 0 && r.at("ok") == 0 && r.at("skipped") == 0)
        << "changes to records the shape does not have: " << r.text();
}

// DR2a at the capture's edges: a change to a record the running capture has
// already passed, and a change after its last latch while it is still in
// the capture phase, each wait a window of their own.
TEST_P(NvmBoth, capture_window_edges) {
    const unsigned first = rids().front();
    const unsigned last = rids().back();
    Files f = fx().files({{"g.bin", "golden@5"}});
    Result r = go(port(), f,
                  {"--slot-b", "g.bin", "--boot", "--set-pattern", "1", "--until-phase", num(NVM_P_CAPTURE),
                   "--service", "3", "--mark", "--set", set_word(first, value(first, 9)), "--until-idle"});
    EXPECT_TRUE(r.at("ok") == 2 && in(after_mark(r, 1), 1000 * kMs, 1050 * kMs))
        << "a change the capture has passed: erase " << after_mark(r, 1) << " us after it: " << r.text();
    r = go(port(), f,
           {"--slot-b", "g.bin", "--boot", "--set", set_word(last, value(last, 1)), "--until-phase",
            num(NVM_P_CAPTURE), "--service", "1", "--mark", "--set", set_word(first, value(first, 9)), "--until-idle"});
    EXPECT_TRUE(r.at("ok") == 2 && in(after_mark(r, 1), 1000 * kMs, 1050 * kMs))
        << "a change after the capture's last latch: erase " << after_mark(r, 1) << " us after it: " << r.text();
}

}  // namespace
}  // namespace nvm_test
