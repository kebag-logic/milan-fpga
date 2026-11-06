// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_mbx_dma_driver.cpp - the mailbox driver as the split image builds it:
// its accesses made in place on the window (CTRL_MBX_BASE, mmio_window.h)
// and each record's payload moved by the record mover (CTRL_MBX_DMA_BASE,
// plat/mbx_dma.h), over a register model of KL_mbx_dma (#665; mmio_dma.h).
//
// The model is written from the mover's register contract (mbx_dma.h's
// header comment, KL_mbx_dma.sv's ports), never read off the driver: CFG
// [15:0] the ring's word 0 as a word address in the window and [31:16] its
// words less one; MEM the memory side's first byte; CMD [15:0] the first
// payload word's ring index, [27:16] its bytes, [31] memory to the ring, a
// write of which starts a move; STATUS [0] BUSY and [1] ERR. A move leaves
// memory or the ring as the driver's word loop would: in ring order, a
// transmit word's lanes past the length zero, a receive move's bytes past
// the length untouched. A start with MEM off a word is refused with ERR, as
// the mover refuses it, and the test can make the next move end in an error
// response, after part of its payload moved.
//
//   R1  a record's payload is moved from its ring, from the first word past
//       its header, at every tail length and across the ring's end; the
//       record is released at RX_TAIL; the driver polls STATUS until BUSY
//       falls;
//   R2  a move that ends with ERR leaves no record: the driver gives the
//       record back as bad and releases everything to RX_HEAD;
//   T1  a frame on a word is moved memory to the ring past the header words
//       the driver wrote, at every tail length and across the ring's end,
//       and committed at TX_HEAD;
//   T2  a move that ends with ERR is not committed: TX_HEAD and the sequence
//       stay, and the next frame is written at the same head;
//   T3  a frame off a word takes the driver's word loop, and the mover is
//       not started.

#include <gtest/gtest.h>

#include <cstdint>
#include <cstring>
#include <utility>
#include <vector>

#include "fw_gtest.hpp"
#include "mbx.h"
#include "mbx_wire.h"
#include "mmio_dma.h"
#include "mmio_window.h"
#include "unit_window.hpp"

FW_TALLY_LABEL("ctrl mailbox driver with the record mover (host register model)");

static_assert(MBX_WINDOW_BYTES <= 4u * CTRL_TEST_WINDOW_WORDS, "the host window holds the contract's");

namespace {

constexpr unsigned kCfg = 0, kMem = 1, kCmd = 2, kStatus = 3;   // the bank's words, in order
constexpr std::uint32_t kBusy = 0x1u, kErr = 0x2u;
//! CMD between starts: bits [30:28] are set by no command the contract defines.
constexpr std::uint32_t kNoCmd = 0x70000000u;
constexpr std::uint8_t kGuard = 0xEE;

//! One start the driver made: the three operand registers as it wrote them.
struct Start {
    std::uint32_t cfg, mem, cmd;
    std::uint32_t base() const { return cfg & 0xFFFFu; }
    std::uint32_t words() const { return (cfg >> 16) + 1u; }
    std::uint32_t index() const { return cmd & 0xFFFFu; }
    std::uint32_t len() const { return (cmd >> 16) & 0xFFFu; }
    bool to_ring() const { return (cmd >> 31) != 0u; }
};

class Mover {
 public:
    std::vector<Start> starts;
    unsigned busy_reads = 2;   // the accesses after a start that still see BUSY
    bool fail = false;         // the next move ends with an error response, after its first line
    unsigned accesses = 0;     // register accesses since reset()
    std::vector<std::pair<std::uint8_t*, std::size_t>> memory;   // what the test gave the driver

    void reset() {
        std::memset(ctrl_test_dma, 0, sizeof ctrl_test_dma);
        ctrl_test_dma[kCmd] = kNoCmd;
        starts.clear();
        memory.clear();
        busy_reads = 2;
        fail = false;
        accesses = 0;
        busy_left_ = 0;
    }

    //! The bank's address for the access the driver is about to make.
    std::uintptr_t access() {
        ++accesses;
        if (ctrl_test_dma[kCmd] != kNoCmd) {
            start();
        } else if (busy_left_ != 0u) {
            --busy_left_;
            ctrl_test_dma[kStatus] = busy_left_ != 0u ? kBusy : final_;
        }
        return reinterpret_cast<std::uintptr_t>(ctrl_test_dma);
    }

