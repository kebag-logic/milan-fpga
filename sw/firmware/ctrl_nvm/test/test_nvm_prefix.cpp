// SPDX-License-Identifier: CERN-OHL-W-2.0
// Exact-sized allocations make a read beyond loaded visible to AddressSanitizer.

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <memory>
#include <vector>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"

namespace fw_test {
const char* tally_label() { return "NVM erased prefixes under AddressSanitizer"; }
}

TEST(NvmCodec, codec_erased_loaded_prefix) {
    std::vector<std::uint8_t> blank(NVM_IMG_LEN);
    nvm_klj2_blank(blank.data());
    ASSERT_EQ(nvm_klj2_check(blank.data(), NVM_IMG_LEN), NVM_VD_OK);
    for (const std::uint32_t loaded : {40u, 47u, 48u}) {
        auto prefix = std::make_unique<std::uint8_t[]>(loaded);
        std::copy_n(blank.data(), loaded, prefix.get());
        EXPECT_EQ(nvm_klj2_check_body(prefix.get(), NVM_IMG_LEN, loaded), NVM_VD_REC)
            << "erased prefix of exactly " << loaded << " bytes is refused without reading beyond it";
    }
    // At the last payload the verdict distinguishes both sides of the bound.
    // An interior record would hit the next header guard even if this guard failed.
    std::uint32_t end = 0;
    for (nvm_rec r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
        end = NVM_KLJ2_HDR + r.off + NVM_REC_HDR + r.plen;
    }
    for (const std::uint32_t loaded : {end - 1u, end}) {
        auto prefix = std::make_unique<std::uint8_t[]>(loaded);
        std::copy_n(blank.data(), loaded, prefix.get());
        EXPECT_EQ(nvm_klj2_check_body(prefix.get(), NVM_IMG_LEN, loaded),
                  loaded == end ? NVM_VD_OK : NVM_VD_REC)
            << "erased last payload at its exact loaded boundary";
    }
}
