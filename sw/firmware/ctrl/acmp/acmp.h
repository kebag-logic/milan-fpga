// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp.h - Milan connection management on the bare-metal core, a portable
// C11 ports-and-adapters module (#665 lane F3).
//
// THE CORE KNOWS NO MAILBOX. One instance per entity implements Milan v1.2
// 5.5 (connection management, which supersedes IEEE 1722.1-2021 clause 8's
// connect sequence for these commands, 5.5.2.1) and 5.6.4 (the listener's
// discovery machine) over IEEE 1722.1-2021 8.2.1's ACMPDU. Everything outside
// the state machines is a port: the transport (struct acmp_ports: frames,
// time, one timer per AVB interface, the gPTP pair, a seed), which the
// mailbox adapter (acmp_mbx.h) or a test provides, and the entity's other
// owners (struct acmp_env: the lock, the talker's sources, the listener's
// SRP, the saved-state store, the notifier), which the integrator provides.
// The core allocates nothing, reaches no global, and every call returns after
// a bounded number of steps.
//
//   ONLY AVTP VERSION 0 IS READ. A received ACMPDU or ADPDU whose AVTP version
//   (frame byte 15, bits 6:4) is not 0, the only version IEEE 1722.1-2021
//   8.2.1.3 and 6.2.2.3 define, is discarded before any field is decoded or
//   anything changes (IEEE 1722-2016 4.4.3.4), and counted as malformed.
//
//   THE LISTENER (5.5.3). One sink per STREAM_INPUT, each with the eight
//   states of Table 5.28 and every transition of Table 5.30 (5.5.3.5.1 to
//   5.5.3.5.48). BIND_RX, UNBIND_RX and GET_RX_STATE with listener_entity_id
//   this entity, and PROBE_TX_RESPONSE with listener_entity_id this entity
//   (5.5.3.1); every other ACMP message is ignored. A command naming a sink
//   that does not exist is answered LISTENER_UNKNOWN_ID (Table 5.27); a
//   PROBE_TX_RESPONSE naming one is ignored.
//
//   RESPONSES KEY ON THE CONSUMER'S UNIQUE ID. A PROBE_TX_RESPONSE belongs to
//   the sink its listener_unique_id names (5.5.3.1), never to whichever sink
//   probes that talker source, and it is that sink's only when its
//   controller_entity_id, talker_entity_id, talker_unique_id and sequence_id
//   equal the PROBE_TX_COMMAND the sink sent (5.5.3.5.18 step 1): the fields
//   are the sent probe's, kept with it, not the binding's, which a re-bind
//   of the same talker may have updated since (5.5.3.5.17 step 2).
//
//   PROBING, TIMEOUTS AND SEQUENCE IDS. A probe is sent at once after a bind
//   (5.5.3.5.3) or after a random TMR_DELAY of 0 to 1 s (Table 5.29) once the
//   talker is discovered; TMR_NO_RESP is 200 ms (Table 5.26) from the send the
//   port accepts, of the probe and of its duplicate alike (5.5.3.5.3 steps 5
//   to 7, 5.5.3.5.16): a probe that waits for transmit room holds its
//   TMR_NO_RESP until acmp_poll sends it; its first
//   expiry sends an exact duplicate, same sequence_id (5.5.3.5.16), its
//   second sets ACMP status LISTENER_TALKER_TIMEOUT and TMR_RETRY 4 s
//   (5.5.3.5.23); a failed response sets the status it carries and TMR_RETRY
//   (5.5.3.5.18 step 3); a settled sink waits TMR_NO_TK 10 s for its talker
//   attribute (5.5.3.5.18 step 4, 5.5.3.5.36). Every new PROBE_TX_COMMAND
//   takes the next sequence_id of one counter per instance (IEEE 1722.1-2021
//   8.2.1.15); a duplicate does not.
//
//   THE LOCK (5.5.2.4, 5.5.2.5). A BIND_RX or UNBIND_RX from a controller
//   other than the locking one is refused CONTROLLER_NOT_AUTHORIZED, which
//   is 16 (IEEE 1722.1-2021 Table 8-3), before anything changes.
//
//   THE TALKER (5.5.4). Stateless (5.5.2.7): PROBE_TX (5.5.4.1, Tables 5.40
//   to 5.43), DISCONNECT_TX (5.5.4.2, Tables 5.44 and 5.45: SUCCESS for a
//   valid source, nothing changes; 5.5.2.7's "always returns SUCCESS" is an
//   overview that defers to 5.5.4, whose 5.5.4.2 validates the source first),
//   GET_TX_STATE (5.5.4.3, Tables 5.46 and 5.47) and
//   GET_TX_CONNECTION (5.5.4.4, Table 5.48: NOT_SUPPORTED), each with
//   talker_entity_id this entity (IEEE 1722.1-2021 8.2.1.9). The first three
//   naming a source that does not exist are answered TALKER_UNKNOWN_ID
//   (Tables 5.40, 5.44 and 5.46). A PROBE_TX that
//   ingressed on another interface than the source's is answered
//   INCOMPATIBLE_REQUEST (Table 5.41), one of the two answers 5.5.4.1 step 2
//   permits. The source's stream, destination MAC, VLAN and SRP state are
//   read from the env's source port when the answer is built.
//
//   DISCOVERY (5.6.4). One machine per sink, running while the sink is bound
//   (5.5.3.5.2 step 1, 5.5.3.5.3 step 4). An ENTITY_AVAILABLE or
//   ENTITY_DEPARTING is processed by every bound sink whose talker it names
//   (5.6.4.1) and whose AVB interface it arrived on (the per-interface key,
//   which the GM check of 5.6.4.5.1 step 1 reads "on this port"). TMR_NO_ADP
//   is the received valid_time in two-second units (IEEE 1722.1-2021
//   6.2.2.5); every Table 5.54 transition and guard of 5.6.4.5.1 to 5.6.4.5.4
//   is implemented, and the EVT_TK_DISCOVERED and EVT_TK_DEPARTED it raises
//   drive the sink's connection machine in the same call. The transport's
//   admit port is told which talker each bound sink names, as its binding
//   changes, so the ingress passes that talker's ENTITY_AVAILABLE and
//   ENTITY_DEPARTING on the sink's interface (the mailbox's bound-talker
//   table, #665 comment 6029368753) and the machine still filters exactly.
//
//   KEYED PER AVB INTERFACE. Each sink and source carries the AVB interface
//   its descriptor is on: a sink's probes leave on it (5.5.3.5.3 step 5), a
//   source answers only probes that arrived on it (5.5.4.1 step 2), and the
//   timers of the sinks on one interface share that interface's one timer
//   port, armed at the earliest deadline among them. The redundancy path
//   (Milan v1.2 8) needs nothing but a second interface index.
//
//   SAVED STATE. A sink's binding is a 20-byte record (the processor's
//   KL_acmp_nvm_shadow BINDING payload, docs/design/SAVED_STATE_FASTCONNECT.md
//   2: flags {bound, started, STREAMING_WAIT}, a reserved byte, then
//   talker_unique_id, talker_entity_id and controller_entity_id, big-endian).
//   acmp_restore_binding() is the F1 store's binding walk (nvm_state.h
//   apply): a saved binding starts its sink as 5.5.3.5.2 does, in
//   PRB_W_AVAIL with discovery running; acmp_restore_rollback() drops every
//   one. A change to a saved field calls env->persist (5.5.2.4: saved to
//   non-volatile memory), and acmp_binding_latch() gives the record back to
//   the store's write path. Whether a change is then written is the store's
//   rule (an unread slot holds its writer, ctrl_nvm/README.md, "Boot" 9).
//
//   RESPONSE BEFORE NOTIFICATION (#653). A change of a sink's observable state
//   (struct acmp_sink_view) is reported through env->changed, and a change a
//   command caused is reported only once that command's response has been
//   taken by the send port: an AECP notifier keyed on env->changed can never
//   put the notice ahead of the response, even when the response waited for
//   transmit room. acmp_change_pending() says which sinks hold one.
//
// A FRAME THE SEND PORT REFUSES IS OWED, never reordered: up to
// ACMP_OWED_MAX frames wait, in order, for acmp_poll(), and nothing passes
// them. A command that would add a response to a full queue is dropped
// before it changes anything (busy_drops). An owed probe's TMR_NO_RESP starts
// when acmp_poll sends it, provided its sink still waits for that probe (the
// same sequence_id); a probe that finds the queue full is counted lost
// (probes_lost) and its TMR_NO_RESP, run from the attempt, recovers it.
//
// PORTS NEVER CALL BACK INTO THE CORE SYNCHRONOUSLY (#678). Every expiry,
// every frame and every SRP event is delivered by the one event loop, never
// from inside a port call. The core guards it: a flag is set around each
// port call, and an entry while it is set does nothing but count
// (`reentries`) and, in a build with CTRL_REENTRY_ASSERT defined (the host
// tests'), call ctrl_reentry_assert(), which a debug platform defines to stop.

