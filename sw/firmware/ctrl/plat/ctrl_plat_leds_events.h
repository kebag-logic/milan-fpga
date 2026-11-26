// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// LD2/LD3 observations belong to the handlers that change their state.
// No tick or idle poll reads a stream, a counter window or the LED register.
#ifndef CTRL_PLAT_LEDS_EVENTS_H
#define CTRL_PLAT_LEDS_EVENTS_H

#include "ctrl_plat_io.h"
#include "ctrl_plat_leds_ports.h"

_Static_assert(ACMP_MAX_SINKS <= 32u, "LED input bitmap capacity");
_Static_assert(ACMP_MAX_SOURCES <= 32u, "LED output bitmap capacity");

static void leds_retry_mark(struct ctrl_app_aecp *c, bool failed)
{
	bool pending = c->led_retry_pending;
	c->led_retry_pending = c->led_retry_inputs != 0u || c->led_retry_outputs != 0u || c->led_retry_domain;
	if (failed && !pending) c->led_retry_at = c->aecp->core.now + 250u;
}

static void leds_publish(struct ctrl_app_aecp *c)
{
	uint32_t word = ctrl_plat_leds_state_word(&c->aecp->core, c->led_media & c->led_enabled,
					       c->led_outputs, c->led_domain_locked);
	if (word != c->led_word) {
		c->led_word = word;
		ctrl_plat_io_write32(CTRL_PLAT_LEDS, word);
	}
}

// ACMP's change callback runs after bind/unbind and start/stop. Media lock
// can precede a binding; keep it independently until a counter event changes it.
static void leds_input(struct ctrl_app_aecp *c, unsigned index)
{
	if (index >= c->app->acmp.acmp.cfg.n_sinks || index >= 32u) return;
	const struct acmp_sink *s = &c->app->acmp.acmp.sinks[index];
	uint32_t bit = 1u << index;
	c->led_enabled = (c->led_enabled & ~bit) | (s->bound && s->started ? bit : 0u);
}

// Listener changes and declaration/withdrawal share SRP's existing delivery
// handler. Undeclared outputs retain the fabric's GET_STREAM_INFO owner.
static void leds_output(struct ctrl_app_aecp *c, uint16_t index)
{
	if (index >= c->app->acmp.acmp.cfg.n_sources || index >= 32u) return;
	uint32_t bit = 1u << index;
	struct aecp_stream_info s;
	s.flags_ex = 0u;
	s.brief = false;
	bool answered = ctrl_plat_leds_stream(c->aecp->core.ports->ctx, 0u, CTRL_PLAT_LEDS_STREAM_OUTPUT, index, &s);
	bool on = answered && (s.flags_ex & 1u) != 0u;
	c->led_outputs = (c->led_outputs & ~bit) | (on ? bit : 0u);
	c->led_retry_outputs = (c->led_retry_outputs & ~bit) | (!answered ? bit : 0u);
	leds_retry_mark(c, !answered);
}

// A counter notification may include unrelated counters. Only its input's
// lock pair, or domain zero's pair, is read; failed observations clear it.
static void leds_counters(struct ctrl_app_aecp *c, uint16_t type, uint16_t index)
{
	if (type == CTRL_PLAT_LEDS_STREAM_INPUT && index < c->app->acmp.acmp.cfg.n_sinks && index < 32u) {
		uint32_t bit = 1u << index;
		bool answered = false;
		bool on = ctrl_plat_leds_lock_state(&c->aecp->core, ctrl_plat_leds_counter_pair, type, index, &answered);
		c->led_media = (c->led_media & ~bit) | (on ? bit : 0u);
		c->led_retry_inputs = (c->led_retry_inputs & ~bit) | (!answered ? bit : 0u);
		leds_retry_mark(c, !answered);
	} else if (type == CTRL_PLAT_LEDS_CLOCK_DOMAIN && index == 0u) {
		bool answered = false;
		c->led_domain_locked = ctrl_plat_leds_lock_state(&c->aecp->core, ctrl_plat_leds_counter_pair, type, index, &answered);
		c->led_retry_domain = !answered;
		leds_retry_mark(c, !answered);
	} else if (type == CTRL_PLAT_LEDS_STREAM_OUTPUT) {
		leds_output(c, index);
	}
}

// Continue a failed state-change observation, one descriptor per 250 ms.
// The retry clock is the core's existing time observation. Healthy idle
// service does no read. A stuck window cannot turn this into an idle scan.
static void leds_retry(struct ctrl_app_aecp *c)
{
	if (!c->led_retry_pending || (int32_t)(c->aecp->core.now - c->led_retry_at) < 0) return;
	c->led_retry_at = c->aecp->core.now + 250u;
	unsigned inputs = c->app->acmp.acmp.cfg.n_sinks;
	unsigned count = 1u + inputs + c->app->acmp.acmp.cfg.n_sources;
	for (unsigned n = 0u; n < count; ++n) {
		unsigned at = c->led_retry_cursor++;
		if (c->led_retry_cursor >= count) c->led_retry_cursor = 0u;
		if (at == 0u && c->led_retry_domain) {
			leds_counters(c, CTRL_PLAT_LEDS_CLOCK_DOMAIN, 0u);
			break;
		} else if (at > 0u && at <= inputs && (c->led_retry_inputs & (1u << (at - 1u))) != 0u) {
			leds_counters(c, CTRL_PLAT_LEDS_STREAM_INPUT, (uint16_t)(at - 1u));
			break;
		} else if (at > inputs && (c->led_retry_outputs & (1u << (at - inputs - 1u))) != 0u) {
			leds_output(c, (uint16_t)(at - inputs - 1u));
			break;
		}
	}
	leds_publish(c);
}

// Bootstrap after restore/open and rebuild after SET_CONFIGURATION. These
// transitions can replace every descriptor, so they alone observe all of them.
static void leds_refresh(struct ctrl_app_aecp *c)
{
	c->led_media = 0u;
	c->led_enabled = 0u;
	c->led_outputs = 0u;
	c->led_retry_inputs = 0u;
	c->led_retry_outputs = 0u;
	c->led_retry_domain = false;
	for (uint16_t n = 0u; n < c->app->acmp.acmp.cfg.n_sinks; ++n) {
		leds_input(c, n);
		leds_counters(c, CTRL_PLAT_LEDS_STREAM_INPUT, n);
	}
	for (uint16_t n = 0u; n < c->app->acmp.acmp.cfg.n_sources; ++n) leds_output(c, n);
	leds_counters(c, CTRL_PLAT_LEDS_CLOCK_DOMAIN, 0u);
	leds_publish(c);
}

#endif
