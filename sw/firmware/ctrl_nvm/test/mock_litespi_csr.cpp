// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_litespi_csr.cpp - host/litespi_model.h's accessors forwarding to the
// alive MockLitespiCsr (see mock_litespi_csr.hpp). The model's other entry
// points are the tests' to call, never the port's, so none is defined here.

#include "mock_litespi_csr.hpp"

#include <gtest/gtest.h>

namespace {

// The mock the test holds; a link seam has no context to carry it in.
MockLitespiCsr* alive = nullptr;

bool present(const char* call) {
    if (alive == nullptr) {
        ADD_FAILURE() << call << " with no MockLitespiCsr alive";
        return false;
    }
    return true;
}

}  // namespace

MockLitespiCsr::MockLitespiCsr() {
    EXPECT_EQ(alive, nullptr) << "two MockLitespiCsr alive at once";
    alive = this;
}

MockLitespiCsr::~MockLitespiCsr() { alive = nullptr; }

extern "C" std::uint32_t litespi_model_status(void) { return present("status") ? alive->status() : 0u; }

extern "C" void litespi_model_cs(std::uint32_t v) {
    if (present("cs")) {
        alive->cs(v);
    }
}

extern "C" void litespi_model_phyconfig(std::uint32_t v) {
    if (present("phyconfig")) {
        alive->phyconfig(v);
    }
}

extern "C" std::uint32_t litespi_model_rxtx_read(void) { return present("rxtx_read") ? alive->rxtx_read() : 0u; }

extern "C" void litespi_model_rxtx_write(std::uint32_t v) {
    if (present("rxtx_write")) {
        alive->rxtx_write(v);
    }
}

extern "C" void litespi_model_timer(enum litespi_timer_reg reg, std::uint32_t v) {
    if (present("timer")) {
        alive->timer(reg, v);
    }
}

extern "C" std::uint32_t litespi_model_timer_value(void) { return present("timer_value") ? alive->timer_value() : 0u; }

extern "C" uintptr_t litespi_model_csr_base(void) { return 0u; }
