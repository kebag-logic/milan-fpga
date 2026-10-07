// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp.c - Milan connection management (see acmp.h for the clauses it serves).
//
// Every public entry that changes state runs the same way: refuse a call made
// from inside a port call (#678), act, reading the clock at most once and only
// when a deadline is needed, then finish(): arm each interface's timer at the
// earliest deadline its sinks hold, tell the admit port every sink whose bound
// talker moved, announce to the store every sink whose saved record moved,
// and report every sink whose view moved and that holds no change behind an
// owed response.
//
// A sink's connection timer holds the one Table 5.29 timer its state owns
// (TMR_DELAY in PRB_W_DELAY, TMR_NO_RESP in PRB_W_RESP and PRB_W_RESP2,
// TMR_RETRY in PRB_W_RETRY, TMR_NO_TK in SETTLED_NO_RSV, none elsewhere), so
// an expiry is read off the timer's kind. TMR_NO_RESP is held, with no
// deadline, while the probe it times waits for transmit room, and starts when
// that probe leaves. Its discovery timer, TMR_NO_ADP, runs beside it and is
// armed only while the talker is discovered.
//
// The random delay costs the same every time: one xorshift step and one
// multiply, uniform to one part in 65536 over 0 to 1000 ms.

#include "acmp.h"

#include <string.h>

#include "wire.h"

#ifdef CTRL_REENTRY_ASSERT
#define REENTRY_TRAP() ctrl_reentry_assert("acmp")
#else
#define REENTRY_TRAP() ((void)0)
#endif

// ACMPDU field offsets in the frame (IEEE 1722.1-2021 Figure 8-1, after the
// 14-byte Ethernet header).
#define PDU ACMP_HEADER_BYTES
#define O_MSG (PDU + 1u)
#define O_STATUS (PDU + 2u)
#define O_STREAM_ID (PDU + 4u)
#define O_CONTROLLER (PDU + 12u)
#define O_TALKER (PDU + 20u)
#define O_LISTENER (PDU + 28u)
#define O_TALKER_UID (PDU + 36u)
#define O_LISTENER_UID (PDU + 38u)
#define O_DEST_MAC (PDU + 40u)
#define O_COUNT (PDU + 46u)
#define O_SEQ (PDU + 48u)
#define O_FLAGS (PDU + 50u)
#define O_VLAN (PDU + 52u)
#define AVTP_VERSION(frame) (((frame)[O_MSG] >> 4) & 0x07u)   // IEEE 1722-2016 Figure 5: bits 6:4 of byte 1

// ADPDU field offsets in the frame (IEEE 1722.1-2021 Figure 6-1, 6.2.2).
#define A_VALID_TIME (PDU + 2u)
#define A_ENTITY_ID (PDU + 4u)
#define A_AVAILABLE_INDEX (PDU + 36u)
#define A_GM (PDU + 40u)
#define A_DOMAIN (PDU + 48u)
#define A_INTERFACE_INDEX (PDU + 54u)

// The binding record's flags byte (KL_acmp_nvm_shadow's payload byte 0).
#define BIND_VALID 0x01u
#define BIND_STARTED 0x02u
#define BIND_STREAMING_WAIT 0x04u

// One ACMPDU, decoded.
struct pdu {
	uint8_t msg;
	uint8_t status;
	uint64_t stream_id;
	uint64_t controller;
	uint64_t talker;
	uint64_t listener;
	uint16_t talker_uid;
	uint16_t listener_uid;
	uint64_t dest_mac;
	uint16_t count;
	uint16_t seq;
	uint16_t flags;
	uint16_t vlan;
};

// ---- ports, each call inside the re-entry flag (#678) ----------------------------

static bool enter(struct acmp *a)
{
	if (a->in_port) {
		a->reentries++;
		REENTRY_TRAP();
		return false;
	}
	a->now_read = false;
	return true;
}

static bool p_send(struct acmp *a, unsigned interface, const uint8_t *frame)
{
	a->in_port = true;
	bool ok = a->ports->send(a->ports->ctx, interface, frame, ACMP_FRAME_BYTES);
	a->in_port = false;
	return ok;
}

// The clock, read once per entry and only by an entry that sets a deadline.
static uint32_t now(struct acmp *a)
{
	if (!a->now_read) {
		a->in_port = true;
		a->now = a->ports->now_ms(a->ports->ctx);
		a->in_port = false;
		a->now_read = true;
	}
	return a->now;
}

static void p_timer(struct acmp *a, unsigned interface, bool armed, uint32_t deadline_ms)
{
	a->in_port = true;
	a->ports->timer(a->ports->ctx, interface, armed, deadline_ms);
	a->in_port = false;
}

static void p_gptp(struct acmp *a, unsigned interface, uint64_t *gm, uint8_t *domain)
{
	a->in_port = true;
	a->ports->gptp(a->ports->ctx, interface, gm, domain);
	a->in_port = false;
}

static uint32_t p_seed(struct acmp *a)
{
	a->in_port = true;
	uint32_t seed = a->ports->seed(a->ports->ctx);
	a->in_port = false;
	return seed;
}

static bool p_locked(struct acmp *a, uint64_t *controller)
{
	a->in_port = true;
	bool locked = a->env->locked(a->env->ctx, controller);
	a->in_port = false;
	return locked;
}

static void p_source(struct acmp *a, unsigned index, struct acmp_source_state *out)
{
	a->in_port = true;
	a->env->source(a->env->ctx, index, out);
	a->in_port = false;
}

static void p_srp(struct acmp *a, unsigned sink, const struct acmp_stream *stream)
{
	a->in_port = true;
	a->env->srp(a->env->ctx, sink, stream);
	a->in_port = false;
}

static void p_persist(struct acmp *a, unsigned sink)
{
	a->in_port = true;
	a->env->persist(a->env->ctx, sink);
	a->in_port = false;
}

static void p_changed(struct acmp *a, unsigned sink)
{
	a->in_port = true;
	a->env->changed(a->env->ctx, sink);
	a->in_port = false;
}

