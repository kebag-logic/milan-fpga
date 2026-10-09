// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// adp_mbx.h - the ADP slice's mailbox adapter: struct adp_ports on the packet
// mailbox, and the bindings into the bare-metal event loop (#665 lane F0).
//
//   send         -> a TX record on the ADP channel (mbx_tx_send)
//   timer_start  -> fabric timer slot `first_slot + interface`, armed at
//                   NOW_MS + delay with a fresh tag
//   timer_stop   -> TMR_CMD cancel of that slot
//   gptp         -> the interface's GM_LO/GM_HI/DOMAIN snapshot
//   link_up      -> LINK
//   seed         -> NOW_MS
//
// and from the loop: the ADP channel's RX records to adp_rx, the TIMER event
// of a slot to adp_timer_expired when its tag is the current arm's (an
// expiry that raced a stop or a restart carries an older tag and is counted,
// never acted on: the mailbox form of Milan v1.2 Table 5.51's "x" cells), the
// LINK and GM events of an interface to adp_link_change and adp_gm_change,
// and a poll that retries a frame the transmit ring had no room for and
// tells the loop it is still owed, so the loop does not sleep on it.
//
// SERVICE LATENCY (the D3 ruling on #640: a deterministic bound per response
// path, stated and tested), under the assumptions A1 to A4 of ctrl_loop.h.
//
// One path's own cost. Every input is handled inside the pass that takes it,
// with a fixed number of mailbox accesses and no wait on the fabric, and its
// response is committed there when A3 holds (otherwise see owed frames).
// ADP_MBX_LAT_* is that number for ONE pass with nothing else pending,
// derived below and counted access by access on the host model (test_adp.cpp,
// C0 to C6), which fails a path that exceeds it:
//
//   an event record    EVT_HEAD + 4 words + EVT_TAIL                    6
//   an ADP RX record   RX_HEAD + 2 header + 21 payload + RX_TAIL        25
//   a TX record        TX_TAIL + 2 header + 21 payload + TX_HEAD        25
//   a timer arm        NOW_MS + TMR_DEADLINE + TMR_CMD                  3
//   a timer stop       TMR_CMD                                          1
//   the gPTP sample    GM_LO + GM_HI + DOMAIN                           3
//   the pass's tail    EVT_HEAD (ring empty) + RX_HEAD (ring empty)     2
//
// At 82 bytes an ADPDU is 21 payload words.
//
// The bound with a backlog. A pass of F0's composition (ADP the only bound
// channel and the only sink and poll) costs at most ADP_MBX_PASS_MAX:
//
//   events  8 x (6 + 31)   a record, then the costliest sink action, a
//                          TMR_DELAY expiry (the frame 25, the gPTP sample
//                          3, TMR_ADVERTISE armed 3)
//   ticks   16 x T         T = a centisecond consumer's accesses (F0 binds
//                          none; lwSRP's states its own)
//   RX      2 x (36 + 4)   RX_HEAD, 2 header words, 32 payload words (the
//                          channel's max_frame_bytes, 128), RX_TAIL, then
//                          the costliest handler (a DISCOVER in WAITING: the
//                          stop 1, TMR_DELAY armed 3)
//   polls   N_IF x 31      one frame at most: an owed ENTITY_AVAILABLE sent,
//                          TMR_ADVERTISE armed (an owed DEPARTING, 28)
//
// (a ring that runs dry ends its stage with one read, which the full count
// above already exceeds). An event is taken by pass CTRL_LOOP_EVT_PASSES (2)
// and an ADP record by pass CTRL_LOOP_RX_PASSES(256) (21: the ring holds 42
// records of the smallest frame the filter passes), counted from the first
// pass that starts after the fabric posted it, and under A3 its response is
// committed in that pass. With the pass already running when the input
// arrived, that is ADP_MBX_EVT_ACCESSES and ADP_MBX_RX_ACCESSES mailbox
// accesses from input to committed response. test_adp.cpp (F0 to F7) fills
// both rings with legal records, coalesces ticks behind them, and fails a
// pass or a path that exceeds these figures.
//
// Owed frames (A3). A frame the transmit ring had no room for is sent by the
// poll, one per pass, the oldest first. An ENTITY_AVAILABLE has at most
// ADP_DEPARTING_OWED_MAX (2) ENTITY_DEPARTINGs owed ahead of it (adp.h). With
// k of them owed when the room returns, it is committed in pass k + 1 counted
// from the first pass that starts after the room returned, or in the pass
// that takes its TMR_DELAY expiry if that comes later (by pass 2, as any
// event). Either way it is committed by pass ADP_MBX_OWED_PASSES (3), counted
// from the first pass that starts after both the room's return and the
// expiry's posting, and with a pass already running then, within
// ADP_MBX_OWED_ACCESSES (4 x 407 = 1,628) accesses. A DEPARTING has at most
// one owed ahead of it. test_adp.cpp E5 runs 1, 2 and 64 SHUTDOWNs behind a full
// ring through the driver, the model and the loop, the expiry taken before
// and after the room returns, and fails a commit later than pass k + 1 or
// beyond these figures.
//
// In time (A4): at an assumed 1 us per access, which this lane has not
// measured, the RX figure is under 9 ms, against Milan v1.2's 0 to 4 s
// TMR_DELAY and 5 s TMR_ADVERTISE (Table 5.50) and the 20 s a listener ages
// the entity out by (valid_time 10).

