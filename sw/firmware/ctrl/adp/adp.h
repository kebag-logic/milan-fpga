// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// adp.h - the ADP advertise slice, a portable C11 ports-and-adapters module
// (#665 lane F0; the shape lwSRP has, as the owner directive of 2026-10-05
// asks of every protocol).
//
// THE CORE KNOWS NO MAILBOX. One instance per AVB interface implements Milan
// v1.2 5.6.3, the Advertise state machine, over IEEE 1722.1-2021 6.2's
// ADPDU. Everything outside the state machine is a port the integrator
// provides (struct adp_ports): sending a frame, one timer per interface, the
// gPTP grandmaster and domain, the link level and a seed. The mailbox adapter
// (adp_mbx.h) is one implementation of those ports; the unit tests' fake is
// another. The core allocates nothing, reaches no global, and every call
// returns after a bounded number of steps.
//
//   * ENTITY_AVAILABLE on its schedule (5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.5,
//     5.6.3.5.9): a random TMR_DELAY, the frame, then TMR_ADVERTISE (5 s),
//     with available_index incremented after each one sent (IEEE
//     1722.1-2021 6.2.2.15; Figure 6-2, WAITING);
//   * the ENTITY_DISCOVER answer (5.6.3.1, 5.6.3.5.4): entity_id 0 or this
//     entity, in WAITING only;
//   * the re-advertise on a grandmaster change (5.6.3.5.7);
//   * ENTITY_DEPARTING on SHUTDOWN (5.6.3.5.8, 5.6.3.5.11), never on a link
//     change (5.6.3.5.6, 5.6.3.5.10). It carries the CURRENT available_index:
//     Figure 6-3's DEPARTING calls txEntityDeparting(), which sets every
//     field but the per-interface ones from entityInfo (6.2.5.2.2), and only
//     Figure 6-2's INITIALIZE zeroes it. 6.2.2.15's reset to 0 "when
//     transmitting an ENTITY_DEPARTING" therefore shows on the next start's
//     first ENTITY_AVAILABLE, which carries 0 (the ruling on PR #668,
//     comment 5994972330).
//
// The ADPDU's fields are the entity model's (struct adp_entity, generated
// from the end-station config by adp_entity.py, the same derivation the
// fabric's ADP engine is fed from) plus the gPTP pair sampled when the frame
// is built. The listener's discovery machine (5.6.4) feeds ACMP and is left
// to that lane (F3).

#ifndef ADP_H
#define ADP_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define ADP_ETHERTYPE 0x22F0u           // IEEE 1722-2016 Table 5 (AVTP)
#define ADP_SUBTYPE 0xFAu               // IEEE 1722.1-2021 6.2.2.1
#define ADP_MULTICAST_MAC 0x91E0F0010000ull // IEEE 1722.1-2021 Table B.1, the ADP and ACMP destination
#define ADP_HEADER_BYTES 14u            // the untagged Ethernet header
#define ADP_PDU_BYTES 68u               // IEEE 1722.1-2021 Figure 6-1
#define ADP_FRAME_BYTES 82u             // header + ADPDU
#define ADP_CONTROL_DATA_LENGTH 56u     // IEEE 1722.1-2021 6.2.2.6
#define ADP_VALID_TIME 10u              // Milan v1.2 5.6.2: 2 s units, so a 5 s cadence
#define ADP_ADVERTISE_MS 5000u          // Milan v1.2 Table 5.50, TMR_ADVERTISE
#define ADP_DELAY_MAX_MS 4000u          // Milan v1.2 Table 5.50, TMR_DELAY
#define ADP_DELAY_STARTUP_MAX_MS 2000u  // Milan v1.2 5.6.3.5.2

// IEEE 1722.1-2021 Table 6-1
#define ADP_MSG_ENTITY_AVAILABLE 0u
#define ADP_MSG_ENTITY_DEPARTING 1u
#define ADP_MSG_ENTITY_DISCOVER 2u

// Milan v1.2 Table 5.49, coded as the processor's dbg_adv_state so the two
// implementations' walks compare state for state.
enum adp_state {
	ADP_STATE_DOWN = 0,
	ADP_STATE_DELAY = 2,
	ADP_STATE_WAITING = 3,
};

