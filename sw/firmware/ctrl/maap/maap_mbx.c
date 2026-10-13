// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "maap_mbx.h"

#include <string.h>

static bool send_frame(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx;
	return mbx_tx_send(MBX_CH_MAAP, interface, frame, (uint16_t)len) == MBX_STATUS_OK;
}

static void arm(void *ctx, unsigned interface, uint32_t delay_ms)
{
	struct maap_mbx *m = ctx;
	struct maap_mbx_if *i = &m->ifs[interface];
	i->tag++;
	i->armed = true;
	mbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);
}

static void cancel(void *ctx, unsigned interface)
{
	struct maap_mbx *m = ctx;
	struct maap_mbx_if *i = &m->ifs[interface];
	i->armed = false;
	mbx_timer_cancel(i->slot);
}

static uint32_t clock_ms(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

static void refresh_demand(struct maap_mbx *m)
{
	m->demand = 0u;
	if (m->acmp != NULL) {
		for (unsigned s = 0; s < m->acmp->cfg.n_sources; ++s) {
			// Retire observed expiry in the core, even while its source owner
			// has no destination. Only the dispatch path may call a core.
			(void)acmp_declaring(m->acmp, s);
			const struct acmp_source *source = &m->acmp->sources[s];
			if (source->answered || source->listener_registered) {
				m->demand |= UINT32_C(1) << s;
			}
		}
	}
}

static uint32_t declaring(const struct maap_mbx *m, unsigned interface, uint16_t count, bool valid)
{
	uint32_t gate = 0u;
	if (m->acmp != NULL) {
		for (unsigned s = 0; s < m->acmp->cfg.n_sources; ++s) {
			bool demand = (m->demand & (UINT32_C(1) << s)) != 0u;
			if (m->acmp->cfg.source_interface[s] == interface && valid && s < count && demand) {
				gate |= UINT32_C(1) << s;
			}
		}
	}
	return gate;
}

void maap_mbx_bind_acmp(struct maap_mbx *m, struct acmp *acmp)
{
	m->acmp = acmp;
}

static void range(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid)
{
	struct maap_mbx *m = ctx;
	// The current contract has one range filter. For multiple interfaces use
	// the envelope of live ranges; the indexed cores reject disjoint input.
	uint64_t first = MAAP_POOL_BASE + MAAP_POOL_SIZE;
	uint64_t last = MAAP_POOL_BASE;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		const struct maap *core = &m->ifs[k].core;
		uint16_t n = k == interface ? count : (core->state == MAAP_INITIAL ? 0u : core->count);
		if (n != 0u) {
			uint64_t start = k == interface ? base : core->base;
			if (start < first) {
				first = start;
			}
			if (start + n > last) {
				last = start + n;
			}
		}
	}
	mbx_filter_set_maap_range(first, last > first ? (uint16_t)(last - first) : 0u);
	// The datapath's talker DA gate (the publication block), before the
	// allocation is reported: source s holds address base + s while the range
	// is valid and ACMP has fresh probe or registered Listener demand
	// (Milan v1.2 4.3.3.1).
	// count never exceeds the entity's talker sources, which the publication
	// block holds (maap_mbx_init).
	m->published_gate[interface] = declaring(m, interface, count, valid);
	(void)mbx_pub_da_gate(interface, m->published_gate[interface]);
	m->allocation(m->allocation_ctx, interface, base, count, valid);
}

bool maap_mbx_init(struct maap_mbx *m, const uint64_t mac[MBX_N_IF], uint16_t count,
		   unsigned first_slot, maap_allocation_fn allocation, void *ctx)
{
	memset(m, 0, sizeof *m);
	if (first_slot > MBX_N_TIMERS - MBX_N_IF || allocation == NULL || count > MBX_N_PUB_SOURCES) {
		return false;
	}
	m->ports = (struct maap_ports){m, send_frame, arm, cancel, range, clock_ms};
	m->allocation = allocation;
	m->allocation_ctx = ctx;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		if (!maap_init(&m->ifs[k].core, &m->ports, k, mac[k], count)) {
			return false;
		}
		m->ifs[k].slot = (uint8_t)(first_slot + k);
	}
	return true;
}

static void receive(void *ctx, const struct mbx_frame *f)
{
	struct maap_mbx *m = ctx;
	if (f->interface >= MBX_N_IF) {
		m->foreign_if++;
		return;
	}
	refresh_demand(m);
	maap_rx(&m->ifs[f->interface].core, f->bytes, f->len);
}

static void event(void *ctx, const struct mbx_event *ev)
{
	struct maap_mbx *m = ctx;
	if (ev->type == MBX_EV_TYPE_TIMER) {
		for (unsigned k = 0; k < MBX_N_IF; ++k) {
			struct maap_mbx_if *i = &m->ifs[k];
			if (ev->timer_slot != i->slot) {
				continue;
			}
			if (!i->armed || ev->timer_tag != i->tag) {
				i->stale_expiries++;
				return;
			}
			i->armed = false;
			refresh_demand(m);
			maap_timer_expired(&i->core);
			return;
		}
	} else if (ev->type == MBX_EV_TYPE_LINK) {
		if (ev->interface >= MBX_N_IF) {
			m->foreign_if++;
			return;
		}
		struct maap_mbx_if *i = &m->ifs[ev->interface];
		if (i->link != ev->link_up) {
			i->link = ev->link_up;
			refresh_demand(m);
			maap_port_operational(&i->core, i->link);
		}
	}
}

static bool poll(void *ctx)
{
	struct maap_mbx *m = ctx;
	bool owed = false;
	refresh_demand(m);
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		owed = maap_poll(&m->ifs[k].core) || owed;
		const struct maap *core = &m->ifs[k].core;
		uint32_t gate = declaring(m, k, core->count, core->valid);
		if (gate != m->published_gate[k]) {
			m->published_gate[k] = gate;
			(void)mbx_pub_da_gate(k, gate);
		}
	}
	return owed;
}

bool maap_mbx_attach(struct maap_mbx *m, struct ctrl_loop *loop)
{
	// Check room before any binding, so a refusal cannot half-attach a core.
	if (loop->n_sinks >= CTRL_LOOP_MAX_SINKS || loop->n_polls >= CTRL_LOOP_MAX_POLLS ||
	    loop->rx[MBX_CH_MAAP].fn != NULL) {
		return false;
	}
	(void)ctrl_loop_bind_rx(loop, MBX_CH_MAAP, receive, m);
	(void)ctrl_loop_add_sink(loop, event, m);
	(void)ctrl_loop_add_poll(loop, poll, m);
	return true;
}

bool maap_mbx_start(struct maap_mbx *m, uint64_t preferred)
{
	bool ok = true;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		m->ifs[k].link = mbx_link_up(k);
		maap_port_operational(&m->ifs[k].core, m->ifs[k].link);
		if (!maap_begin(&m->ifs[k].core, preferred)) {
			ok = false;
		}
	}
	return ok;
}

void maap_mbx_stop(struct maap_mbx *m)
{
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		maap_release(&m->ifs[k].core);
	}
}
