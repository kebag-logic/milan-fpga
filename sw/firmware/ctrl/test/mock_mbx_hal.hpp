// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_mbx_hal.hpp - mbx_hal.h, the firmware's whole bus port, as a
// GoogleMock object (#665 lane FT).
//
// mbx_hal.h is a link seam: the firmware calls three C functions and a
// platform defines them (plat/mbx_plat_mmio.c on a target, host/
// mbx_plat_host.c on the model). A unit-test binary links mock_mbx_hal.cpp
// in their place, whose three functions forward to the MockMbxHal alive in
// the test. A call with none alive fails the test that made it.
//
// escape_after(n) lets a test leave a loop that never returns: the n-th
// mbx_hal_wait() from then on jumps back to the test's setjmp point, from
// the forwarding function itself, after the mock has recorded the call.

#ifndef MOCK_MBX_HAL_HPP
#define MOCK_MBX_HAL_HPP

#include <gmock/gmock.h>

#include <csetjmp>
#include <cstdint>

#include "mbx_hal.h"

class MockMbxHal {
 public:
    MockMbxHal();
    ~MockMbxHal();
    MockMbxHal(const MockMbxHal&) = delete;
    MockMbxHal& operator=(const MockMbxHal&) = delete;

    MOCK_METHOD(std::uint32_t, read32, (std::uint32_t byte_offset));
    MOCK_METHOD(void, write32, (std::uint32_t byte_offset, std::uint32_t value));
    MOCK_METHOD(void, wait, ());

    //! The n-th mbx_hal_wait() from now longjmps to `to` (n >= 1).
    void escape_after(unsigned n, std::jmp_buf* to) {
        escape_in_ = n;
        escape_to_ = to;
    }
    //! Called by mbx_hal_wait() after the mock saw the call.
    std::jmp_buf* take_escape() {
        if (escape_to_ == nullptr || --escape_in_ != 0u) {
            return nullptr;
        }
        std::jmp_buf* to = escape_to_;
        escape_to_ = nullptr;
        return to;
    }

 private:
    unsigned escape_in_ = 0;
    std::jmp_buf* escape_to_ = nullptr;
};

#endif  // MOCK_MBX_HAL_HPP
