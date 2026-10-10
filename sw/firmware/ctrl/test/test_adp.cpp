// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_adp.cpp - the ADP slice beyond the processor's walk (#665 lanes F0
// and FT; GoogleTest):
//
//   A   the core over fake ports is the TSN stack's own (#697): the
//       tsn-c-stack submodule's tests/test_adp.cpp, linked into the same
//       binary by the adp arm (ctrl_arms.ADP_TESTS);
//   B   the mailbox adapter on the model: an expiry that raced a re-arm is
//       discarded by its tag;
//   C   the service-latency bound of every response path (adp_mbx.h), counted
//       access by access on the model, in the pass that takes the input;
//   E   a frame owed behind a full transmit ring, with a HAL that really
//       sleeps until the mailbox interrupt: the loop must not sleep on it,
//       and once the ring drains the frame leaves with its timer restarted;
//       and the same through the mailbox for a DEPARTING owed across a
//       restart whose TMR_DELAY expires first (E4); and the pass in which an
//       ENTITY_AVAILABLE behind owed DEPARTINGs is committed (E5);
//   F   the bound with full legal backlogs (ctrl_loop.h A1 to A4): both
//       rings full, ticks coalesced behind them, every pass and path held to
//       the stated figures, events first in every pass.
//
// One test per labelled step or scenario; each assertion carries the check's
// name from the hand-rolled suite it replaces (sw/firmware/gtest/README.md,
// "The port").

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <tuple>

#include "adp.h"
#include "adp_mbx.h"
#include "ctrl_app.h"
#include "fw_gtest.hpp"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "wire.h"

FW_TALLY_LABEL("ctrl ADP slice (fake ports and host model)");

namespace {

const struct adp_entity entity = {
    .entity_id = 0x1122334455667788ull,
    .entity_model_id = 0x99AABBCCDDEEFF01ull,
    .mac = 0x001B921122AAull,
    .entity_capabilities = 0xC588u,
    .talker_stream_sources = 8u,
    .talker_capabilities = 0x4801u,
    .listener_stream_sinks = 8u,
    .listener_capabilities = 0x4801u,
    .identify_control_index = 5u,
};

void discover(uint8_t* f, uint8_t msg, uint64_t eid) {
    std::memset(f, 0, ADP_FRAME_BYTES);
    wire_put_be(f, 0x91E0F0010000ull, 6);
    wire_put_be(f + 12, ADP_ETHERTYPE, 2);
    f[14] = ADP_SUBTYPE;
    f[15] = msg;
    wire_put_be(f + 18, eid, 8);
}

// ---- the adapter and the latency bounds, on the model ---------------------------

struct mbx_model model;
struct ctrl_app app;
alignas(std::max_align_t) uint8_t arena[1024];
const struct ctrl_pool_class classes[] = {{32u, 8u}};

void boot(void) {
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr, nullptr,
                                   nullptr, nullptr, 0};
    EXPECT_TRUE(ctrl_app_start(&app, &cfg)) << "B0 the app starts on the model";
}

struct adp* adp0(void) {
    return &app.adp.ifs[0].adp;
}

// The measured accesses of a path against its bound, printed as evidence and checked.
void bound(const char* path, uint64_t accesses, unsigned limit) {
    std::printf("  %-44s %3u accesses (bound %u)\n", path, static_cast<unsigned>(accesses), limit);
    EXPECT_TRUE(accesses <= limit) << path;
}

// One service pass; returns its mailbox accesses.
uint64_t pass(void) {
    uint64_t before = model.reads + model.writes;
    static_cast<void>(ctrl_loop_service(&app.loop));
    return model.reads + model.writes - before;
}

void settle(void) {
    while (ctrl_loop_service(&app.loop) != 0u) {}
}

// Run the model until the instance is in WAITING with TMR_ADVERTISE armed.
void to_waiting(void) {
    for (unsigned k = 0; k < 12000u && adp0()->state != ADP_STATE_WAITING; ++k) {
        mbx_model_advance_ms(&model, 1);
        settle();
    }
}

