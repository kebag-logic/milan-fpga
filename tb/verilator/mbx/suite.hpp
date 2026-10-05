// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// suite.hpp - the packet-mailbox checks, written once against the contract
// and run on every bench that answers the same calls (#665 lane F0):
//
//   * mbx_tb::Bench (bench.hpp): the RTL, KL_mbx behind KL_mbx_wb or
//     KL_mbx_axil, cycle by cycle (sim_main.cpp, both adapters);
//   * mbx_tb::ModelBench (sw/firmware/ctrl/test/model_bench.hpp): the C model
//     of the fabric side the firmware's host tests run against.
//
// So the model is not graded against itself: a behaviour where the model and
// the RTL differ fails one of the runs. The register offsets and field
// positions are the generated contract (mbx_contract.h); the frames are
// written from the clauses (frames.hpp); the expectations are the contract's
// sentences: byte k of a frame in ring word k/4 at bits 8*(k%4), a record
// committed whole or not at all, a drop never touching an unread record,
// every source coalesced, the interrupt the OR of the enabled levels.
//
// A bench provides: reset, idle(n), ms(n), set_link(mask), set_gm, gm_change,
// send_frame, drain_rx, wait_tx(n), tx_ready_pattern, read, write(off, v,
// strobes), irq(), and the members tx_frames and bus_timeouts.

#ifndef MBX_SUITE_HPP
#define MBX_SUITE_HPP

#include <cstdint>
#include <vector>

#include "../../common/verilator_harness.hpp"
#include "frames.hpp"
#include "mbx_contract.h"

namespace mbx_tb {

inline constexpr std::uint64_t kOwnEid = 0x0011223344556677ull;
inline constexpr std::uint64_t kForeignEid = 0x7766554433221100ull;
inline constexpr std::uint32_t kAdp = MBX_CH_ADP;

//! One RX record as the core reads it.
struct Record {
    std::uint32_t w0 = 0;
    std::uint32_t w1 = 0;
    std::vector<std::uint8_t> bytes;
};

inline std::uint32_t field(std::uint32_t word, std::uint32_t lsb, std::uint32_t width) {
    const std::uint32_t mask = width >= 32u ? 0xFFFFFFFFu : ((1u << width) - 1u);
    return (word >> lsb) & mask;
}

inline std::uint32_t ch_reg(std::uint32_t ch, std::uint32_t reg) { return MBX_CH_BASE + MBX_CH_STRIDE * ch + reg; }

template <class Bench>
class Suite {
 public:
    Suite(Bench& bench, milan::tb::Checker& check) : b_(bench), ck_(check) {}

    void run() {
        b_.reset();
        check_reset_and_identity();
        check_register_masks();
        restart();
        check_partial_strobe_refused();
        restart();
        check_adp_filter();
        restart();
        check_classification();
        restart();
        check_drop_never_touches_an_unread_record();
        restart();
        check_rate_limit();
        restart();
        check_tx_merge();
        restart();
        check_tx_refusals();
        restart();
        check_link_and_gm_events();
        restart();
        check_timers();
        restart();
        check_tick();
        restart();
        check_gm_snapshot();
        ck_.dec("no bus access went unanswered", b_.bus_timeouts, 0);
    }

 private:
    void restart() {
        b_.reset();
        rx_tail_.assign(MBX_N_CH, 0);
        evt_tail_ = 0;
        b_.tx_frames.clear();
        b_.tx_ready_pattern(0xFF);
    }

    std::uint32_t rd(std::uint32_t off) { return b_.read(off); }
    void wr(std::uint32_t off, std::uint32_t v) { b_.write(off, v); }

    void open(std::uint32_t mask) {
        wr(MBX_REG_OWN_EID_LO, static_cast<std::uint32_t>(kOwnEid));
        wr(MBX_REG_OWN_EID_HI, static_cast<std::uint32_t>(kOwnEid >> 32));
        wr(MBX_REG_FILTER_EN, mask);
    }

    std::uint32_t rx_head(std::uint32_t ch) { return rd(ch_reg(ch, MBX_CH_REG_RX_HEAD)); }
    std::uint32_t rx_pass(std::uint32_t ch) { return rd(ch_reg(ch, MBX_CH_REG_RX_PASS)); }

