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
#include <string>
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
inline std::uint32_t iff_reg(std::uint32_t i, std::uint32_t reg) { return MBX_IFF_BASE + MBX_IFF_STRIDE * i + reg; }
//! Register `reg` of entry e of interface i's bound-talker table.
inline std::uint32_t bnd_reg(std::uint32_t i, std::uint32_t e, std::uint32_t reg) {
    return MBX_BND_BASE + MBX_BND_STRIDE * i + MBX_BND_ENTRY_STRIDE * e + reg;
}

//! The interface indices the ingress stream can name: every configured
//! interface and, where the index is wider, ones with no interface behind them.
inline constexpr std::uint32_t kIfIndices = 1u << MBX_IF_W;

//! The checks are graded by `Check`: milan::tb::Checker on the RTL benches,
//! and on the host model a GoogleTest adapter (sw/firmware/ctrl/test/
//! model_suite.cpp), which runs each group as a test of its own. A Check
//! answers hex(), dec() and that() as Checker does.
template <class Bench, class Check = milan::tb::Checker>
class Suite {
 public:
    Suite(Bench& bench, Check& check) : b_(bench), ck_(check) {}

    //! The groups run() runs, in its order.
    static constexpr unsigned kGroups = 23;
    static constexpr const char* kGroupNames[kGroups] = {
        "ResetIdentityAndRegisterMasks", "PartialStrobeRefused", "AdpFilter", "Classification",
        "DropNeverTouchesAnUnreadRecord", "RateLimit", "TxMerge", "TxCommitOrder", "TxRefusals",
        "BadHostCounters", "LinkAndGmEvents", "Timers", "Tick", "GmSnapshot",
        // lane FC: the full-tuple filter (REQUIREMENTS.md section 1, NFR-SCOUT-08)
        "TupleControls", "TupleRejections", "StreamDataNeverDelivered", "AecpBothDirections",
        "OwnMacPerInterface", "FilterMismatchCount", "TokensApartFromTheFilter",
        // lane FC round 2: the MAAP DEFEND to own unicast (IEEE 1722-2016 B.2.1)
        "MaapDefendToOwnUnicast",
        // lane F3 round 2: the adp channel's bound talkers (#665, comment 6029368753)
        "AdpBoundTalkers"};

    void run() {
        for (unsigned g = 0; g < kGroups; ++g) {
            run_group(g);
        }
        ck_.dec("no bus access went unanswered", b_.bus_timeouts, 0);
    }

    //! The fabric's own timing around the bound-talker table (lane F3 round 3):
    //! a frame stalled inside its identity, and the copier beside the host,
    //! which only a cycle-by-cycle bench shows. sim_main runs it after run();
    //! the model, whose frames arrive whole, never does.
    void run_bound_timing() {
        restart();
        check_bound_timing();
        ck_.dec("no bus access went unanswered in the timing checks", b_.bus_timeouts, 0);
    }

    //! One group: the first on the bench's reset, every later one on a restart.
    void run_group(unsigned g) {
        if (g == 0) {
            b_.reset();
            check_reset_and_identity();
            check_register_masks();
            return;
        }
        restart();
        switch (g) {
        case 1: check_partial_strobe_refused(); break;
        case 2: check_adp_filter(); break;
        case 3: check_classification(); break;
        case 4: check_drop_never_touches_an_unread_record(); break;
        case 5: check_rate_limit(); break;
        case 6: check_tx_merge(); break;
        case 7: check_tx_commit_order(); break;
        case 8: check_tx_refusals(); break;
        case 9: check_bad_host_counters(); break;
        case 10: check_link_and_gm_events(); break;
        case 11: check_timers(); break;
        case 12: check_tick(); break;
        case 13: check_gm_snapshot(); break;
        case 14: check_tuple_controls(); break;
        case 15: check_tuple_rejections(); break;
        case 16: check_stream_data(); break;
        case 17: check_aecp_both_directions(); break;
        case 18: check_own_mac_per_interface(); break;
        case 19: check_filter_mismatch_count(); break;
        case 20: check_tokens_apart(); break;
        case 21: check_maap_defend(); break;
        default: check_adp_bound_talkers(); break;
        }
    }

 private:
    void restart() {
        b_.reset();
        rx_tail_.assign(MBX_N_CH, 0);
        evt_tail_ = 0;
        b_.tx_frames.clear();
        b_.tx_ready_pattern(0xFF);
        tx_seq_ = 0;
    }

    std::uint32_t rd(std::uint32_t off) { return b_.read(off); }
    void wr(std::uint32_t off, std::uint32_t v) { b_.write(off, v); }

    //! OWN_MAC of interface i, as the firmware writes it.
    void set_own_mac(std::uint32_t i, std::uint64_t mac) {
        wr(iff_reg(i, MBX_IFF_REG_OWN_MAC_LO), static_cast<std::uint32_t>(mac));
        wr(iff_reg(i, MBX_IFF_REG_OWN_MAC_HI), static_cast<std::uint32_t>(mac >> 32) & 0xFFFFu);
    }

    //! Entry e of interface i's bound-talker table, as the firmware writes it:
    //! BOUND_EN cleared first, then the identity, then BOUND_EN.
    void set_bound(std::uint32_t i, std::uint32_t e, std::uint64_t eid, bool en) {
        wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EN), 0u);
        wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_LO), static_cast<std::uint32_t>(eid));
        wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_HI), static_cast<std::uint32_t>(eid >> 32));
        wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EN), en ? 1u : 0u);
    }

    //! The firmware's bring-up order: identities first (OWN_EID, and interface
    //! i's own MAC, kOwnMac + i), then the channels.
    void open(std::uint32_t mask) {
        wr(MBX_REG_OWN_EID_LO, static_cast<std::uint32_t>(kOwnEid));
        wr(MBX_REG_OWN_EID_HI, static_cast<std::uint32_t>(kOwnEid >> 32));
        for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
            set_own_mac(i, kOwnMac + i);
        }
        wr(MBX_REG_FILTER_EN, mask);
    }

    std::uint32_t rx_head(std::uint32_t ch) { return rd(ch_reg(ch, MBX_CH_REG_RX_HEAD)); }
    std::uint32_t rx_pass(std::uint32_t ch) { return rd(ch_reg(ch, MBX_CH_REG_RX_PASS)); }
    std::uint32_t mismatches() { return rd(MBX_REG_FILTER_MISMATCH); }

    //! Where one offered frame went: the channel whose ring it reached
    //! (MBX_N_CH: none, no RX_HEAD and no RX_PASS moved anywhere), the record,
    //! and how much FILTER_MISMATCH moved.
    struct Verdict {
        std::uint32_t channel = MBX_N_CH;
        Record record;
        std::uint32_t mismatched = 0;
    };

    //! Offer one frame on interface `iface`, release what it committed, then
    //! give every token bucket a refill, so a run of offers grades the filter
    //! and never the rate limiter (TokensApartFromTheFilter grades that).
    Verdict offer(const std::vector<std::uint8_t>& f, unsigned iface = 0) {
        std::vector<std::uint32_t> pass;
        std::vector<std::uint32_t> head;
        for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
            pass.push_back(rx_pass(c));
            head.push_back(rx_head(c));
        }
        const std::uint32_t before = mismatches();
        b_.send_frame(f, iface);
        b_.drain_rx();
        Verdict v;
        v.mismatched = (mismatches() - before) & 0xFFFFu;
        for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
            if (rx_pass(c) != pass[c] || rx_head(c) != head[c]) {
                v.channel = v.channel == MBX_N_CH ? c : MBX_N_CH + 1u;   // two channels: never a channel
            }
        }
        if (v.channel < MBX_N_CH) {
            v.record = peek(v.channel);
            release(v.channel, v.record);
        }
        b_.ms(kRefillMs);
        return v;
    }

    //! offer() on interface `iface`, with the stream stalled after the
    //! frame's first `cut` bytes while `during` runs (the cycle-by-cycle bench
    //! only).
    template <class During>
    Verdict offer_stalled(const std::vector<std::uint8_t>& f, std::size_t cut, During during, unsigned iface = 0) {
        std::vector<std::uint32_t> pass;
        std::vector<std::uint32_t> head;
        for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
            pass.push_back(rx_pass(c));
            head.push_back(rx_head(c));
        }
        const std::uint32_t before = mismatches();
        b_.send_bytes(std::vector<std::uint8_t>(f.begin(), f.begin() + static_cast<std::ptrdiff_t>(cut)), iface, false);
        b_.drain_rx();
        during();
        b_.send_bytes(std::vector<std::uint8_t>(f.begin() + static_cast<std::ptrdiff_t>(cut), f.end()), iface, true);
        b_.drain_rx();
        Verdict v;
        v.mismatched = (mismatches() - before) & 0xFFFFu;
        for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
            if (rx_pass(c) != pass[c] || rx_head(c) != head[c]) {
                v.channel = v.channel == MBX_N_CH ? c : MBX_N_CH + 1u;
            }
        }
        if (v.channel < MBX_N_CH) {
            v.record = peek(v.channel);
            release(v.channel, v.record);
        }
        b_.ms(kRefillMs);
        return v;
    }

    //! Every channel's refill period at most: one token for every bucket.
    static constexpr std::uint32_t kRefillMs = 20;

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
    void check_tx_commit_order();
    void check_tx_refusals();
    void check_bad_host_counters();
    void check_link_and_gm_events();
    void check_timers();
    void check_tick();
    void check_gm_snapshot();
    void check_tuple_controls();
    void check_tuple_rejections();
    void check_rejected(const std::string& what, const std::vector<std::uint8_t>& f, std::uint32_t counted);
    void check_stream_data();
    void check_aecp_both_directions();
    void check_own_mac_per_interface();
    void check_filter_mismatch_count();
    void check_tokens_apart();
    void check_maap_defend();
    void check_adp_bound_talkers();
    void check_bound_table_per_interface();
    void check_bound_identity_bytes();
    void check_bound_reset();
    void check_bound_timing();
    void clear_bound();

    //! One row of the owner's table (REQUIREMENTS.md section 1): its valid
    //! frame, the channel it must reach, and whether it carries an AVTP subtype.
    struct Row {
        const char* name;
        std::uint32_t channel;
        std::vector<std::uint8_t> frame;
        bool avtp;
    };
    std::vector<Row> table_rows();
    void filter_up();
    void send_tx(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t w0, std::uint32_t w1);
    void send_tx_seq(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t seq);
    std::vector<std::uint32_t> take_event();
    void fill_event_ring_with_expiries();

    Bench& b_;
    Check& ck_;
    std::vector<std::uint32_t> rx_tail_ = std::vector<std::uint32_t>(MBX_N_CH, 0);
    std::vector<std::uint32_t> tx_head_ = std::vector<std::uint32_t>(MBX_N_CH, 0);
    std::uint32_t evt_tail_ = 0;
    std::uint32_t tx_seq_ = 0;   //!< the commit count send_tx stamps into SEQ, as the driver does
};

