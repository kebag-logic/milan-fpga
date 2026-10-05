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
#include <vector>

#include "Vtb_mbx_top.h"
#include "frames.hpp"

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
        if (rx_taken) {
            rx_q_.pop_front();
        }
        dut_->ms_tick_p_i = 0;
        dut_->gm_change_p_i = 0;
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
        dut_->gm_id_i = gm;
        dut_->gptp_domain_i = domain;
        (void)iface;
    }

    void set_link(unsigned mask) { dut_->link_up_i = mask; }

    //! Queue one frame on the ingress stream; it leaves at the RTL's pace.
    void send_frame(const std::vector<std::uint8_t>& frame, unsigned iface) {
        for (std::size_t i = 0; i < frame.size(); ++i) {
            rx_q_.push_back(RxByte{frame[i], i + 1 == frame.size(), iface});
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

    Vtb_mbx_top* dut() const { return dut_; }
    bool irq() const { return dut_->irq_o != 0; }
    std::uint64_t cycles() const { return cycles_; }
    std::uint64_t reads() const { return reads_; }
    std::uint64_t writes() const { return writes_; }

    std::vector<TxFrame> tx_frames;   //!< every frame the merge sent, in order
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
    }

    bool tx_ready_now() const { return ((tx_pattern_ >> (cycles_ % 8)) & 1u) != 0; }

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