    //! The record at the harness's tail of channel `ch`, read word by word.
    Record peek(std::uint32_t ch) {
        static const std::uint32_t base[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
        static const std::uint32_t words[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;
        auto word = [&](std::uint32_t i) { return rd(base[ch] + 4u * ((rx_tail_[ch] + i) & (words[ch] - 1u))); };
        Record r;
        r.w0 = word(0);
        r.w1 = word(1);
        const std::uint32_t len = field(r.w0, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH);
        std::uint32_t lanes = 0;
        for (std::uint32_t k = 0; k < len && k < 2048u; ++k) {
            if (k % 4u == 0u) {
                lanes = word(2u + k / 4u);
            }
            r.bytes.push_back(static_cast<std::uint8_t>(lanes >> (8u * (k % 4u))));
        }
        return r;
    }

    //! Release the record at the tail (the RX doorbell).
    void release(std::uint32_t ch, const Record& r) {
        const std::uint32_t len = field(r.w0, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH);
        rx_tail_[ch] = (rx_tail_[ch] + 2u + (len + 3u) / 4u) & 0xFFFFu;
        wr(ch_reg(ch, MBX_CH_REG_RX_TAIL), rx_tail_[ch]);
    }

    bool same_bytes(const std::vector<std::uint8_t>& a, const std::vector<std::uint8_t>& b) { return a == b; }

    void check_reset_and_identity();
    void check_register_masks();
    void check_partial_strobe_refused();
    void check_adp_filter();
    void check_adp_terms();
    void check_classification();
    void check_classification_avtp();
    void check_classification_other();
    void check_drop_never_touches_an_unread_record();
    void check_rate_limit();
    void check_tx_merge();
    void check_tx_refusals();
    void check_link_and_gm_events();
    void check_timers();
    void check_tick();
    void check_gm_snapshot();
    void send_tx(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t w0, std::uint32_t w1);
    std::vector<std::uint32_t> take_event();
    void fill_event_ring_with_expiries();

    Bench& b_;
    milan::tb::Checker& ck_;
    std::vector<std::uint32_t> rx_tail_ = std::vector<std::uint32_t>(MBX_N_CH, 0);
    std::vector<std::uint32_t> tx_head_ = std::vector<std::uint32_t>(MBX_N_CH, 0);
    std::uint32_t evt_tail_ = 0;
};

template <class Bench>
void Suite<Bench>::check_reset_and_identity() {
    const std::uint32_t id = rd(MBX_REG_ID);
    ck_.hex("R0 ID.MAGIC", field(id, MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH), MBX_MAGIC);
    ck_.hex("R0 ID.MAJOR", field(id, MBX_ID_MAJOR_LSB, MBX_ID_MAJOR_WIDTH), MBX_VERSION_MAJOR);
    ck_.hex("R0 ID.MINOR", field(id, MBX_ID_MINOR_LSB, MBX_ID_MINOR_WIDTH), MBX_VERSION_MINOR);
    const std::uint32_t caps = rd(MBX_REG_CAPS);
    ck_.dec("R0 CAPS.N_CH", field(caps, MBX_CAPS_N_CH_LSB, MBX_CAPS_N_CH_WIDTH), MBX_N_CH);
    ck_.dec("R0 CAPS.N_IF", field(caps, MBX_CAPS_N_IF_LSB, MBX_CAPS_N_IF_WIDTH), MBX_N_IF);
    ck_.dec("R0 CAPS.N_TIMERS", field(caps, MBX_CAPS_N_TIMERS_LSB, MBX_CAPS_N_TIMERS_WIDTH), MBX_N_TIMERS);
    ck_.dec("R0 CAPS.EVT_WORDS", 1u << field(caps, MBX_CAPS_EVT_WORDS_LOG2_LSB, MBX_CAPS_EVT_WORDS_LOG2_WIDTH),
            MBX_EVT_WORDS);
    const std::uint32_t zero_regs[] = {MBX_REG_IRQ_STATUS, MBX_REG_IRQ_ENABLE, MBX_REG_NOW_MS, MBX_REG_TICK_CTL,
                                       MBX_REG_OWN_EID_LO, MBX_REG_OWN_EID_HI, MBX_REG_FILTER_EN,
                                       MBX_REG_MAAP_COUNT, MBX_REG_EVT_HEAD, MBX_REG_EVT_TAIL, MBX_REG_BUS_ERR};
    bool all_zero = true;
    for (std::uint32_t off : zero_regs) {
        all_zero = all_zero && rd(off) == 0u;
    }
    ck_.that("R0 every status, enable and counter register reads 0 after reset", all_zero);
    bool ch_zero = true;
    for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
        for (std::uint32_t r = 0; r < MBX_CH_STRIDE; r += 4u) {
            ch_zero = ch_zero && rd(ch_reg(c, r)) == 0u;
        }
    }
    ck_.that("R0 every channel register reads 0 after reset", ch_zero);
    ck_.dec("R0 the interrupt is low after reset", b_.irq(), 0);
    b_.ms(3);
    ck_.dec("R0 NOW_MS counts the millisecond pulse", rd(MBX_REG_NOW_MS), 3);
}

template <class Bench>
void Suite<Bench>::check_register_masks() {
    struct Rw {
        std::uint32_t off;
        std::uint32_t mask;
        const char* what;
    };
    const Rw regs[] = {
        {MBX_REG_IRQ_ENABLE, 0x800001FFu, "R1 IRQ_ENABLE keeps RX[7:0], EVT and ERR only"},
        {MBX_REG_TICK_CTL, 0x00000001u, "R1 TICK_CTL keeps EN only"},
        {MBX_REG_OWN_EID_LO, 0xFFFFFFFFu, "R1 OWN_EID_LO keeps every bit"},
        {MBX_REG_OWN_EID_HI, 0xFFFFFFFFu, "R1 OWN_EID_HI keeps every bit"},
        {MBX_REG_MAAP_BASE_LO, 0xFFFFFFFFu, "R1 MAAP_BASE_LO keeps every bit"},
        {MBX_REG_MAAP_BASE_HI, 0x0000FFFFu, "R1 MAAP_BASE_HI keeps address bits 47:32 only"},
        {MBX_REG_MAAP_COUNT, 0x0000FFFFu, "R1 MAAP_COUNT keeps 16 bits"},
        {MBX_REG_TMR_DEADLINE, 0xFFFFFFFFu, "R1 TMR_DEADLINE keeps every bit"},
    };
    for (const Rw& r : regs) {
        wr(r.off, 0xFFFFFFFFu);
        ck_.hex(r.what, rd(r.off), r.mask);
        wr(r.off, 0u);
    }
    wr(MBX_REG_FILTER_EN, 0xFFFFFFFFu);
    ck_.hex("R1 FILTER_EN keeps OPEN[7:0] only", rd(MBX_REG_FILTER_EN), 0xFFu);
    wr(MBX_REG_FILTER_EN, 0u);
    wr(MBX_REG_NOW_MS, 0x12345678u);
    wr(MBX_REG_ID, 0u);
    ck_.that("R1 a write to a read-only register changes nothing",
             rd(MBX_REG_NOW_MS) < 100u && field(rd(MBX_REG_ID), MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH) == MBX_MAGIC);
}

template <class Bench>
void Suite<Bench>::check_partial_strobe_refused() {
    b_.write(MBX_REG_OWN_EID_LO, 0xA5A5A5A5u, 0x3);
    ck_.hex("R2 a write with a partial strobe leaves the register", rd(MBX_REG_OWN_EID_LO), 0);
    ck_.dec("R2 the refusal counts in BUS_ERR", rd(MBX_REG_BUS_ERR), 1);
    ck_.dec("R2 the refusal sets IRQ_STATUS.ERR",
            field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, MBX_IRQ_STATUS_ERR_WIDTH), 1);
    b_.idle(2);
    ck_.dec("R2 a cause that is not enabled leaves the line low", b_.irq(), 0);
    wr(MBX_REG_IRQ_ENABLE, 1u << MBX_IRQ_ENABLE_ERR_LSB);
    b_.idle(2);
    ck_.dec("R2 an enabled ERR raises the interrupt", b_.irq(), 1);
    wr(MBX_REG_IRQ_STATUS, 1u << MBX_IRQ_STATUS_ERR_LSB);
    b_.idle(2);
    ck_.dec("R2 writing 1 to ERR clears it", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, 1), 0);
    ck_.dec("R2 and the interrupt falls", b_.irq(), 0);
    wr(MBX_REG_TMR_CMD, (3u << MBX_TMR_CMD_OP_LSB) | 1u);
    wr(MBX_REG_TMR_CMD, (1u << MBX_TMR_CMD_OP_LSB) | MBX_N_TIMERS);
    ck_.dec("R2 a TMR_CMD with no op, or naming no slot, counts in BUS_ERR", rd(MBX_REG_BUS_ERR), 3);
    ck_.dec("R2 a write that reaches no register is still answered", b_.bus_timeouts, 0);
}

