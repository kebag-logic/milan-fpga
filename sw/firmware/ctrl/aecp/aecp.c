// SPDX-License-Identifier: CERN-OHL-W-2.0
// Transport-independent AECP owner. No allocation, image or register access.
#include "aecp_internal.h"

static struct aecp *port_owner;

bool aecp_enter(struct aecp *a)
{
	if (port_owner != NULL || (a != NULL && a->in_port)) {
		if (a == NULL) a = port_owner;
		++a->reentries;
#ifdef CTRL_REENTRY_ASSERT
		ctrl_reentry_assert("aecp");
#endif
		return false;
	}
	return true;
}

void aecp_port_begin(struct aecp *a)
{
	a->in_port = true;
	port_owner = a;
}

void aecp_port_end(struct aecp *a)
{
	port_owner = NULL;
	a->in_port = false;
}

static uint32_t now(struct aecp *a)
{
	aecp_port_begin(a);
	uint32_t value = a->ports->now_ms(a->ports->ctx);
	aecp_port_end(a);
	a->now = value;
	return value;
}

static bool due(uint32_t time, uint32_t deadline)
{
	return (uint32_t)(time - deadline) < 0x80000000u;
}

_Static_assert(AECP_REGISTRATIONS == 16u, "16 per AVB Interface (Milan v1.2 5.3.4.2), a bit each in aecp.used");

// Whether registry[i][n] is used, off aecp.used (#665).
static bool used(const struct aecp *a, unsigned i, unsigned n)
{
	return ((a->used[i] >> n) & 1u) != 0u;
}

// aecp.live from every event, in descriptor order (#665).
static void relist(struct aecp *a)
{
	a->live = 0u;
	for (size_t n = a->cfg.model->count; n-- > 0u;) {
		struct aecp_event *e = &a->cfg.events[n];
		if ((e->pending | e->retry_pending) != 0u) {
			e->next = a->live;
			a->live = (uint16_t)(n + 1u);
		}
	}
}

// Link event n, which held neither a notice nor a retry, into aecp.live in
// descriptor order (#665).
static void list(struct aecp *a, size_t n)
{
	uint16_t *link = &a->live;
	while (*link != 0u && *link <= n) {
		link = &a->cfg.events[*link - 1u].next;
	}
	a->cfg.events[n].next = *link;
	*link = (uint16_t)(n + 1u);
}

static bool applied(struct aecp *a)
{
	aecp_port_begin(a);
	bool value = a->ports->applied(a->ports->ctx);
	aecp_port_end(a);
	return value;
}

static void monitor(struct aecp *a, struct aecp_registration *r)
{
	aecp_port_begin(a);
	uint32_t draw = a->ports->random(a->ports->ctx);
	aecp_port_end(a);
	r->probing = 0;
	r->deadline = a->now + 30000u + draw % 30001u;
}

// Big-endian header fields in 32-bit arithmetic: wire_put_be shifts its
// value as 64 bits, a runtime call a byte on RV32I (#665).
void aecp_put16(uint8_t *p, uint32_t v)
{
	p[0] = (uint8_t)(v >> 8);
	p[1] = (uint8_t)v;
}

void aecp_put32(uint8_t *p, uint32_t v)
{
	aecp_put16(p, v >> 16);
	aecp_put16(p + 2, v);
}

void aecp_put48(uint8_t *p, uint64_t v)
{
	aecp_put16(p, (uint32_t)(v >> 32));
	aecp_put32(p + 2, (uint32_t)v);
}

void aecp_put64(uint8_t *p, uint64_t v)
{
	aecp_put32(p, (uint32_t)(v >> 32));
	aecp_put32(p + 4, (uint32_t)v);
}

// The AECP_HEADER_BYTES of a response but its status and length, which
// finish() writes. Its body is zeroed and written by the path that builds
// it, so a response clears only the bytes it sends (#665, FR_NFR.md 3.4.1:
// clearing the whole 1,514-byte frame cost 3 ms a pass).
static void header(struct aecp *a, unsigned interface, uint64_t mac, uint64_t target,
		   uint64_t controller, uint16_t seq, uint16_t cmd, unsigned msg)
{
	aecp_put48(a->response, mac);
	aecp_put48(a->response + 6, a->cfg.mac[interface]);
	aecp_put16(a->response + 12, 0x22f0u);
	a->response[14] = 0xfbu;
	a->response[15] = (uint8_t)msg;
	aecp_put64(a->response + 18, target);
	aecp_put64(a->response + 26, controller);
	aecp_put16(a->response + 34, seq);
	aecp_put16(a->response + 36, cmd);
	a->response_interface = interface;
	a->recipient = 0;
	a->probe_recipient = -1;
	a->counter_event = a->cfg.model->count;
}