 private:
    void start() {
        const Start s{ctrl_test_dma[kCfg], ctrl_test_dma[kMem], ctrl_test_dma[kCmd]};
        starts.push_back(s);
        ctrl_test_dma[kCmd] = kNoCmd;
        std::uint8_t* p = resolve(s.mem, s.len());
        final_ = 0u;
        if ((s.mem & 3u) != 0u || p == nullptr) {
            final_ = kErr;   // refused: nothing moves
        } else if (fail) {
            fail = false;
            final_ = kErr;   // an error response after the first line's sixteen words
            move(s, p, s.len() < 64u ? s.len() : 64u);
        } else {
            move(s, p, s.len());
        }
        busy_left_ = busy_reads;
        ctrl_test_dma[kStatus] = busy_left_ != 0u ? kBusy : final_;
    }

    //! The memory MEM names, len bytes of it, in a buffer the test gave the driver.
    std::uint8_t* resolve(std::uint32_t mem, std::uint32_t len) const {
        for (const auto& [base, size] : memory) {
            const std::uint32_t off = mem - static_cast<std::uint32_t>(reinterpret_cast<std::uintptr_t>(base));
            if (off <= size && len <= size - off) return base + off;
        }
        ADD_FAILURE() << "MEM names memory the test did not give the driver";
        return nullptr;
    }

    void move(const Start& s, std::uint8_t* p, std::uint32_t bytes) {
        for (std::uint32_t k = 0; k < bytes; ++k) {
            std::uint32_t& word = ctrl_test_window[s.base() + ((s.index() + k / 4u) & (s.words() - 1u))];
            const unsigned lane = 8u * (k % 4u);
            if (s.to_ring()) {
                if (k % 4u == 0u) word = 0u;   // a transmit word's lanes past the length stay zero
                word |= std::uint32_t(p[k]) << lane;
            } else {
                p[k] = static_cast<std::uint8_t>(word >> lane);
            }
        }
    }

    unsigned busy_left_ = 0;
    std::uint32_t final_ = 0;
};

Mover mover;

}  // namespace

extern "C" {
std::uint32_t ctrl_test_window[CTRL_TEST_WINDOW_WORDS];
std::uint32_t ctrl_test_dma[CTRL_TEST_DMA_WORDS];
void ctrl_test_wfi(void) {}
uintptr_t ctrl_test_dma_base(void) { return mover.access(); }
}

namespace {

constexpr unsigned kCh = MBX_CH_AECP;

std::uint32_t& at(std::uint32_t byte_offset) { return ctrl_test_window[byte_offset / 4u]; }
std::uint32_t& rx_ring(std::uint32_t index) { return at(MBX_CH_AECP_RX_BASE + 4u * (index % MBX_CH_AECP_RX_WORDS)); }
std::uint32_t& tx_ring(std::uint32_t index) { return at(MBX_CH_AECP_TX_BASE + 4u * (index % MBX_CH_AECP_TX_WORDS)); }

std::uint8_t pattern(std::uint32_t i) { return static_cast<std::uint8_t>(0x3Cu ^ (i * 41u + (i >> 3))); }

//! The ring word a driver's word loop writes for payload word k of a frame.
std::uint32_t lanes(const std::uint8_t* frame, std::uint32_t len, std::uint32_t k) {
    const std::uint32_t left = len - 4u * k;
    return ring_lanes_pack(frame + 4u * k, left < 4u ? left : 4u);
}

class MbxDma : public ::testing::Test {
 protected:
    //! A clean window and mover, the channel's cursors at `rx_tail` and `tx_head`, and the driver opened.
    void open(std::uint16_t rx_tail, std::uint16_t tx_head) {
        std::memset(ctrl_test_window, 0, sizeof ctrl_test_window);
        mover.reset();
        at(MBX_REG_ID) = unit::contract_id();
        at(MBX_REG_CAPS) = unit::contract_caps();
        at(unit::ch_reg(kCh, MBX_CH_REG_RX_TAIL)) = rx_tail;
        at(unit::ch_reg(kCh, MBX_CH_REG_RX_HEAD)) = rx_tail;
        at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)) = tx_head;
        at(unit::ch_reg(kCh, MBX_CH_REG_TX_TAIL)) = tx_head;
        ASSERT_TRUE(mbx_open()) << "the driver opens on the window's ID and CAPS";
        mover.accesses = 0;
    }

    //! A received record of len bytes at tail, its payload's bytes pattern(i + len); returns its words.
    std::uint32_t post(std::uint16_t tail, std::uint32_t len) {
        rx_ring(tail) = mbx_place(len, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH) |
                        mbx_place(MBX_RX_KIND, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH);
        rx_ring(tail + 1u) = 0x0BADF00Du;
        std::uint8_t bytes[MBX_FRAME_BYTES_MAX];
        for (std::uint32_t i = 0; i < len; ++i) bytes[i] = pattern(i + len);
        const std::uint32_t words = (len + 3u) / 4u;
        for (std::uint32_t k = 0; k < words; ++k) rx_ring(tail + MBX_RX_HDR_WORDS + k) = lanes(bytes, len, k);
        const std::uint32_t record = MBX_RX_HDR_WORDS + words;
        at(unit::ch_reg(kCh, MBX_CH_REG_RX_HEAD)) = static_cast<std::uint16_t>(tail + record);
        return record;
    }
};