template <class Bench>
void Suite<Bench>::check_adp_filter() {
    const auto discover0 = mbx_tb::adpdu(2, 0);
    b_.send_frame(discover0, 0);
    b_.drain_rx();
    ck_.dec("F0 a closed channel stores nothing", rx_head(kAdp), 0);
    ck_.dec("F0 and counts nothing", rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)) + rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 0);
    open(1u << kAdp);
    b_.ms(7);
    b_.send_frame(discover0, 0);
    b_.drain_rx();
    ck_.dec("F1 ENTITY_DISCOVER for entity_id 0 is committed whole", rx_head(kAdp), 2u + 82u / 4u + 1u);
    ck_.dec("F1 RX_PASS counts it", rx_pass(kAdp), 1);
    ck_.dec("F1 IRQ_STATUS.RX shows the channel", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_RX_LSB, 8),
            1u << kAdp);
    const Record r = peek(kAdp);
    ck_.dec("F1 record LEN", field(r.w0, MBX_RXREC_W0_LEN_LSB, MBX_RXREC_W0_LEN_WIDTH), 82);
    ck_.dec("F1 record KIND", field(r.w0, MBX_RXREC_W0_KIND_LSB, MBX_RXREC_W0_KIND_WIDTH), MBX_RX_KIND);
    ck_.dec("F1 record IF", field(r.w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH), 0);
    ck_.dec("F1 record ARRIVAL_MS is NOW_MS at the last byte", r.w1, 7);
    ck_.that("F1 frame byte k is ring word 2 + k/4, bits 8*(k%4) (little-endian lanes)",
             same_bytes(r.bytes, discover0));
    wr(MBX_REG_IRQ_ENABLE, 1u << kAdp);
    b_.idle(2);
    ck_.dec("F1 an enabled RX level raises the interrupt", b_.irq(), 1);
    release(kAdp, r);
    b_.idle(2);
    ck_.dec("F1 releasing the record (RX_TAIL) drops the level and the line", b_.irq(), 0);
    check_adp_terms();
}

