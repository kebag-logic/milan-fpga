// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_split.cpp - the split placement's control path, end to end (#665).
//
// tb_split_top composes KL_mbx (100 MHz, the mailbox's clock), KL_mbx_cdc, two
// byte FIFOs and milan_datapath with CTRL_SPLIT_P = 1 (50 MHz, the datapath's
// clock), as milan_soc.py's split SoC does. Every check writes the contract's
// registers through KL_mbx's host port and reads either the contract's
// registers or what the datapath's consumers read (tb_split_top's probes), so
// a check passes only through the crossing and the ctl ports:
//
//   [PUB]   the publication block reaches its class-D consumers, a sink's
//           stream_id only once SID_VALID is set, within its bound
//   [FACE]  a commit's settings reach the datapath only at the commit, every
//           one at once, and the acknowledgement clears BUSY within
//           MBX_FACE_ACK_CYCLES
//   [WIN]   each window's request is answered DONE under its own tag within
//           its wait bound, by the datapath's answer logic
//   [RX]    an ADP frame at the MAC reaches the adp ring whole; an AAF frame
//           never reaches the mailbox; a burst at the MAC past the datapath's
//           own tap FIFO is counted in the datapath's PP_DIAG[15:8] net
//   [TX]    a frame committed to the adp ring leaves the MAC byte for byte
//   [LINK]  the datapath's effective link sets LINK.UP, and its loss clears it
//   [TAP]   KL_ctrl_split alone (tb_split_top's u_tap): each tuple class it
//           accepts is handed out whole and each it refuses is not; a burst
//           past its FIFO loses frames, and each lost control frame is
//           counted once, a refused frame or a runt never, saturating at 255
//
// Each failing check prints FAIL with its label; the tally line is the
// suite's verdict.

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <memory>
#include <string>
#include <vector>

#include "Vtb_split_top.h"
#include "verilated.h"
#include "mbx_contract.h"
#include "frames.hpp"

namespace {

constexpr std::uint64_t kOwnEid = 0x0011223344556677ull;

class Tb {
 public:
    explicit Tb(Vtb_split_top* d) : d_(d) {}

    //! One unit: sys toggles on even units (period 4), dp on every fourth, offset by one (period 8).
    void unit() {
        ++u_;
        if (u_ % 2 == 0) {
            const bool rising = !d_->sys_clk;
            d_->sys_clk = rising;
            d_->eval();
            if (rising) {
                ++sys_cycles_;
                d_->ms_tick_p_i = 0;
            }
        } else if (u_ % 4 == 1) {
            const bool rising = !d_->dp_clk;
            if (rising) {
                tap_beat_ = d_->tap_tvalid;
                tap_take_ = d_->tap_valid && d_->tap_ready;
                tap_byte_ = d_->tap_data;
                tap_byte_last_ = d_->tap_last;
                rx_take_ = d_->rx_tvalid && d_->rx_tready;
                tx_take_ = d_->tx_tvalid && d_->tx_tready;
                tx_data_ = d_->tx_tdata;
                tx_keep_ = d_->tx_tkeep;
                tx_last_ = d_->tx_tlast;
            }
            d_->dp_clk = rising;
            d_->eval();
            if (rising) on_dp_rise();
        }
    }

    //! Run until n more sys rising edges have passed.
    void sys(std::uint64_t n) {
        const std::uint64_t until = sys_cycles_ + n;
        while (sys_cycles_ < until) unit();
    }

    void reset() {
        d_->sys_rst_n = 0;
        d_->dp_rst_n = 0;
        d_->host_req_i = 0;
        d_->rx_tvalid = 0;
        d_->tx_tready = 1;
        d_->link_up = 1;
        d_->tap_tvalid = 0;
        d_->tap_ready = 1;
        sys(20);
        d_->sys_rst_n = 1;
        d_->dp_rst_n = 1;
        sys(20);
    }

    //! One host access: the request for one sys cycle, then the cycle its ack arrives.
    std::uint32_t access(std::uint32_t byte_off, bool we, std::uint32_t v) {
        drive_host(byte_off, we, v);
        for (int i = 0; i < 8; ++i) {
            if (d_->host_ack_o) {
                const std::uint32_t r = d_->host_rdata_o;
                sys(1);
                return r;
            }
            sys(1);
        }
        std::printf("FAIL host access at 0x%x never acknowledged\n", byte_off);
        ++fail_;
        return 0;
    }
    void wr(std::uint32_t off, std::uint32_t v) { (void)access(off, true, v); }
    std::uint32_t rd(std::uint32_t off) { return access(off, false, 0); }

    //! Queue a frame for the MAC's receive side, little lane order.
    void mac_rx(const std::vector<std::uint8_t>& f) {
        for (std::size_t k = 0; k < f.size(); k += 8) {
            Beat b{};
            for (std::size_t j = 0; j < 8 && k + j < f.size(); ++j) {
                b.data |= static_cast<std::uint64_t>(f[k + j]) << (8u * j);
                b.keep |= 1u << j;
            }
            b.last = (k + 8 >= f.size());
            rx_q_.push_back(b);
        }
    }

