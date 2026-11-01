// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// bench.hpp - the clock, the two bus hosts and the frame streams around
// tb_mbx_top, shared by the RTL checks (sim_main.cpp) and the firmware
// co-simulation (cosim_main.cpp).
//
// THE ONE DECISION THAT MATTERS: every host access goes through the adapter
// the top was built with (Wishbone or AXI4-Lite), cycle by cycle, with the
// handshake each bus defines. Nothing here pokes KL_mbx's host port, so a
// check that passes has passed through a real adapter.
//
// On the AXI4-Lite build every clock is also a structural probe: before the
// edge, each AXI input is moved in turn (every VALID and READY flipped, the
// addresses, data and strobes scrambled) and every AXI output must stay
// where it was, since IHI0022H A3.1.1 and A3.2.1 forbid a combinational
// path from an input to an output. `comb_paths` counts the cycles where one
// moved, over every state the checks visit.

#ifndef MBX_BENCH_HPP
#define MBX_BENCH_HPP

#include <array>
#include <cstdint>
#include <deque>
#include <functional>
#include <type_traits>
#include <vector>

#include "Vtb_mbx_top.h"
#include "frames.hpp"
#include "mbx_contract.h"

namespace mbx_tb {

//! The bench: drives tb_mbx_top one clock at a time.
class Bench {
 public:
    //! `host` is the adapter the top was built with: 0 Wishbone, 1 AXI4-Lite.
    Bench(Vtb_mbx_top* dut, unsigned host) : dut_(dut), host_(host) {}

    //! Hold reset for a few clocks with every input idle.
    void reset() {
        dut_->rst_n = 0;
        idle_inputs();
        for (int i = 0; i < 4; ++i) {
            step();
        }
        dut_->rst_n = 1;
        step();
    }

    //! One clock: drive the RX byte at the head of the queue, sample the TX
    //! byte, rise.
    void step() {
        dut_->rx_valid_i = rx_q_.empty() ? 0 : 1;
        if (!rx_q_.empty()) {
            dut_->rx_data_i = rx_q_.front().data;
            dut_->rx_last_i = rx_q_.front().last ? 1 : 0;
            dut_->rx_if_i = rx_q_.front().iface;
        }
        dut_->tx_ready_i = tx_ready_now() ? 1 : 0;
        dut_->clk_i = 0;
        dut_->eval();
        if (host_ == 1) {
            probe_axil();
        }
        const bool rx_taken = dut_->rx_valid_i && dut_->rx_ready_o;
        if (dut_->tx_valid_o && dut_->tx_ready_i) {
            take_tx_byte();
        }
        dut_->clk_i = 1;
        dut_->eval();
        if (on_clock) {
            on_clock();
        }
        if (rx_taken) {
            rx_q_.pop_front();
        }
        dut_->ms_tick_p_i = 0;
        dut_->gm_change_p_i = 0;
        clear_face_pulses();
        ++cycles_;
    }

    //! Clocks with nothing new offered.
    void idle(unsigned n) {
        for (unsigned i = 0; i < n; ++i) {
            step();
        }
    }

    //! One NOW_MS millisecond: the pulse, then a few idle clocks so the
    //! scanner and the poster see it.
    void ms(unsigned n = 1) {
        for (unsigned i = 0; i < n; ++i) {
            dut_->ms_tick_p_i = 1;
            step();
            idle(kClocksPerMs - 1);
        }
    }

    //! A grandmaster change pulse on interface `iface`.
    void gm_change(unsigned iface, std::uint64_t gm, std::uint8_t domain) {
        set_gm(iface, gm, domain);
        dut_->gm_change_p_i = 1u << iface;
        step();
    }

    void set_gm(unsigned iface, std::uint64_t gm, std::uint8_t domain) {
#if MBX_N_IF == 1
        dut_->gm_id_i = gm;
        dut_->gptp_domain_i = domain;
        (void)iface;
#else
        // a contract of more interfaces (the two-interface variant): gm_id_i is
        // a Verilator wide signal of 32-bit words, least significant first
        dut_->gm_id_i[2u * iface] = static_cast<std::uint32_t>(gm);
        dut_->gm_id_i[2u * iface + 1u] = static_cast<std::uint32_t>(gm >> 32);
        const unsigned shift = 8u * iface;
        dut_->gptp_domain_i = (dut_->gptp_domain_i & ~(0xFFu << shift)) | (static_cast<unsigned>(domain) << shift);
#endif
    }