template <class Bench>
void Suite<Bench>::check_adp_terms() {
    b_.send_frame(mbx_tb::adpdu(2, kOwnEid), 0);
    b_.drain_rx();
    ck_.dec("F2 ENTITY_DISCOVER for this entity passes", rx_pass(kAdp), 2);
    release(kAdp, peek(kAdp));
    b_.send_frame(mbx_tb::adpdu(2, kForeignEid), 0);
    b_.send_frame(mbx_tb::adpdu(0, 0), 0);
    b_.send_frame(mbx_tb::adpdu(0, kOwnEid), 0);
    b_.send_frame(mbx_tb::adpdu(1, kOwnEid), 0);
    b_.drain_rx();
    ck_.dec("F2 ENTITY_DISCOVER for another entity, and AVAILABLE or DEPARTING, are not passed", rx_pass(kAdp), 2);
    ck_.dec("F2 and are dropped uncounted (not addressed to this entity)",
            rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)) + rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 0);
    b_.send_frame(mbx_tb::adpdu(2, 0, 25), 0);
    b_.drain_rx();
    ck_.dec("F2 a DISCOVER truncated inside its entity_id field is not passed", rx_pass(kAdp), 2);
}

template <class Bench>
void Suite<Bench>::check_classification() {
    open((1u << MBX_N_CH) - 1u);
    wr(MBX_REG_MAAP_BASE_LO, 0x00000100u);
    wr(MBX_REG_MAAP_BASE_HI, 0x91E0u);
    wr(MBX_REG_MAAP_COUNT, 8u);
    check_classification_avtp();
    check_classification_other();
}

template <class Bench>
void Suite<Bench>::check_classification_avtp() {
    b_.send_frame(mbx_tb::acmpdu(0, kOwnEid, kForeignEid), 0);
    b_.send_frame(mbx_tb::acmpdu(2, kForeignEid, kOwnEid), 0);
    b_.send_frame(mbx_tb::acmpdu(2, kForeignEid, kForeignEid), 0);
    b_.drain_rx();
    ck_.dec("C0 ACMP to this talker or this listener passes; to neither does not", rx_pass(MBX_CH_ACMP), 2);
    ck_.dec("C0 no ACMP frame lands in the ADP ring", rx_pass(kAdp), 0);
    b_.send_frame(mbx_tb::aecpdu(kOwnEid), 0);
    b_.send_frame(mbx_tb::aecpdu(kForeignEid), 0);
    b_.drain_rx();
    ck_.dec("C1 AECP to this entity passes; to another does not", rx_pass(MBX_CH_AECP), 1);
    const std::uint64_t base = 0x91E000000100ull;
    b_.send_frame(mbx_tb::maap(1, base + 6, 4), 0);
    b_.send_frame(mbx_tb::maap(2, base - 2, 3), 0);
    b_.send_frame(mbx_tb::maap(3, base + 7, 1), 0);
    b_.send_frame(mbx_tb::maap(1, base + 8, 4), 0);
    b_.send_frame(mbx_tb::maap(1, base - 4, 4), 0);
    b_.send_frame(mbx_tb::maap(1, base + 2, 0), 0);
    b_.send_frame(mbx_tb::maap(0, base + 2, 2), 0);
    b_.drain_rx();
    ck_.dec("C2 MAAP PROBE/DEFEND/ANNOUNCE overlapping this range pass; adjacent, empty or other types do not",
            rx_pass(MBX_CH_MAAP), 3);
}

