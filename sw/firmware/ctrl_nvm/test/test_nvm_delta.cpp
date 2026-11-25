// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_delta.cpp - the delta frames (#1009). A save writes only the
// records the slot it writes lacks, in a frame after that slot's container,
// erasing nothing; the slot that is authoritative is never touched, and the
// blank check and the verify cover the frame. A boot applies a slot's frames
// in order over its container and judges the result by section 6.2. Every
// byte is the fixture's (nvm_klj3.py's klj3_delta and klj3_slot), and every
// restored state is one of its payload sets.

#include <cstdint>
#include <string>
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

//! The first binding record, what a BIND_RX saves.
unsigned bind_rid() { return static_cast<unsigned>(fx().num("bind_rid")); }

//! A slot after the store appended the fixture's frames to `base`, each on its own page.
Bytes with_frames(const Bytes& base, const std::vector<std::string>& frames) {
    Bytes out = base;
    out.resize(static_cast<std::size_t>(fx().num("delta_base")), 0xffu);
    for (const std::string& name : frames) {
        const Bytes& frame = fx().blob(name);
        out.insert(out.end(), frame.begin(), frame.end());
        out.resize((out.size() + 255u) / 256u * 256u, 0xffu);
    }
    return out;
}

//! Two slots of the same records, sequences 5 and 6, at the minor that takes frames: the boot knows the older one
//! lacks nothing, so the next save is a frame into it.
const std::vector<std::string> kTwin = {"--slot-a", "a5.bin", "--slot-b", "b6.bin"};
Files twin() { return fx().files({{"a5.bin", "golden@5/minor1"}, {"b6.bin", "golden@6/minor1"}}); }

//! A boot of the slots a run dumped as a.bin and b.bin, its state kept as st.
Result boot_dumped(Port port, Files& f) {
    return go(port, f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
}

const std::vector<std::string> kDump = {"--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"};

// The shape's frames' room is the reference's.
TEST_P(NvmBoth, delta_room) {
    EXPECT_TRUE(fx().num("delta_base") == NVM_DELTA_BASE && fx().num("delta_end") == NVM_DELTA_END &&
                NVM_DELTA_END - NVM_DELTA_BASE >= 2u * NVM_FLASH_PAGE)
        << "the room is " << NVM_DELTA_BASE << " to " << NVM_DELTA_END << ", the reference's "
        << fx().num("delta_base") << " to " << fx().num("delta_end");
}

// #1009's save: a BIND_RX's one record goes as a one-page frame into the older slot, after its container, with no
// erase; the authoritative slot is untouched; the stage holds the whole new container; its window is DR2a's and the
// save is durable a few steps after it; the next boot restores it.
TEST_P(NvmBoth, bind_save_is_a_frame) {
    Files f = twin();
    const unsigned rb = bind_rid();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--mark", "--set", set_word(rb, value(rb, 7)), "--until-idle",
                                              "--dump-stage", "stage.bin"},
                                             kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 1 && r.at("erases") == 0 && r.at("programs") == 1 &&
                r.at("failed") == 0 && r.at("auth") == 0 && r.at("seq") == 7)
        << "a frame of the one record: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], with_frames(fx().blob("golden@5/minor1"), {"kld/bind7@7"})))
        << "slot A is not its container and the reference's frame";
    EXPECT_TRUE(slot_holds(f.blobs["b.bin"], fx().blob("golden@6/minor1"))) << "the authoritative slot changed";
    EXPECT_TRUE(f.blobs["stage.bin"] == fx().blob("bind7@7/minor1")) << "the stage is not the whole new container";
    EXPECT_TRUE(in(sealed_after_mark(r, 0), 1000 * kMs, 1050 * kMs) && !r.ok_at.empty() &&
                in(static_cast<long long>(r.ok_at[0] - r.marks.back()), 1000 * kMs, 1050 * kMs))
        << "sealed " << sealed_after_mark(r, 0) << " us after the change: " << r.text();
    const Result b = boot_dumped(port(), f);
    EXPECT_TRUE(b.at("auth") == 0 && b.at("seq") == 7 && b.at("seq_a") == 7 && b.at("terminal") == NVM_T_COMPLETE &&
                b.at("phase") == NVM_P_IDLE)
        << "the frame's boot: " << b.text();
    expect_state(f, "st", fx().payloads("bind7"), "the frame's boot");
}

