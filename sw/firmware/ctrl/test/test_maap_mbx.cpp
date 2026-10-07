// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// H-MAAP observes original inputs and accepted TX_HEAD writes on the host.
#include <gtest/gtest.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

#include "fw_gtest.hpp"
#include "ctrl_app.h"
#include "maap_mbx.h"
#include "maap_csr.h"
#include "mbx_model.h"
#include "wire.h"

FW_TALLY_LABEL("ctrl H-MAAP mailbox");

namespace {
constexpr std::uint64_t kMac = 0x020000000080ULL;
constexpr std::uint64_t kBase = 0x91e0f0000100ULL;
using Frame = std::array<std::uint8_t, 60>;

Frame incoming(unsigned type, std::uint64_t destination = MAAP_MULTICAST,
               std::uint64_t requested = kBase) {
    Frame f{};
    wire_put_be(f.data(), destination, 6); wire_put_be(f.data() + 6, 0x060000000040ULL, 6);
    f[12] = 0x22; f[13] = 0xf0; f[14] = 0xfe; f[15] = static_cast<std::uint8_t>(type);
    f[16] = 8; f[17] = 16;
    wire_put_be(f.data() + 26, requested, 6); f[33] = 8;
    if (type == 2) { wire_put_be(f.data() + 34, requested, 6); f[41] = 8; }
    return f;
}

class MaapHost : public ::testing::Test {
 protected:
    mbx_model model{};
    ctrl_loop loop{};
    maap_mbx adapter{};
    std::array<std::uint64_t, MBX_N_IF> macs{};
    std::array<bool, MBX_N_IF> valid{};
    std::vector<std::uint64_t> commits;
    // Reference bus: 100 ns per ordered transaction. No measured CPU claim.
    std::uint64_t now_ns = 0;

