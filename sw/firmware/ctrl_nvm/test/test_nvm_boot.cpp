// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_boot.cpp - the boot path of the saved-state store (#665 lanes F1
// and FT; GoogleTest): valid, absent, torn, corrupted and wrong-version
// slots, read faults at every boot read, and the binding and D3 restore walks.
//
// One test per check of the hand-rolled suite this replaces
// (nvm_checks.py until #665 FT), under the check's own name, so
// nvm_mutants.py names the test that must fail on each planted defect. Every
// image is the fixture's (nvm_fixture.py, from scripts/nvm_klj2.py).

#include <gtest/gtest.h>

#include <array>
#include <string>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

// The tally of this binary, the boot and write paths (test_nvm_write.cpp).
FW_TALLY_LABEL("ctrl_nvm saved-state store, boot and write paths (" NVM_TALLY_SHAPE ")");

namespace nvm_test {
namespace {

std::string hex(unsigned long long v) {
    char buf[24];
    std::snprintf(buf, sizeof buf, "%llx", v);
    return buf;
}

// A blank board boots BLANK, releases AECP once, applies nothing, and stages
// the all-erased container the Python encoder writes.
TEST_P(NvmBoth, blank_boot) {
    Files f;
    const Result r = go(port(), f, {"--blank", "--boot", "--dump-stage", "stage.bin"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_BLANK && r.at("vd_a") == NVM_VD_BLANK && r.at("vd_b") == NVM_VD_BLANK &&
                r.at("releases") == 1 && r.at("sm_releases") == 1 && r.at("sm_applies") == 0 && r.at("auth") == -1 &&
                r.at("phase") == 1)
        << "blank boot state: " << r.text();
    EXPECT_TRUE(f.blobs["stage.bin"] == fx().blob("erased@0"))
        << "the staged blank container differs from nvm_klj2.py's";
}

// A golden slot is chosen, every record is applied in the D3 order (the
// settle step once, between the maps and the names) and the state equals
// what klj2_decode reads out of the same bytes.
TEST_P(NvmBoth, golden_restore) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f, {"--slot-b", "g.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("auth") == 1 && r.at("seq") == 5 &&
                r.at("vd_a") == NVM_VD_BLANK && r.at("vd_b") == NVM_VD_OK &&
                r.at("applied") == static_cast<long long>(rids().size()) && r.at("refused") == 0 &&
                r.at("blank") == 0 && r.at("sm_settles") == 1 && r.at("releases") == 1)
        << "golden restore state: " << r.text();
    expect_state(f, "st", fx().payloads("golden"));
}

// An erased record applies nothing and keeps its image default; the framed
// ones beside it are applied (section 6.1, the erased-record rule).
TEST_P(NvmBoth, erased_records) {
    Files f = fx().files({{"h.bin", "half@3"}});
    const Result r = go(port(), f, {"--slot-a", "h.bin", "--boot", "--dump-state", "st"});
    const long long n_erased = (static_cast<long long>(rids().size()) + 1) / 2;
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("blank") == n_erased &&
                r.at("applied") == static_cast<long long>(rids().size()) - n_erased)
        << "erased-record counts: " << r.text();
    expect_state(f, "st", fx().payloads("half"));
}

// The newer accepted slot wins, by the wrap-safe compare of section 7, and
// its records are the ones applied; on equal sequences slot A wins (#665
// decision 1, as the shipping writer's nvm_pick_slot), at the wrap too, the
// two slots holding different payloads.
TEST_P(NvmBoth, newer_wins) {
    struct Case {
        unsigned long long seq_a;
        unsigned long long seq_b;
        long long want;
    };
    static constexpr Case kCases[] = {{9, 10, 1}, {10, 9, 0},  {0xFFFFFFFF, 0, 1},
                                      {0, 0xFFFFFFFF, 0}, {7, 7, 0}, {0xFFFFFFFF, 0xFFFFFFFF, 0}};
    for (const Case& c : kCases) {
        Files f = fx().files({{"a.bin", "golden@" + hex(c.seq_a)}, {"b.bin", "changed2b@" + hex(c.seq_b)}});
        const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
        EXPECT_TRUE(r.at("auth") == c.want && r.at("terminal") == NVM_T_COMPLETE)
            << "seq A 0x" << hex(c.seq_a) << " B 0x" << hex(c.seq_b) << ": chose " << r.at("auth") << ", want "
            << c.want;
        expect_state(f, "st", fx().payloads(c.want == 0 ? "golden" : "changed2b"));
    }
}

// A torn newer slot falls back to the older one, whose records apply.
TEST_P(NvmBoth, torn_falls_back) {
    Files f = fx().files({{"a.bin", "golden@9"}, {"b.bin", "golden@a~43"}});
    const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("auth") == 0 && r.at("seq") == 9 && r.at("vd_b") == NVM_VD_CRC &&
                r.at("terminal") == NVM_T_COMPLETE)
        << "torn newer slot: " << r.text();
    expect_state(f, "st", fx().payloads("golden"));
}