    //! Queue a frame for u_tap's receive side, little lane order; the tap takes a beat a cycle.
    void tap_send(const std::vector<std::uint8_t>& f) {
        for (std::size_t k = 0; k < f.size(); k += 8) {
            Beat b{};
            for (std::size_t j = 0; j < 8 && k + j < f.size(); ++j) {
                b.data |= static_cast<std::uint64_t>(f[k + j]) << (8u * j);
                b.keep |= 1u << j;
            }
            b.last = (k + 8 >= f.size());
            tap_q_.push_back(b);
        }
    }
    //! Hold u_tap's byte side (the mailbox not ready), or release it.
    void tap_hold(bool hold) { d_->tap_ready = hold ? 0 : 1; }
    bool tap_idle() const { return tap_q_.empty() && !d_->tap_tvalid; }

    std::vector<std::vector<std::uint8_t>> tx_frames;   //!< every frame the MAC sent
    std::vector<std::vector<std::uint8_t>> tap_out;     //!< every frame u_tap handed out
    std::uint64_t sys_cycles() const { return sys_cycles_; }
    Vtb_split_top* dut() { return d_; }

    void check(const char* label, bool ok) {
        ++checks_;
        if (!ok) {
            ++fail_;
            std::printf("FAIL %s\n", label);
        }
    }
    void check_eq(const char* label, std::uint64_t got, std::uint64_t want) {
        ++checks_;
        if (got != want) {
            ++fail_;
            std::printf("FAIL %s: got 0x%llx, want 0x%llx\n", label, static_cast<unsigned long long>(got),
                        static_cast<unsigned long long>(want));
        }
    }
    int finish() const {
        std::printf("checks: %d   failures: %d\n", checks_, fail_);
        return fail_ ? 1 : 0;
    }

 private:
    struct Beat {
        std::uint64_t data = 0;
        std::uint32_t keep = 0;
        bool last = false;
    };

    void drive_host(std::uint32_t byte_off, bool we, std::uint32_t v) {
        d_->host_req_i = 1;
        d_->host_we_i = we;
        d_->host_addr_i = byte_off / 4u;
        d_->host_wdata_i = v;
        d_->host_be_i = 0xF;
        sys(1);
        d_->host_req_i = 0;
        d_->host_we_i = 0;
    }

    void on_dp_rise() {
        if (tap_beat_ && !tap_q_.empty()) tap_q_.pop_front();
        if (tap_q_.empty()) {
            d_->tap_tvalid = 0;
            d_->tap_tlast = 0;
        } else {
            d_->tap_tvalid = 1;
            d_->tap_tdata = tap_q_.front().data;
            d_->tap_tkeep = tap_q_.front().keep;
            d_->tap_tlast = tap_q_.front().last;
        }
        if (tap_take_) {
            tap_cur_.push_back(tap_byte_);
            if (tap_byte_last_) {
                tap_out.push_back(tap_cur_);
                tap_cur_.clear();
            }
        }
        if (rx_take_ && !rx_q_.empty()) rx_q_.erase(rx_q_.begin());
        if (rx_q_.empty()) {
            d_->rx_tvalid = 0;
            d_->rx_tlast = 0;
        } else {
            d_->rx_tvalid = 1;
            d_->rx_tdata = rx_q_.front().data;
            d_->rx_tkeep = rx_q_.front().keep;
            d_->rx_tlast = rx_q_.front().last;
        }
        if (tx_take_) {
            for (unsigned j = 0; j < 8; ++j) {
                if (tx_keep_ & (1u << j)) tx_cur_.push_back(static_cast<std::uint8_t>(tx_data_ >> (8u * j)));
            }
            if (tx_last_) {
                tx_frames.push_back(tx_cur_);
                tx_cur_.clear();
            }
        }
    }

