// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_adp.cpp - the ADP slice beyond the processor's walk (#665 lanes F0
// and FT; GoogleTest):
//
//   A   the core over fake ports, the paths the mailbox cannot provoke on
//       demand: a send the port refuses (deferred, retried, dropped by a
//       link loss), a stray expiry, the firmware's own 5.6.3.1 discard
//       (the fabric filter normally spares it the work), the two draw kinds,
//       an owed ENTITY_DEPARTING across a restart (A15 to A17), the owed-frame
//       rule across a link loss, a GM change, a DISCOVER and a stray expiry
//       (A18 to A20), and the bound on owed DEPARTINGs (A21);
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

struct fake {
    bool room;
    bool link;
    unsigned sends;
    uint8_t last[ADP_FRAME_BYTES];
    uint8_t msg[16];     // message_type of each frame taken, in order
    uint32_t index[16];  // and its available_index
    unsigned starts;
    uint32_t last_delay;
    unsigned stops;
    uint64_t gm;
    uint8_t domain;
};

struct fake fk;

bool fake_send(void* ctx, unsigned interface, const uint8_t* frame, size_t len) {
    static_cast<void>(ctx);
    static_cast<void>(interface);
    if (!fk.room || len != ADP_FRAME_BYTES) {
        return false;
    }
    std::memcpy(fk.last, frame, len);
    if (fk.sends < 16u) {
        fk.msg[fk.sends] = frame[15] & 0x0Fu;
        fk.index[fk.sends] = wire_be32(frame + 50);
    }
    fk.sends++;
    return true;
}

void fake_start(void* ctx, unsigned interface, uint32_t delay_ms) {
    static_cast<void>(ctx);
    static_cast<void>(interface);
    fk.starts++;
    fk.last_delay = delay_ms;
}

void fake_stop(void* ctx, unsigned interface) {
    static_cast<void>(ctx);
    static_cast<void>(interface);
    fk.stops++;
}

void fake_gptp(void* ctx, unsigned interface, uint64_t* gm, uint8_t* domain) {
    static_cast<void>(ctx);
    static_cast<void>(interface);
    *gm = fk.gm;
    *domain = fk.domain;
}

bool fake_link(void* ctx, unsigned interface) {
    static_cast<void>(ctx);
    static_cast<void>(interface);
    return fk.link;
}

uint32_t fake_seed(void* ctx) {
    static_cast<void>(ctx);
    return 0x5EEDu;
}

const struct adp_ports ports = {nullptr, fake_send, fake_start, fake_stop, fake_gptp, fake_link, fake_seed};

void discover(uint8_t* f, uint8_t msg, uint64_t eid) {
    std::memset(f, 0, ADP_FRAME_BYTES);
    wire_put_be(f, 0x91E0F0010000ull, 6);
    wire_put_be(f + 12, ADP_ETHERTYPE, 2);
    f[14] = ADP_SUBTYPE;
    f[15] = msg;
    wire_put_be(f + 18, eid, 8);
}

void fresh(struct adp* a, bool link) {
    std::memset(&fk, 0, sizeof fk);
    fk.room = true;
    fk.link = link;
    fk.gm = 0xA1A2A3A4A5A6A7A8ull;
    adp_init(a, &entity, &ports, 0, 2);
}