static void p_admit(struct acmp *a, unsigned interface, unsigned sink, bool bound, uint64_t talker)
{
	a->in_port = true;
	a->ports->admit(a->ports->ctx, interface, sink, bound, talker);
	a->in_port = false;
}

// ---- the wire ----------------------------------------------------------------------

static void decode(const uint8_t *frame, struct pdu *p)
{
	p->msg = frame[O_MSG] & 0x0Fu;
	p->status = (uint8_t)(frame[O_STATUS] >> 3);
	p->stream_id = wire_be64(frame + O_STREAM_ID);
	p->controller = wire_be64(frame + O_CONTROLLER);
	p->talker = wire_be64(frame + O_TALKER);
	p->listener = wire_be64(frame + O_LISTENER);
	p->talker_uid = wire_be16(frame + O_TALKER_UID);
	p->listener_uid = wire_be16(frame + O_LISTENER_UID);
	p->dest_mac = ((uint64_t)wire_be16(frame + O_DEST_MAC) << 32) | wire_be32(frame + O_DEST_MAC + 2u);
	p->count = wire_be16(frame + O_COUNT);
	p->seq = wire_be16(frame + O_SEQ);
	p->flags = wire_be16(frame + O_FLAGS);
	p->vlan = wire_be16(frame + O_VLAN);
}

// The frame of `p` as this entity sends it on `interface`: to the ACMP
// multicast address (IEEE 1722.1-2021 8.2.1), h and version 0 (8.2.1.2,
// 8.2.1.3), the Milan control_data_length, connected_listeners_entries 0
// (Milan v1.2 5.5.2.2: a reserved field).
static void build(const struct acmp *a, unsigned interface, const struct pdu *p, uint8_t *frame)
{
	memset(frame, 0, ACMP_FRAME_BYTES);
	wire_put_be(frame, ACMP_MULTICAST_MAC, 6);
	wire_put_be(frame + 6, a->cfg.mac[interface], 6);
	wire_put_be(frame + 12, ACMP_ETHERTYPE, 2);
	frame[PDU] = ACMP_SUBTYPE;
	frame[O_MSG] = p->msg & 0x0Fu;
	wire_put_be(frame + O_STATUS, ((uint32_t)p->status << 11) | ACMP_CONTROL_DATA_LENGTH, 2);
	wire_put_be(frame + O_STREAM_ID, p->stream_id, 8);
	wire_put_be(frame + O_CONTROLLER, p->controller, 8);
	wire_put_be(frame + O_TALKER, p->talker, 8);
	wire_put_be(frame + O_LISTENER, p->listener, 8);
	wire_put_be(frame + O_TALKER_UID, p->talker_uid, 2);
	wire_put_be(frame + O_LISTENER_UID, p->listener_uid, 2);
	wire_put_be(frame + O_DEST_MAC, p->dest_mac, 6);
	wire_put_be(frame + O_COUNT, p->count, 2);
	wire_put_be(frame + O_SEQ, p->seq, 2);
	wire_put_be(frame + O_FLAGS, p->flags, 2);
	wire_put_be(frame + O_VLAN, p->vlan, 2);
}

// A response to `cmd` carrying every field its table gives as "Same value as
// in the command message", and 0 in every other field (the tables' 0 and,
// where they say "Undefined", a value the receiver ignores).
static struct pdu echo(const struct pdu *cmd, uint8_t status)
{
	struct pdu r;
	memset(&r, 0, sizeof r);
	r.msg = (uint8_t)(cmd->msg + 1u);
	r.status = status;
	r.controller = cmd->controller;
	r.talker = cmd->talker;
	r.listener = cmd->listener;
	r.talker_uid = cmd->talker_uid;
	r.listener_uid = cmd->listener_uid;
	r.seq = cmd->seq;
	return r;
}

// ---- owed frames, in order ---------------------------------------------------------

enum sent { SENT, OWED, LOST };

// Send a frame now, or queue it behind those already owed. `release` names the
// sinks whose change may be reported only once this frame has left; a probe
// names its sink in `probe_of` (1 + the sink, 0 for a response). LOST when the
// queue is full.
static enum sent transmit(struct acmp *a, unsigned interface, const uint8_t *frame, uint32_t release,
			  unsigned probe_of)
{
	if (a->owed_count == 0u && p_send(a, interface, frame)) {
		return SENT;
	}
	if (a->owed_count >= ACMP_OWED_MAX) {
		return LOST;
	}
	struct acmp_owed *o = &a->owed[(a->owed_head + a->owed_count) % ACMP_OWED_MAX];
	o->interface = (uint8_t)interface;
	o->probe_of = (uint8_t)probe_of;
	o->release = release;
	memcpy(o->frame, frame, ACMP_FRAME_BYTES);
	a->owed_count++;
	a->deferred_sends++;
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
		a->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + ((release >> k) & 1u));
	}
	return OWED;
}

// A response; the command that asked for it saw room for it in the queue.
static void respond(struct acmp *a, unsigned interface, const struct pdu *r, uint32_t release)
{
	uint8_t frame[ACMP_FRAME_BYTES];
	build(a, interface, r, frame);
	(void)transmit(a, interface, frame, release, 0u);
}

// Room for one more frame; a command that finds none is dropped before it
// changes anything.
static bool room(struct acmp *a)
{
	if (a->owed_count < ACMP_OWED_MAX) {
		return true;
	}
	a->busy_drops++;
	return false;
}

// ---- timers ----------------------------------------------------------------------

static bool due(uint32_t deadline, uint32_t at)
{
	return (int32_t)(deadline - at) <= 0;
}

static void sm_timer(struct acmp *a, struct acmp_sink *s, enum acmp_timer kind, uint32_t delay_ms)
{
	s->timer = kind;
	s->timer_deadline = now(a) + delay_ms;
	s->timer_held = false;
}

static void sm_stop(struct acmp_sink *s)
{
	s->timer = ACMP_TIMER_NONE;
	s->timer_held = false;
}

// The connection timer runs: armed, and not held for an owed probe.
static bool sm_running(const struct acmp_sink *s)
{
	return s->timer != ACMP_TIMER_NONE && !s->timer_held;
}

