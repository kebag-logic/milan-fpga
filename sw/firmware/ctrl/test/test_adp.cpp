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
//       the stated figures, events first in every pass;
//   G   the first ENTITY_AVAILABLE after a link-up (#970), with Milan's draws:
//       within its draw, 0 to 4 s on LINK_UP and 0 to 2 s at a startup with
//       the link up, so within the declared 6.0 s discovery time
//       (docs/reference/FR_NFR.md), each draw spread over its whole range
//       (uniform, IEEE 1722.1-2021 6.2.4.2.2); a grandmaster change before it
//       re-arms nothing and is carried by it, one after it is announced by a
//       new ENTITY_AVAILABLE after its own 0 to 4 s draw; available_index
//       advancing by one per ENTITY_AVAILABLE across the link-ups; every later
//       delay 0 to 4 s (Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.5, 5.6.3.5.7,
//       5.6.3.5.9 and Table 5.51; IEEE 1722.1-2021 6.2.2.15 and 6.2.2.16);
//   H   THE DRAW (adp_mbx.h): the first delays of neighbouring entity IDs
//       started together, and of one entity's boots, each uniform over its
//       range at a startup and at a LINK_UP (IEEE 1722.1-2021 6.2.4.2.2); the
//       seed's terms; the seed without a clock.
//
// One test per labelled step or scenario; each assertion carries the check's
// name from the hand-rolled suite it replaces (sw/firmware/gtest/README.md,
// "The port").

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <set>
#include <tuple>
#include <vector>

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
    wire_put_be(f + 16, 56u, 2);
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
    unsigned tick_passes;  // the passes up to rx_at that dispatched a centisecond (THE TICK's cap, ctrl_loop.h)
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
        s.tick_passes += s.rx_at == 0u && ticks_seen > t0 ? 1u : 0u;
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
    // a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records (THE TICK's cap, ctrl_loop.h)
    const unsigned lost = s.tick_passes * (CTRL_LOOP_RX_PER_PASS - CTRL_LOOP_RX_PER_TICK_PASS);
    EXPECT_TRUE(s.rx_at == (b.stored + lost + CTRL_LOOP_RX_PER_PASS - 1u) / CTRL_LOOP_RX_PER_PASS)
        << "F3 the receive backlog is taken by pass ceil(records / CTRL_LOOP_RX_PER_PASS), one record later for each "
           "pass among them that dispatches a centisecond";
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

// ---- G: the first ENTITY_AVAILABLE after a link-up (#970) ----------------------------
//
// The entity's declared discovery time is 6.0 s (docs/reference/FR_NFR.md, its derivation): a controller waits that
// long for the first ENTITY_AVAILABLE after a link-up. This group holds the part of it ADP owns, with Milan's draws
// stated here as literals, independently of the core's names: the first ENTITY_AVAILABLE within its draw of the
// LINK event's posting, and each draw spread over its whole range.

constexpr uint32_t kDiscoveryMs = 6000u;        // the declared discovery time (FR_NFR)
constexpr uint32_t kLinkUpDrawMaxMs = 4000u;    // Milan v1.2 5.6.3.5.3, Table 5.50
constexpr uint32_t kStartupDrawMaxMs = 2000u;   // Milan v1.2 5.6.3.5.2
constexpr uint32_t kDelayMaxMs = 4000u;         // Milan v1.2 Table 5.50: DISCOVER, TMR_ADVERTISE, GM_CHANGE
constexpr uint32_t kAdvertiseMs = 5000u;        // Milan v1.2 Table 5.50
constexpr uint32_t kPassMs = 2u;                // the passes that take the LINK event and the expiry, on the model
constexpr uint64_t kGmA = 0x00AABBFFFE000001ull;
constexpr uint64_t kGmB = 0x00CCDDFFFE000002ull;

// One ENTITY_AVAILABLE interface 0 sent: when, its available_index and its gptp_grandmaster_id.
struct Available {
    uint32_t ms;
    uint32_t index;
    uint64_t gm;
};

// The ENTITY_AVAILABLEs the model sent since the last call, read before its capture wraps.
struct Wire {
    uint32_t seen = 0;
    std::vector<Available> available;

