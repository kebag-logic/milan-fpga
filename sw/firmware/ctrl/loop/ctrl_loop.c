// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_loop.c - the bare-metal event loop (see ctrl_loop.h).

#include "ctrl_loop.h"

#include <string.h>

#include "mbx_hal.h"
#include "mbx_wire.h"

void ctrl_loop_init(struct ctrl_loop *l)
{
	memset(l, 0, sizeof *l);
}

bool ctrl_loop_bind_rx(struct ctrl_loop *l, unsigned ch, ctrl_rx_fn fn, void *ctx)
{
	if (ch >= MBX_N_CH || fn == NULL) {
		return false;
	}
	l->rx[ch].fn = fn;
	l->rx[ch].ctx = ctx;
	return true;
}

void ctrl_loop_set_rx_ready(struct ctrl_loop *l, unsigned ch, bool (*ready)(void *ctx))
{
    if (ch < MBX_N_CH) {
        l->rx[ch].ready = ready;
    }
}

bool ctrl_loop_add_sink(struct ctrl_loop *l, ctrl_event_fn fn, void *ctx)
{
	if (l->n_sinks >= CTRL_LOOP_MAX_SINKS || fn == NULL) {
		return false;
	}
	l->sinks[l->n_sinks].fn = fn;
	l->sinks[l->n_sinks].ctx = ctx;
	l->n_sinks++;
	return true;
}

bool ctrl_loop_add_tick(struct ctrl_loop *l, ctrl_tick_fn fn)
{
	if (l->n_ticks >= CTRL_LOOP_MAX_TICKS || fn == NULL) {
		return false;
	}
	l->ticks[l->n_ticks++] = fn;
	return true;
}

bool ctrl_loop_add_poll(struct ctrl_loop *l, ctrl_poll_fn fn, void *ctx)
{
	if (l->n_polls >= CTRL_LOOP_MAX_POLLS || fn == NULL) {
		return false;
	}
	l->polls[l->n_polls].fn = fn;
	l->polls[l->n_polls].ctx = ctx;
	l->n_polls++;
	return true;
}

bool ctrl_loop_set_step(struct ctrl_loop *l, ctrl_step_fn fn, void *ctx, ctrl_clock_fn clock, void *clock_ctx)
{
	if (l->step != NULL || fn == NULL || clock == NULL) {
		return false;
	}
	l->step = fn;
	l->step_ctx = ctx;
	l->clock = clock;
	l->clock_ctx = clock_ctx;
	return true;
}

bool ctrl_loop_set_retry(struct ctrl_loop *l, ctrl_retry_fn fn, ctrl_retry_aged_fn aged, void *ctx)
{
	if (l->retry != NULL || fn == NULL || aged == NULL) {
		return false;
	}
	l->retry = fn;
	l->retry_aged = aged;
	l->retry_ctx = ctx;
	return true;
}

bool ctrl_loop_set_transmit(struct ctrl_loop *l, ctrl_transmit_fn fn, ctrl_transmit_aged_fn aged, void *ctx)
{
	if (l->transmit != NULL || fn == NULL || aged == NULL) {
		return false;
	}
	l->transmit = fn;
	l->transmit_aged = aged;
	l->transmit_ctx = ctx;
	return true;
}

bool ctrl_loop_open(struct ctrl_loop *l, uint64_t entity_id, const uint64_t own_mac[MBX_N_IF])
{
	if (!mbx_open()) {
		return false;
	}
	uint32_t open = 0;
	for (unsigned ch = 0; ch < MBX_N_CH; ++ch) {
		if (l->rx[ch].fn != NULL) {
			open |= 1u << ch;
		}
	}
	mbx_filter_set_own_eid(entity_id);
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		(void)mbx_filter_set_own_mac(i, own_mac[i]);    // every i is an interface of the contract
	}
	mbx_irq_enable(mbx_place(open, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |
		       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));
	mbx_tick_enable(l->n_ticks > 0u);
	mbx_filter_open(open);
	return true;
}

// Dispatch owed centiseconds, at most `budget`; returns how many.
static uint32_t dispatch_ticks(struct ctrl_loop *l, uint32_t budget)
{
	uint32_t count = l->ticks_owed < budget ? l->ticks_owed : budget;
	for (uint32_t k = 0; k < count; ++k) {
		for (unsigned i = 0; i < l->n_ticks; ++i) {
			l->ticks[i]();
		}
	}
	l->ticks_owed -= count;
	l->stats.ticks += count;
	l->step_age += count;
	return count;
}

