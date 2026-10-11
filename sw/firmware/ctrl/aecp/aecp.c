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

static void monitor(struct aecp *a, struct aecp_registration *r)
{
	aecp_port_begin(a);
	uint32_t draw = a->ports->random(a->ports->ctx);
	aecp_port_end(a);
	r->probing = 0;
	r->deadline = a->now + 30000u + draw % 30001u;
}

static void header(struct aecp *a, unsigned interface, uint64_t mac, uint64_t target,
		   uint64_t controller, uint16_t seq, uint16_t cmd, unsigned msg)
{
	memset(a->response, 0, sizeof a->response);
	wire_put_be(a->response, mac, 6);
	wire_put_be(a->response + 6, a->cfg.mac[interface], 6);
	wire_put_be(a->response + 12, 0x22f0u, 2);
	a->response[14] = 0xfbu;
	a->response[15] = (uint8_t)msg;
	wire_put_be(a->response + 18, target, 8);
	wire_put_be(a->response + 26, controller, 8);
	wire_put_be(a->response + 34, seq, 2);
	wire_put_be(a->response + 36, cmd, 2);
	a->response_interface = interface;
	a->recipient = 0;
	a->probe_recipient = -1;
	a->counter_event = a->cfg.model->count;
}

static void finish(struct aecp *a, unsigned status, size_t body)
{
	wire_put_be(a->response + 16, ((uint32_t)status << 11) | (12u + body), 2);
	a->response_bytes = 38u + body;
	a->response_owed = true;
}

static void arm(struct aecp *a)
{
	bool armed = a->locked || a->start_pending;
	uint32_t deadline = a->start_pending ? a->start_deadline : a->lock_deadline;
	for (unsigned i = 0; i < a->cfg.interfaces; ++i) {
		for (unsigned n = 0; n < AECP_REGISTRATIONS; ++n) {
			struct aecp_registration *r = &a->registry[i][n];
			if (r->used && (!armed || due(deadline, r->deadline))) {
				deadline = r->deadline;
				armed = true;
			}
		}
	}
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_event *e = &a->cfg.events[n];
		if (e->retry_pending != 0u && (!armed || due(deadline, e->retry_at))) {
			deadline = e->retry_at;
			armed = true;
		}
		if ((e->pending & 8u) != 0u && (e->retry_pending & 8u) == 0u &&
		    e->counter_sent && !e->awaiting_output &&
		    (!armed || due(deadline, e->counter_at))) {
			deadline = e->counter_at;
			armed = true;
		}
	}
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
	    cfg->model->count == 0u || cfg->model->configurations == 0u) {
		return false;
	}
	a->cfg = *cfg;
	a->ports = ports;
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
	return a->locked;
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
	for (unsigned n = 0; n < AECP_REGISTRATIONS; ++n) {
		struct aecp_registration *r = &a->registry[interface][n];
		if (r->used && r->probing != 0u && r->controller == wire_be64(p + 4) &&
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
			wire_put_be(a->response + 46, 1u, 4);
			body = 20u;
			status = 0u;
		} else if (cmd == 1u || cmd == 2u) {
			if (cmd == 2u || (bytes >= 40u && wire_be64(p + 32) != 0u && !aecp_foreign_lock(a))) {
				if (cmd == 1u && a->system_id != wire_be64(p + 32)) {
					a->system_id = wire_be64(p + 32);
					aecp_note(a, AECP_CHANGE_SYSTEM_ID, 0, 0);
					a->notify = false; // MVU defines no unsolicited SUID response.
				}
				a->response[44] = a->response[45] = 0;
				wire_put_be(a->response + 46, a->system_id, 8);
				body = 16u;
				status = 0u;
			}
		}
	}
	finish(a, status, body);
}

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
	for (unsigned n = 0; n < AECP_REGISTRATIONS; ++n) {
		struct aecp_registration *r = &a->registry[interface][n];
		if (r->used && r->controller == a->requester) {
			monitor(a, r);
		}
	}
	uint16_t cmd = (uint16_t)(wire_be16(p + 22) & 0x3fffu);
	uint64_t source = ((uint64_t)wire_be32(frame + 6) << 16) | wire_be16(frame + 10);
	header(a, interface, source, a->cfg.entity_id, a->requester, (uint16_t)wire_be16(p + 20), cmd, msg + 1u);
	if (msg == 6u) {
		mvu(a, p, bytes);
	} else if (msg == 8u) {
		// IEEE 9.7.4: empty HDCP data, retaining flags and fragment offset.
		wire_put_be(a->response + 36, 0u, 2);
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
		finish(a, status, result);
		if (a->start_pending) {
			/* Reserve service time and millisecond quantization within T_svc. */
			a->start_deadline = a->now + 8u;
		}
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
		a->cfg.events[d - a->cfg.model->descriptors].pending |= (uint8_t)(events & supported);
	}
}