    void take() {
        for (; seen < model.tx_sent; ++seen) {
            const struct mbx_model_tx* f = mbx_model_tx_frame(&model, seen);
            if (f != nullptr && f->channel == MBX_CH_ADP && f->interface == 0u && f->len >= ADP_FRAME_BYTES &&
                (f->bytes[15] & 0x0Fu) == ADP_MSG_ENTITY_AVAILABLE) {
                available.push_back(Available{f->now_ms, wire_be32(f->bytes + 50), wire_be64(f->bytes + 54)});
            }
        }
    }
};

// Run the model one millisecond at a time, the loop serviced after each, for `ms`.
void run_ms(Wire& w, uint32_t ms) {
    for (uint32_t k = 0; k < ms; ++k) {
        mbx_model_advance_ms(&model, 1);
        settle();
        w.take();
    }
}

// Run until `n` ENTITY_AVAILABLEs have been seen or `limit` ms pass; true when they were.
bool run_until(Wire& w, size_t n, uint32_t limit) {
    for (uint32_t k = 0; k < limit && w.available.size() < n; ++k) {
        run_ms(w, 1);
    }
    return w.available.size() >= n;
}

// The deadline of the ADP slot's latest arm since timer operation `from`, 0 when there is none.
uint32_t last_arm(uint32_t from) {
    uint32_t deadline = 0;
    for (uint32_t k = from; k < model.tmr_ops; ++k) {
        const struct mbx_model_tmr_op* op = mbx_model_tmr_op(&model, k);
        if (op != nullptr && op->op == MBX_TMR_OP_ARM && op->slot == CTRL_APP_ADP_FIRST_SLOT) {
            deadline = op->deadline_ms;
        }
    }
    return deadline;
}

// The app on a fresh model, the link down, the grandmaster kGmA, the clock moved on by `skew` ms so the seed the
// machine mixes in at its start differs from run to run.
void boot_down(Wire& w, uint32_t skew) {
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    mbx_model_advance_ms(&model, skew);
    mbx_model_set_gm(&model, 0, kGmA, 0);
    struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr, nullptr,
                                   nullptr, nullptr, 0};
    EXPECT_TRUE(ctrl_app_start(&app, &cfg)) << "G0 the app starts on the model";
    settle();
    w = Wire{};
    w.seen = model.tx_sent;
}

// The delays seen, their latest and how many fall in each of `bins` equal parts of 0 to `max` ms.
struct Spread {
    uint32_t worst = 0;
    std::set<uint32_t> values;
    std::vector<uint32_t> all;
    void add(uint32_t v) {
        worst = v > worst ? v : worst;
        values.insert(v);
        all.push_back(v);
    }
    // How many fall in each of `bins` equal parts of 0 to `max` ms (a delay past `max` in the last).
    std::vector<unsigned> bins(uint32_t max, unsigned n) const {
        std::vector<unsigned> in(n, 0u);
        for (const uint32_t v : all) {
            const uint32_t b = v * n / (max + 1u);
            ++in[b < n ? b : n - 1u];
        }
        return in;
    }
    // True when each of `n` equal parts of the range holds at least `least` of the delays.
    bool covers(uint32_t max, unsigned n, unsigned least) const {
        bool ok = true;
        for (const unsigned in : bins(max, n)) ok = ok && in >= least;
        return ok;
    }
    void print_bins(const char* what, uint32_t max, unsigned n) const {
        std::printf("  %s, by %u parts of 0 to %u ms:", what, n, static_cast<unsigned>(max));
        for (const unsigned in : bins(max, n)) std::printf(" %u", in);
        std::printf("\n");
    }
};

