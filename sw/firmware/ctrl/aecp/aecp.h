// SPDX-License-Identifier: CERN-OHL-W-2.0
// IEEE 1722.1-2021 7.4/7.5 and Milan v1.2 5.4. Single event-loop owner.
#ifndef CTRL_AECP_H
#define CTRL_AECP_H
#include "aecp_model.h"

#ifdef __cplusplus
extern "C" {
#endif

#define AECP_INTERFACES 2u
// The registered controllers of one AVB Interface, at most (Milan v1.2 5.3.4.2): every registry and fan-out derives
// from this constant, so the recipients of a notice are 16 at one interface and at most 32 at two, each registration on
// its own port (Milan v1.2 5.4.5.1).
#define AECP_REGISTRATIONS 16u
#define AECP_FRAME_BYTES 1514u
#define AECP_PATH_ITEMS 64u
#define AECP_MAP_PAGE 176u
// A notice whose observation port is unavailable is retried 1, 2, 4, then
// every 8 ms until it is built (#665: a 1 ms retry rebuilt every pending
// notice each millisecond). Only notices wait on it: a solicited response
// never does (aecp_ready), so the 240 ms response bound of IEEE 1722.1-2021
// 9.3.2.6 (9.2.1.2.5 in 1722.1-2013) and Milan v1.2 5.4.3.4 is untouched.
// A retry is deferrable (THE RETRY, ctrl_loop.h): with aecp.retry_hold set, as
// aecp_mbx sets it, aecp_poll builds no notice and holds a due retry, arming no
// timer for it and reporting it owed, and only aecp_retry builds or tries one,
// in a round the event loop calls in a pass that took no input and dispatched
// no centisecond, after an aged step or a build (THE TRANSMIT), or in a pass of
// its own once aecp_retry_aged reports a notice waiting and the last round's
// pace passed. So once the port answers, the notice of Milan v1.2 5.4.5.2 and
// Table 5.22 is built at its next retry, within AECP_RETRY_MAX_MS, in the round
// that follows, under any input, a backlog or input that leaves no pass empty
// included, and committed to every recipient in that pass. A datapath reset can
// leave AECP_NOTICES_MOST notices pending at once, each round taking what its
// pass has room for: FR_NFR.md 3.4.1 bounds the first of them by AECP_NOTICE_MS
// from its port's answer and those queued behind it by AECP_QUEUED_MS, which
// aecp_mbx.h derives. That holds while nothing waits ahead of a round: a
// response owed is committed first (ctrl_loop.h, A3), and while a command waits
// on its apply (AECP_WAIT_MS) or a START or STOP is pending no round builds.
// Measured from the port's answer to the last recipient's commit, under every
// receive channel at its refill rate with its bursts and a grandmaster change
// as every pass starts, with a save in flight (the CPU budget harness's notice
// groups, eight phases of the spacing, with and without the drafts): MEASURED-ONE
// and MEASURED-QUEUE (docs/design/SPLIT_CONTROL_MEMORY.md section 13).
// GET_COUNTERS keeps its one-second spacing, and the 60 s unlock and the
// controller monitor of Milan v1.2 5.4.2.2 and 5.4.5.3 are not retries.
#define AECP_RETRY_MAX_MS 8u
// The longest frame the fan port takes: every notice's but a long GET_AS_PATH's.
#define AECP_FAN_BYTES 256u
// What a refused attempt charges its round, in microseconds: a round of AECP_ROUND_PORTS refusals costs about 20,500
// CPU cycles past its first attempt's cold misses, the walk of the events included. So a round spends at most what it
// is given (aecp_retry): each attempt starts with a notice's time left, and each refused one is charged.
#define AECP_ATTEMPT_US 34u
// The ports a round tries, one attempt each: GET_STREAM_INFO's and GET_COUNTERS', which a notice reads through the
// first interface's window, and each AVB interface's GET_AVB_INFO and GET_AS_PATH, through its own. A port is a window
// read, which answers for all it serves or for none (#665).
#define AECP_ROUND_PORTS (2u + 2u * MBX_N_IF)
// The most notices a datapath reset can leave pending, one for every observation of every descriptor that has one:
// each stream's GET_STREAM_INFO and GET_COUNTERS, each AVB interface's GET_AVB_INFO, GET_AS_PATH and GET_COUNTERS, each
// clock domain's GET_COUNTERS, at the fixture's two shapes. The CPU budget harness holds the model to it.
#define AECP_NOTICES_MOST (MBX_N_IF == 1u ? 12u : 40u)
// A notification's bound, min(T_svc, the 24 ms notification ceiling), of
// FR_NFR.md 3.4.1: from a retried notice's port answer to its last
// recipient's commit, no extra budget at a retry.
#define AECP_NOTICE_MS 20u
// aecp_find's index (#665) holds a run per descriptor type of IEEE 1722.1-2021
// Table 7-1, ENTITY (0x0000) to PTP_PORT (0x0028), for the first
// AECP_INDEXED_CONFIGURATIONS configurations: every shipped model has one.
// A key outside them is scanned for, as before.
#define AECP_DESCRIPTOR_TYPES 0x29u
#define AECP_INDEXED_CONFIGURATIONS 1u
// An aecp_run.count for a key whose descriptors are not one run.
#define AECP_RUN_SCAN 0xffffu

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
	// A notice's frame with no completion of its own, or NULL, when send takes
	// every frame: the same delivery, committed by the next fan or by fan_end at
	// the latest, which gives the notice's last frame cookie's completion and is
	// false when it has no room for it (#665).
	bool (*fan)(void *, unsigned, const uint8_t *, size_t);
	bool (*fan_end)(void *, uint32_t cookie);
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
	uint8_t retry_ms;  // the next retry's wait, 0 before the first (AECP_RETRY_MAX_MS)
	uint16_t next;     // the next event in aecp.live: its descriptor index + 1, 0 at the end
	uint16_t awaited_next; // the next event in aecp.awaited, as next
};
// One key's descriptors, at model positions first + 0 .. first + count - 1,
// each at the position of its index: count 0 when the model has none, and
// AECP_RUN_SCAN when they are anywhere else.
struct aecp_run {
	uint16_t first;
	uint16_t count;
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
	bool retry_hold; // a due retry waits for aecp_retry (THE RETRY, ctrl_loop.h; #665)
	bool retry_held; // with retry_hold, a notice waits for aecp_retry: arm armed no timer for it
	uint8_t refused; // the ports that refused this round (AECP_ROUND_PORTS), one bit each
	int32_t round_us; // what this round has left, in microseconds
	int32_t notice_us; // what a notice costs a round, set by its owner with retry_hold
	uint32_t retry_pace; // when the next round given a pass may start
	// The events holding a notice or a retry, in descriptor order, linked through
	// aecp_event.next: the first one's index + 1, 0 when none. The event scans walk
	// only these (#665).
	uint16_t live;
	// Bit n of used[i]: registry[i][n].used. The registry scans visit only these (#665).
	uint16_t used[AECP_INTERFACES];
	// aecp_find's index of the model's keys, which aecp_init builds and nothing
	// rewrites after it (#665): runs[c][t] holds configuration c's descriptors
	// of type t.
	struct aecp_run runs[AECP_INDEXED_CONFIGURATIONS][AECP_DESCRIPTOR_TYPES];
	uint16_t awaited; // the events whose snapshot awaits its frame's completion, the list aecp_tx_complete walks
	// On a line of the data cache: what a recipient changes of a frame stays in one, which the record mover's read
	// takes back from the cache each frame (#665).
	uint8_t response[AECP_FRAME_BYTES] __attribute__((aligned(64)));
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
// THE RETRY's round (ctrl_loop.h, #665): at most `notices` notices built from
// what its pass has left, left_us, each charged notice_us and each refused
// attempt AECP_ATTEMPT_US, one attempt a port, then the timer armed for the
// next. Only while no response or notice is owed, as aecp_poll builds one. True
// while a notice or a due retry still waits or the built notice is owed.
bool aecp_retry(struct aecp *, unsigned notices, int32_t left_us);
// THE RETRY's age (ctrl_loop.h, #665): true when a held retry's time is age_ms
// or more past, on the now_ms port, and nothing waits ahead of aecp_retry's
// round, so the loop gives the round a pass of its own.
bool aecp_retry_aged(struct aecp *, uint32_t pace_ms);
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
