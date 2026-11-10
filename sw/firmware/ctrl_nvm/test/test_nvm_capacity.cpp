// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_capacity.cpp - the layout 3 NAME block at its capacity (#823
// decision 1, scope item 4; GoogleTest). Built only at the shipping 1x1
// shape, with its writable names raised to the NAME block's capacity as
// nvm_layout3.h declares it, so the shape's last name is the block's last
// id. Every byte is the capacity fixture's (nvm_fixture.py
// write_capacity_fixture, from scripts/nvm_klj3.py).
//
//   name_block_ends      the first name is the block's first id, the last
//                        name its last, and no record lies one past it;
//   capacity_round_trip  every record committed, byte for byte as the
//                        reference, across two erase blocks, and booted back;
//   capacity_commit_over_stale  a commit into a slot holding an older
//                        container in every block it spans: each erase at its
//                        block's address, and the reference's bytes;
//   one_past_refused     a record one past the block is refused VD_REC.
//
// One past the capacity does not build: nvm_shape.h refuses it at compile
// time, and test_ctrl_nvm.py holds that refusal.

#include <gtest/gtest.h>

#include <cstdint>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

FW_TALLY_LABEL("ctrl_nvm saved-state store, layout 3 NAME capacity (" NVM_TALLY_SHAPE ")");

namespace nvm_test {
namespace {

TEST(NvmCapacity, name_block_ends) {
    const std::vector<long long>& ids = fx().list("name_ids");
    ASSERT_EQ(ids.size(), 2u) << "the fixture names the first and last name ids";
    EXPECT_EQ(fx().num("n_names"), static_cast<long long>(NVM3_CAP_NAME)) << "the build is not at capacity";
    const nvm_rec first = nvm_rec_of(NVM_G_NAME, 0);
    const nvm_rec last = nvm_rec_of(NVM_G_NAME, MILAN_NVM3_N_NAME - 1u);
    EXPECT_TRUE(first.ok && first.id == ids[0] && ids[0] == fx().num("name_block_first"))
        << "the first name is id " << unsigned{first.id} << "; the reference's " << ids[0]
        << ", the block's first " << fx().num("name_block_first");
    EXPECT_TRUE(last.ok && last.id == ids[1] && ids[1] == fx().num("name_block_last"))
        << "the last name is id " << unsigned{last.id} << "; the reference's " << ids[1] << ", the block's last "
        << fx().num("name_block_last");
    EXPECT_FALSE(nvm_rec_of(NVM_G_NAME, MILAN_NVM3_N_NAME).ok) << "a name past the capacity has a record";
    EXPECT_FALSE(nvm_rec_by_id(static_cast<unsigned>(fx().num("id_space"))).ok)
        << "id " << fx().num("id_space") << ", one past the block, has a record";
    EXPECT_TRUE(NVM_N_REC == rids().size() && NVM_IMG_LEN == static_cast<unsigned long long>(fx().num("img_len")))
        << "records " << NVM_N_REC << " of " << rids().size() << ", container " << NVM_IMG_LEN << " of "
        << fx().num("img_len");
    EXPECT_TRUE(nvm_shape_consistent()) << "the record walk and the sizes disagree at capacity";
}

TEST_P(NvmBoth, capacity_round_trip) {
    Files f;
    Result r = go(port(), f, {"--blank", "--boot", "--set-pattern", "0", "--commit", "--dump-slot-a", "a.bin"});
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 1 && r.at("auth") == 0 && r.at("compactions") == 1 &&
                r.at("erases") == 0 && NVM_ERASE_BLOCKS > 1u && r.at("programs") == pages())
        << "the commit at capacity: " << r.text();
    EXPECT_TRUE(slot_holds(f.blobs["a.bin"], fx().blob("golden@1")))
        << "the container at capacity differs from nvm_klj3.py's";
    r = go(port(), f, {"--slot-a", "a.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("applied") == static_cast<long long>(rids().size()))
        << "the boot at capacity: " << r.text();
    expect_state(f, "st", fx().payloads("golden"));
}

// The background preparation over a slot that is not blank, at capacity: a
// stale container in slot B spans two erase blocks, and each is erased in
// turn, then a compaction lands on it; then slot A, the old one, is erased
// the same way. Every erase is of the block its check found written, the
// addresses read from the flash map by the fixture, and the base the
// compaction writes over the stale one is the reference's, byte for byte.
TEST_P(NvmBoth, capacity_commit_over_stale) {
    Files f = fx().files({{"a.bin", "golden@1"}, {"b.bin", "golden@0"}});
    const Result r = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--protect-auth", "--commit",
                                    "--dump-slot-a", "a1.bin", "--dump-slot-b", "b1.bin"});
    const long long blocks = static_cast<long long>(NVM_ERASE_BLOCKS);
    ASSERT_TRUE(r.at("compactions") == 1 && r.at("failed") == 0 && r.at("seq") == 1 && r.at("auth") == 1 &&
                blocks > 1 && r.at("erases") == 2 * blocks && r.erase_at.size() == static_cast<std::size_t>(2 * blocks))
        << "a compaction over a stale slot at capacity: " << r.text();
    for (long long n = 0; n < 2 * blocks; ++n) {
        const long long slot = fx().num(n < blocks ? "journal_b" : "journal_a");
        const long long want = slot + (n % blocks) * fx().num("erase_block");
        EXPECT_EQ(static_cast<long long>(r.erase_at[static_cast<std::size_t>(n)]), want)
            << "erase " << n << (n < blocks ? " of slot B's preparation" : " of slot A's");
    }
    EXPECT_TRUE(slot_holds(f.blobs["b1.bin"], fx().blob("golden@1")))
        << "the base over the stale container differs from nvm_klj3.py's";
    EXPECT_TRUE(f.blobs["a1.bin"] == padded(Bytes{})) << "the old slot is not erased";
}

TEST(NvmCapacity, one_past_refused) {
    const Bytes& blob = fx().blob("one_past@1");
    ASSERT_GT(blob.size(), static_cast<std::size_t>(NVM_KLJ_MIN));
    EXPECT_TRUE(nvm_klj2_check(blob.data(), static_cast<std::uint32_t>(blob.size())) == NVM_VD_REC &&
                fx().num("one_past_verdict") == NVM_VD_REC)
        << "a record one past the NAME block: codec " << nvm_klj2_check(blob.data(), static_cast<std::uint32_t>(blob.size()))
        << ", klj3_decode " << fx().num("one_past_verdict");
}

}  // namespace
}  // namespace nvm_test