#ifndef ACMP_H
#define ACMP_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifndef ACMP_MAX_SINKS
#define ACMP_MAX_SINKS 16u              // STREAM_INPUTs: the saved-state binding block holds 16
#endif
#ifndef ACMP_MAX_SOURCES
#define ACMP_MAX_SOURCES 16u            // STREAM_OUTPUTs
#endif
#define ACMP_MAX_INTERFACES 4u          // AVB interfaces (the mailbox CAPS.N_IF field is 4 bits)
#define ACMP_OWED_MAX 8u                // frames waiting for transmit room, at most
#define ACMP_AVTP_VERSION 0u            // IEEE 1722.1-2021 8.2.1.3 (ACMP) and 6.2.2.3 (ADP)

#define ACMP_ETHERTYPE 0x22F0u          // IEEE 1722-2016 Table 5 (AVTP)
#define ACMP_SUBTYPE 0xFCu              // IEEE 1722-2016 Table 6; IEEE 1722.1-2021 8.2.1.1
#define ACMP_MULTICAST_MAC 0x91E0F0010000ull // IEEE 1722.1-2021 Table B.1; 8.2.1: every ACMPDU goes to it
#define ACMP_HEADER_BYTES 14u           // the untagged Ethernet header
#define ACMP_PDU_BYTES 56u              // Milan v1.2 5.5.2.2: the truncated ACMPDU
#define ACMP_FRAME_BYTES 70u            // header + ACMPDU
#define ACMP_CONTROL_DATA_LENGTH 44u    // the 56-byte PDU less its 12-byte common header
#define ACMP_BINDING_BYTES 20u          // the saved binding payload (see the top of this file)

