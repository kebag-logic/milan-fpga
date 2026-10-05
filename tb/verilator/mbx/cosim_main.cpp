// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// cosim_main.cpp - the control-plane firmware (the mailbox driver, the event
// loop, the lwSRP port layer and the ADP slice, compiled as C11 exactly as the
// target builds them) run twice on one scenario: once on the RTL, KL_mbx
// behind KL_mbx_wb with every mbx_hal.h access a Wishbone transaction, and
// once on the host model the firmware's own tests use (#665 lane F0).
//
// THE ORACLE IS THE OTHER FABRIC. Both runs see the same stimulus at the same
// NOW_MS (a link rise, an ENTITY_DISCOVER, a grandmaster change, a shutdown),
// and the firmware's random delays are seeded from NOW_MS, so the two runs
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
        // its doorbell (IDLE, W0, W1, LOAD); give it those, then let it finish
        b_.idle(8);
        (void)b_.wait_tx(b_.tx_frames.size(), 400);
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

//! The scenario: boot, link rise, two advertising cycles, a DISCOVER, a GM change, a shutdown.
std::vector<Sent> scenario(Fabric& fab) {
    current() = &fab;
    const adp_entity entity{0x0011223344556677ull, 0x99AABBCCDDEEFF01ull, 0x001B92000077ull, 0x0000C588u, 2, 0x4801,
                            2, 0x4801, 0};
    const ctrl_pool_class classes[1] = {{32u, 8u}};
    std::vector<std::uint8_t> arena(1024);
    const auto app = std::make_unique<ctrl_app>();
    const ctrl_app_config cfg{&entity, 0, arena.data(), arena.size(), classes, 1, nullptr, nullptr};
    std::vector<Sent> out;
    if (!ctrl_app_start(app.get(), &cfg)) {
        return out;
    }
    for (std::uint32_t t = 0; t < 21000u; ++t) {
        if (t == 50u) {
            fab.link(true);
        } else if (t == 12000u) {
            fab.frame(discover0());
        } else if (t == 16000u) {
            fab.gm_change(kGm1);
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
    check.that("the firmware advertised on the model (AVAILABLE x4 or more, then DEPARTING)", on_model.size() >= 5u);
    check.dec("the RTL put as many frames on the wire as the model", on_rtl.size(), on_model.size());
    for (std::size_t k = 0; k < on_model.size() && k < on_rtl.size(); ++k) {
        char what[96];
        std::snprintf(what, sizeof what, "frame %zu leaves at the same NOW_MS", k);
        check.dec(what, on_rtl[k].ms, on_model[k].ms);
        std::snprintf(what, sizeof what, "frame %zu is the same, byte for byte", k);
        check.that(what, on_rtl[k].bytes == on_model[k].bytes);
    }
    for (std::size_t k = 0; k < on_rtl.size(); ++k) {
        std::printf("  frame %zu: NOW_MS %u, message_type %u, available_index %u\n", k, on_rtl[k].ms,
                    on_rtl[k].bytes.size() > 15 ? on_rtl[k].bytes[15] & 0x0Fu : 99u,
                    on_rtl[k].bytes.size() > 53 ? static_cast<unsigned>(on_rtl[k].bytes[53]) : 99u);
    }
    check.dec("every Wishbone access was answered", rtl.timeouts(), 0);
    return check.report();
}