TEST_F(MbxDma, R1ARecordsPayloadIsMovedAndReleased) {
    for (std::uint32_t len : {60u, 61u, 62u, 63u}) {
        const std::uint16_t tail = MBX_CH_AECP_RX_WORDS - 5u;   // the payload crosses the ring's end
        open(tail, 0);
        const std::uint32_t record = post(tail, len);
        static mbx_frame got;
        std::memset(&got, kGuard, sizeof got);
        mover.memory = {{got.bytes, sizeof got.bytes}};
        ASSERT_EQ(mbx_rx_take(kCh, &got), MBX_STATUS_OK) << "R1 a record is taken, " << len << " bytes";
        ASSERT_EQ(mover.starts.size(), 1u) << "R1 the mover is started once, " << len << " bytes";
        const Start& s = mover.starts[0];
        EXPECT_TRUE(s.base() == MBX_CH_AECP_RX_BASE / 4u && s.words() == MBX_CH_AECP_RX_WORDS)
            << "R1 CFG names the ring's base and size, " << len << " bytes";
        EXPECT_TRUE(s.index() == static_cast<std::uint16_t>(tail + MBX_RX_HDR_WORDS) && s.len() == len &&
                    !s.to_ring())
            << "R1 the move starts at the payload's first ring word, " << len << " bytes";
        bool same = got.len == len;
        for (std::uint32_t i = 0; i < len; ++i) same = same && got.bytes[i] == pattern(i + len);
        for (std::uint32_t i = len; i < sizeof got.bytes; ++i) same = same && got.bytes[i] == kGuard;
        EXPECT_TRUE(same) << "R1 the record's payload is the ring's bytes and nothing past them, " << len
                          << " bytes";
        EXPECT_EQ(got.arrival_ms, 0x0BADF00Du) << "R1 the header is the driver's own read";
        EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_RX_TAIL)), static_cast<std::uint16_t>(tail + record))
            << "R1 the record is released at RX_TAIL, " << len << " bytes";
        EXPECT_EQ(mover.accesses, 3u + mover.busy_reads + 1u)
            << "R1 the driver polls STATUS until BUSY falls, " << len << " bytes";
    }
}

TEST_F(MbxDma, R2AMoveEndingInErrorResynchronises) {
    const std::uint16_t tail = 40;
    open(tail, 0);
    const std::uint32_t record = post(tail, 200);
    const std::uint32_t second = post(static_cast<std::uint16_t>(tail + record), 100);
    static mbx_frame got;
    mover.memory = {{got.bytes, sizeof got.bytes}};
    mover.fail = true;
    EXPECT_EQ(mbx_rx_take(kCh, &got), MBX_STATUS_BAD) << "R2 a move that ends in ERR leaves no record";
    const std::uint16_t head = static_cast<std::uint16_t>(tail + record + second);
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_RX_TAIL)), head) << "R2 and everything to RX_HEAD is released";
    EXPECT_EQ(mbx_rx_take(kCh, &got), MBX_STATUS_EMPTY) << "R2 so the next take finds the ring empty";
}

