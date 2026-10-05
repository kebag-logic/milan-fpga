// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_adp.c - the ADP slice beyond the processor's walk (#665 lane F0):
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

#include <stdio.h>
#include <string.h>

#include "adp.h"
#include "adp_mbx.h"
#include "ctrl_app.h"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "test_check.h"
#include "wire.h"

static const struct adp_entity entity = {
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
	uint8_t msg[16];        // message_type of each frame taken, in order
	uint32_t index[16];     // and its available_index
	unsigned starts;
	uint32_t last_delay;
	unsigned stops;
	uint64_t gm;
	uint8_t domain;
};

static struct fake fk;

static bool fake_send(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx;
	(void)interface;
	if (!fk.room || len != ADP_FRAME_BYTES) {
		return false;
	}
	memcpy(fk.last, frame, len);
	if (fk.sends < 16u) {
		fk.msg[fk.sends] = frame[15] & 0x0Fu;
		fk.index[fk.sends] = wire_be32(frame + 50);
	}
	fk.sends++;
	return true;
}

static void fake_start(void *ctx, unsigned interface, uint32_t delay_ms)
{
	(void)ctx;
	(void)interface;
	fk.starts++;
	fk.last_delay = delay_ms;
}

static void fake_stop(void *ctx, unsigned interface)
{
	(void)ctx;
	(void)interface;
	fk.stops++;
}

static void fake_gptp(void *ctx, unsigned interface, uint64_t *gm, uint8_t *domain)
{
	(void)ctx;
	(void)interface;
	*gm = fk.gm;
	*domain = fk.domain;
}

static bool fake_link(void *ctx, unsigned interface)
{
	(void)ctx;
	(void)interface;
	return fk.link;
}

static uint32_t fake_seed(void *ctx)
{
	(void)ctx;
	return 0x5EEDu;
}

static const struct adp_ports ports = {NULL, fake_send, fake_start, fake_stop, fake_gptp, fake_link, fake_seed};

static void discover(uint8_t *f, uint8_t msg, uint64_t eid)
{
	memset(f, 0, ADP_FRAME_BYTES);
	wire_put_be(f, 0x91E0F0010000ull, 6);
	wire_put_be(f + 12, ADP_ETHERTYPE, 2);
	f[14] = ADP_SUBTYPE;
	f[15] = msg;
	wire_put_be(f + 18, eid, 8);
}

static void fresh(struct adp *a, bool link)
{
	memset(&fk, 0, sizeof fk);
	fk.room = true;
	fk.link = link;
	fk.gm = 0xA1A2A3A4A5A6A7A8ull;
	adp_init(a, &entity, &ports, 0, 2);
}

static void core_schedule(void)
{
	struct adp a;
	fresh(&a, false);
	adp_set_enable(&a, true);
	check_eq("A0 enabled with the link down: DOWN (5.6.3.5.1)", a.state, ADP_STATE_DOWN);
	check_eq("A0 and no timer", fk.starts, 0);
	adp_link_change(&a, true);
	check("A0 LINK_UP: DELAY with a 0..4 s draw (5.6.3.5.3)", a.state == ADP_STATE_DELAY &&
	      a.last_draw == ADP_DRAW_DELAY && fk.last_delay == a.last_draw_ms && fk.last_delay <= ADP_DELAY_MAX_MS);
	adp_timer_expired(&a);
	check("A1 TMR_DELAY: ENTITY_AVAILABLE, WAITING, TMR_ADVERTISE 5 s (5.6.3.5.9)",
	      fk.sends == 1u && fk.last[15] == ADP_MSG_ENTITY_AVAILABLE && a.state == ADP_STATE_WAITING &&
		      fk.last_delay == ADP_ADVERTISE_MS);
	check_eq("A1 valid_time 10, control_data_length 56", wire_be16(fk.last + 16), (10u << 11) | 56u);
	check_eq("A1 the first available_index is 0", wire_be32(fk.last + 50), 0);
	check_eq("A1 available_index is incremented after the send (6.2.2.15)", a.available_index, 1);
	fk.gm = 0x0102030405060708ull;
	fk.domain = 3;
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	check("A2 the next cycle carries index 1 and the grandmaster sampled at build",
	      fk.sends == 2u && wire_be32(fk.last + 50) == 1u && wire_be64(fk.last + 54) == 0x0102030405060708ull &&
		      fk.last[62] == 3u);
	adp_set_current_configuration(&a, 0x0103);
	adp_gm_change(&a);
	adp_timer_expired(&a);
	check_eq("A2 GM_CHANGE in WAITING re-advertises (5.6.3.5.7)", fk.sends, 3);
	check_eq("A2 with the new current_configuration_index (6.2.2.18)", wire_be16(fk.last + 64), 0x0103);
	check_eq("A2 and the entity's identify_control_index (6.2.2.19)", wire_be16(fk.last + 66), 5);
}

static void core_discard(void)
{
	struct adp a;
	uint8_t f[ADP_FRAME_BYTES];
	fresh(&a, true);
	adp_set_enable(&a, true);
	check("A3 enabled with the link up: DELAY with a 0..2 s draw (5.6.3.5.2)",
	      a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_STARTUP && a.last_draw_ms <= ADP_DELAY_STARTUP_MAX_MS);
	discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
	unsigned starts = fk.starts;
	adp_rx(&a, f, sizeof f);
	check("A3 RCV_ADP_DISCOVER in DELAY is ignored (Table 5.51)", fk.starts == starts && a.discarded == 0u);
	adp_timer_expired(&a);
	discover(f, ADP_MSG_ENTITY_DISCOVER, 0x7766554433221100ull);
	adp_rx(&a, f, sizeof f);
	discover(f, ADP_MSG_ENTITY_AVAILABLE, 0);
	adp_rx(&a, f, sizeof f);
	adp_rx(&a, f, 25u);
	check_eq("A4 a foreign DISCOVER, an AVAILABLE and a truncated ADPDU are discarded (5.6.3.1)", a.discarded, 3);
	check_eq("A4 and leave WAITING alone", a.state, ADP_STATE_WAITING);
	discover(f, ADP_MSG_ENTITY_DISCOVER, entity.entity_id);
	unsigned stops = fk.stops;
	adp_rx(&a, f, sizeof f);
	check("A4 a DISCOVER for this entity stops TMR_ADVERTISE and enters DELAY (5.6.3.5.4)",
	      fk.stops == stops + 1u && a.state == ADP_STATE_DELAY && a.last_draw == ADP_DRAW_DELAY);
	adp_timer_expired(&a);
	unsigned sends = fk.sends;
	a.timer = ADP_TIMER_NONE;
	adp_timer_expired(&a);
	check_eq("A5 an expiry with no timer running is a stray, counted", a.stray_expiries, 1);
	check_eq("A5 and sends nothing", fk.sends, sends);
}