void adapter_race(void) {
    boot();
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    EXPECT_EQ(adp0()->state, ADP_STATE_WAITING) << "B1 the model reaches WAITING";
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms - 1u);
    mbx_model_gm_change(&model, 0, 0x5150515051505150ull, 0);
    mbx_model_advance_ms(&model, 1);
    settle();
    EXPECT_EQ(app.adp.ifs[0].stale_expiries, 1)
        << "B1 an expiry of the arm a GM_CHANGE replaced is discarded by its tag";
    EXPECT_TRUE(adp0()->state == ADP_STATE_DELAY && app.adp.ifs[0].armed) << "B1 and the replacing TMR_DELAY stands";
}

void latency(void) {
    uint8_t f[ADP_FRAME_BYTES];
    boot();
    mbx_model_set_link(&model, 0, true);
    uint64_t n = pass();
    EXPECT_TRUE(adp0()->state == ADP_STATE_DELAY) << "C0 LINK_UP -> TMR_DELAY armed, one pass";
    bound("C0 LINK_UP -> TMR_DELAY armed", n, ADP_MBX_LAT_LINK);
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
    uint32_t sent = model.tx_sent;
    n = pass();
    EXPECT_TRUE(model.tx_sent == sent + 1u && adp0()->state == ADP_STATE_WAITING)
        << "C1 TMR_DELAY -> ENTITY_AVAILABLE committed and TMR_ADVERTISE armed, one pass";
    bound("C1 TMR_DELAY -> ENTITY_AVAILABLE, TMR_ADVERTISE", n, ADP_MBX_LAT_DELAY);
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    static_cast<void>(mbx_model_rx(&model, f, sizeof f, 0));
    n = pass();
    EXPECT_TRUE(adp0()->state == ADP_STATE_DELAY) << "C2 RCV_ADP_DISCOVER -> TMR_DELAY armed, one pass";
    bound("C2 RCV_ADP_DISCOVER -> TMR_DELAY armed", n, ADP_MBX_LAT_DISCOVER);
    settle();
    to_waiting();
    arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
    n = pass();
    EXPECT_TRUE(adp0()->state == ADP_STATE_DELAY) << "C3 TMR_ADVERTISE -> TMR_DELAY armed, one pass";
    bound("C3 TMR_ADVERTISE -> TMR_DELAY armed", n, ADP_MBX_LAT_ADVERTISE);
    to_waiting();
    mbx_model_gm_change(&model, 0, 0x5150515051505150ull, 0);
    n = pass();
    EXPECT_TRUE(adp0()->state == ADP_STATE_DELAY) << "C4 GM_CHANGE -> TMR_DELAY armed, one pass";
    bound("C4 GM_CHANGE -> TMR_DELAY armed", n, ADP_MBX_LAT_GM);
    mbx_model_set_link(&model, 0, false);
    n = pass();
    EXPECT_TRUE(adp0()->state == ADP_STATE_DOWN && !app.adp.ifs[0].armed)
        << "C5 LINK_DOWN -> timer cancelled, one pass";
    bound("C5 LINK_DOWN -> timer cancelled", n, ADP_MBX_LAT_LINK);
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    sent = model.tx_sent;
    uint64_t before = model.reads + model.writes;
    adp_mbx_set_enable(&app.adp, false);
    n = model.reads + model.writes - before;
    EXPECT_TRUE(model.tx_sent == sent + 1u) << "C6 SHUTDOWN -> ENTITY_DEPARTING committed";
    bound("C6 SHUTDOWN -> ENTITY_DEPARTING committed", n, ADP_MBX_LAT_SHUTDOWN);
}

// ---- a frame owed behind a full transmit ring, and a HAL that sleeps ----------------

struct waiter {
    unsigned waits;  // mbx_hal_wait() calls
    unsigned dead;   // waits no interrupt ended within 30 s
};

struct waiter waiter;

// mbx_hal_wait() as a core that sleeps until the mailbox interrupt: model
// time runs until the line rises, for 30 s at most. A wait that reaches the
// end had no wake source.
void wait_for_irq(void* ctx) {
    auto* w = static_cast<struct waiter*>(ctx);
    w->waits++;
    for (unsigned ms = 0; ms < 30000u && !mbx_model_irq(&model); ++ms) {
        mbx_model_advance_ms(&model, 1);
    }
    w->dead += mbx_model_irq(&model) ? 0u : 1u;
}

