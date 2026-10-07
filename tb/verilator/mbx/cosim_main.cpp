// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// cosim_main.cpp - the control-plane firmware (the mailbox driver, the event
// loop, the lwSRP port layer, the ADP slice and the ACMP module, compiled as
// C11 exactly as the target builds them) run twice on one scenario: once on
// the RTL, KL_mbx behind KL_mbx_wb with every mbx_hal.h access a Wishbone
// transaction, and once on the host model the firmware's own tests use (#665
// lanes F0 and F3).
//
// THE ORACLE IS THE OTHER FABRIC. Both runs see the same stimulus at the same
// NOW_MS (a link rise, an ENTITY_DISCOVER, a grandmaster change, a shutdown;
// a BIND_RX left unanswered through its probe, duplicate and retry, the
// talker's and the listener's other commands, a command for another listener
// and an ENTITY_AVAILABLE, which both filters refuse), and the firmware's
// random delays are seeded from NOW_MS, so the two runs
// must put the same frames on the wire at the same millisecond. A frame that
// differs, or leaves at another time, is a difference between the model and
// the RTL that the firmware can see; the per-check suites (suite.hpp) catch
// the differences the firmware cannot.

#include <cstdint>
#include <cstdio>
#include <memory>
#include <vector>

#include "../../common/verilator_harness.hpp"
#include "Vtb_mbx_top.h"
#include "bench.hpp"
#include "verilated.h"

#include "ctrl_app.h"
#include "mbx_hal.h"
#include "mbx_model.h"

namespace {

constexpr std::uint64_t kGm0 = 0xA1A2A3A4A5A6A7A8ull;
constexpr std::uint64_t kGm1 = 0x5150515051505150ull;
constexpr std::uint64_t kEntityId = 0x0011223344556677ull;
constexpr std::uint64_t kMac = 0x001B92000077ull;
constexpr std::uint64_t kTalker = 0x0202DEADBEEF0001ull;
constexpr std::uint64_t kController = 0x1111222233334444ull;

//! One fabric the firmware can run on.
class Fabric {
 public:
    virtual ~Fabric() = default;
    virtual std::uint32_t read(std::uint32_t off) = 0;
    virtual void write(std::uint32_t off, std::uint32_t v) = 0;
    virtual void ms() = 0;
    virtual void link(bool up) = 0;
    virtual void gm_change(std::uint64_t gm) = 0;
    virtual void frame(const std::vector<std::uint8_t>& f) = 0;
    //! Frames that left since the last call.
    virtual std::vector<std::vector<std::uint8_t>> sent() = 0;
};

class RtlFabric final : public Fabric {
 public:
    explicit RtlFabric(Vtb_mbx_top* dut) : b_(dut, 0) {
        b_.reset();
        b_.set_gm(0, kGm0, 0);
        b_.set_link(0);
        b_.idle(8);
    }
    std::uint32_t read(std::uint32_t off) override { return b_.read(off); }
    void write(std::uint32_t off, std::uint32_t v) override { b_.write(off, v); }
    void ms() override { b_.ms(1); }
    void link(bool up) override {
        b_.set_link(up ? 1u : 0u);
        b_.idle(8);
    }
    void gm_change(std::uint64_t gm) override {
        b_.gm_change(0, gm, 0);
        b_.idle(8);
    }
    void frame(const std::vector<std::uint8_t>& f) override {
        b_.send_frame(f, 0);
        (void)b_.drain_rx();
    }
    std::vector<std::vector<std::uint8_t>> sent() override {
        // a record committed by the last access starts within a few clocks of
        // its doorbell (IDLE, the commit-order scan's N_CH + 1 steps, PICK,
        // W0, W1, LOAD: 11 with five channels); give it those, then let it
        // finish. Repeat while a frame finished: a pass can commit two (an
        // ACMP BIND_RX's response and its probe), and the second starts only
        // after the first has left, which may already be on the stream here
        const auto finished = [this] { return b_.tx_frames.size() - (b_.tx_open() ? 1u : 0u); };
        std::size_t before = 0;
        do {
            before = finished();
            b_.idle(16);
            (void)b_.wait_tx(b_.tx_frames.size(), 400);
        } while (finished() != before);
        std::vector<std::vector<std::uint8_t>> out;
        for (const auto& t : b_.tx_frames) {
            out.push_back(t.bytes);
        }
        b_.tx_frames.clear();
        return out;
    }
    unsigned timeouts() const { return b_.bus_timeouts; }