static void core_deferred(void)
{
	struct adp a;
	fresh(&a, true);
	adp_set_enable(&a, true);
	fk.room = false;
	adp_timer_expired(&a);
	check("A6 a refused send keeps ENTITY_AVAILABLE owed in DELAY",
	      a.available_owed && a.state == ADP_STATE_DELAY && a.deferred_sends == 1u);
	adp_poll(&a);
	check_eq("A6 a poll without room retries and keeps it", a.deferred_sends, 2);
	fk.room = true;
	adp_poll(&a);
	check("A6 a poll with room sends it and completes 5.6.3.5.9",
	      fk.sends == 1u && a.state == ADP_STATE_WAITING && !a.available_owed &&
		      fk.last_delay == ADP_ADVERTISE_MS);
	adp_timer_expired(&a);
	fk.room = false;
	adp_timer_expired(&a);
	adp_link_change(&a, false);
	fk.room = true;
	adp_poll(&a);
	check("A7 a link loss drops an owed ENTITY_AVAILABLE and departs nothing (5.6.3.5.10)",
	      fk.sends == 1u && a.state == ADP_STATE_DOWN && !a.available_owed && a.departing_owed == 0u);
	adp_link_change(&a, true);
	adp_timer_expired(&a);
	uint32_t index = a.available_index;
	fk.room = false;
	adp_set_enable(&a, false);
	check("A8 SHUTDOWN with no room keeps ENTITY_DEPARTING owed, index reset",
	      a.departing_owed == 1u && a.available_index == 0u && a.state == ADP_STATE_DOWN);
	adp_link_change(&a, false);
	fk.room = true;
	adp_poll(&a);
	check("A8 a link loss does not drop it; the next poll sends it with the index current at SHUTDOWN",
	      fk.last[15] == ADP_MSG_ENTITY_DEPARTING && wire_be32(fk.last + 50) == index && wire_be16(fk.last + 16) == 56u);
	unsigned sends = fk.sends;
	fk.link = false;
	adp_set_enable(&a, true);
	adp_set_enable(&a, false);
	check_eq("A8 SHUTDOWN in DOWN sends nothing (Table 5.51)", fk.sends, sends);
}

// IEEE 1722.1-2021 6.2.2.15 with Figures 6-2 and 6-3 and 6.2.5.2.2 (the
// ruling on PR #668, comment 5994972330): ENTITY_DEPARTING carries the
// CURRENT available_index, and the first ENTITY_AVAILABLE after a restart
// carries 0. Every value below is read off the frame the port was given.
static uint32_t wire_index(void)
{
	return wire_be32(fk.last + 50);
}

static bool wire_is(uint8_t msg, uint32_t index)
{
	return (fk.last[15] & 0x0Fu) == msg && wire_index() == index;
}

static void core_departing_index(void)
{
	struct adp a;
	fresh(&a, true);
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	check("A10 the first ENTITY_AVAILABLE carries 0", wire_is(ADP_MSG_ENTITY_AVAILABLE, 0));
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	check("A10 the second carries 1", wire_is(ADP_MSG_ENTITY_AVAILABLE, 1));
	check_eq("A10 SHUTDOWN is taken in WAITING", a.state, ADP_STATE_WAITING);
	adp_set_enable(&a, false);
	check("A10 SHUTDOWN in WAITING, sent at once: ENTITY_DEPARTING carries the current index, 2",
	      wire_is(ADP_MSG_ENTITY_DEPARTING, 2));
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	check("A11 the first ENTITY_AVAILABLE after a restart carries 0", wire_is(ADP_MSG_ENTITY_AVAILABLE, 0));
	adp_timer_expired(&a);
	check_eq("A12 SHUTDOWN is taken in DELAY", a.state, ADP_STATE_DELAY);
	adp_set_enable(&a, false);
	check("A12 SHUTDOWN in DELAY, sent at once: ENTITY_DEPARTING carries the current index, 1",
	      wire_is(ADP_MSG_ENTITY_DEPARTING, 1));
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	fk.room = false;
	adp_set_enable(&a, false);
	check("A13 SHUTDOWN with no room leaves ENTITY_DEPARTING owed", a.departing_owed == 1u);
	fk.room = true;
	adp_poll(&a);
	check("A13 sent from a later poll, it carries the index current at SHUTDOWN, 2",
	      wire_is(ADP_MSG_ENTITY_DEPARTING, 2));
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	check("A13 and the restart's first ENTITY_AVAILABLE carries 0", wire_is(ADP_MSG_ENTITY_AVAILABLE, 0));
	adp_timer_expired(&a);
	a.available_index = 0xFFFFFFFFu;
	adp_timer_expired(&a);
	check("A14 available_index 0xFFFFFFFF goes on the wire", wire_is(ADP_MSG_ENTITY_AVAILABLE, 0xFFFFFFFFu));
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	check("A14 the next ENTITY_AVAILABLE carries 0, modulo 2^32", wire_is(ADP_MSG_ENTITY_AVAILABLE, 0));
	adp_set_enable(&a, false);
	check("A14 SHUTDOWN after the wrap: ENTITY_DEPARTING carries the current index, 1",
	      wire_is(ADP_MSG_ENTITY_DEPARTING, 1));
}