template <class Bench>
void Suite<Bench>::check_classification_other() {
    const std::vector<std::uint8_t> body = {0x01, 0x22, 0x04, 0x00, 0x00};
    b_.send_frame(mbx_tb::mrp(mbx_tb::kEtherMsrp, body), 0);
    b_.send_frame(mbx_tb::mrp(mbx_tb::kEtherMvrp, body), 0);
    b_.drain_rx();
    ck_.dec("C3 every MSRP and MVRP PDU reaches the SRP ring", rx_pass(MBX_CH_SRP), 2);
    const Record r = peek(MBX_CH_SRP);
    ck_.that("C3 the MRPDU is frame bytes 14.. of the record, ProtocolVersion first (lwSRP's mrp_rx input)",
             r.bytes.size() == 20u && r.bytes[14] == 0x00u && r.bytes[15] == 0x01u && r.bytes[16] == 0x22u);
    auto tagged = mbx_tb::adpdu(2, 0, 86);
    for (std::size_t i = 85; i >= 16; --i) {
        tagged[i] = tagged[i - 4];
    }
    tagged[12] = 0x81;
    tagged[13] = 0x00;
    b_.send_frame(tagged, 0);
    b_.send_frame(mbx_tb::eth(0x91E0F0010000ull, 0x88F7, 64), 0);
    auto short_frame = mbx_tb::adpdu(2, 0, 14);
    b_.send_frame(short_frame, 0);
    b_.drain_rx();
    std::uint32_t total = 0;
    for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
        total += rx_pass(c);
    }
    ck_.dec("C4 a tagged frame, a foreign EtherType and a frame ending before the subtype pass nowhere", total, 8);
}

template <class Bench>
void Suite<Bench>::check_drop_never_touches_an_unread_record() {
    open(1u << kAdp);
    static const std::uint32_t words[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;
    const std::uint32_t per = 2u + 21u;
    const std::uint32_t fit = words[kAdp] / per;
    std::vector<std::vector<std::uint8_t>> sent;
    for (std::uint32_t i = 0; i < fit; ++i) {
        auto f = mbx_tb::adpdu(2, 0);
        f[60] = static_cast<std::uint8_t>(i + 1u);
        sent.push_back(f);
        b_.send_frame(f, 0);
        b_.drain_rx();
        b_.ms(MBX_CH_ADP_RATE_REFILL_MS);
    }
    ck_.dec("D0 records fill the ring to the last whole one", rx_pass(kAdp), fit);
    auto extra = mbx_tb::adpdu(2, 0);
    extra[60] = 0xEE;
    b_.send_frame(extra, 0);
    b_.drain_rx();
    ck_.dec("D0 a frame the free space cannot hold counts in RX_DROP", rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)), 1);
    ck_.dec("D0 and is not committed", rx_pass(kAdp), fit);
    bool intact = true;
    for (std::uint32_t i = 0; i < fit; ++i) {
        const Record r = peek(kAdp);
        intact = intact && same_bytes(r.bytes, sent[i]);
        release(kAdp, r);
    }
    ck_.that("D0 every unread record survives the dropped frame byte for byte", intact);
    b_.send_frame(extra, 0);
    b_.drain_rx();
    ck_.dec("D0 once released, the space takes the next frame", rx_pass(kAdp), fit + 1u);
    b_.send_frame(mbx_tb::adpdu(2, 0, MBX_CH_ADP_MAX_FRAME_BYTES + 2u), 0);
    b_.drain_rx();
    ck_.dec("D1 a frame over max_frame_bytes counts in RX_DROP", rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)), 2);
    ck_.dec("D1 and sets IRQ_STATUS.ERR", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, 1), 1);
    ck_.that("D1 the record after it is still the next frame's", same_bytes(peek(kAdp).bytes, extra));
}

template <class Bench>
void Suite<Bench>::check_rate_limit() {
    open(1u << kAdp);
    const std::uint32_t burst = MBX_CH_ADP_RATE_BURST;
    for (std::uint32_t i = 0; i < burst + 2u; ++i) {
        b_.send_frame(mbx_tb::adpdu(2, kOwnEid), 0);
    }
    b_.drain_rx(40000);
    ck_.dec("T0 a burst of the bucket's depth passes", rx_pass(kAdp), burst);
    ck_.dec("T0 the frames past it count in RATE_DROP", rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 2);
    for (std::uint32_t i = 0; i < burst; ++i) {
        release(kAdp, peek(kAdp));
    }
    b_.ms(MBX_CH_ADP_RATE_REFILL_MS);
    b_.send_frame(mbx_tb::adpdu(2, kOwnEid), 0);
    b_.send_frame(mbx_tb::adpdu(2, kOwnEid), 0);
    b_.drain_rx();
    ck_.dec("T1 one refill period buys exactly one more frame", rx_pass(kAdp), burst + 1u);
    ck_.dec("T1 and the next is refused again", rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 3);
}