void core_schedule(void) {
    struct adp a;
    fresh(&a, false);
    adp_set_enable(&a, true);
    EXPECT_EQ(a.state, ADP_STATE_DOWN) << "A0 enabled with the link down: DOWN (5.6.3.5.1)";
    EXPECT_EQ(fk.starts, 0) << "A0 and no timer";
    adp_link_change(&a, true);
    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY && fk.last_delay == a.last_draw_ms &&
                fk.last_delay <= ADP_DELAY_MAX_MS)
        << "A0 LINK_UP: DELAY with a 0..4 s draw (5.6.3.5.3)";
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 1u && fk.last[15] == ADP_MSG_ENTITY_AVAILABLE && a.state == ADP_STATE_WAITING &&
                fk.last_delay == ADP_ADVERTISE_MS)
        << "A1 TMR_DELAY: ENTITY_AVAILABLE, WAITING, TMR_ADVERTISE 5 s (5.6.3.5.9)";
    EXPECT_EQ(wire_be16(fk.last + 16), (10u << 11) | 56u) << "A1 valid_time 10, control_data_length 56";
    EXPECT_EQ(wire_be32(fk.last + 50), 0) << "A1 the first available_index is 0";
    EXPECT_EQ(a.available_index, 1) << "A1 available_index is incremented after the send (6.2.2.15)";
    fk.gm = 0x0102030405060708ull;
    fk.domain = 3;
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 2u && wire_be32(fk.last + 50) == 1u && wire_be64(fk.last + 54) == 0x0102030405060708ull &&
                fk.last[62] == 3u)
        << "A2 the next cycle carries index 1 and the grandmaster sampled at build";
    adp_set_current_configuration(&a, 0x0103);
    adp_gm_change(&a);
    adp_timer_expired(&a);
    EXPECT_EQ(fk.sends, 3) << "A2 GM_CHANGE in WAITING re-advertises (5.6.3.5.7)";
    EXPECT_EQ(wire_be16(fk.last + 64), 0x0103) << "A2 with the new current_configuration_index (6.2.2.18)";
    EXPECT_EQ(wire_be16(fk.last + 66), 5) << "A2 and the entity's identify_control_index (6.2.2.19)";
}

void core_discard(void) {
    struct adp a;
    uint8_t f[ADP_FRAME_BYTES];
    fresh(&a, true);
    adp_set_enable(&a, true);
    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_STARTUP &&
                a.last_draw_ms <= ADP_DELAY_STARTUP_MAX_MS)
        << "A3 enabled with the link up: DELAY with a 0..2 s draw (5.6.3.5.2)";
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    unsigned starts = fk.starts;
    adp_rx(&a, f, sizeof f);
    EXPECT_TRUE(fk.starts == starts && a.discarded == 0u) << "A3 RCV_ADP_DISCOVER in DELAY is ignored (Table 5.51)";
    adp_timer_expired(&a);
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0x7766554433221100ull);
    adp_rx(&a, f, sizeof f);
    discover(f, ADP_MSG_ENTITY_AVAILABLE, 0);
    adp_rx(&a, f, sizeof f);
    adp_rx(&a, f, 25u);
    EXPECT_EQ(a.discarded, 3) << "A4 a foreign DISCOVER, an AVAILABLE and a truncated ADPDU are discarded (5.6.3.1)";
    EXPECT_EQ(a.state, ADP_STATE_WAITING) << "A4 and leave WAITING alone";
    discover(f, ADP_MSG_ENTITY_DISCOVER, entity.entity_id);
    unsigned stops = fk.stops;
    adp_rx(&a, f, sizeof f);
    EXPECT_TRUE(fk.stops == stops + 1u && a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY)
        << "A4 a DISCOVER for this entity stops TMR_ADVERTISE and enters DELAY (5.6.3.5.4)";
    adp_timer_expired(&a);
    unsigned sends = fk.sends;
    a.timer = ADP_TIMER_NONE;
    adp_timer_expired(&a);
    EXPECT_EQ(a.stray_expiries, 1) << "A5 an expiry with no timer running is a stray, counted";
    EXPECT_EQ(fk.sends, sends) << "A5 and sends nothing";
}