// The seed is taken at the first draw, inside the event loop: nothing reads the
// mailbox before the contract is checked (ctrl_loop_open).
static uint32_t draw_ms(struct acmp *a)
{
	if (!a->seeded) {
		a->rng ^= p_seed(a);
		a->seeded = true;
		if (a->rng == 0u) {
			a->rng = 1u;                            // xorshift never leaves 0
		}
	}
	uint32_t x = a->rng;
	x ^= x << 13;
	x ^= x >> 17;
	x ^= x << 5;
	a->rng = x;
	uint32_t ms = ((x >> 16) * (ACMP_TMR_DELAY_MAX_MS + 1u)) >> 16;
	a->draws++;
	a->last_draw_ms = ms;
	return ms;
}

// The earlier of a deadline and the earliest found so far.
static void earliest(bool *any, uint32_t *at, bool armed, uint32_t deadline)
{
	if (armed && (!*any || (int32_t)(deadline - *at) < 0)) {
		*at = deadline;
		*any = true;
	}
}

// Arm each interface's timer at the earliest deadline its sinks hold, or stop
// it; the port is called only when that changes.
static void rearm(struct acmp *a)
{
	for (unsigned i = 0; i < a->cfg.n_interfaces; ++i) {
		bool any = false;
		uint32_t at = 0;
		for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
			const struct acmp_sink *s = &a->sinks[k];
			if (s->interface == i) {
				earliest(&any, &at, sm_running(s), s->timer_deadline);
				earliest(&any, &at, s->adp_armed, s->adp_deadline);
			}
		}
		if (any && (!a->timer_armed[i] || a->timer_at[i] != at)) {
			a->timer_armed[i] = true;
			a->timer_at[i] = at;
			p_timer(a, i, true, at);
		} else if (!any && a->timer_armed[i]) {
			a->timer_armed[i] = false;
			p_timer(a, i, false, 0u);
		}
	}
}

// ---- the view, the saved record and the reports --------------------------------------

static void view_of(const struct acmp_sink *s, struct acmp_sink_view *v)
{
	memset(v, 0, sizeof *v);
	v->state = s->state;
	v->bound = s->bound;
	v->binding = s->binding;
	v->started = s->started;
	v->probing_status = s->probing;
	v->acmp_status = s->acmp_status;
	v->settled = s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK;
	if (v->settled) {
		v->stream = s->stream;
	}
	v->talker_registered = s->state == ACMP_SETTLED_RSV_OK;
	v->registering_failed = v->talker_registered && s->tk_failed;
	v->talker_discovered = s->discovered;
}

// Whether a GET_STREAM_INFO notification is due: Milan v1.2 Table 5.22's
// STREAM_INPUT items (the bound state, the started/stopped state, the probing
// and ACMP status, the stream ID, destination MAC and VLAN ID, and the MSRP
// Talker attribute registration state) are the same in both views. Every item
// is compared, in one expression with no early exit.
static bool view_equal(const struct acmp_sink_view *x, const struct acmp_sink_view *y)
{
	uint64_t diff = (x->stream.stream_id ^ y->stream.stream_id) | (x->stream.dest_mac ^ y->stream.dest_mac) |
			(uint64_t)(x->stream.vlan_id ^ y->stream.vlan_id) |
			(uint64_t)((unsigned)x->probing_status ^ (unsigned)y->probing_status) |
			(uint64_t)(x->acmp_status ^ y->acmp_status) | (uint64_t)(x->bound != y->bound) |
			(uint64_t)(x->started != y->started) | (uint64_t)(x->talker_registered != y->talker_registered) |
			(uint64_t)(x->registering_failed != y->registering_failed);
	return diff == 0u;
}

// The saved binding record (acmp.h): an unbound sink's is all zeros, which is
// how the store saves an unbind (5.5.3.5.8 step 3: the parameters cleared).
static void record_of(const struct acmp_sink *s, uint8_t payload[ACMP_BINDING_BYTES])
{
	memset(payload, 0, ACMP_BINDING_BYTES);
	if (s->bound) {
		payload[0] = (uint8_t)(BIND_VALID | (s->started ? BIND_STARTED : 0u) |
				       (s->binding.streaming_wait ? BIND_STREAMING_WAIT : 0u));
		wire_put_be(payload + 2, s->binding.talker_unique_id, 2);
		wire_put_be(payload + 4, s->binding.talker_entity_id, 8);
		wire_put_be(payload + 12, s->binding.controller_entity_id, 8);
	}
}

// Two binding records, byte for byte (no memcmp: the freestanding build links
// memset and memcpy only).
static bool same_record(const uint8_t *x, const uint8_t *y)
{
	uint8_t diff = 0;
	for (unsigned i = 0; i < ACMP_BINDING_BYTES; ++i) {
		diff |= (uint8_t)(x[i] ^ y[i]);
	}
	return diff == 0u;
}

// The ingress passes the ENTITY_AVAILABLE and ENTITY_DEPARTING of each bound
// sink's talker on its interface (5.6.4.1); the port is called only for a sink
// whose bound talker moved.
static void admit(struct acmp *a)
{
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
		struct acmp_sink *s = &a->sinks[k];
		uint64_t talker = s->binding.talker_entity_id;
		if (s->bound != s->admitted || (s->bound && talker != s->admitted_talker)) {
			s->admitted = s->bound;
			s->admitted_talker = talker;
			p_admit(a, s->interface, k, s->bound, talker);
		}
	}
}

// After every entry: the timers, the ingress, then the store, then the notifier.
static void finish(struct acmp *a)
{
	rearm(a);
	admit(a);
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
		struct acmp_sink *s = &a->sinks[k];
		uint8_t record[ACMP_BINDING_BYTES];
		record_of(s, record);
		if (!same_record(record, s->saved)) {
			memcpy(s->saved, record, ACMP_BINDING_BYTES);
			p_persist(a, k);
		}
		struct acmp_sink_view v;
		view_of(s, &v);
		if (s->change_owed == 0u && !view_equal(&v, &s->reported)) {
			s->reported = v;
			p_changed(a, k);
		}
	}
}