// Milan v1.2 Table 5.26 and Table 5.29.
#define ACMP_TMR_NO_RESP_MS 200u
#define ACMP_TMR_RETRY_MS 4000u
#define ACMP_TMR_DELAY_MAX_MS 1000u
#define ACMP_TMR_NO_TK_MS 10000u
#define ACMP_VALID_TIME_UNIT_MS 2000u   // IEEE 1722.1-2021 6.2.2.5: two-second increments

// IEEE 1722.1-2021 Table 8-2, with Milan v1.2 5.5.2.2's names.
#define ACMP_MSG_PROBE_TX_COMMAND 0u
#define ACMP_MSG_PROBE_TX_RESPONSE 1u
#define ACMP_MSG_DISCONNECT_TX_COMMAND 2u
#define ACMP_MSG_DISCONNECT_TX_RESPONSE 3u
#define ACMP_MSG_GET_TX_STATE_COMMAND 4u
#define ACMP_MSG_GET_TX_STATE_RESPONSE 5u
#define ACMP_MSG_BIND_RX_COMMAND 6u
#define ACMP_MSG_BIND_RX_RESPONSE 7u
#define ACMP_MSG_UNBIND_RX_COMMAND 8u
#define ACMP_MSG_UNBIND_RX_RESPONSE 9u
#define ACMP_MSG_GET_RX_STATE_COMMAND 10u
#define ACMP_MSG_GET_RX_STATE_RESPONSE 11u
#define ACMP_MSG_GET_TX_CONNECTION_COMMAND 12u
#define ACMP_MSG_GET_TX_CONNECTION_RESPONSE 13u

// IEEE 1722.1-2021 Table 8-3, the codes this module sends or keeps.
#define ACMP_STATUS_SUCCESS 0u
#define ACMP_STATUS_LISTENER_UNKNOWN_ID 1u
#define ACMP_STATUS_TALKER_UNKNOWN_ID 2u
#define ACMP_STATUS_TALKER_DEST_MAC_FAIL 3u
#define ACMP_STATUS_LISTENER_TALKER_TIMEOUT 7u
#define ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED 16u
#define ACMP_STATUS_INCOMPATIBLE_REQUEST 17u
#define ACMP_STATUS_NOT_SUPPORTED 31u