// What the interface's one timer holds.
enum adp_timer {
	ADP_TIMER_NONE = 0,
	ADP_TIMER_DELAY,        // TMR_DELAY
	ADP_TIMER_ADVERTISE,    // TMR_ADVERTISE
};

// The two random-delay draws Milan distinguishes.
enum adp_draw {
	ADP_DRAW_NONE = 0,
	ADP_DRAW_STARTUP,       // 5.6.3.5.2: 0 to 2 s
	ADP_DRAW_DELAY,         // every other entry into DELAY: 0 to 4 s
};

// A frame the core still owes the wire because the send port had no room.
enum adp_pending {
	ADP_PENDING_NONE = 0,
	ADP_PENDING_AVAILABLE,
	ADP_PENDING_DEPARTING,
};

// The ADPDU fields the entity model fixes.
struct adp_entity {
	uint64_t entity_id;
	uint64_t entity_model_id;
	uint64_t mac;                       // 48-bit source address
	uint32_t entity_capabilities;
	uint16_t talker_stream_sources;
	uint16_t talker_capabilities;
	uint16_t listener_stream_sinks;
	uint16_t listener_capabilities;
	uint16_t identify_control_index;
};

// The ports the core calls. Every pointer is required; `ctx` is passed back.
struct adp_ports {
	void *ctx;
	// Queue one frame on `interface`; true when it was taken, false when there
	// is no room now (the core keeps it and retries from adp_poll).
	bool (*send)(void *ctx, unsigned interface, const uint8_t *frame, size_t len);
	// Start (or restart, replacing) the interface's one timer; it calls
	// adp_timer_expired once, delay_ms later, unless stopped or restarted.
	void (*timer_start)(void *ctx, unsigned interface, uint32_t delay_ms);
	void (*timer_stop)(void *ctx, unsigned interface);
	// The gPTP grandmaster identity and domain of the interface, now.
	void (*gptp)(void *ctx, unsigned interface, uint64_t *gm_id, uint8_t *domain);
	// The link level of the interface, now.
	bool (*link_up)(void *ctx, unsigned interface);
	// Entropy mixed into the random delays when the machine starts.
	uint32_t (*seed)(void *ctx);
};

struct adp {
	const struct adp_entity *entity;
	const struct adp_ports *ports;
	uint8_t interface;                  // the AVB interface and interface_index
	enum adp_state state;
	bool enabled;                       // started (Milan v1.2 5.6.1)
	bool link_up;                       // the level the machine last acted on
	uint32_t available_index;
	uint16_t current_configuration_index;
	enum adp_timer timer;               // what the port's timer holds
	uint32_t rng;                       // xorshift32 state of the random delays
	enum adp_pending pending;
	uint32_t pending_index;             // available_index the pending frame carries
	// diagnostics
	uint32_t gm_changed;                // GPTP_GM_CHANGED
	uint32_t draws;                     // random delays drawn
	uint32_t last_draw_ms;
	enum adp_draw last_draw;
	uint32_t stray_expiries;            // an expiry with no timer running
	uint32_t discarded;                 // ADPDUs discarded (Milan v1.2 5.6.3.1)
	uint32_t deferred_sends;            // sends the port had no room for
};

void adp_init(struct adp *a, const struct adp_entity *entity, const struct adp_ports *ports,
	      unsigned interface, uint16_t current_configuration_index);

// Start (5.6.3.5.1, 5.6.3.5.2) or shut down (SHUTDOWN) the machine.
void adp_set_enable(struct adp *a, bool enable);

// The configuration the next ADPDU carries (IEEE 1722.1-2021 6.2.2.18).
void adp_set_current_configuration(struct adp *a, uint16_t index);

// Inputs: a received frame, the timer's expiry, the link and the grandmaster.
void adp_rx(struct adp *a, const uint8_t *frame, size_t len);
void adp_timer_expired(struct adp *a);
void adp_link_change(struct adp *a, bool up);
void adp_gm_change(struct adp *a);

// Retry a frame the send port had no room for; true while one is still owed.
bool adp_poll(struct adp *a);

// The ADPDU this instance would send now, built into frame[ADP_FRAME_BYTES].
void adp_build(const struct adp *a, uint8_t message_type, uint32_t available_index, uint8_t *frame);

#ifdef __cplusplus
}
#endif

#endif // ADP_H
