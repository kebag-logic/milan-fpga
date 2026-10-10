// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx.h - the portable mailbox driver: rings, doorbells, the interrupt, time,
// fabric timers and events (#665 lane F0).
//
// This is the layer every protocol adapter is written against. It is
// portable C11: every fabric access goes through mbx_hal.h's three bus
// functions, every layout comes from the generated mbx_contract.h, and it
// allocates nothing, so the same file runs on the on-chip RISC-V, on a hard
// core and on the host against the mailbox model.
//
// The doorbells are the counter writes the contract defines: releasing an RX
// record writes RX_TAIL, committing a TX record writes TX_HEAD, consuming an
// event writes EVT_TAIL. The fabric holds the one interrupt high while an RX
// ring or the event ring holds a record (IRQ_STATUS levels), so a service
// pass that drains them leaves the line low.

// No synchronous callbacks (#678): a port must return before any core
// input is dispatched by the single bare-metal event loop. A port never
// calls back into a protocol core or the store, including on zero-delay
// timer arms or TX completion. Interrupts defer dispatch to the loop.
// F2 to F5 inherit this rule for every protocol port.

#ifndef MBX_H
#define MBX_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "mbx_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

enum mbx_status {
	MBX_STATUS_OK = 0,      // done
	MBX_STATUS_EMPTY,       // nothing to take
	MBX_STATUS_FULL,        // the transmit ring has no room for the record now
	MBX_STATUS_BAD,         // refused: a malformed record or argument
};

// One received frame, copied out of its receive ring.
struct mbx_frame {
	uint16_t len;                           // frame bytes
	uint8_t interface;                      // interface it arrived on
	uint32_t arrival_ms;                    // NOW_MS at its last byte
	uint8_t bytes[MBX_FRAME_BYTES_MAX];     // Ethernet header first, no FCS
};

// One fabric event, its four words decoded by type.
struct mbx_event {
	uint8_t type;           // MBX_EV_TYPE_*
	uint8_t interface;
	uint16_t seq;
	uint8_t timer_slot;     // TIMER
	uint16_t timer_tag;     // TIMER: the tag of the arm that expired
	uint32_t deadline_ms;   // TIMER
	uint32_t now_ms;        // TIMER, LINK and TICK: NOW_MS at posting
	bool link_up;           // LINK
	uint64_t gm_id;         // GM
	uint8_t domain;         // GM
	uint16_t tick_count;    // TICK: centiseconds since the previous TICK
};

// Check the window's ID and CAPS against the contract this firmware was built
// against and take the current counters. False means the bitstream carries
// another contract: the caller must not open a channel.
bool mbx_open(void);