// Two torn slots boot on the defaults, naming the failure.
TEST_P(NvmBoth, both_torn_blank) {
    Files f = fx().files({{"a.bin", "golden@9~49"}, {"b.bin", "golden@a~43"}});
    const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_BLANK && r.at("last") == NVM_VD_CRC && r.at("sm_applies") == 0 &&
                r.at("releases") == 1)
        << "two torn slots: " << r.text();
    expect_state(f, "st", {});
}

// For every section 6.2 refusal, both faces of the erased-record rule and a
// blank slot, the store's verdict equals klj2_decode's for the same bytes
// (the shipping writer suite's table, plus three refusals it does not carry).
TEST_P(NvmBoth, verdict_parity) {
    const std::vector<long long>& verdicts = fx().list("parity_verdicts");
    for (std::size_t n = 0; n < verdicts.size(); ++n) {
        Files f = fx().files({{"p.bin", "parity/" + std::to_string(n)}});
        const Result r = go(port(), f, {"--slot-a", "p.bin", "--boot"});
        EXPECT_EQ(r.at("vd_a"), verdicts[n]) << "parity: " << fx().text("parity_label/" + std::to_string(n))
                                             << ": store " << r.at("vd_a") << ", klj2_decode " << verdicts[n];
    }
}

// A newer slot of another major version is refused VD_VER, never
// reinterpreted, and the older slot is offered.
TEST_P(NvmBoth, wrong_version_falls_back) {
    for (const int major : {1, 3}) {
        Files f = fx().files({{"a.bin", "golden@3"}, {"b.bin", "golden@4/major" + std::to_string(major)}});
        const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot"});
        EXPECT_TRUE(r.at("vd_b") == NVM_VD_VER && r.at("auth") == 0 && r.at("seq") == 3)
            << "major " << major << ": " << r.text();
    }
}

// The chosen slot is read again and judged again in RAM: a bit the read
// flips after the slot was judged is never applied. One flipped re-stage is
// read again and the slot applied; a slot whose NVM_READ_TRIES re-stages all
// flip is UNREAD, the other slot is applied, and the writer is held (#665
// decision 2).
TEST_F(NvmModel, read_flip_at_stage) {
    Files f = fx().files({{"a.bin", "golden@3"}, {"b.bin", "changed41@4"}});
    const std::vector<std::string> slots = {"--slot-a", "a.bin", "--slot-b", "b.bin"};
    // two reads judge each slot (the header, then the container); the fifth
    // read re-stages slot B
    std::vector<std::string> words = slots;
    words.insert(words.end(), {"--boot-fault", "read-flip:1:4", "--boot", "--dump-state", "st"});
    Result r = go(port(), f, words);
    EXPECT_TRUE(r.at("auth") == 1 && r.at("seq") == 4 && r.at("cause") == 0 && r.at("unread") == 0 &&
                r.at("read_faults") == 1 && r.at("phase") == NVM_P_IDLE && r.at("terminal") == NVM_T_COMPLETE)
        << "one flipped re-stage: " << r.text();
    expect_state(f, "st", fx().payloads("changed41"));
    words = slots;
    words.insert(words.end(),
                 {"--boot-fault", "read-flip:" + std::to_string(kReadTries) + ":4", "--boot", "--dump-state", "st"});
    r = go(port(), f, words);
    EXPECT_TRUE(r.at("cause") == NVM_C_STAGE && r.at("auth") == 0 && r.at("seq") == 3 && r.at("vd_b") == NVM_VD_LEN &&
                r.at("unread") == 2 && r.at("phase") == NVM_P_HELD && r.at("terminal") == NVM_T_COMPLETE)
        << "every re-stage flipped: " << r.text();
    expect_state(f, "st", fx().payloads("golden"));
}

//! The sequences slots A and B hold.
using SeqPair = std::array<unsigned long long, 2>;

