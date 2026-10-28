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
// LOCK: the LOCK_ENTITY state moved (a lock, an unlock or its expiry), before
// the response or the notification that reports it (#665).
enum aecp_change {
	AECP_CHANGE_CONFIGURATION, AECP_CHANGE_FORMAT, AECP_CHANGE_LATENCY,
	AECP_CHANGE_RATE, AECP_CHANGE_CLOCK, AECP_CHANGE_NAME, AECP_CHANGE_MAP,
	AECP_CHANGE_IDENTIFY, AECP_CHANGE_SYSTEM_ID, AECP_CHANGE_LOCK
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
	// storage. This is the persistence/physical-apply notification port;
	// whether the apply completed is read through applied.
	void (*changed)(void *, enum aecp_change, uint16_t, uint16_t);
	// START/STOP is ACMP-owned. Queue a request; later call aecp_start_done.
	void (*start)(void *, uint16_t, bool);
	// Physical format support is an integrator decision, separate from maps.
	bool (*format)(void *, uint16_t, uint16_t, uint64_t);
	// Current ADP owner value for the ingress interface (IEEE 7.2.1/6.2.2.15).
	uint32_t (*available_index)(void *, unsigned);
	// Whether every change given to changed is applied: false while an apply
	// waits for an acknowledgement it has not had (#665). While it is false
	// the lock check refuses every change, ENTITY_MISBEHAVING (ENTITY_LOCKED
	// where another controller holds the lock in force), before it changes
	// anything. A change of face state (AECP_WAITS) after which it is
	// false is undone and answered IN_PROGRESS; it is done again, answered and
	// notified once this is true within AECP_WAIT_MS, else it stays undone and
	// answers ENTITY_MISBEHAVING. A lock released at its expiry holds, by its
	// owner, for every response and read until this is true, and is then
	// notified (docs/ARCHITECTURE_HW_SW_SPLIT.md section 1; Milan v1.2
	// 5.4.2.2, 5.4.5.2; IEEE 1722.1-2021 7.5.2, 9.3.2.6).
	bool (*applied)(void *);
};
// The commands whose change a face commit carries: LOCK_ENTITY,
// SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and
// SET_CONTROL, one bit per command_type (#665).
#define AECP_WAITS 0x01404142u
// How long such a change waits for applied, from its command: its final
// response then follows the IN_PROGRESS within the 120 ms cadence, and the
// command within 240 ms (IEEE 1722.1-2021 9.3.2.6).
#define AECP_WAIT_MS 100u
// A command's own response at most: SET_STREAM_INFO's, the longest of
// AECP_WAITS.
#define AECP_HELD_BYTES (38u + 84u)
// The values one command of AECP_WAITS changes at most: LOCK_ENTITY's three,
// or SET_CONFIGURATION's configuration, override and the ENTITY copy of each of
// two configurations; a further copy, which READ_DESCRIPTOR never reads, is not
// kept (the builder ships one configuration).
#define AECP_KEPT 4u
struct aecp_kept {
	uint8_t *at;
	uint8_t n;
	uint8_t was[8];
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
	// A change the platform has not applied (#665): the command waits, its
	// change undone and its response held, until applied or wait_deadline.
	bool waiting;
	bool refusing;          // the lock check refuses every change
	bool unlocked;          // a lock released at its expiry, held until applied
	uint8_t kept;
	struct aecp_kept keep[AECP_KEPT];   // what the command changed, as it found it
	enum aecp_change noted;
	uint16_t noted_type;
	uint16_t noted_index;
	uint32_t wait_deadline;
	uint64_t held_requester;
	unsigned held_interface;
	size_t held_bytes;
	uint8_t held[AECP_HELD_BYTES];
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