template <class Bench>
void Suite<Bench>::send_tx(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t w0, std::uint32_t w1) {
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
    static const std::uint32_t words[MBX_N_CH] = MBX_CH_TX_WORDS_TBL;
    auto put = [&](std::uint32_t i, std::uint32_t v) { wr(base[ch] + 4u * ((tx_head_[ch] + i) & (words[ch] - 1u)), v); };
    put(0, w0);
    put(1, w1);
    for (std::size_t k = 0; k < frame.size(); k += 4) {
        std::uint32_t w = 0;
        for (std::size_t j = 0; j < 4 && k + j < frame.size(); ++j) {
            w |= static_cast<std::uint32_t>(frame[k + j]) << (8u * j);
        }
        put(2u + static_cast<std::uint32_t>(k / 4), w);
    }
    tx_head_[ch] = (tx_head_[ch] + 2u + static_cast<std::uint32_t>((frame.size() + 3u) / 4u)) & 0xFFFFu;
    wr(ch_reg(ch, MBX_CH_REG_TX_HEAD), tx_head_[ch]);
}

inline std::uint32_t tx_w0(std::size_t len, std::uint32_t iface, std::uint32_t kind) {
    return (static_cast<std::uint32_t>(len) << MBX_TXREC_W0_LEN_LSB) | (iface << MBX_TXREC_W0_IF_LSB) |
           (kind << MBX_TXREC_W0_KIND_LSB);
}

template <class Bench>
void Suite<Bench>::check_tx_merge() {
    tx_head_.assign(MBX_N_CH, 0);
    b_.tx_ready_pattern(0x5A);
    auto a = mbx_tb::adpdu(0, kOwnEid);
    a[40] = 0x3C;
    auto m = mbx_tb::maap(1, 0x91E000000100ull, 8);
    send_tx(kAdp, a, tx_w0(a.size(), 0, MBX_TX_KIND), 0);
    send_tx(MBX_CH_MAAP, m, tx_w0(m.size(), 0, MBX_TX_KIND), 0);
    send_tx(kAdp, m, tx_w0(m.size(), 0, MBX_TX_KIND), 0);
    ck_.that("X0 three committed records leave as three frames under backpressure", b_.wait_tx(3));
    if (b_.tx_frames.size() >= 3) {
        ck_.that("X0 the first frame leaves byte for byte, wire order", same_bytes(b_.tx_frames[0].bytes, a));
        ck_.dec("X0 with its channel", b_.tx_frames[0].channel, kAdp);
        ck_.dec("X0 round-robin: the other channel's record goes next", b_.tx_frames[1].channel, MBX_CH_MAAP);
        ck_.that("X0 and its bytes are its own", same_bytes(b_.tx_frames[1].bytes, m));
        ck_.dec("X0 then the first channel's second record", b_.tx_frames[2].channel, kAdp);
    }
    b_.idle(8);
    ck_.dec("X0 TX_TAIL reaches TX_HEAD once the frames have left", rd(ch_reg(kAdp, MBX_CH_REG_TX_TAIL)),
            tx_head_[kAdp]);
    ck_.dec("X0 no record was refused", rd(ch_reg(kAdp, MBX_CH_REG_TX_ERR)), 0);
}

template <class Bench>
void Suite<Bench>::check_tx_refusals() {
    tx_head_.assign(MBX_N_CH, 0);
    const auto a = mbx_tb::adpdu(0, kOwnEid);
    struct Bad {
        std::uint32_t w0;
        std::uint32_t w1;
    };
    const Bad bad[] = {
        {tx_w0(a.size(), 0, MBX_RX_KIND), 0},
        {tx_w0(a.size(), 0, MBX_TX_KIND), 1},
        {tx_w0(a.size(), MBX_N_IF, MBX_TX_KIND), 0},
        {tx_w0(13, 0, MBX_TX_KIND), 0},
        {tx_w0(MBX_CH_ADP_MAX_FRAME_BYTES + 2u, 0, MBX_TX_KIND), 0},
    };
    std::uint32_t n = 0;
    for (const Bad& x : bad) {
        send_tx(kAdp, a, x.w0, x.w1);
        b_.idle(40);
        ++n;
        ck_.dec("X1 a malformed TX record counts once in TX_ERR", rd(ch_reg(kAdp, MBX_CH_REG_TX_ERR)), n);
        ck_.dec("X1 and flushes the ring to TX_HEAD", rd(ch_reg(kAdp, MBX_CH_REG_TX_TAIL)), tx_head_[kAdp]);
    }
    ck_.dec("X1 no malformed record reached the wire", b_.tx_frames.size(), 0);
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
    wr(base[kAdp] + 4u * (tx_head_[kAdp] & (MBX_CH_ADP_TX_WORDS - 1u)), tx_w0(a.size(), 0, MBX_TX_KIND));
    wr(base[kAdp] + 4u * ((tx_head_[kAdp] + 1u) & (MBX_CH_ADP_TX_WORDS - 1u)), 0);
    tx_head_[kAdp] = (tx_head_[kAdp] + 2u) & 0xFFFFu;
    wr(ch_reg(kAdp, MBX_CH_REG_TX_HEAD), tx_head_[kAdp]);
    b_.idle(40);
    ck_.dec("X1 a header whose payload lies past TX_HEAD is refused, not read", rd(ch_reg(kAdp, MBX_CH_REG_TX_ERR)),
            n + 1u);
    send_tx(kAdp, a, tx_w0(a.size(), 0, MBX_TX_KIND), 0);
    ck_.that("X1 the ring carries the next good record after the refusals", b_.wait_tx(1) &&
             same_bytes(b_.tx_frames[0].bytes, a));
}

