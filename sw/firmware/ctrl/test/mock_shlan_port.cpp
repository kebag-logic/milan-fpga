// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_shlan_port.cpp - shlan_port.h's functions forwarding to the alive
// MockShlanPort (see mock_shlan_port.hpp).

#include "mock_shlan_port.hpp"

#include <gtest/gtest.h>

#include <cstdarg>
#include <cstdio>

namespace {

// The mock the test holds; a link seam has no context to carry it in.
MockShlanPort* alive = nullptr;

bool present(const char* call) {
    if (alive == nullptr) {
        ADD_FAILURE() << call << " with no MockShlanPort alive";
        return false;
    }
    return true;
}

}  // namespace

MockShlanPort::MockShlanPort() {
    EXPECT_EQ(alive, nullptr) << "two MockShlanPort alive at once";
    alive = this;
}

MockShlanPort::~MockShlanPort() { alive = nullptr; }

extern "C" void* shlan_malloc(std::size_t size) { return present("shlan_malloc") ? alive->malloc(size) : nullptr; }

extern "C" void* shlan_calloc(std::size_t nmemb, std::size_t size) {
    return present("shlan_calloc") ? alive->calloc(nmemb, size) : nullptr;
}

extern "C" void shlan_free(void* ptr) {
    if (present("shlan_free")) {
        alive->free(ptr);
    }
}

extern "C" int shlan_printf(const char* fmt, ...) {
    char text[256];
    va_list ap;
    va_start(ap, fmt);
    const int n = std::vsnprintf(text, sizeof text, fmt, ap);
    va_end(ap);
    if (n < 0 || !present("shlan_printf")) {
        return n < 0 ? n : 0;
    }
    return alive->print(text);
}

extern "C" void shlan_port_bind_pool(ctrl_pool* pool) {
    if (present("shlan_port_bind_pool")) {
        alive->bind_pool(pool);
    }
}

extern "C" ctrl_pool* shlan_port_pool(void) { return present("shlan_port_pool") ? alive->pool() : nullptr; }
