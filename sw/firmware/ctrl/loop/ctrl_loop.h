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
//   2. receive rings: THE DRAIN's channel, then each bound channel in channel
//      order, at most CTRL_LOOP_RX_PER_PASS records, each to its handler, then
//      what the pass has left to the records still waiting, one a channel in
//      turn;
//   3. polls: every module once; a poll returns true while its module still
//      owes output (a frame its transmit ring had no room for).
// A pass that handled anything, or after which output or centiseconds are
// still owed, is followed by the next pass at once. Only a pass that handled
// nothing and owes nothing sleeps in mbx_hal_wait(), and everything it then
// waits for raises the mailbox interrupt (an RX level, the event level), so
// no owed frame waits on a wake that never comes.
//
// THE BOUND. An input is taken by pass CTRL_LOOP_EVT_PASSES (an event) or
// CTRL_LOOP_RX_PASSES(rx_words) (a record of a channel), and one pass later
// for each pass among them that dispatches a centisecond, which takes
// CTRL_LOOP_RX_PER_TICK_PASS records of a channel (THE TICK), counted from the
// first pass that starts after the fabric posted it, and the module's
// response is committed in the pass that takes it (A3 says when it is
// not). A pass given whole (THE STEP, THE RETRY, THE TRANSMIT) takes no input
// and is not counted: it costs the input the step's, the round's or the
// build's time, and it holds no more than THE SHARE. At most
// CTRL_LOOP_WHOLE_RUN stand in a row, and one between two ordinary passes while
// an event or a record of THE DRAIN's channel waits, or while records wait and
// the client yields. A pass costs at most the budgets below times the modules'
// stated costs. That holds under four assumptions:
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
// THE SHARE (#665, #397's one-hart rule). A pass is the only opportunity to
// take an input, and the smallest bound every input shares is T_svc, 20 ms
// (FR_NFR.md 3.4.1; SRP's own since the owner's ruling of 2026-11-06). An input
// waits for the pass running when it arrives, then is taken N passes later and
// answered in that pass, so (N + 1) passes must fit that bound. The deepest
// admitted wait is nine passes: THE DRAIN's and THE TRANSMIT's at two
// interfaces, and the A3 row of seven owed frames, answered in pass 8 after the
// room returns. So no pass may exceed 20 ms / 10 = 2.0 ms of CPU time, a pass
// to spare: 200,000 cycles of the split CPU's own clock, the 100 MHz bus clock
// it runs on (#665, owner decision 2026-10-30). Every slice serves that share,
// and each module's work in one pass is bounded, the rest resumed on the next
// pass:
//   * the loop: the events, records and centiseconds per pass above, and one
//     clock read a pass when a clock is bound (THE STEP);
//   * ADP and ACMP: the records the loop hands them, and one owed frame per
//     interface (adp_mbx.h, acmp_mbx.h);
//   * MAAP: its records, and at most two queued frames per interface
//     (tsn-c-stack maap.c, pump);
//   * AECP: the records the loop hands it, each answered in its pass and taken
//     only while no response or notice is owed; its change notices only in
//     THE RETRY's round, as many as the pass has room for;
//   * SRP: its records (THE DRAIN), and an interface's two MRPDUs in a pass
//     given whole (THE TRANSMIT); a link change withdraws in the pass that
//     takes it and builds in the next, and a pass builds one interface at most
//     (srp_bounds.h);
//   * the saved-state store: one service step, taken only in a pass that
//     took no input and has room for it, or as the whole of a pass once it
//     has waited past its age limit (THE STEP, nvm_store.h).
// So each kind of pass has a worst case, the heaviest of each the CPU budget
// harness measures at this image across every group it stages, both arms,
// with and without the drafts (docs/design/SPLIT_CONTROL_MEMORY.md section
// 13), and each sits at least 6,490 CPU cycles, the swing the data layout
// alone made on the same records, under THE SHARE, at this image's layout
// and in the groups measured with THE RETRY's and THE TRANSMIT's fields at
// their structs' ends:
//   * a pass that takes a record (its events, its records, the polls):
//     190,420 cycles at 8x8/2if, 116,176 at 1x1/1if;
//   * one that takes events and no record (the polls, at most one event
//     beside THE TRANSMIT's build): 140,363 and 52,247;
//   * one that takes nothing and writes to the mailbox (the polls' owed
//     output, THE TRANSMIT's build, THE RETRY's round, THE STEP before its
//     deadline): 171,351 and 128,083;
//   * one given whole to an aged step (the step and one round): 97,806 and
//     97,378;
//   * one given whole to an aged retry (one round): 12,571 and 9,610;
//   * one given whole to an aged build (one build and one round, no poll):
//     no group stages one; it holds at most the heaviest pass that carries
//     a build and the heaviest round, 171,351 + 12,571 = 183,922 and
//     128,083 + 9,610 = 137,693;
//   * one that writes nothing (the polls with nothing owed, or THE STEP
//     before its deadline): 118,647 and 106,887.
//
// THE STEP (#665). One client takes a deferrable step at the end of a pass
// that took no input, no event and no record, after the polls: the
// saved-state store's write path. Its flash steps (a page program's issue up
// to 0.97 ms, a 128-byte read-back 0.77 ms) do not fit beside the heaviest
// pass the other slices make (1.90 ms at 8x8/2if), and in a pass that takes
// records they lengthen every record still waiting (the last SRP record of a
// full ring waits sixteen passes), so its centisecond consumer only owes a
// step, and the loop calls the step only once a pass takes nothing. It hands
// the step the clock's value at which the pass has spent
// CTRL_LOOP_SHARE_US, read once as the pass starts; the client takes its
// step only when its stated cost still fits before that deadline. Otherwise
// the step stays owed, the loop passes again at once, and the first pass
// that takes nothing and has room takes it. An input that arrives during
// such a pass waits for it, as for any pass running when it arrives.
// Input that never leaves a pass empty would hold the step off for good, so
// it has an age limit: once more than CTRL_LOOP_STEP_AGE centiseconds have
// been dispatched since the step last ran or owed nothing, the next pass is
// the step's alone. It calls the step before it takes any input, with the
// deadline read as it starts, then THE RETRY's client, and returns one, so
// the input it held off is taken by the next pass: an input waits one step
// and one retry round at most. Under such input the client steps once every
// CTRL_LOOP_STEP_AGE + 1 centiseconds, and nvm_store.h states the worst case
// that makes of a save.
//
// THE RETRY (#665). One client's deferrable round: AECP's change notices and
// their retries (aecp.h), which answer no input. Its module's poll and sinks
// build no notice, arm no timer for a due retry and report it owed, and only
// the loop calls the client, in three kinds of pass: one that took no input and
// dispatched no centisecond, after its polls and before THE STEP; one given
// whole to an aged step or a build, after it; and one given whole to the round,
// which the client asks for as each pass given whole may start (aecp.c,
// aecp_retry_aged): a notice waits, nothing waits ahead of its round, and the
// pace the last round set has passed. The loop tells the client what the pass
// has left of THE SHARE under CTRL_LOOP_SHARE_MARGIN_US, and the client fills
// it with as many notices as their stated cost allows (aecp_mbx.c, retry), so a
// round takes no pass over THE SHARE by construction.
// While records wait a round yields, one notice at a slower pace, so the CPU
// they wait for is not spent on notices; a queue's first AECP_ROUND_YIELDS
// rounds beside records do, and then the client stands firm (retry_firm), so
// input that never lets up holds no notice past its bound. aecp.h states that
// bound and derives it.
//
// THE TRANSMIT (#665). One client's build: SRP's MRPDUs (srp_mbx.c, transmit).
// Built in a pass that takes records, it lengthened every record still waiting,
// and it is the one thing the join, periodic and LeaveAll timers wait for, so
// a build has a pass given whole of its own, the first the loop can give once
// the client reports one owed. That pass makes every interface's declarations
// and sends both MRPDUs of the first interface that owes one, then THE RETRY's
// client fills what is left of it. Its module's poll builds nothing; it sends
// only a frame already owed (A3), and no build is owed ahead of that frame. The
// client owes a pass for a join timer's end, a LeaveAll timer's where no join
// timer holds it, or an Applicant that moves with its join timer idle, and for
// a declaration, which while notices are queued waits for the join timer, so
// each comes at most once a JoinTime a participant and THE RETRY's bound can
// count them. CTRL_LOOP_TX_MS states the bound.
//
// THE DRAIN (#665). One channel's records go first, past
// CTRL_LOOP_RX_PER_PASS, to CTRL_LOOP_DRAIN_RECORDS, while the pass has spent
// less than CTRL_LOOP_DRAIN_US: SRP's, whose burst is twice any other's and
// whose bound the composed burst would pass at two a pass. A pass that took
// more than CTRL_LOOP_RX_PER_PASS of them takes no other channel's, and a
// record follows only the events posted before it (rx_order, read before the
// pass's events): an event posted during every pass holds it back no longer.
// CTRL_LOOP_SRP_MS states the bound.
//
// THE TICK. A TICK event carries the centiseconds the fabric counted since
// the previous one; the loop calls every registered centisecond consumer
// that many times, in registration order, at most CTRL_LOOP_TICKS_PER_PASS
// per pass, and a pass that dispatches one takes at most
// CTRL_LOOP_RX_PER_TICK_PASS records of a channel, the rest waiting for the
// next pass. lwSRP's shlan_timer_tick() is such a consumer (shlan_port.h), so
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
// The records one pass takes, kept under the owner's D4(b) decision of
// 2026-10-27 (#665: the admitted backlog first). RX: two of a channel, the
// most maximum-length records SRP's ring holds (srp_bounds.h). Every module's
// pass bound charges a record at its channel's maximum length, so a larger
// count is charged for records no ring can hold until those bounds are
// restated in ring words. Events: eight, half the ring. The whole ring would
// take an event behind a full ring by the first pass, but every pass's bound
// would carry sixteen events: CTRL_APP_PASS_MAX 3,988 accesses instead of
// 3,116 at one interface, and ACMP's owed-frame bound 12,222 instead of 9,270,
// over the 10 ms T_svc first proposed at 1 us an access (docs/design/MAILBOX_SPLIT.md).
#define CTRL_LOOP_EVENTS_PER_PASS 8u    // event records one pass takes at most
#define CTRL_LOOP_RX_PER_PASS 2u        // RX records one pass takes per channel at most
#define CTRL_LOOP_TICKS_PER_PASS 16u    // centiseconds one pass dispatches at most
// THE TICK's cap (#665): RX records of a channel a pass that dispatches a
// centisecond takes at most. The centisecond's consumers cost about 43,000
// CPU cycles at 8x8/2if (lwSRP's timers and the walks after them), and beside
// the composed burst's records, two a channel, that pass was the heaviest the
// burst made before this cap, 195,756 cycles, 4,244 under THE SHARE. With one
// record a channel it holds a channel's record fewer than any other pass of
// the burst.
#define CTRL_LOOP_RX_PER_TICK_PASS 1u
// THE DRAIN: the records of its channel a pass takes at most, and what the pass
// may have spent, in microseconds, for it to take another past
// CTRL_LOOP_RX_PER_PASS.
#define CTRL_LOOP_DRAIN_RECORDS 12u
#define CTRL_LOOP_DRAIN_US 1300u
// The passes given whole that may stand in a row. Three carry a queue of notices
// past the two a row would, at no record's cost, since none stands in a row
// beside a record of THE DRAIN's channel or a full pass's events.
#define CTRL_LOOP_WHOLE_RUN 3u
// THE SHARE in microseconds: T_svc's 20 ms over ten passes, one more than the
// deepest wait the loop admits.
#define CTRL_LOOP_T_SVC_MS 20u
#define CTRL_LOOP_SHARE_PASSES 10u
#define CTRL_LOOP_SHARE_US (1000u * CTRL_LOOP_T_SVC_MS / CTRL_LOOP_SHARE_PASSES)
// What a round leaves of THE SHARE in microseconds: the 6,490 cycles the data
// layout alone moved a pass by, which every pass class keeps.
#define CTRL_LOOP_SHARE_MARGIN_US 65u
// THE STEP's age limit in centiseconds. Two. A window that opens with the
// age at the limit, after input that left no pass empty, takes an aged step
// among its records at its next centisecond, at any limit; none drains in two
// ticks, so it takes one at most, and one opened at age zero, after a pass
// that took nothing, takes none at two, where at one it would. Every row the
// budget stages fits with that step at each placement measured, the least
// margin 0.235 ms (8x8/2if, the last SRP record of a save's verify window
// opened one short of the limit) against a step of up to 0.97 ms; at three a
// save would take a step every four ticks under such input (nvm_store.h)
// (#665).
#define CTRL_LOOP_STEP_AGE 2u
// The measured costs the bounds below rest on, in microseconds, each the
// heaviest at 8x8/2if rounded up (CPU budget harness; 100 cycles a microsecond):
// a pass given whole to an aged step, to a build of both of an interface's
// MRPDUs, and to a build of one; one record of SRP's burst; the first
// registration of a burst; and a centisecond's consumers.
#define CTRL_LOOP_STEP_PASS_US 980u
#define CTRL_LOOP_BUILD_PASS_US 1250u
#define CTRL_LOOP_BUILD_ONE_PASS_US 980u
#define CTRL_LOOP_SRP_RECORD_US 123u
#define CTRL_LOOP_SRP_FIRST_US 400u
#define CTRL_LOOP_TICK_US 430u
// THE TRANSMIT's bound (#665), every MRPDU a join, periodic or LeaveAll timer
// makes owed, from the deadline to its commit, by pass class, each within THE
// SHARE under any input: the pass running when the centisecond's TICK is
// posted; a row of passes given whole; the ordinary pass that takes
// CTRL_LOOP_EVENTS_PER_PASS events ahead of the TICK, a full ring's half; the
// one pass given whole that may follow it, since events still wait; the
// ordinary pass that takes the TICK and dispatches the centisecond, which owes
// the build; and one pass given whole a build first, an interface each. 18 ms at
// two interfaces, 16 ms at one, inside T_svc (FR_NFR.md 3.4.1; ctrl_loop.c holds
// it).
#define CTRL_LOOP_TX_PASSES (1u + CTRL_LOOP_WHOLE_RUN + 1u + 1u + 1u + MBX_N_IF)
#define CTRL_LOOP_TX_MS (CTRL_LOOP_TX_PASSES * CTRL_LOOP_SHARE_US / 1000u)
// THE DRAIN's bound (#665), the composed burst's last SRP record from its
// arrival to the pass that takes it, by pass class, each within THE SHARE under
// any input: the pass running at its arrival, then a pass given whole and an
// ordinary pass, CTRL_LOOP_SRP_DRAINS times, none in a row while a record waits.
// An ordinary pass takes the records it starts before CTRL_LOOP_DRAIN_US: the
// fewest in the four the burst needs are one beside a centisecond and the first
// registration, one alone, one beside the next centisecond, 10 ms on, and one
// alone. 18 ms, inside T_svc (FR_NFR.md 3.4.1; ctrl_loop.c holds the sum to the
// burst).
#define CTRL_LOOP_DRAIN_TAKES(spent_us) \
	((CTRL_LOOP_DRAIN_US - (spent_us) + CTRL_LOOP_SRP_RECORD_US - 1u) / CTRL_LOOP_SRP_RECORD_US)