    Vtb_split_top* d_;
    std::uint64_t u_ = 0;
    std::uint64_t sys_cycles_ = 0;
    std::vector<Beat> rx_q_;
    bool rx_take_ = false;
    bool tx_take_ = false;
    bool tx_last_ = false;
    std::uint64_t tx_data_ = 0;
    std::uint32_t tx_keep_ = 0;
    std::vector<std::uint8_t> tx_cur_;
    std::deque<Beat> tap_q_;
    bool tap_beat_ = false;
    bool tap_take_ = false;
    bool tap_byte_last_ = false;
    std::uint8_t tap_byte_ = 0;
    std::vector<std::uint8_t> tap_cur_;
    int checks_ = 0;
    int fail_ = 0;
};

std::uint32_t pub(std::uint32_t reg) { return MBX_PUB_BASE + reg; }
std::uint32_t pub_sink(unsigned k, std::uint32_t reg) { return MBX_PUB_BASE + MBX_PUB_SINK_BASE + MBX_PUB_SINK_STRIDE * k + reg; }
std::uint32_t pub_src(unsigned s, std::uint32_t reg) { return MBX_PUB_BASE + MBX_PUB_SRC_BASE + MBX_PUB_SRC_STRIDE * s + reg; }
std::uint32_t face(std::uint32_t reg) { return MBX_FACE_BASE + reg; }
std::uint32_t face_src(unsigned s, std::uint32_t reg) { return MBX_FACE_BASE + MBX_FACE_SOURCE_BASE + MBX_FACE_SOURCE_STRIDE * s + reg; }
std::uint32_t ch_reg(unsigned ch, std::uint32_t reg) { return MBX_CH_BASE + MBX_CH_STRIDE * ch + reg; }

//! Wait until pred() holds or n sys cycles pass; the cycles it took, or n + 1.
template <class Pred>
std::uint64_t wait_for(Tb& tb, Pred pred, std::uint64_t n) {
    for (std::uint64_t i = 0; i <= n; ++i) {
        if (pred()) return i;
        tb.sys(1);
    }
    return n + 1;
}

void check_pub(Tb& tb) {
    auto* d = tb.dut();
    const std::uint64_t sid = 0x91E0F00001230001ull;
    const std::uint32_t bound_started = (1u << MBX_BINDING_BOUND_LSB) | (1u << MBX_BINDING_STARTED_LSB);
    // the firmware's order (mbx_pub_sink): BINDING without SID_VALID, the two words, then BINDING with it
    tb.wr(pub_sink(0, MBX_PUB_SINK_REG_BINDING), bound_started);
    tb.wr(pub_sink(0, MBX_PUB_SINK_REG_SID_LO), static_cast<std::uint32_t>(sid));
    tb.wr(pub_sink(0, MBX_PUB_SINK_REG_SID_HI), static_cast<std::uint32_t>(sid >> 32));
    tb.sys(60);
    tb.check_eq("[PUB] sink 0 bound reaches the listener", d->p_bound & 1u, 1);
    tb.check_eq("[PUB] sink 0 started reaches the listener", d->p_started & 1u, 1);
    tb.check_eq("[PUB] a stream_id without SID_VALID never reaches the listener", d->p_bound_sid0, 0);
    tb.wr(pub_sink(0, MBX_PUB_SINK_REG_BINDING), bound_started | (1u << MBX_BINDING_SID_VALID_LSB));
    const std::uint64_t took = wait_for(tb, [&] { return d->p_bound_sid0 == sid; }, 60);
    tb.check("[PUB] the stream_id reaches the listener once SID_VALID is set, within 60 mailbox cycles", took <= 60);
    std::printf("[PUB] SID_VALID to the listener: %llu mailbox cycles\n", static_cast<unsigned long long>(took));
    // a move of STARTED alone keeps the stream
    tb.wr(pub_sink(0, MBX_PUB_SINK_REG_BINDING), (1u << MBX_BINDING_BOUND_LSB) | (1u << MBX_BINDING_SID_VALID_LSB));
    tb.sys(60);
    tb.check_eq("[PUB] STOP moves started alone", d->p_started & 1u, 0);
    tb.check_eq("[PUB] ...and keeps the settled stream", d->p_bound_sid0, sid);
    // the source side and the interface registers
    const std::uint64_t src_sid = 0x0011223344550000ull;
    tb.wr(pub_src(0, MBX_PUB_SRC_REG_SRC_SID_LO), static_cast<std::uint32_t>(src_sid));
    tb.wr(pub_src(0, MBX_PUB_SRC_REG_SRC_SID_HI), static_cast<std::uint32_t>(src_sid >> 32));
    tb.wr(pub(MBX_PUB_REG_DA_GATE), 1u);
    tb.wr(pub(MBX_PUB_REG_LICENCE), 1u);
    tb.wr(pub(MBX_PUB_REG_TALKER_DECL), 1u);
    tb.wr(pub(MBX_PUB_REG_IDLE_SLOPE), 1234567u);
    tb.wr(pub(MBX_PUB_REG_SR_DOMAIN), (2u << MBX_SR_DOMAIN_VID_LSB) | (3u << MBX_SR_DOMAIN_PRIORITY_LSB) |
                                          (1u << MBX_SR_DOMAIN_ADOPTED_LSB));
    tb.sys(60);
    tb.check_eq("[PUB] DA_GATE.OPEN reaches the talker's declaration predicate", d->p_declaring & 1u, 1);
    tb.check_eq("[PUB] LICENCE.ACTIVE reaches the stream gate's ACTIVE term", d->p_active & 1u, 1);
    tb.check_eq("[PUB] ...and its admitted term", d->p_admitted & 1u, 1);
    // the declaration state's encoding {0 NONE, 1 ADVERTISE, 2 FAILED}, as GET_STREAM_INFO reads it
    tb.check_eq("[PUB] TALKER_DECL.DECLARED reaches the declaration state as ADVERTISE", d->p_tk_decl0, 1);
    tb.check_eq("[PUB] the talker stream_id reaches the framer", d->p_src_sid0, src_sid);
    tb.check_eq("[PUB] IDLE_SLOPE.BPS", d->p_slope, 1234567u);
    tb.check_eq("[PUB] SR_DOMAIN.VID", d->p_vid, 2);
    tb.check_eq("[PUB] SR_DOMAIN.PRIORITY", d->p_prio, 3);
    tb.check_eq("[PUB] SR_DOMAIN.ADOPTED", d->p_adopted, 1);
}

void check_face(Tb& tb) {
    auto* d = tb.dut();
    const std::uint64_t fmt = 0x0205022000806000ull;
    tb.wr(face(MBX_FACE_REG_F_CLOCK), 1u << MBX_F_CLOCK_SOURCE_INDEX_LSB);
    tb.wr(face(MBX_FACE_REG_F_ENTITY), 255u << MBX_F_ENTITY_IDENTIFY_LSB);
    tb.wr(face(MBX_FACE_REG_F_AECP), 1u << MBX_F_AECP_LOCK_HELD_LSB);
    tb.wr(face(MBX_FACE_REG_F_RESTORE), 1u << MBX_F_RESTORE_DONE_LSB);
    tb.wr(face(MBX_FACE_REG_F_NVM), 1u << MBX_F_NVM_BACKED_LSB);
    tb.wr(face_src(0, MBX_FACE_SRC_REG_F_PT_OFFSET), 2000000u);
    tb.wr(face_src(0, MBX_FACE_SRC_REG_F_FMT_OUT_LO), static_cast<std::uint32_t>(fmt));
    tb.wr(face_src(0, MBX_FACE_SRC_REG_F_FMT_OUT_HI), static_cast<std::uint32_t>(fmt >> 32));
    tb.wr(face_src(0, MBX_FACE_SRC_REG_F_SRC_VALID), (1u << MBX_F_SRC_VALID_PT_OFFSET_LSB) |
                                                         (1u << MBX_F_SRC_VALID_FMT_OUT_LSB));
    tb.sys(60);
    tb.check_eq("[FACE] a setting not committed does not reach the datapath", d->p_clk_src, 0);
    tb.check_eq("[FACE] ...nor a format", d->p_fmt_out0, 0);
    tb.wr(face(MBX_FACE_REG_F_COMMIT), 1u << MBX_F_COMMIT_GO_LSB);
    const std::uint64_t took = wait_for(tb, [&] {
        return !(tb.rd(face(MBX_FACE_REG_F_STATUS)) & (1u << MBX_F_STATUS_BUSY_LSB));
    }, MBX_FACE_ACK_CYCLES);
    tb.check("[FACE] the commit is acknowledged within MBX_FACE_ACK_CYCLES", took <= MBX_FACE_ACK_CYCLES);
    std::printf("[FACE] commit to BUSY clear: %llu polls\n", static_cast<unsigned long long>(took));
    tb.check_eq("[FACE] F_CLOCK.SOURCE_INDEX reaches the media clock's selector", d->p_clk_src, 1);
    tb.check_eq("[FACE] F_ENTITY.IDENTIFY", d->p_identify, 255);
    tb.check_eq("[FACE] F_AECP.LOCK_HELD reaches the map lock", d->p_lock_held, 1);
    tb.check_eq("[FACE] F_RESTORE.DONE reaches CSR status", d->p_restore_done, 1);
    tb.check_eq("[FACE] F_NVM.BACKED reaches the REBOOT drain", d->p_nvm_backed, 1);
    tb.check_eq("[FACE] source 0's F_FMT_OUT", d->p_fmt_out0, fmt);
    tb.check_eq("[FACE] ...its valid bit", d->p_fmt_out_v0, 1);
    tb.check_eq("[FACE] source 0's F_PT_OFFSET", d->p_pt_offset0, 2000000u);
}

//! One window: its request words, GO, and the answer; the status it closed with.
struct Win {
    const char* name;
    std::uint32_t req;
    std::uint32_t cmd;
    std::uint32_t status;
    std::uint32_t data_lo;
    std::uint32_t data_hi;
    std::uint32_t done_lsb;
    std::uint32_t timeout_lsb;
    std::uint32_t tag_lsb;
    std::uint32_t wait;
};

std::uint32_t run_window(Tb& tb, const Win& w, std::uint64_t* data, std::uint64_t* took) {
    tb.wr(face(w.cmd), 1u);
    *took = wait_for(tb, [&] {
        const std::uint32_t s = tb.rd(face(w.status));
        return ((s >> w.done_lsb) & 1u) || ((s >> w.timeout_lsb) & 1u);
    }, 4u * w.wait);
    const std::uint32_t s = tb.rd(face(w.status));
    *data = tb.rd(face(w.data_lo));
    if (w.data_hi != w.data_lo) *data |= static_cast<std::uint64_t>(tb.rd(face(w.data_hi))) << 32;
    return s;
}

void check_windows(Tb& tb) {
    const Win ctr{"CTR", MBX_FACE_REG_CTR_REQ, MBX_FACE_REG_CTR_CMD, MBX_FACE_REG_CTR_STATUS, MBX_FACE_REG_CTR_DATA,
                  MBX_FACE_REG_CTR_DATA, MBX_CTR_STATUS_DONE_LSB, MBX_CTR_STATUS_TIMEOUT_LSB, MBX_CTR_STATUS_TAG_LSB,
                  MBX_WIN_CTR_WAIT_CYCLES};
    const Win amap{"AMAP", MBX_FACE_REG_AMAP_REQ, MBX_FACE_REG_AMAP_CMD, MBX_FACE_REG_AMAP_STATUS,
                   MBX_FACE_REG_AMAP_DATA_LO, MBX_FACE_REG_AMAP_DATA_HI, MBX_AMAP_STATUS_DONE_LSB,
                   MBX_AMAP_STATUS_TIMEOUT_LSB, MBX_AMAP_STATUS_TAG_LSB, MBX_WIN_AMAP_WAIT_CYCLES};
    const Win gsi{"GSI", MBX_FACE_REG_GSI_REQ, MBX_FACE_REG_GSI_CMD, MBX_FACE_REG_GSI_STATUS, MBX_FACE_REG_GSI_DATA_LO,
                  MBX_FACE_REG_GSI_DATA_HI, MBX_GSI_STATUS_DONE_LSB, MBX_GSI_STATUS_TIMEOUT_LSB,
                  MBX_GSI_STATUS_TAG_LSB, MBX_WIN_GSI_WAIT_CYCLES};
    // GET_COUNTERS of STREAM_OUTPUT 0 (IEEE 1722.1-2021 7.4.42), word 0, its STREAM_START counter
    tb.wr(face(MBX_FACE_REG_CTR_REQ), (0x0006u << MBX_CTR_REQ_TYPE_LSB) | (0u << MBX_CTR_REQ_INDEX_LSB));
    tb.wr(face(MBX_FACE_REG_CTR_WORD), 0u);
    std::uint64_t data = 0;
    std::uint64_t took = 0;
    for (unsigned round = 0; round < 2; ++round) {
        const std::uint32_t s = run_window(tb, ctr, &data, &took);
        tb.check("[WIN] CTR closes DONE, not TIMEOUT", ((s >> ctr.done_lsb) & 1u) && !((s >> ctr.timeout_lsb) & 1u));
        tb.check_eq("[WIN] CTR's answer carries the request's tag, a new one each GO", (s >> ctr.tag_lsb) & 0xFu,
                    round + 1u);
        std::printf("[WIN] CTR round %u: status 0x%x data 0x%llx in %llu polls\n", round, s,
                    static_cast<unsigned long long>(data), static_cast<unsigned long long>(took));
    }
    // GET_AUDIO_MAP of STREAM_PORT_OUTPUT 0, map 0 (IEEE 1722.1-2021 7.4.44)
    tb.wr(face(MBX_FACE_REG_AMAP_REQ), (0x000Fu << MBX_AMAP_REQ_TYPE_LSB) | (0u << MBX_AMAP_REQ_INDEX_LSB));
    tb.wr(face(MBX_FACE_REG_AMAP_PAGE), 0u);
    std::uint32_t s = run_window(tb, amap, &data, &took);
    tb.check("[WIN] AMAP closes DONE, not TIMEOUT", ((s >> amap.done_lsb) & 1u) && !((s >> amap.timeout_lsb) & 1u));
    std::printf("[WIN] AMAP: status 0x%x data 0x%llx in %llu polls\n", s, static_cast<unsigned long long>(data),
                static_cast<unsigned long long>(took));
    // GET_STREAM_INFO of STREAM_INPUT 0 (IEEE 1722.1-2021 7.4.16)
    tb.wr(face(MBX_FACE_REG_GSI_REQ), (0x0005u << MBX_GSI_REQ_TYPE_LSB) | (0u << MBX_GSI_REQ_INDEX_LSB));
    tb.wr(face(MBX_FACE_REG_GSI_SEL), 0u);
    s = run_window(tb, gsi, &data, &took);
    tb.check("[WIN] GSI closes DONE, not TIMEOUT", ((s >> gsi.done_lsb) & 1u) && !((s >> gsi.timeout_lsb) & 1u));
    std::printf("[WIN] GSI: status 0x%x data 0x%llx in %llu polls\n", s, static_cast<unsigned long long>(data),
                static_cast<unsigned long long>(took));
    // the same request again: the answer is the datapath's served word, not a stale one
    std::uint64_t again = 0;
    s = run_window(tb, gsi, &again, &took);
    tb.check_eq("[WIN] GSI answers the same request with the same word", again, data);
    tb.check("[WIN] ...and that word is not the empty one", data != 0);
    std::uint64_t map0 = 0;
    std::uint64_t map1 = 0;
    (void)run_window(tb, amap, &map0, &took);
    (void)run_window(tb, amap, &map1, &took);
    tb.check_eq("[WIN] AMAP answers the same request with the same word", map1, map0);
    tb.check("[WIN] ...and that word is not the empty one", map0 != 0);
}

void check_rx(Tb& tb) {
    auto* d = tb.dut();
    tb.wr(MBX_REG_OWN_EID_LO, static_cast<std::uint32_t>(kOwnEid));
    tb.wr(MBX_REG_OWN_EID_HI, static_cast<std::uint32_t>(kOwnEid >> 32));
    tb.wr(MBX_REG_FILTER_EN, 1u << MBX_CH_ADP);
    const std::uint32_t head0 = tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_RX_HEAD));
    const std::uint16_t frames0 = d->p_rx_frames;
    // an AAF frame (IEEE 1722-2016 subtype 0x02): the tap never hands it to the mailbox
    auto aaf = mbx_tb::adpdu(2, kOwnEid);
    aaf[14] = 0x02;
    tb.mac_rx(aaf);
    tb.sys(400);
    tb.check_eq("[RX] an AAF frame reaches no ring", tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_RX_HEAD)), head0);
    tb.check_eq("[RX] ...and the tap hands out no frame", d->p_rx_frames, frames0);
    // an ENTITY_DISCOVER for this entity (IEEE 1722.1-2021 6.2.1.5): delivered whole
    const auto f = mbx_tb::adpdu(2, kOwnEid);
    tb.mac_rx(f);
    tb.sys(600);
    const std::uint32_t head1 = tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_RX_HEAD));
    tb.check("[RX] an ADP ENTITY_DISCOVER reaches the adp ring", head1 != head0);
    tb.check_eq("[RX] the tap hands out one frame", d->p_rx_frames, static_cast<std::uint16_t>(frames0 + 1));
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
    const std::uint32_t w0 = tb.rd(base[MBX_CH_ADP] + 4u * head0);
    tb.check_eq("[RX] its record's length is the frame's", (w0 >> MBX_RXREC_W0_LEN_LSB) & 0xFFFFu, f.size());
    bool same = true;
    for (std::size_t k = 0; k < f.size(); k += 4) {
        const std::uint32_t w = tb.rd(base[MBX_CH_ADP] + 4u * (head0 + 2u + k / 4));
        for (std::size_t j = 0; j < 4 && k + j < f.size(); ++j) {
            same = same && (static_cast<std::uint8_t>(w >> (8u * j)) == f[k + j]);
        }
    }
    tb.check("[RX] ...and its bytes are the frame's", same);
}