void core_deferred(void) {
    struct adp a;
    fresh(&a, true);
    adp_set_enable(&a, true);
    fk.room = false;
    adp_timer_expired(&a);
    EXPECT_TRUE(a.available_owed && a.state == ADP_STATE_DELAY && a.deferred_sends == 1u)
        << "A6 a refused send keeps ENTITY_AVAILABLE owed in DELAY";
    adp_poll(&a);
    EXPECT_EQ(a.deferred_sends, 2) << "A6 a poll without room retries and keeps it";
    fk.room = true;
    adp_poll(&a);
    EXPECT_TRUE(fk.sends == 1u && a.state == ADP_STATE_WAITING && !a.available_owed &&
                fk.last_delay == ADP_ADVERTISE_MS)
        << "A6 a poll with room sends it and completes 5.6.3.5.9";
    adp_timer_expired(&a);
    fk.room = false;
    adp_timer_expired(&a);
    adp_link_change(&a, false);
    fk.room = true;
    adp_poll(&a);
    EXPECT_TRUE(fk.sends == 1u && a.state == ADP_STATE_DOWN && !a.available_owed && a.departing_owed == 0u)
        << "A7 a link loss drops an owed ENTITY_AVAILABLE and departs nothing (5.6.3.5.10)";
    adp_link_change(&a, true);
    adp_timer_expired(&a);
    uint32_t index = a.available_index;
    fk.room = false;
    adp_set_enable(&a, false);
    EXPECT_TRUE(a.departing_owed == 1u && a.available_index == 0u && a.state == ADP_STATE_DOWN)
        << "A8 SHUTDOWN with no room keeps ENTITY_DEPARTING owed, index reset";
    adp_link_change(&a, false);
    fk.room = true;
    adp_poll(&a);
    EXPECT_TRUE(fk.last[15] == ADP_MSG_ENTITY_DEPARTING && wire_be32(fk.last + 50) == index &&
                wire_be16(fk.last + 16) == 56u)
        << "A8 a link loss does not drop it; the next poll sends it with the index current at SHUTDOWN";
    unsigned sends = fk.sends;
    fk.link = false;
    adp_set_enable(&a, true);
    adp_set_enable(&a, false);
    EXPECT_EQ(fk.sends, sends) << "A8 SHUTDOWN in DOWN sends nothing (Table 5.51)";
}

// IEEE 1722.1-2021 6.2.2.15 with Figures 6-2 and 6-3 and 6.2.5.2.2 (the
// ruling on PR #668, comment 5994972330): ENTITY_DEPARTING carries the
// CURRENT available_index, and the first ENTITY_AVAILABLE after a restart
// carries 0. Every value below is read off the frame the port was given.
uint32_t wire_index(void) {
    return wire_be32(fk.last + 50);
}

bool wire_is(uint8_t msg, uint32_t index) {
    return (fk.last[15] & 0x0Fu) == msg && wire_index() == index;
}

void core_departing_index(void) {
    struct adp a;
    fresh(&a, true);
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 0)) << "A10 the first ENTITY_AVAILABLE carries 0";
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 1)) << "A10 the second carries 1";
    EXPECT_EQ(a.state, ADP_STATE_WAITING) << "A10 SHUTDOWN is taken in WAITING";
    adp_set_enable(&a, false);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_DEPARTING, 2))
        << "A10 SHUTDOWN in WAITING, sent at once: ENTITY_DEPARTING carries the current index, 2";
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 0)) << "A11 the first ENTITY_AVAILABLE after a restart carries 0";
    adp_timer_expired(&a);
    EXPECT_EQ(a.state, ADP_STATE_DELAY) << "A12 SHUTDOWN is taken in DELAY";
    adp_set_enable(&a, false);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_DEPARTING, 1))
        << "A12 SHUTDOWN in DELAY, sent at once: ENTITY_DEPARTING carries the current index, 1";
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    fk.room = false;
    adp_set_enable(&a, false);
    EXPECT_TRUE(a.departing_owed == 1u) << "A13 SHUTDOWN with no room leaves ENTITY_DEPARTING owed";
    fk.room = true;
    adp_poll(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_DEPARTING, 2))
        << "A13 sent from a later poll, it carries the index current at SHUTDOWN, 2";
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 0)) << "A13 and the restart's first ENTITY_AVAILABLE carries 0";
    adp_timer_expired(&a);
    a.available_index = 0xFFFFFFFFu;
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 0xFFFFFFFFu)) << "A14 available_index 0xFFFFFFFF goes on the wire";
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_AVAILABLE, 0)) << "A14 the next ENTITY_AVAILABLE carries 0, modulo 2^32";
    adp_set_enable(&a, false);
    EXPECT_TRUE(wire_is(ADP_MSG_ENTITY_DEPARTING, 1))
        << "A14 SHUTDOWN after the wrap: ENTITY_DEPARTING carries the current index, 1";
}

// The frame the fake took k-th is `msg` carrying `index`.
bool took(unsigned k, uint8_t msg, uint32_t index) {
    return k < fk.sends && k < 16u && fk.msg[k] == msg && fk.index[k] == index;
}