 private:
    mbx_tb::Bench b_;
};

class ModelFabric final : public Fabric {
 public:
    ModelFabric() {
        mbx_model_reset(m_.get());
        mbx_model_set_gm(m_.get(), 0, kGm0, 0);
    }
    std::uint32_t read(std::uint32_t off) override { return mbx_model_read(m_.get(), off); }
    void write(std::uint32_t off, std::uint32_t v) override { mbx_model_write(m_.get(), off, v, 0xF); }
    void ms() override { mbx_model_advance_ms(m_.get(), 1); }
    void link(bool up) override { mbx_model_set_link(m_.get(), 0, up); }
    void gm_change(std::uint64_t gm) override { mbx_model_gm_change(m_.get(), 0, gm, 0); }
    void frame(const std::vector<std::uint8_t>& f) override { (void)mbx_model_rx(m_.get(), f.data(), f.size(), 0); }
    std::vector<std::vector<std::uint8_t>> sent() override {
        std::vector<std::vector<std::uint8_t>> out;
        for (; seen_ < m_->tx_sent; ++seen_) {
            const mbx_model_tx* t = mbx_model_tx_frame(m_.get(), seen_);
            out.emplace_back(t->bytes, t->bytes + t->len);
        }
        return out;
    }

 private:
    std::unique_ptr<mbx_model> m_ = std::make_unique<mbx_model>();
    std::uint32_t seen_ = 0;
};

//! The fabric mbx_hal.h reaches, chosen per run.
Fabric*& current() {
    static Fabric* fabric = nullptr;
    return fabric;
}

//! One frame on the wire and the NOW_MS it left at.
struct Sent {
    std::uint32_t ms;
    std::vector<std::uint8_t> bytes;
};

std::vector<std::uint8_t> discover0() {
    std::vector<std::uint8_t> f(82, 0);
    const std::uint8_t head[] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00, 0, 0x1B, 0x92, 0, 0, 1, 0x22, 0xF0, 0xFA, 0x02};
    for (std::size_t i = 0; i < sizeof head; ++i) {
        f[i] = head[i];
    }
    return f;
}

void put_be(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t v, unsigned n) {
    for (unsigned k = 0; k < n; ++k) {
        f[at + k] = static_cast<std::uint8_t>(v >> (8u * (n - 1u - k)));
    }
}

//! A 70-byte ACMP frame (Milan v1.2 5.5.2.2; IEEE 1722.1-2021 Figure 8-1) to the ACMP multicast address.
std::vector<std::uint8_t> acmp_frame(std::uint8_t msg, std::uint64_t talker, std::uint64_t listener, std::uint16_t seq) {
    std::vector<std::uint8_t> f(70, 0);
    put_be(f, 0, 0x91E0F0010000ull, 6);
    put_be(f, 6, 0x001B92000099ull, 6);
    put_be(f, 12, 0x22F0u, 2);
    f[14] = 0xFC;
    f[15] = msg;
    put_be(f, 16, 44u, 2);
    put_be(f, 26, kController, 8);
    put_be(f, 34, talker, 8);
    put_be(f, 42, listener, 8);
    put_be(f, 62, seq, 2);
    return f;
}

//! The talker's ENTITY_AVAILABLE (IEEE 1722.1-2021 Figure 6-1, valid_time 10).
std::vector<std::uint8_t> available() {
    std::vector<std::uint8_t> f = discover0();
    f[15] = 0x00;
    put_be(f, 16, (10u << 11) | 56u, 2);
    put_be(f, 18, kTalker, 8);
    put_be(f, 50, 1u, 4);
    put_be(f, 54, kGm0, 8);
    return f;
}

bool env_locked(void*, std::uint64_t*) { return false; }
void env_source(void*, unsigned, acmp_source_state* out) {
    *out = acmp_source_state{true, {0x001B920000770000ull, 0x91E0FE000001ull, 2u}, false};
}
void env_srp(void*, unsigned, const acmp_stream*) {}
void env_note(void*, unsigned) {}

//! The ACMP stimulus: message_type and frame per NOW_MS.
std::vector<std::uint8_t> acmp_at(std::uint32_t t) {
    switch (t) {
        case 1000u: return acmp_frame(6, kTalker, kEntityId, 0x0101);    // BIND_RX: response, probe, duplicate, retry
        case 2000u: return available();                                  // refused by the adp channel's filter
        case 3000u: return acmp_frame(4, kEntityId, kTalker, 0x0102);    // GET_TX_STATE
        case 3500u: return acmp_frame(0, kEntityId, kTalker, 0x0103);    // PROBE_TX
        case 4000u: return acmp_frame(6, kTalker, kTalker, 0x0104);      // another listener's: refused
        case 6000u: return acmp_frame(10, kTalker, kEntityId, 0x0105);   // GET_RX_STATE, in PRB_W_AVAIL
        case 7000u: return acmp_frame(8, kTalker, kEntityId, 0x0106);    // UNBIND_RX
        default: return {};
    }
}