// The frame the fake took k-th is `msg` carrying `index`.
static bool took(unsigned k, uint8_t msg, uint32_t index)
{
	return k < fk.sends && k < 16u && fk.msg[k] == msg && fk.index[k] == index;
}

// One ENTITY_AVAILABLE sent (index 0, so 1 is current), then SHUTDOWN behind
// a full transmit path: ENTITY_DEPARTING owed with index 1. Then a restart.
static void advertise_then_depart_owed(struct adp *a)
{
	fresh(a, true);
	adp_set_enable(a, true);
	adp_timer_expired(a);
	fk.room = false;
	adp_set_enable(a, false);
	adp_set_enable(a, true);
}

// R497-2-F1: an owed ENTITY_DEPARTING is never lost to a restart. It keeps
// its SHUTDOWN index and leaves before the restart's ENTITY_AVAILABLE.
static void core_owed_departing(void)
{
	struct adp a;
	advertise_then_depart_owed(&a);
	check("A15 advertised once, SHUTDOWN behind a full ring: ENTITY_DEPARTING owed with index 1",
	      took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && fk.sends == 1u && a.departing_owed == 1u && a.departing_index == 1u);
	check("A15 the restart runs while it is owed: DELAY, the startup TMR_DELAY armed",
	      a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && a.last_draw == ADP_DRAW_STARTUP);
	unsigned starts = fk.starts;
	adp_timer_expired(&a);
	check("A15 that TMR_DELAY expires before the ring has room: ENTITY_AVAILABLE owed behind it, no timer",
	      a.available_owed && a.departing_owed == 1u && a.departing_index == 1u && a.state == ADP_STATE_DELAY &&
		      a.timer == ADP_TIMER_NONE && fk.starts == starts && fk.sends == 1u);
	check("A15 a poll without room keeps both owed",
	      adp_poll(&a) && a.available_owed && a.departing_owed == 1u && fk.sends == 1u);
	fk.room = true;
	check("A15 with room, the next poll sends the owed ENTITY_DEPARTING first, with its SHUTDOWN index 1",
	      adp_poll(&a) && fk.sends == 2u && took(1, ADP_MSG_ENTITY_DEPARTING, 1));
	check("A15 and the one after it the restart's ENTITY_AVAILABLE, with index 0",
	      !adp_poll(&a) && fk.sends == 3u && took(2, ADP_MSG_ENTITY_AVAILABLE, 0));
	check("A15 then WAITING with TMR_ADVERTISE armed 5 s, available_index 1",
	      a.state == ADP_STATE_WAITING && a.timer == ADP_TIMER_ADVERTISE && fk.starts == starts + 1u &&
		      fk.last_delay == ADP_ADVERTISE_MS && a.available_index == 1u);
	check("A15 and nothing stranded: nothing owed, a further poll sends nothing",
	      !a.available_owed && a.departing_owed == 0u && !adp_poll(&a) && fk.sends == 3u);
	adp_timer_expired(&a);
	adp_timer_expired(&a);
	check("A15 the schedule runs on: the next ENTITY_AVAILABLE carries 1", fk.sends == 4u &&
	      took(3, ADP_MSG_ENTITY_AVAILABLE, 1));

	// A second SHUTDOWN while the first DEPARTING is owed queues its own.
	advertise_then_depart_owed(&a);
	adp_timer_expired(&a);
	adp_set_enable(&a, false);
	check("A16 a SHUTDOWN while one is owed queues its own ENTITY_DEPARTING and drops the owed AVAILABLE",
	      a.departing_owed == 2u && a.departing_index == 1u && !a.available_owed && a.state == ADP_STATE_DOWN);
	adp_set_enable(&a, true);
	fk.room = true;
	(void)adp_poll(&a);
	bool owed = adp_poll(&a);
	check("A16 each leaves in order with its SHUTDOWN's index: 1, then 0 (that run sent nothing)",
	      fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_DEPARTING, 0) && !owed);
	check("A16 the restart running meanwhile is untouched: DELAY, its TMR_DELAY armed",
	      a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && !a.available_owed);
	adp_timer_expired(&a);
	check("A16 its ENTITY_AVAILABLE, with index 0, leaves at its TMR_DELAY expiry; WAITING",
	      fk.sends == 4u && took(3, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING);

	// Room returns, and the restart's TMR_DELAY expires before any poll.
	advertise_then_depart_owed(&a);
	fk.room = true;
	adp_timer_expired(&a);
	check("A17 room back and TMR_DELAY expiring before a poll: the ENTITY_AVAILABLE does not pass the owed DEPARTING",
	      fk.sends == 1u && a.available_owed && a.departing_owed == 1u && a.state == ADP_STATE_DELAY);
	(void)adp_poll(&a);
	owed = adp_poll(&a);
	check("A17 the polls then send DEPARTING with index 1 and AVAILABLE with index 0, in that order",
	      fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_AVAILABLE, 0) && !owed &&
		      a.state == ADP_STATE_WAITING);
}

