// SPDX-License-Identifier: CERN-OHL-W-2.0
// IEEE 1722.1-2021 7.4/7.5 and Milan v1.2 5.4. Single event-loop owner.
#ifndef CTRL_AECP_H
#define CTRL_AECP_H
#include "aecp_model.h"

#ifdef __cplusplus
extern "C" {
#endif

#define AECP_INTERFACES 2u
#define AECP_REGISTRATIONS 16u
#define AECP_FRAME_BYTES 1514u
#define AECP_PATH_ITEMS 64u
#define AECP_MAP_PAGE 176u
// A notice whose observation port is unavailable is retried 1, 2, 4, then
// every 8 ms until it is built (#665: a 1 ms retry rebuilt every pending
// notice each millisecond). Only notices wait on it: a solicited response
// never does (aecp_ready), so the 240 ms response bound of IEEE 1722.1-2021
// 9.3.2.6 (9.2.1.2.5 in 1722.1-2013) and Milan v1.2 5.4.3.4 is untouched.
// Once the port answers, the notice of Milan v1.2 5.4.5.2 and Table 5.22 is
// built within 8 ms plus the pass that takes it, inside T_svc = 10 ms and
// the 24 ms notification ceiling of FR_NFR.md 3.4.1; GET_COUNTERS keeps its
// one-second spacing, and the 60 s unlock and the controller monitor of
// Milan v1.2 5.4.2.2 and 5.4.5.3 are not retries.
#define AECP_RETRY_MAX_MS 8u

enum aecp_status {
	AECP_SUCCESS = 0, AECP_NOT_IMPLEMENTED = 1, AECP_NO_SUCH_DESCRIPTOR = 2,
	AECP_ENTITY_LOCKED = 3, AECP_ENTITY_ACQUIRED = 4, AECP_NOT_AUTHENTICATED = 5,
	AECP_AUTHENTICATION_DISABLED = 6, AECP_BAD_ARGUMENTS = 7, AECP_NO_RESOURCES = 8,
	AECP_IN_PROGRESS = 9, AECP_ENTITY_MISBEHAVING = 10, AECP_NOT_SUPPORTED = 11,
	AECP_STREAM_IS_RUNNING = 12
};

struct aecp_stream_info {
	uint64_t stream_id;
	uint64_t dest_mac;
	uint64_t failure_bridge_id;
	uint32_t flags;
	uint32_t latency;
	uint32_t flags_ex;
	uint16_t vlan;
	uint8_t failure_code;
	uint8_t probing_status;
	uint8_t acmp_status;
	bool bound;
	bool running;
};
struct aecp_avb_info {
	uint64_t gm_id;
	uint32_t propagation_delay;
	uint8_t domain;
	uint8_t flags;
	uint8_t class_priority;
	uint16_t class_vlan;
};
struct aecp_counters {
	uint32_t valid;
	uint32_t value[32];
};
struct aecp_mapping {
	uint16_t stream;
	uint16_t channel;
	uint16_t cluster;
	uint16_t cluster_channel;
};
// One pool per descriptor; storage is supplied by the shape, never allocated.
// Defaults are the model's power-on routing, not a copy of mutable live state.
struct aecp_map {
	uint16_t type;
	uint16_t index;
	uint16_t configuration;
	uint16_t page_channels;
	struct aecp_mapping *rows;
	size_t count;
	size_t capacity;
	const struct aecp_mapping *defaults;
	size_t default_count;
};
enum aecp_change {
	AECP_CHANGE_CONFIGURATION, AECP_CHANGE_FORMAT, AECP_CHANGE_LATENCY,
	AECP_CHANGE_RATE, AECP_CHANGE_CLOCK, AECP_CHANGE_NAME, AECP_CHANGE_MAP,
	AECP_CHANGE_IDENTIFY, AECP_CHANGE_SYSTEM_ID
};
// All ports are required. They return without delivering ANY protocol input.
// A port may publish an observation or apply a hardware value synchronously;
// completion/event delivery is deferred to the event loop (#678).
struct aecp_ports {
	void *ctx;
	// Completion identifies the accepted cookie, after the final output beat.
	// Deliver aecp_tx_complete later, never from inside send.
	bool (*send)(void *, unsigned, const uint8_t *, size_t, uint32_t cookie);
	uint32_t (*now_ms)(void *);
	uint32_t (*random)(void *);
	void (*timer)(void *, bool, uint32_t);
	bool (*stream)(void *, unsigned, uint16_t, uint16_t, struct aecp_stream_info *);
	bool (*avb)(void *, unsigned, uint16_t, struct aecp_avb_info *);
	bool (*path)(void *, unsigned, uint16_t, uint64_t *, size_t, size_t *);
	bool (*counters)(void *, unsigned, uint16_t, uint16_t, struct aecp_counters *);
	// Called only after a validated change. The value remains in core-owned
	// storage. This is the persistence/physical-apply notification port.
	void (*changed)(void *, enum aecp_change, uint16_t, uint16_t);
	// START/STOP is ACMP-owned. Queue a request; later call aecp_start_done.
	void (*start)(void *, uint16_t, bool);
	// Physical format support is an integrator decision, separate from maps.
	bool (*format)(void *, uint16_t, uint16_t, uint64_t);
	// Current ADP owner value for the ingress interface (IEEE 7.2.1/6.2.2.15).
	uint32_t (*available_index)(void *, unsigned);
};
struct aecp_registration {
	uint64_t controller;
	uint64_t mac;
	uint32_t deadline;
	uint16_t sequence;
	uint16_t probe_sequence;
	uint8_t probing; // 0 monitor, 1 first probe, 2 retry
	bool used;
};
// One event row per descriptor. Counter eligibility is shared by every
// recipient of that descriptor's snapshot.
struct aecp_event {
	uint32_t counter_at;
	uint32_t cookie;
	uint32_t retry_at;
	uint8_t pending;
	uint8_t retry_pending;
	bool counter_sent;
	bool awaiting_output;
	uint8_t overrides; // bit 0 scalar, bit 1 latency: a default-valued SET counts
	uint8_t retry_ms;  // the next retry's wait, 0 before the first (AECP_RETRY_MAX_MS)
	uint16_t next;     // the next event in aecp.live: its descriptor index + 1, 0 at the end
};
struct aecp_config {
	uint64_t entity_id;
	uint64_t mac[AECP_INTERFACES];
	unsigned interfaces;
	struct aecp_model *model;
	struct aecp_map *maps;
	size_t map_count;
	struct aecp_event *events; // model->count entries
	uint32_t *latency; // one entry per STREAM_OUTPUT descriptor
};
struct aecp {
	struct aecp_config cfg;
	const struct aecp_ports *ports;
	struct aecp_registration registry[AECP_INTERFACES][AECP_REGISTRATIONS];
	uint64_t lock_owner;
	uint64_t system_id;
	uint64_t requester;
	uint32_t lock_deadline;
	uint32_t now;
	uint16_t configuration;
	uint16_t probe_sequence;
	uint8_t identify;
	bool locked;
	bool in_port;
	bool open;
	bool start_pending;
	bool notices; // an event may hold a notice or a retry: the event scans run only then (#665)
	// The events holding a notice or a retry, in descriptor order, linked through
	// aecp_event.next: the first one's index + 1, 0 when none. The event scans walk
	// only these (#665).
	uint16_t live;
	// Bit n of used[i]: registry[i][n].used. The registry scans visit only these (#665).
	uint16_t used[AECP_INTERFACES];
	unsigned awaiting; // events whose snapshot awaits its frame's completion: aecp_tx_complete scans only then
	uint8_t response[AECP_FRAME_BYTES];
	size_t response_bytes;
	unsigned response_interface;
	unsigned recipient;
	bool response_owed;
	bool notify;
	int probe_recipient;
	size_t counter_event;
	uint32_t start_deadline;
	uint32_t tx_cookie;
	uint32_t malformed;
	uint32_t ignored;
	uint32_t busy_drops;
	uint32_t reentries;
};

bool aecp_init(struct aecp *, const struct aecp_config *, const struct aecp_ports *);
void aecp_open(struct aecp *);
bool aecp_ready(struct aecp *);
void aecp_rx(struct aecp *, unsigned interface, const uint8_t *, size_t);
bool aecp_poll(struct aecp *);
void aecp_start_done(struct aecp *, bool success, bool changed);
// departure_ms is the final output beat's time, or a later observation of it.
// A later cookie for the same descriptor supersedes an earlier completion.
void aecp_tx_complete(struct aecp *, uint32_t cookie, uint32_t departure_ms);
// Table 5.22 events: bit 0 STREAM_INFO, bit 1 AVB_INFO, bit 2 AS_PATH,
// bit 3 COUNTERS. Call after causal ACMP responses have committed (#653).
void aecp_changed(struct aecp *, uint16_t type, uint16_t index, unsigned events);
bool aecp_locked(struct aecp *, uint64_t *owner);

#ifdef CTRL_REENTRY_ASSERT
void ctrl_reentry_assert(const char *module);
#endif
#ifdef __cplusplus
}
#endif
#endif