// A sink as the configuration starts it, and as a restore or a roll-back
// leaves it: UNBOUND, probing disabled, nothing running (5.5.3.5.1). What the
// admit port holds is not the sink's state, and stays.
static void sink_reset(struct acmp *a, unsigned k)
{
	struct acmp_sink *s = &a->sinks[k];
	bool admitted = s->admitted;
	uint64_t admitted_talker = s->admitted_talker;
	memset(s, 0, sizeof *s);
	s->admitted = admitted;
	s->admitted_talker = admitted_talker;
	s->interface = a->cfg.sink_interface[k];
	s->state = ACMP_UNBOUND;
	s->probing = ACMP_PROBING_DISABLED;
}

// The store and the notifier are told nothing about a state they did not
// see change: what a boot set is what they start from.
static void sink_settle(struct acmp_sink *s)
{
	record_of(s, s->saved);
	view_of(s, &s->reported);
}

// ---- discovery (5.6.4) and the events it raises ----------------------------------------

static void disc_start(struct acmp_sink *s)
{
	s->disc_running = true;
	s->discovered = false;                  // "at this point, talker has not been discovered"
	s->adp_armed = false;
}

static void disc_stop(struct acmp_sink *s)
{
	s->disc_running = false;
	s->discovered = false;
	s->adp_armed = false;
}

// Start the random TMR_DELAY and go to PRB_W_DELAY.
static void delay(struct acmp *a, struct acmp_sink *s)
{
	sm_timer(a, s, ACMP_TIMER_DELAY, draw_ms(a));
	s->state = ACMP_PRB_W_DELAY;
}

// "set the Probing status to PROBING_PASSIVE and ACMP status to 0 and go to
// the PRB_W_AVAIL state" (5.5.3.5.15 and the others that end the same way).
static void passive(struct acmp_sink *s)
{
	s->probing = ACMP_PROBING_PASSIVE;
	s->acmp_status = ACMP_STATUS_SUCCESS;
	s->state = ACMP_PRB_W_AVAIL;
}

// 5.5.3.5.36 and 5.5.3.5.48 steps 2 and 3, once SRP has stopped.
static void reprobe(struct acmp *a, struct acmp_sink *s)
{
	if (!s->discovered) {
		passive(s);
		return;
	}
	s->probing = ACMP_PROBING_ACTIVE;
	s->acmp_status = ACMP_STATUS_SUCCESS;
	delay(a, s);
}

// EVT_TK_DISCOVERED: 5.5.3.5.9 in PRB_W_AVAIL; noted in every other bound
// state (5.5.3.5.14, .21, .28, .34, .40, .46). Discovery runs only while the
// sink is bound, so UNBOUND never sees it.
static void tk_discovered(struct acmp *a, struct acmp_sink *s)
{
	s->discovered = true;
	if (s->state == ACMP_PRB_W_AVAIL) {
		s->probing = ACMP_PROBING_ACTIVE;
		s->acmp_status = ACMP_STATUS_SUCCESS;
		delay(a, s);
	}
}

// EVT_TK_DEPARTED: 5.5.3.5.15, .22, .29 and .35 stop the probing state's timer
// and go to PRB_W_AVAIL; settled, it is noted only (5.5.3.5.41, .47). The
// talker is never discovered in PRB_W_AVAIL, so that cell (Table 5.30 "x")
// never runs.
static void tk_departed(struct acmp_sink *s)
{
	s->discovered = false;
	if (s->state == ACMP_PRB_W_DELAY || s->state == ACMP_PRB_W_RESP || s->state == ACMP_PRB_W_RESP2 ||
	    s->state == ACMP_PRB_W_RETRY) {
		sm_stop(s);
		passive(s);
	}
}

static void adp_arm(struct acmp *a, struct acmp_sink *s, uint32_t valid_ms)
{
	s->adp_armed = true;
	s->adp_deadline = now(a) + valid_ms;
}

// One received ADPDU's fields, and this port's gPTP pair, sampled only when a
// guard reads it: the periodic refresh of a discovered talker reads none.
struct adpdu {
	unsigned interface;
	uint16_t ifx;
	uint32_t index;
	uint32_t valid_ms;
	uint64_t gm;
	uint8_t domain;
	bool sampled;
	uint64_t local_gm;
	uint8_t local_domain;
};

// The ADPDU's grandmaster and domain are this port's (5.6.4.5.1 step 1,
// 5.6.4.5.2 step 2b).
static bool gm_matches(struct acmp *a, struct adpdu *d)
{
	if (!d->sampled) {
		p_gptp(a, d->interface, &d->local_gm, &d->local_domain);
		d->sampled = true;
	}
	return d->gm == d->local_gm && d->domain == d->local_domain;
}

// RCV_ADP_AVAILABLE: 5.6.4.5.1 in TK_NOT_DISCOVERED, 5.6.4.5.2 in TK_DISCOVERED.
static void disc_available(struct acmp *a, struct acmp_sink *s, struct adpdu *d)
{
	uint16_t ifx = d->ifx;
	uint32_t index = d->index;
	uint32_t valid_ms = d->valid_ms;
	if (!s->discovered) {
		if (!gm_matches(a, d)) {
			return;                                 // 5.6.4.5.1 step 1
		}
		s->disc_interface_index = ifx;                  // step 2
		s->disc_available_index = index;
		adp_arm(a, s, valid_ms);                        // step 3
		tk_discovered(a, s);                            // step 4
		return;
	}
	if (ifx != s->disc_interface_index) {
		return;                                         // 5.6.4.5.2 step 1
	}
	if (index <= s->disc_available_index) {                 // step 2: a new availability cycle
		tk_departed(s);                                 // 2a
		if (!gm_matches(a, d)) {
			s->adp_armed = false;                   // 2b: TK_NOT_DISCOVERED, no step 3
			return;
		}
		tk_discovered(a, s);                            // 2c
	}
	s->disc_available_index = index;                        // step 3
	adp_arm(a, s, valid_ms);
}