static unsigned service_events(struct ctrl_loop *l)
{
	struct mbx_event ev;
	unsigned n = 0;
	// THE DRAIN's order, read before the events: a record before RX_HEAD now follows only events posted by now
	const uint16_t mark = l->drain_ch != 0u ? mbx_rx_mark(l->drain_ch - 1u) : 0u;
	uint32_t ticked = dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS);
	while (n < CTRL_LOOP_EVENTS_PER_PASS && mbx_event_take(&ev)) {
		if (ev.type == MBX_EV_TYPE_TICK) {
			l->ticks_owed += ev.tick_count;
			ticked += dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS - ticked);
		}
		for (unsigned i = 0; i < l->n_sinks; ++i) {
			l->sinks[i].fn(l->sinks[i].ctx, &ev);
		}
		n++;
	}
	l->stats.events += n;
	// THE TICK's cap: a pass that dispatched a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel
	l->rx_cap = ticked != 0u ? CTRL_LOOP_RX_PER_TICK_PASS : CTRL_LOOP_RX_PER_PASS;
	// THE DRAIN's order: a pass that emptied the ring has taken every event posted before the mark
	l->events_left = n == CTRL_LOOP_EVENTS_PER_PASS;
	if (!l->events_left) {
		l->rx_order = mark;
	}
	return n;
}

// A channel's records, in this pass, at most l->rx_cap (THE TICK). THE DRAIN's channel goes past it, to
// CTRL_LOOP_DRAIN_RECORDS, while the pass has spent less than CTRL_LOOP_DRAIN_US; with no clock bound it is any channel.
static unsigned service_rx(struct ctrl_loop *l, unsigned ch, unsigned most, uint32_t deadline)
{
	unsigned n = 0;
	for (unsigned k = 0; k < most; ++k) {
		if (k >= l->rx_cap && (l->clock == NULL ||
		    (int32_t)(deadline - l->clock(l->clock_ctx)) < (int32_t)(CTRL_LOOP_SHARE_US - CTRL_LOOP_DRAIN_US))) {
			break;
		}
		if (l->rx[ch].ready != NULL && !l->rx[ch].ready(l->rx[ch].ctx)) {
			break;
		}
		enum mbx_status st = mbx_rx_take(ch, &l->frame);
		if (st == MBX_STATUS_EMPTY) {
			break;
		}
		if (st == MBX_STATUS_BAD) {
			l->stats.rx_bad++;
			continue;
		}
		l->rx[ch].fn(l->rx[ch].ctx, &l->frame);
		n++;
	}
	l->stats.rx_records += n;
	// a channel that took all it may may have left records: the next passes given whole stand back from them
	l->backlog = l->backlog || (n != 0u && n >= l->rx_cap);
	return n;
}

_Static_assert(CTRL_LOOP_SHARE_US == 2000u, "THE SHARE is not amended");
_Static_assert(CTRL_LOOP_SHARE_PASSES >= CTRL_LOOP_SRP_PASSES && CTRL_LOOP_SHARE_PASSES >= CTRL_LOOP_TX_PASSES,
	       "THE SHARE's passes hold the pass running and the deepest wait");
_Static_assert(CTRL_LOOP_TX_MS <= CTRL_LOOP_T_SVC_MS, "an MRPDU a timer owes must keep T_svc");
_Static_assert(CTRL_LOOP_SRP_MS <= CTRL_LOOP_T_SVC_MS, "the composed burst's last SRP record must keep T_svc");
_Static_assert(CTRL_LOOP_SRP_DRAINED >= MBX_CH_SRP_RATE_BURST, "THE DRAIN's passes must take the burst");

// THE RETRY's round, told what the pass has left of THE SHARE under its margin, in microseconds: all of it with no
// clock bound.
static bool round_of(struct ctrl_loop *l, uint32_t deadline)
{
	const int32_t left = (l->clock != NULL ? (int32_t)(deadline - l->clock(l->clock_ctx)) : (int32_t)CTRL_LOOP_SHARE_US) -
			     (int32_t)CTRL_LOOP_SHARE_MARGIN_US;
	l->stats.retry_passes++;
	return l->retry(l->retry_ctx, left > 0 ? (unsigned)left : 0u);
}