// The slot the store names is the one applied, under the sequence it holds:
// published SEQ = staged SEQ = that slot's own, and the state is its records.
void consistent(const Files& f, const Result& r, const char* const payloads[2], const SeqPair& seqs,
                const std::string& what) {
    const long long auth = r.at("auth");
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && (auth == 0 || auth == 1)) << what << ": " << r.text();
    if (auth != 0 && auth != 1) {
        return;
    }
    const auto stage = f.blobs.find("stage.bin");
    const long long staged = stage == f.blobs.end() || stage->second.size() < 12u
                                 ? -1
                                 : static_cast<long long>(nvm_rd32le(stage->second.data() + 8));
    EXPECT_TRUE(static_cast<unsigned long long>(r.at("seq")) == seqs[auth] &&
                static_cast<unsigned long long>(staged) == seqs[auth])
        << what << ": slot " << auth << " holds seq 0x" << hex(seqs[auth]) << ", published 0x" << hex(r.at("seq"))
        << ", staged 0x" << hex(staged);
    expect_state(f, "st", fx().payloads(payloads[auth]), what + ": ");
}

// A bit a boot read flips in a slot's sequence word (bit 3 of byte 8: 5
// reads as 13) never selects a slot on that word: on every read that covers
// it, of either slot, across the wrap, the store applies one slot's own
// records under that slot's own sequence, and a flip in the OLDER slot never
// displaces the newer one.
TEST_F(NvmModel, read_flip_boot) {
    static const char* const kPayloads[2] = {"golden", "changed37"};
    static constexpr std::array<SeqPair, 4> kPairs{{{5, 6}, {6, 5}, {0xFFFFFFFF, 0}, {0, 0xFFFFFFFF}}};
    for (const auto& seqs : kPairs) {
        const long long newer = ((seqs[0] - seqs[1]) & 0xFFFFFFFFu) < 0x80000000u ? 0 : 1;
        for (const long long slot : {0LL, 1LL}) {
            const unsigned long long base = slot == 0 ? NVM_SLOT_A : NVM_SLOT_B;
            for (unsigned k = 0; k < 3u; ++k) {
                const std::string what = "seq A 0x" + hex(seqs[0]) + " B 0x" + hex(seqs[1]) + ", flip in slot " +
                                         std::to_string(slot) + " read " + std::to_string(k);
                Files f = fx().files({{"a.bin", "golden@" + hex(seqs[0])}, {"b.bin", "changed37@" + hex(seqs[1])}});
                const Result r = go(port(), f,
                                 {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot-fault",
                                  "read-flip-at:1:" + std::to_string(k) + ":0x" + hex(base + 8u), "--boot",
                                  "--dump-stage", "stage.bin", "--dump-state", "st"});
                consistent(f, r, kPayloads, seqs, what);
                EXPECT_TRUE(slot == newer || r.at("auth") == newer)
                    << what << ": the older slot's flipped word displaced the newer: " << r.text();
            }
        }
    }
}

// The re-stage read of the chosen slot answering from the other slot (an
// address line stuck) is caught by its sequence: the bytes are valid but not
// the chosen slot's. Every re-stage aliased, the slot is UNREAD and the other
// is offered and applied under its own sequence, the writer held; one aliased
// re-stage is read again and the chosen slot applied.
TEST_F(NvmModel, read_alias_at_stage) {
    static const char* const kPayloads[2] = {"golden", "changed37"};
    static constexpr SeqPair kSeqs{6, 5};
    Files f = fx().files({{"a.bin", "golden@6"}, {"b.bin", "changed37@5"}});
    // reads 0-3 judge the two slots; read 4 re-stages slot A
    Result r = go(port(), f,
               {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot-fault",
                "read-alias:" + std::to_string(kReadTries) + ":4", "--boot", "--dump-stage", "stage.bin",
                "--dump-state", "st"});
    consistent(f, r, kPayloads, kSeqs, "every re-stage aliased");
    EXPECT_TRUE(r.at("auth") == 1 && r.at("cause") == NVM_C_STAGE && r.at("vd_a") == NVM_VD_LEN &&
                r.at("unread") == 1 && r.at("phase") == NVM_P_HELD)
        << "every re-stage aliased: " << r.text();
    r = go(port(), f,
           {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot-fault", "read-alias:1:4", "--boot", "--dump-stage",
            "stage.bin", "--dump-state", "st"});
    consistent(f, r, kPayloads, kSeqs, "one aliased re-stage");
    EXPECT_TRUE(r.at("auth") == 0 && r.at("unread") == 0 && r.at("phase") == NVM_P_IDLE)
        << "one aliased re-stage: " << r.text();
}

