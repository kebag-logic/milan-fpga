// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// adp_mbx.c - the ADP slice's mailbox adapter (see adp_mbx.h).

#include "adp_mbx.h"

#include <string.h>

static struct adp_mbx_if *instance(void *ctx, unsigned interface)
{
	struct adp_mbx *m = ctx;
	return interface < MBX_N_IF ? &m->ifs[interface] : NULL;
}

static bool port_send(void *ctx, unsigned interface, const uint8_t *frame, size_t len)
{
	(void)ctx;
	return mbx_tx_send(MBX_CH_ADP, interface, frame, (uint16_t)len) == MBX_STATUS_OK;
}

static void port_timer_start(void *ctx, unsigned interface, uint32_t delay_ms)
{
	struct adp_mbx_if *i = instance(ctx, interface);
	i->tag_seq = (uint16_t)(i->tag_seq + 1u);
	i->tag = i->tag_seq;
	i->armed = true;
	mbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);
}

static void port_timer_stop(void *ctx, unsigned interface)
{
	struct adp_mbx_if *i = instance(ctx, interface);
	i->armed = false;
	mbx_timer_cancel(i->slot);
}

static void port_gptp(void *ctx, unsigned interface, uint64_t *gm_id, uint8_t *domain)
{
	(void)ctx;
	*gm_id = mbx_gm_id(interface, domain);
}

static bool port_link_up(void *ctx, unsigned interface)
{
	(void)ctx;
	return mbx_link_up(interface);
}

static uint32_t port_seed(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

bool adp_mbx_init(struct adp_mbx *m, const struct adp_entity *entity, unsigned first_slot,
		  uint16_t current_configuration_index)
{
	memset(m, 0, sizeof *m);
	if (first_slot + MBX_N_IF > MBX_N_TIMERS) {
		return false;
	}
	m->ports.ctx = m;
	m->ports.send = port_send;
	m->ports.timer_start = port_timer_start;
	m->ports.timer_stop = port_timer_stop;
	m->ports.gptp = port_gptp;
	m->ports.link_up = port_link_up;
	m->ports.seed = port_seed;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		adp_init(&m->ifs[k].adp, entity, &m->ports, k, current_configuration_index);
		m->ifs[k].slot = (uint8_t)(first_slot + k);
	}
	return true;
}

static void on_frame(void *ctx, const struct mbx_frame *f)
{
	struct adp_mbx *m = ctx;
	struct adp_mbx_if *i = instance(ctx, f->interface);
	if (i == NULL) {
		m->foreign_if++;
		return;
	}
	adp_rx(&i->adp, f->bytes, f->len);
}

static void on_timer(struct adp_mbx *m, const struct mbx_event *ev)
{
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		struct adp_mbx_if *i = &m->ifs[k];
		if (ev->timer_slot != i->slot) {
			continue;
		}
		if (!i->armed || ev->timer_tag != i->tag) {
			i->stale_expiries++;
			return;
		}
		i->armed = false;
		adp_timer_expired(&i->adp);
		return;
	}
}

static void on_event(void *ctx, const struct mbx_event *ev)
{
	struct adp_mbx *m = ctx;
	if (ev->type == MBX_EV_TYPE_TIMER) {
		on_timer(m, ev);
		return;
	}
	if (ev->type != MBX_EV_TYPE_LINK && ev->type != MBX_EV_TYPE_GM) {
		return;
	}
	struct adp_mbx_if *i = instance(ctx, ev->interface);
	if (i == NULL) {
		m->foreign_if++;
	} else if (ev->type == MBX_EV_TYPE_LINK) {
		adp_link_change(&i->adp, ev->link_up);
	} else {
		adp_gm_change(&i->adp);
	}
}

static void on_poll(void *ctx)
{
	struct adp_mbx *m = ctx;
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		adp_poll(&m->ifs[k].adp);
	}
}

bool adp_mbx_attach(struct adp_mbx *m, struct ctrl_loop *l)
{
	return ctrl_loop_bind_rx(l, MBX_CH_ADP, on_frame, m) && ctrl_loop_add_sink(l, on_event, m) &&
	       ctrl_loop_add_poll(l, on_poll, m);
}

void adp_mbx_set_enable(struct adp_mbx *m, bool enable)
{
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		adp_set_enable(&m->ifs[k].adp, enable);
	}
}