template <class Bench, class Check>
void Suite<Bench, Check>::check_reset_and_identity() {
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
                                       MBX_REG_MAAP_COUNT, MBX_REG_EVT_HEAD, MBX_REG_EVT_TAIL, MBX_REG_BUS_ERR,
                                       MBX_REG_FILTER_MISMATCH};
    bool all_zero = true;
    for (std::uint32_t off : zero_regs) {
        all_zero = all_zero && rd(off) == 0u;
    }
    ck_.that("R0 every status, enable and counter register reads 0 after reset", all_zero);
    bool mac_zero = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        mac_zero = mac_zero && rd(iff_reg(i, MBX_IFF_REG_OWN_MAC_LO)) == 0u && rd(iff_reg(i, MBX_IFF_REG_OWN_MAC_HI)) == 0u;
    }
    ck_.that("R0 every interface's OWN_MAC reads 0 after reset", mac_zero);
    bool bound_zero = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            bound_zero = bound_zero && rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_LO)) == 0u &&
                         rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_HI)) == 0u &&
                         rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EN)) == 0u;
        }
    }
    ck_.that("R0 every entry of every interface's bound-talker table reads 0 after reset", bound_zero);
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_register_masks() {
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
    wr(MBX_REG_FILTER_MISMATCH, 0x5555u);
    ck_.that("R1 a write to a read-only register changes nothing",
             rd(MBX_REG_NOW_MS) < 100u && field(rd(MBX_REG_ID), MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH) == MBX_MAGIC &&
                 rd(MBX_REG_FILTER_MISMATCH) == 0u);
    // each interface's own MAC, in its own block: interface i's write lands
    // in interface i's registers only
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        wr(iff_reg(i, MBX_IFF_REG_OWN_MAC_LO), 0xFFFFFFF0u + i);
        wr(iff_reg(i, MBX_IFF_REG_OWN_MAC_HI), 0xFFFFFFFFu - i);
    }
    bool own = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        own = own && rd(iff_reg(i, MBX_IFF_REG_OWN_MAC_LO)) == 0xFFFFFFF0u + i &&
              rd(iff_reg(i, MBX_IFF_REG_OWN_MAC_HI)) == ((0xFFFFFFFFu - i) & 0xFFFFu);
        set_own_mac(i, 0);
    }
    ck_.that("R1 OWN_MAC_LO keeps every bit and OWN_MAC_HI keeps MAC[47:32] only, per interface", own);
    // each bound-talker entry in its own registers: entry (i, e)'s write lands
    // there only, BOUND_EID keeps every bit and BOUND_EN keeps EN only
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            const std::uint32_t k = i * MBX_N_BOUND + e;
            wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_LO), 0xA5A50000u + k);
            wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_HI), 0x5A5A0000u + k);
            wr(bnd_reg(i, e, MBX_BND_REG_BOUND_EN), 0xFFFFFFFEu | (k & 1u));
        }
    }
    bool bound = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            const std::uint32_t k = i * MBX_N_BOUND + e;
            bound = bound && rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_LO)) == 0xA5A50000u + k &&
                    rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_HI)) == 0x5A5A0000u + k &&
                    rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EN)) == (k & 1u);
            set_bound(i, e, 0, false);
        }
    }
    ck_.that("R1 each bound-talker entry keeps BOUND_EID's every bit and BOUND_EN's EN only, per interface and entry",
             bound);
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_partial_strobe_refused() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_adp_filter() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_adp_terms() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_classification() {
    open((1u << MBX_N_CH) - 1u);
    wr(MBX_REG_MAAP_BASE_LO, 0x00000100u);
    wr(MBX_REG_MAAP_BASE_HI, 0x91E0u);
    wr(MBX_REG_MAAP_COUNT, 8u);
    check_classification_avtp();
    check_classification_other();
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_classification_avtp() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_classification_other() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_drop_never_touches_an_unread_record() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_rate_limit() {
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

//! Commit one TX record; word 1 is `w1` with the next commit count in SEQ.
template <class Bench, class Check>
void Suite<Bench, Check>::send_tx(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t w0, std::uint32_t w1) {
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
    static const std::uint32_t words[MBX_N_CH] = MBX_CH_TX_WORDS_TBL;
    auto put = [&](std::uint32_t i, std::uint32_t v) { wr(base[ch] + 4u * ((tx_head_[ch] + i) & (words[ch] - 1u)), v); };
    put(0, w0);
    put(1, w1 | ((tx_seq_ & 0xFFFFu) << MBX_TXREC_W1_SEQ_LSB));
    tx_seq_ = (tx_seq_ + 1u) & 0xFFFFu;
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_tx_merge() {
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
        ck_.dec("X0 commit order: the other channel's record goes next", b_.tx_frames[1].channel, MBX_CH_MAAP);
        ck_.that("X0 and its bytes are its own", same_bytes(b_.tx_frames[1].bytes, m));
        ck_.dec("X0 then the first channel's second record", b_.tx_frames[2].channel, kAdp);
    }
    b_.idle(8);
    ck_.dec("X0 TX_TAIL reaches TX_HEAD once the frames have left", rd(ch_reg(kAdp, MBX_CH_REG_TX_TAIL)),
            tx_head_[kAdp]);
    ck_.dec("X0 no record was refused", rd(ch_reg(kAdp, MBX_CH_REG_TX_ERR)), 0);
}

//! A well-formed TX record of channel `ch` whose SEQ is `seq`, not the commit count.
template <class Bench, class Check>
void Suite<Bench, Check>::send_tx_seq(std::uint32_t ch, const std::vector<std::uint8_t>& frame, std::uint32_t seq) {
    const std::uint32_t keep = tx_seq_;
    tx_seq_ = seq;
    send_tx(ch, frame, tx_w0(frame.size(), 0, MBX_TX_KIND), 0);
    tx_seq_ = keep;
}

//! The channels the frames left on, in order.
inline std::vector<std::uint32_t> channels_of(const std::vector<TxFrame>& frames) {
    std::vector<std::uint32_t> out;
    for (const TxFrame& f : frames) {
        out.push_back(f.channel);
    }
    return out;
}

// Records leave in commit order across channels (the #653 case: an ACMP
// response before the AECP notification it causes), whichever channel the
// merge served last and however long the sink stalled.
template <class Bench, class Check>
void Suite<Bench, Check>::check_tx_commit_order() {
    tx_head_.assign(MBX_N_CH, 0);
    const std::uint32_t acmp = MBX_CH_ACMP;
    const std::uint32_t aecp = MBX_CH_AECP;
    const auto r1 = mbx_tb::acmpdu(1, kOwnEid, kForeignEid);
    const auto r2 = mbx_tb::acmpdu(7, kOwnEid, kForeignEid);
    const auto note = mbx_tb::aecpdu(kForeignEid);
    b_.tx_ready_pattern(0x00);
    send_tx(acmp, r1, tx_w0(r1.size(), 0, MBX_TX_KIND), 0);
    b_.idle(40);
    send_tx(acmp, r2, tx_w0(r2.size(), 0, MBX_TX_KIND), 0);
    send_tx(aecp, note, tx_w0(note.size(), 0, MBX_TX_KIND), 0);
    b_.idle(40);
    b_.tx_ready_pattern(0xFF);
    ck_.that("X2 three records committed behind a stalled sink all leave", b_.wait_tx(3));
    ck_.that("X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame leave as 1, 1, 2",
             channels_of(b_.tx_frames) == std::vector<std::uint32_t>{acmp, acmp, aecp});
    if (b_.tx_frames.size() == 3) {
        ck_.that("X2 each with its own bytes", same_bytes(b_.tx_frames[0].bytes, r1) &&
                 same_bytes(b_.tx_frames[1].bytes, r2) && same_bytes(b_.tx_frames[2].bytes, note));
    }

    // From another origin: the merge served SRP last, and AECP, ACMP and
    // ADP are committed in that order, which is not the channel order.
    b_.tx_frames.clear();
    const auto s = mbx_tb::mrp(mbx_tb::kEtherMsrp, std::vector<std::uint8_t>(20, 0));
    const auto a = mbx_tb::adpdu(0, kOwnEid);
    b_.tx_ready_pattern(0x00);
    send_tx(MBX_CH_SRP, s, tx_w0(s.size(), 0, MBX_TX_KIND), 0);
    b_.idle(40);
    send_tx(aecp, note, tx_w0(note.size(), 0, MBX_TX_KIND), 0);
    send_tx(acmp, r1, tx_w0(r1.size(), 0, MBX_TX_KIND), 0);
    send_tx(kAdp, a, tx_w0(a.size(), 0, MBX_TX_KIND), 0);
    b_.idle(40);
    b_.tx_ready_pattern(0xFF);
    ck_.that("X2 after an SRP frame, AECP, ACMP and ADP leave in the order they were committed",
             b_.wait_tx(4) && channels_of(b_.tx_frames) ==
                                  std::vector<std::uint32_t>{MBX_CH_SRP, aecp, acmp, kAdp});

    // Across the 16-bit wrap of SEQ, 0xFFFF comes before 0x0000. A first
    // record (SEQ 0xFFFE) holds the stalled sink, so the merge chooses
    // between the two with both committed.
    b_.tx_frames.clear();
    b_.tx_ready_pattern(0x00);
    send_tx_seq(MBX_CH_SRP, s, 0xFFFEu);
    b_.idle(40);
    send_tx_seq(aecp, note, 0x0000u);
    send_tx_seq(acmp, r1, 0xFFFFu);
    b_.idle(40);
    b_.tx_ready_pattern(0xFF);
    ck_.that("X2 SEQ 0xFFFF leaves before SEQ 0x0000 (modulo 2^16)",
             b_.wait_tx(3) && channels_of(b_.tx_frames) == std::vector<std::uint32_t>{MBX_CH_SRP, acmp, aecp});

    // Equal SEQs leave round-robin from the channel served last: after an
    // ACMP frame, MAAP (channel 3) goes before ADP (channel 0).
    b_.tx_frames.clear();
    b_.tx_ready_pattern(0x00);
    send_tx_seq(acmp, r1, 0x00FFu);
    b_.idle(40);
    send_tx_seq(kAdp, a, 0x0100u);
    send_tx_seq(MBX_CH_MAAP, mbx_tb::maap(1, 0x91E000000100ull, 8), 0x0100u);
    b_.idle(40);
    b_.tx_ready_pattern(0xFF);
    ck_.that("X2 equal SEQs leave round-robin from the channel served last",
             b_.wait_tx(3) && channels_of(b_.tx_frames) == std::vector<std::uint32_t>{acmp, MBX_CH_MAAP, kAdp});
    b_.idle(8);
    bool drained = true;
    for (std::uint32_t c = 0; c < MBX_N_CH; ++c) {
        drained = drained && rd(ch_reg(c, MBX_CH_REG_TX_TAIL)) == tx_head_[c];
    }
    ck_.that("X2 every TX_TAIL reaches its TX_HEAD", drained);
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_tx_refusals() {
    tx_head_.assign(MBX_N_CH, 0);
    const auto a = mbx_tb::adpdu(0, kOwnEid);
    struct Bad {
        std::uint32_t w0;
        std::uint32_t w1;
    };
    const Bad bad[] = {
        {tx_w0(a.size(), 0, MBX_RX_KIND), 0},
        {tx_w0(a.size(), 0, MBX_TX_KIND), 1u << MBX_TXREC_W1_RSVD_LSB},
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

// A wrong host counter (a partial reset, a driver bug) never lets the fabric
// write over a ring: an RX_TAIL or EVT_TAIL out of range leaves no free word,
// and a TX_HEAD more than the ring ahead of TX_TAIL is refused.
template <class Bench, class Check>
void Suite<Bench, Check>::check_bad_host_counters() {
    open(1u << kAdp);
    const auto d = mbx_tb::adpdu(2, 0);
    wr(ch_reg(kAdp, MBX_CH_REG_RX_TAIL), 40u);
    b_.send_frame(d, 0);
    (void)b_.drain_rx();
    ck_.dec("H0 an RX_TAIL ahead of RX_HEAD stores nothing: RX_HEAD stays", rx_head(kAdp), 0);
    ck_.dec("H0 and the frame counts in RX_DROP", rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)), 1);
    wr(ch_reg(kAdp, MBX_CH_REG_RX_TAIL), 0u);
    b_.send_frame(d, 0);
    (void)b_.drain_rx();
    ck_.that("H0 back in range, the next frame is stored", rx_head(kAdp) != 0u);

    // A whole, valid record at TX_TAIL, and a TX_HEAD a ring further on.
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
    const auto a = mbx_tb::adpdu(0, kOwnEid);
    const std::uint32_t rec = MBX_TX_HDR_WORDS + static_cast<std::uint32_t>((a.size() + 3u) / 4u);
    wr(base[kAdp], tx_w0(a.size(), 0, MBX_TX_KIND));
    wr(base[kAdp] + 4u, 0u);
    for (std::size_t k = 0; k < a.size(); k += 4) {
        std::uint32_t w = 0;
        for (std::size_t j = 0; j < 4 && k + j < a.size(); ++j) {
            w |= static_cast<std::uint32_t>(a[k + j]) << (8u * j);
        }
        wr(base[kAdp] + 4u * (MBX_TX_HDR_WORDS + static_cast<std::uint32_t>(k / 4)), w);
    }
    wr(ch_reg(kAdp, MBX_CH_REG_TX_HEAD), rec + MBX_CH_ADP_TX_WORDS);
    b_.idle(60);
    ck_.dec("H1 a TX_HEAD more than the ring ahead of TX_TAIL is refused: TX_ERR counts it",
            rd(ch_reg(kAdp, MBX_CH_REG_TX_ERR)), 1);
    ck_.dec("H1 and nothing reaches the wire", b_.tx_frames.size(), 0);

    const std::uint32_t head = rd(MBX_REG_EVT_HEAD) & 0xFFFFu;
    wr(MBX_REG_EVT_TAIL, (head + 8u) & 0xFFFFu);
    wr(MBX_REG_TMR_DEADLINE, rd(MBX_REG_NOW_MS));
    wr(MBX_REG_TMR_CMD, (1u << MBX_TMR_CMD_OP_LSB) | (0x55u << MBX_TMR_CMD_TAG_LSB) | 2u);
    b_.ms(2);
    ck_.dec("H2 an EVT_TAIL ahead of EVT_HEAD posts nothing: EVT_HEAD stays", rd(MBX_REG_EVT_HEAD) & 0xFFFFu, head);
    wr(MBX_REG_EVT_TAIL, head);
    b_.ms(2);
    ck_.dec("H2 back in range, the waiting expiry posts", rd(MBX_REG_EVT_HEAD) & 0xFFFFu, (head + MBX_EV_WORDS) & 0xFFFFu);
}

template <class Bench, class Check>
std::vector<std::uint32_t> Suite<Bench, Check>::take_event() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_link_and_gm_events() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::fill_event_ring_with_expiries() {
    const std::uint32_t now = rd(MBX_REG_NOW_MS);
    for (std::uint32_t s = 0; s < MBX_EVT_WORDS / MBX_EV_WORDS; ++s) {
        wr(MBX_REG_TMR_DEADLINE, now);
        wr(MBX_REG_TMR_CMD, (1u << MBX_TMR_CMD_OP_LSB) | ((0x100u + s) << MBX_TMR_CMD_TAG_LSB) | (s % MBX_N_TIMERS));
        b_.idle(MBX_N_TIMERS + 8u);
    }
    ck_.dec("E2 the ring is full of expiries", (rd(MBX_REG_EVT_HEAD) - evt_tail_) & 0xFFFFu, MBX_EVT_WORDS);
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_timers() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_tick() {
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

template <class Bench, class Check>
void Suite<Bench, Check>::check_gm_snapshot() {
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

// ---- lane FC: the full-tuple filter -------------------------------------------
//
// The owner's table (#664, comment 6014311316; REQUIREMENTS.md section 1,
// NFR-SCOUT-08, the FR_NFR.md section 3.4.2 hooks): each channel matches its
// exact tuple (VLAN tag absent, destination MAC, EtherType, AVTP subtype), then
// its identity term. The frames are the clauses' (frames.hpp), never the
// contract's tables.

//! Every channel open, the identities written, the MAAP range 8 addresses at
//! 91:E0:00:00:01:00.
template <class Bench, class Check>
void Suite<Bench, Check>::filter_up() {
    open((1u << MBX_N_CH) - 1u);
    wr(MBX_REG_MAAP_BASE_LO, 0x00000100u);
    wr(MBX_REG_MAAP_BASE_HI, 0x91E0u);
    wr(MBX_REG_MAAP_COUNT, 8u);
}

template <class Bench, class Check>
std::vector<typename Suite<Bench, Check>::Row> Suite<Bench, Check>::table_rows() {
    const std::vector<std::uint8_t> mrpdu = {0x00, 0x01, 0x22, 0x04, 0x00, 0x00};
    return {
        {"adp", MBX_CH_ADP, mbx_tb::adpdu(2, 0), true},
        {"acmp, multicast", MBX_CH_ACMP, mbx_tb::acmpdu(0, kOwnEid, kForeignEid), true},
        {"acmp, own unicast", MBX_CH_ACMP, mbx_tb::to(mbx_tb::acmpdu(0, kOwnEid, kForeignEid), kOwnMac), true},
        {"aecp, command", MBX_CH_AECP, mbx_tb::aecp(0, kOwnEid, kForeignEid), true},
        {"aecp, response", MBX_CH_AECP, mbx_tb::aecp(1, kForeignEid, kOwnEid, kOwnMac, kControllerAvailable), true},
        {"maap", MBX_CH_MAAP, mbx_tb::maap(1, 0x91E000000100ull + 6u, 4), true},
        {"maap, DEFEND to own unicast", MBX_CH_MAAP, mbx_tb::to(mbx_tb::maap(2, 0x91E000000100ull, 8), kOwnMac), true},
        {"srp MSRP", MBX_CH_SRP, mbx_tb::mrp(mbx_tb::kEtherMsrp, mrpdu), false},
        {"srp MVRP", MBX_CH_SRP, mbx_tb::mrp(mbx_tb::kEtherMvrp, mrpdu), false},
    };
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_tuple_controls() {
    filter_up();
    for (const Row& r : table_rows()) {
        const Verdict v = offer(r.frame);
        const std::string row = std::string(" (") + r.name + ")";
        ck_.dec(("Q0 a valid frame reaches its channel" + row).c_str(), v.channel, r.channel);
        ck_.that(("Q0 its record is the frame, byte for byte" + row).c_str(), same_bytes(v.record.bytes, r.frame));
        ck_.dec(("Q0 a valid frame never counts in FILTER_MISMATCH" + row).c_str(), v.mismatched, 0);
    }
    ck_.dec("Q0 and sets no IRQ_STATUS.ERR", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, 1), 0);
}

//! A frame that must reach no channel (no RX record, no RX_PASS) and move
//! FILTER_MISMATCH by `counted`.
template <class Bench, class Check>
void Suite<Bench, Check>::check_rejected(const std::string& what, const std::vector<std::uint8_t>& f,
                                         std::uint32_t counted) {
    const Verdict v = offer(f);
    ck_.dec((what + ": no RX record, no delivery").c_str(), v.channel, MBX_N_CH);
    ck_.dec((what + (counted != 0u ? ": FILTER_MISMATCH counts it once" : ": FILTER_MISMATCH does not count it"))
                .c_str(),
            v.mismatched, counted);
}

// Each tuple element changed alone, per row. A tag, or a refused identity,
// counts nothing; a destination, EtherType or subtype that leaves no tuple
// holding counts once.
template <class Bench, class Check>
void Suite<Bench, Check>::check_tuple_rejections() {
    filter_up();
    for (const Row& r : table_rows()) {
        const std::string row = std::string(" (") + r.name + ")";
        check_rejected("Q1 tagged, it" + row, mbx_tb::tagged(r.frame), 0);
        std::uint64_t other = kForeignMac;                  // a unicast nobody here owns: flooded traffic
        if (r.channel == MBX_CH_ADP) {
            other = mbx_tb::kIdentifyMac;                   // the other ATDECC multicast address
        } else if (r.channel == MBX_CH_MAAP && (r.frame[0] & 0x01u) != 0u) {
            other = mbx_tb::kAdpAcmpMac;                    // the multicast row; the DEFEND row keeps kForeignMac
        } else if (r.channel == MBX_CH_SRP) {               // each MRP application at the other's address
            other = r.frame[5] == 0x0Eu ? mbx_tb::kMvrpMac : mbx_tb::kMsrpMac;
        }
        check_rejected("Q2 to another destination MAC, it" + row, mbx_tb::to(r.frame, other), 1);
        const std::uint16_t et = r.avtp ? mbx_tb::kEtherMvrp
                                        : (r.frame[5] == 0x0Eu ? mbx_tb::kEtherMvrp : mbx_tb::kEtherMsrp);
        check_rejected("Q3 under another control EtherType, it" + row, mbx_tb::with_ethertype(r.frame, et), 1);
        if (r.avtp) {
            check_rejected("Q4 with an unassigned AVTP subtype, it" + row,
                           mbx_tb::with_subtype(r.frame, mbx_tb::kSubReserved), 1);
        } else {
            // MSRP and MVRP read no subtype: AVTP at their address selects no channel, whatever byte 14 holds
            const auto avtp = mbx_tb::with_ethertype(r.frame, mbx_tb::kEtherAvtp);
            check_rejected("Q4 as AVTP, a wrong AVTP subtype cannot select srp" + row, avtp, 1);
            check_rejected("Q4 as AVTP with the ADP subtype, it cannot select srp" + row,
                           mbx_tb::with_subtype(avtp, mbx_tb::kSubAdp), 1);
        }
    }
    check_rejected("Q3 under a non-control EtherType (gPTP), an ADPDU",
                   mbx_tb::with_ethertype(mbx_tb::adpdu(2, 0), mbx_tb::kEtherPtp), 0);
    // the identity term, each refusal uncounted: the tuple held
    check_rejected("Q5 ENTITY_DISCOVER for another entity", mbx_tb::adpdu(2, kForeignEid), 0);
    check_rejected("Q5 ENTITY_AVAILABLE of this entity", mbx_tb::adpdu(0, kOwnEid), 0);
    check_rejected("Q5 ACMP for neither this talker nor this listener", mbx_tb::acmpdu(0, kForeignEid, kForeignEid), 0);
    check_rejected("Q5 an AECP command for another target, even with this controller",
                   mbx_tb::aecp(0, kForeignEid, kOwnEid), 0);
    check_rejected("Q5 an AECP response for another controller, even to this target",
                   mbx_tb::aecp(1, kOwnEid, kForeignEid), 0);
    check_rejected("Q5 a MAAP PROBE beside this entity's range", mbx_tb::maap(1, 0x91E000000100ull + 8u, 4), 0);
    ck_.dec("Q5 no frame was refused for size, space or rate", rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)) +
            rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)) + rd(ch_reg(MBX_CH_AECP, MBX_CH_REG_RATE_DROP)), 0);
}

// AAF and CRF have no channel (#664: the SR class VLAN carries them). Stray
// untagged ones are control-EtherType frames no tuple holds: never delivered,
// counted once; the tagged media the fabric carries count nothing.
template <class Bench, class Check>
void Suite<Bench, Check>::check_stream_data() {
    filter_up();
    check_rejected("Q6 untagged AAF to a stream address", mbx_tb::stream_pdu(mbx_tb::kSubAaf), 1);
    check_rejected("Q6 untagged CRF to a stream address", mbx_tb::stream_pdu(mbx_tb::kSubCrf), 1);
    check_rejected("Q6 untagged AAF to the ADP and ACMP address",
                   mbx_tb::stream_pdu(mbx_tb::kSubAaf, mbx_tb::kAdpAcmpMac), 1);
    check_rejected("Q6 untagged CRF to this interface's own MAC", mbx_tb::stream_pdu(mbx_tb::kSubCrf, kOwnMac), 1);
    check_rejected("Q6 tagged AAF, the media path's", mbx_tb::tagged(mbx_tb::stream_pdu(mbx_tb::kSubAaf)), 0);
    check_rejected("Q6 tagged CRF, the media path's", mbx_tb::tagged(mbx_tb::stream_pdu(mbx_tb::kSubCrf)), 0);
}

// Two-sided AECP (Milan v1.2 5.4.5.3; IEEE 1722.1-2021 Table 9-1, 9.2.2.7 and
// 9.2.2.8): a command passes on target_entity_id, a response on
// controller_entity_id, whatever the other identity holds.
template <class Bench, class Check>
void Suite<Bench, Check>::check_aecp_both_directions() {
    filter_up();
    const auto reply = mbx_tb::aecp(1, kForeignEid, kOwnEid, kOwnMac, kControllerAvailable);
    const Verdict v = offer(reply);
    ck_.dec("Q7 the CONTROLLER_AVAILABLE response for this controller reaches the AECP ring", v.channel,
            MBX_CH_AECP);
    ck_.that("Q7 its record is the response, byte for byte", same_bytes(v.record.bytes, reply));
    check_rejected("Q7 a CONTROLLER_AVAILABLE response for another controller",
                   mbx_tb::aecp(1, kOwnEid, kForeignEid, kOwnMac, kControllerAvailable), 0);
    std::uint32_t commands = 0;
    std::uint32_t responses = 0;
    std::uint32_t wrong_way = 0;
    for (std::uint8_t mt = 0; mt < 16u; ++mt) {
        // Table 9-1: a command is even, its response the next odd value
        const bool command = (mt & 1u) == 0u;
        const Verdict to_target = offer(mbx_tb::aecp(mt, kOwnEid, kForeignEid));
        const Verdict to_controller = offer(mbx_tb::aecp(mt, kForeignEid, kOwnEid));
        commands += command && to_target.channel == MBX_CH_AECP ? 1u : 0u;
        responses += !command && to_controller.channel == MBX_CH_AECP ? 1u : 0u;
        wrong_way += (command ? to_controller.channel : to_target.channel) != MBX_N_CH ? 1u : 0u;
        wrong_way += to_target.mismatched + to_controller.mismatched;
    }
    ck_.dec("Q7 every command type (even) for this target passes", commands, 8);
    ck_.dec("Q7 every response type (odd) for this controller passes", responses, 8);
    ck_.dec("Q7 no command passes on its controller, no response on its target, none counted", wrong_way, 0);
}

// Own unicast is the arrival interface's OWN_MAC, never any unicast: each
// interface index the stream can name, against each interface's MAC, for
// every `own` tuple (AECP, the ACMP tolerance, the MAAP DEFEND). An index with
// no interface behind it has no own MAC.
template <class Bench, class Check>
void Suite<Bench, Check>::check_own_mac_per_interface() {
    filter_up();
    std::uint32_t right = 0;
    std::uint32_t wrong = 0;
    std::uint32_t counted = 0;
    std::uint32_t indexed = 0;
    for (std::uint32_t r = 0; r < kIfIndices; ++r) {
        for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
            const auto cmd = mbx_tb::aecp(0, kOwnEid, kForeignEid, kOwnMac + i);
            const auto tol = mbx_tb::to(mbx_tb::acmpdu(0, kOwnEid, kForeignEid), kOwnMac + i);
            const auto defend = mbx_tb::to(mbx_tb::maap(2, 0x91E000000100ull, 8), kOwnMac + i);
            const Verdict a = offer(cmd, r);
            const Verdict b = offer(tol, r);
            const Verdict d = offer(defend, r);
            if (r == i) {
                right += (a.channel == MBX_CH_AECP ? 1u : 0u) + (b.channel == MBX_CH_ACMP ? 1u : 0u) +
                         (d.channel == MBX_CH_MAAP ? 1u : 0u);
                indexed += field(a.record.w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) == r ? 1u : 0u;
                indexed += field(d.record.w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) == r ? 1u : 0u;
            } else {
                wrong += (a.channel != MBX_N_CH ? 1u : 0u) + (b.channel != MBX_N_CH ? 1u : 0u) +
                         (d.channel != MBX_N_CH ? 1u : 0u);
                counted += a.mismatched + b.mismatched + d.mismatched;
            }
        }
    }
    const std::uint32_t pairs = kIfIndices * MBX_N_IF - MBX_N_IF;
    ck_.dec("Q8 each interface's own MAC passes AECP, the ACMP tolerance and a MAAP DEFEND on that interface", right,
            3u * MBX_N_IF);
    ck_.dec("Q8 with the record's IF the arrival interface", indexed, 2u * MBX_N_IF);
    ck_.dec("Q8 another interface's own MAC, or one on an index with no interface, reaches no ring", wrong, 0);
    ck_.dec("Q8 and counts once each in FILTER_MISMATCH", counted, 3u * pairs);
    check_rejected("Q8 a MAC differing from OWN_MAC in MAC[47:32] only",
                   mbx_tb::aecp(0, kOwnEid, kForeignEid, kOwnMac ^ 0x020000000000ull), 1);
    check_rejected("Q8 a MAC differing from OWN_MAC in MAC[31:0] only",
                   mbx_tb::aecp(0, kOwnEid, kForeignEid, kOwnMac ^ 0x000000000100ull), 1);
    set_own_mac(0, kOwnMac + 0x10000u);
    check_rejected("Q8 rewritten, the old own MAC", mbx_tb::aecp(0, kOwnEid, kForeignEid), 1);
    ck_.dec("Q8 rewritten, the new own MAC passes",
            offer(mbx_tb::aecp(0, kOwnEid, kForeignEid, kOwnMac + 0x10000u)).channel, MBX_CH_AECP);
}

template <class Bench, class Check>
void Suite<Bench, Check>::check_filter_mismatch_count() {
    // closed channels: the counter judges the tuple, not FILTER_EN
    check_rejected("Q9 with every channel closed, a valid ADPDU", mbx_tb::adpdu(2, 0), 0);
    check_rejected("Q9 with every channel closed, an untagged AAF", mbx_tb::stream_pdu(mbx_tb::kSubAaf), 1);
    ck_.dec("Q9 a mismatch sets IRQ_STATUS.ERR", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, 1), 1);
    wr(MBX_REG_IRQ_STATUS, 1u << MBX_IRQ_STATUS_ERR_LSB);
    filter_up();
    for (unsigned k = 0; k < 5u; ++k) {
        b_.send_frame(mbx_tb::to(mbx_tb::adpdu(2, 0), mbx_tb::kIdentifyMac), 0);
    }
    b_.drain_rx(8000);
    ck_.dec("Q9 five tuple failures in a row count five", mismatches(), 6);
    wr(MBX_REG_IRQ_STATUS, 1u << MBX_IRQ_STATUS_ERR_LSB);
    for (const Row& r : table_rows()) {
        static_cast<void>(offer(r.frame));
        static_cast<void>(offer(mbx_tb::tagged(r.frame)));
    }
    static_cast<void>(offer(mbx_tb::adpdu(2, kForeignEid)));
    static_cast<void>(offer(mbx_tb::eth(mbx_tb::kAdpAcmpMac, mbx_tb::kEtherAvtp, 14)));
    ck_.dec("Q9 valid, tagged and identity-refused frames, and one that ends before byte 14, leave it", mismatches(),
            6);
    ck_.dec("Q9 and set no IRQ_STATUS.ERR", field(rd(MBX_REG_IRQ_STATUS), MBX_IRQ_STATUS_ERR_LSB, 1), 0);
}