//! The scenario: boot, link rise, two advertising cycles, a DISCOVER, a GM
//! change, a shutdown, and the ACMP stimulus of acmp_at().
std::vector<Sent> scenario(Fabric& fab) {
    current() = &fab;
    const adp_entity entity{kEntityId, 0x99AABBCCDDEEFF01ull, kMac, 0x0000C588u, 2, 0x4801, 2, 0x4801, 0};
    acmp_config acmp_cfg{};
    acmp_cfg.entity_id = kEntityId;
    acmp_cfg.n_interfaces = 1;
    acmp_cfg.mac[0] = kMac;
    acmp_cfg.n_sinks = 1;
    acmp_cfg.n_sources = 1;
    const acmp_env acmp_env_{nullptr, env_locked, env_source, env_srp, env_note, env_note};
    const ctrl_pool_class classes[1] = {{32u, 8u}};
    std::vector<std::uint8_t> arena(1024);
    const auto app = std::make_unique<ctrl_app>();
    const ctrl_app_config cfg{&entity, 0, arena.data(), arena.size(), classes, 1, nullptr, nullptr, &acmp_cfg,
                              &acmp_env_};
    std::vector<Sent> out;
    if (!ctrl_app_start(app.get(), &cfg)) {
        return out;
    }
    for (std::uint32_t t = 0; t < 21000u; ++t) {
        const std::vector<std::uint8_t> acmp = acmp_at(t);
        if (t == 50u) {
            fab.link(true);
        } else if (t == 12000u) {
            fab.frame(discover0());
        } else if (t == 16000u) {
            fab.gm_change(kGm1);
        } else if (!acmp.empty()) {
            fab.frame(acmp);
        }
        fab.ms();
        while (ctrl_loop_service(&app->loop) != 0u) {
        }
        if (t == 20000u) {
            adp_mbx_set_enable(&app->adp, false);
        }
        for (auto& f : fab.sent()) {
            out.push_back(Sent{t, std::move(f)});
        }
    }
    current() = nullptr;
    return out;
}

}  // namespace

extern "C" std::uint32_t mbx_hal_read32(std::uint32_t byte_offset) { return current()->read(byte_offset); }
extern "C" void mbx_hal_write32(std::uint32_t byte_offset, std::uint32_t value) {
    current()->write(byte_offset, value);
}
extern "C" void mbx_hal_wait(void) {}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<Vtb_mbx_top> model;
    milan::tb::Checker check{"mbx cosim (firmware on the RTL and on the model)"};
    ModelFabric host;
    const std::vector<Sent> on_model = scenario(host);
    RtlFabric rtl(model.get());
    const std::vector<Sent> on_rtl = scenario(rtl);
    unsigned adp = 0;
    std::vector<unsigned> acmp;
    for (const auto& s : on_model) {
        adp += s.bytes.size() > 15 && s.bytes[14] == 0xFA ? 1u : 0u;
        if (s.bytes.size() > 15 && s.bytes[14] == 0xFC) {
            acmp.push_back(s.bytes[15] & 0x0Fu);
        }
    }
    check.that("the firmware advertised on the model (AVAILABLE x4 or more, then DEPARTING)", adp >= 5u);
    // BIND_RX_RESPONSE, PROBE_TX_COMMAND and its duplicate (Milan v1.2
    // 5.5.3.5.3, 5.5.3.5.16), GET_TX_STATE_RESPONSE, PROBE_TX_RESPONSE,
    // GET_RX_STATE_RESPONSE, UNBIND_RX_RESPONSE; nothing for the refused two
    const std::vector<unsigned> want{7, 0, 0, 5, 1, 11, 9};
    check.that("the firmware answered ACMP on the model, each frame of the scenario in order", acmp == want);
    check.dec("the RTL put as many frames on the wire as the model", on_rtl.size(), on_model.size());
    for (std::size_t k = 0; k < on_model.size() && k < on_rtl.size(); ++k) {
        char what[96];
        std::snprintf(what, sizeof what, "frame %zu leaves at the same NOW_MS", k);
        check.dec(what, on_rtl[k].ms, on_model[k].ms);
        std::snprintf(what, sizeof what, "frame %zu is the same, byte for byte", k);
        check.that(what, on_rtl[k].bytes == on_model[k].bytes);
    }
    for (std::size_t k = 0; k < on_rtl.size(); ++k) {
        const bool is_acmp = on_rtl[k].bytes.size() > 15 && on_rtl[k].bytes[14] == 0xFC;
        std::printf("  frame %zu: NOW_MS %u, %s message_type %u, %s %u\n", k, on_rtl[k].ms, is_acmp ? "ACMP" : "ADP",
                    on_rtl[k].bytes.size() > 15 ? on_rtl[k].bytes[15] & 0x0Fu : 99u,
                    is_acmp ? "sequence_id" : "available_index",
                    is_acmp ? (on_rtl[k].bytes[62] << 8 | on_rtl[k].bytes[63])
                            : on_rtl[k].bytes.size() > 53 ? static_cast<unsigned>(on_rtl[k].bytes[53]) : 99u);
    }
    check.dec("every Wishbone access was answered", rtl.timeouts(), 0);
    return check.report();
}
