// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// model_bench.hpp - the mailbox suite's bench calls (tb/verilator/mbx/
// suite.hpp) answered by the host model instead of the RTL (#665 lane F0).
//
// The model is transaction-level: a frame is filtered when it is offered and
// a TX record leaves when its doorbell is written, so the bench's clock calls
// (idle, drain_rx) have nothing to wait for and the TX ready pattern has no
// clock to apply to, except that a pattern of 0 (a sink that takes nothing)
// pauses the merge until a pattern that takes something. Everything the
// checks read goes through the model's host port, exactly as the firmware's
// reads do.

#ifndef MBX_MODEL_BENCH_HPP
#define MBX_MODEL_BENCH_HPP

#include <cstdint>
#include <vector>

#include "frames.hpp"
#include "mbx_model.h"

namespace mbx_tb {

class ModelBench {
 public:
    explicit ModelBench(mbx_model* model) : m_(model) {}

    void reset() {
        mbx_model_reset(m_);
        synced_ = 0;
    }
    void idle(unsigned n) {
        (void)n;
        sync_tx();
    }
    void ms(unsigned n = 1) {
        mbx_model_advance_ms(m_, n);
        sync_tx();
    }
    void set_link(unsigned mask) {
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mbx_model_set_link(m_, i, ((mask >> i) & 1u) != 0u);
        }
    }
    void set_gm(unsigned iface, std::uint64_t gm, std::uint8_t domain) { mbx_model_set_gm(m_, iface, gm, domain); }
    void gm_change(unsigned iface, std::uint64_t gm, std::uint8_t domain) {
        mbx_model_gm_change(m_, iface, gm, domain);
    }
    void send_frame(const std::vector<std::uint8_t>& frame, unsigned iface) {
        (void)mbx_model_rx(m_, frame.data(), frame.size(), iface);
    }
    bool drain_rx(unsigned patience = 0) {
        (void)patience;
        return true;
    }
    bool wait_tx(std::size_t n, unsigned patience = 0) {
        (void)patience;
        sync_tx();
        return tx_frames.size() >= n;
    }
    void tx_ready_pattern(std::uint8_t pattern) {
        mbx_model_tx_pause(m_, pattern == 0u);
        sync_tx();
    }
    std::uint32_t read(std::uint32_t off) { return mbx_model_read(m_, off); }
    void write(std::uint32_t off, std::uint32_t v, std::uint8_t strobes = 0xF) {
        mbx_model_write(m_, off, v, strobes);
        sync_tx();
    }
    bool irq() const { return mbx_model_irq(m_); }

    std::vector<TxFrame> tx_frames;
    unsigned bus_timeouts = 0;

 private:
    // Copy the frames the model sent since the last call into tx_frames. A
    // harness that clears tx_frames sees only frames sent after the clear.
    void sync_tx() {
        for (; synced_ < m_->tx_sent; ++synced_) {
            const mbx_model_tx* f = mbx_model_tx_frame(m_, synced_);
            if (f != nullptr) {
                tx_frames.push_back(TxFrame{std::vector<std::uint8_t>(f->bytes, f->bytes + f->len),
                                            f->interface, f->channel});
            }
        }
    }

    mbx_model* m_;
    std::uint32_t synced_ = 0;
};

}  // namespace mbx_tb

#endif  // MBX_MODEL_BENCH_HPP