static void finish(struct aecp *a, unsigned status, size_t body)
{
	aecp_put16(a->response + 16, ((uint32_t)status << 11) | (uint32_t)(12u + body));
	a->response_bytes = 38u + body;
	a->response_owed = true;
}

// Exchange each value the waiting command changed with the one it found: its
// change is undone while it waits, and done again once applied (#665).
static void swap(struct aecp *a)
{
	for (unsigned k = 0; k < a->kept; ++k) {
		struct aecp_kept *e = &a->keep[k];
		for (unsigned n = 0; n < e->n; ++n) {
			uint8_t was = e->at[n];
			e->at[n] = e->was[n];
			e->was[n] = was;
		}
	}
}

// Answer the waiting command as the lock check refuses it: with the values in
// force, as its other refusals report them (IEEE 1722.1-2021 7.4.15.1).
static void refuse(struct aecp *a, unsigned status)
{
	size_t result = 0;
	a->refusing = true;
	(void)aecp_command(a, a->held_interface, (uint16_t)wire_be16(a->held + 36), a->held + 38,
			   a->held_bytes - 38u, a->response + 38, &result);
	finish(a, status, result);
}

static void arm(struct aecp *a)
{
	bool armed = a->locked || a->start_pending;
	uint32_t deadline = a->start_pending ? a->start_deadline : a->lock_deadline;
	for (unsigned i = 0; i < a->cfg.interfaces; ++i) {
		for (unsigned n = 0; (a->used[i] >> n) != 0u; ++n) {
			struct aecp_registration *r = &a->registry[i][n];
			if (used(a, i, n) && (!armed || due(deadline, r->deadline))) {
				deadline = r->deadline;
				armed = true;
			}
		}
	}
	bool left = false;
	bool held = false;
	for (unsigned k = a->notices ? a->live : 0u; k != 0u; k = a->cfg.events[k - 1u].next) {
		struct aecp_event *e = &a->cfg.events[k - 1u];
		left = true;
		// held for aecp_retry (THE RETRY): a notice no retry holds, which a round may not have reached beside a retry
		// of its event, and a due retry, since a timer already due would post an event every pass
		held = held || (e->pending & ~e->retry_pending & 7u) != 0u;
		if (e->retry_pending != 0u) {
			if (!a->retry_hold || !due(a->now, e->retry_at)) {
				if (!armed || due(deadline, e->retry_at)) {
					deadline = e->retry_at;
					armed = true;
				}
			} else {
				held = true;
			}
		}
		if ((e->pending & 8u) != 0u && (e->retry_pending & 8u) == 0u && !e->awaiting_output) {
			if (e->counter_sent && !due(a->now, e->counter_at)) {
				if (!armed || due(deadline, e->counter_at)) {
					deadline = e->counter_at;
					armed = true;
				}
			} else {
				held = true;
			}
		}
	}
	a->retry_held = held && a->retry_hold;
	a->notices = left;
	aecp_port_begin(a);
	a->ports->timer(a->ports->ctx, armed, deadline);
	aecp_port_end(a);
}

bool aecp_init(struct aecp *a, const struct aecp_config *cfg, const struct aecp_ports *ports)
{
	// Init storage may be uninitialized: charge its refusal to the caller.
	if (!aecp_enter(NULL)) return false;
	memset(a, 0, sizeof *a);
	if (cfg->interfaces == 0u || cfg->interfaces > AECP_INTERFACES ||
	    cfg->model->count == 0u || cfg->model->count >= 0xffffu || cfg->model->configurations == 0u) {
		return false;
	}
	a->cfg = *cfg;
	a->ports = ports;
	aecp_index(a);
	struct aecp_descriptor *entity = aecp_find(a, 0u, 0u, 0u);
	if (entity == NULL || entity->length < 312u ||
	    wire_be16(entity->value + 310) >= cfg->model->configurations) {
		return false;
	}
	a->configuration = (uint16_t)wire_be16(entity->value + 310);
	memset(cfg->events, 0, cfg->model->count * sizeof *cfg->events);
	for (size_t n = 0; n < cfg->model->count; ++n) {
		struct aecp_descriptor *d = &cfg->model->descriptors[n];
		if (d->type == 6u) {
			cfg->latency[d->index] = 0u;
		}
	}
	for (size_t n = 0; n < cfg->map_count; ++n) {
		struct aecp_map *m = &cfg->maps[n];
		if (m->default_count > m->capacity) {
			return false;
		}
		m->count = m->default_count;
		for (size_t k = 0; k < m->count; ++k) {
			m->rows[k] = m->defaults[k];
		}
	}
	a->counter_event = cfg->model->count;
	a->probe_recipient = -1;
	return true;
}