// One ENTITY_AVAILABLE sent (index 0, so 1 is current), then SHUTDOWN behind
// a full transmit path: ENTITY_DEPARTING owed with index 1. Then a restart.
void advertise_then_depart_owed(struct adp* a) {
    fresh(a, true);
    adp_set_enable(a, true);
    adp_timer_expired(a);
    fk.room = false;
    adp_set_enable(a, false);
    adp_set_enable(a, true);
}

// R497-2-F1: an owed ENTITY_DEPARTING is never lost to a restart. It keeps
// its SHUTDOWN index and leaves before the restart's ENTITY_AVAILABLE.
void core_owed_departing(void) {
    struct adp a;
    advertise_then_depart_owed(&a);
    EXPECT_TRUE(took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && fk.sends == 1u && a.departing_owed == 1u &&
                a.departing_index == 1u)
        << "A15 advertised once, SHUTDOWN behind a full ring: ENTITY_DEPARTING owed with index 1";
    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && a.last_draw == ADP_DRAW_STARTUP)
        << "A15 the restart runs while it is owed: DELAY, the startup TMR_DELAY armed";
    unsigned starts = fk.starts;
    adp_timer_expired(&a);
    EXPECT_TRUE(a.available_owed && a.departing_owed == 1u && a.departing_index == 1u && a.state == ADP_STATE_DELAY &&
                a.timer == ADP_TIMER_NONE && fk.starts == starts && fk.sends == 1u)
        << "A15 that TMR_DELAY expires before the ring has room: ENTITY_AVAILABLE owed behind it, no timer";
    EXPECT_TRUE(adp_poll(&a) && a.available_owed && a.departing_owed == 1u && fk.sends == 1u)
        << "A15 a poll without room keeps both owed";
    fk.room = true;
    EXPECT_TRUE(adp_poll(&a) && fk.sends == 2u && took(1, ADP_MSG_ENTITY_DEPARTING, 1))
        << "A15 with room, the next poll sends the owed ENTITY_DEPARTING first, with its SHUTDOWN index 1";
    EXPECT_TRUE(!adp_poll(&a) && fk.sends == 3u && took(2, ADP_MSG_ENTITY_AVAILABLE, 0))
        << "A15 and the one after it the restart's ENTITY_AVAILABLE, with index 0";
    EXPECT_TRUE(a.state == ADP_STATE_WAITING && a.timer == ADP_TIMER_ADVERTISE && fk.starts == starts + 1u &&
                fk.last_delay == ADP_ADVERTISE_MS && a.available_index == 1u)
        << "A15 then WAITING with TMR_ADVERTISE armed 5 s, available_index 1";
    EXPECT_TRUE(!a.available_owed && a.departing_owed == 0u && !adp_poll(&a) && fk.sends == 3u)
        << "A15 and nothing stranded: nothing owed, a further poll sends nothing";
    adp_timer_expired(&a);
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 4u && took(3, ADP_MSG_ENTITY_AVAILABLE, 1))
        << "A15 the schedule runs on: the next ENTITY_AVAILABLE carries 1";
}

// A second SHUTDOWN while the first DEPARTING is owed queues its own.
void core_owed_second_shutdown(void) {
    struct adp a;
    advertise_then_depart_owed(&a);
    adp_timer_expired(&a);
    adp_set_enable(&a, false);
    EXPECT_TRUE(a.departing_owed == 2u && a.departing_index == 1u && !a.available_owed && a.state == ADP_STATE_DOWN)
        << "A16 a SHUTDOWN while one is owed queues its own ENTITY_DEPARTING and drops the owed AVAILABLE";
    adp_set_enable(&a, true);
    fk.room = true;
    static_cast<void>(adp_poll(&a));
    bool owed = adp_poll(&a);
    EXPECT_TRUE(fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_DEPARTING, 0) && !owed)
        << "A16 each leaves in order with its SHUTDOWN's index: 1, then 0 (that run sent nothing)";
    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && !a.available_owed)
        << "A16 the restart running meanwhile is untouched: DELAY, its TMR_DELAY armed";
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 4u && took(3, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING)
        << "A16 its ENTITY_AVAILABLE, with index 0, leaves at its TMR_DELAY expiry; WAITING";
}

