// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_mbx.c - the ACMP module's mailbox adapter (see acmp_mbx.h).

#include "acmp_mbx.h"

#include <string.h>

// The interfaces' slots fit the bank, so MBX_N_TIMERS - MBX_N_IF cannot wrap;
// and sink k is entry k of its interface's bound-talker table, which holds as
// many entries as the core has sinks (the contract's bound_talkers).
_Static_assert(MBX_N_TIMERS >= MBX_N_IF, "every interface needs a timer slot");
_Static_assert(ACMP_MAX_SINKS <= MBX_N_BOUND, "every sink needs a bound-talker entry");
_Static_assert(ACMP_MAX_SINKS <= MBX_N_PUB_SINKS, "every sink needs a publication entry");

static bool port_send(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx;
	return mbx_tx_send(MBX_CH_ACMP, interface, frame, (uint16_t)len) == MBX_STATUS_OK;
}

static uint32_t port_now(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

// The core calls this for an interface of its configuration, which
// acmp_mbx_init held to the mailbox's.
static void port_timer(void *ctx, unsigned interface, bool armed, uint32_t deadline_ms)
{
	struct acmp_mbx *m = ctx;
	struct acmp_mbx_if *i = &m->ifs[interface];
	i->armed = armed;
	if (!armed) {
		mbx_timer_cancel(i->slot);
		return;
	}
	i->tag_seq = (uint16_t)(i->tag_seq + 1u);
	i->tag = i->tag_seq;
	mbx_timer_arm(i->slot, i->tag, deadline_ms);
}

static void port_gptp(void *ctx, unsigned interface, uint64_t *gm_id, uint8_t *domain)
{
	(void)ctx;
	*gm_id = mbx_gm_id(interface, domain);
}

static uint32_t port_seed(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

// Sink k is entry k of its interface's bound-talker table; the sinks fit the
// table (above) and acmp_mbx_init held the interfaces to the mailbox's, so the
// driver's refusal never applies.
static void port_admit(void *ctx, unsigned interface, unsigned sink, bool bound, uint64_t talker_entity_id)
{
	(void)ctx;
	(void)mbx_filter_set_bound_talker(interface, sink, bound, talker_entity_id);
}

// Sink k is entry k of its interface's publication block, as of its
// bound-talker table: the sinks fit (above) and the interfaces are the
// mailbox's, so the driver's refusal never applies. A stream_id that did not
// move is not rewritten: BINDING alone carries the bound or started move, and
// SID_VALID stays as it was, so the stream never leaves the datapath.
static void port_publish(void *ctx, unsigned interface, unsigned sink, bool bound, bool started, uint64_t stream_id,
			 bool stream_moved)
{
	(void)ctx;
	if (stream_moved) {
		(void)mbx_pub_sink(interface, sink, bound, started, stream_id);
	} else {
		(void)mbx_pub_sink_binding(interface, sink, bound, started, stream_id != 0u);
	}
}

bool acmp_mbx_init(struct acmp_mbx *m, const struct acmp_config *cfg, const struct acmp_env *env,
		   unsigned first_slot)
{
	memset(m, 0, sizeof *m);
	// first_slot is compared, never added to: no sum can wrap and no slot is
	// narrowed into uint8_t until it is known to be one
	if (first_slot > MBX_N_TIMERS - MBX_N_IF || cfg->n_interfaces > MBX_N_IF) {
		return false;
	}
	m->ports.ctx = m;
	m->ports.send = port_send;
	m->ports.now_ms = port_now;
	m->ports.timer = port_timer;
	m->ports.gptp = port_gptp;
	m->ports.seed = port_seed;
	m->ports.admit = port_admit;
	m->ports.publish = port_publish;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		m->ifs[k].slot = (uint8_t)(first_slot + k);
	}
	struct acmp_config config = *cfg;
	// Milan v1.2 4.3.3.1: the mailbox placement uses T-SRP-DAFRESH.
	config.da_fresh_ms = 15000u;
	return acmp_init(&m->acmp, &config, &m->ports, env);
}

// THE KEPT COMMAND (acmp_mbx.h). A record the core declines is kept whole: the
// driver refuses a record longer than the channel's MBX_CH_ACMP_MAX_FRAME_BYTES
// (mbx_rx_take), which is the buffer's size.
static void on_frame(void *ctx, const struct mbx_frame *f)
{
	struct acmp_mbx *m = ctx;
	if (acmp_rx(&m->acmp, f->interface, f->bytes, f->len)) {
		return;
	}
	memcpy(m->kept.frame, f->bytes, f->len);
	m->kept.len = f->len;
	m->kept.interface = f->interface;
}

// While a command is kept no later record of the acmp ring is taken, so the
// commands keep their arrival order (tsn-c-stack ACMP-12).
static bool on_rx_ready(void *ctx)
{
	const struct acmp_mbx *m = ctx;
	return m->kept.len == 0u;
}

static void on_event(void *ctx, const struct mbx_event *ev)
{
	struct acmp_mbx *m = ctx;
	if (ev->type != MBX_EV_TYPE_TIMER) {
		return;
	}
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		struct acmp_mbx_if *i = &m->ifs[k];
		if (ev->timer_slot != i->slot) {
			continue;
		}
		if (!i->armed || ev->timer_tag != i->tag) {
			i->stale_expiries++;
			return;
		}
		i->armed = false;
		acmp_timer_expired(&m->acmp, k);
		return;
	}
}

