// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_mbx_hal.cpp - mbx_hal.h's three functions forwarding to the alive
// MockMbxHal (see mock_mbx_hal.hpp).

#include "mock_mbx_hal.hpp"

#include <gtest/gtest.h>

namespace {

// The mock the test holds; a link seam has no context to carry it in.
MockMbxHal* alive = nullptr;

}  // namespace

MockMbxHal::MockMbxHal() {
    EXPECT_EQ(alive, nullptr) << "two MockMbxHal alive at once";
    alive = this;
}

MockMbxHal::~MockMbxHal() { alive = nullptr; }

extern "C" std::uint32_t mbx_hal_read32(std::uint32_t byte_offset) {
    if (alive == nullptr) {
        ADD_FAILURE() << "mbx_hal_read32(0x" << std::hex << byte_offset << ") with no MockMbxHal alive";
        return 0;
    }
    return alive->read32(byte_offset);
}

extern "C" void mbx_hal_write32(std::uint32_t byte_offset, std::uint32_t value) {
    if (alive == nullptr) {
        ADD_FAILURE() << "mbx_hal_write32(0x" << std::hex << byte_offset << ") with no MockMbxHal alive";
        return;
    }
    alive->write32(byte_offset, value);
}

extern "C" void mbx_hal_wait(void) {
    if (alive == nullptr) {
        ADD_FAILURE() << "mbx_hal_wait() with no MockMbxHal alive";
        return;
    }
    alive->wait();
    // nothing with a destructor is alive in this frame or the C frames above
    // it, so leaving them by longjmp skips no cleanup
    std::jmp_buf* to = alive->take_escape();
    if (to != nullptr) {
        std::longjmp(*to, 1);
    }
}