void check_tx(Tb& tb) {
    auto* d = tb.dut();
    static const std::uint32_t base[MBX_N_CH] = MBX_CH_TX_BASE_TBL;
    static const std::uint32_t words[MBX_N_CH] = MBX_CH_TX_WORDS_TBL;
    const std::uint16_t frames0 = d->p_tx_frames;
    const auto f = mbx_tb::adpdu(0, kOwnEid);       // ENTITY_AVAILABLE
    std::uint32_t head = tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_TX_HEAD));
    auto put = [&](std::uint32_t i, std::uint32_t v) { tb.wr(base[MBX_CH_ADP] + 4u * ((head + i) & (words[MBX_CH_ADP] - 1u)), v); };
    put(0, (static_cast<std::uint32_t>(f.size()) << MBX_TXREC_W0_LEN_LSB) | (MBX_TX_KIND << MBX_TXREC_W0_KIND_LSB));
    put(1, 0u);
    for (std::size_t k = 0; k < f.size(); k += 4) {
        std::uint32_t w = 0;
        for (std::size_t j = 0; j < 4 && k + j < f.size(); ++j) w |= static_cast<std::uint32_t>(f[k + j]) << (8u * j);
        put(2u + static_cast<std::uint32_t>(k / 4), w);
    }
    head = (head + 2u + static_cast<std::uint32_t>((f.size() + 3u) / 4u)) & 0xFFFFu;
    tb.wr(ch_reg(MBX_CH_ADP, MBX_CH_REG_TX_HEAD), head);
    const std::uint64_t took = wait_for(tb, [&] { return !tb.tx_frames.empty(); }, 4000);
    tb.check("[TX] the committed frame leaves the MAC", !tb.tx_frames.empty());
    if (tb.tx_frames.empty()) {
        std::printf("[TX] TX_HEAD 0x%x TX_TAIL 0x%x TX_ERR 0x%x\n", tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_TX_HEAD)),
                    tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_TX_TAIL)), tb.rd(ch_reg(MBX_CH_ADP, MBX_CH_REG_TX_ERR)));
    }
    if (!tb.tx_frames.empty()) {
        tb.check("[TX] ...byte for byte", tb.tx_frames.front() == f);
        std::printf("[TX] commit to the MAC's last byte: %llu mailbox cycles, %zu bytes\n",
                    static_cast<unsigned long long>(took), tb.tx_frames.front().size());
    }
    tb.check_eq("[TX] the packer counts one frame", d->p_tx_frames, static_cast<std::uint16_t>(frames0 + 1));
}

