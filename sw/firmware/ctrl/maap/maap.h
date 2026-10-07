// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// IEEE 1722-2016 Annex B: one static machine per interface and address range.
// Ports never call back synchronously. The single event loop delivers all
// inputs, including timer expiries (#678). Every port returns without waiting.
#ifndef CTRL_MAAP_H
#define CTRL_MAAP_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define MAAP_POOL_BASE UINT64_C(0x91e0f0000000)
#define MAAP_POOL_SIZE 0xfe00u                  // B.4, Table B.9
#define MAAP_MULTICAST UINT64_C(0x91e0f000ff00) // B.4, Table B.10
#define MAAP_FRAME_BYTES 60u
#define MAAP_PROBE_RETRANSMITS 3u              // B.3.3, Table B.8
#define MAAP_PROBE_BASE_MS 500u
#define MAAP_PROBE_VARIATION_MS 100u
#define MAAP_ANNOUNCE_BASE_MS 30000u
#define MAAP_ANNOUNCE_VARIATION_MS 2000u
#define MAAP_SERVICE_MS 10u
#define MAAP_QUEUE_FRAMES 16u

enum maap_state { MAAP_INITIAL, MAAP_PROBE, MAAP_DEFEND };
enum maap_message { MAAP_MSG_PROBE = 1, MAAP_MSG_DEFEND = 2, MAAP_MSG_ANNOUNCE = 3 };

struct maap_ports {
	void *ctx;
	// True means the complete frame was committed. False leaves it owed.
	bool (*send)(void *ctx, unsigned interface, const uint8_t *frame, size_t len);
	void (*timer_start)(void *ctx, unsigned interface, uint32_t delay_ms);
	void (*timer_stop)(void *ctx, unsigned interface);
	// The filter follows a tentative range too; consumers use only valid=true.
	// count=0 withdraws the range. This port also invalidates stream addresses.
	void (*range)(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid);
	// Least-significant bits of the local real-time clock, B.3.6.1.
	uint32_t (*clock)(void *ctx);
};

struct maap {
	const struct maap_ports *ports;
	uint64_t mac;
	uint64_t base;
	uint16_t count;
	uint8_t interface;
	enum maap_state state;
	uint32_t rng;
	uint32_t last_delay_ms;
	uint8_t probe_count;
	bool enabled;
	bool operational;
	bool timer_running;
	bool expiry_owed;
	bool valid;
	bool in_call;
	uint8_t queue[MAAP_QUEUE_FRAMES][MAAP_FRAME_BYTES];
	unsigned queued;
	// Modulo-2^32 diagnostics; overflow is failed service, never success.
	uint32_t conflicts;
	uint32_t discarded;
	uint32_t stale_expiries;
	uint32_t deferred;
	uint32_t overflow;
	uint32_t reentries;
};

// All pointers and port functions are required. Init is used only before
// binding the machine. Invalid interface, address or count returns false.
bool maap_init(struct maap *m, const struct maap_ports *ports, unsigned interface,
	       uint64_t mac, uint16_t count);
// Begin! in INITIAL only. preferred=0 draws; otherwise a valid pool range
// is used under Table B.7 note a. An invalid preferred range is refused.
bool maap_begin(struct maap *m, uint64_t preferred);
void maap_release(struct maap *m);
// Link down withdraws; link up implements PortOperational!, including
// re-probing an active range. The event loop suppresses duplicate link levels.
void maap_port_operational(struct maap *m, bool up);
void maap_rx(struct maap *m, const uint8_t *frame, size_t len);
void maap_timer_expired(struct maap *m);
// At most two sends, enough for the final retransmission then ANNOUNCE.
// True keeps the event loop awake while output or a deferred expiry is owed.
bool maap_poll(struct maap *m);

#ifdef __cplusplus
}
#endif
#endif