#define CTRL_LOOP_SRP_DRAINS 4u
#define CTRL_LOOP_SRP_DRAINED \
	(CTRL_LOOP_DRAIN_TAKES(CTRL_LOOP_TICK_US + CTRL_LOOP_SRP_FIRST_US) + CTRL_LOOP_DRAIN_TAKES(0u) + \
	 CTRL_LOOP_DRAIN_TAKES(CTRL_LOOP_TICK_US) + CTRL_LOOP_DRAIN_TAKES(0u))
#define CTRL_LOOP_SRP_PASSES (1u + 2u * CTRL_LOOP_SRP_DRAINS)
#define CTRL_LOOP_SRP_MS (CTRL_LOOP_SRP_PASSES * CTRL_LOOP_SHARE_US / 1000u)

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
// THE STEP: deadline is the clock's value at which the pass has spent its
// share; true while the client still owes a step it had no room for.
typedef bool (*ctrl_step_fn)(void *ctx, uint32_t deadline);
typedef uint32_t (*ctrl_clock_fn)(void *ctx);   // microseconds, counting up; differences wrap
// THE RETRY: what the pass has left of THE SHARE under its margin, which the
// round fills; true while the client still owes, a retry still due or what it
// built not yet sent.
typedef bool (*ctrl_retry_fn)(void *ctx, unsigned left_us);
// THE RETRY's pace: true when a notice waits, nothing waits ahead of its round
// and the pace the last round set has passed.
typedef bool (*ctrl_retry_aged_fn)(void *ctx);
// THE TRANSMIT: the build of a pass given whole.
typedef void (*ctrl_transmit_fn)(void *ctx);
// THE TRANSMIT's due: true when the client owes a build and no frame ahead of it.
typedef bool (*ctrl_transmit_aged_fn)(void *ctx);