void check_link(Tb& tb) {
    auto* d = tb.dut();
    // the link guard qualifies the PHY's level over SETTLE_CYC_C datapath cycles (KL_link_guard)
    const std::uint64_t up = wait_for(tb, [&] { return (tb.rd(MBX_REG_LINK) >> MBX_LINK_UP_LSB) & 1u; }, 3000000);
    tb.check("[LINK] the datapath's effective link reaches LINK.UP", up <= 3000000);
    d->link_up = 0;
    const std::uint64_t down = wait_for(tb, [&] { return !((tb.rd(MBX_REG_LINK) >> MBX_LINK_UP_LSB) & 1u); }, 200000);
    tb.check("[LINK] ...and its loss clears it", down <= 200000);
    d->link_up = 1;
    const std::uint64_t again = wait_for(tb, [&] { return (tb.rd(MBX_REG_LINK) >> MBX_LINK_UP_LSB) & 1u; }, 3000000);
    tb.check("[LINK] ...and its return sets it again", again <= 3000000);
    std::printf("[LINK] up after %llu polls, down after %llu, up again after %llu\n",
                static_cast<unsigned long long>(up), static_cast<unsigned long long>(down),
                static_cast<unsigned long long>(again));
}

//! A frame of n bytes for u_tap: destination, a source, the EtherType, the subtype byte, then a pattern.
std::vector<std::uint8_t> tap_frame(std::uint64_t da, std::uint16_t etype, std::uint8_t subtype, unsigned tag,
                                    std::size_t n = 64) {
    std::vector<std::uint8_t> f(n);
    for (std::size_t i = 0; i < n; ++i) f[i] = static_cast<std::uint8_t>(tag + i);
    for (unsigned i = 0; i < 6; ++i) f[i] = static_cast<std::uint8_t>(da >> (8u * (5u - i)));
    for (unsigned i = 6; i < 12; ++i) f[i] = static_cast<std::uint8_t>(0x20u + i);
    f[12] = static_cast<std::uint8_t>(etype >> 8);
    f[13] = static_cast<std::uint8_t>(etype);
    f[14] = subtype;
    return f;
}