// Room returns, and the restart's TMR_DELAY expires before any poll.
void core_owed_room_first(void) {
    struct adp a;
    advertise_then_depart_owed(&a);
    fk.room = true;
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 1u && a.available_owed && a.departing_owed == 1u && a.state == ADP_STATE_DELAY)
        << "A17 room back and TMR_DELAY expiring before a poll: the ENTITY_AVAILABLE does not pass the owed DEPARTING";
    static_cast<void>(adp_poll(&a));
    bool owed = adp_poll(&a);
    EXPECT_TRUE(fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_AVAILABLE, 0) &&
                !owed && a.state == ADP_STATE_WAITING)
        << "A17 the polls then send DEPARTING with index 1 and AVAILABLE with index 0, in that order";
}

// R496-3-F2: the legs of the owed-frame rule (adp.h) A15 to A17 leave open.
// A link loss while the restart runs, before and after its TMR_DELAY expiry.
void core_owed_link_loss(void) {
    struct adp a;
    advertise_then_depart_owed(&a);
    adp_link_change(&a, false);
    EXPECT_TRUE(a.state == ADP_STATE_DOWN && a.timer == ADP_TIMER_NONE && a.departing_owed == 1u &&
                a.departing_index == 1u && fk.sends == 1u)
        << "A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING, index 1";
    adp_link_change(&a, true);
    EXPECT_TRUE(a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && a.last_draw == ADP_DRAW_DELAY &&
                a.departing_owed == 1u && a.departing_index == 1u)
        << "A18 the link's return starts a new run with the ENTITY_DEPARTING still owed (5.6.3.5.3)";
    adp_timer_expired(&a);
    adp_link_change(&a, false);
    EXPECT_TRUE(a.state == ADP_STATE_DOWN && !a.available_owed && a.departing_owed == 1u && a.departing_index == 1u &&
                fk.sends == 1u)
        << "A18 a link loss with that run's ENTITY_AVAILABLE owed drops the AVAILABLE and keeps the DEPARTING";
    adp_link_change(&a, true);
    fk.room = true;
    bool owed = adp_poll(&a);
    EXPECT_TRUE(!owed && fk.sends == 2u && took(1, ADP_MSG_ENTITY_DEPARTING, 1))
        << "A18 with room the ENTITY_DEPARTING leaves, index 1";
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 3u && took(2, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING)
        << "A18 then the new run's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING";
}

// Inputs that leave an owed ENTITY_AVAILABLE owed: Milan v1.2 Table 5.51
// ignores GM_CHANGE and RCV_ADP_DISCOVER in DELAY, and a stray is no input.
void core_owed_inputs_ignored(void) {
    struct adp a;
    uint8_t f[ADP_FRAME_BYTES];
    fresh(&a, true);
    adp_set_enable(&a, true);
    fk.room = false;
    adp_timer_expired(&a);
    unsigned starts = fk.starts;
    adp_gm_change(&a);
    EXPECT_TRUE(a.available_owed && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_NONE && fk.starts == starts)
        << "A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed, no timer started";
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    adp_rx(&a, f, sizeof f);
    EXPECT_TRUE(a.available_owed && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_NONE && fk.starts == starts)
        << "A19 so does an ENTITY_DISCOVER";
    adp_timer_expired(&a);
    EXPECT_TRUE(a.available_owed && a.stray_expiries == 1u && a.state == ADP_STATE_DELAY && fk.sends == 0u)
        << "A19 and a stray expiry, which is counted";
    fk.room = true;
    bool owed = adp_poll(&a);
    EXPECT_TRUE(!owed && fk.sends == 1u && took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING &&
                a.timer == ADP_TIMER_ADVERTISE && fk.last_delay == ADP_ADVERTISE_MS)
        << "A19 the next poll with room sends it, index 0, then WAITING with TMR_ADVERTISE 5 s";
}

// A link loss itself drops an owed ENTITY_AVAILABLE, with no poll between.
void core_owed_link_loss_drops(void) {
    struct adp a;
    fresh(&a, true);
    adp_set_enable(&a, true);
    fk.room = false;
    adp_timer_expired(&a);
    adp_link_change(&a, false);
    EXPECT_TRUE(!a.available_owed && a.state == ADP_STATE_DOWN && a.departing_owed == 0u)
        << "A20 a link loss drops the owed ENTITY_AVAILABLE at once, before any poll (5.6.3.5.10)";
    adp_link_change(&a, true);
    fk.room = true;
    bool owed = adp_poll(&a);
    EXPECT_TRUE(!owed && fk.sends == 0u && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY &&
                a.last_draw == ADP_DRAW_DELAY)
        << "A20 after the link's return a poll sends nothing: the new run waits for its TMR_DELAY (5.6.3.5.3)";
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 1u && took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING)
        << "A20 whose expiry sends the ENTITY_AVAILABLE, index 0; WAITING";
}