    void set_link(unsigned mask) { dut_->link_up_i = mask; }

    //! Queue one frame on the ingress stream; it leaves at the RTL's pace.
    void send_frame(const std::vector<std::uint8_t>& frame, unsigned iface) {
        send_bytes(frame, iface, true);
    }

    //! Queue part of a frame: its last byte ends the frame only when `ends`,
    //! so the stream stalls between two parts while the queue is empty.
    void send_bytes(const std::vector<std::uint8_t>& bytes, unsigned iface, bool ends) {
        for (std::size_t i = 0; i < bytes.size(); ++i) {
            rx_q_.push_back(RxByte{bytes[i], ends && i + 1 == bytes.size(), iface});
        }
    }

    //! Clock until the ingress queue is empty and the record is settled.
    bool drain_rx(unsigned patience = 4000) {
        for (unsigned i = 0; i < patience && !rx_q_.empty(); ++i) {
            step();
        }
        idle(8);
        return rx_q_.empty();
    }

    //! Clock until `n` whole frames (last byte taken) have left the TX merge,
    //! or the patience runs out.
    bool wait_tx(std::size_t n, unsigned patience = 20000) {
        for (unsigned i = 0; i < patience && !tx_done(n); ++i) {
            step();
        }
        return tx_done(n);
    }

    bool tx_done(std::size_t n) const { return tx_frames.size() > n || (tx_frames.size() == n && !tx_open_); }

    //! A frame is on the TX stream now, its last byte not yet taken.
    bool tx_open() const { return tx_open_; }

    //! The TX sink takes a byte on cycles where the pattern's bit is set
    //! (bit k of `pattern` for cycle k modulo 8); 0xFF is always ready.
    void tx_ready_pattern(std::uint8_t pattern) { tx_pattern_ = pattern; }

    std::uint32_t read(std::uint32_t byte_offset) {
        ++reads_;
        return host_ == 0 ? wb(false, byte_offset, 0, 0xF) : axil_read(byte_offset);
    }

    void write(std::uint32_t byte_offset, std::uint32_t value, std::uint8_t strobes = 0xF) {
        ++writes_;
        if (host_ == 0) {
            (void)wb(true, byte_offset, value, strobes);
        } else {
            axil_write(byte_offset, value, strobes);
        }
    }