constexpr std::uint64_t kDaAdp = 0x91E0F0010000ull;    // the ADP and ACMP multicast address (IEEE 1722.1-2021)
constexpr std::uint64_t kDaMaap = 0x91E0F000FF00ull;   // the MAAP multicast address (IEEE 1722-2016 Annex B)
constexpr std::uint64_t kDaMsrp = 0x0180C200000Eull;   // MSRP's group address (IEEE 802.1Q)
constexpr std::uint64_t kDaMvrp = 0x0180C2000021ull;   // MVRP's group address (IEEE 802.1Q)
constexpr std::uint64_t kDaUnicast = 0x001122334455ull;

void check_tap(Tb& tb) {
    auto* d = tb.dut();
    struct Tuple {
        const char* what;
        std::uint64_t da;
        std::uint16_t etype;
        std::uint8_t subtype;
        bool kept;
    };
    // the subtypes of IEEE 1722.1-2021 (ADP, AECP, ACMP) and IEEE 1722-2016 Annex B (MAAP) on
    // EtherType 0x22F0; MSRP (0x22EA) and MVRP (0x88F5) only at their own group address
    static const Tuple kTuples[] = {
        {"ADP (0x22F0, subtype 0xFA)", kDaAdp, 0x22F0, 0xFA, true},
        {"AECP (0x22F0, subtype 0xFB)", kDaUnicast, 0x22F0, 0xFB, true},
        {"ACMP (0x22F0, subtype 0xFC)", kDaAdp, 0x22F0, 0xFC, true},
        {"MAAP (0x22F0, subtype 0xFE)", kDaMaap, 0x22F0, 0xFE, true},
        {"MSRP at 01-80-C2-00-00-0E", kDaMsrp, 0x22EA, 0x00, true},
        {"MVRP at 01-80-C2-00-00-21", kDaMvrp, 0x88F5, 0x00, true},
        {"MSRP's EtherType at MVRP's group address", kDaMvrp, 0x22EA, 0x00, false},
        {"MVRP's EtherType at MSRP's group address", kDaMsrp, 0x88F5, 0x00, false},
        {"MSRP's EtherType at a unicast address", kDaUnicast, 0x22EA, 0x00, false},
        {"AAF (0x22F0, subtype 0x02)", kDaAdp, 0x22F0, 0x02, false},
        {"a 0x22F0 subtype with no control channel (0xFD)", kDaAdp, 0x22F0, 0xFD, false},
    };
    unsigned tag = 0;
    for (const Tuple& t : kTuples) {
        const std::size_t out0 = tb.tap_out.size();
        const std::uint16_t frames0 = d->tap_frames;
        const auto f = tap_frame(t.da, t.etype, t.subtype, tag++);
        tb.tap_send(f);
        tb.sys(400);
        if (t.kept) {
            const std::string label = std::string("[TAP] ") + t.what + " is handed out whole, and counted";
            tb.check(label.c_str(), tb.tap_out.size() == out0 + 1 && tb.tap_out.back() == f &&
                                        d->tap_frames == static_cast<std::uint16_t>(frames0 + 1));
        } else {
            const std::string label = std::string("[TAP] ") + t.what + " is refused";
            tb.check(label.c_str(), tb.tap_out.size() == out0 && d->tap_frames == frames0);
        }
    }
    tb.check_eq("[TAP] a FIFO that never filled has lost nothing", d->tap_drops, 0);
}

