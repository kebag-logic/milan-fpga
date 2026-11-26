// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// LD2/LD3 observations belong to the handlers that change their state.
// No tick or idle poll reads a stream, a counter window or the LED register.
#ifndef CTRL_PLAT_LEDS_EVENTS_H
#define CTRL_PLAT_LEDS_EVENTS_H

#include "ctrl_plat_io.h"
#include "ctrl_plat_leds_ports.h"

_Static_assert(ACMP_MAX_SINKS <= 32u, "LED input bitmap capacity");

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
	bool on = ctrl_plat_leds_listened(&c->aecp->core, ctrl_plat_leds_stream, index);
	c->led_outputs = (c->led_outputs & ~bit) | (on ? bit : 0u);
}

// A counter notification may include unrelated counters. Only its input's
// lock pair, or domain zero's pair, is read; failed observations clear it.
static void leds_counters(struct ctrl_app_aecp *c, uint16_t type, uint16_t index)
{
	if (type == CTRL_PLAT_LEDS_STREAM_INPUT && index < c->app->acmp.acmp.cfg.n_sinks && index < 32u) {
		uint32_t bit = 1u << index;
		bool on = ctrl_plat_leds_locked(&c->aecp->core, ctrl_plat_leds_counter_pair, type, index);
		c->led_media = (c->led_media & ~bit) | (on ? bit : 0u);
	} else if (type == CTRL_PLAT_LEDS_CLOCK_DOMAIN && index == 0u) {
		c->led_domain_locked = ctrl_plat_leds_locked(&c->aecp->core, ctrl_plat_leds_counter_pair, type, index);
	} else if (type == CTRL_PLAT_LEDS_STREAM_OUTPUT) {
		leds_output(c, index);
	}
}

// Bootstrap after restore/open and rebuild after SET_CONFIGURATION. These
// transitions can replace every descriptor, so they alone observe all of them.
static void leds_refresh(struct ctrl_app_aecp *c)
{
	c->led_media = 0u;
	c->led_enabled = 0u;
	c->led_outputs = 0u;
	for (uint16_t n = 0u; n < c->app->acmp.acmp.cfg.n_sinks; ++n) {
		leds_input(c, n);
		leds_counters(c, CTRL_PLAT_LEDS_STREAM_INPUT, n);
	}
	for (uint16_t n = 0u; n < c->app->acmp.acmp.cfg.n_sources; ++n) leds_output(c, n);
	leds_counters(c, CTRL_PLAT_LEDS_CLOCK_DOMAIN, 0u);
	leds_publish(c);
}

#endif