void aecp_open(struct aecp *a)
{
	if (!aecp_enter(a)) {
		return;
	}
	a->open = true;
	a->notices = true; // rescan the events, whatever set them before the open
	relist(a);
	(void)now(a);
	arm(a);
}

bool aecp_ready(struct aecp *a)
{
	return aecp_enter(a) && a->open && !a->response_owed && !a->notify;
}

bool aecp_locked(struct aecp *a, uint64_t *owner)
{
	if (!aecp_enter(a)) return false;
	*owner = a->lock_owner;
	return a->locked || a->unlocked; // the lock in force (aecp_other_lock)
}

unsigned aecp_registry_command(struct aecp *a, unsigned interface, uint16_t cmd, uint64_t mac,
			      const uint8_t *in, size_t len, uint8_t *out, size_t *bytes)
{
	(void)in;
	(void)len; // Milan 5.4.2.21 accepts the older no-flags form.
	*bytes = cmd == 36u ? 4u : 0u;
	memset(out, 0, 4u);
	struct aecp_registration *found = NULL, *free_slot = NULL;
	for (unsigned n = 0; n < AECP_REGISTRATIONS; ++n) {
		struct aecp_registration *r = &a->registry[interface][n];
		if (r->used && r->controller == a->requester) {
			found = r;
		} else if (!r->used && free_slot == NULL) {
			free_slot = r;
		}
	}
	if (cmd == 37u) {
		if (found != NULL) {
			found->used = false;
			a->used[interface] &= (uint16_t)~(1u << (found - a->registry[interface]));
		}
		return AECP_SUCCESS;
	}
	if (found == NULL) {
		found = free_slot;
		if (found == NULL) {
			return AECP_NO_RESOURCES;
		}
		memset(found, 0, sizeof *found);
		found->controller = a->requester;
		found->used = true;
		a->used[interface] |= (uint16_t)(1u << (found - a->registry[interface]));
	}
	found->mac = mac;
	monitor(a, found);
	return AECP_SUCCESS;
}

static bool probe_reply(struct aecp *a, unsigned interface, const uint8_t *p)
{
	if ((wire_be16(p + 22) & 0xbfffu) != 3u || wire_be64(p + 12) != a->cfg.entity_id) {
		return false;
	}
	for (unsigned n = 0; (a->used[interface] >> n) != 0u; ++n) {
		struct aecp_registration *r = &a->registry[interface][n];
		if (used(a, interface, n) && r->probing != 0u && r->controller == wire_be64(p + 4) &&
		    r->probe_sequence == wire_be16(p + 20)) {
			monitor(a, r);
			return true;
		}
	}
	return false;
}

static void mvu(struct aecp *a, const uint8_t *p, size_t bytes)
{
	size_t body = bytes - 24u;
	memcpy(a->response + 36, p + 22, bytes - 22u);
	unsigned status = 1u;
	if (bytes >= 32u && wire_be32(p + 22) == 0x001bc50au && wire_be16(p + 26) == 0xc100u) {
		unsigned cmd = (unsigned)wire_be16(p + 28) & 0x7fffu;
		a->response[42] &= 0x7fu;
		if (cmd == 0u) {
			memset(a->response + 44, 0, 14u);
			aecp_put32(a->response + 46, 1u);
			body = 20u;
			status = 0u;
		} else if (cmd == 1u || cmd == 2u) {
			bool set = cmd == 1u && bytes >= 40u && wire_be64(p + 32) != 0u;
			if (cmd == 2u || (set && !aecp_other_lock(a))) {
				status = 0u;
				if (set && a->refusing) {
					// refused as every change is while one waits for the
					// platform, with the identifier in force (#665; Milan
					// v1.2 5.4.4.2)
					status = AECP_ENTITY_MISBEHAVING;
				} else if (set && a->system_id != wire_be64(p + 32)) {
					a->system_id = wire_be64(p + 32);
					aecp_note(a, AECP_CHANGE_SYSTEM_ID, 0, 0);
					a->notify = false; // MVU defines no unsolicited SUID response.
				}
				a->response[44] = a->response[45] = 0;
				aecp_put64(a->response + 46, a->system_id);
				body = 16u;
			}
		}
	}
	finish(a, status, body);
}