void check_tap_drops(Tb& tb) {
    auto* d = tb.dut();
    // the mailbox stalls, and the tap is offered 100 ADP frames of 64 bytes, 6,400 bytes at its
    // 4,096-byte FIFO, then one of 24 bytes and eight of 16 that fill what room is left, to its last word
    std::vector<std::vector<std::uint8_t>> kept;
    for (unsigned n = 0; n < 100; ++n) kept.push_back(tap_frame(kDaAdp, 0x22F0, 0xFA, n));
    kept.push_back(tap_frame(kDaAdp, 0x22F0, 0xFA, 0x7Fu, 24));
    for (unsigned n = 0; n < 8; ++n) kept.push_back(tap_frame(kDaAdp, 0x22F0, 0xFA, 0x80u + n, 16));
    const std::size_t out0 = tb.tap_out.size();
    tb.tap_hold(true);
    for (const auto& f : kept) tb.tap_send(f);
    (void)wait_for(tb, [&] { return tb.tap_idle(); }, 8000);
    tb.sys(40);
    const unsigned lost = d->tap_drops;
    tb.check("[TAP] a burst past the FIFO's 4,096 bytes counts the frames it lost", lost > 0);
    // refused frames turned away by the full FIFO lose no control frame
    for (unsigned n = 0; n < 8; ++n) tb.tap_send(tap_frame(kDaAdp, 0x22F0, 0x02, n));
    (void)wait_for(tb, [&] { return tb.tap_idle(); }, 8000);
    tb.sys(40);
    tb.check_eq("[TAP] ...and not the refused frames a full FIFO turns away", d->tap_drops, lost);
    // one-beat runts (8 bytes, shorter than any control frame) turned away by the full FIFO; with a
    // word of room each would be stored and reclaimed instead, and this check would hold nothing
    tb.check("[TAP] the burst leaves the FIFO full to its last word", d->tap_full);
    for (unsigned n = 0; n < 8; ++n) tb.tap_send(tap_frame(kDaAdp, 0x22F0, 0xFA, 0x90u + n, 8));
    (void)wait_for(tb, [&] { return tb.tap_idle(); }, 8000);
    tb.sys(40);
    tb.check_eq("[TAP] ...nor the one-beat runts a full FIFO turns away", d->tap_drops, lost);
    tb.tap_hold(false);
    tb.sys(40000);
    const std::size_t handed = tb.tap_out.size() - out0;
    tb.check_eq("[TAP] every frame of the burst is handed out or counted lost", handed + lost, kept.size());
    tb.check("[TAP] ...and the FIFO holds 4,096 bytes of it before it loses one", handed >= 4096u / 64u);
    std::size_t at = 0;
    bool in_order = true;
    for (std::size_t i = out0; i < tb.tap_out.size(); ++i) {
        while (at < kept.size() && kept[at] != tb.tap_out[i]) ++at;
        in_order = in_order && at < kept.size();
        ++at;
    }
    tb.check("[TAP] ...each frame handed out whole and in order", in_order);
    std::printf("[TAP] burst: %zu frames offered, %zu handed out, %u counted lost\n", kept.size(), handed, lost);
    // a second burst of 320 frames: 255 lost or more, and the count holds at 255
    tb.tap_hold(true);
    for (unsigned n = 0; n < 320; ++n) tb.tap_send(tap_frame(kDaAdp, 0x22F0, 0xFA, n));
    (void)wait_for(tb, [&] { return tb.tap_idle(); }, 20000);
    tb.sys(40);
    tb.check_eq("[TAP] the count saturates at 255", d->tap_drops, 255);
    tb.tap_hold(false);
    tb.sys(40000);
}