// The token buckets stay (NFR-SCOUT-02), and a refusal by the filter takes no
// token: the bucket is observed apart from the tuple and the identity term.
template <class Bench, class Check>
void Suite<Bench, Check>::check_tokens_apart() {
    filter_up();
    const std::uint32_t burst = MBX_CH_ADP_RATE_BURST;
    for (std::uint32_t k = 0; k < 2u * burst; ++k) {
        b_.send_frame(mbx_tb::to(mbx_tb::adpdu(2, 0), mbx_tb::kIdentifyMac), 0);
        b_.send_frame(mbx_tb::adpdu(2, kForeignEid), 0);
    }
    b_.drain_rx(40000);
    for (std::uint32_t k = 0; k < burst + 1u; ++k) {
        b_.send_frame(mbx_tb::adpdu(2, kOwnEid), 0);
    }
    b_.drain_rx(40000);
    ck_.dec("Q10 refusals by the filter take no token: a full burst still passes after them", rx_pass(kAdp), burst);
    ck_.dec("Q10 the bucket refuses the frame past it in RATE_DROP", rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 1);
    ck_.dec("Q10 and FILTER_MISMATCH counts the tuple failures only", mismatches(), 2u * burst);
}

// The MAAP DEFEND (IEEE 1722-2016 B.2.1): PROBE and ANNOUNCE go to the MAAP
// multicast address, a DEFEND to the source MAC of the PROBE it answers, so
// to this interface's own MAC when this entity probed. Only a DEFEND passes
// there, a tuple failure like any other counts once, and the identity term
// (the requested range overlaps this entity's, B.3.5.6) still follows.
template <class Bench, class Check>
void Suite<Bench, Check>::check_maap_defend() {
    filter_up();
    const std::uint64_t base = 0x91E000000100ull;                  // filter_up()'s range, 8 addresses
    auto own = [&](std::uint8_t mt) { return mbx_tb::to(mbx_tb::maap(mt, base, 8), kOwnMac); };
    const auto defend = own(2);
    const Verdict v = offer(defend);
    ck_.dec("Q11 a DEFEND to this interface's own MAC reaches the MAAP ring", v.channel, MBX_CH_MAAP);
    ck_.that("Q11 its record is the DEFEND, byte for byte", same_bytes(v.record.bytes, defend));
    ck_.dec("Q11 and FILTER_MISMATCH does not count it", v.mismatched, 0);
    check_rejected("Q11 a PROBE to this interface's own MAC", own(1), 1);
    check_rejected("Q11 an ANNOUNCE to this interface's own MAC", own(3), 1);
    std::uint32_t reached = 0;
    std::uint32_t counted = 0;
    for (std::uint8_t mt = 0; mt < 16u; ++mt) {
        if (mt < 1u || mt > 3u) {                                  // Table B.1: reserved
            const Verdict o = offer(own(mt));
            reached += o.channel != MBX_N_CH ? 1u : 0u;
            counted += o.mismatched;
        }
    }
    ck_.dec("Q11 no reserved message_type to this interface's own MAC reaches a ring", reached, 0);
    ck_.dec("Q11 and each counts once in FILTER_MISMATCH", counted, 13);
    check_rejected("Q11 a DEFEND to a unicast MAC no interface owns", mbx_tb::to(mbx_tb::maap(2, base, 8), kForeignMac),
                   1);
    check_rejected("Q11 a DEFEND to this interface's own MAC for a range beside this entity's",
                   mbx_tb::to(mbx_tb::maap(2, base + 8u, 4), kOwnMac), 0);
    ck_.dec("Q11 a DEFEND to the MAAP multicast address still passes", offer(mbx_tb::maap(2, base, 8)).channel,
            MBX_CH_MAAP);
    // the message_type is byte 15's low nibble: a frame that ends at byte 14
    // has none, so no DEFEND, and one that ends at byte 15 carries no range
    auto cut = defend;
    cut.resize(MBX_MSG_TYPE_BYTE);
    check_rejected("Q11 a DEFEND to this interface's own MAC that ends at byte 14, before its message_type", cut, 1);
    cut = defend;
    cut.resize(MBX_MSG_TYPE_BYTE + 1u);
    check_rejected("Q11 a DEFEND to this interface's own MAC that ends at byte 15, before its range", cut, 0);
    ck_.dec("Q11 the DEFEND after them still reaches the MAAP ring", offer(defend).channel, MBX_CH_MAAP);
    ck_.dec("Q11 no frame was refused for size, space or rate",
            rd(ch_reg(MBX_CH_MAAP, MBX_CH_REG_RX_DROP)) + rd(ch_reg(MBX_CH_MAAP, MBX_CH_REG_RATE_DROP)), 0);
}