// Frames alternate between the slots, each carrying what its slot lacks; after a boot, what the other slot lacks
// is read off its container, so the next save is a frame again.
TEST_P(NvmBoth, frames_chain) {
    Files f = twin();
    const unsigned rb = bind_rid();
    Result r = go(port(), f,
                  concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--set",
                                        set_word(rb, value(rb, 8)), "--until-idle", "--set",
                                        set_word(rb, value(rb, 9)), "--until-idle"},
                                       kDump)));
    EXPECT_TRUE(r.at("ok") == 3 && r.at("deltas") == 3 && r.at("erases") == 0 && r.at("auth") == 0 && r.at("seq") == 9)
        << "three frames: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], with_frames(fx().blob("golden@5/minor1"), {"kld/bind7@7", "kld/bind9@9"})))
        << "slot A is not its container and two frames";
    EXPECT_TRUE(slot_holds(f.blobs["b.bin"], with_frames(fx().blob("golden@6/minor1"), {"kld/bind8@8"})))
        << "slot B is not its container and one frame";
    r = go(port(), f,
           concat({"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st0", "--set",
                   set_word(rb, value(rb, 7)), "--until-idle", "--boot", "--dump-state", "st"},
                  {}));
    expect_state(f, "st0", fx().payloads("bind9"), "two frames' boot");
    expect_state(f, "st", fx().payloads("bind7"), "the frame after a boot");
    r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--set", set_word(rb, value(rb, 7)),
                       "--until-idle"});
    EXPECT_TRUE(r.at("deltas") == 1 && r.at("erases") == 0 && r.at("seq") == 10)
        << "after a boot the other slot's lack is known: " << r.text();
}

// A container of the previous minor takes no frame: the first save into its slot is written whole, at minor 1,
// and the save after the next goes as a frame into it (#1009's old-format read).
TEST_P(NvmBoth, previous_minor_written_whole_first) {
    Files f = fx().files({{"a5.bin", "golden@5"}, {"b6.bin", "golden@6"}});
    const unsigned rb = bind_rid();
    const Result r = go(port(), f,
                        concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--dump-slot-a",
                                       "a1.bin", "--set", set_word(rb, value(rb, 8)), "--until-idle", "--dump-slot-b",
                                       "b1.bin", "--set", set_word(rb, value(rb, 9)), "--until-idle", "--dump-slot-a",
                                       "a2.bin"}));
    EXPECT_TRUE(r.at("ok") == 3 && r.at("deltas") == 1 && r.at("erases") == 2) << "two whole, one frame: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a1.bin"], fx().blob("bind7@7/minor1"))) << "slot A is not written whole";
    EXPECT_TRUE(slot_holds(f.blobs["b1.bin"], fx().blob("bind8@8/minor1"))) << "slot B is not written whole";
    EXPECT_TRUE(slot_holds(f.blobs["a2.bin"], with_frames(fx().blob("bind7@7/minor1"), {"kld/bind9@9"})))
        << "the third save is not a frame into slot A";
}