static bool transmit(struct aecp *a);

void aecp_rx(struct aecp *a, unsigned interface, const uint8_t *frame, size_t len)
{
	if (!aecp_enter(a)) {
		return;
	}
	if (!a->open || interface >= a->cfg.interfaces || len < 38u || len > AECP_FRAME_BYTES) {
		++a->malformed;
		return;
	}
	const uint8_t *p = frame + 14;
	size_t bytes = 12u + (size_t)(wire_be16(p + 2) & 0x7ffu);
	unsigned msg = p[1] & 15u;
	uint64_t mac = ((uint64_t)wire_be32(frame) << 16) | wire_be16(frame + 4);
	if (wire_be16(frame + 12) != 0x22f0u || p[0] != 0xfbu || (p[1] & 0xf0u) != 0u ||
	    mac != a->cfg.mac[interface] || bytes < 24u || bytes > len - 14u) {
		++a->malformed;
		return;
	}
	(void)now(a);
	if (msg == 1u) {
		if (!probe_reply(a, interface, p)) {
			++a->ignored;
		}
		arm(a);
		return;
	}
	// IEEE Table 9-1: reserved/extended message types have no command contract.
	if ((msg != 0u && msg != 2u && msg != 4u && msg != 6u && msg != 8u) ||
	    wire_be64(p + 4) != a->cfg.entity_id) {
		++a->ignored;
		return;
	}
	if (msg == 8u && bytes < 28u) {
		++a->malformed;
		return;
	}
	if (!aecp_ready(a)) {
		++a->busy_drops;
		return;
	}
	a->requester = wire_be64(p + 12);
	for (unsigned n = 0; (a->used[interface] >> n) != 0u; ++n) {
		struct aecp_registration *r = &a->registry[interface][n];
		if (used(a, interface, n) && r->controller == a->requester) {
			monitor(a, r);
		}
	}
	uint16_t cmd = (uint16_t)(wire_be16(p + 22) & 0x3fffu);
	uint64_t source = ((uint64_t)wire_be32(frame + 6) << 16) | wire_be16(frame + 10);
	header(a, interface, source, a->cfg.entity_id, a->requester, (uint16_t)wire_be16(p + 20), cmd, msg + 1u);
	// While a change waits, the platform has not applied every change, or an
	// expiry is not yet notified, no change is taken (#665); a command that may
	// change something records it afresh
	a->refusing = a->waiting || a->unlocked || !applied(a);
	if (!a->refusing) {
		a->kept = 0;
	}
	if (msg == 6u) {
		mvu(a, p, bytes);
	} else if (msg == 8u) {
		// IEEE 9.7.4: empty HDCP data, retaining flags and fragment offset.
		memset(a->response + AECP_HEADER_BYTES, 0, 4u);
		aecp_put16(a->response + 36, 0u);
		a->response[38] = p[24];
		memcpy(a->response + 40, p + 26, 2u);
		finish(a, AECP_NOT_IMPLEMENTED, 4u);
	} else if (msg == 2u || msg == 4u) {
		// IEEE 9.4.4/9.4.5 and 9.5.4/9.5.5: unsupported AA and AV/C.
		memcpy(a->response + 36, p + 22, bytes - 22u);
		finish(a, AECP_NOT_IMPLEMENTED, bytes - 24u);
	} else {
		size_t result = 0;
		unsigned status;
		if (cmd == 36u || cmd == 37u) {
			status = aecp_registry_command(a, interface, cmd, source, p + 24, bytes - 24u,
					       a->response + 38, &result);
		} else {
			status = aecp_command(a, interface, cmd, p + 24, bytes - 24u, a->response + 38, &result);
		}
		if (status == AECP_ENTITY_LOCKED && a->refusing && !aecp_other_lock(a)) {
			status = AECP_ENTITY_MISBEHAVING;
		}
		finish(a, status, result);
		if (a->notify && cmd < 32u && ((AECP_WAITS >> cmd) & 1u) != 0u && !applied(a)) {
			// the face has not taken the change: it waits, undone, so every
			// response and notification meanwhile reports the values in force;
			// IN_PROGRESS, then one final response (#665; IEEE 1722.1-2021
			// 7.4, 9.3.2.6)
			memcpy(a->held, a->response, a->response_bytes);
			a->held_bytes = a->response_bytes;
			a->held_interface = interface;
			a->held_requester = a->requester;
			a->waiting = true;
			a->notify = false;
			a->wait_deadline = a->now + AECP_WAIT_MS;
			swap(a);
			refuse(a, AECP_IN_PROGRESS);
		}
		if (a->start_pending) {
			/* Reserve service time and millisecond quantization within T_svc. */
			a->start_deadline = a->now + 8u;
		}
	}
	// A plain response is committed in the record's turn, so the pass may take the channel's next (#665)
	if (!a->notify && !a->waiting && !a->start_pending) {
		(void)transmit(a);
	}
	arm(a);
}