// The adp channel's bound talkers (#665, comment 6029368753; Milan v1.2
// 5.6.4.1): an ENTITY_AVAILABLE or ENTITY_DEPARTING passes when its
// entity_id is an enabled entry of the arrival interface's bound-talker
// table. Anything else the term refuses is dropped uncounted, as every
// identity refusal is: the tuple held.
template <class Bench, class Check>
void Suite<Bench, Check>::check_adp_bound_talkers() {
    filter_up();
    const std::uint64_t talker = 0x0A0B0C0D0E0F1011ull;
    const std::uint64_t other = 0x0A0B0C0D0E0F1012ull;
    check_rejected("Q12 with the bound-talker table empty, an ENTITY_AVAILABLE", mbx_tb::adpdu(0, talker), 0);
    set_bound(0, 0, talker, true);
    const auto available = mbx_tb::adpdu(0, talker);
    const Verdict a = offer(available);
    ck_.dec("Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring", a.channel, kAdp);
    ck_.that("Q12 its record is the ADPDU, byte for byte", same_bytes(a.record.bytes, available));
    ck_.dec("Q12 and FILTER_MISMATCH does not count it", a.mismatched, 0);
    ck_.dec("Q12 an ENTITY_DEPARTING of a bound talker reaches the adp ring", offer(mbx_tb::adpdu(1, talker)).channel,
            kAdp);
    check_rejected("Q12 an ENTITY_AVAILABLE of a talker no entry holds", mbx_tb::adpdu(0, other), 0);
    check_rejected("Q12 an ENTITY_DEPARTING of a talker no entry holds", mbx_tb::adpdu(1, other), 0);
    check_rejected("Q12 an entity_id differing from the entry in [63:32] only",
                   mbx_tb::adpdu(0, talker ^ 0x0000000100000000ull), 0);
    check_rejected("Q12 an entity_id differing from the entry in [31:0] only", mbx_tb::adpdu(0, talker ^ 1u), 0);
    std::uint32_t reached = 0;
    for (std::uint8_t mt = 2; mt < 16u; ++mt) {
        reached += offer(mbx_tb::adpdu(mt, talker)).channel != MBX_N_CH ? 1u : 0u;
    }
    ck_.dec("Q12 no other message_type of a bound talker passes on its entity_id, ENTITY_DISCOVER included", reached,
            0);
    ck_.dec("Q12 ENTITY_DISCOVER for every entity and for this one still pass",
            (offer(mbx_tb::adpdu(2, 0)).channel == kAdp ? 1u : 0u) +
                (offer(mbx_tb::adpdu(2, kOwnEid)).channel == kAdp ? 1u : 0u),
            2);
    // the field must be whole: a frame that ends inside entity_id has none,
    // even when the bytes it carries, right-aligned, are an enabled entry
    set_bound(0, 1, talker >> 8, true);
    check_rejected("Q12 an ENTITY_AVAILABLE of a bound talker that ends inside its entity_id",
                   mbx_tb::adpdu(0, talker, MBX_CH_ADP_T2_OFFSET + MBX_TERM_FIELD_BYTES - 1u), 0);
    set_bound(0, 1, 0, false);
    ck_.dec("Q12 one that ends with its entity_id passes",
            offer(mbx_tb::adpdu(0, talker, MBX_CH_ADP_T2_OFFSET + MBX_TERM_FIELD_BYTES)).channel, kAdp);
    // an entry takes part only while BOUND_EN is set, and every entry does
    set_bound(0, 0, talker, false);
    check_rejected("Q12 an entry with BOUND_EN clear, its identity still written", available, 0);
    set_bound(0, MBX_N_BOUND - 1u, talker, true);
    ck_.dec("Q12 the last entry passes its talker", offer(available).channel, kAdp);
    set_bound(0, MBX_N_BOUND - 1u, other, true);
    check_rejected("Q12 rewritten, the entry's old talker", available, 0);
    ck_.dec("Q12 rewritten, the entry's new talker passes", offer(mbx_tb::adpdu(0, other)).channel, kAdp);
    std::uint32_t every = 0;
    for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
        set_bound(0, e, talker + 0x100u * e, true);
    }
    for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
        every += offer(mbx_tb::adpdu(e & 1u, talker + 0x100u * e)).channel == kAdp ? 1u : 0u;
    }
    ck_.dec("Q12 with every entry enabled, each entry's talker passes", every, MBX_N_BOUND);
    ck_.dec("Q12 no frame was refused for size, space or rate",
            rd(ch_reg(kAdp, MBX_CH_REG_RX_DROP)) + rd(ch_reg(kAdp, MBX_CH_REG_RATE_DROP)), 0);
    check_bound_table_per_interface();
    check_bound_identity_bytes();
    check_bound_reset();
}

