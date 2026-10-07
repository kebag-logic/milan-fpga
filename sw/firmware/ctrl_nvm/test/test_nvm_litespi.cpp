// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_litespi.cpp - the on-chip flash port (plat/nvm_flash_litespi.c)
// alone, on GoogleMock's command master and timer0 (mock_litespi_csr.hpp)
// (#665 lane FT):
//
//   port_read_range      a read past the device is refused before any byte;
//   port_write_refusals  a program of nothing, of more than a page, across a
//                        page or outside the journal, and an erase outside
//                        it, are refused before the master is touched;
//   port_drain_deadline  a master whose receive side keeps reporting a byte
//                        past the call's deadline ends the call with a
//                        failure, chip select released, before LS_POLL_MAX.

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <cstdint>

#include "fw_gtest.hpp"
#include "mock_litespi_csr.hpp"
#include "nvm_c.hpp"

extern "C" {
#include <generated/csr.h>
}

FW_TALLY_LABEL("ctrl_nvm LiteSPI port (command master and timer0 mocked)");

namespace {

using ::testing::_;
using ::testing::AnyNumber;
using ::testing::AtLeast;
using ::testing::Between;
using ::testing::NiceMock;
using ::testing::Return;
using ::testing::StrictMock;

const nvm_flash& port() { return nvm_flash_litespi; }

// LS_POLL_MAX of plat/nvm_flash_litespi.c, the bound on every wait: a drain
// that ends on the call's deadline ends well inside it (the deadline is
// consulted every LS_LATE_EVERY, 64, reads).
constexpr int kPollMax = 4096;

TEST(NvmLitespiPort, port_read_range) {
    StrictMock<MockLitespiCsr> csr;
    std::uint8_t buf[4] = {};
    EXPECT_NE(port().read(port().ctx, NVM_FMODEL_BYTES, buf, 1), 0) << "a read starting past the device is refused";
    EXPECT_NE(port().read(port().ctx, NVM_FMODEL_BYTES - 1u, buf, 2), 0) << "a read running past it is refused";
    EXPECT_EQ(port().read(port().ctx, NVM_FMODEL_BYTES - 2u, buf, 2), 0) << "a read ending at its last byte is taken";
}

TEST(NvmLitespiPort, port_write_refusals) {
    StrictMock<MockLitespiCsr> csr;
    static const std::uint8_t page[NVM_FLASH_PAGE + 1u] = {};
    EXPECT_NE(port().program(port().ctx, NVM_SLOT_B, page, 0), 0) << "a program of nothing is refused";
    EXPECT_NE(port().program(port().ctx, NVM_SLOT_B, page, NVM_FLASH_PAGE + 1u), 0)
        << "a program of more than a page is refused";
    EXPECT_NE(port().program(port().ctx, NVM_SLOT_B + 255u, page, 2), 0) << "a program across a page is refused";
    EXPECT_NE(port().program(port().ctx, NVM_SLOT_A - NVM_FLASH_PAGE, page, 4), 0)
        << "a program below the journal is refused";
    EXPECT_NE(port().erase(port().ctx, NVM_SLOT_B + 2u * NVM_SLOT_BYTES), 0) << "an erase past the journal is refused";
}

TEST(NvmLitespiPort, port_drain_deadline) {
    NiceMock<MockLitespiCsr> csr;
    std::uint32_t timer = 0xFFFFFFFFu;
    // timer0 counts down: the call starts at one reading, and every later
    // reading is a whole deadline and a clock later
    ON_CALL(csr, timer_value()).WillByDefault([&timer]() {
        const std::uint32_t now = timer;
        timer -= nvm_flash_litespi_call_ticks + 1u;
        return now;
    });
    ON_CALL(csr, status()).WillByDefault(Return(1u << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET));
    // the drain reads what the master holds until the deadline, never to the
    // poll bound: a drain that stops only there ignored the deadline
    EXPECT_CALL(csr, rxtx_read()).Times(Between(1, kPollMax - 1));
    EXPECT_CALL(csr, cs(0u)).Times(AtLeast(1));
    EXPECT_CALL(csr, cs(1u)).Times(0);
    EXPECT_CALL(csr, timer(_, _)).Times(AnyNumber());
    nvm_flash_litespi_power_on();
    EXPECT_LT(port().busy(port().ctx), 0) << "a drain still busy past the call's deadline fails the call";
}

}  // namespace