// G1 64 link-ups, each LINK_UP to its first ENTITY_AVAILABLE, then that ENTITY_AVAILABLE's TMR_ADVERTISE to the
// next one, then the link down. G5 reads the later delays from the same run.
void first_after_link_up(Spread& first, Spread& later) {
    Wire w;
    boot_down(w, 3u);
    bool within = true;
    bool indexed = true;
    bool later_within = true;
    uint32_t expect_index = 0;
    for (unsigned k = 0; k < 64u; ++k) {
        mbx_model_set_link(&model, 0, true);
        const uint32_t up = model.now_ms;
        const size_t before = w.available.size();
        settle();
        w.take();
        within = run_until(w, before + 1u, kDiscoveryMs) && within;
        if (w.available.size() <= before) {
            break;
        }
        const Available a = w.available[before];
        within = within && a.ms - up <= kLinkUpDrawMaxMs + kPassMs;
        first.add(a.ms - up);
        indexed = indexed && a.index == expect_index;
        later_within = run_until(w, before + 2u, kAdvertiseMs + kDelayMaxMs + 2u) && later_within;
        if (w.available.size() > before + 1u) {
            const Available b = w.available[before + 1u];
            later_within = later_within && b.ms - a.ms >= kAdvertiseMs && b.ms - a.ms <= kAdvertiseMs + kDelayMaxMs;
            later.add(b.ms - a.ms - kAdvertiseMs);
            indexed = indexed && b.index == expect_index + 1u;
        }
        expect_index += 2u;
        mbx_model_set_link(&model, 0, false);
        run_ms(w, 10u);
    }
    std::printf("  G1 64 LINK_UPs: the first ENTITY_AVAILABLE %u distinct delays, the latest %u ms after LINK_UP "
                "(its draw 0 to %u ms; the declared discovery time %u ms)\n", static_cast<unsigned>(first.values.size()),
                static_cast<unsigned>(first.worst), static_cast<unsigned>(kLinkUpDrawMaxMs),
                static_cast<unsigned>(kDiscoveryMs));
    std::printf("  G5 the TMR_ADVERTISE delays after them: %u distinct, the latest %u ms (0 to %u)\n",
                static_cast<unsigned>(later.values.size()), static_cast<unsigned>(later.worst),
                static_cast<unsigned>(kDelayMaxMs));
    first.print_bins("G1 the LINK_UP delays", kLinkUpDrawMaxMs, 4u);
    later.print_bins("G5 the TMR_ADVERTISE delays", kDelayMaxMs, 4u);
    EXPECT_TRUE(within) << "G1 the first ENTITY_AVAILABLE leaves within its 0 to 4 s draw of every LINK_UP, inside "
                           "the declared discovery time";
    EXPECT_TRUE(first.covers(kLinkUpDrawMaxMs, 4u, 8u))
        << "G1 the LINK_UP delay is spread over 0 to 4 s: each quarter holds at least 8 of the 64";
    EXPECT_TRUE(indexed)
        << "G1 each ENTITY_AVAILABLE carries the next available_index, across every link-up (6.2.2.15)";
    EXPECT_TRUE(later_within) << "G5 each TMR_ADVERTISE delay is drawn from 0 to 4 s (5.6.3.5.5, Table 5.50)";
    EXPECT_TRUE(later.covers(kDelayMaxMs, 4u, 8u))
        << "G5 the TMR_ADVERTISE delay is spread over 0 to 4 s: each quarter holds at least 8 of the 64";
}

// G2 32 startups with the link up, each from reset as another entity (the generator's seed is its entity ID and the
// clock, IEEE 1722.1-2021 6.2.4.2.2), to the first ENTITY_AVAILABLE.
void first_after_startup(void) {
    bool within = true;
    Spread first;
    for (unsigned k = 0; k < 32u; ++k) {
        Wire w;
        struct adp_entity other = entity;
        other.entity_id = entity.entity_id ^ (0x9E3779B97F4A7C15ull * (k + 1u));
        mbx_model_reset(&model);
        mbx_model_bind(&model, nullptr, nullptr);
        mbx_model_advance_ms(&model, 7u * k + 1u);
        mbx_model_set_gm(&model, 0, kGmA, 0);
        mbx_model_set_link(&model, 0, true);
        struct ctrl_app_config cfg = {&other, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr,
                                       nullptr, nullptr, nullptr, 0};
        const uint32_t start = model.now_ms;
        EXPECT_TRUE(ctrl_app_start(&app, &cfg)) << "G0 the app starts on the model";
        settle();
        w.take();
        within = run_until(w, 1u, kDiscoveryMs) && within;
        if (!w.available.empty()) {
            within = within && w.available[0].ms - start <= kStartupDrawMaxMs + kPassMs && w.available[0].index == 0u;
            first.add(w.available[0].ms - start);
        }
    }
    std::printf("  G2 32 startups with the link up: the first ENTITY_AVAILABLE %u distinct delays, the latest %u ms "
                "(its draw 0 to %u ms)\n", static_cast<unsigned>(first.values.size()),
                static_cast<unsigned>(first.worst), static_cast<unsigned>(kStartupDrawMaxMs));
    first.print_bins("G2 the startup delays", kStartupDrawMaxMs, 2u);
    EXPECT_TRUE(within) << "G2 the first ENTITY_AVAILABLE, index 0, leaves within its 0 to 2 s draw of a startup "
                           "with the link up (5.6.3.5.2)";
    EXPECT_TRUE(first.covers(kStartupDrawMaxMs, 2u, 8u))
        << "G2 the startup delay is spread over 0 to 2 s: each half holds at least 8 of the 32";
}