void pending_wake(void) {
    boot();
    std::memset(&waiter, 0, sizeof waiter);
    mbx_model_bind(&model, wait_for_irq, &waiter);
    mbx_model_set_link(&model, 0, true);
    for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_EQ(adp0()->state, ADP_STATE_DELAY) << "E0 LINK_UP takes the machine to DELAY";
    mbx_model_tx_pause(&model, true);
    uint8_t filler[ADP_FRAME_BYTES];
    adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0, filler);
    while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {}
    for (unsigned k = 0; k < 8u && adp0()->deferred_sends == 0u; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_TRUE(adp0()->available_owed && adp0()->state == ADP_STATE_DELAY)
        << "E0 TMR_DELAY expires behind a full transmit ring: ENTITY_AVAILABLE is owed";
    EXPECT_TRUE(!mbx_model_irq(&model) && model.tick_ctl == 0u)
        << "E0 and nothing else can wake the core: no RX, no event, TICK off";
    unsigned waits = waiter.waits;
    for (unsigned k = 0; k < 16u; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_EQ(waiter.waits, waits) << "E1 the loop does not sleep while a frame is owed";
    uint32_t sent = model.tx_sent;
    mbx_model_tx_pause(&model, false);
    uint32_t drained = model.tx_sent;
    ctrl_loop_step(&app.loop);
    const struct mbx_model_tx* t = mbx_model_tx_frame(&model, model.tx_sent - 1u);
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    EXPECT_TRUE(drained > sent && model.tx_sent == drained + 1u && t != nullptr &&
                t->bytes[15] == ADP_MSG_ENTITY_AVAILABLE && !adp0()->available_owed)
        << "E2 once the ring drains, the next pass sends the owed ENTITY_AVAILABLE";
    EXPECT_TRUE(t != nullptr && arm->op == MBX_TMR_OP_ARM && arm->deadline_ms == t->now_ms + ADP_ADVERTISE_MS &&
                app.adp.ifs[0].armed && adp0()->state == ADP_STATE_WAITING)
        << "E2 and restarts its timer: TMR_ADVERTISE armed 5 s after the frame left, the machine in WAITING";
    for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_TRUE(waiter.waits > waits && waiter.dead == 0u && adp0()->state == ADP_STATE_DELAY)
        << "E3 then the loop sleeps, and the TMR_ADVERTISE expiry wakes it";
    mbx_model_bind(&model, nullptr, nullptr);
}

// The k-th frame the model sent is `msg` carrying `index`.
bool model_sent(uint32_t k, uint8_t msg, uint32_t index) {
    const struct mbx_model_tx* t = mbx_model_tx_frame(&model, k);
    return t != nullptr && (t->bytes[15] & 0x0Fu) == msg && wire_be32(t->bytes + 50) == index;
}

// R497-2-F1 through the mailbox driver, the model's timer and the loop.
void owed_departing_wake(void) {
    boot();
    std::memset(&waiter, 0, sizeof waiter);
    mbx_model_bind(&model, wait_for_irq, &waiter);
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    EXPECT_TRUE(model.tx_sent >= 1u && model_sent(model.tx_sent - 1u, ADP_MSG_ENTITY_AVAILABLE, 0) &&
                adp0()->state == ADP_STATE_WAITING)
        << "E4 advertised once: the first ENTITY_AVAILABLE left with index 0, the machine in WAITING";
    mbx_model_tx_pause(&model, true);
    uint8_t filler[ADP_FRAME_BYTES];
    adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x0F0F0F0Fu, filler);
    while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {}
    adp_mbx_set_enable(&app.adp, false);
    adp_mbx_set_enable(&app.adp, true);
    EXPECT_TRUE(adp0()->departing_owed == 1u && adp0()->departing_index == 1u && adp0()->state == ADP_STATE_DELAY &&
                app.adp.ifs[0].armed)
        << "E4 SHUTDOWN behind the full ring leaves ENTITY_DEPARTING owed with index 1; the restart arms TMR_DELAY";
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
    unsigned waits = waiter.waits;
    for (unsigned k = 0; k < 16u; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_TRUE(adp0()->available_owed && adp0()->departing_owed == 1u && adp0()->state == ADP_STATE_DELAY &&
                !app.adp.ifs[0].armed)
        << "E4 its TMR_DELAY expires before the ring drains: ENTITY_AVAILABLE owed behind the DEPARTING, no arm";
    EXPECT_EQ(waiter.waits, waits) << "E4 the loop does not sleep while both are owed";
    mbx_model_tx_pause(&model, false);
    uint32_t drained = model.tx_sent;
    ctrl_loop_step(&app.loop);
    ctrl_loop_step(&app.loop);
    const struct mbx_model_tx* t = mbx_model_tx_frame(&model, drained + 1u);
    arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    EXPECT_TRUE(model.tx_sent == drained + 2u && model_sent(drained, ADP_MSG_ENTITY_DEPARTING, 1) &&
                model_sent(drained + 1u, ADP_MSG_ENTITY_AVAILABLE, 0))
        << "E4 once the ring drains: ENTITY_DEPARTING with index 1, then ENTITY_AVAILABLE with index 0";
    EXPECT_TRUE(t != nullptr && arm->op == MBX_TMR_OP_ARM && arm->deadline_ms == t->now_ms + ADP_ADVERTISE_MS &&
                app.adp.ifs[0].armed && adp0()->state == ADP_STATE_WAITING)
        << "E4 then WAITING with TMR_ADVERTISE armed 5 s after the ENTITY_AVAILABLE left";
    for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
        ctrl_loop_step(&app.loop);
    }
    EXPECT_TRUE(!adp0()->available_owed && adp0()->departing_owed == 0u && model.tx_sent == drained + 2u &&
                waiter.waits > waits && waiter.dead == 0u && adp0()->state == ADP_STATE_DELAY)
        << "E4 nothing stranded: no frame owed, the loop sleeps, and the TMR_ADVERTISE expiry wakes it";
    mbx_model_bind(&model, nullptr, nullptr);
}

