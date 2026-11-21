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

// The record is the frame, then its trailer (mailbox.yaml, the gptp channel; KL_ctrl_split): an event message's
// ingress stamp goes to its port first, so the port holds it when the frame arrives (gptp_port_ts, ingress).
static void on_rx(void *ctx, const struct mbx_frame *f)
{
	struct gptp_mbx *g = ctx;
	if (f->interface >= MBX_N_IF) {
		g->foreign_if++;
		return;
	}
	if (f->len < GPTP_MBX_TRAILER) {
		g->rx_short++;
		return;
	}
	unsigned len = f->len - GPTP_MBX_TRAILER;
	uint64_t stamp = 0;
	for (unsigned k = 0; k < GPTP_MBX_TRAILER; k++)
		stamp = (stamp << 8) | f->bytes[len + k];
	unsigned type = 0;
	uint16_t seq = 0;
	struct gptp_port *p = &g->port[f->interface];
	// an IEEE 802.1AS event message (majorSdoId 1, messageType 0 to 3) is the one the unit stamps
	if (gptp_frame_key(f->bytes, len, &type, &seq) && type <= 3u && (f->bytes[GPTP_ETH_BYTES] >> 4) == 1u) {
		if (stamp == GPTP_MBX_NO_STAMP) {
			g->rx_unstamped++;
		} else {
			g->rx_stamped++;
			gptp_port_ts(p, false, type, seq, stamp, true);
		}
	}
	gptp_port_rx(p, f->bytes, len);
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
	if (ev->type == MBX_EV_TYPE_TIMESTAMP && !ev->ts_egress)
		g->ts_foreign++;   // a received frame's stamp rides in its record, never in an event
	else if (ev->type == MBX_EV_TYPE_TIMESTAMP)
		gptp_port_ts(&g->port[ev->interface], true, ev->ts_msg_type, ev->ts_seq, ev->ts_ns, ev->ts_ok);
	else
		gptp_port_link(&g->port[ev->interface], ev->link_up);
}

static void on_tick(void)
{
	uint32_t now = mbx_now_ms();
	for (unsigned i = 0; i < MBX_N_IF; i++)
		gptp_port_tick(&the_gptp->port[i], now);
}

_Static_assert(MBX_PUB_GPTP_WORDS == 3u, "the narrowed publication: GPTP_GM_LO, GPTP_GM_HI, GPTP_STATE");

void gptp_mbx_words(const struct gptp_pub *pub, uint8_t gen, uint32_t w[MBX_PUB_GPTP_WORDS])
{
	w[0] = (uint32_t)pub->gm_id;
	w[1] = (uint32_t)(pub->gm_id >> 32);
	w[2] = mbx_place(pub->domain, MBX_GPTP_STATE_DOMAIN_LSB, MBX_GPTP_STATE_DOMAIN_WIDTH) |
	       mbx_place(pub->as_capable ? 1u : 0u, MBX_GPTP_STATE_AS_CAPABLE_LSB, MBX_GPTP_STATE_AS_CAPABLE_WIDTH) |
	       mbx_place(pub->sync_ok ? 1u : 0u, MBX_GPTP_STATE_SYNC_OK_LSB, MBX_GPTP_STATE_SYNC_OK_WIDTH) |
	       mbx_place(pub->slew ? 1u : 0u, MBX_GPTP_STATE_SLEW_LSB, MBX_GPTP_STATE_SLEW_WIDTH) |
	       mbx_place(pub->disc, MBX_GPTP_STATE_DISC_LSB, MBX_GPTP_STATE_DISC_WIDTH) |
	       mbx_place(gen, MBX_GPTP_STATE_GEN_LSB, MBX_GPTP_STATE_GEN_WIDTH);
}

// the served propagation delay: unsigned, a negative measurement (legal noise) as 0
static uint32_t served_pdelay(int32_t ns)
{
	return ns < 0 ? 0u : (uint32_t)ns;
}

// the served path's length: none while there is no grandmaster
static unsigned served_count(const struct gptp_pub *p)
{
	return p->gm_id == 0u ? 0u : p->path_count;
}

unsigned gptp_mbx_changes(const struct gptp_pub *a, const struct gptp_pub *b)
{
	unsigned ev = 0;
	if (a->gm_id != b->gm_id || served_pdelay(a->pdelay_ns) != served_pdelay(b->pdelay_ns) ||
	    a->domain != b->domain || a->as_capable != b->as_capable)
		ev |= GPTP_MBX_AVB_INFO;
	unsigned n = served_count(a);
	if (n != served_count(b) || memcmp(a->path, b->path, n * sizeof *a->path))
		ev |= GPTP_MBX_AS_PATH;
	return ev;
}

void gptp_mbx_avb(void *ctx, unsigned interface, uint64_t *gm, uint32_t *pdelay, uint8_t *domain, bool *as_capable)
{
	const struct gptp_pub *s = gptp_mbx_snapshot(ctx, interface);
	*gm = s != NULL ? s->gm_id : 0u;
	*pdelay = s != NULL ? served_pdelay(s->pdelay_ns) : 0u;
	*domain = s != NULL ? s->domain : 0u;
	*as_capable = s != NULL && s->as_capable;
}

bool gptp_mbx_path(void *ctx, unsigned interface, uint64_t *out, size_t capacity, size_t *count)
{
	const struct gptp_pub *s = gptp_mbx_snapshot(ctx, interface);
	unsigned n = s != NULL ? served_count(s) : 0u;
	if (n > capacity)
		return false;
	for (unsigned k = 0; k < n; k++)
		out[k] = s->path[k];
	*count = n;
	return true;
}

// what a publication carries or the AECP owner answers moved (the offset and the change counters move with them)
static bool moved(const struct gptp_pub *a, const struct gptp_pub *b)
{
	return gptp_mbx_changes(a, b) != 0u || a->parent_id != b->parent_id || a->sync_ok != b->sync_ok ||
	       a->slew != b->slew || a->disc != b->disc;
}

static bool on_poll(void *ctx)
{
	struct gptp_mbx *g = ctx;
	for (unsigned i = 0; i < MBX_N_IF; i++) {
		uint32_t w[MBX_PUB_GPTP_WORDS];
		if (!gptp_port_pub_dirty(&g->port[i]))
			continue;
		const struct gptp_pub *pub = gptp_port_pub(&g->port[i]);
		if (g->snap_v[i] && !moved(pub, &g->snap[i]))
			continue;   // only the offset moved: nothing published or answered
		unsigned ev = g->snap_v[i] ? gptp_mbx_changes(&g->snap[i], pub) : (GPTP_MBX_AVB_INFO | GPTP_MBX_AS_PATH);
		g->gen[i]++;
		gptp_mbx_words(pub, g->gen[i], w);
		mbx_pub_gptp(i, w);
		g->snap[i] = *pub;
		g->snap_v[i] = true;
		g->published++;
		if (ev != 0u && g->aecp.changed != NULL) {
			g->aecp.changed(g->aecp.ctx, i, ev);
			g->notices++;
		}
	}
	return false;
}

void gptp_mbx_notify(struct gptp_mbx *g, const struct gptp_mbx_aecp *aecp)
{
	g->aecp = *aecp;
}

const struct gptp_pub *gptp_mbx_snapshot(const struct gptp_mbx *g, unsigned interface)
{
	return interface < MBX_N_IF && g->snap_v[interface] ? &g->snap[interface] : NULL;
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