// G3 a grandmaster change while the link-up's delay runs, at each of 32 link-ups: it re-arms nothing, so the first
// ENTITY_AVAILABLE leaves at the LINK_UP's own deadline, and carries the new grandmaster (Table 5.51: GM_CHANGE in
// DELAY is ignored; the frame samples the grandmaster when it is built, 6.2.2.16).
void gm_change_before_first(void) {
    Wire w;
    Spread first;
    boot_down(w, 5u);
    bool own_deadline = true;
    bool carried = true;
    unsigned changed = 0;
    for (unsigned k = 0; k < 32u; ++k) {
        mbx_model_set_gm(&model, 0, kGmA, 0);
        mbx_model_set_link(&model, 0, true);
        const uint32_t up = model.now_ms;
        const uint32_t ops = model.tmr_ops;
        const size_t before = w.available.size();
        settle();
        w.take();
        const uint32_t deadline = last_arm(ops);
        if (w.available.size() == before && adp0()->state == ADP_STATE_DELAY && deadline > model.now_ms) {
            mbx_model_gm_change(&model, 0, kGmB, 0);
            settle();
            w.take();
            changed++;
            own_deadline = run_until(w, before + 1u, kDiscoveryMs) && own_deadline;
            if (w.available.size() > before) {
                own_deadline = own_deadline && w.available[before].ms <= deadline + kPassMs;
                first.add(w.available[before].ms - up);
                carried = carried && w.available[before].gm == kGmB;
            }
        }
        mbx_model_set_link(&model, 0, false);
        run_ms(w, 10u);
    }
    std::printf("  G3 %u LINK_UPs with a grandmaster change in the delay: the first ENTITY_AVAILABLE the latest %u ms "
                "after LINK_UP\n", changed, static_cast<unsigned>(first.worst));
    EXPECT_TRUE(changed >= 24u) << "G3 the grandmaster changed inside the link-up's delay in at least 24 of 32";
    EXPECT_TRUE(own_deadline) << "G3 a grandmaster change before the first ENTITY_AVAILABLE re-arms nothing: it "
                                 "leaves at the LINK_UP's own deadline";
    EXPECT_TRUE(carried) << "G3 and that ENTITY_AVAILABLE carries the new gptp_grandmaster_id";
}

// G4 the bench's order, at each of 32 link-ups: the first ENTITY_AVAILABLE, then a grandmaster change 4.5 s after
// the link-up, in WAITING: a delay at once, then a new ENTITY_AVAILABLE with the new grandmaster and the next index
// within its 0 to 4 s draw (5.6.3.5.7), the draws across the link-ups passing 2 s.
void gm_change_after_first(void) {
    Wire w;
    Spread first;
    Spread change_to_new;
    boot_down(w, 11u);
    bool within = true;
    bool announced = true;
    for (unsigned k = 0; k < 32u; ++k) {
        mbx_model_set_gm(&model, 0, kGmA, 0);
        mbx_model_set_link(&model, 0, true);
        const uint32_t up = model.now_ms;
        const size_t before = w.available.size();
        settle();
        w.take();
        within = run_until(w, before + 1u, kDiscoveryMs) && within;
        if (w.available.size() <= before) {
            break;
        }
        const Available a = w.available[before];
        within = within && a.ms - up <= kLinkUpDrawMaxMs + kPassMs && a.gm == kGmA;
        first.add(a.ms - up);
        run_ms(w, 4500u - (model.now_ms - up));
        const uint32_t change = model.now_ms;
        mbx_model_gm_change(&model, 0, kGmB, 0);
        settle();
        w.take();
        announced = announced && adp0()->state == ADP_STATE_DELAY && w.available.size() == before + 1u;
        announced = run_until(w, before + 2u, kDelayMaxMs + kPassMs) && announced;
        if (w.available.size() > before + 1u) {
            const Available b = w.available[before + 1u];
            announced = announced && b.gm == kGmB && b.index == a.index + 1u && b.ms - change <= kDelayMaxMs + kPassMs;
            change_to_new.add(b.ms - change);
        }
        mbx_model_set_link(&model, 0, false);
        run_ms(w, 10u);
    }
    std::printf("  G4 32 LINK_UPs, a grandmaster change 4.5 s after each: the first ENTITY_AVAILABLE the latest %u ms "
                "after LINK_UP, the new grandmaster's the latest %u ms after the change\n",
                static_cast<unsigned>(first.worst), static_cast<unsigned>(change_to_new.worst));
    change_to_new.print_bins("G4 the grandmaster change's delays", kDelayMaxMs, 2u);
    EXPECT_TRUE(within) << "G4 the first ENTITY_AVAILABLE leaves within its 0 to 4 s draw, a grandmaster change to "
                           "come";
    EXPECT_TRUE(announced) << "G4 a grandmaster change after the first ENTITY_AVAILABLE starts a delay at once and "
                              "is announced by a new one, its next index";
    EXPECT_TRUE(change_to_new.all.size() == 32u && change_to_new.worst > kStartupDrawMaxMs + kPassMs)
        << "G4 the grandmaster change's delay is the 0 to 4 s draw: across the link-ups it passes 2 s";
}