// RCV_ADP_DEPARTING: ignored in TK_NOT_DISCOVERED (Table 5.54 "-"), 5.6.4.5.3
// in TK_DISCOVERED.
static void disc_departing(struct acmp_sink *s, uint16_t ifx)
{
	if (!s->discovered || ifx != s->disc_interface_index) {
		return;
	}
	s->adp_armed = false;
	tk_departed(s);
}

// ---- the listener's actions ----------------------------------------------------------

// "Clear the SRP parameters and stop SRP", from a settled state: the only
// states that listen (5.5.3.5.18 step 4 started it).
static void srp_stop(struct acmp *a, unsigned k)
{
	struct acmp_sink *s = &a->sinks[k];
	memset(&s->stream, 0, sizeof s->stream);
	s->tk_failed = false;
	p_srp(a, k, NULL);
}

// The sink's saved PROBE_TX_COMMAND (Table 5.33) on its interface; TMR_NO_RESP
// 200 ms from the send the port accepts: a probe owed behind others holds it
// until acmp_poll sends the probe (probe_left). A probe the queue has no room
// for is lost and TMR_NO_RESP, run from the attempt, recovers it.
static void send_probe(struct acmp *a, unsigned k)
{
	struct acmp_sink *s = &a->sinks[k];
	sm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);
	struct pdu p;
	memset(&p, 0, sizeof p);
	p.msg = ACMP_MSG_PROBE_TX_COMMAND;
	p.controller = s->probe_controller;
	p.talker = s->probe_talker;
	p.listener = a->cfg.entity_id;
	p.talker_uid = s->probe_talker_uid;
	p.listener_uid = (uint16_t)k;
	p.seq = s->probe_seq;
	p.flags = ACMP_FLAG_FAST_CONNECT;
	uint8_t frame[ACMP_FRAME_BYTES];
	build(a, s->interface, &p, frame);
	enum sent sent = transmit(a, s->interface, frame, 0u, k + 1u);
	if (sent == OWED) {
		s->timer_held = true;
	} else if (sent == LOST) {
		a->probes_lost++;
	}
}

// An owed frame has left. When it is the probe a sink's held TMR_NO_RESP waits
// for (its sequence_id the sink's current probe's: a probe re-bound since is
// not), the timer starts now (5.5.3.5.3 step 7, 5.5.3.5.16 step 2).
static void probe_left(struct acmp *a, const struct acmp_owed *o)
{
	if (o->probe_of == 0u) {
		return;
	}
	struct acmp_sink *s = &a->sinks[o->probe_of - 1u];
	if (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {
		sm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);
	}
}

// A new PROBE_TX_COMMAND from the binding, with the next sequence_id
// (IEEE 1722.1-2021 8.2.1.15), and its copy kept (5.5.3.5.3 step 6).
static void probe(struct acmp *a, unsigned k)
{
	struct acmp_sink *s = &a->sinks[k];
	s->probe_controller = s->binding.controller_entity_id;
	s->probe_talker = s->binding.talker_entity_id;
	s->probe_talker_uid = s->binding.talker_unique_id;
	s->probe_seq = a->sequence_id;
	a->sequence_id = (uint16_t)(a->sequence_id + 1u);
	s->probe_retried = false;
	send_probe(a, k);
}

// The connection timer of sink k expired.
static void sm_expired(struct acmp *a, unsigned k)
{
	struct acmp_sink *s = &a->sinks[k];
	enum acmp_timer kind = s->timer;
	sm_stop(s);
	if (kind == ACMP_TIMER_DELAY) {                         // 5.5.3.5.10
		probe(a, k);
		s->state = ACMP_PRB_W_RESP;
	} else if (kind == ACMP_TIMER_NO_RESP && s->state == ACMP_PRB_W_RESP) {   // 5.5.3.5.16
		s->probe_retried = true;
		send_probe(a, k);                               // the same sequence_id
		s->state = ACMP_PRB_W_RESP2;
	} else if (kind == ACMP_TIMER_NO_RESP) {                // 5.5.3.5.23, in PRB_W_RESP2
		sm_timer(a, s, ACMP_TIMER_RETRY, ACMP_TMR_RETRY_MS);
		s->acmp_status = ACMP_STATUS_LISTENER_TALKER_TIMEOUT;
		s->state = ACMP_PRB_W_RETRY;
	} else if (kind == ACMP_TIMER_RETRY && !s->discovered) {   // 5.5.3.5.30 step 1
		passive(s);
	} else if (kind == ACMP_TIMER_RETRY) {                  // step 2: the ACMP status stays
		delay(a, s);
	} else {                                                // 5.5.3.5.36, TMR_NO_TK
		srp_stop(a, k);
		reprobe(a, s);
	}
}

// ---- the listener's commands (5.5.3.1) ---------------------------------------------

static bool lock_refuses(struct acmp *a, const struct pdu *cmd)
{
	uint64_t holder = 0;
	if (p_locked(a, &holder) && holder != cmd->controller) {
		a->refused_locked++;
		return true;
	}
	return false;
}

static void bind_response(struct acmp *a, unsigned interface, unsigned k, const struct pdu *cmd)
{
	struct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);             // Table 5.32
	r.count = 1u;
	r.flags = cmd->flags & ACMP_FLAG_STREAMING_WAIT;
	respond(a, interface, &r, 1u << k);
}

