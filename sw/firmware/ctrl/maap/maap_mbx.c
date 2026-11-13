// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "maap_mbx.h"

#include <string.h>

#include "../plat/ctrl_cc.h"

// sid_written and sid_wait hold a bit per source the publication block holds;
// a gate opens no other source, since its count never exceeds them (#905).
_Static_assert(MBX_N_PUB_SOURCES <= 16u, "a source's SRC_SID mark needs its bit");

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
			// The owner supplies per-source destination validity and retires
			// observed probe expiry. Only dispatch may call a protocol core.
			if (acmp_declaring(m->acmp, s)) {
				m->demand |= UINT32_C(1) << s;
			}
		}
	}
}

// A closed source opens only once its SRC_SID is written since it last
// opened, by the start or the poll (#905): each it holds for that waits in
// sid_wait for the poll, and each it lets open spends its written mark. Every
// caller publishes the gate it returns.
static uint32_t declaring(struct maap_mbx *m, unsigned interface, uint16_t count, bool valid)
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
	uint32_t may = gate & (m->published_gate[interface] | m->sid_written);
	m->sid_wait[interface] = (uint16_t)(gate & ~may);
	m->sid_written &= (uint16_t)~may;
	return may;
}

// Source s's stream_id as the declaration owner's source port reports it, the
// port acmp_declaring reads: the ID its Talker declares and ACMP answers with
// (Milan v1.2 5.3.7.5), which the datapath stamps on its frames (KL_mbx_pkg.sv
// SRC_SID_LO; #905).
static uint64_t stream_of(const struct maap_mbx *m, unsigned s)
{
	struct acmp_source_state st;
	memset(&st, 0, sizeof st);
	m->acmp->env->source(m->acmp->env->ctx, s, &st);
	return st.stream.stream_id;
}

// Whether interface k's poll owes a SRC_SID word: one source's are in flight
// at a time, so the high word owed, when its source is k's, or else, with none
// owed, the low word of a source k's gate holds (#905).
static bool sid_owed(const struct maap_mbx *m, unsigned k)
{
	unsigned s = m->sid_half;
	return s != 0u ? m->acmp->cfg.source_interface[s - 1u] == k : m->sid_wait[k] != 0u;
}

// One word of a waiting source's SRC_SID, read from its port, the low word
// first, in an interface's poll that writes no DA_GATE: its one publication
// write (maap_mbx.h), on the source's own interface. The source's DA_GATE bit
// stays clear until both are written, so no frame carries a half-written
// stream_id, and none a stream_id its port no longer reports (KL_mbx_pkg.sv
// SRC_SID_LO; #905).
static CTRL_CC_NOINLINE void publish_sid(struct maap_mbx *m, unsigned k)
{
	unsigned s = m->sid_half;
	if (s != 0u) {
		--s;
		(void)mbx_pub_src_sid(k, s, true, m->sid_high);
		m->sid_written |= (uint16_t)(UINT32_C(1) << s);
		m->sid_half = 0u;
		return;
	}
	while ((m->sid_wait[k] >> s & 1u) == 0u) {
		++s;
	}
	uint64_t id = stream_of(m, s);
	(void)mbx_pub_src_sid(k, s, false, (uint32_t)id);
	m->sid_high = (uint32_t)(id >> 32);
	m->sid_half = (uint8_t)(s + 1u);
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
	// is valid and ACMP's cached per-source declaration predicate holds
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
		} else if (sid_owed(m, k)) {
			// A waiting SRC_SID is work owed: the next passes write it,
			// and the one after its last word opens the gate (#905)
			publish_sid(m, k);
			owed = true;
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
	// Every source's SRC_SID first: no DA_GATE bit has opened since init and
	// no pass has run, so each is written before its gate opens and before any
	// declaration or PROBE_TX response that carries it (KL_mbx_pkg.sv; #905)
	if (m->acmp != NULL) {
		for (unsigned s = 0; s < m->acmp->cfg.n_sources; ++s) {
			uint64_t id = stream_of(m, s);
			unsigned k = m->acmp->cfg.source_interface[s];
			(void)mbx_pub_src_sid(k, s, false, (uint32_t)id);
			(void)mbx_pub_src_sid(k, s, true, (uint32_t)(id >> 32));
			m->sid_written |= (uint16_t)(UINT32_C(1) << s);
		}
	}
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