    static void allocation(void* ctx, unsigned interface, std::uint64_t, std::uint16_t, bool good) {
        static_cast<MaapHost*>(ctx)->valid.at(interface) = good;
    }
    static void trace(void* ctx, bool write, std::uint32_t offset, std::uint32_t) {
        auto& r = *static_cast<MaapHost*>(ctx);
        auto prior_ms = r.now_ns / 1000000u;
        r.now_ns += 100;
        mbx_model_advance_ms(&r.model, static_cast<unsigned>(r.now_ns / 1000000u - prior_ms));
        if (write && offset == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_MAAP + MBX_CH_REG_TX_HEAD)
            r.commits.push_back(r.now_ns);
    }
    void SetUp() override {
        mbx_model_reset(&model); mbx_model_bind(&model, nullptr, nullptr); mbx_host_trace(trace, this);
        ctrl_loop_init(&loop);
        for (unsigned k = 0; k < MBX_N_IF; ++k) { macs[k] = kMac + k; mbx_model_set_link(&model, k, true); }
        ASSERT_TRUE(maap_mbx_init(&adapter, macs.data(), 8, 2, allocation, this));
        ASSERT_TRUE(maap_mbx_attach(&adapter, &loop));
        ASSERT_TRUE(ctrl_loop_open(&loop, 1, macs.data()));
        ASSERT_TRUE(maap_mbx_start(&adapter, kBase));
        ctrl_loop_service(&loop);
    }
    void TearDown() override { mbx_host_trace(nullptr, nullptr); }
    std::uint64_t accesses() const { return model.reads + model.writes; }
    void advance(unsigned ms) { now_ns += static_cast<std::uint64_t>(ms) * 1000000; mbx_model_advance_ms(&model, ms); }
    void expiry(unsigned interface = 0) {
        const auto slot = adapter.ifs[interface].slot;
        ASSERT_TRUE(model.timers[slot].armed);
        advance(model.timers[slot].deadline_ms - model.now_ms);
        ctrl_loop_service(&loop);
    }
    void acquire() {
        // Other interface expiries can share the pass; stop them for this path.
        for (unsigned k = 1; k < MBX_N_IF; ++k) maap_release(&adapter.ifs[k].core);
        for (unsigned k = 0; k < 3; ++k) expiry();
        ASSERT_TRUE(valid[0]);
    }
    bool inject(const Frame& f, unsigned interface = 0, unsigned len = 60) {
        return mbx_model_rx(&model, f.data(), len, interface);
    }
    bool service_bound(std::uint64_t start) const {
        return !commits.empty() && commits.back() - start <= 10000000ULL;
    }
};

TEST_F(MaapHost, HMaapTimerCommitsAndIntervals) {
    for (unsigned k = 1; k < MBX_N_IF; ++k) maap_release(&adapter.ifs[k].core);
    for (unsigned k = 0; k < 4; ++k) {
        const auto slot = adapter.ifs[0].slot;
        const auto wait = model.timers[slot].deadline_ms - model.now_ms;
        auto deadline = now_ns - now_ns % 1000000u + static_cast<std::uint64_t>(wait) * 1000000u;
        auto before = accesses();
        expiry();
        EXPECT_TRUE(service_bound(deadline)) << "H-MAAP original timer deadline to TX_HEAD within 10 ms";
        EXPECT_LE(accesses() - before, MAAP_MBX_PASS_MAX) << "H-MAAP event work bound";
        std::printf("  H-MAAP timer %u: %llu accesses, %llu ns from original deadline (model)\n", k,
                    static_cast<unsigned long long>(accesses() - before),
                    static_cast<unsigned long long>(commits.back() - deadline));
        const auto* frame = mbx_model_tx_frame(&model, model.tx_sent - 1);
        ASSERT_NE(frame, nullptr);
        EXPECT_EQ(frame->bytes[15], k < 2 ? 1u : 3u);
        EXPECT_EQ(frame->bytes[17], 16u);
        if (k < 3) { EXPECT_GT(wait, 500u); EXPECT_LT(wait, 600u); }
        else { EXPECT_GT(wait, 30000u); EXPECT_LT(wait, 32000u); }
    }
}

TEST_F(MaapHost, HMaapConflictLossAndRetry) {
    acquire();
    auto start = now_ns; auto before = accesses(); auto n = model.tx_sent;
    ASSERT_TRUE(inject(incoming(1)));
    ctrl_loop_service(&loop);
    EXPECT_TRUE(service_bound(start)) << "H-MAAP RX_HEAD to DEFEND TX_HEAD within 10 ms";
    EXPECT_LE(accesses() - before, MAAP_MBX_PASS_MAX);
    std::printf("  H-MAAP DEFEND: %llu accesses, %llu ns from RX_HEAD (model)\n",
                static_cast<unsigned long long>(accesses() - before),
                static_cast<unsigned long long>(commits.back() - start));
    auto frame = mbx_model_tx_frame(&model, n); ASSERT_NE(frame, nullptr);
    EXPECT_EQ(frame->bytes[15], 2u);
    EXPECT_EQ(frame->bytes[0], 6u); EXPECT_EQ(frame->bytes[5], 0x40u) << "unicast DEFEND destination";
    start = now_ns;
    ASSERT_TRUE(inject(incoming(2, macs[0])));
    ctrl_loop_service(&loop);
    EXPECT_FALSE(valid[0]); EXPECT_EQ(adapter.ifs[0].core.state, MAAP_PROBE);
    EXPECT_TRUE(service_bound(start)) << "H-MAAP own unicast DEFEND triggers retry";
    auto current = adapter.ifs[0].core.base;
    start = now_ns; ASSERT_TRUE(inject(incoming(3, MAAP_MULTICAST, current)));
    ctrl_loop_service(&loop);
    EXPECT_TRUE(service_bound(start)); EXPECT_EQ(adapter.ifs[0].core.conflicts, 2u);
    maap_mbx_stop(&adapter);
    EXPECT_EQ(model.maap_count, 0u) << "release closes range filter";
}

TEST_F(MaapHost, HMaapFilterTupleAndRate) {
    auto mismatch = mbx_filter_mismatch();
    for (unsigned type : {1u, 3u}) EXPECT_FALSE(inject(incoming(type, macs[0])));
    EXPECT_FALSE(inject(incoming(2, 0x020000000001ULL)));
    auto bad = incoming(1); bad[14] = 0xff; EXPECT_FALSE(inject(bad));
    EXPECT_EQ(mbx_filter_mismatch(), mismatch + 4) << "tuple refusals counted once";
    bad = incoming(1); bad[12] = 0x81; bad[13] = 0;
    EXPECT_FALSE(inject(bad)); EXPECT_EQ(mbx_filter_mismatch(), mismatch + 4) << "tagged frame uncounted";
    bad = incoming(1, MAAP_MULTICAST, kBase + 100);
    EXPECT_FALSE(inject(bad)); EXPECT_EQ(mbx_filter_mismatch(), mismatch + 4) << "identity refusal uncounted";
    EXPECT_EQ(model.ch[MBX_CH_MAAP].rx_head, model.ch[MBX_CH_MAAP].rx_tail) << "no core delivery for refused frames";
    auto defend = incoming(2, macs[0]); ASSERT_TRUE(inject(defend));
    ctrl_loop_service(&loop); EXPECT_EQ(adapter.ifs[0].core.conflicts, 1u) << "own unicast reaches core";
    auto current = adapter.ifs[0].core.base;
    auto f = incoming(1, MAAP_MULTICAST, current);
    for (unsigned k = 0; k < 12; ++k) {
        (void)inject(f);
        mbx_frame drained{};
        (void)mbx_rx_take(MBX_CH_MAAP, &drained); // keep ring capacity independent of bucket capacity
    }
    EXPECT_GT(model.ch[MBX_CH_MAAP].rate_drop, 0u) << "token bucket enforced separately";
}

TEST_F(MaapHost, HMaapBacklogAndStallNeverRestartClock) {
    acquire();
    auto f = incoming(1);
    // Fill the event ring; the last expiry cannot bypass existing events.
    for (unsigned k = 0; k < 16; ++k) mbx_model_set_gm(&model, 0, k + 2, 0);
    for (unsigned k = 0; k < 7; ++k) ASSERT_TRUE(inject(f));
    auto start = now_ns, before = accesses();
    for (unsigned k = 0; k < 12; ++k) {
        auto pass = accesses(); ctrl_loop_service(&loop);
        EXPECT_LE(accesses() - pass, MAAP_MBX_PASS_MAX) << "H-MAAP full backlog pass bound";
    }
    EXPECT_EQ(model.ch[MBX_CH_MAAP].rx_head, model.ch[MBX_CH_MAAP].rx_tail);
    EXPECT_LE(accesses() - before, 12u * MAAP_MBX_PASS_MAX);
    EXPECT_TRUE(service_bound(start)) << "H-MAAP backlog included";
    mbx_model_tx_pause(&model, true);
    for (unsigned k = 0; k < 7; ++k) ASSERT_EQ(mbx_tx_send(MBX_CH_MAAP, 0, f.data(), 60), MBX_STATUS_OK);
    advance(20); ASSERT_TRUE(inject(f)); start = now_ns;
    auto previous = commits.size(); ctrl_loop_service(&loop);
    EXPECT_EQ(commits.size(), previous); EXPECT_GT(adapter.ifs[0].core.queued, 0u);
    advance(5); mbx_model_tx_pause(&model, false); ctrl_loop_service(&loop);
    EXPECT_TRUE(service_bound(start)) << "H-MAAP short TX stall charged to original RX";
    mbx_model_tx_pause(&model, true);
    for (unsigned k = 0; k < 7; ++k) ASSERT_EQ(mbx_tx_send(MBX_CH_MAAP, 0, f.data(), 60), MBX_STATUS_OK);
    advance(20); ASSERT_TRUE(inject(f)); start = now_ns; ctrl_loop_service(&loop);
    advance(11); mbx_model_tx_pause(&model, false); ctrl_loop_service(&loop);
    EXPECT_FALSE(service_bound(start)) << "late recovery is a failed bound, not a fresh 10 ms";
}

TEST_F(MaapHost, StaleTagsForeignInputsAndLinkEdges) {
    auto& i = adapter.ifs[0];
    mbx_event ev{}; ev.type = MBX_EV_TYPE_TIMER; ev.timer_slot = i.slot;
    ev.timer_tag = static_cast<std::uint16_t>(i.tag - 1);
    loop.sinks[0].fn(loop.sinks[0].ctx, &ev);
    EXPECT_EQ(i.stale_expiries, 1u) << "old timer tag ignored";
    maap_release(&i.core); ev.timer_tag = i.tag;
    loop.sinks[0].fn(loop.sinks[0].ctx, &ev); EXPECT_EQ(i.stale_expiries, 2u);
    ev.timer_slot = MBX_N_TIMERS - 1; loop.sinks[0].fn(loop.sinks[0].ctx, &ev);
    ev.type = MBX_EV_TYPE_GM; loop.sinks[0].fn(loop.sinks[0].ctx, &ev);
    ev.type = MBX_EV_TYPE_LINK; ev.interface = MBX_N_IF;
    loop.sinks[0].fn(loop.sinks[0].ctx, &ev);
    mbx_frame frame{}; frame.interface = MBX_N_IF;
    loop.rx[MBX_CH_MAAP].fn(loop.rx[MBX_CH_MAAP].ctx, &frame);
    EXPECT_EQ(adapter.foreign_if, 2u);
    ASSERT_TRUE(maap_mbx_start(&adapter, kBase));
    mbx_model_set_link(&model, 0, false); ctrl_loop_service(&loop);
    EXPECT_EQ(i.core.state, MAAP_INITIAL); EXPECT_FALSE(valid[0]);
    mbx_model_set_link(&model, 0, true); ctrl_loop_service(&loop);
    EXPECT_EQ(i.core.state, MAAP_PROBE);
    ev.interface = 0; ev.link_up = true; auto n = model.tx_sent;
    loop.sinks[0].fn(loop.sinks[0].ctx, &ev); EXPECT_EQ(model.tx_sent, n) << "duplicate link level ignored";
}

TEST_F(MaapHost, AttachRefusalsAndTimerWrap) {
    maap_mbx other{};
    EXPECT_FALSE(maap_mbx_init(&other, macs.data(), 8, UINT32_MAX, allocation, this));
    EXPECT_FALSE(maap_mbx_init(&other, macs.data(), 8, 0, nullptr, this));
    EXPECT_FALSE(maap_mbx_init(&other, macs.data(), 0, 0, allocation, this));
    EXPECT_FALSE(maap_mbx_attach(&adapter, &loop));
    ctrl_loop full{}; full.n_sinks = CTRL_LOOP_MAX_SINKS;
    EXPECT_FALSE(maap_mbx_attach(&adapter, &full));
    full.n_sinks = 0; full.n_polls = CTRL_LOOP_MAX_POLLS;
    EXPECT_FALSE(maap_mbx_attach(&adapter, &full));
    EXPECT_EQ(full.rx[MBX_CH_MAAP].fn, nullptr) << "no partial attachment";
    maap_mbx_stop(&adapter); model.now_ms = UINT32_MAX - 200u;
    adapter.ifs[0].tag = UINT16_MAX;
    ASSERT_TRUE(maap_mbx_start(&adapter, kBase));
    EXPECT_EQ(adapter.ifs[0].tag, 0u);
    auto n = model.tx_sent; expiry(); EXPECT_GT(model.tx_sent, n) << "deadline wraps with fabric clock";
    EXPECT_FALSE(maap_mbx_start(&adapter, MAAP_POOL_BASE - 1));
}

TEST_F(MaapHost, InterfaceIsolationAndRangeEnvelope) {
    for (unsigned k = 0; k < MBX_N_IF; ++k) {
        ASSERT_TRUE(inject(incoming(2, macs[k]), k));
        ctrl_loop_service(&loop);
        EXPECT_EQ(adapter.ifs[k].core.conflicts, 1u) << "record index selects state";
        for (unsigned j = k + 1; j < MBX_N_IF; ++j) EXPECT_EQ(adapter.ifs[j].core.conflicts, 0u);
    }
    for (unsigned k = 0; k < MBX_N_IF; ++k) {
        const auto& c = adapter.ifs[k].core;
        EXPECT_LE(model.maap_base, c.base);
        EXPECT_GE(model.maap_base + model.maap_count, c.base + c.count) << "filter covers every tentative range";
    }
    for (unsigned k = 0; k < MBX_N_IF; ++k) maap_release(&adapter.ifs[k].core);
    EXPECT_EQ(model.maap_count, 0u);
}

TEST_F(MaapHost, ExplicitAppComposition) {
    maap_mbx_stop(&adapter); mbx_model_reset(&model);
    static std::array<std::uint8_t, 1024> arena;
    const ctrl_pool_class classes[] = {{64, 4}};
    adp_entity entity{}; entity.mac = kMac; entity.entity_id = 1; entity.talker_stream_sources = 8;
    ctrl_app_config config{&entity, 0, arena.data(), arena.size(), classes, 1, nullptr, nullptr, nullptr,
                           nullptr};
    ctrl_app app{};
    for (unsigned k = 0; k < MBX_N_IF; ++k) mbx_model_set_link(&model, k, true);
    EXPECT_FALSE(ctrl_app_start_maap(&app, &config, allocation, this, MAAP_POOL_BASE - 1));
    EXPECT_FALSE(ctrl_app_start_maap(&app, &config, allocation, this, MAAP_POOL_BASE + MAAP_POOL_SIZE));
    EXPECT_FALSE(ctrl_app_start_maap(&app, &config, allocation, this, UINT64_MAX));
    EXPECT_FALSE(ctrl_app_start_maap(&app, &config, nullptr, this, kBase));
    auto saved = config.arena_bytes; config.arena_bytes = 0;
    EXPECT_FALSE(ctrl_app_start_maap(&app, &config, allocation, this, kBase));
    config.arena_bytes = saved;
    ASSERT_TRUE(ctrl_app_start_maap(&app, &config, allocation, this, kBase));
    EXPECT_EQ(model.filter_en, (1u << MBX_CH_ADP) | (1u << MBX_CH_MAAP));
    EXPECT_EQ(app.maap.ifs[0].core.state, MAAP_PROBE);
    EXPECT_NE(app.maap.ifs[0].slot, app.adp.ifs[0].slot) << "protocol timer slots disjoint";
    mbx_model_reset(&model);
    ASSERT_TRUE(ctrl_app_start_maap(&app, &config, allocation, this, 0));
}

// R529-1-F1 probe extended through the actual loop wait/wake boundary.
TEST_F(MaapHost, AppWaitWakesForMaapWithinBudget) {
    maap_mbx_stop(&adapter); mbx_model_reset(&model);
    std::array<std::uint8_t, 1024> arena{};
    const ctrl_pool_class classes[] = {{64, 4}};
    adp_entity entity{}; entity.mac = kMac; entity.entity_id = 1; entity.talker_stream_sources = 8;
    ctrl_app_config config{&entity, 0, arena.data(), arena.size(), classes, 1, nullptr, nullptr, nullptr,
                           nullptr};
    ctrl_app app{};
    for (unsigned k = 0; k < MBX_N_IF; ++k) mbx_model_set_link(&model, k, true);
    ASSERT_TRUE(ctrl_app_start_maap(&app, &config, allocation, this, kBase));
    EXPECT_EQ(model.irq_enable, (1u << (MBX_IRQ_ENABLE_RX_LSB + MBX_CH_ADP)) |
              (1u << (MBX_IRQ_ENABLE_RX_LSB + MBX_CH_MAAP)) | (1u << MBX_IRQ_ENABLE_EVT_LSB))
        << "MAAP wake preserves ADP and event interrupts";
    for (unsigned k = 0; k < MBX_N_IF; ++k) {
        for (unsigned n = 0; n < 8 && ctrl_loop_service(&app.loop); ++n) {}
        ASSERT_FALSE(mbx_model_irq(&model));
        struct WaitInput {
            mbx_model* model;
            const std::uint64_t* now_ns;
            unsigned interface;
            unsigned waits = 0;
            bool woke = false;
            std::uint64_t published_ns = 0;
        } input{&model, &now_ns, k};
        mbx_model_bind(&model, [](void* ctx) {
            auto& w = *static_cast<WaitInput*>(ctx);
            ++w.waits;
            EXPECT_FALSE(mbx_model_irq(w.model)) << "loop entered idle wait";
            w.published_ns = *w.now_ns;
            const auto frame = incoming(1);
            EXPECT_TRUE(mbx_model_rx(w.model, frame.data(), frame.size(), w.interface));
            w.woke = mbx_model_irq(w.model);
        }, &input);
        const auto previous = commits.size();
        ctrl_loop_step(&app.loop);
        EXPECT_EQ(input.waits, 1u);
        EXPECT_TRUE(input.woke) << "accepted MAAP wakes idle loop";
        // A waiting platform cannot service until an enabled cause wakes it.
        if (input.woke) ctrl_loop_step(&app.loop);
        EXPECT_EQ(app.maap.ifs[k].core.conflicts, 1u) << "woken input reaches indexed core";
        ASSERT_EQ(commits.size(), previous + 1u) << "wake commits the conflict retry";
        EXPECT_TRUE(service_bound(input.published_ns)) << "H-MAAP wake from original RX within 10 ms";
        EXPECT_EQ(model.ch[MBX_CH_MAAP].rx_head, model.ch[MBX_CH_MAAP].rx_tail);
        EXPECT_FALSE(mbx_model_irq(&model));
        std::printf("  H-MAAP wake interface %u: %llu ns from RX_HEAD (model)\n", k,
                    static_cast<unsigned long long>(commits.back() - input.published_ns));
        mbx_model_bind(&model, nullptr, nullptr);
    }
    maap_mbx_stop(&app.maap);
}

#if MBX_N_IF > 1
TEST_F(MaapHost, InterfaceOneStallDrainsWithinBudget) {
    maap_release(&adapter.ifs[0].core);
    for (unsigned k = 0; k < 3; ++k) expiry(1);
    ASSERT_TRUE(valid[1]);
    auto f = incoming(1);
    mbx_model_tx_pause(&model, true);
    for (unsigned k = 0; k < 7; ++k) ASSERT_EQ(mbx_tx_send(MBX_CH_MAAP, 0, f.data(), 60), MBX_STATUS_OK);
    ASSERT_TRUE(inject(f, 1));
    auto start = now_ns; auto previous = commits.size();
    ctrl_loop_step(&loop);
    EXPECT_EQ(commits.size(), previous); EXPECT_EQ(adapter.ifs[1].core.queued, 1u);
    advance(5); mbx_model_tx_pause(&model, false);
    const auto before = accesses();
    ctrl_loop_step(&loop);
    EXPECT_LE(accesses() - before, MAAP_MBX_PASS_MAX);
    EXPECT_EQ(adapter.ifs[1].core.queued, 0u) << "interface 1 poll drains deferred output";
    ASSERT_EQ(commits.size(), previous + 1u) << "interface 1 response committed";
    EXPECT_TRUE(service_bound(start)) << "H-MAAP interface 1 stall charged to original RX";
    auto frame = mbx_model_tx_frame(&model, model.tx_sent - 1);
    ASSERT_NE(frame, nullptr);
    EXPECT_EQ(frame->interface, 1u); EXPECT_EQ(frame->bytes[15], 2u);
    std::printf("  H-MAAP interface 1 stall: %llu ns from RX_HEAD (model)\n",
                static_cast<unsigned long long>(commits.back() - start));
}
#endif

TEST_F(MaapHost, CallbackWorkAndEveryOutputCount) {
    // Counts 1..9 cover every shipped AAF+CRF shape; audio rate is not a MAAP input.
    for (unsigned count = 1; count <= 9; ++count) {
        maap_mbx_stop(&adapter); mbx_model_reset(&model); ctrl_loop_init(&loop);
        for (unsigned k = 0; k < MBX_N_IF; ++k) mbx_model_set_link(&model, k, true);
        ASSERT_TRUE(maap_mbx_init(&adapter, macs.data(), count, 2, allocation, this));
        ASSERT_TRUE(maap_mbx_attach(&adapter, &loop));
        ASSERT_TRUE(ctrl_loop_open(&loop, 1, macs.data()));
        ASSERT_TRUE(maap_mbx_start(&adapter, kBase));
        for (unsigned k = 1; k < MBX_N_IF; ++k) maap_release(&adapter.ifs[k].core);
        for (unsigned retry = 0; retry < 3; ++retry) {
            auto& i = adapter.ifs[0];
            mbx_event ev{}; ev.type = MBX_EV_TYPE_TIMER; ev.timer_slot = i.slot; ev.timer_tag = i.tag;
            auto before = accesses();
            loop.sinks[0].fn(loop.sinks[0].ctx, &ev);
            EXPECT_LE(accesses() - before, MAAP_MBX_EVENT_MAX) << "callback work bound";
            if (retry == 2) {
                EXPECT_EQ(accesses() - before, 48u) << "final probe and ANNOUNCE cost";
            }
        }
        EXPECT_TRUE(valid[0]) << "every output count acquired";
        EXPECT_EQ(adapter.ifs[0].core.count, count);
    }
}

TEST_F(MaapHost, IgnoredInputCommitsStateWithinOriginalBudget) {
    for (unsigned k = 1; k < MBX_N_IF; ++k) maap_release(&adapter.ifs[k].core);
    auto probe = incoming(1); probe[11] = 0xc0; // local reversed-octet priority wins
    auto start = now_ns; auto n = commits.size();
    ASSERT_TRUE(inject(probe));
    ctrl_loop_service(&loop);
    EXPECT_EQ(commits.size(), n) << "ignored input does not transmit";
    EXPECT_EQ(adapter.ifs[0].core.state, MAAP_PROBE);
    EXPECT_LE(now_ns - start, 10000000u) << "state completion uses original RX budget";
}

TEST_F(MaapHost, AcquiredRangeFeedsExistingCsrPath) {
    struct Destination {
        std::array<std::array<std::uint32_t, 1024>, MBX_N_IF> words{};
        maap_csr output{};
    } destination;
    const maap_csr_port csr_port{&destination,
        [](void* ctx, unsigned interface, std::uint32_t offset) {
            return static_cast<Destination*>(ctx)->words.at(interface).at(offset / 4);
        },
        [](void* ctx, unsigned interface, std::uint32_t offset, std::uint32_t value) {
            static_cast<Destination*>(ctx)->words.at(interface).at(offset / 4) = value;
        }};
    ASSERT_TRUE(maap_csr_init(&destination.output, csr_port, 8, true, 1, 1));
    maap_mbx_stop(&adapter); mbx_model_reset(&model); ctrl_loop_init(&loop);
    mbx_model_set_link(&model, 0, true);
    ASSERT_TRUE(maap_mbx_init(&adapter, macs.data(), 9, 2, maap_csr_allocation, &destination.output));
    ASSERT_TRUE(maap_mbx_attach(&adapter, &loop));
    ASSERT_TRUE(ctrl_loop_open(&loop, 1, macs.data()));
    ASSERT_TRUE(maap_mbx_start(&adapter, kBase));
    for (unsigned k = 0; k < 3; ++k) expiry();
    const auto& words = destination.words[0];
    EXPECT_EQ(words[0x658 / 4], static_cast<std::uint32_t>(kBase)) << "allocation reaches AAF CSR";
    EXPECT_EQ(words[0x65c / 4], kBase >> 32);
    EXPECT_EQ(words[0x75c / 4], static_cast<std::uint32_t>(kBase + 8)) << "allocation reaches CRF CSR";
    EXPECT_EQ(words[0x654 / 4], 1u);
    ASSERT_TRUE(inject(incoming(2, macs[0]))); ctrl_loop_service(&loop);
    EXPECT_EQ(words[0x654 / 4], 0u) << "conflict withdraws media admission";
    EXPECT_EQ(words[0x750 / 4], 0u);
    // Stop protocol activity before the callback's context goes away.
    maap_mbx_stop(&adapter);
}
} // namespace