// What ends a slot's frames at boot, and what the next save then does.
TEST_P(NvmBoth, chain_ends) {
    struct Case {
        const char* image;
        long long vd_a;
        long long seq_a;
        long long auth;
        long long next_erases;  // the next save: 0 a frame, 1 written whole
        const char* state;
    };
    const Case cases[] = {
        {"slot/g5+torn", NVM_VD_OK, 5, 1, 1, "golden"},     // a frame cut short: the slot takes no frame
        {"slot/g5+prev4", NVM_VD_OK, 5, 1, 1, "golden"},    // a frame after another sequence
        {"slot/g5+long", NVM_VD_OK, 5, 1, 1, "golden"},     // a span past the record area
        {"slot/g5+lowoff", NVM_VD_OK, 5, 1, 1, "golden"},   // a span inside the container's header
        {"slot/g5+b7+torn", NVM_VD_OK, 7, 0, 0, "bind7"},   // the first frame stands, the second cut short
        {"slot/g5+badrec", NVM_VD_REC, 0, 1, 1, "golden"},  // a frame whose CRC closes over a refused record
        {"slot/g5+badcrc", NVM_VD_CRC, 0, 1, 1, "golden"},  // a frame whose result's CRC does not close
        {"slot/g5+e9", NVM_VD_OK, 9, 0, 0, "golden"},       // a later frame of nothing: the areas are the same
        {"slot/g5+b9", NVM_VD_OK, 9, 0, 0, "bind9"},        // the other slot not the one before: its lack read
        {"slot/g5+older", NVM_VD_OK, 5, 1, 1, "golden"},    // a frame whose sequence is not newer
        {"slot/g5+highoff", NVM_VD_OK, 5, 1, 1, "golden"},  // a span starting past the record area
        {"slot/g5+magic", NVM_VD_OK, 5, 1, 1, "golden"},    // another kind of frame
        {"slot/g5+bigroom", NVM_VD_OK, fx().num("bigroom_seq"), 0, 0, "golden"},  // a frame past the room left
        {"slot/g5+brim", NVM_VD_OK, fx().num("brim_seq"), 0, 0, "golden"},        // frames to the room's last byte
    };
    const unsigned rb = bind_rid();
    for (const Case& c : cases) {
        Files f = fx().files({{"a5.bin", c.image}, {"b6.bin", "golden@6/minor1"}});
        const Result b = go(port(), f, concat(kTwin, {"--boot", "--dump-state", "st"}));
        EXPECT_TRUE(b.at("vd_a") == c.vd_a && (c.vd_a != NVM_VD_OK || b.at("seq_a") == c.seq_a) &&
                    b.at("auth") == c.auth && b.at("unread") == 0 && b.at("phase") == NVM_P_IDLE)
            << c.image << ": " << b.text();
        expect_state(f, "st", fx().payloads(c.state), c.image);
        const Result r = go(port(), f,
                            concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 8)), "--until-idle"},
                                                 kDump)));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("erases") == c.next_erases && r.at("deltas") == 1 - c.next_erases)
            << c.image << ": the next save: " << r.text();
        boot_dumped(port(), f);
        expect_state(f, "st", fx().payloads("bind8"), c.image);
    }
}

// What the other slot lacks is read at boot off its container: the records where it differs from the chosen slot's
// state, and its own frames' span, which its container does not show. The next save is a frame of that and its own,
// and boots the new state: a binding the chosen slot's last commit changed, carried with the new one; a binding the
// other slot's own frame changed, carried back by a console commit of nothing.
TEST_P(NvmBoth, lag_read_at_boot) {
    const unsigned rb = bind_rid();
    struct Case {
        const char* a;
        const char* b;
        std::vector<std::string> change;
        Payloads want;
    };
    const Case cases[] = {
        {"golden@5/minor1", "bind8@8/minor1", {"--set", set_word(rb, value(rb, 9))},
         with(fx().payloads("golden"), {{rb, value(rb, 9)}})},
        {"slot/g5+b7", "golden@8/minor1", {"--commit"}, fx().payloads("golden")}};
    for (const Case& c : cases) {
        Files f = fx().files({{"a5.bin", c.a}, {"b6.bin", c.b}});
        const Result r = go(port(), f, concat(kTwin, concat(concat({"--boot"}, c.change), concat({"--until-idle"}, kDump))));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 1 && r.at("erases") == 0) << c.a << ": " << r.text();
        const Result b = boot_dumped(port(), f);
        EXPECT_TRUE(b.at("vd_a") == NVM_VD_OK && b.at("auth") == 0 && b.at("seq") == 9) << c.a << ": " << b.text();
        expect_state(f, "st", c.want, c.a);
    }
}

// What the other slot lacks, not known at boot, makes the next save a whole one: the slot is blank, or its header
// differs from the chosen one's past the sequence (a container of the previous minor chosen). The change is the
// first record's, next to the header, so a frame taken for the header would fit any shape's buffer.
TEST_P(NvmBoth, lag_unknown_written_whole) {
    const unsigned rb = bind_rid();
    const unsigned first = rids().front();
    struct Case {
        std::pair<const char*, const char*> slots;
        unsigned rid;
        long long seq;  // the commit's: the chosen slot's next
    };
    const Case cases[] = {{{"erased@0", "bind8@8/minor1"}, rb, 9}, {{"golden@5/minor1", "golden@6"}, first, 7}};
    for (const auto& [slots, rid, seq] : cases) {
        Files f = fx().files({{"a5.bin", slots.first}, {"b6.bin", slots.second}});
        const Result r = go(port(), f,
                            concat(kTwin, concat({"--boot", "--set", set_word(rid, value(rid, 9)), "--until-idle"},
                                                 kDump)));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 0 && r.at("erases") == 1) << slots.first << ": " << r.text();
        const Result b = boot_dumped(port(), f);
        EXPECT_TRUE(b.at("vd_a") == NVM_VD_OK && b.at("auth") == 0 && b.at("seq") == seq)
            << slots.first << ": " << b.text();
        expect_state(f, "st", with(fx().payloads("golden"), {{rid, value(rid, 9)}}),
                     slots.first);
    }
}

