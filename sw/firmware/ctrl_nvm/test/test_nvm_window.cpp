// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_window.cpp - the first-dirty windows (DR2a), the binding class's
// own (#1009): Milan v1.2 5.5.3.5.3 saves the binding parameters before the
// BIND_RX_RESPONSE is sent, and 5.3.8.3 counts a stream input's started/stopped
// state with them, so a change of a binding record is captured 100 ms after
// the first such change; every other record keeps 1,000 ms. A window is not
// restarted, a save captures everything dirty, and a binding change the save in
// flight cannot take opens the next window.

#include <algorithm>
#include <cstdint>
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

const std::vector<std::string> kTwin = {"--slot-a", "a5.bin", "--slot-b", "b6.bin"};
const std::vector<std::string> kDump = {"--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"};
Files twin() { return fx().files({{"a5.bin", "golden@5/minor1"}, {"b6.bin", "golden@6/minor1"}}); }

unsigned bind_rid() { return static_cast<unsigned>(fx().num("bind_rid")); }
unsigned bind_rid2() { return static_cast<unsigned>(fx().num("bind_rid2")); }

//! A binding change's window and any other's, each as the time of the save's commit after the change: a frame's
//! commit, or a whole container's, is some steps after its capture's start, and both bounds leave that room.
constexpr long long kBindLo = 100 * kMs;
constexpr long long kOtherLo = 1000 * kMs;
constexpr long long kSlack = 100 * kMs;

long long ok_after_mark(const Result& r, std::size_t k) {
    return (r.ok_at.size() <= k || r.marks.empty())
               ? -1
               : static_cast<long long>(r.ok_at[k]) - static_cast<long long>(r.marks.back());
}

// The window's length is the record's class: the binding records' 100 ms, and 1,000 ms for the first record below and
// the first above their block, the last record and the first.
TEST_P(NvmBoth, binding_window) {
    const std::vector<long long> ids = fx().list("binding_ids");
    std::vector<unsigned> others;
    unsigned below = 0;
    unsigned above = 0;
    for (const unsigned rid : rids()) {
        if (rid < static_cast<unsigned>(ids.front())) {
            below = rid;
        } else if (rid > static_cast<unsigned>(ids.back()) && above == 0u) {
            above = rid;
        }
    }
    others = {rids().front(), below, above, rids().back()};
    for (const unsigned rid : {static_cast<unsigned>(ids.front()), static_cast<unsigned>(ids.back())}) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, {"--boot", "--mark", "--set", set_word(rid, value(rid, 7)), "--until-idle"}));
        EXPECT_TRUE(r.at("ok") == 1 && in(ok_after_mark(r, 0), kBindLo, kBindLo + kSlack))
            << "binding record " << rid << ": committed " << ok_after_mark(r, 0) << " us after it: " << r.text();
    }
    for (const unsigned rid : others) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, {"--boot", "--mark", "--set", set_word(rid, value(rid, 7)), "--until-idle",
                                           "--run-ms", "2000"}));
        EXPECT_TRUE(r.at("ok") == 1 && ok_after_mark(r, 0) >= kOtherLo)
            << "record " << rid << ": committed " << ok_after_mark(r, 0) << " us after it: " << r.text();
    }
}

// The window starts at the class's first change and is not restarted: a second binding change 60 ms into it, and one
// again 60 ms later, are in the same save, at the first one's time.
TEST_P(NvmBoth, binding_window_not_restarted) {
    const unsigned rb = bind_rid();
    const unsigned rb2 = bind_rid2();
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--mark", "--set", set_word(rb, value(rb, 7)), "--run-ms", "60",
                                              "--set", set_word(rb2, value(rb2, 7)), "--run-ms", "30", "--set",
                                              set_word(rb, value(rb, 8)), "--until-idle"},
                                             kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && in(ok_after_mark(r, 0), kBindLo, kBindLo + kSlack))
        << "committed " << ok_after_mark(r, 0) << " us after the first change: " << r.text();
    const Result b = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(b.at("terminal") == NVM_T_COMPLETE) << b.text();
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 8)}, {rb2, value(rb2, 7)}}), "both changes");
}

// The earliest end of the open windows starts the capture, which takes everything dirty: a binding change 300 ms into
// another record's window, and another record's 50 ms into a binding's.
TEST_P(NvmBoth, earliest_window_takes_everything) {
    const unsigned rb = bind_rid();
    const unsigned other = rids().back();
    Files f = twin();
    Result r = go(port(), f,
                  concat(kTwin, concat({"--boot", "--set", set_word(other, value(other, 7)), "--run-ms", "300", "--mark",
                                        "--set", set_word(rb, value(rb, 7)), "--until-idle", "--run-ms", "2000"},
                                       kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && in(sealed_after_mark(r, 0), kBindLo, kBindLo + kSlack))
        << "a binding change inside another window: sealed " << sealed_after_mark(r, 0) << " us after it: " << r.text();
    go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 7)}, {other, value(other, 7)}}),
                 "one save takes both");
    f = twin();
    r = go(port(), f,
           concat(kTwin, concat({"--boot", "--mark", "--set", set_word(rb, value(rb, 8)), "--run-ms", "50", "--set",
                                 set_word(other, value(other, 8)), "--until-idle", "--run-ms", "2000"},
                                kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && in(sealed_after_mark(r, 0), kBindLo, kBindLo + kSlack))
        << "another record's change inside a binding window: sealed " << sealed_after_mark(r, 0) << ": " << r.text();
    go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 8)}, {other, value(other, 8)}}),
                 "one save takes both, the other way");
}

