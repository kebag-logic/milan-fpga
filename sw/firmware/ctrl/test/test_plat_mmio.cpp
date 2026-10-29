// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_mmio.cpp - plat/ctrl_plat_mmio.c, ctrl_plat_io.h on the target's
// bus, built over a host array (#665 S3):
//
//   I1  a read is one 32-bit load of the word at the address
//   I2  a write is one 32-bit store of the word at the address, and no other

#include <gtest/gtest.h>

#include <cstdint>

#include "ctrl_plat_io.h"
#include "fw_gtest.hpp"

FW_TALLY_LABEL("ctrl split platform MMIO (host array)");

namespace {

std::uint32_t window[64];

TEST(PlatMmio, I1ReadIsTheWordAtTheAddress) {
    window[9] = 0x01020304u;
    EXPECT_EQ(ctrl_plat_io_read32(reinterpret_cast<std::uintptr_t>(&window[9])), 0x01020304u)
        << "I1 a read returns the word at the address";
}

TEST(PlatMmio, I2WriteIsTheWordAtTheAddressAlone) {
    ctrl_plat_io_write32(reinterpret_cast<std::uintptr_t>(&window[20]), 0xA5A55A5Au);
    EXPECT_EQ(window[20], 0xA5A55A5Au) << "I2 a write lands in the word at the address";
    EXPECT_EQ(window[19] | window[21], 0u) << "I2 and in no neighbour";
}

}  // namespace