// The boot's read of the other slot's container stands only on its CRC-32: a read the port fails, of its records or
// of its trailer, or one that returns other bytes, leaves the lag unknown and the next save whole.
TEST_F(NvmModel, boot_lag_read_faults) {
    const auto hex = [](uint32_t v) {
        char s[16];
        std::snprintf(s, sizeof s, "0x%x", static_cast<unsigned>(v));
        return std::string(s);
    };
    const uint32_t area = NVM_SLOT_A + NVM_KLJ_HDR + 100u;
    const uint32_t trailer = NVM_SLOT_A + NVM_IMG_LEN - NVM_KLJ_TRAILER;
    // the slot's judgement reads each byte once; the boot's lag read is the second
    const std::string faults[] = {"read-fail-at:1:1:" + hex(area), "read-fail-at:1:1:" + hex(trailer),
                                  "read-flip-at:1:1:" + hex(area)};
    const unsigned rb = bind_rid();
    for (const std::string& fault : faults) {
        Files f = twin();
        const Result r = go(port(), f,
                            concat(kTwin, concat({"--boot-fault", fault, "--boot", "--set", set_word(rb, value(rb, 7)),
                                                  "--until-idle"},
                                                 kDump)));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 0 && r.at("erases") == 1 && r.at("unread") == 0)
            << fault << ": " << r.text();
        boot_dumped(port(), f);
        expect_state(f, "st", fx().payloads("bind7"), fault);
    }
}

// A frame's span that does not read erased, under an erased header: the save is written whole instead, in the same
// attempt, no failure counted.
TEST_P(NvmBoth, frame_span_not_erased) {
    Files f = fx().files({{"a5.bin", "slot/g5+stray"}, {"b6.bin", "golden@6/minor1"}});
    const unsigned rb = bind_rid();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle"}, kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 0 && r.at("erases") == 1 && r.at("failed") == 0)
        << "written whole: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("bind7@7/minor1"))) << "slot A is not written whole";
}

// A frame that fails, named by its step, leaves its slot taking no frame: the retry writes the save whole. A page
// the part refuses fails its call on the model's port; through LiteSPI the call cannot see it, and the verify does.
TEST_P(NvmBoth, frame_failure_written_whole) {
    const long long refused = port() == Port::Model ? NVM_VD_PROGRAM : NVM_VD_VERIFY;
    const std::pair<const char*, long long> faults[] = {{"program-drop:1", NVM_VD_VERIFY},
                                                        {"program-refuse:1", refused}};
    const unsigned rb = bind_rid();
    for (const auto& [fault, vd] : faults) {
        Files f = twin();
        const std::vector<std::string> head = {"--boot", "--fault", fault, "--set", set_word(rb, value(rb, 7)),
                                               "--run-ms", "1200"};
        Result r = go(port(), f, concat(kTwin, head), {"ls_refused"});
        EXPECT_TRUE(r.at("ok") == 0 && r.at("failed") == 1 && r.at("last") == vd && r.at("stale") == 1)
            << fault << ": the frame's failure: " << r.text();
        r = go(port(), f, concat(kTwin, concat(concat(head, {"--run-ms", "3000", "--until-idle"}), kDump)),
               {"ls_refused"});
        EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 1 && r.at("deltas") == 0 && r.at("erases") == 1 &&
                    r.at("stale") == 0)
            << fault << ": the retry: " << r.text();
        EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("bind7@7/minor1"))) << fault << ": not written whole";
    }
}