// ---- H: THE DRAW (#970; IEEE 1722.1-2021 6.2.4.2.2) ----------------------------------

// The seed's clock in these tests: the value in *ctx, as the platform's microseconds would give it.
unsigned clock_reads = 0;
uint32_t fixed_clock(void* ctx) {
    ++clock_reads;
    return *static_cast<uint32_t*>(ctx);
}

// A LINK event of interface 0 at `up`, handed to every sink of the loop as the loop hands one it takes: the model
// posts one only on a change, so a duplicate comes this way.
void link_event(bool up) {
    struct mbx_event ev{};
    ev.type = MBX_EV_TYPE_LINK;
    ev.interface = 0;
    ev.link_up = up;
    for (unsigned k = 0; k < app.loop.n_sinks; ++k) {
        app.loop.sinks[k].fn(app.loop.sinks[k].ctx, &ev);
    }
}

// The clock port is the composition's, not the app's: each test leaves none behind.
struct AdpDraw : ::testing::Test {
    uint32_t sample = 0;
    void SetUp() override { adp_mbx_set_clock(fixed_clock, &sample); }
    void TearDown() override { adp_mbx_set_clock(nullptr, nullptr); }
};

// The app on a fresh model as `e`, its link up before its start or at a LINK_UP after it: its first delay is drawn.
void draw_first(const struct adp_entity& e, bool startup, uint32_t skew = 0) {
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    mbx_model_advance_ms(&model, skew);
    mbx_model_set_gm(&model, 0, kGmA, 0);
    mbx_model_set_link(&model, 0, startup);
    struct ctrl_app_config cfg = {&e, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr, nullptr,
                                   nullptr, nullptr, 0};
    ASSERT_TRUE(ctrl_app_start(&app, &cfg)) << "H0 the app starts on the model";
    if (!startup) {
        mbx_model_set_link(&model, 0, true);
    }
    settle();
    ASSERT_TRUE(adp0()->draws == 1u && adp0()->last_draw == (startup ? ADP_DRAW_STARTUP : ADP_DRAW_DELAY))
        << "H0 one delay is drawn, of its kind";
}

struct adp_entity neighbour(uint32_t k, bool own_mac) {
    struct adp_entity e = entity;
    e.mac = own_mac ? 0x024b4c4b4000ull + k : entity.mac;
    e.entity_id = 0x024b4cfffe4b4000ull + k;
    return e;
}

constexpr uint32_t kHosts = 1024u;
constexpr double kChiSquare99 = 30.58;          // 15 degrees of freedom, 99 %

// Pearson's statistic of the delays over sixteen equal parts of the range.
double chi_square(const Spread& d, uint32_t max_ms) {
    const double expected = static_cast<double>(d.all.size()) / 16.0;
    double sum = 0;
    for (const unsigned n : d.bins(max_ms, 16u)) {
        sum += (n - expected) * (n - expected) / expected;
    }
    return sum;
}