    //! What the face block drives into interface `iface`'s datapath, read off
    //! tb_mbx_top's fw_*_o and window ports.
    FaceView face(unsigned iface) const {
        FaceView v;
#define MBX_TB_SETTING(port, reg, fld) slice(dut_->port, MBX_##reg##_##fld##_WIDTH * iface, MBX_##reg##_##fld##_WIDTH)
        v.send = static_cast<std::uint32_t>(slice(dut_->fw_send_o, iface, 1));
        v.setting = {MBX_TB_SETTING(fw_ctrl_ready_o, F_CTRL, READY),
                     MBX_TB_SETTING(fw_entity_cur_config_o, F_ENTITY, CUR_CONFIG),
                     MBX_TB_SETTING(fw_entity_identify_o, F_ENTITY, IDENTIFY),
                     MBX_TB_SETTING(fw_clock_source_index_o, F_CLOCK, SOURCE_INDEX),
                     MBX_TB_SETTING(fw_aecp_lock_held_o, F_AECP, LOCK_HELD),
                     MBX_TB_SETTING(fw_aecp_dyn_dirty_o, F_AECP, DYN_DIRTY),
                     MBX_TB_SETTING(fw_restore_busy_o, F_RESTORE, BUSY),
                     MBX_TB_SETTING(fw_restore_done_o, F_RESTORE, DONE),
                     MBX_TB_SETTING(fw_restore_fail_o, F_RESTORE, FAIL),
                     MBX_TB_SETTING(fw_restore_blank_o, F_RESTORE, BLANK),
                     MBX_TB_SETTING(fw_restore_closed_o, F_RESTORE, CLOSED),
                     MBX_TB_SETTING(fw_restore_rb_o, F_RESTORE, RB),
                     MBX_TB_SETTING(fw_restore_rs_cause_o, F_RESTORE, RS_CAUSE),
                     MBX_TB_SETTING(fw_restore_cause_o, F_RESTORE, CAUSE),
                     MBX_TB_SETTING(fw_nvm_backed_o, F_NVM, BACKED),
                     MBX_TB_SETTING(fw_nvm_alarm_o, F_NVM, ALARM),
                     MBX_TB_SETTING(fw_nvm_dirty_o, F_NVM, DIRTY),
                     MBX_TB_SETTING(fw_nvm_stale_o, F_NVM, STALE),
                     MBX_TB_SETTING(fw_nvm_pend_o, F_NVM, PEND),
                     MBX_TB_SETTING(fw_nvm_img_valid_o, F_NVM, IMG_VALID),
                     MBX_TB_SETTING(fw_nvm_verdict_o, F_NVM, VERDICT)};
#undef MBX_TB_SETTING
        for (unsigned s = 0; s < MBX_N_PUB_SOURCES; ++s) {
            const unsigned at = MBX_N_PUB_SOURCES * iface + s;
            v.pt_offset.push_back(slice(dut_->fw_pt_offset_ns_o, 32u * at, 32u));
            v.fmt_out.push_back(slice(dut_->fw_fmt_out_o, 64u * at, 64u));
            v.pt_offset_v |= static_cast<std::uint32_t>(slice(dut_->fw_pt_offset_v_o, at, 1u)) << s;
            v.fmt_out_v |= static_cast<std::uint32_t>(slice(dut_->fw_fmt_out_v_o, at, 1u)) << s;
        }
        for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
            const unsigned at = MBX_N_PUB_SINKS * iface + k;
            v.fmt_in.push_back(slice(dut_->fw_fmt_in_o, 64u * at, 64u));
            v.fmt_in_v |= static_cast<std::uint32_t>(slice(dut_->fw_fmt_in_v_o, at, 1u)) << k;
        }
        auto win = [&](unsigned w, const auto& req, const auto& tag, std::uint32_t tag_width,
                       std::vector<std::uint64_t> fields) {
            v.req[w] = static_cast<std::uint32_t>(slice(req, iface, 1u));
            v.tag[w] = static_cast<std::uint32_t>(slice(tag, tag_width * iface, tag_width));
            v.fields[w] = std::move(fields);
        };
#define MBX_TB_FIELD(port, width) slice(dut_->port, (width) * iface, (width))
        win(kWinCtr, dut_->ctr_req_o, dut_->ctr_tag_o, MBX_CTR_STATUS_TAG_WIDTH,
            {MBX_TB_FIELD(ctr_type_o, 16u), MBX_TB_FIELD(ctr_index_o, 16u),
             MBX_TB_FIELD(ctr_word_o, MBX_CTR_WORD_WORD_WIDTH)});
        win(kWinAmap, dut_->amap_req_o, dut_->amap_tag_o, MBX_AMAP_STATUS_TAG_WIDTH,
            {MBX_TB_FIELD(amap_type_o, 16u), MBX_TB_FIELD(amap_index_o, 16u),
             MBX_TB_FIELD(amap_map_index_o, MBX_AMAP_PAGE_MAP_INDEX_WIDTH), MBX_TB_FIELD(amap_sel_o, MBX_AMAP_PAGE_SEL_WIDTH),
             MBX_TB_FIELD(amap_rec_o, MBX_AMAP_PAGE_REC_WIDTH)});
        win(kWinEdit, dut_->edit_req_o, dut_->edit_tag_o, MBX_EDIT_STATUS_TAG_WIDTH,
            {MBX_TB_FIELD(edit_type_o, 16u), MBX_TB_FIELD(edit_index_o, 16u),
             MBX_TB_FIELD(edit_phase_o, MBX_EDIT_BEAT_PHASE_WIDTH), MBX_TB_FIELD(edit_remove_o, MBX_EDIT_BEAT_REMOVE_WIDTH),
             MBX_TB_FIELD(edit_rec_o, MBX_EDIT_BEAT_REC_WIDTH), MBX_TB_FIELD(edit_count_o, MBX_EDIT_BEAT_COUNT_WIDTH),
             MBX_TB_FIELD(edit_record_o, 64u), MBX_TB_FIELD(edit_value_o, 64u)});
        win(kWinGsi, dut_->gsi_req_o, dut_->gsi_tag_o, MBX_GSI_STATUS_TAG_WIDTH,
            {MBX_TB_FIELD(gsi_type_o, 16u), MBX_TB_FIELD(gsi_index_o, 16u), MBX_TB_FIELD(gsi_kind_o, MBX_GSI_SEL_KIND_WIDTH),
             MBX_TB_FIELD(gsi_sel_o, MBX_GSI_SEL_SEL_WIDTH), MBX_TB_FIELD(gsi_ord_o, MBX_GSI_SEL_ORD_WIDTH),
             MBX_TB_FIELD(gsi_prop_o, 64u)});
#undef MBX_TB_FIELD
        return v;
    }