// R496-3-F1 through the driver, the model's timer and the loop (adp_mbx.h,
// owed frames): `shutdowns` SHUTDOWN-and-restart pairs behind a full ring
// leave k = min(shutdowns, 2) DEPARTINGs owed ahead of the last restart's
// ENTITY_AVAILABLE. Its TMR_DELAY expiry is taken while the ring is still
// full, or once the room has returned (`room_first`). The AVAILABLE must be
// committed in pass k + 1 after the room returns, within the stated figures.
void owed_bound(unsigned shutdowns, bool room_first) {
    char what[192];
    unsigned k = shutdowns < ADP_DEPARTING_OWED_MAX ? shutdowns : ADP_DEPARTING_OWED_MAX;
    const char* when = room_first ? "expiry taken after the room" : "expiry taken before the room";
    boot();
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    mbx_model_tx_pause(&model, true);
    uint8_t filler[ADP_FRAME_BYTES];
    adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x0F0F0F0Fu, filler);
    while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {}
    for (unsigned s = 0; s < shutdowns; ++s) {
        adp_mbx_set_enable(&app.adp, false);
        adp_mbx_set_enable(&app.adp, true);
    }
    std::snprintf(what, sizeof what,
                  "E5 %u SHUTDOWNs behind a full ring, %s: %u DEPARTINGs owed, the oldest index 1, "
                  "%u coalesced",
                  shutdowns, when, k, shutdowns - k);
    EXPECT_TRUE(adp0()->departing_owed == k && adp0()->departing_index == 1u &&
                adp0()->departing_coalesced == shutdowns - k)
        << what;
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
    if (!room_first) {
        for (unsigned p = 0; p < 4u; ++p) {
            static_cast<void>(pass());
        }
        std::snprintf(what, sizeof what,
                      "E5 %u SHUTDOWNs behind a full ring, %s: the ENTITY_AVAILABLE owed behind them", shutdowns, when);
        EXPECT_TRUE(adp0()->available_owed && adp0()->state == ADP_STATE_DELAY && !app.adp.ifs[0].armed) << what;
    }
    mbx_model_tx_pause(&model, false);
    uint32_t base = model.tx_sent;
    uint64_t accesses = 0;
    unsigned at = 0;
    for (unsigned p = 1; p <= 8u && at == 0u; ++p) {
        accesses += pass();
        for (uint32_t j = base; j < model.tx_sent; ++j) {
            at = model_sent(j, ADP_MSG_ENTITY_AVAILABLE, 0) ? p : at;
        }
    }
    std::snprintf(what, sizeof what,
                  "E5 %u SHUTDOWNs behind a full ring, %s: the ENTITY_AVAILABLE is committed in pass "
                  "k + 1 = %u after the room returns, within ADP_MBX_OWED_PASSES",
                  shutdowns, when, k + 1u);
    EXPECT_TRUE(at == k + 1u && at <= ADP_MBX_OWED_PASSES) << what;
    std::snprintf(what, sizeof what, "E5 %u SHUTDOWNs, %s: room to ENTITY_AVAILABLE", shutdowns, when);
    bound(what, at != 0u ? accesses : UINT64_MAX, ADP_MBX_OWED_ACCESSES);
    std::snprintf(what, sizeof what,
                  "E5 %u SHUTDOWNs behind a full ring, %s: the wire carries DEPARTING 1, %sAVAILABLE 0", shutdowns,
                  when, k == 2u ? "DEPARTING 0, " : "");
    EXPECT_TRUE(model.tx_sent == base + k + 1u && model_sent(base, ADP_MSG_ENTITY_DEPARTING, 1) &&
                (k < 2u || model_sent(base + 1u, ADP_MSG_ENTITY_DEPARTING, 0)) &&
                model_sent(base + k, ADP_MSG_ENTITY_AVAILABLE, 0))
        << what;
    std::snprintf(what, sizeof what,
                  "E5 %u SHUTDOWNs behind a full ring, %s: then WAITING, TMR_ADVERTISE armed, "
                  "nothing owed",
                  shutdowns, when);
    EXPECT_TRUE(adp0()->state == ADP_STATE_WAITING && app.adp.ifs[0].armed && !adp0()->available_owed &&
                adp0()->departing_owed == 0u)
        << what;
}