template <class Bench>
std::vector<std::uint32_t> Suite<Bench>::take_event() {
    std::vector<std::uint32_t> w;
    if ((rd(MBX_REG_EVT_HEAD) & 0xFFFFu) == evt_tail_) {
        return w;
    }
    for (std::uint32_t i = 0; i < MBX_EV_WORDS; ++i) {
        w.push_back(rd(MBX_EVT_BASE + 4u * ((evt_tail_ + i) & (MBX_EVT_WORDS - 1u))));
    }
    evt_tail_ = (evt_tail_ + MBX_EV_WORDS) & 0xFFFFu;
    wr(MBX_REG_EVT_TAIL, evt_tail_);
    return w;
}

inline std::uint32_t ev_type(const std::vector<std::uint32_t>& e) {
    return e.empty() ? 0u : field(e[0], MBX_EVREC_W0_TYPE_LSB, MBX_EVREC_W0_TYPE_WIDTH);
}

template <class Bench>
void Suite<Bench>::check_link_and_gm_events() {
    ck_.that("E0 no event before anything changes", take_event().empty());
    wr(MBX_REG_IRQ_ENABLE, 1u << MBX_IRQ_ENABLE_EVT_LSB);
    b_.ms(2);
    b_.set_link(1);
    b_.idle(8);
    ck_.dec("E0 an enabled event level raises the interrupt", b_.irq(), 1);
    auto e = take_event();
    ck_.dec("E0 a link rise posts a LINK event", ev_type(e), MBX_EV_TYPE_LINK);
    ck_.dec("E0 carrying the level", e.size() == 4 ? field(e[1], MBX_EV_LINK_W1_UP_LSB, 1) : 9u, 1);
    ck_.dec("E0 and NOW_MS", e.size() == 4 ? e[3] : 0u, 2);
    b_.idle(2);
    ck_.dec("E0 consuming it (EVT_TAIL) drops the line", b_.irq(), 0);
    b_.gm_change(0, 0xA1A2A3A4A5A6A7A8ull, 7);
    b_.idle(8);
    e = take_event();
    ck_.dec("E1 a grandmaster change posts a GM event", ev_type(e), MBX_EV_TYPE_GM);
    ck_.hex("E1 GM ID_LO", e.size() == 4 ? e[1] : 0u, 0xA5A6A7A8u);
    ck_.hex("E1 GM ID_HI", e.size() == 4 ? e[2] : 0u, 0xA1A2A3A4u);
    ck_.dec("E1 GM DOMAIN", e.size() == 4 ? field(e[3], MBX_EV_GM_W3_DOMAIN_LSB, 8) : 0u, 7);
    ck_.dec("E1 SEQ counts the postings", e.size() == 4 ? field(e[0], MBX_EVREC_W0_SEQ_LSB, 16) : 0u, 1);
    fill_event_ring_with_expiries();
    b_.set_link(0);
    b_.idle(30);
    b_.set_link(1);
    b_.idle(30);
    b_.set_link(0);
    b_.idle(30);
    std::uint32_t links = 0;
    std::uint32_t last_up = 9;
    for (std::vector<std::uint32_t> x = take_event(); !x.empty(); x = take_event()) {
        if (ev_type(x) == MBX_EV_TYPE_LINK) {
            ++links;
            last_up = field(x[1], MBX_EV_LINK_W1_UP_LSB, 1);
        }
        b_.idle(8);
    }
    ck_.dec("E2 a link that flapped while the ring was full posts once", links, 1);
    ck_.dec("E2 with its level at posting time", last_up, 0);
}

template <class Bench>
void Suite<Bench>::fill_event_ring_with_expiries() {
    const std::uint32_t now = rd(MBX_REG_NOW_MS);
    for (std::uint32_t s = 0; s < MBX_EVT_WORDS / MBX_EV_WORDS; ++s) {
        wr(MBX_REG_TMR_DEADLINE, now);
        wr(MBX_REG_TMR_CMD, (1u << MBX_TMR_CMD_OP_LSB) | ((0x100u + s) << MBX_TMR_CMD_TAG_LSB) | (s % MBX_N_TIMERS));
        b_.idle(MBX_N_TIMERS + 8u);
    }
    ck_.dec("E2 the ring is full of expiries", (rd(MBX_REG_EVT_HEAD) - evt_tail_) & 0xFFFFu, MBX_EVT_WORDS);
}