// IEEE 1722.1-2021 Table 8-4 (bit 15 is the least significant) and Milan
// v1.2 Table 5.23 (REGISTERING_FAILED).
#define ACMP_FLAG_FAST_CONNECT 0x0002u
#define ACMP_FLAG_STREAMING_WAIT 0x0008u
#define ACMP_FLAG_REGISTERING_FAILED 0x0040u

// The ADPDU fields discovery reads (IEEE 1722.1-2021 Figure 6-1, 6.2.2).
#define ACMP_ADP_SUBTYPE 0xFAu
#define ACMP_ADP_FRAME_BYTES 82u        // header + the 68-byte ADPDU
#define ACMP_ADP_MSG_ENTITY_AVAILABLE 0u
#define ACMP_ADP_MSG_ENTITY_DEPARTING 1u

// Milan v1.2 Table 5.28, coded as the processor's lsm_state_e so the two
// implementations' walks compare state for state.
enum acmp_sink_state {
	ACMP_UNBOUND = 0,
	ACMP_PRB_W_AVAIL = 1,
	ACMP_PRB_W_DELAY = 2,
	ACMP_PRB_W_RESP = 3,
	ACMP_PRB_W_RESP2 = 4,
	ACMP_PRB_W_RETRY = 5,
	ACMP_SETTLED_NO_RSV = 6,
	ACMP_SETTLED_RSV_OK = 7,
};

// Milan v1.2 5.3.8.6: the probing_status GET_STREAM_INFO reports.
enum acmp_probing {
	ACMP_PROBING_DISABLED = 0,
	ACMP_PROBING_PASSIVE = 1,
	ACMP_PROBING_ACTIVE = 2,
	ACMP_PROBING_COMPLETED = 3,
};

// The one timer of a sink's connection machine (Table 5.29), and its
// discovery machine's TMR_NO_ADP, which runs beside it.
enum acmp_timer {
	ACMP_TIMER_NONE = 0,
	ACMP_TIMER_NO_RESP,
	ACMP_TIMER_RETRY,
	ACMP_TIMER_DELAY,
	ACMP_TIMER_NO_TK,
};

// A sink's binding parameters (5.5.2.4).
struct acmp_binding {
	uint64_t talker_entity_id;
	uint64_t controller_entity_id;
	uint16_t talker_unique_id;
	bool streaming_wait;
};

// SRP stream parameters (5.5.1.3: what settlement learns).
struct acmp_stream {
	uint64_t stream_id;
	uint64_t dest_mac;                      // 48 bits
	uint16_t vlan_id;
};

// What a STREAM_OUTPUT's owners say about it now (5.5.4.1, 5.5.4.3).
struct acmp_source_state {
	bool dest_mac_valid;                    // 5.5.4.1 step 3: MAAP holds a destination MAC for it
	struct acmp_stream stream;
	bool asking_failed;                     // Table 5.47: a Listener Asking Failed attribute is registered
};

// A sink's dynamic state (Milan v1.2 5.3.8.2 to 5.3.8.9). env->changed fires
// when one of Table 5.22's STREAM_INPUT items moves: bound, started,
// probing_status, acmp_status, the stream's three fields, talker_registered
// or registering_failed.
struct acmp_sink_view {
	enum acmp_sink_state state;
	bool bound;                             // 5.3.8.2
	struct acmp_binding binding;            // 5.3.8.3
	bool started;                           // 5.3.8.7, undefined (false) while unbound
	enum acmp_probing probing_status;       // 5.3.8.6
	uint8_t acmp_status;
	bool settled;                           // 5.3.8.5
	struct acmp_stream stream;              // 5.3.8.9: as the last PROBE_TX_RESPONSE gave it, 0 while not settled
	bool talker_registered;                 // 5.3.8.8: a matching Talker attribute (SETTLED_RSV_OK)
	bool registering_failed;                // ... and it is a Talker Failed
	bool talker_discovered;                 // 5.3.8.4
};

struct acmp_config {
	uint64_t entity_id;
	unsigned n_interfaces;                  // 1 to ACMP_MAX_INTERFACES
	uint64_t mac[ACMP_MAX_INTERFACES];      // each interface's source MAC, 48 bits
	unsigned n_sinks;                       // STREAM_INPUTs of the current configuration
	uint8_t sink_interface[ACMP_MAX_SINKS];
	unsigned n_sources;                     // STREAM_OUTPUTs
	uint8_t source_interface[ACMP_MAX_SOURCES];
};