// ---- the bound with full backlogs (ctrl_loop.h A1 to A4, adp_mbx.h) -----------------

unsigned ticks_seen;

void count_tick(void) {
    ticks_seen++;
}

bool rx_touched;        // this pass has touched the ADP receive ring
unsigned out_of_order;  // event-ring accesses after a receive-ring access in one pass

void trace_order(void* ctx, bool write, uint32_t off, uint32_t value) {
    static_cast<void>(ctx);
    static_cast<void>(write);
    static_cast<void>(value);
    bool rx = off == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_ADP + MBX_CH_REG_RX_HEAD ||
              off == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_ADP + MBX_CH_REG_RX_TAIL ||
              (off >= MBX_CH_ADP_RX_BASE && off < MBX_CH_ADP_RX_BASE + 4u * MBX_CH_ADP_RX_WORDS);
    bool evt = off == MBX_REG_EVT_HEAD || off == MBX_REG_EVT_TAIL ||
               (off >= MBX_EVT_BASE && off < MBX_EVT_BASE + 4u * MBX_EVT_WORDS);
    rx_touched = rx_touched || rx;
    out_of_order += evt && rx_touched ? 1u : 0u;
}

// The backlog F0 to F7 grade, posted while the loop does not run.
struct Backlog {
    unsigned stored;     // receive records
    uint32_t ticks_due;  // centiseconds coalesced behind the full event ring
    uint32_t events0;
    uint32_t rx0;
    uint32_t sent0;
};

// What the passes that take the backlog measured.
struct Passes {
    unsigned evt_at;
    unsigned answer_at;
    unsigned rx_at;
    unsigned idle_at;
    unsigned most_ticks;
    uint64_t worst;
    uint64_t answer_accesses;
    uint64_t rx_accesses;
};