// The model's read faults on a frame's blank check and its verify fail that attempt by its step.
TEST_F(NvmModel, frame_read_faults) {
    const std::string at = "0x" + [] {
        char s[16];
        std::snprintf(s, sizeof s, "%x", static_cast<unsigned>(NVM_SLOT_A + NVM_DELTA_BASE));
        return std::string(s);
    }();
    // the boot reads the room's first header twice; the blank check reads it next, then the verify
    const std::pair<std::string, long long> faults[] = {{"read-fail-at:1:2:" + at, NVM_VD_ERASE},
                                                        {"read-fail-at:1:3:" + at, NVM_VD_VERIFY}};
    const unsigned rb = bind_rid();
    for (const auto& [fault, vd] : faults) {
        Files f = twin();
        const std::vector<std::string> head = {"--boot-fault", fault, "--boot", "--set", set_word(rb, value(rb, 7)),
                                               "--run-ms", "1200"};
        Result r = go(port(), f, concat(kTwin, head));
        EXPECT_TRUE(r.at("ok") == 0 && r.at("failed") == 1 && r.at("last") == vd) << fault << ": " << r.text();
        r = go(port(), f, concat(kTwin, concat(head, {"--run-ms", "3000", "--until-idle"})));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("failed") == 1 && r.at("erases") == 1) << fault << ": " << r.text();
    }
}

// What ends a slot's frames stands only on a second read of the same bytes: an erased header, a header refused, or a
// frame cut short, each read differently every time, leaves the slot UNREAD and the writer held (#665 decision 2).
TEST_F(NvmModel, chain_end_reads_twice) {
    char at[16];
    std::snprintf(at, sizeof at, "%x", static_cast<unsigned>(NVM_SLOT_A + NVM_DELTA_BASE + 2u));
    char in_frame[16];
    std::snprintf(in_frame, sizeof in_frame, "%x", static_cast<unsigned>(NVM_SLOT_A + NVM_DELTA_BASE + 40u));
    char trailer[16];
    std::snprintf(trailer, sizeof trailer, "%x", static_cast<unsigned>(NVM_SLOT_A + NVM_DELTA_BASE + 60u));
    // a binding frame is 64 bytes: the header, its span (the binding record's frame) from 28, the pad, the trailer
    // at 60
    const std::pair<const char*, std::string> cases[] = {
        {"golden@5/minor1", std::string("read-vary-at:999:0:0x") + at},   // an erased header, read two ways
        {"slot/g5+prev4", std::string("read-vary-at:999:0:0x") + at},     // a refused header, read two ways
        {"slot/g5+torn", std::string("read-vary-at:999:0:0x") + in_frame}, // a frame cut short, two CRCs
        {"golden@5/minor1", std::string("read-fail-at:999:0:0x") + at},   // the header read fails
        {"slot/g5+torn", std::string("read-fail-at:999:1:0x") + in_frame}, // the second CRC's read fails
        {"slot/g5+b7", std::string("read-fail-at:999:0:0x") + in_frame},   // the CRC's read fails
        {"slot/g5+b7", std::string("read-fail-at:999:0:0x") + trailer},    // the trailer's read fails
        {"slot/g5+b7", std::string("read-fail-at:999:1:0x") + in_frame},   // the span's read fails
        {"golden@5/minor1", std::string("read-fail-at:999:1:0x") + at}};  // the header's second read fails
    for (const auto& [image, fault] : cases) {
        Files f = fx().files({{"a5.bin", image}, {"b6.bin", "golden@6/minor1"}});
        const Result r = go(port(), f, concat(kTwin, {"--boot-fault", fault, "--boot"}));
        EXPECT_TRUE(r.at("unread") == 1 && r.at("vd_a") == NVM_VD_LEN && r.at("auth") == 1 &&
                    r.at("phase") == NVM_P_HELD)
            << image << " " << fault << ": " << r.text();
    }
}

