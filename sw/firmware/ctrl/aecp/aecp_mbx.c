// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "aecp_mbx.h"
#include "mbx_hal.h"
#include <string.h>

static uint16_t tx_count(uint32_t reg)
{
	return (uint16_t)mbx_hal_read32(MBX_CH_BASE + MBX_CH_AECP * MBX_CH_STRIDE + reg);
}

static bool send(void *ctx, unsigned interface, const uint8_t *frame, size_t len, uint32_t cookie)
{
	struct aecp_mbx *m = ctx;
	if (m->completion_count == AECP_MBX_COMPLETIONS ||
	    mbx_tx_send(MBX_CH_AECP, interface, frame, (uint16_t)len) != MBX_STATUS_OK) {
		return false;
	}
	unsigned n = (m->completion_head + m->completion_count) % AECP_MBX_COMPLETIONS;
	m->completions[n] = (struct aecp_mbx_completion){cookie, tx_count(MBX_CH_REG_TX_HEAD)};
	++m->completion_count;
	return true;
}

static uint32_t now(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

static void timer(void *ctx, bool armed, uint32_t deadline)
{
	struct aecp_mbx *m = ctx;
	if (m->armed == armed && (!armed || m->deadline == deadline)) {
		return;
	}
	m->armed = armed;
	m->deadline = deadline;
	if (armed) {
		++m->tag;
		mbx_timer_arm(m->slot, m->tag, deadline);
	} else {
		mbx_timer_cancel(m->slot);
	}
}

static uint32_t random_value(void *ctx)
{
	struct aecp_mbx *m = ctx;
	return m->environment->random(m->environment->ctx);
}

static bool stream(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_stream_info *out)
{
	struct aecp_mbx *m = ctx;
	return m->environment->stream(m->environment->ctx, interface, type, index, out);
}

static bool avb(void *ctx, unsigned interface, uint16_t index, struct aecp_avb_info *out)
{
	struct aecp_mbx *m = ctx;
	return m->environment->avb(m->environment->ctx, interface, index, out);
}

static bool path(void *ctx, unsigned interface, uint16_t index, uint64_t *out, size_t capacity, size_t *count)
{
	struct aecp_mbx *m = ctx;
	return m->environment->path(m->environment->ctx, interface, index, out, capacity, count);
}

static bool counters(void *ctx, unsigned interface, uint16_t type, uint16_t index, struct aecp_counters *out)
{
	struct aecp_mbx *m = ctx;
	return m->environment->counters(m->environment->ctx, interface, type, index, out);
}

static void changed(void *ctx, enum aecp_change kind, uint16_t type, uint16_t index)
{
	struct aecp_mbx *m = ctx;
	m->environment->changed(m->environment->ctx, kind, type, index);
}

static void start(void *ctx, uint16_t index, bool started)
{
	struct aecp_mbx *m = ctx;
	m->environment->start(m->environment->ctx, index, started);
}

bool aecp_mbx_init(struct aecp_mbx *m, const struct aecp_config *cfg,
		   const struct aecp_ports *environment, unsigned timer_slot)
{
	memset(m, 0, sizeof *m);
	if (timer_slot >= MBX_N_TIMERS || cfg->interfaces > MBX_N_IF) {
		return false;
	}
	m->slot = timer_slot;
	m->environment = environment;
	m->ports = (struct aecp_ports){m, send, now, random_value, timer,
		stream, avb, path, counters, changed, start};
	return aecp_init(&m->core, cfg, &m->ports);
}

static void frame(void *ctx, const struct mbx_frame *f)
{
	struct aecp_mbx *m = ctx;
	aecp_rx(&m->core, f->interface, f->bytes, f->len);
}

static bool ready(void *ctx)
{
	struct aecp_mbx *m = ctx;
	return aecp_ready(&m->core);
}

static void event(void *ctx, const struct mbx_event *e)
{
	struct aecp_mbx *m = ctx;
	if (e->type == MBX_EV_TYPE_TIMER && e->timer_slot == m->slot) {
		if (!m->armed || e->timer_tag != m->tag) {
			++m->stale_expiries;
		} else {
			m->armed = false;
			(void)aecp_poll(&m->core);
		}
	}
}

static bool poll(void *ctx)
{
	struct aecp_mbx *m = ctx;
	if (m->completion_count != 0u) {
		uint16_t tail = tx_count(MBX_CH_REG_TX_TAIL);
		uint32_t observed = mbx_now_ms();
		while (m->completion_count != 0u) {
			const struct aecp_mbx_completion *c = &m->completions[m->completion_head];
			if ((uint16_t)(tail - c->end) >= 0x8000u) {
				break;
			}
			aecp_tx_complete(&m->core, c->cookie, observed);
			m->completion_head = (m->completion_head + 1u) % AECP_MBX_COMPLETIONS;
			--m->completion_count;
		}
	}
	bool busy = aecp_poll(&m->core);
	return busy || m->completion_count != 0u;
}

bool aecp_mbx_attach(struct aecp_mbx *m, struct ctrl_loop *l)
{
	if (l->rx[MBX_CH_AECP].fn != NULL || l->n_sinks == CTRL_LOOP_MAX_SINKS || l->n_polls == CTRL_LOOP_MAX_POLLS) {
		return false;
	}
	(void)ctrl_loop_add_sink(l, event, m);
	(void)ctrl_loop_add_poll(l, poll, m);
	(void)ctrl_loop_bind_rx(l, MBX_CH_AECP, frame, m);
	ctrl_loop_set_rx_ready(l, MBX_CH_AECP, ready);
	m->loop = l;
	return true;
}

void aecp_mbx_open(struct aecp_mbx *m)
{
	aecp_open(&m->core);
}