// RCV_BIND_RX_CMD in every state: 5.5.3.5.3, .6, .11, .17, .24, .31, .37, .43.
static void bind(struct acmp *a, unsigned interface, unsigned k, const struct pdu *cmd)
{
	struct acmp_sink *s = &a->sinks[k];
	bool sw = (cmd->flags & ACMP_FLAG_STREAMING_WAIT) != 0u;
	if (s->bound && cmd->talker == s->binding.talker_entity_id && cmd->talker_uid == s->binding.talker_unique_id) {
		// step 2: the same source; the controller and STREAMING_WAIT updated
		s->binding.controller_entity_id = cmd->controller;
		s->binding.streaming_wait = sw;
		s->started = !sw;
		bind_response(a, interface, k, cmd);
		return;
	}
	if (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {
		srp_stop(a, k);                                 // 5.5.3.5.37 and .43 step 3
	}
	disc_stop(s);
	sm_stop(s);
	s->bound = true;
	s->binding.talker_entity_id = cmd->talker;
	s->binding.talker_unique_id = cmd->talker_uid;
	s->binding.controller_entity_id = cmd->controller;
	s->binding.streaming_wait = sw;
	// IEEE 1722.1-2021 7.4.35: a stream bound with STREAMING_WAIT waits for
	// START_STREAMING (Milan v1.2 5.3.8.7)
	s->started = !sw;
	bind_response(a, interface, k, cmd);
	disc_start(s);
	probe(a, k);
	s->probing = ACMP_PROBING_ACTIVE;
	s->acmp_status = ACMP_STATUS_SUCCESS;
	s->state = ACMP_PRB_W_RESP;
}

// RCV_UNBIND_RX_CMD in every state: 5.5.3.5.5, .8, .13, .20, .27, .33, .39,
// .45. From UNBOUND every step but the response finds nothing to change.
static void unbind(struct acmp *a, unsigned interface, unsigned k, const struct pdu *cmd)
{
	struct acmp_sink *s = &a->sinks[k];
	if (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {
		srp_stop(a, k);
	}
	disc_stop(s);
	s->bound = false;
	memset(&s->binding, 0, sizeof s->binding);
	s->started = false;
	s->probing = ACMP_PROBING_DISABLED;
	s->acmp_status = ACMP_STATUS_SUCCESS;
	sm_stop(s);
	struct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);             // Table 5.36
	r.talker = 0u;
	r.talker_uid = 0u;
	respond(a, interface, &r, 1u << k);
	s->state = ACMP_UNBOUND;
}

// RCV_GET_RX_STATE in every state: Tables 5.34, 5.37, 5.38 and 5.39.
static void get_rx_state(struct acmp *a, unsigned interface, unsigned k, const struct pdu *cmd)
{
	const struct acmp_sink *s = &a->sinks[k];
	struct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);
	r.talker = s->binding.talker_entity_id;
	r.talker_uid = s->binding.talker_unique_id;
	if (s->bound) {
		r.count = 1u;
		r.flags = (uint16_t)(ACMP_FLAG_FAST_CONNECT | (s->binding.streaming_wait ? ACMP_FLAG_STREAMING_WAIT : 0u));
	}
	if (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {
		r.stream_id = s->stream.stream_id;
		r.dest_mac = s->stream.dest_mac;
		r.vlan = s->stream.vlan_id;
	}
	if (s->state == ACMP_SETTLED_RSV_OK && s->tk_failed) {
		r.flags |= ACMP_FLAG_REGISTERING_FAILED;
	}
	respond(a, interface, &r, 0u);
}

static void listener_command(struct acmp *a, unsigned interface, const struct pdu *cmd)
{
	if (!room(a)) {
		return;
	}
	unsigned k = cmd->listener_uid;
	if (k >= a->cfg.n_sinks) {
		a->unknown_sink++;
		struct pdu r = echo(cmd, ACMP_STATUS_LISTENER_UNKNOWN_ID);         // Table 5.27
		respond(a, interface, &r, 0u);
		return;
	}
	if (cmd->msg == ACMP_MSG_GET_RX_STATE_COMMAND) {
		get_rx_state(a, interface, k, cmd);
	} else if (lock_refuses(a, cmd)) {
		struct pdu r = echo(cmd, ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED);   // Tables 5.31, 5.35
		respond(a, interface, &r, 0u);
	} else if (cmd->msg == ACMP_MSG_BIND_RX_COMMAND) {
		bind(a, interface, k, cmd);
	} else {
		unbind(a, interface, k, cmd);
	}
}

// RCV_PROBE_TX_RESP: 5.5.3.5.18 in PRB_W_RESP and 5.5.3.5.25 in PRB_W_RESP2;
// ignored in every other state (Table 5.30 "-").
static void probe_response(struct acmp *a, const struct pdu *rsp)
{
	unsigned k = rsp->listener_uid;
	if (k >= a->cfg.n_sinks) {
		a->unknown_sink++;                              // 5.5.3.1: ignored
		return;
	}
	struct acmp_sink *s = &a->sinks[k];
	if (s->state != ACMP_PRB_W_RESP && s->state != ACMP_PRB_W_RESP2) {
		a->rx_ignored++;
		return;
	}
	if (rsp->controller != s->probe_controller || rsp->talker != s->probe_talker ||
	    rsp->talker_uid != s->probe_talker_uid || rsp->seq != s->probe_seq) {
		a->probe_mismatch++;                            // step 1
		return;
	}
	sm_stop(s);                                             // step 2
	if (rsp->status != ACMP_STATUS_SUCCESS) {               // step 3
		sm_timer(a, s, ACMP_TIMER_RETRY, ACMP_TMR_RETRY_MS);
		s->acmp_status = rsp->status;
		s->state = ACMP_PRB_W_RETRY;
		return;
	}
	s->stream.stream_id = rsp->stream_id;                   // step 4, kept exactly (Milan v1.2 5.3.8.9)
	s->stream.dest_mac = rsp->dest_mac;
	s->stream.vlan_id = rsp->vlan;
	p_srp(a, k, &s->stream);
	sm_timer(a, s, ACMP_TIMER_NO_TK, ACMP_TMR_NO_TK_MS);
	s->probing = ACMP_PROBING_COMPLETED;
	s->acmp_status = ACMP_STATUS_SUCCESS;
	s->state = ACMP_SETTLED_NO_RSV;
}

// ---- the talker (5.5.4) --------------------------------------------------------------

static void talker_command(struct acmp *a, unsigned interface, const struct pdu *cmd)
{
	if (!room(a)) {
		return;
	}
	unsigned src = cmd->talker_uid;
	if (cmd->msg == ACMP_MSG_GET_TX_CONNECTION_COMMAND) {
		struct pdu r = echo(cmd, ACMP_STATUS_NOT_SUPPORTED);              // 5.5.4.4, Table 5.48
		respond(a, interface, &r, 0u);
		return;
	}
	if (src >= a->cfg.n_sources) {
		struct pdu r = echo(cmd, ACMP_STATUS_TALKER_UNKNOWN_ID);          // Tables 5.40, 5.44, 5.46
		respond(a, interface, &r, 0u);
		return;
	}
	if (cmd->msg == ACMP_MSG_DISCONNECT_TX_COMMAND) {
		struct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);                    // 5.5.4.2, Table 5.45
		respond(a, interface, &r, 0u);
		return;
	}
	if (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND && interface != a->cfg.source_interface[src]) {
		struct pdu r = echo(cmd, ACMP_STATUS_INCOMPATIBLE_REQUEST);       // 5.5.4.1 step 2, Table 5.41
		respond(a, interface, &r, 0u);
		return;
	}
	struct acmp_source_state st;
	memset(&st, 0, sizeof st);
	p_source(a, src, &st);
	if (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND) {
		struct pdu r = echo(cmd, st.dest_mac_valid ? ACMP_STATUS_SUCCESS : ACMP_STATUS_TALKER_DEST_MAC_FAIL);
		if (st.dest_mac_valid) {                                         // Table 5.43, else 5.42
			r.flags = cmd->flags & (ACMP_FLAG_FAST_CONNECT | ACMP_FLAG_STREAMING_WAIT);
			r.stream_id = st.stream.stream_id;
			r.dest_mac = st.stream.dest_mac;
			r.vlan = st.stream.vlan_id;
		}
		respond(a, interface, &r, 0u);
		return;
	}
	struct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);                            // 5.5.4.3, Table 5.47
	r.listener = 0u;
	r.listener_uid = 0u;
	r.flags = st.asking_failed ? ACMP_FLAG_REGISTERING_FAILED : 0u;
	r.stream_id = st.stream.stream_id;
	r.dest_mac = st.dest_mac_valid ? st.stream.dest_mac : 0u;
	r.vlan = st.stream.vlan_id;
	respond(a, interface, &r, 0u);
}

