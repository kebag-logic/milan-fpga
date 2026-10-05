// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_loop.h - the bare-metal event loop of the control-plane firmware
// (#665 lane F0; the owner directive of 2026-10-05: no OS, no heap, static
// pools, one event loop).
//
// One loop, one thread, no OS service. A pass takes a bounded number of
// fabric events and a bounded number of RX records per channel, hands each to
// the module bound to it, then gives every module one poll; when a pass finds
// nothing it sleeps in mbx_hal_wait() until the mailbox interrupt (an RX or
// event level, ctrl_loop_open enables both) wakes it. Everything a module
// needs is bound before ctrl_loop_open: an RX handler per channel, any number
// of event sinks, the centisecond consumers and the polls, each in a fixed
// table sized below.
//
// THE PASS IS THE UNIT OF THE SERVICE-LATENCY BOUND. A record that arrives
// while a pass runs is taken by the next pass at the latest, and a pass costs
// at most CTRL_LOOP_EVENTS_PER_PASS events plus CTRL_LOOP_RX_PER_PASS records
// per channel plus one poll per module, each a bounded number of bus
// accesses. A protocol states its bound per response path in passes and bus
// accesses on top of that (adp_mbx.h for ADP).
//
// THE TICK. A TICK event carries the centiseconds the fabric counted since
// the previous one; the loop calls every registered centisecond consumer
// that many times, in registration order. lwSRP's shlan_timer_tick() is such
// a consumer (shlan_port.h), so its leave, LeaveAll and periodic timers run
// on the fabric's time and lose no tick when the core is late.

#ifndef CTRL_LOOP_H
#define CTRL_LOOP_H

#include <stdbool.h>
#include <stdint.h>

#include "mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

#define CTRL_LOOP_MAX_SINKS 8u          // event sinks
#define CTRL_LOOP_MAX_TICKS 4u          // centisecond consumers
#define CTRL_LOOP_MAX_POLLS 8u          // polled modules
#define CTRL_LOOP_EVENTS_PER_PASS 8u    // event records one pass takes at most
#define CTRL_LOOP_RX_PER_PASS 2u        // RX records one pass takes per channel at most

typedef void (*ctrl_rx_fn)(void *ctx, const struct mbx_frame *f);
typedef void (*ctrl_event_fn)(void *ctx, const struct mbx_event *ev);
typedef void (*ctrl_tick_fn)(void);
typedef void (*ctrl_poll_fn)(void *ctx);

struct ctrl_loop_rx {
	ctrl_rx_fn fn;
	void *ctx;
};

struct ctrl_loop_sink {
	ctrl_event_fn fn;
	void *ctx;
};

struct ctrl_loop_poll {
	ctrl_poll_fn fn;
	void *ctx;
};

struct ctrl_loop_stats {
	uint32_t passes;        // service passes run
	uint32_t events;        // event records taken
	uint32_t rx_records;    // RX records handed to a module
	uint32_t rx_bad;        // RX records the driver refused (ring resynchronised)
	uint32_t ticks;         // centiseconds dispatched
};

struct ctrl_loop {
	struct ctrl_loop_rx rx[MBX_N_CH];
	struct ctrl_loop_sink sinks[CTRL_LOOP_MAX_SINKS];
	unsigned n_sinks;
	ctrl_tick_fn ticks[CTRL_LOOP_MAX_TICKS];
	unsigned n_ticks;
	struct ctrl_loop_poll polls[CTRL_LOOP_MAX_POLLS];
	unsigned n_polls;
	struct mbx_frame frame;         // the one RX buffer every handler borrows
	struct ctrl_loop_stats stats;
};

void ctrl_loop_init(struct ctrl_loop *l);

// Bind a module. False when the table is full or the channel is unknown.
bool ctrl_loop_bind_rx(struct ctrl_loop *l, unsigned ch, ctrl_rx_fn fn, void *ctx);
bool ctrl_loop_add_sink(struct ctrl_loop *l, ctrl_event_fn fn, void *ctx);
bool ctrl_loop_add_tick(struct ctrl_loop *l, ctrl_tick_fn fn);
bool ctrl_loop_add_poll(struct ctrl_loop *l, ctrl_poll_fn fn, void *ctx);

// Bring the mailbox up in the contract's order: check the contract, write the
// filter's entity_id, enable the interrupt causes, start the tick when a
// centisecond consumer is bound, and only then open the bound channels.
// False when the bitstream carries another contract (nothing is opened).
bool ctrl_loop_open(struct ctrl_loop *l, uint64_t entity_id);

// One service pass; returns the records and events it handled.
unsigned ctrl_loop_service(struct ctrl_loop *l);

// Service passes forever, sleeping in mbx_hal_wait() after an idle pass.
void ctrl_loop_run(struct ctrl_loop *l);

#ifdef __cplusplus
}
#endif

#endif // CTRL_LOOP_H