void aecp_start_done(struct aecp *a, bool success, bool changed)
{
	if (!aecp_enter(a) || !a->start_pending) {
		return;
	}
	a->start_pending = false;
	a->notify = success && changed;
	finish(a, success ? AECP_SUCCESS : AECP_ENTITY_MISBEHAVING, 4u);
}

void aecp_changed(struct aecp *a, uint16_t type, uint16_t index, unsigned events)
{
	if (!aecp_enter(a)) {
		return;
	}
	struct aecp_descriptor *d = aecp_find(a, a->configuration, type, index);
	if (d != NULL) {
		unsigned supported = type == 5u || type == 6u ? 9u : type == 9u ? 14u : type == 36u ? 8u : 0u;
		size_t n = (size_t)(d - a->cfg.model->descriptors);
		bool listed = (a->cfg.events[n].pending | a->cfg.events[n].retry_pending) != 0u;
		a->cfg.events[n].pending |= (uint8_t)(events & supported);
		a->notices = true;
		// An event that held neither a notice nor a retry joins aecp.live (#665).
		if (!listed && a->cfg.events[n].pending != 0u) {
			list(a, n);
		}
	}
}

// What the frame just accepted leaves a counter notice waiting on (aecp_tx_complete): a later cookie for the same
// descriptor supersedes an earlier completion.
static void sent_frame(struct aecp *a)
{
	if (a->counter_event < a->cfg.model->count) {
		struct aecp_event *e = &a->cfg.events[a->counter_event];
		if (!e->awaiting_output) {
			e->awaited_next = a->awaited;
			a->awaited = (uint16_t)(a->counter_event + 1u);
		}
		e->cookie = a->tx_cookie;
		e->awaiting_output = true;
	}
	++a->tx_cookie;
}

static bool send(struct aecp *a)
{
	aecp_port_begin(a);
	bool ok = a->ports->send(a->ports->ctx, a->response_interface, a->response, a->response_bytes, a->tx_cookie);
	aecp_port_end(a);
	if (ok) {
		sent_frame(a);
	}
	return ok;
}

void aecp_tx_complete(struct aecp *a, uint32_t cookie, uint32_t departure_ms)
{
	if (!aecp_enter(a)) {
		return;
	}
	// a round's completions come together, in the pass after it: only the notices that wait are walked (#665)
	for (uint16_t *link = &a->awaited; *link != 0u; link = &a->cfg.events[*link - 1u].awaited_next) {
		struct aecp_event *e = &a->cfg.events[*link - 1u];
		if (e->cookie == cookie) {
			*link = e->awaited_next;
			e->awaiting_output = false;
			e->counter_sent = true;
			e->counter_at = departure_ms + 1000u;
			break;
		}
	}
}