// The table read is the arrival interface's: a talker bound on interface i
// passes only on i, and an index with no interface behind it has no table.
template <class Bench, class Check>
void Suite<Bench, Check>::check_bound_table_per_interface() {
    const std::uint64_t talker = 0x0A0B0C0D0E0F2000ull;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            set_bound(i, e, 0, false);
        }
    }
    std::uint32_t right = 0;
    std::uint32_t wrong = 0;
    std::uint32_t indexed = 0;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        set_bound(i, i, talker + i, true);
    }
    for (std::uint32_t r = 0; r < kIfIndices; ++r) {
        for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
            const Verdict v = offer(mbx_tb::adpdu(0, talker + i), r);
            if (r == i) {
                right += v.channel == kAdp ? 1u : 0u;
                indexed += field(v.record.w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) == r ? 1u : 0u;
            } else {
                wrong += (v.channel != MBX_N_CH ? 1u : 0u) + v.mismatched;
            }
        }
    }
    ck_.dec("Q13 a talker bound on interface i passes on interface i", right, MBX_N_IF);
    ck_.dec("Q13 with the record's IF the arrival interface", indexed, MBX_N_IF);
    ck_.dec("Q13 on another interface, or an index with no interface, it reaches no ring and counts nothing", wrong, 0);
}