double uniform(const char* what, const Spread& d, uint32_t max_ms) {
    const double x = chi_square(d, max_ms);
    std::printf("  %s: %u draws over 0 to %u ms, chi-square %.1f (99 %%: %.1f)\n", what,
                static_cast<unsigned>(d.all.size()), static_cast<unsigned>(max_ms), x, kChiSquare99);
    return x;
}

// ---- the tests -----------------------------------------------------------------------

// H4 neighbouring entity IDs started together, at one sample, with neighbouring MAC addresses and with one: each kind's
// first delays are uniform.
TEST_F(AdpDraw, H4NeighbouringEntitiesDrawUniformly) {
    for (const bool startup : {true, false}) {
        const uint32_t max_ms = startup ? kStartupDrawMaxMs : kLinkUpDrawMaxMs;
        for (const bool own_mac : {true, false}) {
            sample = own_mac ? 0u : 41000u;
            Spread d;
            for (uint32_t k = 0; k < kHosts; ++k) {
                ASSERT_NO_FATAL_FAILURE(draw_first(neighbour(k, own_mac), startup));
                d.add(adp0()->last_draw_ms);
            }
            EXPECT_TRUE(uniform(startup ? "H4 neighbours, startup" : "H4 neighbours, LINK_UP", d, max_ms) <= kChiSquare99)
                << "H4 neighbouring entities started together draw their first delay uniformly";
        }
    }
}

// H5 one entity's boots, their samples one microsecond apart and one millisecond apart.
TEST_F(AdpDraw, H5BootsDrawUniformly) {
    for (const bool startup : {true, false}) {
        const uint32_t max_ms = startup ? kStartupDrawMaxMs : kLinkUpDrawMaxMs;
        for (const uint32_t step : {1u, 1000u}) {
            Spread d;
            for (uint32_t k = 0; k < kHosts; ++k) {
                sample = 41000u + k * step;
                ASSERT_NO_FATAL_FAILURE(draw_first(entity, startup));
                d.add(adp0()->last_draw_ms);
            }
            EXPECT_TRUE(uniform(startup ? "H5 boots, startup" : "H5 boots, LINK_UP", d, max_ms) <= kChiSquare99)
                << "H5 one entity's boots draw their first delay uniformly";
        }
    }
}

// H6 without a clock the sample is NOW_MS: boots one millisecond apart still draw uniformly.
TEST_F(AdpDraw, H6WithoutAClockBootsDrawUniformly) {
    adp_mbx_set_clock(nullptr, nullptr);
    for (const bool startup : {true, false}) {
        Spread d;
        for (uint32_t k = 0; k < kHosts; ++k) {
            ASSERT_NO_FATAL_FAILURE(draw_first(entity, startup, 30u + k));
            d.add(adp0()->last_draw_ms);
        }
        EXPECT_TRUE(uniform(startup ? "H6 no clock, startup" : "H6 no clock, LINK_UP", d,
                            startup ? kStartupDrawMaxMs : kLinkUpDrawMaxMs) <= kChiSquare99)
            << "H6 without a clock the seed's NOW_MS still spreads one entity's boots";
    }
}

// H7 the seed's terms: the sum of MAC address and clock with an end-around carry (6.2.4.2.2), and the entity ID.
TEST_F(AdpDraw, H7TheSeedIsTheSumOfMacAndClockMixedWithTheEntityId) {
    const auto seeded = [this](const struct adp_entity& e, uint32_t at) {
        sample = at;
        draw_first(e, true);
        return adp0()->rng;
    };
    const uint32_t base = seeded(entity, 41000u);
    struct adp_entity e = entity;
    e.mac += 1u;
    EXPECT_NE(seeded(e, 41000u), base) << "H7 the MAC address is in the seed";
    EXPECT_EQ(seeded(e, 40999u), base) << "H7 the seed is the sum of MAC address and clock";
    e.mac = 0xFFFFFFFFull;
    const uint32_t wrapped = seeded(e, 5u);
    e.mac = 0;
    EXPECT_EQ(seeded(e, 5u), wrapped) << "H7 the sum carries end around";
}