// A recipient's fields of a notice's frame (Milan v1.2 5.4.5.1; IEEE 1722.1-2021 7.5.2, 9.2.1.1): its MAC as the
// destination, its interface's as the source, its entity ID as the controller_entity_id and its sequence_id, each
// byte stored once from the two words that hold it (#665: through the put helpers' calls these were a third of a
// recipient's cost).
static inline void address(uint8_t *f, const struct aecp_registration *r, uint64_t source)
{
	const uint32_t mac_hi = (uint32_t)(r->mac >> 32), mac_lo = (uint32_t)r->mac;
	const uint32_t src_hi = (uint32_t)(source >> 32), src_lo = (uint32_t)source;
	const uint32_t id_hi = (uint32_t)(r->controller >> 32), id_lo = (uint32_t)r->controller;
	f[0] = (uint8_t)(mac_hi >> 8);
	f[1] = (uint8_t)mac_hi;
	f[2] = (uint8_t)(mac_lo >> 24);
	f[3] = (uint8_t)(mac_lo >> 16);
	f[4] = (uint8_t)(mac_lo >> 8);
	f[5] = (uint8_t)mac_lo;
	f[6] = (uint8_t)(src_hi >> 8);
	f[7] = (uint8_t)src_hi;
	f[8] = (uint8_t)(src_lo >> 24);
	f[9] = (uint8_t)(src_lo >> 16);
	f[10] = (uint8_t)(src_lo >> 8);
	f[11] = (uint8_t)src_lo;
	f[26] = (uint8_t)(id_hi >> 24);
	f[27] = (uint8_t)(id_hi >> 16);
	f[28] = (uint8_t)(id_hi >> 8);
	f[29] = (uint8_t)id_hi;
	f[30] = (uint8_t)(id_lo >> 24);
	f[31] = (uint8_t)(id_lo >> 16);
	f[32] = (uint8_t)(id_lo >> 8);
	f[33] = (uint8_t)id_lo;
	f[34] = (uint8_t)(r->sequence >> 8);
	f[35] = (uint8_t)r->sequence;
}

// A notice to every recipient from a->recipient on, true while one is left: the
// port's guard taken once, and through the fan port, which is still reading a
// frame as the next recipient's is written, so the two alternate between the
// frame and its copy past it (#665: a recipient's frame sets the notice's cost,
// and with it how many a pass carries, THE RETRY in ctrl_loop.h). The notice is
// built once and each recipient's frame only addressed (address), the used
// registrations walked by their mask. A->requester is left out (Milan v1.2
// 5.4.5.1). Fan_end's completion stands for every frame. A frame the fan port
// reports lost is owed: the notice resumes at its recipient, whose sequence_id
// it did not spend (IEEE 1722.1-2021 7.5.2: each registered controller is sent
// the notice).
static bool fan_out(struct aecp *a)
{
	const unsigned total = a->cfg.interfaces * AECP_REGISTRATIONS;
	const bool fan = a->ports->fan != NULL && a->response_bytes <= AECP_FAN_BYTES;
	uint8_t *frame = a->response;
	uint8_t *other = a->response + AECP_FAN_BYTES;
	bool owed = false;
	bool lost = false;
	unsigned held = 0; // the recipient of the frame the fan port holds uncommitted, and its registration
	struct aecp_registration *held_r = NULL;
	a->response[36] |= 0x80u;
	if (fan) {
		memcpy(other, frame, a->response_bytes);
	}
	aecp_port_begin(a);
	unsigned k = a->recipient;
	while (!owed && k < total) {
		const unsigned i = k / AECP_REGISTRATIONS;
		struct aecp_registration *r = &a->registry[i][k % AECP_REGISTRATIONS];
		// the interface's used slots from k on (aecp.used), each a step of r and k
		for (unsigned slots = (unsigned)a->used[i] >> (k % AECP_REGISTRATIONS); slots != 0u; slots >>= 1, ++r, ++k) {
			if ((slots & 1u) == 0u || r->controller == a->requester) {
				continue;
			}
			address(frame, r, a->cfg.mac[i]);
			const enum aecp_fan taken = fan ? a->ports->fan(a->ports->ctx, i, frame, a->response_bytes) :
				a->ports->send(a->ports->ctx, i, frame, a->response_bytes, a->tx_cookie) ? AECP_FAN_TAKEN :
				AECP_FAN_REFUSED;
			if (taken != AECP_FAN_TAKEN) {
				owed = true;
				lost = taken == AECP_FAN_LOST;
				break;
			}
			if (fan) {
				uint8_t *next = other;
				other = frame;
				frame = next;
				held = k;
				held_r = r;
			} else {
				sent_frame(a);
			}
			++r->sequence;
		}
		if (!owed) {
			k = (i + 1u) * AECP_REGISTRATIONS;
		}
	}
	if (fan) {
		// a queue with no room for its completion leaves the notice owed, past its last recipient; a last frame lost
		// leaves it owed at that frame's
		const enum aecp_fan end = a->ports->fan_end(a->ports->ctx, a->tx_cookie);
		lost = lost || end == AECP_FAN_LOST;
		owed = end != AECP_FAN_TAKEN || owed;
		if (!owed) {
			sent_frame(a);
		}
	}
	if (lost) {
		// a lost frame is one this walk started: its recipient is sent it again, at the sequence_id it did not have
		k = held;
		--held_r->sequence;
	}
	a->recipient = k;
	aecp_port_end(a);
	a->notify = owed;
	return owed;
}

