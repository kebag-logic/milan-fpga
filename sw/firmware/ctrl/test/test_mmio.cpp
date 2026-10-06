// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_mmio.cpp - plat/mbx_plat_mmio.c, mbx_hal.h on a memory-mapped window,
// built over a host array through its own configuration macros (#665 lane
// FT; mmio_window.h):
//
//   M1  every access is one 32-bit load or store of the word at the window's
//       base plus the byte offset;
//   M2  mbx_hal_wait() is the platform's CTRL_MBX_WFI, once per call.

#include <gtest/gtest.h>

#include <cstdint>

#include "fw_gtest.hpp"
#include "mbx_hal.h"
#include "mmio_window.h"

FW_TALLY_LABEL("ctrl MMIO platform (host window)");

extern "C" {
std::uint32_t ctrl_test_window[CTRL_TEST_WINDOW_WORDS];
}

namespace {

unsigned waits;

}  // namespace

extern "C" void ctrl_test_wfi(void) { ++waits; }

namespace {

TEST(MmioPlatform, M1OneWordAtBasePlusOffset) {
    mbx_hal_write32(0x40u, 0xA5A55A5Au);
    EXPECT_EQ(ctrl_test_window[0x10], 0xA5A55A5Au) << "M1 a write lands in the word at base + offset";
    EXPECT_EQ(ctrl_test_window[0x0F] | ctrl_test_window[0x11], 0u) << "M1 and in no neighbour";
    ctrl_test_window[0x20] = 0x01020304u;
    EXPECT_EQ(mbx_hal_read32(0x80u), 0x01020304u) << "M1 a read returns the word at base + offset";
}

TEST(MmioPlatform, M2WaitIsThePlatformWfi) {
    const unsigned before = waits;
    mbx_hal_wait();
    mbx_hal_wait();
    EXPECT_EQ(waits - before, 2u) << "M2 each mbx_hal_wait() waits once, through CTRL_MBX_WFI";
}

}  // namespace
