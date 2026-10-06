// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_shlan_port.hpp - lwSRP's port layer (port/shlan_port.h) as a
// GoogleMock object (#665 lane FT).
//
// shlan_port.h is a link seam: lwSRP calls shlan_malloc, shlan_calloc,
// shlan_free and shlan_printf, and the composition binds the pool behind
// them, and port/shlan_port.c defines all six on the static pool and the
// debug sink. A unit-test binary links mock_shlan_port.cpp in its place,
// whose functions forward to the MockShlanPort alive in the test; the
// printf is formatted first and the mock sees the text. A call with none
// alive fails the test that made it.

#ifndef MOCK_SHLAN_PORT_HPP
#define MOCK_SHLAN_PORT_HPP

#include <gmock/gmock.h>

#include <cstddef>
#include <string>

#include "shlan_port.h"

class MockShlanPort {
 public:
    MockShlanPort();
    ~MockShlanPort();
    MockShlanPort(const MockShlanPort&) = delete;
    MockShlanPort& operator=(const MockShlanPort&) = delete;

    MOCK_METHOD(void*, malloc, (std::size_t size));
    MOCK_METHOD(void*, calloc, (std::size_t nmemb, std::size_t size));
    MOCK_METHOD(void, free, (void* ptr));
    MOCK_METHOD(int, print, (const std::string& text));
    MOCK_METHOD(void, bind_pool, (ctrl_pool * pool));
    MOCK_METHOD(ctrl_pool*, pool, ());
};

#endif  // MOCK_SHLAN_PORT_HPP
