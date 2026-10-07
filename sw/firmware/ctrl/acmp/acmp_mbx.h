// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_mbx.h - the ACMP module's mailbox adapter: struct acmp_ports on the
// packet mailbox, and the bindings into the bare-metal event loop (#665 lane
// F3).
//
//   send         -> a TX record on the acmp channel (mbx_tx_send)
//   now_ms       -> NOW_MS
//   timer        -> fabric timer slot `first_slot + interface`, armed at the
//                   core's absolute deadline with a fresh tag, or cancelled
//   gptp         -> the interface's GM_LO/GM_HI/DOMAIN snapshot
//   seed         -> NOW_MS
//
// and from the loop: the acmp channel's RX records to acmp_rx, the TIMER
// event of a slot to acmp_timer_expired when its tag is the current arm's (an
// expiry that raced a re-arm or a stop carries an older tag and is counted,
// never acted on), and a poll that sends one owed frame per pass and tells
// the loop it still owes one. The env (struct acmp_env) is the integrator's.
//
// THE ADP CHANNEL'S AVAILABLE AND DEPARTING (Milan v1.2 5.6.4.1). The listener's
// discovery machine needs every ENTITY_AVAILABLE and ENTITY_DEPARTING of a bound
// talker. acmp_mbx_attach() takes the adp channel's handler, which F0's ADP
// adapter bound, and puts one in front of it that hands each AVAILABLE and
// DEPARTING record to acmp_adp_rx and every other record (ENTITY_DISCOVER, and
// anything else ADP discards and counts, 5.6.3.1) to that handler unchanged.
// It reaches F0's module through the loop's public binding only. The contract's
// adp channel (sw/mailbox/mailbox.yaml, major 2) passes ENTITY_DISCOVER alone
// today, so until it carries the term docs/design/MAILBOX_SPLIT.md's open items
// name, the tap's discovery half receives nothing from the fabric.
//
// SERVICE LATENCY (NFR-SCOUT-03, the H-ACMP and H-DISC hooks of FR_NFR.md
// 3.4.2), under the assumptions A1 to A4 of ctrl_loop.h, counted in mailbox
// accesses as adp_mbx.h counts them.
//
// One path's own cost, in the pass that takes its input with nothing else
// pending, in a composition of ADP and ACMP (two bound channels: the pass's
// tail reads EVT_HEAD once and each ring's RX_HEAD once more):
//
//   an ACMP RX record   RX_HEAD + 2 header + 18 payload + RX_TAIL       22
//   an ACMP TX record   TX_TAIL + 2 header + 18 payload + TX_HEAD       22
//   an ADP RX record    RX_HEAD + 2 header + 21 payload + RX_TAIL       25
//   an event record     EVT_HEAD + 4 words + EVT_TAIL                    6
//   the clock           NOW_MS                                           1
//   a timer arm         TMR_DEADLINE + TMR_CMD                           2
//   a timer stop        TMR_CMD                                          1
//   the gPTP sample     GM_LO + GM_HI + DOMAIN                           3
//   the seed            NOW_MS, at the run's first TMR_DELAY draw        1
//   the pass's tail     EVT_HEAD + RX_HEAD (adp) + RX_HEAD (acmp)        3
//
// At 70 bytes an ACMP frame is 18 payload words. ACMP_MBX_LAT_* below are
// these sums, and test_acmp_mbx.cpp (C0 to C12) counts every path access by
// access on the host model and fails one that exceeds its figure.
//
// The bound with a backlog. A pass of the ADP and ACMP composition costs at
// most ACMP_MBX_PASS_MAX:
//
//   events  8 x (6 + 31 + 4)     a record; ADP's costliest action (a TMR_DELAY
//                                expiry, adp_mbx.h); ACMP's per-event cost
//                                (the clock, the seed and a re-arm)
//   ACMP timer work  16 x 22     every sink's due timers, once per pass: at most
//                                one probe each (a TMR_RETRY or TMR_NO_TK that
//                                draws 0 ms sends it at once), then TMR_NO_RESP
//                                lies 200 ms ahead
//   ADP RX  2 x (36 + 7)         the channel's largest record (128 bytes) and
//                                the tap's costliest handler: a record goes to
//                                ADP (4, adp_mbx.h) or to discovery (gPTP 3,
//                                clock 1, seed 1, re-arm 2), never to both
//   ACMP RX 2 x (36 + 47)        the largest record and the costliest handler
//                                (a BIND: the clock, the response and the probe,
//                                TMR_NO_RESP armed)
//   polls   31 + 22              ADP's (adp_mbx.h) and one owed ACMP frame
//
// The smallest ACMP record the filter passes is 13 words (a frame that reaches
// the end of talker_entity_id, byte 42), so a full acmp ring holds 19 and its
// record is taken by pass ACMP_MBX_RX_PASSES (10), counted from the first pass
// that starts after the fabric posted it; an event by pass 2. With the pass
// already running when the input arrived, and under A3, a response is
// committed within ACMP_MBX_RX_ACCESSES and an event's action within
// ACMP_MBX_EVT_ACCESSES. An adp record is taken by pass
// CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) (21, adp_mbx.h's A1), so an
// ENTITY_AVAILABLE or ENTITY_DEPARTING behind a full adp ring reaches every
// matching sink within ACMP_MBX_ADP_RX_ACCESSES (H-DISC). Owed frames (A3):
// at most ACMP_OWED_MAX (8) wait, and a poll sends one per pass, so a
// response with k owed ahead of it is committed in pass k + 1 after the room
// returns, k <= 7.
//
// In time (A4): the per-path figures are under 0.1 ms at an assumed 1 us per
// access, which this lane has not measured. The full-backlog figures are
// stated against T_svc = 10 ms and the 20 ms ACMP ceiling (200 ms, Milan v1.2
// Table 5.26, x 10 %) in docs/design/MAILBOX_SPLIT.md, with what they require
// of the access time.