// A binding change the save in flight cannot take opens the next window, and the save is the one that takes it; any
// other record's starts the next save at the first idle step, as #920 has it, and takes a binding change with it.
TEST_P(NvmBoth, binding_change_in_flight_opens_window) {
    const unsigned rb = bind_rid();
    const unsigned rb2 = bind_rid2();
    const unsigned other = rids().back();
    Files f = twin();
    Result r = go(port(), f,
                  concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-phase",
                                        num(NVM_P_SEAL), "--mark", "--set", set_word(rb2, value(rb2, 7)),
                                        "--until-idle"},
                                       kDump)));
    EXPECT_TRUE(r.at("ok") == 2 && in(ok_after_mark(r, 1), kBindLo, kBindLo + kSlack) &&
                static_cast<long long>(r.ok_at[1] - r.ok_at[0]) >= kBindLo - kSlack)
        << "committed " << ok_after_mark(r, 1) << " us after a change in flight: " << r.text();
    go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 7)}}), "both saves");
    f = twin();
    r = go(port(), f,
           concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-phase", num(NVM_P_SEAL), "--mark",
                          "--set", set_word(other, value(other, 7)), "--set", set_word(rb2, value(rb2, 7)),
                          "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 2 && ok_after_mark(r, 1) >= 0 && ok_after_mark(r, 1) < 1000 * kMs &&
                static_cast<long long>(r.sealed[1] - r.ok_at[0]) < kBindLo)
        << "another record's change in flight: the next save at the first idle step, " << r.text();
}

// A slot whose frames leave the room two largest frames is not written whole while idle, and one page less is: the
// room's reserve is what the next change's frame, and one more, need in the other slot.
TEST_P(NvmBoth, room_reserve) {
    const unsigned rb = bind_rid();
    const long long base = fx().num("delta_base");
    const long long pages = (fx().num("delta_end") - base) / NVM_FLASH_PAGE;
    const long long reserve = NVM_DELTA_RESERVE / NVM_FLASH_PAGE;
    for (const long long left : {reserve, reserve - 1}) {
        // the frames a save of one binding leaves, of one page each: A's, so that the pages left are `left`; a frame
        // into B first makes A the one that is not authoritative
        const long long n = pages - left;
        Bytes a = fx().blob("golden@5/minor1");
        a.resize(static_cast<std::size_t>(base), 0xffu);
        for (long long k = 0; k < n; ++k) {
            const Bytes& one = fx().blob("kld/chain@" + num(k));
            a.insert(a.end(), one.begin(), one.end());
            a.resize((a.size() + 255u) / 256u * 256u, 0xffu);
        }
        Files f = fx().files({{"b6.bin", "golden@6/minor1"}});
        f.blobs["a5.bin"] = a;
        const Result r = go(port(), f,
                            concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--run-ms",
                                           "3000"}));
        EXPECT_TRUE(r.at("deltas") == 1 && r.at("tidied") == (left < reserve ? 1 : 0))
            << left << " pages left of " << pages << ": tidied " << r.at("tidied") << ", " << r.text();
    }
}

// A binding change that arrives while a full slot is written whole goes as a frame into the other slot after it, and
// is the state a boot restores.
TEST_P(NvmBoth, binding_change_in_a_full_room_commit) {
    const unsigned rb = bind_rid();
    const unsigned rb2 = bind_rid2();
    Files f = fx().files({{"a5.bin", "slot/g5+full"}, {"b6.bin", "golden@6/minor1"}});
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--times", "150:500", "--set", set_word(rb, value(rb, 7)),
                                              "--until-phase", num(NVM_P_IDLE), "--until-phase",
                                              num(NVM_P_ERASE_WAIT), "--mark", "--set", set_word(rb2, value(rb2, 8)),
                                              "--until-idle"},
                                             kDump)));
    EXPECT_TRUE(r.at("ok") == 3 && r.at("tidied") == 1 && r.at("deltas") == 2 && r.at("erases") == 1)
        << "a frame, the full slot whole, then a frame: " << r.text();
    go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 8)}}),
                 "the change that arrived in the full room's commit");
}

// A burst of 64 bindings, one every 10 ms over every input: it converges, the last value of each bound, in as many
// saves as the windows that open, and (#876) with no erase where each save's span fits a frame.
TEST_P(NvmBoth, burst_of_64_bindings) {
    const std::vector<long long> ids = fx().list("binding_ids");
    Files f = twin();
    std::vector<std::string> words = concat(kTwin, {"--boot", "--mark"});
    Payloads want = fx().payloads("golden");
    for (unsigned k = 0; k < 64u; ++k) {
        const unsigned rid = static_cast<unsigned>(ids[k % ids.size()]);
        words = concat(words, {"--set", set_word(rid, value(rid, 1u + k)), "--run-ms", "10"});
        want[rid] = value(rid, 1u + k);
    }
    words = concat(words, concat({"--until-idle", "--run-ms", "3000"}, kDump));
    const Result r = go(port(), f, words);
    EXPECT_TRUE(r.at("dirty") == 0 && r.at("pending") == 0 && r.at("failed") == 0 && r.at("stale") == 0)
        << "the burst converges: " << r.text();
    // 640 ms of changes: a save every window and its length, and at most one more for what the last one left
    EXPECT_TRUE(in(r.at("ok"), 3, 10)) << "saves of the burst: " << r.at("ok") << ", " << r.text();
    if (NVM_DLEN(static_cast<unsigned>(ids.size()) * (NVM_REC_HDR + plen(static_cast<unsigned>(ids.front())))) <=
        NVM_PAYLOAD_MAX) {
        EXPECT_TRUE(r.at("erases") == 0 && r.at("deltas") == r.at("ok"))
            << "erases " << r.at("erases") << ", frames " << r.at("deltas") << ": " << r.text();
    }
    go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    expect_state(f, "st", want, "the burst's last values");
}

}  // namespace
}  // namespace nvm_test