// A read the port fails is a media fault, never a verdict: the slot is read
// again, NVM_READ_TRIES reads in all. Two failed reads of the newer slot,
// then a good one, and it is applied; its container read failing on every
// try, or its re-stage, and it is UNREAD (VD_LEN, rule 4): the older is
// applied and the writer held (#665 decision 2). One failed re-stage is read
// again.
TEST_F(NvmModel, read_fail_boot) {
    static const char* const kPayloads[2] = {"golden", "changed37"};
    static constexpr SeqPair kSeqs{5, 6};
    struct Case {
        std::string fault;
        long long auth;
        long long cause;
        long long faults;
    };
    // reads 0 and 1 judge slot A, 2 and 3 slot B (its header, then its
    // container); the container's middle covers SLOT_B + 0x100, the header not
    const std::string body = "0x" + hex(NVM_SLOT_B + 0x100u);
    const std::string tries = std::to_string(kReadTries);
    const Case cases[] = {{"read-fail:2:2", 1, 0, 2},
                          {"read-fail-at:" + tries + ":0:" + body, 0, 0, kReadTries},
                          {"read-fail:" + tries + ":4", 0, NVM_C_STAGE, kReadTries},
                          {"read-fail:1:4", 1, 0, 1}};
    for (const Case& c : cases) {
        Files f = fx().files({{"a.bin", "golden@5"}, {"b.bin", "changed37@6"}});
        const Result r = go(port(), f,
                         {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot-fault", c.fault, "--boot", "--dump-stage",
                          "stage.bin", "--dump-state", "st"});
        consistent(f, r, kPayloads, kSeqs, c.fault);
        const bool held = c.auth == 0;
        EXPECT_TRUE(r.at("auth") == c.auth && r.at("cause") == c.cause && r.at("read_faults") == c.faults &&
                    r.at("unread") == (held ? 2 : 0) && r.at("vd_b") == (held ? NVM_VD_LEN : NVM_VD_OK) &&
                    r.at("phase") == (held ? NVM_P_HELD : NVM_P_IDLE))
            << c.fault << ": " << r.text();
    }
}