    //! One clock with the datapath's acknowledgement of interface iface's commit.
    void face_ack(unsigned iface) {
        put(dut_->fw_ack_p_i, iface, 1u, 1u);
        step();
    }

    //! One clock with window w's answer on interface iface: its tag and data.
    void win_answer(unsigned w, unsigned iface, std::uint32_t tag, std::uint64_t data) {
        win_data(w, iface, tag, data);
        switch (w) {
        case kWinCtr: put(dut_->ctr_ans_p_i, iface, 1u, 1u); break;
        case kWinAmap: put(dut_->amap_ans_p_i, iface, 1u, 1u); break;
        case kWinEdit: put(dut_->edit_ans_p_i, iface, 1u, 1u); break;
        default: put(dut_->gsi_ans_p_i, iface, 1u, 1u); break;
        }
        step();
    }

    //! Window w's answer tag and data on interface iface, held, with no pulse.
    void win_data(unsigned w, unsigned iface, std::uint32_t tag, std::uint64_t data) {
        switch (w) {
        case kWinCtr:
            put(dut_->ctr_ans_tag_i, MBX_CTR_STATUS_TAG_WIDTH * iface, MBX_CTR_STATUS_TAG_WIDTH, tag);
            put(dut_->ctr_ans_data_i, 32u * iface, 32u, data);
            break;
        case kWinAmap:
            put(dut_->amap_ans_tag_i, MBX_AMAP_STATUS_TAG_WIDTH * iface, MBX_AMAP_STATUS_TAG_WIDTH, tag);
            put(dut_->amap_ans_data_i, 64u * iface, 64u, data);
            break;
        case kWinEdit:
            put(dut_->edit_ans_tag_i, MBX_EDIT_STATUS_TAG_WIDTH * iface, MBX_EDIT_STATUS_TAG_WIDTH, tag);
            put(dut_->edit_ans_data_i, 64u * iface, 64u, data);
            break;
        default:
            put(dut_->gsi_ans_tag_i, MBX_GSI_STATUS_TAG_WIDTH * iface, MBX_GSI_STATUS_TAG_WIDTH, tag);
            put(dut_->gsi_ans_data_i, 64u * iface, 64u, data);
            break;
        }
    }

    //! Window w's open request on interface iface left unanswered past its wait bound.
    void win_expire(unsigned w, unsigned iface) {
        (void)iface;
        idle(kWaitCycles[w] + 2u);
    }

    //! One clock with a face event pulse on interface iface: 0 a counter change
    //! naming (type, index), 1 AVB_INFO, 2 AS_PATH, 3 a live map write.
    void face_event(unsigned kind, unsigned iface, std::uint32_t type = 0, std::uint32_t index = 0) {
        switch (kind) {
        case 0:
            put(dut_->ctr_chg_type_i, 16u * iface, 16u, type);
            put(dut_->ctr_chg_index_i, 16u * iface, 16u, index);
            put(dut_->ctr_chg_p_i, iface, 1u, 1u);
            break;
        case 1:
            put(dut_->avb_chg_p_i, iface, 1u, 1u);
            break;
        case 2:
            put(dut_->asp_chg_p_i, iface, 1u, 1u);
            break;
        default:
            put(dut_->amap_wr_p_i, iface, 1u, 1u);
            break;
        }
        step();
    }

