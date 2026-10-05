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
// and a poll that retries a frame the transmit ring had no room for.
//
// SERVICE LATENCY (the D3 ruling on #640: a deterministic bound per response
// path, stated and tested). Every input is handled inside the service pass
// that takes it, with a fixed number of mailbox accesses and no wait on the
// fabric. ADP_MBX_LAT_* is that number for ONE pass of the F0 composition
// (ADP the only bound channel, nothing else pending), derived below and
// counted access by access on the host model (test_adp.c, C0 to C6), which
// fails a path that exceeds it. An input that arrives while a pass runs waits
// at most for that pass to end, so the response is committed within two
// passes of the input reaching the mailbox. Each further bound channel adds
// one RX_HEAD read to every pass, and each further record a pass takes adds
// its own cost; CTRL_LOOP_EVENTS_PER_PASS and CTRL_LOOP_RX_PER_PASS cap both.
//
//   an event record    EVT_HEAD + 4 words + EVT_TAIL                    6
//   an ADP RX record   RX_HEAD + 2 header + 21 payload + RX_TAIL        25
//   a TX record        TX_TAIL + 2 header + 21 payload + TX_HEAD        25
//   a timer arm        NOW_MS + TMR_DEADLINE + TMR_CMD                  3
//   a timer stop       TMR_CMD                                          1
//   the gPTP sample    GM_LO + GM_HI + DOMAIN                           3
//   the pass's tail    EVT_HEAD (ring empty) + RX_HEAD (ring empty)     2
//
// At 82 bytes an ADPDU is 21 payload words. Milan v1.2's tightest ADP timing
// is the 0 to 4 s TMR_DELAY and the 5 s TMR_ADVERTISE (Table 5.50), against
// a 10-unit valid_time (20 s) a listener ages the entity out by; two passes of
// at most 40 accesses each add microseconds on any bus, a margin of more
// than five orders of magnitude.

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
