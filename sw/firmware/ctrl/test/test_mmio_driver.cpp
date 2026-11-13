// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_mmio_driver.cpp - the mailbox driver as the image builds it: for the
// memory-mapped window (CTRL_MBX_BASE), with each access made in place
// (plat/mbx_mmio.h), over a host array (#665; mmio_window.h):
//
//   M3  the driver opens on the window's ID and CAPS, takes a record from
//       its ring and releases it at RX_TAIL, commits a frame to its ring and
//       TX_HEAD, and takes an event and releases it at EVT_TAIL, every
//       access at the window's base plus its byte offset.

#include <gtest/gtest.h>

#include <cstdint>
#include <cstring>

#include "fw_gtest.hpp"
#include "mbx.h"
#include "mbx_wire.h"
#include "mmio_window.h"
#include "unit_window.hpp"

FW_TALLY_LABEL("ctrl mailbox driver on the MMIO window (host window)");

static_assert(MBX_WINDOW_BYTES <= 4u * CTRL_TEST_WINDOW_WORDS, "the host window holds the contract's");

extern "C" {
std::uint32_t ctrl_test_window[CTRL_TEST_WINDOW_WORDS];
void ctrl_test_wfi(void) {}
}

namespace {

std::uint32_t& at(std::uint32_t byte_offset) { return ctrl_test_window[byte_offset / 4u]; }

TEST(MmioDriver, M3EveryAccessInPlaceAtBasePlusOffset) {
    std::memset(ctrl_test_window, 0, sizeof ctrl_test_window);
    at(MBX_REG_ID) = unit::contract_id();
    at(MBX_REG_CAPS) = unit::contract_caps();
    const unsigned ch = MBX_CH_ADP;
    at(unit::ch_reg(ch, MBX_CH_REG_RX_TAIL)) = 7u;
    at(unit::ch_reg(ch, MBX_CH_REG_TX_HEAD)) = 9u;
    at(unit::ch_reg(ch, MBX_CH_REG_TX_TAIL)) = 9u;
    ASSERT_TRUE(mbx_open()) << "M3 the driver opens on the window's ID and CAPS";

    alignas(4) static std::uint8_t frame[18];
    for (std::size_t j = 0; j < sizeof frame; ++j) {
        frame[j] = static_cast<std::uint8_t>(0xC1u + 29u * j);
    }
    const std::uint32_t rx = MBX_CH_ADP_RX_BASE + 4u * 7u;
    at(rx) = mbx_place(sizeof frame, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH) |
             mbx_place(MBX_RX_KIND, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH);
    at(rx + 4u) = 0x0BADF00Du;
    for (unsigned k = 0; k < 5u; ++k) {
        at(rx + 8u + 4u * k) = ring_lanes_pack(frame + 4u * k, k < 4u ? 4u : 2u);
    }
    at(unit::ch_reg(ch, MBX_CH_REG_RX_HEAD)) = 7u + 2u + 5u;
    static mbx_frame got;
    ASSERT_EQ(mbx_rx_take(ch, &got), MBX_STATUS_OK) << "M3 a record is taken from its ring";
    EXPECT_TRUE(got.len == sizeof frame && got.arrival_ms == 0x0BADF00Du &&
                std::memcmp(got.bytes, frame, sizeof frame) == 0)
        << "M3 the record's words are read at the window's base plus their offset";
    EXPECT_EQ(at(unit::ch_reg(ch, MBX_CH_REG_RX_TAIL)), 7u + 2u + 5u) << "M3 and released at RX_TAIL";

    ASSERT_EQ(mbx_tx_send(ch, 0, frame, sizeof frame), MBX_STATUS_OK) << "M3 a frame is committed";
    const std::uint32_t tx = MBX_CH_ADP_TX_BASE + 4u * 9u;
    EXPECT_EQ(mbx_field(at(tx), MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH), sizeof frame)
        << "M3 its record's length in the ring's word at TX_HEAD";
    for (unsigned k = 0; k < 5u; ++k) {
        EXPECT_EQ(at(tx + 8u + 4u * k), ring_lanes_pack(frame + 4u * k, k < 4u ? 4u : 2u))
            << "M3 payload word " << k << " written at the window's base plus its offset";
    }
    EXPECT_EQ(at(unit::ch_reg(ch, MBX_CH_REG_TX_HEAD)), 9u + 2u + 5u) << "M3 and committed at TX_HEAD";

    at(MBX_EVT_BASE) = mbx_place(MBX_EV_TYPE_LINK, MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
    at(MBX_EVT_BASE + 4u) = mbx_place(1u, MBX_EV_LINK_W1_UP_LSB, MBX_EV_LINK_W1_UP_WIDTH);
    at(MBX_REG_EVT_HEAD) = MBX_EV_WORDS;
    mbx_event ev{};
    EXPECT_TRUE(mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_LINK && ev.link_up) << "M3 an event is taken";
    EXPECT_EQ(at(MBX_REG_EVT_TAIL), MBX_EV_WORDS) << "M3 and released at EVT_TAIL";
}

}  // namespace
