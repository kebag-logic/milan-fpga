// SPDX-License-Identifier: CERN-OHL-W-2.0
// Deferred protocol delivery (#678) and response-before-notice ordering (#653).
#include "ctrl_app_aecp.h"
#include "mbx_wire.h"
#include "nvm_store.h"
#include <string.h>

_Static_assert(CTRL_APP_AECP_SLOT < MBX_N_TIMERS, "AECP needs its own timer slot");

static bool locked(void *ctx, uint64_t *owner)
{
	struct ctrl_app_aecp *c = ctx;
	return aecp_locked(&c->aecp->core, owner);
}

static void source(void *ctx, unsigned index, struct acmp_source_state *value)
{
	struct ctrl_app_aecp *c = ctx;
	c->acmp_owner->source(c->acmp_owner->ctx, index, value);
}

static void srp(void *ctx, unsigned index, const struct acmp_stream *value)
{
	struct ctrl_app_aecp *c = ctx;
	c->acmp_owner->srp(c->acmp_owner->ctx, index, value);
}

static void persist(void *ctx, unsigned index)
{
	struct ctrl_app_aecp *c = ctx;
	c->bindings |= 1u << index;
	c->acmp_owner->persist(c->acmp_owner->ctx, index);
}

static void acmp_changed(void *ctx, unsigned index)
{
	struct ctrl_app_aecp *c = ctx;
	c->input_events[index] |= 1u;
	c->acmp_owner->changed(c->acmp_owner->ctx, index);
}

static uint32_t random_value(void *ctx)
{
	struct ctrl_app_aecp *c = ctx;
	return c->environment->random(c->environment->ctx);
}

static bool stream(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_stream_info *v)
{
	struct ctrl_app_aecp *c = ctx;
	if (!c->environment->stream(c->environment->ctx, interface, type, index, v)) return false;
	if (type == 5u) {
		struct acmp_sink_view s;
		if (!acmp_view(&c->app->acmp.acmp, index, &s)) return false;
		v->bound = s.bound; v->running = s.started;
		v->stream_id = s.stream.stream_id; v->dest_mac = s.stream.dest_mac; v->vlan = s.stream.vlan_id;
		v->probing_status = (uint8_t)s.probing_status; v->acmp_status = s.acmp_status;
		// Milan Tables 5.9/5.10. Other observations retain their physical owner.
		v->flags = 0x80000000u | (s.settled ? 0x52000000u : 0u) |
			(s.talker_registered ? 0x20000000u : 0u) |
			(s.registering_failed ? 0x08000040u : 0u) |
			(s.bound ? 0x04000006u : 0u) | (s.bound && !s.started ? 8u : 0u);
		v->flags_ex = s.talker_registered ? 1u : 0u;
	}
	return true;
}

static bool avb(void *ctx, unsigned interface, uint16_t index, struct aecp_avb_info *v)
{
	struct ctrl_app_aecp *c = ctx;
	return c->environment->avb(c->environment->ctx, interface, index, v);
}

static bool path(void *ctx, unsigned interface, uint16_t index, uint64_t *v, size_t capacity, size_t *count)
{
	struct ctrl_app_aecp *c = ctx;
	return c->environment->path(c->environment->ctx, interface, index, v, capacity, count);
}

static bool counters(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_counters *v)
{
	struct ctrl_app_aecp *c = ctx;
	return c->environment->counters(c->environment->ctx, interface, type, index, v);
}

static void changed(void *ctx, enum aecp_change kind, uint16_t type, uint16_t index)
{
	struct ctrl_app_aecp *c = ctx;
	aecp_nvm_changed(c->state, kind, type, index);
	c->environment->changed(c->environment->ctx, kind, type, index);
}

static void start(void *ctx, uint16_t index, bool value)
{
	struct ctrl_app_aecp *c = ctx;
	c->start_index = index; c->start_value = value; c->start_pending = true;
}

static bool format(void *ctx, uint16_t type, uint16_t index, uint64_t value)
{
	struct ctrl_app_aecp *c = ctx;
	return c->environment->format(c->environment->ctx, type, index, value);
}

static bool deliver(void *ctx)
{
	struct ctrl_app_aecp *c = ctx;
	struct acmp *a = &c->app->acmp.acmp;
	if (c->start_pending) {
		c->start_pending = false;
		// The AECP poll precedes this poll: an expired request cannot apply late.
		if (c->aecp->core.start_pending) {
			struct acmp_sink_view old;
			bool exists = acmp_view(a, c->start_index, &old);
			// Milan 5.4.2.19/.20: an unbound input is a successful no-op.
			bool ok = exists && (!old.bound || acmp_set_started(a, c->start_index, c->start_value));
			aecp_start_done(&c->aecp->core, ok, ok && old.bound && old.started != c->start_value);
		}
	}
	bool pending = aecp_nvm_poll(c->state);
	for (unsigned n = 0; n < a->cfg.n_sinks; ++n) {
		if ((c->bindings & (1u << n)) != 0u) {
			c->bindings &= ~(1u << n);
			nvm_store_changed(NVM_G_BIND, n);
		}
		if (c->input_events[n] != 0u) {
			if (acmp_change_pending(a, n)) pending = true;
			else {
				aecp_changed(&c->aecp->core, 5, (uint16_t)n, c->input_events[n]);
				c->input_events[n] = 0;
			}
		}
	}
	return pending;
}

bool ctrl_app_compose_aecp(struct ctrl_app *app, struct ctrl_app_aecp *c, struct aecp_mbx *m,
			  const struct aecp_config *cfg, const struct aecp_ports *env, struct aecp_nvm *state)
{
	if (app->loop.rx[MBX_CH_ACMP].fn == NULL || app->loop.rx[MBX_CH_AECP].fn != NULL ||
	    app->loop.n_polls + 2u > CTRL_LOOP_MAX_POLLS) return false;
	memset(c, 0, sizeof *c);
	c->app = app; c->aecp = m; c->state = state; c->environment = env;
	c->ports = (struct aecp_ports){.ctx = c, .random = random_value, .stream = stream,
		.avb = avb, .path = path, .counters = counters, .changed = changed, .start = start, .format = format};
	if (!aecp_mbx_init(m, cfg, &c->ports, CTRL_APP_AECP_SLOT) || !aecp_mbx_attach(m, &app->loop)) return false;
	c->acmp_owner = app->acmp.acmp.env;
	c->acmp_ports = (struct acmp_env){c, locked, source, srp, persist, acmp_changed};
	app->acmp.acmp.env = &c->acmp_ports;
	(void)ctrl_loop_add_poll(&app->loop, deliver, c);
	return true;
}

bool ctrl_app_open_aecp(struct ctrl_app_aecp *c)
{
	if (!c->state->released) return false;
	uint32_t channels = 0;
	for (unsigned n = 0; n < MBX_N_CH; ++n) {
		if (c->app->loop.rx[n].fn != NULL) channels |= 1u << n;
	}
	mbx_irq_enable(mbx_place(channels, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |
		       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));
	mbx_filter_open(channels);
	aecp_mbx_open(c->aecp);
	return true;
}

void ctrl_app_aecp_changed(struct ctrl_app_aecp *c, uint16_t type, uint16_t index, unsigned events)
{
	if (type == 5u && index < c->app->acmp.acmp.cfg.n_sinks) c->input_events[index] |= (uint8_t)events;
	else aecp_changed(&c->aecp->core, type, index, events);
}