static bool transmit(struct aecp *a)
{
	if (a->response_owed) {
		if (!send(a)) {
			return true;
		}
		a->response_owed = false;
		if (a->probe_recipient >= 0) {
			unsigned k = (unsigned)a->probe_recipient;
			a->registry[k / AECP_REGISTRATIONS][k % AECP_REGISTRATIONS].deadline = now(a) + 250u;
			a->probe_recipient = -1;
		}
	}
	return a->notify && fan_out(a);
}

static bool scan(struct aecp *a);

static bool asynchronous(struct aecp *a)
{
	if (a->locked && due(a->now, a->lock_deadline)) {
		// released to the platform; until it applied the release the lock
		// holds, by its owner, for every response and read (#665)
		a->locked = false;
		aecp_note(a, AECP_CHANGE_LOCK, 0, 0);
		a->notify = false;
		a->unlocked = true;
	}
	if (a->unlocked && applied(a)) {
		// Milan v1.2 5.4.2.2: the expiry's notification, once the platform
		// applied the release, however late (#665)
		a->unlocked = false;
		a->lock_owner = 0;
		header(a, 0, 0, a->cfg.entity_id, 0, 0, 1u, 1u);
		memset(a->response + AECP_HEADER_BYTES, 0, 16u);
		aecp_put32(a->response + 38, 1u);
		finish(a, AECP_SUCCESS, 16u);
		a->response_owed = false;
		a->notify = true;
		a->requester = 0;
		return true;
	}
	for (unsigned i = 0; i < a->cfg.interfaces; ++i) {
		for (unsigned n = 0; (a->used[i] >> n) != 0u; ++n) {
			struct aecp_registration *r = &a->registry[i][n];
			if (!used(a, i, n) || !due(a->now, r->deadline)) {
				continue;
			}
			if (r->probing == 2u) {
				header(a, i, r->mac, a->cfg.entity_id, r->controller, r->sequence, 0x8025u, 1u);
				finish(a, AECP_SUCCESS, 0u);
				r->used = false;
				a->used[i] &= (uint16_t)~(1u << n);
			} else {
				if (r->probing == 0u) {
					r->probe_sequence = a->probe_sequence++;
				}
				++r->probing;
				header(a, i, r->mac, r->controller, a->cfg.entity_id, r->probe_sequence, 3u, 0u);
				finish(a, AECP_SUCCESS, 0u);
				a->probe_recipient = (int)(i * AECP_REGISTRATIONS + n);
			}
			return true;
		}
	}
	// With retry_hold every notice waits for aecp_retry's round (THE RETRY), so none stands beside a pass's input
	return !a->retry_hold && scan(a);
}