TEST_F(MbxDma, T1AFrameOnAWordIsMovedAndCommitted) {
    for (std::uint32_t len : {60u, 61u, 62u, 63u}) {
        const std::uint16_t head = MBX_CH_AECP_TX_WORDS - 6u;   // the payload crosses the ring's end
        open(0, head);
        alignas(4) static std::uint8_t frame[MBX_FRAME_BYTES_MAX];
        for (std::uint32_t i = 0; i < len; ++i) frame[i] = pattern(i + 7u * len);
        for (std::uint32_t k = 0; k < 20u; ++k) tx_ring(head + MBX_TX_HDR_WORDS + k) = 0xDEADBEEFu;
        mover.memory = {{frame, sizeof frame}};
        ASSERT_EQ(mbx_tx_send(kCh, 0, frame, static_cast<std::uint16_t>(len)), MBX_STATUS_OK)
            << "T1 a frame on a word is sent, " << len << " bytes";
        ASSERT_EQ(mover.starts.size(), 1u) << "T1 the mover is started once, " << len << " bytes";
        const Start& s = mover.starts[0];
        EXPECT_TRUE(s.base() == MBX_CH_AECP_TX_BASE / 4u && s.words() == MBX_CH_AECP_TX_WORDS)
            << "T1 CFG names the ring's base and size, " << len << " bytes";
        EXPECT_TRUE(s.index() == static_cast<std::uint16_t>(head + MBX_TX_HDR_WORDS) && s.len() == len &&
                    s.to_ring())
            << "T1 the move runs memory to the ring from the payload's first word, " << len << " bytes";
        const std::uint32_t words = (len + 3u) / 4u;
        bool same = mbx_field(tx_ring(head), MBX_TXREC_W0_LEN_LSB, MBX_TXREC_W0_LEN_WIDTH) == len;
        for (std::uint32_t k = 0; k < words; ++k) same = same && tx_ring(head + MBX_TX_HDR_WORDS + k) == lanes(frame, len, k);
        same = same && tx_ring(head + MBX_TX_HDR_WORDS + words) == 0xDEADBEEFu;
        EXPECT_TRUE(same) << "T1 the ring holds the header and the frame's words and nothing past them, " << len
                          << " bytes";
        EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), static_cast<std::uint16_t>(head + MBX_TX_HDR_WORDS + words))
            << "T1 the record is committed at TX_HEAD, " << len << " bytes";
    }
}

TEST_F(MbxDma, T2AMoveEndingInErrorIsNotCommitted) {
    const std::uint16_t head = 100;
    open(0, head);
    alignas(4) static std::uint8_t frame[200];
    for (std::uint32_t i = 0; i < sizeof frame; ++i) frame[i] = pattern(i);
    mover.memory = {{frame, sizeof frame}};
    mover.fail = true;
    EXPECT_EQ(mbx_tx_send(kCh, 0, frame, sizeof frame), MBX_STATUS_BAD)
        << "T2 a move that ends in ERR is refused";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), head) << "T2 a move that ends in ERR is not committed";
    const std::uint32_t seq = tx_ring(head + 1u);
    ASSERT_EQ(mbx_tx_send(kCh, 0, frame, sizeof frame), MBX_STATUS_OK) << "T2 the next frame is sent";
    EXPECT_TRUE(mover.starts.size() == 2u && mover.starts[1].index() == head + MBX_TX_HDR_WORDS &&
                tx_ring(head + 1u) == seq)
        << "T2 the next frame is written at the same head with the same sequence";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), head + MBX_TX_HDR_WORDS + sizeof frame / 4u)
        << "T2 and committed there";
}

TEST_F(MbxDma, T3AFrameOffAWordTakesTheWordLoop) {
    const std::uint16_t head = MBX_CH_AECP_TX_WORDS - 4u;
    open(0, head);
    alignas(4) static std::uint8_t buffer[72];
    const std::uint8_t* frame = buffer + 1;
    const std::uint32_t len = 61;
    for (std::uint32_t i = 0; i < sizeof buffer; ++i) buffer[i] = pattern(i);
    mover.memory = {{buffer, sizeof buffer}};
    ASSERT_EQ(mbx_tx_send(kCh, 0, frame, static_cast<std::uint16_t>(len)), MBX_STATUS_OK)
        << "T3 a frame off a word takes the word loop";
    EXPECT_TRUE(mover.starts.empty()) << "T3 a frame off a word starts no move";
    bool same = true;
    for (std::uint32_t k = 0; k < (len + 3u) / 4u; ++k) same = same && tx_ring(head + MBX_TX_HDR_WORDS + k) == lanes(frame, len, k);
    EXPECT_TRUE(same) << "T3 the ring holds the frame's words";
    EXPECT_EQ(at(unit::ch_reg(kCh, MBX_CH_REG_TX_HEAD)), static_cast<std::uint16_t>(head + MBX_TX_HDR_WORDS + 16u))
        << "T3 and the record is committed at TX_HEAD";
}

}  // namespace
