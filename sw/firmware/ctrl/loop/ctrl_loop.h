// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_loop.h - the bare-metal event loop of the control-plane firmware
// (#665 lane F0; the owner directive of 2026-10-05: no OS, no heap, static
// pools, one event loop).
//
// One loop, one thread, no OS service. Everything a module needs is bound
// before ctrl_loop_open: an RX handler per channel, any number of event
// sinks, the centisecond consumers and the polls, each in a fixed table sized
// below.
//
// THE PASS, in this order (the events-first ruling on PR #668):
//   1. events: at most CTRL_LOOP_EVENTS_PER_PASS records, in ring order, each
//      to every sink; a TICK record's centiseconds go to the centisecond
//      consumers, at most CTRL_LOOP_TICKS_PER_PASS per pass, the rest carried
//      to the next pass;
//   2. receive rings: each bound channel in channel order, at most
//      CTRL_LOOP_RX_PER_PASS records, each to its handler;
//   3. polls: every module once; a poll returns true while its module still
//      owes output (a frame its transmit ring had no room for).
// A pass that handled anything, or after which output or centiseconds are
// still owed, is followed by the next pass at once. Only a pass that handled
// nothing and owes nothing sleeps in mbx_hal_wait(), and everything it then
// waits for raises the mailbox interrupt (an RX level, the event level), so
// no owed frame waits on a wake that never comes.
//
// THE BOUND. An input is taken by pass CTRL_LOOP_EVT_PASSES (an event) or
// CTRL_LOOP_RX_PASSES(rx_words) (a record of a channel), counted from the
// first pass that starts after the fabric posted it, and the module's
// response is committed in the pass that takes it (A3 says when it is
// not). A pass costs at most the
// budgets below times the modules' stated costs. That holds under four
// assumptions:
//   A1 backlog: at most a full event ring (CTRL_LOOP_EVT_BACKLOG records,
//      the ring holds no more) and at most a full receive ring per channel
//      (CTRL_LOOP_RX_BACKLOG records: the smallest record the filter passes
//      is two header words and a frame that reaches the subtype byte, 15
//      bytes in 4 words);
//   A2 callbacks: a sink, a handler, a centisecond consumer and a poll each
//      cost at most the accesses its module states (adp_mbx.h for ADP) and
//      none waits on the fabric;
//   A3 transmit room: a response finds room in its transmit ring, and its
//      module owes no frame ahead of it. When it does not, its module owes
//      it and the loop keeps passing; a poll sends one owed frame per pass
//      and interface, oldest first. A response with k frames owed ahead of
//      it is committed in pass k + 1 counted from the first pass that starts
//      after the merge frees the room, and not before the pass that takes
//      its input. A module bounds k and states the figure (adp_mbx.h, owed
//      frames: k <= 2 for ADP);
//   A4 bus: the bound counts mailbox accesses. Time is that count times the
//      platform's cost per access, which this lane has not measured.
// A protocol composes its own figures from these (ADP_MBX_PASS_MAX).
//
// THE TICK. A TICK event carries the centiseconds the fabric counted since
// the previous one; the loop calls every registered centisecond consumer
// that many times, in registration order, at most CTRL_LOOP_TICKS_PER_PASS
// per pass. lwSRP's shlan_timer_tick() is such a consumer (shlan_port.h), so
// its leave, LeaveAll and periodic timers run on the fabric's time and lose
// no tick when the core is late; a long stall is caught up a bounded slice at
// a time.

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
#define CTRL_LOOP_TICKS_PER_PASS 16u    // centiseconds one pass dispatches at most

// A1: the backlogs the bound assumes, in records.
#define CTRL_LOOP_EVT_BACKLOG (MBX_EVT_WORDS / MBX_EV_WORDS)
#define CTRL_LOOP_RX_MIN_RECORD_WORDS (MBX_RX_HDR_WORDS + 4u)
#define CTRL_LOOP_RX_BACKLOG(rx_words) ((rx_words) / CTRL_LOOP_RX_MIN_RECORD_WORDS)

// The pass that takes an input at the latest, counted from the first pass
// that starts after it was posted.
#define CTRL_LOOP_EVT_PASSES \
	((CTRL_LOOP_EVT_BACKLOG + CTRL_LOOP_EVENTS_PER_PASS - 1u) / CTRL_LOOP_EVENTS_PER_PASS)
#define CTRL_LOOP_RX_PASSES(rx_words) \
	((CTRL_LOOP_RX_BACKLOG(rx_words) + CTRL_LOOP_RX_PER_PASS - 1u) / CTRL_LOOP_RX_PER_PASS)

typedef void (*ctrl_rx_fn)(void *ctx, const struct mbx_frame *f);
typedef void (*ctrl_event_fn)(void *ctx, const struct mbx_event *ev);
typedef void (*ctrl_tick_fn)(void);
typedef bool (*ctrl_poll_fn)(void *ctx);   // true while the module still owes output

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
	uint32_t owed_passes;   // passes after which output or centiseconds were still owed
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
	uint32_t ticks_owed;            // centiseconds taken from TICK records, not yet dispatched
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

// One service pass; returns the events and records it handled, plus one when
// output or centiseconds are still owed. 0 means the loop may sleep.
unsigned ctrl_loop_service(struct ctrl_loop *l);

// One turn of ctrl_loop_run: a pass, then mbx_hal_wait() if it returned 0.
void ctrl_loop_step(struct ctrl_loop *l);

// Turn forever.
void ctrl_loop_run(struct ctrl_loop *l);

#ifdef __cplusplus
}
#endif

#endif // CTRL_LOOP_H