// THE KEPT COMMAND's redelivery (acmp_mbx.h): the kept record first, then the
// records waiting in the acmp ring in arrival order, each to acmp_rx until it
// declines one, which is kept, or none is left; at most
// ACMP_MBX_REDELIVER_RECORDS taken, in the loop's buffer and counted as the
// loop counts its own. A record the driver refuses resynchronises the ring
// (mbx_rx_take), so none is left after it.
static void redeliver(struct acmp_mbx *m)
{
	if (m->kept.len != 0u) {
		if (!acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {
			return;
		}
		m->kept.len = 0u;
	}
	struct ctrl_loop *l = m->loop;
	for (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {
		const enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);
		if (st != MBX_STATUS_OK) {
			l->stats.rx_bad += st == MBX_STATUS_BAD;
			return;
		}
		l->stats.rx_records++;
		on_frame(m, &l->frame);
	}
}

// One owed frame sent when the egress has room; once that send freed a slot
// the redelivery runs, in this pass, so before the next pass's timer service
// (tsn-c-stack ACMP-12). True while a frame is still owed, so the loop does
// not sleep on it; a kept command is declined only behind owed frames.
static bool on_poll(void *ctx)
{
	struct acmp_mbx *m = ctx;
	const unsigned owed = m->acmp.owed_count;
	(void)acmp_poll(&m->acmp);
	if (m->acmp.owed_count < owed) {
		redeliver(m);
	}
	return m->acmp.owed_count != 0u;
}

// Each ADP record to the module that acts on it: an ENTITY_AVAILABLE or
// ENTITY_DEPARTING to the listener's discovery (Milan v1.2 5.6.4.1), anything
// else to the handler that was bound before the tap (F0's ADP adapter). The
// record's buffer holds MBX_FRAME_BYTES_MAX bytes, so its message_type byte
// is always there to read; a record too short to carry it is refused by the
// module it reaches (acmp_adp_rx, adp_rx), whichever that is.
static void on_adp_frame(void *ctx, const struct mbx_frame *f)
{
	struct acmp_mbx *m = ctx;
	if ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) <= ACMP_ADP_MSG_ENTITY_DEPARTING) {
		acmp_adp_rx(&m->acmp, f->interface, f->bytes, f->len);
		return;
	}
	m->adp_next.fn(m->adp_next.ctx, f);
}

void acmp_mbx_open(struct acmp_mbx *m)
{
	acmp_open(&m->acmp);
}

bool acmp_mbx_attach(struct acmp_mbx *m, struct ctrl_loop *l)
{
	if (l->rx[MBX_CH_ADP].fn == NULL || !ctrl_loop_add_sink(l, on_event, m) || !ctrl_loop_add_poll(l, on_poll, m)) {
		return false;
	}
	m->adp_next = l->rx[MBX_CH_ADP];
	m->loop = l;
	// a channel bind refuses only a channel past MBX_N_CH or no function:
	// neither here
	(void)ctrl_loop_bind_rx(l, MBX_CH_ACMP, on_frame, m);
	ctrl_loop_set_rx_ready(l, MBX_CH_ACMP, on_rx_ready);
	(void)ctrl_loop_bind_rx(l, MBX_CH_ADP, on_adp_frame, m);
	return true;
}
