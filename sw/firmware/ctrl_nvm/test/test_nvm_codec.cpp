// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_codec.cpp - the KLJ2 codec itself (nvm_klj2.c), asked directly
// (#665 lane FT): every refusal of the parity table and every one the
// fixture crafts for a test of the acceptance order the table does not
// reach, each held to klj2_decode's verdict on the same bytes; the room a
// container is held in; a loaded prefix that ends before a record header;
// and the record lookups' answers for a record the shape does not have.

#include <gtest/gtest.h>

#include <cstdint>
#include <string>
#include <vector>

#include "nvm_c.hpp"
#include "nvm_suite.hpp"

namespace nvm_test {
namespace {

// The verdict the store's boot read takes of `blob`: the whole order over a
// container held in a slot, or (staged) the record walk over the first
// NVM_STAGE_BYTES of a container longer than the stage, as nvm_slot_read
// asks it after streaming the CRC.
long long codec_verdict(const Bytes& blob, bool staged) {
    if (blob.size() < NVM_KLJ2_HDR) {
        return -1;
    }
    if (staged) {
        return nvm_klj2_check_body(blob.data(), nvm_rd32le(blob.data() + 16), NVM_STAGE_BYTES);
    }
    return nvm_klj2_check(blob.data(), static_cast<std::uint32_t>(blob.size()));
}

TEST(NvmCodec, codec_parity) {
    const std::vector<long long>& parity = fx().list("parity_verdicts");
    for (std::size_t n = 0; n < parity.size(); ++n) {
        const Bytes& blob = fx().blob("parity/" + std::to_string(n));
        if (blob.size() > NVM_SLOT_BYTES) {
            continue;  // no slot holds it; the store refuses it unread (verdict_parity)
        }
        EXPECT_EQ(codec_verdict(blob, false), parity[n])
            << "parity: " << fx().text("parity_label/" + std::to_string(n)) << ": codec " << codec_verdict(blob, false)
            << ", klj2_decode " << parity[n];
    }
    const std::vector<long long>& verdicts = fx().list("codec_verdicts");
    const std::vector<long long>& staged = fx().list("codec_staged");
    ASSERT_EQ(verdicts.size(), staged.size());
    for (std::size_t n = 0; n < verdicts.size(); ++n) {
        const long long got = codec_verdict(fx().blob("codec/" + std::to_string(n)), staged[n] != 0);
        EXPECT_EQ(got, verdicts[n]) << "codec: " << fx().text("codec_label/" + std::to_string(n)) << ": codec " << got
                                    << ", klj2_decode " << verdicts[n];
    }
}

// A container longer than the room it is held in is refused VD_LEN before
// its CRC is read past that room.
TEST(NvmCodec, codec_room) {
    const Bytes& golden = fx().blob("golden@5");
    ASSERT_GT(golden.size(), 0u);
    EXPECT_EQ(nvm_klj2_check(golden.data(), static_cast<std::uint32_t>(golden.size()) - 1u), NVM_VD_LEN)
        << "a container one byte longer than its room is refused VD_LEN";
    EXPECT_EQ(nvm_klj2_check(golden.data(), static_cast<std::uint32_t>(golden.size())), NVM_VD_OK)
        << "and accepted in a room of its own length";
}

// nvm_klj2.h lets a caller judge a CRC-closed container with only its first
// `loaded` bytes at hand, whatever the store loads. A prefix that ends before
// a record header is refused VD_REC: the blank container's container header
// alone, and its first record header one byte short; then, before every
// record of a container of frames, its header one byte short, and its header
// whole with its payload not loaded. Each buffer holds the whole container,
// so a walk that read past the prefix would find valid bytes there, and the
// blank one's erased records would be accepted (#665 FT, R507-1-F1).
TEST(NvmCodec, codec_loaded_prefix) {
    std::vector<std::uint8_t> blank(NVM_IMG_LEN);
    nvm_klj2_blank(blank.data());
    ASSERT_EQ(nvm_klj2_check(blank.data(), NVM_IMG_LEN), NVM_VD_OK) << "the blank container is CRC-closed";
    EXPECT_EQ(nvm_klj2_check_body(blank.data(), NVM_IMG_LEN, NVM_KLJ2_HDR), NVM_VD_REC)
        << "a prefix of the container header alone is refused VD_REC";
    EXPECT_EQ(nvm_klj2_check_body(blank.data(), NVM_IMG_LEN, NVM_KLJ2_HDR + NVM_REC_HDR - 1u), NVM_VD_REC)
        << "a prefix one byte short of the first record header is refused VD_REC";
    const Bytes& frames = fx().blob("golden@5");
    const auto len = static_cast<std::uint32_t>(frames.size());
    ASSERT_EQ(nvm_klj2_check(frames.data(), len), NVM_VD_OK) << "the container of frames is CRC-closed";
    for (nvm_rec r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
        const std::uint32_t header = NVM_KLJ2_HDR + r.off;
        EXPECT_EQ(nvm_klj2_check_body(frames.data(), len, header + NVM_REC_HDR - 1u), NVM_VD_REC)
            << "a prefix one byte short of record " << unsigned{r.id} << "'s header is refused VD_REC";
        if (r.plen != 0u) {
            EXPECT_EQ(nvm_klj2_check_body(frames.data(), len, header + NVM_REC_HDR), NVM_VD_REC)
                << "a prefix holding record " << unsigned{r.id} << "'s header but not its payload is refused VD_REC";
        }
    }
    EXPECT_EQ(nvm_klj2_check_body(frames.data(), len, len), NVM_VD_OK) << "and the whole container is accepted";
}

// The lookups answer "no record" for a group or an index the shape does not
// have, and for an id outside the shape.
TEST(NvmCodec, codec_lookups) {
    EXPECT_EQ(nvm_rec_of(NVM_G_COUNT, 0).ok, 0u) << "no record of a group past the last";
    EXPECT_EQ(nvm_rec_of(NVM_G_CFG, 1).ok, 0u) << "no record past a group's count";
    EXPECT_EQ(nvm_rec_by_id(0xFFu).ok, 0u) << "no record of an id the shape does not use";
    EXPECT_EQ(nvm_rec_after(0xFF).ok, 0u) << "no record after the last id";
    const nvm_rec first = nvm_rec_first();
    EXPECT_TRUE(first.ok && nvm_rec_of(first.group, first.index).id == first.id)
        << "and the first record is found by its group and index";
}

}  // namespace
}  // namespace nvm_test