// The slot offered after the newer fails its re-stage is re-staged and
// judged again too: both re-staged NVM_READ_TRIES times with a bit flipped
// every time, neither is applied. The boot ends BLANK on the defaults with
// both slots UNREAD, so the writer is held and no commit restarts the
// sequence below either.
TEST_F(NvmModel, fallback_restage) {
    const unsigned last = rids().back();
    Files f = fx().files({{"a.bin", "golden@5"}, {"b.bin", "changed37@6"}});
    const Result r = go(port(), f,
                     {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot-fault",
                      "read-flip:" + std::to_string(2 * kReadTries) + ":4", "--boot", "--dump-state", "st", "--set",
                      set_word(last, Bytes(plen(last), 0u)), "--run-ms", "3000", "--commit-try"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_BLANK && r.at("cause") == NVM_C_STAGE && r.at("sm_applies") == 0 &&
                r.at("vd_a") == NVM_VD_LEN && r.at("vd_b") == NVM_VD_LEN && r.at("unread") == 3 &&
                r.at("read_faults") == 2 * kReadTries && r.at("releases") == 1 && r.at("phase") == NVM_P_HELD &&
                r.at("erases") == 0 && r.at("commit_refused") == 1)
        << "both re-stages flipped: " << r.text();
    expect_state(f, "st", {});
}

// Boot a golden slot B under the state-model knobs given.
Result golden_boot(Port port, Files& f, const std::vector<std::string>& knobs) {
    f = fx().files({{"g.bin", "golden@5"}});
    std::vector<std::string> words = {"--slot-b", "g.bin"};
    words.insert(words.end(), knobs.begin(), knobs.end());
    words.insert(words.end(), {"--boot", "--dump-state", "st"});
    return go(port, f, words);
}

// The golden slot's bindings: what a D3 roll-back leaves applied.
Payloads bindings_saved() { return only(fx().payloads("golden"), fx().list("binding_ids"), true); }

// A value rule that cannot be judged aborts the D3 walk and rolls every D3
// value back to its image default: DEFAULTS, AECP released. The binding walk
// ran first and its bindings stay applied (D3 section 8.6).
TEST_P(NvmBoth, apply_fault_rolls_back) {
    const std::vector<long long>& d3 = fx().list("d3_ids");
    Files f;
    const Result r = golden_boot(port(), f, {"--apply-fault", std::to_string(d3[d3.size() / 2])});
    EXPECT_TRUE(r.at("terminal") == NVM_T_DEFAULTS && r.at("cause") == NVM_C_APPLY && r.at("sm_rollbacks") == 1 &&
                r.at("sm_unbinds") == 0 && r.at("bind_terminal") == NVM_T_COMPLETE && r.at("releases") == 1 &&
                r.at("phase") == 1)
        << "apply fault: " << r.text();
    expect_state(f, "st", bindings_saved());
}

// A formats-against-maps judgement that cannot be made rolls the D3 walk
// back too, and leaves the bindings applied.
TEST_P(NvmBoth, settle_fault_rolls_back) {
    Files f;
    const Result r = golden_boot(port(), f, {"--settle-fault"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_DEFAULTS && r.at("cause") == NVM_C_SETTLE && r.at("sm_rollbacks") == 1 &&
                r.at("sm_unbinds") == 0 && r.at("releases") == 1)
        << "settle fault: " << r.text();
    expect_state(f, "st", bindings_saved());
}

// The binding walk is its own unit (D3 section 8.1 step 4, 8.6): a binding
// whose rule cannot be judged fails that walk whole, nothing preloaded, and
// the D3 walk still restores every other record; a walk whose preloads cannot
// be dropped ends CLOSED. The state model polices that every binding precedes
// the D3 walk.
TEST_P(NvmBoth, binding_walk) {
    const std::string last = std::to_string(fx().list("binding_ids").back());
    Files f;
    Result r = golden_boot(port(), f, {"--apply-fault", last});
    EXPECT_TRUE(r.at("bind_terminal") == NVM_T_DEFAULTS && r.at("bind_cause") == NVM_C_APPLY &&
                r.at("sm_unbinds") == 1 && r.at("terminal") == NVM_T_COMPLETE && r.at("sm_rollbacks") == 0 &&
                r.at("releases") == 1)
        << "binding fault: " << r.text();
    expect_state(f, "st", only(fx().payloads("golden"), fx().list("binding_ids"), false));
    r = golden_boot(port(), f, {"--apply-fault", last, "--unbind-fault"});
    EXPECT_TRUE(r.at("bind_terminal") == NVM_T_CLOSED && r.at("terminal") == NVM_T_CLOSED && r.at("releases") == 0 &&
                r.at("phase") == 0)
        << "binding undo fault: " << r.text();
}

// A roll-back that fails ends CLOSED: AECP is never released and the writer
// never runs, so a later change reaches no slot.
TEST_P(NvmBoth, rollback_fault_closes) {
    const unsigned last = rids().back();
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--apply-fault", std::to_string(fx().list("d3_ids")[2]), "--rollback-fault",
                      "--boot", "--set", set_word(last, Bytes(plen(last), 0u)), "--run-ms", "3000"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_CLOSED && r.at("releases") == 0 && r.at("sm_releases") == 0 &&
                r.at("phase") == 0 && r.at("erases") == 0)
        << "rollback fault: " << r.text();
}

// No entity model to judge against (D3 section 8.1 step 6): the binding walk,
// which needs none, has run first (steps 4 and 5) and its bindings stay;
// nothing of the D3 walk is applied, the restore ends CLOSED, AECP is held and
// no writer runs. On blank media too.
TEST_P(NvmBoth, model_unproven_closes) {
    Files f;
    Result r = golden_boot(port(), f, {"--not-ready"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_CLOSED && r.at("cause") == NVM_C_MODEL && r.at("releases") == 0 &&
                r.at("bind_terminal") == NVM_T_COMPLETE &&
                r.at("sm_applies") == static_cast<long long>(fx().list("binding_ids").size()) &&
                r.at("sm_settles") == 0 && r.at("sm_unbinds") == 0 && r.at("phase") == NVM_P_OFF)
        << "unproven model: " << r.text();
    expect_state(f, "st", bindings_saved());
    r = go(port(), f, {"--blank", "--not-ready", "--boot"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_CLOSED && r.at("cause") == NVM_C_MODEL && r.at("releases") == 0 &&
                r.at("sm_applies") == 0 && r.at("phase") == NVM_P_OFF)
        << "unproven model, blank: " << r.text();
}

// A value its rule refuses keeps its image default and the walk goes on to
// apply every later record (section 8.3).
TEST_P(NvmBoth, refused_keeps_default) {
    const std::vector<unsigned> ids = rids();
    const std::vector<long long> refuse = {ids[1], ids[ids.size() / 2]};
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                     {"--slot-b", "g.bin", "--refuse", std::to_string(refuse[0]), "--refuse", std::to_string(refuse[1]),
                      "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("refused") == 2 &&
                r.at("applied") == static_cast<long long>(ids.size()) - 2)
        << "refusals: " << r.text();
    expect_state(f, "st", only(fx().payloads("golden"), refuse, false));
}

}  // namespace
}  // namespace nvm_test