// The chosen slot's frames read again at its re-stage: the re-stage applies them, so the state staged is the
// frame's; a re-stage whose frame cannot be read, every time, leaves it UNREAD, and the other slot is offered (#665
// decision 2).
TEST_F(NvmModel, restage_reads_frames) {
    char in_frame[16];
    std::snprintf(in_frame, sizeof in_frame, "%x", static_cast<unsigned>(NVM_SLOT_A + NVM_DELTA_BASE + 40u));
    Files f = fx().files({{"a5.bin", "slot/g5+b7"}, {"b6.bin", "golden@6/minor1"}});
    const Result ok = go(port(), f, concat(kTwin, {"--boot", "--dump-state", "st"}));
    EXPECT_TRUE(ok.at("auth") == 0 && ok.at("seq") == 7 && ok.at("unread") == 0 && ok.at("phase") == NVM_P_IDLE)
        << "the re-stage applies the frame: " << ok.text();
    expect_state(f, "st", fx().payloads("bind7"), "the re-staged frame");
    // the judgement reads the frame's byte 40 twice, its CRC and its span; the re-stage's CRC read is the third
    const Result r = go(port(), f,
                        concat(kTwin, {"--boot-fault", std::string("read-fail-at:999:2:0x") + in_frame, "--boot",
                                       "--dump-state", "st"}));
    EXPECT_TRUE(r.at("auth") == 1 && r.at("unread") == 1 && r.at("cause") == NVM_C_STAGE &&
                r.at("vd_a") == NVM_VD_LEN && r.at("phase") == NVM_P_HELD)
        << "every re-stage of the frame failed: " << r.text();
    expect_state(f, "st", fx().payloads("golden"), "the other slot offered");
}

// Each frame carries what its slot lacks: the other slot's last records with this save's, lower or higher. Two
// adjacent bindings are one span; a shape whose frame buffer cannot hold it writes those saves whole.
TEST_P(NvmBoth, frames_carry_the_lag) {
    Files f = twin();
    const unsigned rb = bind_rid();
    const unsigned rb2 = static_cast<unsigned>(fx().num("bind_rid2"));
    const long long two = NVM_DLEN(2u * (NVM_REC_HDR + plen(rb))) <= NVM_PAYLOAD_MAX ? 1 : 0;
    Result r = go(port(), f,
                  concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--set",
                                        set_word(rb2, value(rb2, 8)), "--until-idle"},
                                       kDump)));
    EXPECT_TRUE(r.at("ok") == 2 && r.at("deltas") == 1 + two && r.at("erases") == 1 - two)
        << "two frames: " << r.text();
    boot_dumped(port(), f);
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 8)}}),
                 "the second frame without the first's record");
    r = go(port(), f,
           {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--set", set_word(rb, value(rb, 9)), "--until-idle",
            "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == two && r.at("erases") == 1 - two) << "a third frame: " << r.text();
    boot_dumped(port(), f);
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 9)}, {rb2, value(rb2, 8)}}),
                 "the third frame without the second's record");
}

// A frame larger than the buffer it is made in, or than the room its slot has left, is not written: the save is
// written whole. The room's lack of space is found with a change waiting, so no whole commit was begun for it.
TEST_P(NvmBoth, frame_too_big_written_whole) {
    const unsigned rb = bind_rid();
    const unsigned last = rids().back();
    Files f = twin();
    Result r = go(port(), f,
                  concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--set", set_word(last, value(last, 7)),
                                 "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 0 && r.at("erases") == 1)
        << "a span past the frame buffer: " << r.text();
    f = fx().files({{"a5.bin", "golden@40/minor1"}, {"b6.bin", "slot/g5+brim"}});
    r = go(port(), f, concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 0 && r.at("erases") == 1 && r.at("tidied") == 0)
        << "a full room: " << r.text();
}

// A slot's frames' room full: once nothing waits, the slot the next save goes to is written whole, and the save
// after it is a frame again. A failed one is not begun again until a commit is verified, and leaves no claim stale.
TEST_P(NvmBoth, full_room_written_whole_idle) {
    const unsigned rb = bind_rid();
    Files f = fx().files({{"a5.bin", "slot/g5+full"}, {"b6.bin", "golden@6/minor1"}});
    Result r = go(port(), f,
                  concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--run-ms", "3000",
                                 "--set", set_word(rb, value(rb, 8)), "--until-idle", "--boot", "--dump-state", "st"}));
    expect_state(f, "st", fx().payloads("bind8"), "after the room was written whole");
    r = go(port(), f,
           concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--run-ms", "3000", "--set",
                          set_word(rb, value(rb, 8)), "--until-idle"}));
    EXPECT_TRUE(r.at("ok") == 3 && r.at("tidied") == 1 && r.at("deltas") == 2 && r.at("erases") == 1)
        << "a frame, the full slot whole, a frame: " << r.text();
    r = go(port(), f,
           concat(kTwin, {"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--fault", "erase-refuse:1",
                          "--run-ms", "3000", "--set", set_word(rb, value(rb, 8)), "--until-idle", "--run-ms", "3000"}),
           {"ls_refused"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("tidied") == 1 && r.at("failed") == 1 && r.at("stale") == 0 &&
                r.at("attempts") == 0 && r.at("erases") == 1)
        << "a failed one, then the next save written whole: " << r.text();
}