// ---- public entries ----------------------------------------------------------------

bool acmp_init(struct acmp *a, const struct acmp_config *cfg, const struct acmp_ports *ports,
	       const struct acmp_env *env)
{
	if (cfg->n_interfaces == 0u || cfg->n_interfaces > ACMP_MAX_INTERFACES || cfg->n_sinks > ACMP_MAX_SINKS ||
	    cfg->n_sources > ACMP_MAX_SOURCES) {
		return false;
	}
	for (unsigned k = 0; k < cfg->n_sinks; ++k) {
		if (cfg->sink_interface[k] >= cfg->n_interfaces) {
			return false;
		}
	}
	for (unsigned k = 0; k < cfg->n_sources; ++k) {
		if (cfg->source_interface[k] >= cfg->n_interfaces) {
			return false;
		}
	}
	memset(a, 0, sizeof *a);
	a->cfg = *cfg;
	a->ports = ports;
	a->env = env;
	for (unsigned k = 0; k < cfg->n_sinks; ++k) {
		sink_reset(a, k);
		sink_settle(&a->sinks[k]);
	}
	a->rng = (uint32_t)cfg->entity_id ^ (uint32_t)(cfg->entity_id >> 32) ^ 0x7F4A7C15u;
	return true;
}

void acmp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len)
{
	if (!enter(a)) {
		return;
	}
	if (interface >= a->cfg.n_interfaces || len < ACMP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||
	    frame[PDU] != ACMP_SUBTYPE || AVTP_VERSION(frame) != ACMP_AVTP_VERSION) {
		a->rx_malformed++;
		return;
	}
	struct pdu cmd;
	decode(frame, &cmd);
	bool talker = cmd.talker == a->cfg.entity_id;
	bool listener = cmd.listener == a->cfg.entity_id;
	switch (cmd.msg) {
	case ACMP_MSG_PROBE_TX_COMMAND:
	case ACMP_MSG_DISCONNECT_TX_COMMAND:
	case ACMP_MSG_GET_TX_STATE_COMMAND:
	case ACMP_MSG_GET_TX_CONNECTION_COMMAND:
		if (talker) {
			talker_command(a, interface, &cmd);
		} else {
			a->rx_ignored++;
		}
		break;
	case ACMP_MSG_BIND_RX_COMMAND:
	case ACMP_MSG_UNBIND_RX_COMMAND:
	case ACMP_MSG_GET_RX_STATE_COMMAND:
		if (listener) {
			listener_command(a, interface, &cmd);
		} else {
			a->rx_ignored++;
		}
		break;
	case ACMP_MSG_PROBE_TX_RESPONSE:
		if (listener) {
			probe_response(a, &cmd);
		} else {
			a->rx_ignored++;
		}
		break;
	default:
		a->rx_ignored++;                                // 5.5.3.1: every other message
		break;
	}
	finish(a);
}

void acmp_adp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len)
{
	if (!enter(a)) {
		return;
	}
	if (interface >= a->cfg.n_interfaces || len < ACMP_ADP_FRAME_BYTES || wire_be16(frame + 12) != ACMP_ETHERTYPE ||
	    frame[PDU] != ACMP_ADP_SUBTYPE || AVTP_VERSION(frame) != ACMP_AVTP_VERSION ||
	    (frame[O_MSG] & 0x0Fu) > ACMP_ADP_MSG_ENTITY_DEPARTING) {
		a->adp_ignored++;                               // not an ENTITY_AVAILABLE or ENTITY_DEPARTING
		return;
	}
	uint8_t msg = frame[O_MSG] & 0x0Fu;
	uint64_t entity = wire_be64(frame + A_ENTITY_ID);
	struct adpdu d;
	memset(&d, 0, sizeof d);
	d.interface = interface;
	d.valid_ms = (uint32_t)(frame[A_VALID_TIME] >> 3) * ACMP_VALID_TIME_UNIT_MS;   // 6.2.2.5
	d.index = wire_be32(frame + A_AVAILABLE_INDEX);
	d.gm = wire_be64(frame + A_GM);
	d.domain = frame[A_DOMAIN];
	d.ifx = wire_be16(frame + A_INTERFACE_INDEX);
	unsigned taken = 0;
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {        // 5.6.4.1: every bound sink of this talker
		struct acmp_sink *s = &a->sinks[k];
		if (!s->disc_running || s->interface != interface || s->binding.talker_entity_id != entity) {
			continue;
		}
		taken++;
		if (msg == ACMP_ADP_MSG_ENTITY_DEPARTING) {
			disc_departing(s, d.ifx);
		} else {
			disc_available(a, s, &d);
		}
	}
	if (taken == 0u) {
		a->adp_ignored++;
	}
	finish(a);
}