// The transport. Every pointer is required; `ctx` is passed back. None may
// call back into the core (see the top of this file).
struct acmp_ports {
	void *ctx;
	// Queue one frame on `interface`; true when it was taken, false when there
	// is no room now (the core keeps it owed and retries from acmp_poll).
	bool (*send)(void *ctx, unsigned interface, const uint8_t *frame, size_t len);
	// Milliseconds, modulo 2^32, of the clock every deadline is on.
	uint32_t (*now_ms)(void *ctx);
	// The interface's one timer: arm it to call acmp_timer_expired once at
	// deadline_ms (replacing any arm), or, with armed false, stop it.
	void (*timer)(void *ctx, unsigned interface, bool armed, uint32_t deadline_ms);
	// The gPTP grandmaster identity and domain of the interface, now.
	void (*gptp)(void *ctx, unsigned interface, uint64_t *gm_id, uint8_t *domain);
	// Entropy mixed into the random TMR_DELAY.
	uint32_t (*seed)(void *ctx);
	// The ingress of `interface` passes the ENTITY_AVAILABLE and
	// ENTITY_DEPARTING of `talker_entity_id` for `sink` (one entry per sink),
	// or, with bound false, no longer for it. Called when a sink is bound,
	// unbound or bound to another talker, and by acmp_open for every binding
	// the store restored.
	void (*admit)(void *ctx, unsigned interface, unsigned sink, bool bound, uint64_t talker_entity_id);
};

// The entity's other owners. Every pointer is required; none may call back
// into the core.
struct acmp_env {
	void *ctx;
	// True when the entity is locked (Milan v1.2 5.3.4.1), with the locking
	// controller.
	bool (*locked)(void *ctx, uint64_t *controller_entity_id);
	// The STREAM_OUTPUT's state now.
	void (*source)(void *ctx, unsigned index, struct acmp_source_state *out);
	// Start listening with `stream` (5.5.3.5.18 step 4: initiate the SRP
	// reservation and listen for the stream's packets), or with NULL stop
	// and clear it (5.5.3.5.36 step 1).
	void (*srp)(void *ctx, unsigned sink, const struct acmp_stream *stream);
	// A saved field of the sink's binding changed: the store marks its record.
	void (*persist)(void *ctx, unsigned sink);
	// The sink's view changed (released after its response, see above).
	void (*changed)(void *ctx, unsigned sink);
};

struct acmp_sink {
	enum acmp_sink_state state;
	uint8_t interface;
	bool bound;
	bool started;
	struct acmp_binding binding;
	enum acmp_probing probing;
	uint8_t acmp_status;
	// the PROBE_TX_COMMAND last sent (5.5.3.5.3 step 6: its saved copy)
	uint64_t probe_controller;
	uint64_t probe_talker;
	uint16_t probe_talker_uid;
	uint16_t probe_seq;
	bool probe_retried;                     // the duplicate went (5.5.3.5.16)
	// settlement
	struct acmp_stream stream;              // env->srp holds it while settled
	bool tk_failed;                         // the registered Talker attribute is a Talker Failed
	// discovery (5.6.4)
	bool disc_running;
	bool discovered;
	uint16_t disc_interface_index;
	uint32_t disc_available_index;
	// timers, absolute milliseconds
	enum acmp_timer timer;
	uint32_t timer_deadline;
	bool timer_held;                        // TMR_NO_RESP waits for its owed probe to leave
	bool adp_armed;
	uint32_t adp_deadline;
	// what the admit port holds for the sink
	bool admitted;
	uint64_t admitted_talker;
	// notification (#653) and the store
	uint8_t change_owed;                    // owed frames whose leaving releases this sink's change
	struct acmp_sink_view reported;         // the view env->changed last reported
	uint8_t saved[ACMP_BINDING_BYTES];      // the record env->persist last announced
};

// A frame waiting for transmit room, and the sinks whose change it releases.
struct acmp_owed {
	uint8_t interface;
	uint8_t probe_of;                       // 1 + the sink whose PROBE_TX_COMMAND it is; 0 for a response
	uint32_t release;                       // bit s: sink s's change is reported once it leaves
	uint8_t frame[ACMP_FRAME_BYTES];
};