// Events: an expiry on each of the 15 slots ADP does not own, then ADP's own
// TMR_DELAY expiry (the costliest sink path) as the 16th record, which fills
// the ring; then, once the receive ring is full too, 30 centiseconds the
// fabric coalesces behind them. The tick is held off until then, so the 16
// records are exactly these.
Backlog backlog_post(void) {
    const uint64_t own_mac[MBX_N_IF] = {entity.mac};
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    ctrl_loop_init(&app.loop);
    EXPECT_TRUE(adp_mbx_init(&app.adp, &entity, CTRL_APP_ADP_FIRST_SLOT, 2) && adp_mbx_attach(&app.adp, &app.loop) &&
                ctrl_loop_add_tick(&app.loop, count_tick) && ctrl_loop_open(&app.loop, entity.entity_id, own_mac))
        << "F0 the F0 composition with a centisecond consumer comes up";
    adp_mbx_set_enable(&app.adp, true);
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    uint8_t f[ADP_FRAME_BYTES];
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    static_cast<void>(mbx_model_rx(&model, f, sizeof f, 0));
    settle();
    const struct mbx_model_tmr_op* arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
    uint32_t deadline = arm->deadline_ms;
    mbx_tick_enable(false);
    for (unsigned slot = 1; slot < MBX_N_TIMERS; ++slot) {
        mbx_timer_arm(slot, 0x77u, mbx_now_ms());
    }
    mbx_model_advance_ms(&model, 0);
    mbx_model_advance_ms(&model, deadline - model.now_ms);
    uint32_t last =
        model.window[(MBX_EVT_BASE + 4u * (static_cast<uint32_t>(model.evt_head - 3u) & (MBX_EVT_WORDS - 1u))) / 4u];
    EXPECT_TRUE(static_cast<uint16_t>(model.evt_head - model.evt_tail) == MBX_EVT_WORDS &&
                mbx_field(last, MBX_EV_TIMER_W1_SLOT_LSB, MBX_EV_TIMER_W1_SLOT_WIDTH) == CTRL_APP_ADP_FIRST_SLOT)
        << "F0 the event ring is full, ADP's TMR_DELAY expiry its 16th record";
    // Receive: the smallest ENTITY_DISCOVER the filter passes (26 bytes,
    // through entity_id) until the ring refuses one, at the rate the
    // channel's token bucket admits.
    Backlog b{};
    for (unsigned k = 0; k < 100000u && model.ch[MBX_CH_ADP].rx_drop == 0u; ++k) {
        if (mbx_model_rx(&model, f, 26u, 0)) {
            b.stored++;
        } else if (model.ch[MBX_CH_ADP].rx_drop == 0u) {
            mbx_model_advance_ms(&model, 1);
        }
    }
    EXPECT_TRUE(model.ch[MBX_CH_ADP].rx_drop == 1u) << "F0 the receive ring is full: it refuses the next frame";
    mbx_tick_enable(true);
    mbx_model_advance_ms(&model, 30u * MBX_TICK_MS);
    b.ticks_due = model.tick_count;
    EXPECT_EQ(b.ticks_due, 30u) << "F0 30 centiseconds wait coalesced behind the full event ring";
    EXPECT_TRUE(b.stored > 0u && b.stored <= CTRL_LOOP_RX_BACKLOG(MBX_CH_ADP_RX_WORDS))
        << "F0 and holds no more records than A1 assumes";
    std::printf("  backlog: 16 event records, %u centiseconds, %u receive records\n",
                static_cast<unsigned>(b.ticks_due), b.stored);
    b.events0 = app.loop.stats.events;
    b.rx0 = app.loop.stats.rx_records;
    b.sent0 = model.tx_sent;
    return b;
}

// The passes until the loop may sleep, each measured.
Passes backlog_take(const Backlog& b) {
    Passes s{};
    uint64_t total = 0;
    ticks_seen = 0;
    out_of_order = 0;
    mbx_host_trace(trace_order, nullptr);
    for (unsigned p = 1; p <= 64u && s.idle_at == 0u; ++p) {
        rx_touched = false;
        unsigned t0 = ticks_seen;
        uint64_t before = model.reads + model.writes;
        unsigned work = ctrl_loop_service(&app.loop);
        uint64_t n = model.reads + model.writes - before;
        total += n;
        s.worst = n > s.worst ? n : s.worst;
        s.most_ticks = ticks_seen - t0 > s.most_ticks ? ticks_seen - t0 : s.most_ticks;
        if (s.evt_at == 0u && app.loop.stats.events - b.events0 >= 16u) {
            s.evt_at = p;
        }
        if (s.answer_at == 0u && model.tx_sent > b.sent0) {
            s.answer_at = p;
            s.answer_accesses = total;
        }
        if (s.rx_at == 0u && app.loop.stats.rx_records - b.rx0 >= b.stored) {
            s.rx_at = p;
            s.rx_accesses = total;
        }
        if (work == 0u) {
            s.idle_at = p;
        }
    }
    mbx_host_trace(nullptr, nullptr);
    std::printf(
        "  passes: events by %u, ENTITY_AVAILABLE in %u (%u accesses), receive ring by %u (%u accesses), "
        "idle at %u; worst pass %u accesses\n",
        s.evt_at, s.answer_at, static_cast<unsigned>(s.answer_accesses), s.rx_at, static_cast<unsigned>(s.rx_accesses),
        s.idle_at, static_cast<unsigned>(s.worst));
    return s;
}