// R497-3-F1: at most ADP_DEPARTING_OWED_MAX DEPARTINGs are owed; a SHUTDOWN
// beyond them is coalesced into the queued one and counted (adp.h).
void core_departing_capacity(void) {
    struct adp a;
    advertise_then_depart_owed(&a);
    adp_timer_expired(&a);
    adp_set_enable(&a, false);
    EXPECT_TRUE(a.departing_owed == ADP_DEPARTING_OWED_MAX && a.departing_owed == 2u && a.departing_index == 1u &&
                a.departing_coalesced == 0u)
        << "A21 a second SHUTDOWN takes the last place: two owed, the oldest with index 1, none coalesced";
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    adp_set_enable(&a, false);
    EXPECT_TRUE(a.departing_owed == 2u && a.departing_index == 1u && a.departing_coalesced == 1u && !a.available_owed &&
                a.state == ADP_STATE_DOWN && fk.sends == 1u)
        << "A21 the next SHUTDOWN is coalesced into the queued one and counted; its run's owed AVAILABLE is dropped";
    for (unsigned k = 0; k < 100000u; ++k) {
        adp_set_enable(&a, true);
        adp_set_enable(&a, false);
    }
    EXPECT_TRUE(a.departing_owed == 2u && a.departing_index == 1u && a.departing_coalesced == 100001u && fk.sends == 1u)
        << "A21 and so are 100000 more, each counted, the two owed unchanged";
    adp_set_enable(&a, true);
    fk.room = true;
    static_cast<void>(adp_poll(&a));
    bool owed = adp_poll(&a);
    EXPECT_TRUE(fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_DEPARTING, 0) &&
                !owed && !adp_poll(&a) && fk.sends == 3u)
        << "A21 with room the wire carries DEPARTING 1, then one DEPARTING 0, and nothing more is owed";
    adp_timer_expired(&a);
    EXPECT_TRUE(fk.sends == 4u && took(3, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING)
        << "A21 then the running restart's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING";
}

void core_draws(void) {
    struct adp a;
    fresh(&a, true);
    uint32_t max_start = 0;
    uint32_t max_delay = 0;
    bool in_range = true;
    for (unsigned k = 0; k < 400u; ++k) {
        adp_set_enable(&a, true);
        in_range = in_range && a.last_draw == ADP_DRAW_STARTUP && a.last_draw_ms <= ADP_DELAY_STARTUP_MAX_MS;
        max_start = a.last_draw_ms > max_start ? a.last_draw_ms : max_start;
        adp_link_change(&a, false);
        adp_link_change(&a, true);
        in_range = in_range && a.last_draw == ADP_DRAW_DELAY && a.last_draw_ms <= ADP_DELAY_MAX_MS;
        max_delay = a.last_draw_ms > max_delay ? a.last_draw_ms : max_delay;
        adp_set_enable(&a, false);
    }
    EXPECT_TRUE(in_range) << "A9 every startup draw is 0..2 s and every other draw 0..4 s";
    EXPECT_TRUE(max_delay > ADP_DELAY_STARTUP_MAX_MS) << "A9 the two kinds are distinct: the 0..4 s draws pass 2 s";
    EXPECT_TRUE(max_start > 1800u && max_delay > 3600u) << "A9 and both reach near their maxima";
}

// The random-delay generator never sticks at zero: an entity whose id words
// cancel the seed constant, and a start seed equal to the state, each leave
// it at 1 (xorshift32 maps 0 to 0 for ever) (#665 FT, coverage).
uint32_t seed_value;

uint32_t chosen_seed(void* ctx) {
    static_cast<void>(ctx);
    return seed_value;
}

