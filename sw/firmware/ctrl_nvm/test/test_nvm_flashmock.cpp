// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_flashmock.cpp - the boot read's agreement rule (#665 decision 2,
// issue comment 5999350068) on GoogleMock's flash port, which answers each
// read with bytes the test chooses (#665 lane FT). A refusal stands only on
// two reads that returned the same bytes: the same verdict, the same CRC-32
// digest and the same count. The flash model changes one byte the same way
// on every read it faults, so these two cases need a medium no model plays:
//
//   reads_differ_in_verdict          two refusals of different verdicts are
//                                    a media fault, and the read after them
//                                    is judged;
//   reads_agree_in_digest_not_length two refusals alike in verdict and in
//                                    digest, over different byte counts
//                                    (a CRC-32 collision the test forges),
//                                    are a media fault too: the count is
//                                    part of "the same bytes".

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <array>
#include <cstdint>
#include <deque>

#include "mock_nvm_flash.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

namespace nvm_test {
namespace {

using ::testing::_;
using ::testing::AnyNumber;

// CRC-32/ISO-HDLC (reflected 0xEDB88320) as a running register, with its
// table built here: the test's own, never the store's.
const std::array<std::uint32_t, 256>& crc_table() {
    static const std::array<std::uint32_t, 256> table = [] {
        std::array<std::uint32_t, 256> t{};
        for (std::uint32_t i = 0; i < 256u; ++i) {
            std::uint32_t c = i;
            for (int k = 0; k < 8; ++k) {
                c = (c >> 1) ^ (0xEDB88320u & (0u - (c & 1u)));
            }
            t[i] = c;
        }
        return t;
    }();
    return table;
}

std::uint32_t crc_run(std::uint32_t reg, const Bytes& bytes) {
    for (const std::uint8_t b : bytes) {
        reg = (reg >> 8) ^ crc_table()[(reg ^ b) & 0xFFu];
    }
    return reg;
}

// Four bytes that take the register from `from` to `to`: each step's table
// index is fixed by the top byte it must leave, so the indices are found
// backwards and the bytes forwards.
Bytes forge(std::uint32_t from, std::uint32_t to) {
    std::array<std::uint8_t, 256> index_of_top{};
    for (std::uint32_t i = 0; i < 256u; ++i) {
        index_of_top[crc_table()[i] >> 24] = static_cast<std::uint8_t>(i);
    }
    std::array<std::uint8_t, 4> idx{};
    std::uint32_t reg = to;
    for (int k = 3; k >= 0; --k) {
        idx[k] = index_of_top[reg >> 24];
        reg = (reg ^ crc_table()[idx[k]]) << 8;
    }
    Bytes out;
    reg = from;
    for (int k = 0; k < 4; ++k) {
        out.push_back(static_cast<std::uint8_t>((reg ^ idx[k]) & 0xFFu));
        reg = (reg >> 8) ^ crc_table()[idx[k]];
    }
    return out;
}

// Slot A answers each read with the next queued image (its first `len`
// bytes); slot B is blank. Every read is counted.
struct Medium {
    std::deque<Bytes> slot_a;
    unsigned reads_a = 0;

    void serve(MockNvmFlash& flash) {
        EXPECT_CALL(flash, read(_, _, _))
            .Times(AnyNumber())
            .WillRepeatedly([this](std::uint32_t addr, std::uint8_t* dst, std::uint32_t len) {
                const bool a = addr >= NVM_SLOT_A && addr < NVM_SLOT_A + NVM_SLOT_BYTES;
                for (std::uint32_t k = 0; k < len; ++k) {
                    dst[k] = 0xFFu;
                }
                if (a && !slot_a.empty()) {
                    const Bytes image = slot_a.front();
                    slot_a.pop_front();
                    reads_a++;
                    for (std::uint32_t k = 0; k < len && addr - NVM_SLOT_A + k < image.size(); ++k) {
                        dst[k] = image[addr - NVM_SLOT_A + k];
                    }
                }
                return 0;
            });
        EXPECT_CALL(flash, now_us()).Times(AnyNumber());
    }
};

Bytes with_word(Bytes image, std::size_t at, std::uint32_t v) {
    nvm_wr32le(image.data() + at, v);
    return image;
}

TEST(NvmFlashMock, reads_differ_in_verdict) {
    const Bytes& golden = fx().blob("golden@5");
    ASSERT_GT(golden.size(), static_cast<std::size_t>(NVM_KLJ2_HDR));
    MockNvmFlash flash;
    Medium m;
    // a refusal VD_MAGIC, then one VD_VER, then the slot clean: header and
    // container, then the re-stage of the slot chosen
    m.slot_a = {with_word(golden, 0, 0x314A4C4Bu), with_word(golden, 4, 3u << 16), golden, golden, golden};
    m.serve(flash);
    nvm_smodel_reset();
    nvm_store_boot(flash.port(), &nvm_smodel_port);
    const nvm_status* s = nvm_store_status();
    EXPECT_TRUE(s->verdict_a == NVM_VD_OK && s->auth == 0 && s->read_faults == 1u && s->unread == 0u &&
                s->terminal == NVM_T_COMPLETE && m.reads_a == 5u)
        << "two refusals of different verdicts are one media fault, and the clean read after them is applied: "
        << "verdict " << s->verdict_a << ", auth " << s->auth << ", faults " << s->read_faults << ", reads "
        << m.reads_a;
}

TEST(NvmFlashMock, reads_agree_in_digest_not_length) {
    const Bytes& golden = fx().blob("golden@5");
    const std::uint32_t len = static_cast<std::uint32_t>(golden.size());
    ASSERT_GT(len, NVM_KLJ2_MIN + 8u);
    MockNvmFlash flash;
    Medium m;
    // read one: the container with its trailer broken (VD_CRC); its digest is
    // the register over the header read and the container read
    Bytes broken = golden;
    broken.back() ^= 0x01u;
    const Bytes head_one(broken.begin(), broken.begin() + NVM_KLJ2_HDR);
    const std::uint32_t digest = crc_run(crc_run(0xFFFFFFFFu, head_one), broken);
    // read two: IMG_LEN four bytes shorter, the last four bytes forged so the
    // register over its 40 + len - 4 bytes is the same digest
    Bytes shorter = with_word(golden, 16, len - 4u);
    shorter.resize(len - 4u);
    const Bytes head_two(shorter.begin(), shorter.begin() + NVM_KLJ2_HDR);
    const Bytes body(shorter.begin(), shorter.end() - 4);
    const Bytes tail = forge(crc_run(crc_run(0xFFFFFFFFu, head_two), body), digest);
    std::copy(tail.begin(), tail.end(), shorter.end() - 4);
    ASSERT_EQ(crc_run(crc_run(0xFFFFFFFFu, head_two), shorter), digest) << "(the forged read collides)";
    // reads one and two, then read one again, which agrees with the first
    m.slot_a = {broken, broken, shorter, shorter, broken, broken};
    m.serve(flash);
    nvm_smodel_reset();
    nvm_store_boot(flash.port(), &nvm_smodel_port);
    const nvm_status* s = nvm_store_status();
    EXPECT_TRUE(s->verdict_a == NVM_VD_CRC && s->read_faults == 1u && s->unread == 0u && m.reads_a == 6u)
        << "two refusals alike in verdict and digest over different byte counts are a media fault; the third "
        << "read agrees with the first: verdict " << s->verdict_a << ", faults " << s->read_faults << ", reads "
        << m.reads_a;
}

}  // namespace
}  // namespace nvm_test