struct ctrl_loop_rx {
	bool (*ready)(void *ctx);
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
	uint32_t aged_passes;   // passes given whole to an aged step (THE STEP)
	uint32_t retry_passes;  // passes that called THE RETRY's client
	uint32_t transmit_passes;    // passes given whole to THE TRANSMIT's client
};

struct ctrl_loop {
	struct ctrl_loop_rx rx[MBX_N_CH];
	struct ctrl_loop_sink sinks[CTRL_LOOP_MAX_SINKS];
	unsigned n_sinks;
	ctrl_tick_fn ticks[CTRL_LOOP_MAX_TICKS];
	unsigned n_ticks;
	struct ctrl_loop_poll polls[CTRL_LOOP_MAX_POLLS];
	unsigned n_polls;
	ctrl_step_fn step;              // THE STEP's client, or NULL
	void *step_ctx;
	ctrl_clock_fn clock;
	void *clock_ctx;
	ctrl_retry_fn retry;            // THE RETRY's client, or NULL
	ctrl_retry_aged_fn retry_aged;  // its age
	void *retry_ctx;
	struct mbx_frame frame;         // the one RX buffer every handler borrows
	uint32_t ticks_owed;            // centiseconds taken from TICK records, not yet dispatched
	uint32_t step_age;              // centiseconds dispatched since the step last ran or owed nothing
	struct ctrl_loop_stats stats;
	ctrl_transmit_fn transmit;      // THE TRANSMIT's client, or NULL
	ctrl_transmit_aged_fn transmit_aged;  // its age
	void *transmit_ctx;
	uint32_t rx_cap;                // the records of a channel this pass takes at most (THE TICK)
	uint32_t run;                   // ordinary passes since the last pass given whole
	uint32_t whole;                 // passes given whole since the last ordinary one
	bool backlog;                   // the last ordinary pass left a record it could have taken
	bool retry_firm;                // THE RETRY's client takes its rounds whatever waits
	bool retry_queued;              // THE RETRY's client has notices queued
	unsigned drain_ch;              // THE DRAIN's channel + 1, 0 when none
	bool events_left;               // the last pass that took events took all it may
	uint16_t rx_order;              // the records before this follow only events already taken
};

