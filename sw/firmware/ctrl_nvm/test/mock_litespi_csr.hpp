// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_litespi_csr.hpp - the LiteSPI command master and timer0 behind the
// on-chip flash port's CSR accessors, as a GoogleMock object (#665 lane FT).
//
// plat/nvm_flash_litespi.c reaches the hardware only through LiteX's
// generated CSR accessors (<generated/csr.h>), which on the host are the
// stubs in host/stubs routing each to a litespi_model_* function: a link
// seam. A unit-test binary links mock_litespi_csr.cpp in place of
// host/litespi_model.c, whose functions forward to the MockLitespiCsr alive
// in the test, so a test can script a master or a timer the model never
// plays (a drain that outlasts the call's deadline).

#ifndef MOCK_LITESPI_CSR_HPP
#define MOCK_LITESPI_CSR_HPP

#include <gmock/gmock.h>

#include <cstdint>

#define _Static_assert static_assert
extern "C" {
#include "litespi_model.h"
}
#undef _Static_assert

class MockLitespiCsr {
 public:
    MockLitespiCsr();
    ~MockLitespiCsr();
    MockLitespiCsr(const MockLitespiCsr&) = delete;
    MockLitespiCsr& operator=(const MockLitespiCsr&) = delete;

    MOCK_METHOD(std::uint32_t, status, ());
    MOCK_METHOD(void, cs, (std::uint32_t v));
    MOCK_METHOD(void, phyconfig, (std::uint32_t v));
    MOCK_METHOD(std::uint32_t, rxtx_read, ());
    MOCK_METHOD(void, rxtx_write, (std::uint32_t v));
    MOCK_METHOD(void, timer, (litespi_timer_reg reg, std::uint32_t v));
    MOCK_METHOD(std::uint32_t, timer_value, ());
};

#endif  // MOCK_LITESPI_CSR_HPP