void core_rng_never_zero(void) {
    static const adp_entity cancelling = {0x000000009E3779B9ull, 1u, 2u, 3u, 1u, 1u, 1u, 1u, 0u};
    static const adp_ports seeded = {nullptr, fake_send, fake_start, fake_stop, fake_gptp, fake_link, chosen_seed};
    struct adp a;
    fresh(&a, true);
    adp_init(&a, &cancelling, &seeded, 0, 0);
    EXPECT_EQ(a.rng, 1u) << "A22 an entity id whose words cancel the seed constant starts the generator at 1";
    seed_value = a.rng;
    adp_set_enable(&a, true);
    EXPECT_TRUE(a.rng != 0u && a.state == ADP_STATE_DELAY && a.draws == 1u)
        << "A22 a start seed equal to the state leaves it at 1 and the startup draw is made";
}

// A repeated enable or disable changes nothing: no draw, no timer, no frame
// (#665 FT, coverage).
void core_enable_idempotent(void) {
    struct adp a;
    fresh(&a, true);
    adp_set_enable(&a, false);
    EXPECT_TRUE(fk.sends == 0u && fk.stops == 0u && a.state == ADP_STATE_DOWN)
        << "A23 a disable while disabled sends and stops nothing";
    adp_set_enable(&a, true);
    const unsigned draws = a.draws;
    const unsigned starts = fk.starts;
    adp_set_enable(&a, true);
    EXPECT_TRUE(a.draws == draws && fk.starts == starts && a.state == ADP_STATE_DELAY)
        << "A23 an enable while enabled draws and arms nothing";
}

// 5.6.3.1 discards an ADPDU of another EtherType or another subtype, counted
// (#665 FT, coverage).
void core_discard_kinds(void) {
    struct adp a;
    uint8_t f[ADP_FRAME_BYTES];
    fresh(&a, true);
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    wire_put_be(f + 12, 0x88F5u, 2);
    adp_rx(&a, f, sizeof f);
    discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
    f[ADP_HEADER_BYTES] = 0xFCu;
    adp_rx(&a, f, sizeof f);
    EXPECT_EQ(a.discarded, 2u) << "A24 a DISCOVER under another EtherType or subtype is discarded and counted";
    EXPECT_EQ(a.state, ADP_STATE_WAITING) << "A24 and leaves WAITING alone";
}

// ---- the adapter and the latency bounds, on the model ---------------------------

struct mbx_model model;
struct ctrl_app app;
alignas(std::max_align_t) uint8_t arena[1024];
const struct ctrl_pool_class classes[] = {{32u, 8u}};

void boot(void) {
    mbx_model_reset(&model);
    mbx_model_bind(&model, nullptr, nullptr);
    struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, nullptr, nullptr, nullptr, nullptr};
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

TEST(AdpCore, A0toA2Schedule) {
    core_schedule();
}
TEST(AdpCore, A3toA5DiscoverAndDiscard) {
    core_discard();
}
TEST(AdpCore, A6toA8DeferredSends) {
    core_deferred();
}
TEST(AdpCore, A9DrawKinds) {
    core_draws();
}
TEST(AdpCore, A10toA14DepartingIndex) {
    core_departing_index();
}
TEST(AdpCore, A15OwedDepartingAcrossARestart) {
    core_owed_departing();
}
TEST(AdpCore, A16SecondShutdownQueuesItsOwn) {
    core_owed_second_shutdown();
}
TEST(AdpCore, A17RoomBackBeforeAPoll) {
    core_owed_room_first();
}
TEST(AdpCore, A18LinkLossKeepsTheOwedDeparting) {
    core_owed_link_loss();
}
TEST(AdpCore, A19IgnoredInputsKeepTheOwedAvailable) {
    core_owed_inputs_ignored();
}
TEST(AdpCore, A20LinkLossDropsTheOwedAvailable) {
    core_owed_link_loss_drops();
}
TEST(AdpCore, A21DepartingCapacity) {
    core_departing_capacity();
}
TEST(AdpCore, A22GeneratorNeverStuckAtZero) { core_rng_never_zero(); }
TEST(AdpCore, A23RepeatedEnableOrDisableChangesNothing) { core_enable_idempotent(); }
TEST(AdpCore, A24OtherEtherTypeOrSubtypeDiscarded) { core_discard_kinds(); }
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