// A console commit of nothing goes as a frame of an empty span; a record the stage still holds erased goes as its
// erased bytes.
TEST_P(NvmBoth, frame_of_nothing) {
    Files f = twin();
    Result r = go(port(), f, concat(kTwin, concat({"--boot", "--commit"}, kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 1 && r.at("erases") == 0) << "a frame of nothing: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], with_frames(fx().blob("golden@5/minor1"), {"kld/empty@7"})))
        << "slot A is not its container and an empty frame";
    f = fx().files({{"a5.bin", "erased@5/minor1"}, {"b6.bin", "erased@6/minor1"}});
    r = go(port(), f, concat(kTwin, concat({"--boot", "--touch", num(bind_rid()), "--commit"}, kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("deltas") == 1) << "an erased record touched: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], with_frames(fx().blob("erased@5/minor1"), {"kld/erased@7"})))
        << "slot A's frame holds an erased record";
}

// A delta frame torn by a power cut inside its page program, a quarter, half or all but the last of its bytes
// landed: its slot's container is untouched, the boot ends that slot's frames at the torn one, and the old binding
// boots from the other slot. The torn slot then takes no frame: its next save is written whole and boots back.
TEST_P(NvmBoth, torn_frame) {
    const unsigned rb = bind_rid();
    const std::size_t room = static_cast<std::size_t>(fx().num("delta_base"));
    for (const unsigned frac : {64u, 128u, 255u}) {
        Files f = twin();
        const std::string what = "cut at " + num(frac) + "/256 of the frame's page";
        Result r = go(port(), f,
                      concat(kTwin, concat({"--boot", "--cut-at", "1:" + num(frac), "--set", set_word(rb, value(rb, 7)),
                                            "--run-ms", "1500"},
                                           kDump)));
        EXPECT_TRUE(r.at("erases") == 0 && r.at("programs") == 1 && r.at("ok") == 0) << what << ": " << r.text();
        const Bytes& a = f.blobs["a.bin"];
        Bytes base = fx().blob("golden@5/minor1");
        base.resize(room, 0xffu);
        EXPECT_TRUE(a.size() > room && a[room] != 0xffu &&
                    Bytes(a.begin(), a.begin() + static_cast<std::ptrdiff_t>(room)) == base)
            << what << ": slot A is not its container and a torn frame after it";
        const Result b = boot_dumped(port(), f);
        EXPECT_TRUE(b.at("vd_a") == NVM_VD_OK && b.at("seq_a") == 5 && b.at("auth") == 1 && b.at("seq") == 6 &&
                    b.at("unread") == 0 && b.at("phase") == NVM_P_IDLE)
            << what << ": " << b.text();
        expect_state(f, "st", fx().payloads("golden"), what);
        r = go(port(), f, concat({"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--set",
                                  set_word(rb, value(rb, 8)), "--until-idle"},
                                 kDump));
        EXPECT_TRUE(r.at("ok") == 1 && r.at("erases") == 1 && r.at("deltas") == 0) << what << ": " << r.text();
        boot_dumped(port(), f);
        expect_state(f, "st", fx().payloads("bind8"), what + ", then the next save");
    }
}

// A full delta area: frames to its room's last byte boot as their last one, and the next save into that slot is
// written whole, whatever waits; the save after it is a frame again, into the other slot.
TEST_P(NvmBoth, full_delta_area) {
    const unsigned rb = bind_rid();
    Files f = fx().files({{"a5.bin", "golden@40/minor1"}, {"b6.bin", "slot/g5+brim"}});
    Result r = go(port(), f, concat(kTwin, {"--boot", "--dump-state", "st"}));
    EXPECT_TRUE(r.at("vd_b") == NVM_VD_OK && r.at("seq_b") == fx().num("brim_seq") && r.at("auth") == 0)
        << "the full slot's boot: " << r.text();
    expect_state(f, "st", fx().payloads("golden"), "the full slot");
    r = go(port(), f, concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle"}, kDump)));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("erases") == 1 && r.at("deltas") == 0 && r.at("tidied") == 0)
        << "the save into the full slot: " << r.text();
    Result b = boot_dumped(port(), f);
    EXPECT_TRUE(b.at("auth") == 1 && b.at("seq") == 0x41) << b.text();
    expect_state(f, "st", fx().payloads("bind7"), "the full slot written whole");
    r = go(port(), f, concat({"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--set", set_word(rb, value(rb, 8)),
                              "--until-idle"},
                             kDump));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("erases") == 0 && r.at("deltas") == 1) << "the save after: " << r.text();
    b = boot_dumped(port(), f);
    EXPECT_TRUE(b.at("auth") == 0 && b.at("seq") == 0x42) << b.text();
    expect_state(f, "st", fx().payloads("bind8"), "a frame again");
}

// A store the 2509db68 image wrote: both slots as its own store left them in the save harness, at the minor before
// frames (data/2509db68). The boot reads both and restores the newer one's state; the first save into each slot is
// written whole, at minor 1, and the save after both is a frame. A shape no such store was written for has none.
TEST_P(NvmBoth, store_of_2509db68) {
    if (fx().num("old_store") == 0) {
        return;
    }
    const unsigned rb = bind_rid();
    const long long newer = (fx().num("old_seq_b") - fx().num("old_seq_a")) % (1LL << 32) < (1LL << 31) ? 1 : 0;
    const long long seq = newer ? fx().num("old_seq_b") : fx().num("old_seq_a");
    Files f = fx().files({{"a5.bin", "old/a"}, {"b6.bin", "old/b"}});
    Result r = go(port(), f, concat(kTwin, {"--boot", "--dump-state", "st"}));
    EXPECT_TRUE(r.at("vd_a") == NVM_VD_OK && r.at("vd_b") == NVM_VD_OK && r.at("seq_a") == fx().num("old_seq_a") &&
                r.at("seq_b") == fx().num("old_seq_b") && r.at("auth") == newer && r.at("terminal") == NVM_T_COMPLETE &&
                r.at("phase") == NVM_P_IDLE)
        << "the old store's boot: " << r.text();
    expect_state(f, "st", fx().payloads("old"), "the old store's boot");
    r = go(port(), f,
           concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--set",
                                 set_word(rb, value(rb, 8)), "--until-idle", "--set", set_word(rb, value(rb, 9)),
                                 "--until-idle"},
                                kDump)));
    EXPECT_TRUE(r.at("ok") == 3 && r.at("erases") == 2 && r.at("deltas") == 1 && r.at("seq") == seq + 3)
        << "two whole, then a frame: " << r.text();
    const Result b = boot_dumped(port(), f);
    // the saves alternate: the older slot, the newer, the older again
    EXPECT_TRUE(b.at("seq") == seq + 3 && b.at("auth") == 1 - newer && b.at("terminal") == NVM_T_COMPLETE) << b.text();
    expect_state(f, "st", with(fx().payloads("old"), {{rb, value(rb, 9)}}), "the old store after three saves");
}

// #1009's acceptance: the power cut every 10 ms from a binding change to 3 s after it, and inside each of its
// save's media effects, with the part's erase and page times; every cut boots the old binding or the new one, never
// neither and never a mix, and the next change commits. Once as a frame, once written whole.
TEST_P(NvmBoth, swept_cut) {
    const std::pair<std::pair<const char*, const char*>, long long> cases[] = {
        {{"golden@5/minor1", "golden@6/minor1"}, 1}, {{"golden@5", "golden@6"}, 0}};
    for (const auto& [slots, delta] : cases) {
        Files f = fx().files({{"a5.bin", slots.first}, {"b6.bin", slots.second}});
        const Result r = go(port(), f, concat(kTwin, {"--times", "150:500", "--sweep-cut", "10"}));
        const auto at = [&r](const char* k) { return r.sweep.count(k) != 0u ? r.sweep.at(k) : -1; };
        EXPECT_TRUE(at("bad") == 0 && at("cases") >= 301 && at("old") > 0 && at("new") > 0 && at("delta") == delta)
            << slots.first << ": cases " << at("cases") << " old " << at("old") << " new " << at("new") << " bad "
            << at("bad") << " effects " << at("effects") << " durable " << at("durable_us") << " us; "
            << r.text();
        for (const std::string& line : r.fails) {
            ADD_FAILURE() << line;
        }
    }
}

}  // namespace
}  // namespace nvm_test