// H8 a LINK_UP after a link loss takes a fresh sample: over samples one microsecond apart its delay is uniform too.
TEST_F(AdpDraw, H8ALaterLinkUpTakesAFreshSample) {
    Spread d;
    for (uint32_t k = 0; k < kHosts; ++k) {
        sample = 41000u;
        ASSERT_NO_FATAL_FAILURE(draw_first(entity, false));
        mbx_model_set_link(&model, 0, false);
        settle();
        sample = 90000u + k;
        mbx_model_set_link(&model, 0, true);
        settle();
        ASSERT_EQ(adp0()->draws, 2u) << "H8 the second LINK_UP draws";
        d.add(adp0()->last_draw_ms);
    }
    EXPECT_TRUE(uniform("H8 a later LINK_UP", d, kLinkUpDrawMaxMs) <= kChiSquare99)
        << "H8 a LINK_UP after a link loss draws from a fresh sample";
}

// H9 through the adapter, the clock is read once for each qualified rise and for the startup draw, and never for a
// duplicate LINK_UP or a LINK_UP while disabled (IEEE 1722.1-2021 6.2.4.2.2; Milan v1.2 5.6.3.5.2, 5.6.3.5.3).
TEST_F(AdpDraw, H9EachQualifiedRiseReadsTheClockOnce) {
    sample = 41000u;
    clock_reads = 0;
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    mbx_model_set_gm(&model, 0, kGmA, 0);
    struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr, nullptr,
                                   nullptr, nullptr, 0};
    ASSERT_TRUE(ctrl_app_start(&app, &cfg)) << "H9 the app starts on the model";
    settle();
    EXPECT_EQ(clock_reads, 0u) << "H9 a start with the link down reads no clock";
    for (unsigned rise = 1; rise <= 3u; ++rise) {
        const uint32_t draws = adp0()->draws;
        mbx_model_set_link(&model, 0, true);
        settle();
        EXPECT_TRUE(clock_reads == rise && adp0()->draws == draws + 1u)
            << "H9 each qualified LINK_UP reads the clock once through the adapter";
        link_event(true);
        EXPECT_TRUE(clock_reads == rise && adp0()->draws == draws + 1u) << "H9 a duplicate LINK_UP reads no clock";
        mbx_model_set_link(&model, 0, false);
        settle();
    }
    adp_mbx_set_enable(&app.adp, false);
    mbx_model_set_link(&model, 0, true);
    settle();
    EXPECT_EQ(clock_reads, 3u) << "H9 a LINK_UP while disabled reads no clock";
    adp_mbx_set_enable(&app.adp, true);
    EXPECT_TRUE(clock_reads == 4u && adp0()->last_draw == ADP_DRAW_STARTUP)
        << "H9 the startup draw reads the clock once";
}

// H10 boots alike up to a LINK_UP, their clocks apart only when it comes: the LINK_UP's sample sets its draw.
TEST_F(AdpDraw, H10TheClockAtTheLinkUpSetsItsDraw) {
    Spread d;
    for (uint32_t k = 0; k < kHosts; ++k) {
        sample = 7u;
        mbx_model_reset(&model);
        mbx_model_bind(&model, nullptr, nullptr);
        mbx_model_set_gm(&model, 0, kGmA, 0);
        struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr,
                                       nullptr, nullptr, nullptr, 0};
        ASSERT_TRUE(ctrl_app_start(&app, &cfg)) << "H10 the app starts on the model";
        settle();
        sample = 41000u + k;
        mbx_model_set_link(&model, 0, true);
        settle();
        ASSERT_EQ(adp0()->draws, 1u) << "H10 the LINK_UP draws";
        d.add(adp0()->last_draw_ms);
    }
    std::printf("  H10 %u distinct first delays of %u boots apart only at the LINK_UP\n",
                static_cast<unsigned>(d.values.size()), static_cast<unsigned>(kHosts));
    EXPECT_TRUE(d.values.size() >= 600u) << "H10 boots apart only at the LINK_UP draw apart";
    EXPECT_TRUE(uniform("H10 the first LINK_UP", d, kLinkUpDrawMaxMs) <= kChiSquare99)
        << "H10 and draw uniformly from the clock read at the LINK_UP";
}

TEST(AdpAdapter, B1StaleTagDiscarded) {
    adapter_race();
}