static bool send(struct aecp *a)
{
	aecp_port_begin(a);
	bool ok = a->ports->send(a->ports->ctx, a->response_interface, a->response, a->response_bytes, a->tx_cookie);
	aecp_port_end(a);
	if (ok) {
		if (a->counter_event < a->cfg.model->count) {
			struct aecp_event *e = &a->cfg.events[a->counter_event];
			e->cookie = a->tx_cookie;
			e->awaiting_output = true;
		}
		++a->tx_cookie;
	}
	return ok;
}

void aecp_tx_complete(struct aecp *a, uint32_t cookie, uint32_t departure_ms)
{
	if (!aecp_enter(a)) {
		return;
	}
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
		struct aecp_event *e = &a->cfg.events[n];
		if (e->awaiting_output && e->cookie == cookie) {
			e->awaiting_output = false;
			e->counter_sent = true;
			e->counter_at = departure_ms + 1000u;
		}
	}
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
	while (a->notify && a->recipient < a->cfg.interfaces * AECP_REGISTRATIONS) {
		unsigned i = a->recipient / AECP_REGISTRATIONS;
		unsigned n = a->recipient % AECP_REGISTRATIONS;
		struct aecp_registration *r = &a->registry[i][n];
		if (r->used && r->controller != a->requester) {
			a->response_interface = i;
			wire_put_be(a->response, r->mac, 6);
			wire_put_be(a->response + 6, a->cfg.mac[i], 6);
			wire_put_be(a->response + 26, r->controller, 8);
			wire_put_be(a->response + 34, r->sequence, 2);
			a->response[36] |= 0x80u;
			if (!send(a)) {
				return true;
			}
			++r->sequence;
		}
		++a->recipient;
	}
	a->notify = false;
	return false;
}

static bool asynchronous(struct aecp *a)
{
	if (a->locked && due(a->now, a->lock_deadline)) {
		a->locked = false;
		a->lock_owner = 0;
		header(a, 0, 0, a->cfg.entity_id, 0, 0, 1u, 1u);
		wire_put_be(a->response + 38, 1u, 4);
		finish(a, AECP_SUCCESS, 16u);
		a->response_owed = false;
		a->notify = true;
		a->requester = 0;
		return true;
	}
	for (unsigned i = 0; i < a->cfg.interfaces; ++i) {
		for (unsigned n = 0; n < AECP_REGISTRATIONS; ++n) {
			struct aecp_registration *r = &a->registry[i][n];
			if (!r->used || !due(a->now, r->deadline)) {
				continue;
			}
			if (r->probing == 2u) {
				header(a, i, r->mac, a->cfg.entity_id, r->controller, r->sequence, 0x8025u, 1u);
				finish(a, AECP_SUCCESS, 0u);
				r->used = false;
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
	static const uint16_t commands[4] = {
		15u, 39u, 40u, 41u
	};
	for (size_t n = 0; n < a->cfg.model->count; ++n) {
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
			uint8_t input[4] = {0};
			wire_put_be(input, bit == 2u ? d->index : d->type, 2);
			if (bit != 2u) {
				wire_put_be(input + 2, d->index, 2);
			}
			header(a, 0, 0, a->cfg.entity_id, 0, 0, commands[bit], 1u);
			a->requester = 0;
			size_t bytes = 0;
			unsigned status = aecp_command(a, 0, commands[bit], input, 4u, a->response + 38, &bytes);
			if (status == AECP_SUCCESS) {
				e->pending &= (uint8_t)~(1u << bit);
				e->retry_pending &= (uint8_t)~(1u << bit);
				finish(a, status, bytes);
				a->response_owed = false;
				a->notify = true;
				if (bit == 3u) {
					a->counter_event = n;
				}
				return true;
			}
			// Keep the event; other snapshots progress before this retry.
			e->retry_pending |= (uint8_t)(1u << bit);
			e->retry_at = a->now + 1u;
		}
	}
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
	bool pending = asynchronous(a);
	arm(a);
	return pending;
}