// Every timer of the interface's sinks that is due, in sink order; a sink's
// TMR_NO_ADP before its connection timer. A connection timer is taken again
// while it is due: a TMR_RETRY or TMR_NO_TK that draws a 0 ms TMR_DELAY sends
// its probe in the same call, and TMR_NO_RESP then lies 200 ms ahead, so a
// sink is taken at most twice.
void acmp_timer_expired(struct acmp *a, unsigned interface)
{
	if (!enter(a)) {
		return;
	}
	if (interface >= a->cfg.n_interfaces) {
		a->impossible++;
		return;
	}
	a->timer_armed[interface] = false;                      // the port's timer has fired
	uint32_t t = now(a);
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
		struct acmp_sink *s = &a->sinks[k];
		if (s->interface != interface) {
			continue;
		}
		if (s->adp_armed && due(s->adp_deadline, t)) {   // 5.6.4.5.4
			s->adp_armed = false;
			tk_departed(s);
		}
		while (sm_running(s) && due(s->timer_deadline, t)) {
			sm_expired(a, k);
		}
	}
	finish(a);
}

void acmp_tk_registered(struct acmp *a, unsigned sink, bool failed)
{
	if (!enter(a)) {
		return;
	}
	if (sink >= a->cfg.n_sinks || a->sinks[sink].state != ACMP_SETTLED_NO_RSV) {
		a->impossible++;                                // Table 5.30 "x"
		return;
	}
	struct acmp_sink *s = &a->sinks[sink];                  // 5.5.3.5.42
	sm_stop(s);
	s->tk_failed = failed;
	s->state = ACMP_SETTLED_RSV_OK;
	finish(a);
}

void acmp_tk_unregistered(struct acmp *a, unsigned sink)
{
	if (!enter(a)) {
		return;
	}
	if (sink >= a->cfg.n_sinks || a->sinks[sink].state != ACMP_SETTLED_RSV_OK) {
		a->impossible++;                                // Table 5.30 "x"
		return;
	}
	srp_stop(a, sink);                                      // 5.5.3.5.48
	reprobe(a, &a->sinks[sink]);
	finish(a);
}

bool acmp_set_started(struct acmp *a, unsigned sink, bool started)
{
	if (!enter(a)) {
		return false;
	}
	if (sink >= a->cfg.n_sinks || !a->sinks[sink].bound) {
		return false;
	}
	a->sinks[sink].started = started;
	finish(a);
	return true;
}

bool acmp_poll(struct acmp *a)
{
	if (!enter(a)) {
		return a->owed_count != 0u;
	}
	if (a->owed_count != 0u) {
		const struct acmp_owed *o = &a->owed[a->owed_head];
		if (p_send(a, o->interface, o->frame)) {
			for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
				a->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed - ((o->release >> k) & 1u));
			}
			probe_left(a, o);
			a->owed_head = (a->owed_head + 1u) % ACMP_OWED_MAX;
			a->owed_count--;
			finish(a);
		}
	}
	return a->owed_count != 0u;
}

enum acmp_restore acmp_restore_binding(struct acmp *a, unsigned sink, const uint8_t *payload, unsigned len)
{
	if (!enter(a)) {
		return ACMP_RESTORE_REFUSED;
	}
	if (sink >= a->cfg.n_sinks || len != ACMP_BINDING_BYTES) {
		return ACMP_RESTORE_REFUSED;
	}
	sink_reset(a, sink);
	struct acmp_sink *s = &a->sinks[sink];
	if ((payload[0] & BIND_VALID) != 0u) {                  // 5.5.3.5.2
		s->bound = true;
		s->started = (payload[0] & BIND_STARTED) != 0u;
		s->binding.streaming_wait = (payload[0] & BIND_STREAMING_WAIT) != 0u;
		s->binding.talker_unique_id = wire_be16(payload + 2);
		s->binding.talker_entity_id = wire_be64(payload + 4);
		s->binding.controller_entity_id = wire_be64(payload + 12);
		disc_start(s);
		s->probing = ACMP_PROBING_PASSIVE;
		s->state = ACMP_PRB_W_AVAIL;
	}
	sink_settle(s);
	return ACMP_RESTORE_APPLIED;
}

void acmp_restore_rollback(struct acmp *a)
{
	if (!enter(a)) {
		return;
	}
	for (unsigned k = 0; k < a->cfg.n_sinks; ++k) {
		sink_reset(a, k);
		sink_settle(&a->sinks[k]);
	}
}

void acmp_open(struct acmp *a)
{
	if (!enter(a)) {
		return;
	}
	finish(a);
}

bool acmp_binding_latch(const struct acmp *a, unsigned sink, uint8_t payload[ACMP_BINDING_BYTES])
{
	if (sink >= a->cfg.n_sinks) {
		return false;
	}
	record_of(&a->sinks[sink], payload);
	return true;
}

bool acmp_view(const struct acmp *a, unsigned sink, struct acmp_sink_view *view)
{
	if (sink >= a->cfg.n_sinks) {
		return false;
	}
	view_of(&a->sinks[sink], view);
	return true;
}

bool acmp_change_pending(const struct acmp *a, unsigned sink)
{
	return sink < a->cfg.n_sinks && a->sinks[sink].change_owed != 0u;
}