void refused_discovery(const uint8_t* bytes, unsigned length) {
    boot();
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    adp expected = *adp0();
    expected.discarded++;
    const auto sent = model.tx_sent;
    const auto timers = model.tmr_ops;
    mbx_frame frame{};
    frame.interface = 0;
    frame.len = static_cast<uint16_t>(length);
    std::memcpy(frame.bytes, bytes, length);
    app.loop.rx[MBX_CH_ADP].fn(app.loop.rx[MBX_CH_ADP].ctx, &frame);
    EXPECT_EQ(std::memcmp(adp0(), &expected, sizeof expected), 0)
        << "malformed discovery changes only the discard count through the parent adapter";
    EXPECT_EQ(model.tx_sent, sent) << "malformed discovery sends no response";
    EXPECT_EQ(model.tmr_ops, timers) << "malformed discovery touches no timer";
}

TEST(AdpAdapter, PinRejectsEveryTruncatedDiscovery) {
    uint8_t frame[82];
    discover(frame, 2u, 0u);
    for (unsigned length = 0; length < 82u; ++length) {
        refused_discovery(frame, length);
    }
}

TEST(AdpAdapter, PinRejectsUnsupportedDiscoveryVersions) {
    uint8_t frame[82];
    discover(frame, 2u, 0u);
    for (unsigned version = 1; version < 8u; ++version) {
        frame[15] = static_cast<uint8_t>((version << 4) | 2u);
        refused_discovery(frame, sizeof frame);
    }
}

TEST(AdpAdapter, PinRejectsShortDiscoveryControlLength) {
    uint8_t frame[82];
    discover(frame, 2u, 0u);
    for (unsigned valid_time : {0u, 31u}) {
        for (unsigned length : {0u, 55u}) {
            wire_put_be(frame + 16, (valid_time << 11) | length, 2);
            refused_discovery(frame, sizeof frame);
        }
    }
}

// A longer PDU is read by its first 56 octets (IEEE 1722.1-2021 6.2.2.6 and 6.2.7.1.3, Milan v1.2 5.6.3.1), whole or
// with the surplus absent; 102 fills the channel's largest frame, so 256 and 2047 arrive without theirs.
TEST(AdpAdapter, PinAcceptsLongDiscoveryThroughMailbox) {
    for (unsigned length : {57u, 84u, 102u, 256u, 2047u}) {
        for (size_t octets : {size_t{82}, size_t{26} + length}) {
            if (octets > MBX_CH_ADP_MAX_FRAME_BYTES) {
                continue;
            }
            boot();
            mbx_model_set_link(&model, 0, true);
            settle();
            to_waiting();
            uint8_t frame[MBX_CH_ADP_MAX_FRAME_BYTES];
            std::memset(frame, 0xFF, sizeof frame);
            discover(frame, 2u, entity.entity_id);
            wire_put_be(frame + 16, length, 2);
            const auto discarded = adp0()->discarded;
            ASSERT_TRUE(mbx_model_rx(&model, frame, octets, 0)) << "the adp channel keeps a longer discovery";
            pass();
            EXPECT_EQ(adp0()->state, ADP_STATE_DELAY) << "a longer discovery restarts advertising through the mailbox";
            EXPECT_EQ(adp0()->discarded, discarded) << "a longer discovery is not discarded";
        }
    }
}

TEST(AdpAdapter, PinAcceptsCompleteDiscoveryThroughMailbox) {
    boot();
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    uint8_t frame[82];
    discover(frame, 2u, entity.entity_id);
    wire_put_be(frame + 16, (31u << 11) | 56u, 2);
    const auto discarded = adp0()->discarded;
    ASSERT_TRUE(mbx_model_rx(&model, frame, sizeof frame, 0));
    pass();
    EXPECT_EQ(adp0()->state, ADP_STATE_DELAY) << "complete discovery restarts advertising through the mailbox";
    EXPECT_EQ(adp0()->discarded, discarded) << "valid_time bits are outside control_data_length";
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

TEST(AdpFirstAvailable, G1G5WithinTheLinkUpDrawOfEveryLinkUp) {
    Spread first;
    Spread later;
    first_after_link_up(first, later);
}
TEST(AdpFirstAvailable, G2WithinTheStartupDraw) {
    first_after_startup();
}
TEST(AdpFirstAvailable, G3AGrandmasterChangeBeforeItIsCarriedByIt) {
    gm_change_before_first();
}
TEST(AdpFirstAvailable, G4AGrandmasterChangeAfterItIsAnnounced) {
    gm_change_after_first();
}

TEST(AdpBacklog, F0toF7FullBacklogs) {
    const Backlog b = backlog_post();
    const Passes s = backlog_take(b);
    backlog_grade(b, s);
}

}  // namespace