//! The datapath's own tap, through its PP_DIAG[15:8] net (pp_rx_drops_w): it reads 0 while
//! nothing was lost, and a burst at the MAC, eight bytes a cycle at a tap that drains one,
//! loses frames it counts there, each frame of the burst handed out or counted lost.
void check_dp_drops(Tb& tb) {
    auto* d = tb.dut();
    tb.check_eq("[RX] the datapath's drop count reads 0 while its tap has lost nothing", d->p_rx_drops, 0);
    const std::uint16_t frames0 = d->p_rx_frames;
    const auto f = mbx_tb::adpdu(2, kOwnEid);
    constexpr unsigned kBurst = 100;
    for (unsigned n = 0; n < kBurst; ++n) tb.mac_rx(f);
    tb.sys(40000);
    const unsigned lost = d->p_rx_drops;
    const unsigned handed = static_cast<std::uint16_t>(d->p_rx_frames - frames0);
    tb.check("[RX] a burst at the MAC past the tap's FIFO is counted in the datapath's drop count", lost > 0);
    tb.check_eq("[RX] ...and every frame of it is handed out or counted lost", handed + lost, kBurst);
    std::printf("[RX] burst at the MAC: %u frames offered, %u handed out, %u counted lost\n", kBurst, handed,
                lost);
}

}  // namespace

int main(int argc, char** argv) {
    auto ctx = std::make_unique<VerilatedContext>();
    ctx->commandArgs(argc, argv);
    auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    Tb tb(dut.get());
    tb.reset();
    check_pub(tb);
    check_face(tb);
    check_windows(tb);
    check_rx(tb);
    check_tx(tb);
    check_link(tb);
    check_tap(tb);
    check_tap_drops(tb);
    check_dp_drops(tb);
    std::printf("ran %llu mailbox cycles\n", static_cast<unsigned long long>(tb.sys_cycles()));
    dut->final();
    return tb.finish();
}
