// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_adp.c - the ADP slice beyond the processor's walk (#665 lane F0):
//
//   A   the core over fake ports, the paths the mailbox cannot provoke on
//       demand: a send the port refuses (deferred, retried, dropped by a
//       link loss), a stray expiry, the firmware's own 5.6.3.1 discard
//       (the fabric filter normally spares it the work), the two draw kinds;
//   B   the mailbox adapter on the model: an expiry that raced a re-arm is
//       discarded by its tag;
//   C   the service-latency bound of every response path (adp_mbx.h), counted
//       access by access on the model, in the pass that takes the input.

#include <stdio.h>
#include <string.h>

#include "adp.h"
#include "adp_mbx.h"
#include "ctrl_app.h"
#include "mbx_model.h"
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
	check("A6 a refused send keeps ENTITY_AVAILABLE pending in DELAY",
	      a.pending == ADP_PENDING_AVAILABLE && a.state == ADP_STATE_DELAY && a.deferred_sends == 1u);
	adp_poll(&a);
	check_eq("A6 a poll without room retries and keeps it", a.deferred_sends, 2);
	fk.room = true;
	adp_poll(&a);
	check("A6 a poll with room sends it and completes 5.6.3.5.9",
	      fk.sends == 1u && a.state == ADP_STATE_WAITING && a.pending == ADP_PENDING_NONE &&
		      fk.last_delay == ADP_ADVERTISE_MS);
	adp_timer_expired(&a);
	fk.room = false;
	adp_timer_expired(&a);
	adp_link_change(&a, false);
	fk.room = true;
	adp_poll(&a);
	check("A7 a link loss drops a pending ENTITY_AVAILABLE and departs nothing (5.6.3.5.10)",
	      fk.sends == 1u && a.state == ADP_STATE_DOWN && a.pending == ADP_PENDING_NONE);
	adp_link_change(&a, true);
	adp_timer_expired(&a);
	uint32_t index = a.available_index;
	fk.room = false;
	adp_set_enable(&a, false);
	check("A8 SHUTDOWN with no room keeps ENTITY_DEPARTING pending, index reset",
	      a.pending == ADP_PENDING_DEPARTING && a.available_index == 0u && a.state == ADP_STATE_DOWN);
	adp_link_change(&a, false);
	fk.room = true;
	adp_poll(&a);
	check("A8 a link loss does not drop it; the next poll sends it with the pre-reset index",
	      fk.last[15] == ADP_MSG_ENTITY_DEPARTING && wire_be32(fk.last + 50) == index && wire_be16(fk.last + 16) == 56u);
	unsigned sends = fk.sends;
	fk.link = false;
	adp_set_enable(&a, true);
	adp_set_enable(&a, false);
	check_eq("A8 SHUTDOWN in DOWN sends nothing (Table 5.51)", fk.sends, sends);
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

int main(void)
{
	core_schedule();
	core_discard();
	core_deferred();
	core_draws();
	adapter_race();
	latency();
	return check_report("ctrl ADP slice (fake ports and host model)");
}