// Whether a pass given whole may follow another: input it would keep from a record or from its centisecond may not
// wait on more than one (THE DRAIN and THE TRANSMIT's bounds).
static bool whole_runs(const struct ctrl_loop *l)
{
	return l->whole < CTRL_LOOP_WHOLE_RUN && (!l->backlog || l->retry_firm) && !l->events_left &&
	       (l->drain_ch == 0u || !mbx_rx_waiting(l->drain_ch - 1u, mbx_rx_mark(l->drain_ch - 1u)));
}

unsigned ctrl_loop_service(struct ctrl_loop *l)
{
	// THE SHARE's deadline, read as the pass starts
	uint32_t deadline = l->clock != NULL ? l->clock(l->clock_ctx) + CTRL_LOOP_SHARE_US : 0u;
	// A pass given whole stands after an ordinary one, and after another only as whole_runs says, and each is one
	// input's wait: THE TRANSMIT's build first, whose bound is the shortest, then THE STEP, then THE RETRY, which fills
	// what the other two leave of the pass when it is aged
	if (l->run != 0u || whole_runs(l)) {
		const bool round = l->retry != NULL && l->retry_aged(l->retry_ctx);
		const bool stepping = l->step != NULL && l->step_age > CTRL_LOOP_STEP_AGE;
		bool given = true;
		if (l->transmit != NULL && l->transmit_aged(l->transmit_ctx)) {
			l->transmit(l->transmit_ctx);
			l->stats.transmit_passes++;
		} else if (stepping) {
			l->step_age = 0u;
			(void)l->step(l->step_ctx, deadline);
			l->stats.aged_passes++;
		} else {
			given = round;
		}
		if (round) {
			(void)round_of(l, deadline);
		}
		if (given) {
			l->stats.passes++;
			l->run = 0u;
			l->whole++;
			return 1u;
		}
	}
	const uint32_t ticks = l->stats.ticks;
	unsigned work = service_events(l);
	l->backlog = false;
	unsigned drained = l->drain_ch != 0u ? service_rx(l, l->drain_ch - 1u, CTRL_LOOP_DRAIN_RECORDS, deadline) : 0u;
	work += drained;
	// A pass that took more than CTRL_LOOP_RX_PER_PASS of THE DRAIN's records takes no other channel's, whose
	// records it may be leaving
	// Then what such a pass has left goes to the records still waiting, a record of each channel in turn, once every
	// channel has had its due: passes given whole may stand between two, and a pass that takes few records would leave
	// them waiting on the next. Each pass starts one channel on, so the channel the pass's time runs out at is each in
	// turn, not the last every time
	for (unsigned most = l->rx_cap, sweep = 1u; sweep != 0u && drained <= CTRL_LOOP_RX_PER_PASS; most = 1u) {
		sweep = 0u;
		for (unsigned k = 0, ch = l->rx_from; k < MBX_N_CH; ++k, ch = ch + 1u < MBX_N_CH ? ch + 1u : 0u) {
			if (l->rx[ch].fn != NULL && ch + 1u != l->drain_ch) {
				sweep += service_rx(l, ch, most, deadline);
			}
		}
		work += sweep;
		if (l->rx_cap != 0u && !l->backlog) {
			break;
		}
		l->rx_cap = 0u;
	}
	l->rx_from = l->rx_from + 1u < MBX_N_CH ? l->rx_from + 1u : 0u;
	bool owed = l->ticks_owed != 0u;
	for (unsigned i = 0; i < l->n_polls; ++i) {
		owed = l->polls[i].fn(l->polls[i].ctx) || owed;
	}
	// THE RETRY, only in a pass that took no input and dispatched no centisecond, before THE STEP, whose
	// deadline counts its time
	if (l->retry != NULL && work == 0u && l->stats.ticks == ticks) {
		owed = round_of(l, deadline) || owed;
	}
	// THE STEP, only in a pass that took no input: no input's service waits on it
	if (l->step != NULL && work == 0u) {
		bool waits = l->step(l->step_ctx, deadline);
		l->step_age = waits ? l->step_age : 0u;
		owed = waits || owed;
	}
	l->stats.passes++;
	l->run++;
	l->whole = 0u;
	if (owed) {
		l->stats.owed_passes++;
		work++;
	}
	return work;
}

void ctrl_loop_step(struct ctrl_loop *l)
{
	if (ctrl_loop_service(l) == 0u) {
		mbx_hal_wait();
	}
}

void ctrl_loop_run(struct ctrl_loop *l)
{
	for (;;) {
		ctrl_loop_step(l);
	}
}