// The filter's entity_id (OWN_EID), its channel gates (FILTER_EN) and the
// MAAP range of the range_overlap test.
void mbx_filter_set_own_eid(uint64_t entity_id);
void mbx_filter_open(uint32_t channel_mask);
void mbx_filter_set_maap_range(uint64_t base, uint16_t count);
// The 48-bit own unicast MAC of an interface (OWN_MAC_LO/HI), the destination
// an `own` match tuple takes on a frame that arrived on that interface. False,
// writing nothing, for an interface the contract does not have.
bool mbx_filter_set_own_mac(unsigned interface, uint64_t mac);
// Entry `entry` of an interface's bound-talker table (BOUND_EID, BOUND_EN):
// with bound, the adp channel passes that talker's ENTITY_AVAILABLE and
// ENTITY_DEPARTING on that interface (the eq_bound term); without, the entry
// no longer takes part. BOUND_EN is cleared before the identity is written, so
// a half-written entry never matches. False, writing nothing, for an interface
// or an entry the contract does not have.
bool mbx_filter_set_bound_talker(unsigned interface, unsigned entry, bool bound, uint64_t talker_entity_id);
// The publication block (contract 2.2): the class-D state the firmware
// owner publishes for interface `interface`'s datapath in the split placement
// (#665, comment 6088423771). Each call writes one register, and returns
// false, writing nothing, for an interface or a sink the contract does not
// have. The caller writes each value before it sends the response that
// promises it (docs/ARCHITECTURE_HW_SW_SPLIT.md, section 1).
//   mbx_pub_da_gate     DA_GATE: bit s, MAAP holds source s's destination address
//   mbx_pub_licence     LICENCE: bit s, source s holds its SRP licence
//   mbx_pub_idle_slope  IDLE_SLOPE: the bandwidth SRP admitted, bits per second
//   mbx_pub_domain      SR_DOMAIN: the operational SR class A priority and VID,
//                       and whether they were adopted from a received Domain
//   mbx_pub_talker_decl TALKER_DECL: bit s, source s has a Talker declaration
bool mbx_pub_da_gate(unsigned interface, uint32_t open);
bool mbx_pub_licence(unsigned interface, uint32_t active);
bool mbx_pub_idle_slope(unsigned interface, uint32_t bps);
bool mbx_pub_domain(unsigned interface, bool adopted, uint8_t priority, uint16_t vid);
bool mbx_pub_talker_decl(unsigned interface, uint32_t declared);
// Sink `sink`'s entry, for a stream_id that moved: whether it is bound and
// started, and the stream_id it settled on, 0 for none. BINDING is written
// first, with SID_VALID clear; a nonzero stream_id is then written to SID_LO
// and SID_HI and published by setting SID_VALID, so a half-written stream_id
// never reaches the datapath. One write without a stream_id, four with one.
bool mbx_pub_sink(unsigned interface, unsigned sink, bool bound, bool started, uint64_t stream_id);
// Sink `sink`'s BINDING alone, for a stream_id that did not move: whether it is
// bound and started, with SID_VALID as the entry holds it, so the stream_id
// stays on the datapath through the write. One write.
bool mbx_pub_sink_binding(unsigned interface, unsigned sink, bool bound, bool started, bool sid_valid);
// FILTER_MISMATCH: untagged frames of a control EtherType that matched no
// channel's tuple, saturating at 0xFFFF.
uint16_t mbx_filter_mismatch(void);

// Copy channel ch's next RX record into *f and release it (RX_TAIL).
// EMPTY when the ring is empty; BAD when the record is malformed, in which
// case the ring is resynchronised to RX_HEAD.
enum mbx_status mbx_rx_take(unsigned ch, struct mbx_frame *f);

// Snapshot the published RX prefix and test whether the consumed cursor is
// still at or before it. A lifecycle consumer can discard that prefix for
// one interface while retaining other interfaces. Check on each bounded
// pass; comparison is modulo 2^16 and must not span 32768 consumed words.
uint16_t mbx_rx_mark(unsigned ch);
bool mbx_rx_before(unsigned ch, uint16_t mark);

// Write one frame as a TX record of channel ch and commit it (TX_HEAD).
// FULL when the ring lacks the room now; BAD for a length outside 14 to the
// channel's max_frame_bytes or an unknown interface. Frames leave in the
// order they were committed, across every channel.
enum mbx_status mbx_tx_send(unsigned ch, unsigned interface, const uint8_t *frame, uint16_t len);

// Take the next fabric event and release it (EVT_TAIL); false when none.
bool mbx_event_take(struct mbx_event *ev);

// NOW_MS, the time base of every timer deadline.
uint32_t mbx_now_ms(void);

// Arm a fabric timer slot to expire at deadline_ms with the caller's tag, or
// cancel it. An expiry already posted keeps the tag of the arm it belongs to.
void mbx_timer_arm(unsigned slot, uint16_t tag, uint32_t deadline_ms);
void mbx_timer_cancel(unsigned slot);

// Start or stop the centisecond TICK events (TICK_CTL.EN).
void mbx_tick_enable(bool enable);

// The link level and the grandmaster of an interface, read coherently.
bool mbx_link_up(unsigned interface);
uint64_t mbx_gm_id(unsigned interface, uint8_t *domain);

// The interrupt: the raw causes, the enables, and the sticky error.
uint32_t mbx_irq_status(void);
void mbx_irq_enable(uint32_t mask);
void mbx_irq_clear_err(void);

#ifdef __cplusplus
}
#endif

#endif // MBX_H
