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

// Copy channel ch's next RX record into *f and release it (RX_TAIL).
// EMPTY when the ring is empty; BAD when the record is malformed, in which
// case the ring is resynchronised to RX_HEAD.
enum mbx_status mbx_rx_take(unsigned ch, struct mbx_frame *f);

// Write one frame as a TX record of channel ch and commit it (TX_HEAD).
// FULL when the ring lacks the room now; BAD for a length outside 14 to the
// channel's max_frame_bytes or an unknown interface.
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