//! Every entry of every interface's table cleared, as the firmware unbinds.
template <class Bench, class Check>
void Suite<Bench, Check>::clear_bound() {
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            set_bound(i, e, 0, false);
        }
    }
}

// The match is the frame's own, byte by byte (lane F3 round 3: the table is
// compared as the identity arrives): each identity byte is compared at its own
// position, nothing of one frame's comparison carries into the next, and a
// word rewritten while BOUND_EN stays set takes effect as well.
template <class Bench, class Check>
void Suite<Bench, Check>::check_bound_identity_bytes() {
    const std::uint64_t talker = 0x0A0B0C0D0E0F1011ull;   // eight distinct bytes
    clear_bound();
    set_bound(0, 0, talker, true);
    check_rejected("Q14 another talker's ENTITY_AVAILABLE", mbx_tb::adpdu(0, talker ^ 0x0101010101010101ull), 0);
    ck_.dec("Q14 the bound talker's right after it passes", offer(mbx_tb::adpdu(0, talker)).channel, kAdp);
    check_rejected("Q14 right after that, one differing from it in the first identity byte only",
                   mbx_tb::adpdu(0, talker ^ 0xFF00000000000000ull), 0);
    ck_.dec("Q14 and the bound talker's after that passes", offer(mbx_tb::adpdu(0, talker)).channel, kAdp);
    std::uint32_t refused = 0;
    for (std::uint32_t b = 0; b < MBX_TERM_FIELD_BYTES; ++b) {
        const std::uint64_t one = talker ^ (0xA5ull << (8u * (MBX_TERM_FIELD_BYTES - 1u - b)));
        refused += offer(mbx_tb::adpdu(0, one)).channel == MBX_N_CH ? 1u : 0u;
    }
    ck_.dec("Q15 an entity_id differing from the entry in one identity byte is refused, for each of the eight",
            refused, MBX_TERM_FIELD_BYTES);
    const std::uint64_t low = (talker & 0xFFFFFFFF00000000ull) | 0x21222324u;
    wr(bnd_reg(0, 0, MBX_BND_REG_BOUND_EID_LO), static_cast<std::uint32_t>(low));
    check_rejected("Q16 BOUND_EID_LO rewritten while BOUND_EN stays set: the old talker", mbx_tb::adpdu(0, talker), 0);
    ck_.dec("Q16 the new talker passes", offer(mbx_tb::adpdu(0, low)).channel, kAdp);
    const std::uint64_t high = 0x3132333400000000ull | (low & 0xFFFFFFFFu);
    wr(bnd_reg(0, 0, MBX_BND_REG_BOUND_EID_HI), static_cast<std::uint32_t>(high >> 32));
    check_rejected("Q16 then BOUND_EID_HI rewritten: the talker before", mbx_tb::adpdu(0, low), 0);
    ck_.dec("Q16 the newest talker passes", offer(mbx_tb::adpdu(0, high)).channel, kAdp);
}

