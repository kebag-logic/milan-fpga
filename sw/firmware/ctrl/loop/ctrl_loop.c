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

bool ctrl_loop_set_retry(struct ctrl_loop *l, ctrl_retry_fn fn, void *ctx)
{
	if (l->retry != NULL || fn == NULL) {
		return false;
	}
	l->retry = fn;
	l->retry_ctx = ctx;
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
	return n;
}

static unsigned service_rx(struct ctrl_loop *l, unsigned ch)
{
	unsigned n = 0;
	for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS; ++k) {
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
	return n;
}

unsigned ctrl_loop_service(struct ctrl_loop *l)
{
	// THE STEP's deadline, read as the pass starts
	uint32_t deadline = l->step != NULL ? l->clock(l->clock_ctx) + CTRL_LOOP_SHARE_US : 0u;
	// THE STEP's age limit: a step not run for more than CTRL_LOOP_STEP_AGE centiseconds is this
	// whole pass, before any input, with THE RETRY after it, so an input waits one step and one
	// retry round at most
	if (l->step != NULL && l->step_age > CTRL_LOOP_STEP_AGE) {
		l->step_age = 0u;
		(void)l->step(l->step_ctx, deadline);
		// THE RETRY after the step: under input that leaves no pass empty, no other pass is free
		// of input
		if (l->retry != NULL) {
			(void)l->retry(l->retry_ctx);
			l->stats.retry_passes++;
		}
		l->stats.passes++;
		l->stats.aged_passes++;
		return 1u;
	}
	const uint32_t ticks = l->stats.ticks;
	unsigned work = service_events(l);
	for (unsigned ch = 0; ch < MBX_N_CH; ++ch) {
		if (l->rx[ch].fn != NULL) {
			work += service_rx(l, ch);
		}
	}
	bool owed = l->ticks_owed != 0u;
	for (unsigned i = 0; i < l->n_polls; ++i) {
		owed = l->polls[i].fn(l->polls[i].ctx) || owed;
	}
	// THE RETRY, only in a pass that took no input and dispatched no centisecond, before THE STEP, whose
	// deadline counts its time
	if (l->retry != NULL && work == 0u && l->stats.ticks == ticks) {
		owed = l->retry(l->retry_ctx) || owed;
		l->stats.retry_passes++;
	}
	// THE STEP, only in a pass that took no input: no input's service waits on it
	if (l->step != NULL && work == 0u) {
		bool waits = l->step(l->step_ctx, deadline);
		l->step_age = waits ? l->step_age : 0u;
		owed = waits || owed;
	}
	l->stats.passes++;
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
