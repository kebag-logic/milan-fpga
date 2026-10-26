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
    FaceView face(unsigned iface) const {
        mbx_model_face f;
        mbx_model_face_view(m_, iface, &f);
        const std::uint32_t req[kWindows] = {f.req[0], f.req[1], f.req[2], f.req[3]};
        const std::uint32_t tag[kWindows] = {f.tag[0], f.tag[1], f.tag[2], f.tag[3]};
        auto word = [&](std::uint32_t reg) -> std::uint32_t {
            switch (reg) {
            case MBX_FACE_REG_F_CTRL: return f.ctrl;
            case MBX_FACE_REG_F_ENTITY: return f.entity;
            case MBX_FACE_REG_F_CLOCK: return f.clock;
            case MBX_FACE_REG_F_AECP: return f.aecp;
            case MBX_FACE_REG_F_RESTORE: return f.restore;
            default: return f.nvm;
            }
        };
        auto src = [&](unsigned s, std::uint32_t reg) -> std::uint32_t {
            switch (reg) {
            case MBX_FACE_SRC_REG_F_PT_OFFSET: return f.pt_offset[s];
            case MBX_FACE_SRC_REG_F_FMT_OUT_LO: return static_cast<std::uint32_t>(f.fmt_out[s]);
            case MBX_FACE_SRC_REG_F_FMT_OUT_HI: return static_cast<std::uint32_t>(f.fmt_out[s] >> 32);
            default: return f.src_valid[s];
            }
        };
        auto snk = [&](unsigned k, std::uint32_t reg) -> std::uint32_t {
            switch (reg) {
            case MBX_FACE_SNK_REG_F_FMT_IN_LO: return static_cast<std::uint32_t>(f.fmt_in[k]);
            case MBX_FACE_SNK_REG_F_FMT_IN_HI: return static_cast<std::uint32_t>(f.fmt_in[k] >> 32);
            default: return f.snk_valid[k];
            }
        };
        // a window's request registers, by offset, in the order the model holds them
        static const std::uint32_t regs[kWindows][MBX_MODEL_WIN_WORDS] = {
            {MBX_FACE_REG_CTR_REQ, MBX_FACE_REG_CTR_WORD},
            {MBX_FACE_REG_AMAP_REQ, MBX_FACE_REG_AMAP_PAGE},
            {MBX_FACE_REG_EDIT_REQ, MBX_FACE_REG_EDIT_BEAT, MBX_FACE_REG_EDIT_RECORD_LO, MBX_FACE_REG_EDIT_RECORD_HI,
             MBX_FACE_REG_EDIT_VALUE_LO, MBX_FACE_REG_EDIT_VALUE_HI},
            {MBX_FACE_REG_GSI_REQ, MBX_FACE_REG_GSI_SEL, MBX_FACE_REG_GSI_PROP_LO, MBX_FACE_REG_GSI_PROP_HI}};
        auto request = [&](unsigned w, std::uint32_t reg) -> std::uint32_t {
            for (unsigned k = 0; k < MBX_MODEL_WIN_WORDS; ++k) {
                if (regs[w][k] == reg && (k == 0u || regs[w][k] != 0u)) {
                    return f.request[w][k];
                }
            }
            return 0u;
        };
        return face_from_words(f.send ? 1u : 0u, word, src, snk, req, tag, request);
    }
    void face_ack(unsigned iface) { mbx_model_face_ack(m_, iface); }
    void win_answer(unsigned w, unsigned iface, std::uint32_t tag, std::uint64_t data) {
        mbx_model_win_answer(m_, iface, w, static_cast<std::uint8_t>(tag), data);
    }
    void win_expire(unsigned w, unsigned iface) { mbx_model_win_expire(m_, iface, w); }
    void face_event(unsigned kind, unsigned iface, std::uint32_t type = 0, std::uint32_t index = 0) {
        mbx_model_face_event(m_, iface, static_cast<mbx_model_face_ev>(kind), static_cast<std::uint16_t>(type),
                             static_cast<std::uint16_t>(index));
    }
    PubView pub(unsigned iface) const {
        mbx_model_pub v;
        mbx_model_pub_view(m_, iface, &v);
        PubView out;
        out.da_gate = v.da_gate;
        out.licence = v.licence;
        out.idle_slope_bps = v.idle_slope_bps;
        out.vid = v.vid;
        out.priority = v.priority;
        out.adopted = v.adopted ? 1u : 0u;
        out.talker_decl = v.talker_decl;
        for (unsigned k = 0; k < MBX_N_PUB_SINKS; ++k) {
            out.bound |= (v.bound[k] ? 1u : 0u) << k;
            out.started |= (v.started[k] ? 1u : 0u) << k;
            out.sid.push_back(v.sid[k]);
        }
        return out;
    }

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