void ctrl_loop_init(struct ctrl_loop *l);

// Bind a module. False when the table is full or the channel is unknown.
bool ctrl_loop_bind_rx(struct ctrl_loop *l, unsigned ch, ctrl_rx_fn fn, void *ctx);
void ctrl_loop_set_rx_ready(struct ctrl_loop *l, unsigned ch, bool (*ready)(void *ctx));
bool ctrl_loop_add_sink(struct ctrl_loop *l, ctrl_event_fn fn, void *ctx);
bool ctrl_loop_add_tick(struct ctrl_loop *l, ctrl_tick_fn fn);
bool ctrl_loop_add_poll(struct ctrl_loop *l, ctrl_poll_fn fn, void *ctx);
// Bind THE STEP's client and the clock its deadline is read from. False when
// either function is missing or a step is already bound.
bool ctrl_loop_set_step(struct ctrl_loop *l, ctrl_step_fn fn, void *ctx, ctrl_clock_fn clock, void *clock_ctx);
// Bind THE RETRY's client and its age. False when either function is missing
// or a client is already bound.
bool ctrl_loop_set_retry(struct ctrl_loop *l, ctrl_retry_fn fn, ctrl_retry_aged_fn aged, void *ctx);
// Bind THE TRANSMIT's client and its age. False when either function is
// missing or a client is already bound.
bool ctrl_loop_set_transmit(struct ctrl_loop *l, ctrl_transmit_fn fn, ctrl_transmit_aged_fn aged, void *ctx);

// Bring the mailbox up in the contract's order: check the contract, write the
// filter's entity_id and each interface's own unicast MAC (own_mac[i], 48
// bits, for interface i), enable the interrupt causes, start the tick when a
// centisecond consumer is bound, and only then open the bound channels.
// False when the bitstream carries another contract (nothing is opened).
bool ctrl_loop_open(struct ctrl_loop *l, uint64_t entity_id, const uint64_t own_mac[MBX_N_IF]);

// One service pass; returns the events and records it handled, plus one when
// output, centiseconds, a retry or a build are still owed, or one when it was
// an aged step's alone (THE STEP), an aged retry's (THE RETRY) or an aged
// transmit's (THE TRANSMIT). 0 means the loop may sleep.
unsigned ctrl_loop_service(struct ctrl_loop *l);

// One turn of ctrl_loop_run: a pass, then mbx_hal_wait() if it returned 0.
void ctrl_loop_step(struct ctrl_loop *l);

// Turn forever.
void ctrl_loop_run(struct ctrl_loop *l);

#ifdef __cplusplus
}
#endif

#endif // CTRL_LOOP_H