template <class Bench>
void Suite<Bench>::check_timers() {
    const std::uint32_t now = rd(MBX_REG_NOW_MS);
    auto arm = [&](std::uint32_t slot, std::uint32_t tag, std::uint32_t dl) {
        wr(MBX_REG_TMR_DEADLINE, dl);
        wr(MBX_REG_TMR_CMD, (1u << MBX_TMR_CMD_OP_LSB) | (tag << MBX_TMR_CMD_TAG_LSB) | slot);
    };
    arm(3, 0x1234, now + 5u);
    arm(4, 0x4444, now + 3u);
    wr(MBX_REG_TMR_CMD, (2u << MBX_TMR_CMD_OP_LSB) | 4u);
    arm(5, 0x0001, now + 4u);
    arm(5, 0x0002, now + 6u);
    b_.ms(4);
    ck_.that("M0 no event by +4 ms: slot 3 not before its deadline, slot 4 cancelled, slot 5 re-armed",
             take_event().empty());
    b_.ms(1);
    auto e = take_event();
    ck_.dec("M0 slot 3 expires at its deadline", ev_type(e), MBX_EV_TYPE_TIMER);
    ck_.hex("M0 with the tag of its arm", e.size() == 4 ? field(e[1], MBX_EV_TIMER_W1_TAG_LSB, 16) : 0u, 0x1234);
    ck_.dec("M0 and its slot", e.size() == 4 ? field(e[1], MBX_EV_TIMER_W1_SLOT_LSB, 8) : 0u, 3);
    ck_.dec("M0 and its deadline", e.size() == 4 ? e[2] : 0u, now + 5u);
    b_.ms(1);
    e = take_event();
    ck_.hex("M1 a re-armed slot expires once, with the second arm's tag",
            e.size() == 4 ? field(e[1], MBX_EV_TIMER_W1_TAG_LSB, 16) : 0u, 0x0002);
    b_.ms(5);
    ck_.that("M1 a cancelled slot and the replaced arm post nothing", take_event().empty());
    arm(6, 0x0066, rd(MBX_REG_NOW_MS) - 1u);
    b_.idle(MBX_N_TIMERS + 8u);
    e = take_event();
    ck_.hex("M2 a deadline already past expires at once",
            e.size() == 4 ? field(e[1], MBX_EV_TIMER_W1_TAG_LSB, 16) : 0u, 0x0066);
}

template <class Bench>
void Suite<Bench>::check_tick() {
    b_.ms(25);
    ck_.that("K0 no TICK while TICK_CTL.EN is clear", take_event().empty());
    wr(MBX_REG_TICK_CTL, 1);
    b_.ms(MBX_TICK_MS - 1u);
    ck_.that("K0 no TICK before one period", take_event().empty());
    b_.ms(1);
    auto e = take_event();
    ck_.dec("K0 one period posts a TICK", ev_type(e), MBX_EV_TYPE_TICK);
    ck_.dec("K0 counting one tick", e.size() == 4 ? field(e[1], MBX_EV_TICK_W1_COUNT_LSB, 16) : 0u, 1);
    fill_event_ring_with_expiries();
    b_.ms(5u * MBX_TICK_MS);
    std::uint32_t ticks = 0;
    std::uint32_t records = 0;
    for (std::vector<std::uint32_t> x = take_event(); !x.empty(); x = take_event()) {
        if (ev_type(x) == MBX_EV_TYPE_TICK) {
            ticks += field(x[1], MBX_EV_TICK_W1_COUNT_LSB, 16);
            ++records;
        }
        b_.idle(8);
    }
    ck_.dec("K1 ticks counted while the ring was full are posted as one record", records, 1);
    ck_.dec("K1 carrying every tick", ticks, 5);
    wr(MBX_REG_TICK_CTL, 0);
    b_.ms(3u * MBX_TICK_MS);
    ck_.that("K2 clearing EN stops the ticks", take_event().empty());
}

template <class Bench>
void Suite<Bench>::check_gm_snapshot() {
    b_.set_gm(0, 0x1111111122222222ull, 3);
    b_.idle(2);
    const std::uint32_t lo = rd(MBX_IF_BASE + MBX_IF_REG_GM_LO);
    b_.set_gm(0, 0x3333333344444444ull, 9);
    b_.idle(2);
    const std::uint32_t hi = rd(MBX_IF_BASE + MBX_IF_REG_GM_HI);
    const std::uint32_t dom = rd(MBX_IF_BASE + MBX_IF_REG_DOMAIN);
    ck_.hex("G0 GM_LO reads the live identity", lo, 0x22222222u);
    ck_.hex("G0 GM_HI reads the snapshot GM_LO took", hi, 0x11111111u);
    ck_.dec("G0 DOMAIN reads the same snapshot", dom, 3);
}

}  // namespace mbx_tb

#endif  // MBX_SUITE_HPP