    //! What the publication block drives into interface `iface`'s datapath,
    //! read off tb_mbx_top's pub_*_o ports.
    PubView pub(unsigned iface) const {
        PubView v;
        v.da_gate = static_cast<std::uint32_t>(slice(dut_->pub_da_gate_o, MBX_N_PUB_SOURCES * iface, MBX_N_PUB_SOURCES));
        v.licence = static_cast<std::uint32_t>(slice(dut_->pub_licence_o, MBX_N_PUB_SOURCES * iface, MBX_N_PUB_SOURCES));
        v.idle_slope_bps = static_cast<std::uint32_t>(
            slice(dut_->pub_idle_slope_bps_o, MBX_IDLE_SLOPE_BPS_WIDTH * iface, MBX_IDLE_SLOPE_BPS_WIDTH));
        v.vid = static_cast<std::uint32_t>(slice(dut_->pub_dom_vid_o, MBX_SR_DOMAIN_VID_WIDTH * iface,
                                                 MBX_SR_DOMAIN_VID_WIDTH));
        v.priority = static_cast<std::uint32_t>(
            slice(dut_->pub_dom_prio_o, MBX_SR_DOMAIN_PRIORITY_WIDTH * iface, MBX_SR_DOMAIN_PRIORITY_WIDTH));
        v.adopted = static_cast<std::uint32_t>(
            slice(dut_->pub_dom_adopted_o, MBX_SR_DOMAIN_ADOPTED_WIDTH * iface, MBX_SR_DOMAIN_ADOPTED_WIDTH));
        v.talker_decl = static_cast<std::uint32_t>(
            slice(dut_->pub_talker_decl_o, MBX_N_PUB_SOURCES * iface, MBX_N_PUB_SOURCES));
        for (unsigned s = 0; s < MBX_N_PUB_SOURCES; ++s) {
            v.src_sid.push_back(slice(dut_->pub_src_sid_o, 64u * (MBX_N_PUB_SOURCES * iface + s), 64u));
        }
        v.bound = static_cast<std::uint32_t>(slice(dut_->pub_bound_o, MBX_N_PUB_SINKS * iface, MBX_N_PUB_SINKS));
        v.started = static_cast<std::uint32_t>(slice(dut_->pub_started_o, MBX_N_PUB_SINKS * iface, MBX_N_PUB_SINKS));
        // the stream_id the datapath takes: pub_sid_o while pub_sid_valid_o is set
        for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
            const bool valid = slice(dut_->pub_sid_valid_o, MBX_N_PUB_SINKS * iface + k, 1u) != 0u;
            v.sid.push_back(valid ? slice(dut_->pub_sid_o, 64u * (MBX_N_PUB_SINKS * iface + k), 64u) : 0u);
        }
        return v;
    }

    Vtb_mbx_top* dut() const { return dut_; }
    bool irq() const { return dut_->irq_o != 0; }
    std::uint64_t cycles() const { return cycles_; }
    std::uint64_t reads() const { return reads_; }
    std::uint64_t writes() const { return writes_; }

    std::vector<TxFrame> tx_frames;   //!< every frame the merge sent, in order
    std::function<void()> on_clock;   //!< called after every rising edge, when set (the timing checks' counters)
    unsigned bus_timeouts = 0;        //!< accesses the adapter never answered
    unsigned comb_paths = 0;          //!< AXI4-Lite cycles where an output followed an input
    std::uint64_t probed = 0;         //!< AXI4-Lite cycles the structural probe ran on

    //! Clocks per modeled millisecond: enough for the 16-slot timer scan.
    static constexpr unsigned kClocksPerMs = 24;

 private:
    struct RxByte {
        std::uint8_t data;
        bool last;
        unsigned iface;
    };

    void idle_inputs() {
        dut_->wb_cyc_i = 0;
        dut_->wb_stb_i = 0;
        dut_->s_awvalid_i = 0;
        dut_->s_wvalid_i = 0;
        dut_->s_arvalid_i = 0;
        dut_->s_bready_i = 0;
        dut_->s_rready_i = 0;
        dut_->ms_tick_p_i = 0;
        dut_->gm_change_p_i = 0;
        dut_->rx_valid_i = 0;
        clear_face_pulses();
    }

    //! The face block's one-cycle inputs back to idle.
    void clear_face_pulses() {
        dut_->fw_ack_p_i = 0;
        dut_->ctr_ans_p_i = 0;
        dut_->amap_ans_p_i = 0;
        dut_->edit_ans_p_i = 0;
        dut_->gsi_ans_p_i = 0;
        dut_->ctr_chg_p_i = 0;
        dut_->avb_chg_p_i = 0;
        dut_->asp_chg_p_i = 0;
        dut_->amap_wr_p_i = 0;
    }

    //! Bits [lsb +: width] (width at most 64) of an input port set to value.
    template <class Sig>
    static void put(Sig& sig, unsigned lsb, unsigned width, std::uint64_t value) {
        for (unsigned b = 0; b < width; ++b) {
            const unsigned at = lsb + b;
            const std::uint64_t bit = (value >> b) & 1u;
            if constexpr (std::is_integral_v<Sig>) {
                using U = std::remove_reference_t<Sig>;
                sig = static_cast<U>((static_cast<std::uint64_t>(sig) & ~(std::uint64_t{1} << at)) | (bit << at));
            } else {
                sig[at / 32u] = (sig[at / 32u] & ~(1u << (at % 32u))) | (static_cast<std::uint32_t>(bit) << (at % 32u));
            }
        }
    }

    bool tx_ready_now() const { return ((tx_pattern_ >> (cycles_ % 8)) & 1u) != 0; }

    //! Bits [lsb +: width] (width at most 64) of a port: a Verilator scalar,
    //! or a wide signal of 32-bit words, least significant first.
    template <class Sig>
    static std::uint64_t slice(const Sig& sig, unsigned lsb, unsigned width) {
        std::uint64_t v = 0;
        for (unsigned b = 0; b < width; ++b) {
            const unsigned at = lsb + b;
            std::uint64_t bit = 0;
            if constexpr (std::is_integral_v<Sig>) {
                bit = (static_cast<std::uint64_t>(sig) >> at) & 1u;
            } else {
                bit = (sig[at / 32u] >> (at % 32u)) & 1u;
            }
            v |= bit << b;
        }
        return v;
    }

    //! Every AXI4-Lite output, as one comparable value.
    std::array<std::uint64_t, 8> axil_outputs() const {
        return {dut_->s_awready_o, dut_->s_wready_o, dut_->s_arready_o, dut_->s_bvalid_o,
                dut_->s_bresp_o,   dut_->s_rvalid_o, dut_->s_rdata_o,   dut_->s_rresp_o};
    }

    //! Move each AXI input in turn with the clock held; count a cycle once if
    //! any output followed. The inputs are restored before the edge.
    void probe_axil() {
        ++probed;
        const auto before = axil_outputs();
        bool moved = false;
        auto flip = [&](auto& sig) {
            sig ^= 1u;
            dut_->eval();
            moved = moved || axil_outputs() != before;
            sig ^= 1u;
        };
        flip(dut_->s_awvalid_i);
        flip(dut_->s_wvalid_i);
        flip(dut_->s_arvalid_i);
        flip(dut_->s_bready_i);
        flip(dut_->s_rready_i);
        const auto aw = dut_->s_awaddr_i;
        const auto ar = dut_->s_araddr_i;
        const auto wd = dut_->s_wdata_i;
        const auto ws = dut_->s_wstrb_i;
        dut_->s_awaddr_i = ~aw & 0x7FFCu;
        dut_->s_araddr_i = ~ar & 0x7FFCu;
        dut_->s_wdata_i = ~wd;
        dut_->s_wstrb_i = ~ws & 0xFu;
        dut_->eval();
        moved = moved || axil_outputs() != before;
        dut_->s_awaddr_i = aw;
        dut_->s_araddr_i = ar;
        dut_->s_wdata_i = wd;
        dut_->s_wstrb_i = ws;
        dut_->eval();
        comb_paths += moved ? 1u : 0u;
    }

    void take_tx_byte() {
        if (!tx_open_) {
            tx_frames.push_back(TxFrame{{}, dut_->tx_if_o, dut_->tx_ch_o});
            tx_open_ = true;
        }
        tx_frames.back().bytes.push_back(dut_->tx_data_o);
        if (dut_->tx_last_o) {
            tx_open_ = false;
        }
    }

    std::uint32_t wb(bool we, std::uint32_t byte_offset, std::uint32_t value, std::uint8_t sel) {
        dut_->wb_cyc_i = 1;
        dut_->wb_stb_i = 1;
        dut_->wb_we_i = we ? 1 : 0;
        dut_->wb_adr_i = byte_offset >> 2;
        dut_->wb_dat_i = value;
        dut_->wb_sel_i = sel;
        std::uint32_t data = 0;
        bool acked = false;
        for (int i = 0; i < 16 && !acked; ++i) {
            step();
            if (dut_->wb_ack_o) {
                data = dut_->wb_dat_o;
                acked = true;
            }
        }
        dut_->wb_cyc_i = 0;
        dut_->wb_stb_i = 0;
        step();
        bus_timeouts += acked ? 0u : 1u;
        return data;
    }

    //! AW and W offered together; each is withdrawn after its own handshake.
    void axil_write(std::uint32_t byte_offset, std::uint32_t value, std::uint8_t strobes) {
        dut_->s_awvalid_i = 1;
        dut_->s_wvalid_i = 1;
        dut_->s_awaddr_i = byte_offset;
        dut_->s_wdata_i = value;
        dut_->s_wstrb_i = strobes;
        dut_->s_bready_i = 1;
        bool aw_taken = false;
        bool w_taken = false;
        bool answered = false;
        for (int i = 0; i < 16 && !answered; ++i) {
            dut_->clk_i = 0;
            dut_->eval();
            const bool aw_hs = dut_->s_awvalid_i && dut_->s_awready_o;
            const bool w_hs = dut_->s_wvalid_i && dut_->s_wready_o;
            const bool resp = dut_->s_bvalid_o != 0;
            step();
            if (aw_hs) {
                aw_taken = true;
                dut_->s_awvalid_i = 0;
            }
            if (w_hs) {
                w_taken = true;
                dut_->s_wvalid_i = 0;
            }
            answered = aw_taken && w_taken && resp;
        }
        dut_->s_bready_i = 0;
        bus_timeouts += answered ? 0u : 1u;
    }

    std::uint32_t axil_read(std::uint32_t byte_offset) {
        dut_->s_arvalid_i = 1;
        dut_->s_araddr_i = byte_offset;
        dut_->s_rready_i = 1;
        bool taken = false;
        bool answered = false;
        std::uint32_t data = 0;
        for (int i = 0; i < 16 && !answered; ++i) {
            dut_->clk_i = 0;
            dut_->eval();
            const bool hs = dut_->s_arvalid_i && dut_->s_arready_o;
            const bool resp = dut_->s_rvalid_o != 0;
            if (resp) {
                data = dut_->s_rdata_o;
            }
            step();
            if (hs) {
                taken = true;
                dut_->s_arvalid_i = 0;
            }
            answered = taken && resp;
        }
        dut_->s_rready_i = 0;
        bus_timeouts += answered ? 0u : 1u;
        return data;
    }

    Vtb_mbx_top* dut_;
    unsigned host_;
    std::deque<RxByte> rx_q_;
    bool tx_open_ = false;
    std::uint8_t tx_pattern_ = 0xFF;
    std::uint64_t cycles_ = 0;
    std::uint64_t reads_ = 0;
    std::uint64_t writes_ = 0;
};

}  // namespace mbx_tb

#endif  // MBX_BENCH_HPP