void backlog_grade(const Backlog& b, const Passes& s) {
    EXPECT_EQ(out_of_order, 0u) << "F1 events first: no event-ring access follows a receive-ring access in a pass";
    EXPECT_TRUE(s.evt_at != 0u && s.evt_at <= CTRL_LOOP_EVT_PASSES)
        << "F2 all 16 event records are taken by pass CTRL_LOOP_EVT_PASSES";
    EXPECT_TRUE(s.answer_at != 0u && s.answer_at <= CTRL_LOOP_EVT_PASSES && s.answer_at == s.evt_at)
        << "F2 the TMR_DELAY expiry, posted 16th, has its ENTITY_AVAILABLE committed in the pass that takes it";
    EXPECT_TRUE(s.answer_at != 0u && s.answer_accesses <= ADP_MBX_EVT_ACCESSES)
        << "F2 within ADP_MBX_EVT_ACCESSES of the backlog's first access";
    EXPECT_TRUE(s.rx_at == (b.stored + CTRL_LOOP_RX_PER_PASS - 1u) / CTRL_LOOP_RX_PER_PASS)
        << "F3 the receive backlog is taken by pass ceil(records / CTRL_LOOP_RX_PER_PASS)";
    EXPECT_TRUE(s.rx_at != 0u && s.rx_at <= CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) &&
                s.rx_accesses <= ADP_MBX_RX_ACCESSES)
        << "F3 within CTRL_LOOP_RX_PASSES(256) passes and ADP_MBX_RX_ACCESSES accesses";
    EXPECT_EQ(ticks_seen, b.ticks_due) << "F4 every coalesced centisecond reaches the consumer";
    EXPECT_TRUE(s.most_ticks <= CTRL_LOOP_TICKS_PER_PASS) << "F4 at most CTRL_LOOP_TICKS_PER_PASS of them in a pass";
    bound("F5 the costliest pass of the backlog", s.worst, ADP_MBX_PASS_MAX);
    EXPECT_TRUE(s.idle_at != 0u && s.idle_at > s.rx_at && s.idle_at > s.evt_at && app.loop.ticks_owed == 0u)
        << "F6 the loop passes until the backlog is gone, then may sleep";
    EXPECT_EQ(model.tx_sent, b.sent0 + 1u) << "F7 the backlog left exactly one frame, the ENTITY_AVAILABLE";
}

// ---- the tests -----------------------------------------------------------------------

TEST(AdpAdapter, B1StaleTagDiscarded) {
    adapter_race();
}
TEST(AdpLatency, C0toC6EveryResponsePath) {
    latency();
}
TEST(AdpOwed, E0toE3PendingWake) {
    pending_wake();
}
TEST(AdpOwed, E4OwedDepartingWake) {
    owed_departing_wake();
}

// E5: 1, 2 and 64 SHUTDOWNs, the expiry taken before and after the room returns.
class AdpOwedBound : public ::testing::TestWithParam<std::tuple<unsigned, bool>> {};

TEST_P(AdpOwedBound, E5CommittedInPassKPlusOne) {
    owed_bound(std::get<0>(GetParam()), std::get<1>(GetParam()));
}

INSTANTIATE_TEST_SUITE_P(Shutdowns, AdpOwedBound,
                         ::testing::Combine(::testing::Values(1u, 2u, 64u), ::testing::Bool()));

TEST(AdpBacklog, F0toF7FullBacklogs) {
    const Backlog b = backlog_post();
    const Passes s = backlog_take(b);
    backlog_grade(b, s);
}

}  // namespace