// A reset clears the table, wherever the fabric keeps it: every entry reads
// 0 again, an entry enabled with no identity written since holds talker 0,
// and one with one word written holds that word and 0.
template <class Bench, class Check>
void Suite<Bench, Check>::check_bound_reset() {
    const std::uint64_t talker = 0x0A0B0C0D0E0F1011ull;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            set_bound(i, e, talker + e, true);
        }
    }
    restart();
    filter_up();
    bool zero = true;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        for (std::uint32_t e = 0; e < MBX_N_BOUND; ++e) {
            zero = zero && rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_LO)) == 0u &&
                   rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EID_HI)) == 0u && rd(bnd_reg(i, e, MBX_BND_REG_BOUND_EN)) == 0u;
        }
    }
    ck_.that("Q17 after a reset every entry of every interface's table reads 0 again", zero);
    wr(bnd_reg(0, 0, MBX_BND_REG_BOUND_EN), 1u);
    check_rejected("Q17 an entry enabled after the reset with no identity written: its old talker",
                   mbx_tb::adpdu(0, talker), 0);
    ck_.dec("Q17 it holds talker 0, whose ENTITY_AVAILABLE passes", offer(mbx_tb::adpdu(0, 0)).channel, kAdp);
    wr(bnd_reg(0, 0, MBX_BND_REG_BOUND_EN), 0u);
    const std::uint64_t old = talker + 1u;
    wr(bnd_reg(0, 1, MBX_BND_REG_BOUND_EID_HI), static_cast<std::uint32_t>(old >> 32));
    wr(bnd_reg(0, 1, MBX_BND_REG_BOUND_EN), 1u);
    ck_.hex("Q17 with BOUND_EID_HI alone written since, BOUND_EID_LO reads 0",
            rd(bnd_reg(0, 1, MBX_BND_REG_BOUND_EID_LO)), 0u);
    ck_.dec("Q17 and the entry holds that word and 0, whose ENTITY_AVAILABLE passes",
            offer(mbx_tb::adpdu(0, old & 0xFFFFFFFF00000000ull)).channel, kAdp);
    check_rejected("Q17 its old talker", mbx_tb::adpdu(0, old), 0);
}