struct acmp {
	struct acmp_config cfg;
	const struct acmp_ports *ports;
	const struct acmp_env *env;
	struct acmp_sink sinks[ACMP_MAX_SINKS];
	uint16_t sequence_id;                   // the next PROBE_TX_COMMAND's (8.2.1.15)
	uint32_t rng;                           // xorshift32 state of TMR_DELAY
	bool seeded;                            // the seed port has been mixed in
	bool in_port;                           // a port call is running (#678)
	bool now_read;                          // `now` holds this entry's one clock read
	uint32_t now;
	bool timer_armed[ACMP_MAX_INTERFACES];  // what each interface's timer holds
	uint32_t timer_at[ACMP_MAX_INTERFACES];
	struct acmp_owed owed[ACMP_OWED_MAX];
	unsigned owed_head;
	unsigned owed_count;
	// diagnostics, each counted modulo 2^32
	uint32_t rx_ignored;                    // not addressed to this entity's talker or listener
	uint32_t rx_malformed;                  // not an ACMPDU this module can read (incl. another AVTP version)
	uint32_t unknown_sink;                  // LISTENER_UNKNOWN_ID answers and probe responses ignored for it
	uint32_t probe_mismatch;                // PROBE_TX_RESPONSEs that are not the sink's probe's
	uint32_t refused_locked;                // CONTROLLER_NOT_AUTHORIZED answers
	uint32_t adp_ignored;                   // ADPDUs no sink took, or none this module can read
	uint32_t impossible;                    // events Table 5.30 or 5.54 marks "x"
	uint32_t busy_drops;                    // commands dropped behind a full owed queue
	uint32_t probes_lost;                   // probes dropped behind a full owed queue
	uint32_t deferred_sends;                // sends the port had no room for
	uint32_t reentries;                     // calls made from inside a port call (#678)
	uint32_t draws;                         // TMR_DELAY draws
	uint32_t last_draw_ms;
};

// Bind the instance to its configuration and ports; every sink UNBOUND
// (5.5.3.5.1). False, with nothing set, for a configuration outside the
// static sizes or an interface index outside n_interfaces.
bool acmp_init(struct acmp *a, const struct acmp_config *cfg, const struct acmp_ports *ports,
	       const struct acmp_env *env);

// Inputs: a received ACMP frame, a received ADP frame, the interface's timer.
void acmp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len);
void acmp_adp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len);
void acmp_timer_expired(struct acmp *a, unsigned interface);

// The SRP side: EVT_TK_REGISTERED (with the attribute's kind: a Talker Failed
// is `failed`) and EVT_TK_UNREGISTERED for the sink's settled stream (Table
// 5.29).
void acmp_tk_registered(struct acmp *a, unsigned sink, bool failed);
void acmp_tk_unregistered(struct acmp *a, unsigned sink);

// The AECP side: START_STREAMING / STOP_STREAMING of a bound sink (Milan v1.2
// 5.3.8.7). False for an unbound or unknown sink.
bool acmp_set_started(struct acmp *a, unsigned sink, bool started);

// Attempt to send at most one owed frame, oldest first; return true while any
// frame remains owed.
bool acmp_poll(struct acmp *a);

// The saved-state store's binding walk and write path (see the top of this
// file). acmp_restore_binding is a boot step: it applies one saved record.
enum acmp_restore {
	ACMP_RESTORE_APPLIED = 0,               // nvm_state.h NVM_APPLIED
	ACMP_RESTORE_REFUSED = 1,               // NVM_REFUSED: the sink keeps its default (unbound)
};
enum acmp_restore acmp_restore_binding(struct acmp *a, unsigned sink, const uint8_t *payload, unsigned len);
void acmp_restore_rollback(struct acmp *a);
// The transport is open (the mailbox's contract checked, ctrl_loop_open): the
// admit port is told every binding the store restored. A boot step, after the
// binding walk and before the first input; any later entry would tell it too.
void acmp_open(struct acmp *a);
// The sink's saved record now; false for a sink the configuration does not have.
bool acmp_binding_latch(const struct acmp *a, unsigned sink, uint8_t payload[ACMP_BINDING_BYTES]);

// A sink as GET_STREAM_INFO reports it; false for an unknown sink.
bool acmp_view(const struct acmp *a, unsigned sink, struct acmp_sink_view *view);
// True while the sink's change waits behind its response (#653).
bool acmp_change_pending(const struct acmp *a, unsigned sink);

#ifdef CTRL_REENTRY_ASSERT
// Called once per refused re-entrant call in a build that asserts the rule;
// the platform (or the host test) defines it.
void ctrl_reentry_assert(const char *module);
#endif

#ifdef __cplusplus
}
#endif

#endif // ACMP_H