// R496-3-F2: the legs of the owed-frame rule (adp.h) A15 to A17 leave open.
static void core_owed_rules(void)
{
	struct adp a;
	uint8_t f[ADP_FRAME_BYTES];

	// A link loss while the restart runs, before and after its TMR_DELAY expiry.
	advertise_then_depart_owed(&a);
	adp_link_change(&a, false);
	check("A18 a link loss during the restart stops it and keeps the owed ENTITY_DEPARTING, index 1",
	      a.state == ADP_STATE_DOWN && a.timer == ADP_TIMER_NONE && a.departing_owed == 1u &&
		      a.departing_index == 1u && fk.sends == 1u);
	adp_link_change(&a, true);
	check("A18 the link's return starts a new run with the ENTITY_DEPARTING still owed (5.6.3.5.3)",
	      a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY && a.last_draw == ADP_DRAW_DELAY &&
		      a.departing_owed == 1u && a.departing_index == 1u);
	adp_timer_expired(&a);
	adp_link_change(&a, false);
	check("A18 a link loss with that run's ENTITY_AVAILABLE owed drops the AVAILABLE and keeps the DEPARTING",
	      a.state == ADP_STATE_DOWN && !a.available_owed && a.departing_owed == 1u && a.departing_index == 1u &&
		      fk.sends == 1u);
	adp_link_change(&a, true);
	fk.room = true;
	bool owed = adp_poll(&a);
	check("A18 with room the ENTITY_DEPARTING leaves, index 1", !owed && fk.sends == 2u &&
	      took(1, ADP_MSG_ENTITY_DEPARTING, 1));
	adp_timer_expired(&a);
	check("A18 then the new run's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING",
	      fk.sends == 3u && took(2, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING);

	// Inputs that leave an owed ENTITY_AVAILABLE owed: Milan v1.2 Table 5.51
	// ignores GM_CHANGE and RCV_ADP_DISCOVER in DELAY, and a stray is no input.
	fresh(&a, true);
	adp_set_enable(&a, true);
	fk.room = false;
	adp_timer_expired(&a);
	unsigned starts = fk.starts;
	adp_gm_change(&a);
	check("A19 a GM change in DELAY leaves the owed ENTITY_AVAILABLE owed, no timer started",
	      a.available_owed && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_NONE && fk.starts == starts);
	discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
	adp_rx(&a, f, sizeof f);
	check("A19 so does an ENTITY_DISCOVER",
	      a.available_owed && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_NONE && fk.starts == starts);
	adp_timer_expired(&a);
	check("A19 and a stray expiry, which is counted",
	      a.available_owed && a.stray_expiries == 1u && a.state == ADP_STATE_DELAY && fk.sends == 0u);
	fk.room = true;
	owed = adp_poll(&a);
	check("A19 the next poll with room sends it, index 0, then WAITING with TMR_ADVERTISE 5 s",
	      !owed && fk.sends == 1u && took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING &&
		      a.timer == ADP_TIMER_ADVERTISE && fk.last_delay == ADP_ADVERTISE_MS);

	// A link loss itself drops an owed ENTITY_AVAILABLE, with no poll between.
	fresh(&a, true);
	adp_set_enable(&a, true);
	fk.room = false;
	adp_timer_expired(&a);
	adp_link_change(&a, false);
	check("A20 a link loss drops the owed ENTITY_AVAILABLE at once, before any poll (5.6.3.5.10)",
	      !a.available_owed && a.state == ADP_STATE_DOWN && a.departing_owed == 0u);
	adp_link_change(&a, true);
	fk.room = true;
	owed = adp_poll(&a);
	check("A20 after the link's return a poll sends nothing: the new run waits for its TMR_DELAY (5.6.3.5.3)",
	      !owed && fk.sends == 0u && a.state == ADP_STATE_DELAY && a.timer == ADP_TIMER_DELAY &&
		      a.last_draw == ADP_DRAW_DELAY);
	adp_timer_expired(&a);
	check("A20 whose expiry sends the ENTITY_AVAILABLE, index 0; WAITING",
	      fk.sends == 1u && took(0, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING);
}

// R497-3-F1: at most ADP_DEPARTING_OWED_MAX DEPARTINGs are owed; a SHUTDOWN
// beyond them is coalesced into the queued one and counted (adp.h).
static void core_departing_capacity(void)
{
	struct adp a;
	advertise_then_depart_owed(&a);
	adp_timer_expired(&a);
	adp_set_enable(&a, false);
	check("A21 a second SHUTDOWN takes the last place: two owed, the oldest with index 1, none coalesced",
	      a.departing_owed == ADP_DEPARTING_OWED_MAX && a.departing_owed == 2u && a.departing_index == 1u &&
		      a.departing_coalesced == 0u);
	adp_set_enable(&a, true);
	adp_timer_expired(&a);
	adp_set_enable(&a, false);
	check("A21 the next SHUTDOWN is coalesced into the queued one and counted; its run's owed AVAILABLE is dropped",
	      a.departing_owed == 2u && a.departing_index == 1u && a.departing_coalesced == 1u && !a.available_owed &&
		      a.state == ADP_STATE_DOWN && fk.sends == 1u);
	for (unsigned k = 0; k < 100000u; ++k) {
		adp_set_enable(&a, true);
		adp_set_enable(&a, false);
	}
	check("A21 and so are 100000 more, each counted, the two owed unchanged",
	      a.departing_owed == 2u && a.departing_index == 1u && a.departing_coalesced == 100001u && fk.sends == 1u);
	adp_set_enable(&a, true);
	fk.room = true;
	(void)adp_poll(&a);
	bool owed = adp_poll(&a);
	check("A21 with room the wire carries DEPARTING 1, then one DEPARTING 0, and nothing more is owed",
	      fk.sends == 3u && took(1, ADP_MSG_ENTITY_DEPARTING, 1) && took(2, ADP_MSG_ENTITY_DEPARTING, 0) && !owed &&
		      !adp_poll(&a) && fk.sends == 3u);
	adp_timer_expired(&a);
	check("A21 then the running restart's ENTITY_AVAILABLE, index 0, at its TMR_DELAY expiry; WAITING",
	      fk.sends == 4u && took(3, ADP_MSG_ENTITY_AVAILABLE, 0) && a.state == ADP_STATE_WAITING);
}

static void core_draws(void)
{
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
	check("A9 every startup draw is 0..2 s and every other draw 0..4 s", in_range);
	check("A9 the two kinds are distinct: the 0..4 s draws pass 2 s", max_delay > ADP_DELAY_STARTUP_MAX_MS);
	check("A9 and both reach near their maxima", max_start > 1800u && max_delay > 3600u);
}

// ---- the adapter and the latency bounds, on the model ---------------------------

static struct mbx_model model;
static struct ctrl_app app;
static _Alignas(max_align_t) uint8_t arena[1024];
static const struct ctrl_pool_class classes[] = {{32u, 8u}};

static void boot(void)
{
	mbx_model_reset(&model);
	mbx_model_bind(&model, NULL, NULL);
	struct ctrl_app_config cfg = {&entity, 2, arena, sizeof arena, classes, 1, NULL, NULL};
	check("B0 the app starts on the model", ctrl_app_start(&app, &cfg));
}

static struct adp *adp0(void)
{
	return &app.adp.ifs[0].adp;
}

// The measured accesses of a path against its bound, printed as evidence and checked.
static void bound(const char *path, uint64_t accesses, unsigned limit)
{
	printf("  %-44s %3u accesses (bound %u)\n", path, (unsigned)accesses, limit);
	check(path, accesses <= limit);
}

// One service pass; returns its mailbox accesses.
static uint64_t pass(void)
{
	uint64_t before = model.reads + model.writes;
	(void)ctrl_loop_service(&app.loop);
	return model.reads + model.writes - before;
}

static void settle(void)
{
	while (ctrl_loop_service(&app.loop) != 0u) {
	}
}

// Run the model until the instance is in WAITING with TMR_ADVERTISE armed.
static void to_waiting(void)
{
	for (unsigned k = 0; k < 12000u && adp0()->state != ADP_STATE_WAITING; ++k) {
		mbx_model_advance_ms(&model, 1);
		settle();
	}
}

static void adapter_race(void)
{
	boot();
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	check_eq("B1 the model reaches WAITING", adp0()->state, ADP_STATE_WAITING);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms - 1u);
	mbx_model_gm_change(&model, 0, 0x5150515051505150ull, 0);
	mbx_model_advance_ms(&model, 1);
	settle();
	check_eq("B1 an expiry of the arm a GM_CHANGE replaced is discarded by its tag", app.adp.ifs[0].stale_expiries, 1);
	check("B1 and the replacing TMR_DELAY stands", adp0()->state == ADP_STATE_DELAY && app.adp.ifs[0].armed);
}

static void latency(void)
{
	uint8_t f[ADP_FRAME_BYTES];
	boot();
	mbx_model_set_link(&model, 0, true);
	uint64_t n = pass();
	check("C0 LINK_UP -> TMR_DELAY armed, one pass", adp0()->state == ADP_STATE_DELAY);
	bound("C0 LINK_UP -> TMR_DELAY armed", n, ADP_MBX_LAT_LINK);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	uint32_t sent = model.tx_sent;
	n = pass();
	check("C1 TMR_DELAY -> ENTITY_AVAILABLE committed and TMR_ADVERTISE armed, one pass",
	      model.tx_sent == sent + 1u && adp0()->state == ADP_STATE_WAITING);
	bound("C1 TMR_DELAY -> ENTITY_AVAILABLE, TMR_ADVERTISE", n, ADP_MBX_LAT_DELAY);
	discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
	(void)mbx_model_rx(&model, f, sizeof f, 0);
	n = pass();
	check("C2 RCV_ADP_DISCOVER -> TMR_DELAY armed, one pass", adp0()->state == ADP_STATE_DELAY);
	bound("C2 RCV_ADP_DISCOVER -> TMR_DELAY armed", n, ADP_MBX_LAT_DISCOVER);
	settle();
	to_waiting();
	arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	n = pass();
	check("C3 TMR_ADVERTISE -> TMR_DELAY armed, one pass", adp0()->state == ADP_STATE_DELAY);
	bound("C3 TMR_ADVERTISE -> TMR_DELAY armed", n, ADP_MBX_LAT_ADVERTISE);
	to_waiting();
	mbx_model_gm_change(&model, 0, 0x5150515051505150ull, 0);
	n = pass();
	check("C4 GM_CHANGE -> TMR_DELAY armed, one pass", adp0()->state == ADP_STATE_DELAY);
	bound("C4 GM_CHANGE -> TMR_DELAY armed", n, ADP_MBX_LAT_GM);
	mbx_model_set_link(&model, 0, false);
	n = pass();
	check("C5 LINK_DOWN -> timer cancelled, one pass", adp0()->state == ADP_STATE_DOWN && !app.adp.ifs[0].armed);
	bound("C5 LINK_DOWN -> timer cancelled", n, ADP_MBX_LAT_LINK);
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	sent = model.tx_sent;
	uint64_t before = model.reads + model.writes;
	adp_mbx_set_enable(&app.adp, false);
	n = model.reads + model.writes - before;
	check("C6 SHUTDOWN -> ENTITY_DEPARTING committed", model.tx_sent == sent + 1u);
	bound("C6 SHUTDOWN -> ENTITY_DEPARTING committed", n, ADP_MBX_LAT_SHUTDOWN);
}

// ---- a frame owed behind a full transmit ring, and a HAL that sleeps ----------------

struct waiter {
	unsigned waits;         // mbx_hal_wait() calls
	unsigned dead;          // waits no interrupt ended within 30 s
};

static struct waiter waiter;

// mbx_hal_wait() as a core that sleeps until the mailbox interrupt: model
// time runs until the line rises, for 30 s at most. A wait that reaches the
// end had no wake source.
static void wait_for_irq(void *ctx)
{
	struct waiter *w = ctx;
	w->waits++;
	for (unsigned ms = 0; ms < 30000u && !mbx_model_irq(&model); ++ms) {
		mbx_model_advance_ms(&model, 1);
	}
	w->dead += mbx_model_irq(&model) ? 0u : 1u;
}

static void pending_wake(void)
{
	boot();
	memset(&waiter, 0, sizeof waiter);
	mbx_model_bind(&model, wait_for_irq, &waiter);
	mbx_model_set_link(&model, 0, true);
	for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check_eq("E0 LINK_UP takes the machine to DELAY", adp0()->state, ADP_STATE_DELAY);
	mbx_model_tx_pause(&model, true);
	uint8_t filler[ADP_FRAME_BYTES];
	adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0, filler);
	while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {
	}
	for (unsigned k = 0; k < 8u && adp0()->deferred_sends == 0u; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check("E0 TMR_DELAY expires behind a full transmit ring: ENTITY_AVAILABLE is owed",
	      adp0()->available_owed && adp0()->state == ADP_STATE_DELAY);
	check("E0 and nothing else can wake the core: no RX, no event, TICK off",
	      !mbx_model_irq(&model) && model.tick_ctl == 0u);
	unsigned waits = waiter.waits;
	for (unsigned k = 0; k < 16u; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check_eq("E1 the loop does not sleep while a frame is owed", waiter.waits, waits);
	uint32_t sent = model.tx_sent;
	mbx_model_tx_pause(&model, false);
	uint32_t drained = model.tx_sent;
	ctrl_loop_step(&app.loop);
	const struct mbx_model_tx *t = mbx_model_tx_frame(&model, model.tx_sent - 1u);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	check("E2 once the ring drains, the next pass sends the owed ENTITY_AVAILABLE",
	      drained > sent && model.tx_sent == drained + 1u && t != NULL && t->bytes[15] == ADP_MSG_ENTITY_AVAILABLE &&
		      !adp0()->available_owed);
	check("E2 and restarts its timer: TMR_ADVERTISE armed 5 s after the frame left, the machine in WAITING",
	      t != NULL && arm->op == MBX_TMR_OP_ARM && arm->deadline_ms == t->now_ms + ADP_ADVERTISE_MS &&
		      app.adp.ifs[0].armed && adp0()->state == ADP_STATE_WAITING);
	for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check("E3 then the loop sleeps, and the TMR_ADVERTISE expiry wakes it",
	      waiter.waits > waits && waiter.dead == 0u && adp0()->state == ADP_STATE_DELAY);
	mbx_model_bind(&model, NULL, NULL);
}

// The k-th frame the model sent is `msg` carrying `index`.
static bool model_sent(uint32_t k, uint8_t msg, uint32_t index)
{
	const struct mbx_model_tx *t = mbx_model_tx_frame(&model, k);
	return t != NULL && (t->bytes[15] & 0x0Fu) == msg && wire_be32(t->bytes + 50) == index;
}

// R497-2-F1 through the mailbox driver, the model's timer and the loop.
static void owed_departing_wake(void)
{
	boot();
	memset(&waiter, 0, sizeof waiter);
	mbx_model_bind(&model, wait_for_irq, &waiter);
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	check("E4 advertised once: the first ENTITY_AVAILABLE left with index 0, the machine in WAITING",
	      model.tx_sent >= 1u && model_sent(model.tx_sent - 1u, ADP_MSG_ENTITY_AVAILABLE, 0) &&
		      adp0()->state == ADP_STATE_WAITING);
	mbx_model_tx_pause(&model, true);
	uint8_t filler[ADP_FRAME_BYTES];
	adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x0F0F0F0Fu, filler);
	while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {
	}
	adp_mbx_set_enable(&app.adp, false);
	adp_mbx_set_enable(&app.adp, true);
	check("E4 SHUTDOWN behind the full ring leaves ENTITY_DEPARTING owed with index 1; the restart arms TMR_DELAY",
	      adp0()->departing_owed == 1u && adp0()->departing_index == 1u && adp0()->state == ADP_STATE_DELAY &&
		      app.adp.ifs[0].armed);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	unsigned waits = waiter.waits;
	for (unsigned k = 0; k < 16u; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check("E4 its TMR_DELAY expires before the ring drains: ENTITY_AVAILABLE owed behind the DEPARTING, no arm",
	      adp0()->available_owed && adp0()->departing_owed == 1u && adp0()->state == ADP_STATE_DELAY &&
		      !app.adp.ifs[0].armed);
	check_eq("E4 the loop does not sleep while both are owed", waiter.waits, waits);
	mbx_model_tx_pause(&model, false);
	uint32_t drained = model.tx_sent;
	ctrl_loop_step(&app.loop);
	ctrl_loop_step(&app.loop);
	const struct mbx_model_tx *t = mbx_model_tx_frame(&model, drained + 1u);
	arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	check("E4 once the ring drains: ENTITY_DEPARTING with index 1, then ENTITY_AVAILABLE with index 0",
	      model.tx_sent == drained + 2u && model_sent(drained, ADP_MSG_ENTITY_DEPARTING, 1) &&
		      model_sent(drained + 1u, ADP_MSG_ENTITY_AVAILABLE, 0));
	check("E4 then WAITING with TMR_ADVERTISE armed 5 s after the ENTITY_AVAILABLE left",
	      t != NULL && arm->op == MBX_TMR_OP_ARM && arm->deadline_ms == t->now_ms + ADP_ADVERTISE_MS &&
		      app.adp.ifs[0].armed && adp0()->state == ADP_STATE_WAITING);
	for (unsigned k = 0; k < 8u && adp0()->state != ADP_STATE_DELAY; ++k) {
		ctrl_loop_step(&app.loop);
	}
	check("E4 nothing stranded: no frame owed, the loop sleeps, and the TMR_ADVERTISE expiry wakes it",
	      !adp0()->available_owed && adp0()->departing_owed == 0u && model.tx_sent == drained + 2u &&
		      waiter.waits > waits && waiter.dead == 0u && adp0()->state == ADP_STATE_DELAY);
	mbx_model_bind(&model, NULL, NULL);
}

// R496-3-F1 through the driver, the model's timer and the loop (adp_mbx.h,
// owed frames): `shutdowns` SHUTDOWN-and-restart pairs behind a full ring
// leave k = min(shutdowns, 2) DEPARTINGs owed ahead of the last restart's
// ENTITY_AVAILABLE. Its TMR_DELAY expiry is taken while the ring is still
// full, or once the room has returned (`room_first`). The AVAILABLE must be
// committed in pass k + 1 after the room returns, within the stated figures.
static void owed_bound(unsigned shutdowns, bool room_first)
{
	char what[192];
	unsigned k = shutdowns < ADP_DEPARTING_OWED_MAX ? shutdowns : ADP_DEPARTING_OWED_MAX;
	const char *when = room_first ? "expiry taken after the room" : "expiry taken before the room";
	boot();
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	mbx_model_tx_pause(&model, true);
	uint8_t filler[ADP_FRAME_BYTES];
	adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x0F0F0F0Fu, filler);
	while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {
	}
	for (unsigned s = 0; s < shutdowns; ++s) {
		adp_mbx_set_enable(&app.adp, false);
		adp_mbx_set_enable(&app.adp, true);
	}
	snprintf(what, sizeof what, "E5 %u SHUTDOWNs behind a full ring, %s: %u DEPARTINGs owed, the oldest index 1, "
		 "%u coalesced", shutdowns, when, k, shutdowns - k);
	check(what, adp0()->departing_owed == k && adp0()->departing_index == 1u &&
	      adp0()->departing_coalesced == shutdowns - k);
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	mbx_model_advance_ms(&model, arm->deadline_ms - model.now_ms);
	if (!room_first) {
		for (unsigned p = 0; p < 4u; ++p) {
			(void)pass();
		}
		snprintf(what, sizeof what, "E5 %u SHUTDOWNs behind a full ring, %s: the ENTITY_AVAILABLE owed behind them",
			 shutdowns, when);
		check(what, adp0()->available_owed && adp0()->state == ADP_STATE_DELAY && !app.adp.ifs[0].armed);
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
	snprintf(what, sizeof what, "E5 %u SHUTDOWNs behind a full ring, %s: the ENTITY_AVAILABLE is committed in pass "
		 "k + 1 = %u after the room returns, within ADP_MBX_OWED_PASSES", shutdowns, when, k + 1u);
	check(what, at == k + 1u && at <= ADP_MBX_OWED_PASSES);
	snprintf(what, sizeof what, "E5 %u SHUTDOWNs, %s: room to ENTITY_AVAILABLE", shutdowns, when);
	bound(what, at != 0u ? accesses : UINT64_MAX, ADP_MBX_OWED_ACCESSES);
	snprintf(what, sizeof what, "E5 %u SHUTDOWNs behind a full ring, %s: the wire carries DEPARTING 1, %sAVAILABLE 0",
		 shutdowns, when, k == 2u ? "DEPARTING 0, " : "");
	check(what, model.tx_sent == base + k + 1u && model_sent(base, ADP_MSG_ENTITY_DEPARTING, 1) &&
	      (k < 2u || model_sent(base + 1u, ADP_MSG_ENTITY_DEPARTING, 0)) &&
	      model_sent(base + k, ADP_MSG_ENTITY_AVAILABLE, 0));
	snprintf(what, sizeof what, "E5 %u SHUTDOWNs behind a full ring, %s: then WAITING, TMR_ADVERTISE armed, "
		 "nothing owed", shutdowns, when);
	check(what, adp0()->state == ADP_STATE_WAITING && app.adp.ifs[0].armed && !adp0()->available_owed &&
	      adp0()->departing_owed == 0u);
}

// ---- the bound with full backlogs (ctrl_loop.h A1 to A4, adp_mbx.h) -----------------

static unsigned ticks_seen;

static void count_tick(void)
{
	ticks_seen++;
}

static bool rx_touched;         // this pass has touched the ADP receive ring
static unsigned out_of_order;   // event-ring accesses after a receive-ring access in one pass

static void trace_order(void *ctx, bool write, uint32_t off, uint32_t value)
{
	(void)ctx;
	(void)write;
	(void)value;
	bool rx = off == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_ADP + MBX_CH_REG_RX_HEAD ||
		  off == MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_ADP + MBX_CH_REG_RX_TAIL ||
		  (off >= MBX_CH_ADP_RX_BASE && off < MBX_CH_ADP_RX_BASE + 4u * MBX_CH_ADP_RX_WORDS);
	bool evt = off == MBX_REG_EVT_HEAD || off == MBX_REG_EVT_TAIL ||
		   (off >= MBX_EVT_BASE && off < MBX_EVT_BASE + 4u * MBX_EVT_WORDS);
	rx_touched = rx_touched || rx;
	out_of_order += evt && rx_touched ? 1u : 0u;
}

static void backlog_bound(void)
{
	mbx_model_reset(&model);
	mbx_model_bind(&model, NULL, NULL);
	ctrl_loop_init(&app.loop);
	check("F0 the F0 composition with a centisecond consumer comes up",
	      adp_mbx_init(&app.adp, &entity, CTRL_APP_ADP_FIRST_SLOT, 2) && adp_mbx_attach(&app.adp, &app.loop) &&
		      ctrl_loop_add_tick(&app.loop, count_tick) && ctrl_loop_open(&app.loop, entity.entity_id));
	adp_mbx_set_enable(&app.adp, true);
	mbx_model_set_link(&model, 0, true);
	settle();
	to_waiting();
	uint8_t f[ADP_FRAME_BYTES];
	discover(f, ADP_MSG_ENTITY_DISCOVER, 0);
	(void)mbx_model_rx(&model, f, sizeof f, 0);
	settle();
	const struct mbx_model_tmr_op *arm = mbx_model_tmr_op(&model, model.tmr_ops - 1u);
	uint32_t deadline = arm->deadline_ms;

	// The backlog, posted while the loop does not run. Events: an expiry on
	// each of the 15 slots ADP does not own, then ADP's own TMR_DELAY expiry
	// (the costliest sink path) as the 16th record, which fills the ring;
	// then, once the receive ring is full too, 30 centiseconds the fabric
	// coalesces behind them. The tick is held off until then, so the 16
	// records are exactly these.
	mbx_tick_enable(false);
	for (unsigned slot = 1; slot < MBX_N_TIMERS; ++slot) {
		mbx_timer_arm(slot, 0x77u, mbx_now_ms());
	}
	mbx_model_advance_ms(&model, 0);
	mbx_model_advance_ms(&model, deadline - model.now_ms);
	uint32_t last = model.window[(MBX_EVT_BASE + 4u * ((uint32_t)(model.evt_head - 3u) & (MBX_EVT_WORDS - 1u))) / 4u];
	check("F0 the event ring is full, ADP's TMR_DELAY expiry its 16th record",
	      (uint16_t)(model.evt_head - model.evt_tail) == MBX_EVT_WORDS &&
		      mbx_field(last, MBX_EV_TIMER_W1_SLOT_LSB, MBX_EV_TIMER_W1_SLOT_WIDTH) == CTRL_APP_ADP_FIRST_SLOT);
	// Receive: the smallest ENTITY_DISCOVER the filter passes (26 bytes,
	// through entity_id) until the ring refuses one, at the rate the
	// channel's token bucket admits.
	unsigned stored = 0;
	for (unsigned k = 0; k < 100000u && model.ch[MBX_CH_ADP].rx_drop == 0u; ++k) {
		if (mbx_model_rx(&model, f, 26u, 0)) {
			stored++;
		} else if (model.ch[MBX_CH_ADP].rx_drop == 0u) {
			mbx_model_advance_ms(&model, 1);
		}
	}
	check("F0 the receive ring is full: it refuses the next frame", model.ch[MBX_CH_ADP].rx_drop == 1u);
	mbx_tick_enable(true);
	mbx_model_advance_ms(&model, 30u * MBX_TICK_MS);
	uint32_t ticks_due = model.tick_count;
	check_eq("F0 30 centiseconds wait coalesced behind the full event ring", ticks_due, 30);
	check("F0 and holds no more records than A1 assumes",
	      stored > 0u && stored <= CTRL_LOOP_RX_BACKLOG(MBX_CH_ADP_RX_WORDS));
	printf("  backlog: 16 event records, %u centiseconds, %u receive records\n", (unsigned)ticks_due, stored);

	ticks_seen = 0;
	out_of_order = 0;
	uint32_t events0 = app.loop.stats.events;
	uint32_t rx0 = app.loop.stats.rx_records;
	uint32_t sent0 = model.tx_sent;
	unsigned evt_at = 0;
	unsigned answer_at = 0;
	unsigned rx_at = 0;
	unsigned idle_at = 0;
	unsigned most_ticks = 0;
	uint64_t worst = 0;
	uint64_t total = 0;
	uint64_t answer_accesses = 0;
	uint64_t rx_accesses = 0;
	mbx_host_trace(trace_order, NULL);
	for (unsigned p = 1; p <= 64u && idle_at == 0u; ++p) {
		rx_touched = false;
		unsigned t0 = ticks_seen;
		uint64_t before = model.reads + model.writes;
		unsigned work = ctrl_loop_service(&app.loop);
		uint64_t n = model.reads + model.writes - before;
		total += n;
		worst = n > worst ? n : worst;
		most_ticks = ticks_seen - t0 > most_ticks ? ticks_seen - t0 : most_ticks;
		if (evt_at == 0u && app.loop.stats.events - events0 >= 16u) {
			evt_at = p;
		}
		if (answer_at == 0u && model.tx_sent > sent0) {
			answer_at = p;
			answer_accesses = total;
		}
		if (rx_at == 0u && app.loop.stats.rx_records - rx0 >= stored) {
			rx_at = p;
			rx_accesses = total;
		}
		if (work == 0u) {
			idle_at = p;
		}
	}
	mbx_host_trace(NULL, NULL);
	printf("  passes: events by %u, ENTITY_AVAILABLE in %u (%u accesses), receive ring by %u (%u accesses), "
	       "idle at %u; worst pass %u accesses\n",
	       evt_at, answer_at, (unsigned)answer_accesses, rx_at, (unsigned)rx_accesses, idle_at, (unsigned)worst);
	check_eq("F1 events first: no event-ring access follows a receive-ring access in a pass", out_of_order, 0);
	check("F2 all 16 event records are taken by pass CTRL_LOOP_EVT_PASSES",
	      evt_at != 0u && evt_at <= CTRL_LOOP_EVT_PASSES);
	check("F2 the TMR_DELAY expiry, posted 16th, has its ENTITY_AVAILABLE committed in the pass that takes it",
	      answer_at != 0u && answer_at <= CTRL_LOOP_EVT_PASSES && answer_at == evt_at);
	check("F2 within ADP_MBX_EVT_ACCESSES of the backlog's first access",
	      answer_at != 0u && answer_accesses <= ADP_MBX_EVT_ACCESSES);
	check("F3 the receive backlog is taken by pass ceil(records / CTRL_LOOP_RX_PER_PASS)",
	      rx_at == (stored + CTRL_LOOP_RX_PER_PASS - 1u) / CTRL_LOOP_RX_PER_PASS);
	check("F3 within CTRL_LOOP_RX_PASSES(256) passes and ADP_MBX_RX_ACCESSES accesses",
	      rx_at != 0u && rx_at <= CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) && rx_accesses <= ADP_MBX_RX_ACCESSES);
	check_eq("F4 every coalesced centisecond reaches the consumer", ticks_seen, ticks_due);
	check("F4 at most CTRL_LOOP_TICKS_PER_PASS of them in a pass", most_ticks <= CTRL_LOOP_TICKS_PER_PASS);
	bound("F5 the costliest pass of the backlog", worst, ADP_MBX_PASS_MAX);
	check("F6 the loop passes until the backlog is gone, then may sleep",
	      idle_at != 0u && idle_at > rx_at && idle_at > evt_at && app.loop.ticks_owed == 0u);
	check_eq("F7 the backlog left exactly one frame, the ENTITY_AVAILABLE", model.tx_sent, sent0 + 1u);
}

int main(void)
{
	core_schedule();
	core_discard();
	core_deferred();
	core_departing_index();
	core_owed_departing();
	core_owed_rules();
	core_departing_capacity();
	core_draws();
	adapter_race();
	latency();
	pending_wake();
	owed_departing_wake();
	static const unsigned shutdowns[] = {1u, 2u, 64u};
	for (unsigned s = 0; s < sizeof shutdowns / sizeof shutdowns[0]; ++s) {
		owed_bound(shutdowns[s], false);
		owed_bound(shutdowns[s], true);
	}
	backlog_bound();
	return check_report("ctrl ADP slice (fake ports and host model)");
}
