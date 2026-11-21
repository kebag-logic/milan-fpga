// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// gptp_mbx.c - the gPTP end station ports on the mailbox and the loop (gptp_mbx.h).

#include "gptp_mbx.h"

#include <string.h>

#include "mbx_wire.h"

// the one instance the centisecond consumer (no context) serves
static struct gptp_mbx *the_gptp;

static bool hal_send(void *ctx, unsigned port, const uint8_t *frame, unsigned len)
{
	(void)ctx;
	return mbx_tx_send(MBX_CH_GPTP, port, frame, (uint16_t)len) == MBX_STATUS_OK;
}

static void hal_adjfine(void *ctx, unsigned port, int32_t addend)
{
	struct gptp_mbx *g = ctx;
	g->phc.adjfine(g->phc.ctx, port, addend);
}

static void hal_step(void *ctx, unsigned port, int64_t delta_ns)
{
	struct gptp_mbx *g = ctx;
	g->phc.step(g->phc.ctx, port, delta_ns);
}

static void on_rx(void *ctx, const struct mbx_frame *f)
{
	struct gptp_mbx *g = ctx;
	if (f->interface >= MBX_N_IF) {
		g->foreign_if++;
		return;
	}
	gptp_port_rx(&g->port[f->interface], f->bytes, f->len);
}

static void on_event(void *ctx, const struct mbx_event *ev)
{
	struct gptp_mbx *g = ctx;
	if (ev->type != MBX_EV_TYPE_TIMESTAMP && ev->type != MBX_EV_TYPE_LINK)
		return;
	if (ev->interface >= MBX_N_IF) {
		g->foreign_if++;
		return;
	}
	if (ev->type == MBX_EV_TYPE_TIMESTAMP)
		gptp_port_ts(&g->port[ev->interface], ev->ts_egress, ev->ts_msg_type, ev->ts_seq, ev->ts_ns, ev->ts_ok);
	else
		gptp_port_link(&g->port[ev->interface], ev->link_up);
}

static void on_tick(void)
{
	uint32_t now = mbx_now_ms();
	for (unsigned i = 0; i < MBX_N_IF; i++)
		gptp_port_tick(&the_gptp->port[i], now);
}

void gptp_mbx_words(const struct gptp_pub *pub, uint8_t gen, uint32_t w[MBX_PUB_GPTP_WORDS])
{
	unsigned at = 0;
	memset(w, 0, MBX_PUB_GPTP_WORDS * sizeof *w);
	w[at++] = (uint32_t)pub->gm_id;
	w[at++] = (uint32_t)(pub->gm_id >> 32);
	w[at++] = (uint32_t)pub->parent_id;
	w[at++] = (uint32_t)(pub->parent_id >> 32);
	w[at++] = (uint32_t)pub->pdelay_ns;
	w[at++] = mbx_place(pub->domain, MBX_GPTP_STATE_DOMAIN_LSB, MBX_GPTP_STATE_DOMAIN_WIDTH) |
		  mbx_place(pub->as_capable ? 1u : 0u, MBX_GPTP_STATE_AS_CAPABLE_LSB, MBX_GPTP_STATE_AS_CAPABLE_WIDTH) |
		  mbx_place(pub->sync_ok ? 1u : 0u, MBX_GPTP_STATE_SYNC_OK_LSB, MBX_GPTP_STATE_SYNC_OK_WIDTH) |
		  mbx_place(pub->slew ? 1u : 0u, MBX_GPTP_STATE_SLEW_LSB, MBX_GPTP_STATE_SLEW_WIDTH) |
		  mbx_place(pub->path_count, MBX_GPTP_STATE_PATH_COUNT_LSB, MBX_GPTP_STATE_PATH_COUNT_WIDTH) |
		  mbx_place(pub->disc, MBX_GPTP_STATE_DISC_LSB, MBX_GPTP_STATE_DISC_WIDTH) |
		  mbx_place(pub->path_gen, MBX_GPTP_STATE_PATH_GEN_LSB, MBX_GPTP_STATE_PATH_GEN_WIDTH) |
		  mbx_place(gen, MBX_GPTP_STATE_GEN_LSB, MBX_GPTP_STATE_GEN_WIDTH);
	for (unsigned e = 0; e < GPTP_PATH_MAX && at + 1u < MBX_PUB_GPTP_WORDS; e++) {
		w[at++] = (uint32_t)pub->path[e];
		w[at++] = (uint32_t)(pub->path[e] >> 32);
	}
}

static bool on_poll(void *ctx)
{
	struct gptp_mbx *g = ctx;
	for (unsigned i = 0; i < MBX_N_IF; i++) {
		uint32_t w[MBX_PUB_GPTP_WORDS];
		if (!gptp_port_pub_dirty(&g->port[i]))
			continue;
		gptp_mbx_words(gptp_port_pub(&g->port[i]), g->gen[i], w);
		if (!memcmp(w, g->words[i], sizeof w))
			continue;   // only the offset moved: nothing the datapath reads
		g->gen[i]++;
		gptp_mbx_words(gptp_port_pub(&g->port[i]), g->gen[i], w);
		mbx_pub_gptp(i, w);
		memcpy(g->words[i], w, sizeof w);
		g->published++;
	}
	return false;
}

bool gptp_mbx_attach(struct gptp_mbx *g, struct ctrl_loop *l, const struct gptp_config cfg[MBX_N_IF],
		     const struct gptp_mbx_phc *phc)
{
	struct gptp_hal hal = {g, hal_send, hal_adjfine, hal_step};
	memset(g, 0, sizeof *g);
	g->phc = *phc;
	the_gptp = g;
	for (unsigned i = 0; i < MBX_N_IF; i++)
		gptp_port_init(&g->port[i], i, &cfg[i], &hal, mbx_now_ms());
	return ctrl_loop_bind_rx(l, MBX_CH_GPTP, on_rx, g) && ctrl_loop_add_sink(l, on_event, g) &&
	       ctrl_loop_add_tick(l, on_tick) && ctrl_loop_add_poll(l, on_poll, g);
}
