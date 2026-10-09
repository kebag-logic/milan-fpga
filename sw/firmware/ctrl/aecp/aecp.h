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
	uint64_t stream_id, dest_mac, failure_bridge_id;
	uint32_t flags, latency, flags_ex;
	uint16_t vlan;
	uint8_t failure_code, probing_status, acmp_status;
	bool bound, running;
};
struct aecp_avb_info {
	uint64_t gm_id;
	uint32_t propagation_delay;
	uint8_t domain, flags, class_priority;
	uint16_t class_vlan;
};
struct aecp_counters {
	uint32_t valid;
	uint32_t value[32];
};
struct aecp_mapping {
	uint16_t stream, channel, cluster, cluster_channel;
};
// One pool per descriptor; storage is supplied by the shape, never allocated.
// Defaults are the model's power-on routing, not a copy of mutable live state.
struct aecp_map {
	uint16_t type, index, configuration, page_channels;
	struct aecp_mapping *rows;
	size_t count, capacity;
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
};
struct aecp_registration {
	uint64_t controller, mac;
	uint32_t deadline;
	uint16_t sequence, probe_sequence;
	uint8_t probing; // 0 monitor, 1 first probe, 2 retry
	bool used;
};
// One event row per descriptor. Counter eligibility is shared by every
// recipient of that descriptor's snapshot.
struct aecp_event {
	uint32_t counter_at;
	uint32_t cookie;
	uint8_t pending;
	bool counter_sent, awaiting_output;
	uint8_t overrides; // bit 0 scalar, bit 1 latency: a default-valued SET counts
};
struct aecp_config {
	uint64_t entity_id, mac[AECP_INTERFACES];
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
	uint64_t lock_owner, system_id, requester;
	uint32_t lock_deadline, now;
	uint16_t configuration, probe_sequence;
	uint8_t identify;
	bool locked, in_port, open, start_pending;
	uint8_t response[AECP_FRAME_BYTES];
	size_t response_bytes;
	unsigned response_interface, recipient;
	bool response_owed, notify;
	int probe_recipient;
	size_t counter_event;
	uint32_t start_deadline;
	uint32_t tx_cookie;
	uint32_t malformed, ignored, busy_drops, reentries;
};

bool aecp_init(struct aecp *, const struct aecp_config *, const struct aecp_ports *);
void aecp_open(struct aecp *);
bool aecp_ready(const struct aecp *);
void aecp_rx(struct aecp *, unsigned interface, const uint8_t *, size_t);
bool aecp_poll(struct aecp *);
void aecp_start_done(struct aecp *, bool success, bool changed);
// departure_ms is the final output beat's time, or a later observation of it.
// A later cookie for the same descriptor supersedes an earlier completion.
void aecp_tx_complete(struct aecp *, uint32_t cookie, uint32_t departure_ms);
// Table 5.22 events: bit 0 STREAM_INFO, bit 1 AVB_INFO, bit 2 AS_PATH,
// bit 3 COUNTERS. Call after causal ACMP responses have committed (#653).
void aecp_changed(struct aecp *, uint16_t type, uint16_t index, unsigned events);
bool aecp_locked(const struct aecp *, uint64_t *owner);

#ifdef CTRL_REENTRY_ASSERT
void ctrl_reentry_assert(const char *module);
#endif
#ifdef __cplusplus
}
#endif
#endif
