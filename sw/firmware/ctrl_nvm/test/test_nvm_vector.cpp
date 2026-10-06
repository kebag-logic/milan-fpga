// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_vector.cpp - the round trip against the parent's recorded vector
// (#665 lanes F1 and FT; GoogleTest). Built only for the shapes
// tb/verilator/nvm_backend records a vector of, with the store compiled under
// that vector's identity (scripts/check_nvm_record_space.py
// render_record_table), so its own binary.
//
// The store, given the vector's records, commits the container the backend
// suite grades the RTL against: its length, CRC-32 and every record's offset
// (the table, which the fixture carries), byte for byte as nvm_klj2.py
// assembles it, and boots it back to the same values.

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

FW_TALLY_LABEL("ctrl_nvm saved-state store, recorded vector (" NVM_TALLY_SHAPE ")");

namespace nvm_test {
namespace {

// CRC-32/ISO-HDLC, bit by bit: the table's own CRC, computed here rather
// than by the store whose output it grades.
std::uint32_t crc32(const Bytes& bytes, std::size_t len) {
    std::uint32_t crc = 0xFFFFFFFFu;
    for (std::size_t k = 0; k < len; ++k) {
        crc ^= bytes[k];
        for (int bit = 0; bit < 8; ++bit) {
            crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
        }
    }
    return ~crc;
}

// Every record frame of a container: record id, area offset, framed length
// and payload length, read off its F07.8 headers.
std::vector<std::vector<long long>> walk(const Bytes& blob) {
    std::vector<std::vector<long long>> rows(4);
    if (blob.size() < 16u) {
        return rows;
    }
    const std::uint32_t nrec = nvm_rd32le(blob.data() + 12);
    std::size_t pos = NVM_KLJ2_HDR;
    for (std::uint32_t k = 0; k < nrec && pos + NVM_REC_HDR <= blob.size(); ++k) {
        const long long plen_be = (static_cast<long long>(blob[pos + 4]) << 8) | blob[pos + 5];
        rows[0].push_back(blob[pos + 3]);
        rows[1].push_back(static_cast<long long>(pos - NVM_KLJ2_HDR));
        rows[2].push_back(NVM_REC_HDR + plen_be);
        rows[3].push_back(plen_be);
        pos += NVM_REC_HDR + static_cast<std::size_t>(plen_be);
    }
    return rows;
}

TEST_P(NvmBoth, vector_round_trip) {
    Files f = fx().files({{"v6.bin", "erased@6"}});
    Result r = go(port(), f, {"--slot-a", "v6.bin", "--boot", "--set-pattern", "0", "--commit", "--dump-slot-b", "v7.bin"});
    const Bytes& want = fx().blob("frames@7");
    const Bytes& slot = f.blobs["v7.bin"];
    const Bytes got(slot.begin(), slot.begin() + static_cast<std::ptrdiff_t>(std::min(want.size(), slot.size())));
    EXPECT_TRUE(r.at("ok") == 1 && r.at("seq") == 7 && r.at("auth") == 1) << "vector commit: " << r.text();
    EXPECT_TRUE(got == want) << "the vector container differs from nvm_klj2.py's";
    const std::vector<long long>& rows_rid = fx().list("vector_rows_rid");
    EXPECT_TRUE(static_cast<long long>(got.size()) == fx().num("vector_imglen") &&
                fx().num("vector_nrec") == static_cast<long long>(rows_rid.size()) && got.size() >= 4u &&
                crc32(got, got.size() - 4u) == static_cast<std::uint32_t>(fx().num("vector_crc32")))
        << "length or CRC-32 differs from the recorded vector";
    const std::vector<std::vector<long long>> rows = walk(got);
    EXPECT_TRUE(rows[0] == rows_rid && rows[1] == fx().list("vector_rows_off") &&
                rows[2] == fx().list("vector_rows_flen") && rows[3] == fx().list("vector_rows_plen"))
        << "a record offset differs from the recorded vector";
    r = go(port(), f, {"--slot-b", "v7.bin", "--boot", "--dump-state", "vst"});
    EXPECT_EQ(r.at("applied"), static_cast<long long>(rids().size())) << "vector boot: " << r.text();
    expect_state(f, "vst", fx().payloads("frames"));
}

}  // namespace
}  // namespace nvm_test