// No synchronous callbacks (#678): a port must return before any core
// input is dispatched by the single bare-metal event loop. A port never
// calls back into a protocol core or the store, including on zero-delay
// timer arms or TX completion. Interrupts defer dispatch to the loop.
// F2 to F5 inherit this rule for every protocol port.

#ifndef ADP_MBX_H
#define ADP_MBX_H

#include <stdbool.h>
#include <stdint.h>

#include "adp.h"
#include "ctrl_loop.h"
#include "mbx.h"

#ifdef __cplusplus
extern "C" {
#endif

// Mailbox accesses of one service pass, per response path.
#define ADP_MBX_LAT_DISCOVER 31u        // RX ENTITY_DISCOVER -> TMR_DELAY armed: 1 + 25 + 1 + 3 + 1
#define ADP_MBX_LAT_DELAY 39u           // TIMER -> ENTITY_AVAILABLE and TMR_ADVERTISE: 6 + 3 + 25 + 3 + 2
#define ADP_MBX_LAT_ADVERTISE 11u       // TIMER -> TMR_DELAY armed: 6 + 3 + 2
#define ADP_MBX_LAT_GM 11u              // GM event -> TMR_DELAY armed: 6 + 3 + 2
#define ADP_MBX_LAT_LINK 11u            // LINK up -> TMR_DELAY armed: 6 + 3 + 2 (down, a stop: 9)
#define ADP_MBX_LAT_SHUTDOWN 29u        // disable -> ENTITY_DEPARTING committed: 1 + 3 + 25 (no pass)

// The costliest action per input, and the pass and path bounds they compose.
#define ADP_MBX_SINK_MAX 31u            // an event: TMR_DELAY expiry, 25 + 3 + 3
#define ADP_MBX_HANDLER_MAX 4u          // an RX record: DISCOVER in WAITING, 1 + 3
#define ADP_MBX_POLL_MAX 31u            // a poll: the owed ENTITY_AVAILABLE, 25 + 3 + 3
#define ADP_MBX_RX_RECORD_MAX (2u + MBX_RX_HDR_WORDS + MBX_CH_ADP_MAX_FRAME_BYTES / 4u)
#define ADP_MBX_PASS_MAX                                                                  \
	(CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + ADP_MBX_SINK_MAX) +                 \
	 CTRL_LOOP_RX_PER_PASS * (ADP_MBX_RX_RECORD_MAX + ADP_MBX_HANDLER_MAX) + MBX_N_IF * ADP_MBX_POLL_MAX)
#define ADP_MBX_EVT_ACCESSES ((CTRL_LOOP_EVT_PASSES + 1u) * ADP_MBX_PASS_MAX)
#define ADP_MBX_RX_ACCESSES ((CTRL_LOOP_RX_PASSES(MBX_CH_ADP_RX_WORDS) + 1u) * ADP_MBX_PASS_MAX)
// An owed ENTITY_AVAILABLE: the later of k + 1 <= 3 and the event's pass 2.
#define ADP_MBX_OWED_PASSES \
	(ADP_DEPARTING_OWED_MAX + 1u > CTRL_LOOP_EVT_PASSES ? ADP_DEPARTING_OWED_MAX + 1u : CTRL_LOOP_EVT_PASSES)
#define ADP_MBX_OWED_ACCESSES ((ADP_MBX_OWED_PASSES + 1u) * ADP_MBX_PASS_MAX)

struct adp_mbx_if {
	struct adp adp;
	uint8_t slot;           // the fabric timer slot this interface owns
	bool armed;             // the slot holds an arm of ours
	uint16_t tag;           // that arm's tag
	uint16_t tag_seq;       // the last tag issued
	uint32_t stale_expiries;// expiries of an arm that is no longer current
};

struct adp_mbx {
	struct adp_mbx_if ifs[MBX_N_IF];
	struct adp_ports ports;
	uint32_t foreign_if;    // records or events naming an interface with no instance
};

// One instance per interface, timer slots first_slot .. first_slot + N_IF - 1.
// False when the slots do not fit the fabric's timer bank.
bool adp_mbx_init(struct adp_mbx *m, const struct adp_entity *entity, unsigned first_slot,
		  uint16_t current_configuration_index);

// Bind the ADP channel, the event sink and the poll into the loop.
bool adp_mbx_attach(struct adp_mbx *m, struct ctrl_loop *l);

// Start or shut down every interface's machine.
void adp_mbx_set_enable(struct adp_mbx *m, bool enable);

#ifdef __cplusplus
}
#endif

#endif // ADP_MBX_H