// The event scan: each event holding a notice or a retry, in descriptor order, its notices tried and the first built
// returned. With aecp.retry_hold only aecp_retry's round calls it (THE RETRY, ctrl_loop.h; #665).
static bool scan(struct aecp *a)
{
	static const uint16_t commands[4] = {
		15u, 39u, 40u, 41u
	};
	bool left = false;
	for (uint16_t *link = a->notices ? &a->live : NULL; link != NULL && *link != 0u;
	     link = &a->cfg.events[*link - 1u].next) {
		size_t n = *link - 1u;
		struct aecp_event *e = &a->cfg.events[n];
		struct aecp_descriptor *d = &a->cfg.model->descriptors[n];
		if (e->retry_pending != 0u && due(a->now, e->retry_at)) {
			e->retry_pending = 0u;
		}
		for (unsigned bit = 0; bit < 4u; ++bit) {
			if ((e->pending & (1u << bit)) == 0u ||
			    (e->retry_pending & (1u << bit)) != 0u ||
			    (bit == 3u && (e->awaiting_output || (e->counter_sent && !due(a->now, e->counter_at))))) {
				continue;
			}
			// A port that refused this round refuses the rest of it: one attempt a port (AECP_ROUND_PORTS), and what it
			// skipped stays due, so the next round tries the next of them. A round's time ends before an attempt.
			const unsigned port = 1u << (bit + (bit == 1u || bit == 2u ? 4u * (d->index & 1u) : 0u));
			if ((a->refused & port) != 0u) {
				continue;
			}
			if (a->round_us < a->notice_us) {
				return false;
			}
			uint8_t input[4] = {0};
			aecp_put16(input, bit == 2u ? d->index : d->type);
			if (bit != 2u) {
				aecp_put16(input + 2, d->index);
			}
			header(a, 0, 0, a->cfg.entity_id, 0, 0, commands[bit], 1u);
			a->requester = 0;
			size_t bytes = 0;
			unsigned status = aecp_command(a, 0, commands[bit], input, 4u, a->response + 38, &bytes);
			if (status == AECP_SUCCESS) {
				e->pending &= (uint8_t)~(1u << bit);
				e->retry_pending &= (uint8_t)~(1u << bit);
				if (e->pending == 0u) {
					e->retry_ms = 0u;
				}
				// An event holding neither a notice nor a retry leaves aecp.live (#665).
				if ((e->pending | e->retry_pending) == 0u) {
					*link = e->next;
				}
				finish(a, status, bytes);
				a->response_owed = false;
				a->notify = true;
				if (bit == 3u) {
					a->counter_event = n;
				}
				return true;
			}
			// Keep the event; other snapshots progress before this retry, which
			// the first failure of a round schedules (AECP_RETRY_MAX_MS).
			if (e->retry_pending == 0u) {
				unsigned wait = e->retry_ms != 0u ? e->retry_ms : 1u;
				e->retry_at = a->now + wait;
				e->retry_ms = (uint8_t)(wait < AECP_RETRY_MAX_MS ? wait << 1 : AECP_RETRY_MAX_MS);
			}
			e->retry_pending |= (uint8_t)(1u << bit);
			if (a->retry_hold) {
				a->round_us -= AECP_ATTEMPT_US;
				a->refused |= (uint8_t)port;
			}
		}
		// Only a built notice clears its pending bit, and that returns above;
		// a retry bit is set only on a pending one. So this event still holds one.
		left = true;
	}
	a->notices = left;
	return false;
}

bool aecp_poll(struct aecp *a)
{
	if (!aecp_enter(a) || !a->open) {
		return false;
	}
	(void)now(a);
	if (a->start_pending) {
		if (!due(a->now, a->start_deadline)) {
			return true;
		}
		aecp_start_done(a, false, false);
	}
	if (transmit(a)) {
		return true;
	}
	if (a->waiting) {
		bool taken = applied(a);
		if (!taken && !due(a->now, a->wait_deadline)) {
			return true;
		}
		// Taken by every interface: done again, then answered and notified. Not
		// taken in time: it stays undone and the command fails, notifying no
		// one. Either way the face is given the values in force.
		a->waiting = false;
		if (taken) {
			swap(a);
		}
		aecp_note(a, a->noted, a->noted_type, a->noted_index);
		a->notify = taken;
		// the held response; every response since set the rest as header() does
		memcpy(a->response, a->held, a->held_bytes);
		a->response_bytes = a->held_bytes;
		a->response_interface = a->held_interface;
		a->requester = a->held_requester;
		a->response_owed = true;
		if (!taken) {
			refuse(a, AECP_ENTITY_MISBEHAVING);
		}
		return true;
	}
	bool pending = asynchronous(a);
	arm(a);
	return pending || a->retry_held;
}

// What aecp_poll sends or answers first waits for its pass, and THE RETRY's round for it.
static bool round_waits(const struct aecp *a)
{
	return a->response_owed || a->notify || a->waiting || a->start_pending;
}

bool aecp_retry(struct aecp *a, unsigned notices, int32_t left_us)
{
	if (!aecp_enter(a) || !a->open) {
		return false;
	}
	if (round_waits(a)) {
		return a->retry_held;
	}
	(void)now(a);
	bool owed = false;
	a->round_us = left_us;
	a->refused = 0u;
	// every attempt starts with a notice's time left, and a refused one is charged to the round (scan)
	for (unsigned n = 0; n < notices && !owed && scan(a); ++n) {
		a->round_us -= a->notice_us;
		owed = transmit(a);
	}
	arm(a);
	return owed || a->retry_held;
}

bool aecp_retry_aged(struct aecp *a, uint32_t pace_ms)
{
	// only a held notice, as arm left it, and only when the round would try it now
	if (!aecp_enter(a) || !a->retry_held || round_waits(a) || !due(now(a), a->retry_pace)) {
		return false;
	}
	a->retry_pace = a->now + pace_ms;
	return true;
}