#ifndef ACMP_MBX_H
#define ACMP_MBX_H

#include <stdbool.h>
#include <stdint.h>

#include "acmp.h"
#include "adp_mbx.h"
#include "ctrl_loop.h"
#include "mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

// Mailbox accesses of one service pass, per response path (see above).
#define ACMP_MBX_LAT_BIND 72u           // BIND_RX -> response, PROBE_TX, TMR_NO_RESP: 1 + 1 + 22 + 1 + 22 + 22 + 2 + 1
#define ACMP_MBX_LAT_UNBIND 48u         // UNBIND_RX -> response, timer stopped: 1 + 1 + 22 + 1 + 22 + 1
#define ACMP_MBX_LAT_GET_RX 47u         // GET_RX_STATE -> response: 1 + 1 + 22 + 22 + 1
#define ACMP_MBX_LAT_PROBE_RESP 28u     // PROBE_TX_RESPONSE -> TMR_NO_TK or TMR_RETRY armed: 1 + 1 + 22 + 1 + 2 + 1
#define ACMP_MBX_LAT_TALKER 47u         // PROBE_TX / GET_TX_STATE / DISCONNECT_TX -> response: 1 + 1 + 22 + 22 + 1
#define ACMP_MBX_LAT_TIMER_PROBE 34u    // TMR_DELAY or TMR_NO_RESP -> PROBE_TX, TMR_NO_RESP: 6 + 1 + 22 + 2 + 3
#define ACMP_MBX_LAT_TIMER_ARM 13u      // TMR_NO_RESP (second) / TMR_RETRY / TMR_NO_TK -> next timer: 6 + 1 + 1 + 2 + 3
#define ACMP_MBX_LAT_AVAILABLE 35u      // ENTITY_AVAILABLE -> TMR_DELAY armed: 1 + 25 + 3 + 1 + 1 + 2 + 2
#define ACMP_MBX_LAT_DEPARTING 30u      // ENTITY_DEPARTING -> timer stopped or re-armed: 1 + 25 + 2 + 2
#define ACMP_MBX_LAT_NO_ADP 12u         // TMR_NO_ADP -> TK_NOT_DISCOVERED, timer re-armed: 6 + 1 + 2 + 3