// The fabric copies an entry into its compare bytes when BOUND_EN is set, or
// a word written while it is (lane F3 round 3); an entry takes part only
// while it is set and no copy is owed, from the frame's first identity byte
// to its verdict. A frame stalled inside its identity shows that, and the
// copier must give way to the host's reads and start over on a rewrite. The
// verdict reads the table of the interface the frame arrived on while the
// next frame is already presented, and the owed copy gates the entries of
// that interface, every interface's (round 4, R530-2-F1).
template <class Bench, class Check>
void Suite<Bench, Check>::check_bound_timing() {
    // enough clocks for every entry's copy, ten clocks each at most
    const unsigned settle = 16u * MBX_N_IF * MBX_N_BOUND;
    const std::uint64_t talker = 0x0A0B0C0D0E0F1011ull;
    const std::uint64_t other = 0x1112131415161718ull;
    const std::uint32_t en = bnd_reg(0, 0, MBX_BND_REG_BOUND_EN);
    const auto available = mbx_tb::adpdu(0, talker);
    const std::size_t cut = MBX_CH_ADP_T2_OFFSET + 2u;   // two identity bytes taken, then the stream stalls
    filter_up();
    set_bound(0, 0, talker, true);
    b_.idle(settle);
    ck_.dec("Q18 a bound talker's ENTITY_AVAILABLE stalled inside its identity passes",
            offer_stalled(available, cut, [&] { b_.idle(settle); }).channel, kAdp);
    ck_.dec("Q18 one stalled while BOUND_EN is cleared and set again, the identity unchanged, reaches no ring",
            offer_stalled(available, cut, [&] {
                wr(en, 0u);
                wr(en, 1u);
                b_.idle(settle);
            }).channel,
            MBX_N_CH);
    ck_.dec("Q18 the next one passes", offer(available).channel, kAdp);
    ck_.dec("Q19 one stalled while BOUND_EN is set again alone, its copy made meanwhile, reaches no ring",
            offer_stalled(available, cut, [&] {
                wr(en, 1u);
                b_.idle(settle);
            }).channel,
            MBX_N_CH);
    ck_.dec("Q19 the next one passes", offer(available).channel, kAdp);
    // the host's reads of the table come first; the copy waits for them
    set_bound(0, 1, other, true);
    b_.idle(settle);
    set_bound(0, 0, talker, true);
    bool read = true;
    for (unsigned k = 0; k < 2u * MBX_TERM_FIELD_BYTES; ++k) {
        read = read && rd(bnd_reg(0, 1, MBX_BND_REG_BOUND_EID_LO)) == static_cast<std::uint32_t>(other) &&
               rd(bnd_reg(0, 1, MBX_BND_REG_BOUND_EID_HI)) == static_cast<std::uint32_t>(other >> 32);
    }
    ck_.that("Q20 another entry's words read back while an entry is copied", read);
    b_.idle(settle);
    ck_.dec("Q20 the entry copied meanwhile passes its talker", offer(available).channel, kAdp);
    ck_.dec("Q20 and the entry read meanwhile its own", offer(mbx_tb::adpdu(0, other)).channel, kAdp);
    // a word rewritten at each clock of a running copy: the copy starts over
    const std::uint64_t low = (talker & 0xFFFFFFFF00000000ull) | 0x21222324u;
    std::uint32_t newer = 0;
    std::uint32_t older = 0;
    for (unsigned d = 0; d < 32u; ++d) {
        set_bound(0, 0, talker, true);
        b_.idle(settle);
        wr(en, 1u);
        b_.idle(d);
        wr(bnd_reg(0, 0, MBX_BND_REG_BOUND_EID_LO), static_cast<std::uint32_t>(low));
        b_.idle(settle);
        newer += offer(mbx_tb::adpdu(0, low)).channel == kAdp ? 1u : 0u;
        older += offer(available).channel == MBX_N_CH ? 1u : 0u;
    }
    ck_.dec("Q21 BOUND_EID_LO rewritten at each of 32 clocks after BOUND_EN is set again: the new talker passes",
            newer, 32);
    ck_.dec("Q21 and the old one never does", older, 32);
    // the next frame, another talker's on another index, right behind a bound
    // talker's: the verdict, after the last identity byte, reads the table of
    // the interface the first frame arrived on
    clear_bound();
    std::uint32_t alone = 0;
    std::uint32_t own_if = 0;
    for (std::uint32_t i = 0; i < MBX_N_IF; ++i) {
        set_bound(i, 0, talker, true);
        b_.idle(settle);
        const std::uint32_t before = rx_pass(kAdp);
        b_.send_frame(available, i);
        b_.send_frame(mbx_tb::adpdu(0, other), (i + 1u) % kIfIndices);
        b_.drain_rx();
        const std::uint32_t got = (rx_pass(kAdp) - before) & 0xFFFFu;
        alone += got == 1u ? 1u : 0u;
        for (std::uint32_t k = 0; k < got; ++k) {
            const Record r = peek(kAdp);
            own_if += k == 0u && field(r.w0, MBX_RXREC_W0_IF_LSB, MBX_RXREC_W0_IF_WIDTH) == i ? 1u : 0u;
            release(kAdp, r);
        }
        b_.ms(kRefillMs);
        set_bound(i, 0, 0, false);
    }
    ck_.dec("Q22 a bound talker's ENTITY_AVAILABLE with the next frame, on another index, right behind it passes alone",
            alone, MBX_N_IF);
    ck_.dec("Q22 its record's IF the arrival interface", own_if, MBX_N_IF);
#if MBX_N_IF >= 2
    // the owed copy gates the entry of the frame's own interface: Q19 on
    // every interface past the first
    std::uint32_t stalled = 0;
    std::uint32_t next = 0;
    for (std::uint32_t i = 1; i < MBX_N_IF; ++i) {
        clear_bound();
        set_bound(i, 0, talker, true);
        b_.idle(settle);
        const std::uint32_t en_i = bnd_reg(i, 0, MBX_BND_REG_BOUND_EN);
        stalled += offer_stalled(available, cut, [&] {
                       wr(en_i, 1u);
                       b_.idle(settle);
                   }, i).channel == MBX_N_CH ? 1u : 0u;
        next += offer(available, i).channel == kAdp ? 1u : 0u;
    }
    ck_.dec("Q23 on each interface past the first, one stalled while BOUND_EN is set again alone reaches no ring",
            stalled, MBX_N_IF - 1u);
    ck_.dec("Q23 the next one on that interface passes", next, MBX_N_IF - 1u);
#endif
}

}  // namespace mbx_tb

#endif  // MBX_SUITE_HPP