// The costliest action per input, and the pass and path bounds they compose.
#define ACMP_MBX_EVENT_MAX 4u           // per event: the clock, the seed and a re-arm
#define ACMP_MBX_SINK_WORK 22u          // per sink and pass: one probe frame
#define ACMP_MBX_DISC_MAX 7u            // an ADP record's discovery: gPTP 3, clock 1, seed 1, re-arm 2
#define ACMP_MBX_HANDLER_MAX 47u        // an ACMP record: BIND, 1 + 22 + 22 + 2
#define ACMP_MBX_POLL_MAX 22u           // one owed frame
#define ACMP_MBX_RX_RECORD_MAX (2u + MBX_RX_HDR_WORDS + MBX_CH_ACMP_MAX_FRAME_BYTES / 4u)
#define ACMP_MBX_ADP_HANDLER_MAX (ADP_MBX_HANDLER_MAX > ACMP_MBX_DISC_MAX ? ADP_MBX_HANDLER_MAX : ACMP_MBX_DISC_MAX)
#define ACMP_MBX_PASS_MAX                                                                                          \
	(CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + ADP_MBX_SINK_MAX + ACMP_MBX_EVENT_MAX) +                 \
	 ACMP_MAX_SINKS * ACMP_MBX_SINK_WORK +                                                                     \
	 CTRL_LOOP_RX_PER_PASS * (ADP_MBX_RX_RECORD_MAX + (ACMP_MBX_ADP_HANDLER_MAX)) +                            \
	 CTRL_LOOP_RX_PER_PASS * (ACMP_MBX_RX_RECORD_MAX + ACMP_MBX_HANDLER_MAX) + MBX_N_IF * ADP_MBX_POLL_MAX +    \
	 ACMP_MBX_POLL_MAX)
// A1 for the acmp ring: its smallest record is a frame through talker_entity_id.
#define ACMP_MBX_RX_MIN_RECORD_WORDS (MBX_RX_HDR_WORDS + (MBX_CH_ACMP_T0_OFFSET + MBX_TERM_FIELD_BYTES + 3u) / 4u)
#define ACMP_MBX_RX_BACKLOG (MBX_CH_ACMP_RX_WORDS / ACMP_MBX_RX_MIN_RECORD_WORDS)
#define ACMP_MBX_RX_PASSES ((ACMP_MBX_RX_BACKLOG + CTRL_LOOP_RX_PER_PASS - 1u) / CTRL_LOOP_RX_PER_PASS)
#define ACMP_MBX_EVT_ACCESSES ((CTRL_LOOP_EVT_PASSES + 1u) * ACMP_MBX_PASS_MAX)
#define ACMP_MBX_RX_ACCESSES ((ACMP_MBX_RX_PASSES + 1u) * ACMP_MBX_PASS_MAX)
// H-DISC: an ENTITY_AVAILABLE or ENTITY_DEPARTING behind a full adp ring.
#define ACMP_MBX_ADP_RX_ACCESSES ((CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) + 1u) * ACMP_MBX_PASS_MAX)
// An owed response: k <= ACMP_OWED_MAX - 1 ahead of it, one per pass.
#define ACMP_MBX_OWED_PASSES ACMP_OWED_MAX
#define ACMP_MBX_OWED_ACCESSES ((ACMP_MBX_OWED_PASSES + 1u) * ACMP_MBX_PASS_MAX)

struct acmp_mbx_if {
	uint8_t slot;           // the fabric timer slot this interface's sinks share
	bool armed;             // the slot holds an arm of ours
	uint16_t tag;           // that arm's tag
	uint16_t tag_seq;       // the last tag issued
	uint32_t stale_expiries;// expiries of an arm that is no longer current
};

struct acmp_mbx {
	struct acmp acmp;
	struct acmp_mbx_if ifs[MBX_N_IF];
	struct acmp_ports ports;
	struct ctrl_loop_rx adp_next;   // the adp channel's handler the tap stands in front of
};

// The core on the mailbox, interface i's timer on slot first_slot + i. False
// when the slots do not fit the fabric's timer bank, the configuration names
// more interfaces than the mailbox has, or the core refuses it.
bool acmp_mbx_init(struct acmp_mbx *m, const struct acmp_config *cfg, const struct acmp_env *env,
		   unsigned first_slot);

// Bind the acmp channel, the event sink and the poll into the loop, and stand
// in front of the adp channel's handler (see above). False when no handler is
// bound to the adp channel yet (ADP attaches first) or a table is full.
bool acmp_mbx_attach(struct acmp_mbx *m, struct ctrl_loop *l);

#ifdef __cplusplus
}
#endif

#endif // ACMP_MBX_H
