// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Annex B state transitions with bounded output storage and deferred service.
#include "maap.h"

#include <assert.h>
#include <string.h>

#include "wire.h"

static bool enter(struct maap *m)
{
	if (m->in_call) {
		m->reentries++;
		assert(!m->in_call);
		return false;
	}
	m->in_call = true;
	return true;
}

static bool pool_range(uint64_t base, uint16_t count)
{
	return base >= MAAP_POOL_BASE &&
	       base <= MAAP_POOL_BASE + MAAP_POOL_SIZE - count;
}

// Maximal-period xorshift32. Seed is the low sum of MAC and clock (B.3.6.1).
static uint32_t random_word(struct maap *m)
{
	uint32_t x = m->rng;
	x ^= x << 13;
	x ^= x >> 17;
	x ^= x << 5;
	m->rng = x;
	return x;
}

static uint32_t draw(struct maap *m, uint32_t size)
{
	// The source cycles over 1..UINT32_MAX. Reject the incomplete bucket
	// rather than biasing pool addresses. At most size draws are required:
	// at most size-1 distinct source words are outside the complete buckets.
	uint32_t limit = UINT32_MAX - UINT32_MAX % size;
	uint32_t word;
	do {
		word = random_word(m);
	} while (word > limit);
	return (word - 1u) % size;
}

static void publish(struct maap *m, uint16_t count, bool valid)
{
	m->valid = valid;
	m->ports->range(m->ports->ctx, m->interface, m->base, count, valid);
}

static void stop_timer(struct maap *m)
{
	m->timer_running = false;
	m->expiry_owed = false;
	m->ports->timer_stop(m->ports->ctx, m->interface);
}

static void start_timer(struct maap *m, bool announce)
{
	uint32_t base = announce ? MAAP_ANNOUNCE_BASE_MS : MAAP_PROBE_BASE_MS;
	uint32_t variation = announce ? MAAP_ANNOUNCE_VARIATION_MS : MAAP_PROBE_VARIATION_MS;
	// B.3.4 strict endpoints. Reserve 10 ms at both ends for service jitter.
	m->last_delay_ms = base + MAAP_SERVICE_MS + 1u + draw(m, variation - 2u * MAAP_SERVICE_MS - 1u);
	m->timer_running = true;
	m->ports->timer_start(m->ports->ctx, m->interface, m->last_delay_ms);
}

static void enqueue(struct maap *m, uint8_t type, uint64_t dst, uint64_t requested,
		    uint16_t count, uint64_t conflict, uint16_t conflict_count)
{
	if (m->queued == MAAP_QUEUE_FRAMES) {
		m->overflow++;
		return;
	}
	uint8_t *f = m->queue[m->queued++];
	memset(f, 0, MAAP_FRAME_BYTES);
	wire_put_be(f, dst, 6);
	wire_put_be(f + 6, m->mac, 6);
	wire_put_be(f + 12, 0x22f0u, 2);
	f[14] = 0xfeu;
	f[15] = type;
	f[16] = 0x08u; // maap_version=1, B.2.3; stream_id remains zero, B.2.4
	f[17] = 16u;   // B.2.1: control_data_length, not total PDU length
	wire_put_be(f + 26, requested, 6);
	wire_put_be(f + 32, count, 2);
	wire_put_be(f + 34, conflict, 6);
	wire_put_be(f + 40, conflict_count, 2);
}

static void request(struct maap *m, uint8_t type)
{
	enqueue(m, type, MAAP_MULTICAST, m->base, m->count, 0, 0);
}

static void reserve(struct maap *m, uint64_t preferred)
{
	m->base = preferred != 0u ? preferred : MAAP_POOL_BASE + draw(m, MAAP_POOL_SIZE - m->count + 1u);
	m->preferred = 0; // Table B.7 note a applies once, never to conflict Restart!
	m->probe_count = MAAP_PROBE_RETRANSMITS;
	publish(m, m->count, false);
	start_timer(m, false);
	request(m, MAAP_MSG_PROBE); // Table B.7 ReserveAddress!: initial send
	m->state = MAAP_PROBE;
}

static void restart(struct maap *m)
{
	stop_timer(m);
	m->queued = 0; // old allocation's output must not advertise a lost range
	m->state = MAAP_INITIAL;
	reserve(m, 0);
}

static void expire(struct maap *m)
{
	m->timer_running = false;
	m->expiry_owed = false;
	if (m->state == MAAP_PROBE) {
		start_timer(m, false);
		request(m, MAAP_MSG_PROBE);
		m->probe_count--; // B.3.6.3: only a retransmission decrements
		if (m->probe_count == 0u) {
			stop_timer(m);
			start_timer(m, true);
			request(m, MAAP_MSG_ANNOUNCE);
			m->state = MAAP_DEFEND;
		}
	} else {
		start_timer(m, true);
		request(m, MAAP_MSG_ANNOUNCE);
	}
}

static bool pump(struct maap *m)
{
	for (unsigned n = 0; n < 2u && m->queued != 0u; ++n) {
		if (!m->ports->send(m->ports->ctx, m->interface, m->queue[0], MAAP_FRAME_BYTES)) {
			m->deferred++;
			return true;
		}
		if (m->queue[0][15] == MAAP_MSG_ANNOUNCE && !m->valid) {
			publish(m, m->count, true);
		}
		m->queued--;
		for (unsigned i = 0; i < m->queued; ++i) {
			memcpy(m->queue[i], m->queue[i + 1u], MAAP_FRAME_BYTES);
		}
	}
	if (m->queued == 0u && m->expiry_owed) {
		expire(m);
	}
	return m->queued != 0u;
}

bool maap_init(struct maap *m, const struct maap_ports *ports, unsigned interface,
	       uint64_t mac, uint16_t count)
{
	memset(m, 0, sizeof *m);
	if (interface > UINT8_MAX || mac == 0u || mac > UINT64_C(0xffffffffffff) ||
	    (mac & UINT64_C(0x010000000000)) != 0u || count == 0u || count > MAAP_POOL_SIZE) {
		return false;
	}
	m->ports = ports;
	m->interface = (uint8_t)interface;
	m->mac = mac;
	m->count = count;
	m->operational = true;
	return true;
}

bool maap_begin(struct maap *m, uint64_t preferred)
{
	if (!enter(m)) {
		return false;
	}
	bool accepted = preferred == 0u || pool_range(preferred, m->count);
	if (accepted && m->state == MAAP_INITIAL) {
		m->preferred = preferred;
		m->enabled = true;
		m->rng = (uint32_t)m->mac + m->ports->clock(m->ports->ctx);
		if (m->rng == 0u) {
			m->rng = 1u;
		}
		if (m->operational) {
			reserve(m, preferred);
			(void)pump(m);
		} else {
			publish(m, 0, false);
		}
	}
	m->in_call = false;
	return accepted;
}

static void withdraw(struct maap *m)
{
	stop_timer(m);
	m->state = MAAP_INITIAL;
	m->queued = 0;
	publish(m, 0, false);
}

void maap_release(struct maap *m)
{
	if (!enter(m)) {
		return;
	}
	if (m->state != MAAP_INITIAL) {
		withdraw(m);
	}
	m->enabled = false;
	m->in_call = false;
}

void maap_port_operational(struct maap *m, bool up)
{
	if (!enter(m)) {
		return;
	}
	m->operational = up;
	if (m->enabled) {
		if (up) {
			if (m->preferred != 0u) {
				reserve(m, m->preferred); // Begin! accepted before the port was operational
			} else {
				restart(m); // Table B.7 PortOperational! in every state
			}
			(void)pump(m);
		} else {
			withdraw(m);
		}
	}
	m->in_call = false;
}

static uint64_t reverse_mac(uint64_t mac)
{
	uint64_t reversed = 0;
	for (unsigned i = 0; i < 6u; ++i) {
		reversed = (reversed << 8) | (mac & 0xffu);
		mac >>= 8;
	}
	return reversed;
}

static uint64_t mac_at(const uint8_t *p)
{
	return ((uint64_t)wire_be32(p) << 16) | wire_be16(p + 4);
}

static bool decode(struct maap *m, const uint8_t *f, size_t len)
{
	if (len < 42u || wire_be16(f + 12) != 0x22f0u || f[14] != 0xfeu ||
	    (f[15] & 0xf0u) != 0u || (f[15] & 0x0fu) < MAAP_MSG_PROBE || (f[15] & 0x0fu) > MAAP_MSG_ANNOUNCE ||
	    (wire_be16(f + 16) & 0x7ffu) < 16u || (wire_be16(f + 16) & 0x7ffu) > len - 26u ||
	    ((f[16] >> 3) <= 1u && (wire_be16(f + 16) & 0x7ffu) != 16u) ||
	    mac_at(f + 6) == 0u || (f[6] & 1u) != 0u) {
		return false;
	}
	uint64_t dst = mac_at(f);
	return dst == MAAP_MULTICAST || (f[15] == MAAP_MSG_DEFEND && dst == m->mac);
}

void maap_rx(struct maap *m, const uint8_t *f, size_t len)
{
	if (!enter(m)) {
		return;
	}
	if (!decode(m, f, len)) {
		m->discarded++;
	} else if (m->state != MAAP_INITIAL) {
		uint8_t type = f[15];
		uint64_t peer = mac_at(f + 6);
		uint64_t start = mac_at(f + (type == MAAP_MSG_DEFEND ? 34 : 26));
		uint16_t count = wire_be16(f + (type == MAAP_MSG_DEFEND ? 40 : 32));
		uint64_t end = start + count;
		uint64_t ours_end = m->base + m->count;
		if (count != 0u && start < ours_end && m->base < end) {
			if (type == MAAP_MSG_PROBE && m->state == MAAP_DEFEND) {
				uint64_t overlap = start > m->base ? start : m->base;
				uint64_t last = end < ours_end ? end : ours_end;
				enqueue(m, MAAP_MSG_DEFEND, peer, start, count, overlap, (uint16_t)(last - overlap));
			} else if ((m->state == MAAP_PROBE && type != MAAP_MSG_PROBE) ||
				   reverse_mac(m->mac) >= reverse_mac(peer)) {
				m->conflicts++;
				restart(m); // B.3.2/Table B.7; B.3.6.4 tie break only where named
			}
		}
		(void)pump(m);
	}
	m->in_call = false;
}

void maap_timer_expired(struct maap *m)
{
	if (!enter(m)) {
		return;
	}
	if (!m->timer_running) {
		m->stale_expiries++;
	} else if (m->queued != 0u) {
		m->timer_running = false;
		m->expiry_owed = true;
	} else {
		expire(m);
		(void)pump(m);
	}
	m->in_call = false;
}

bool maap_poll(struct maap *m)
{
	if (!enter(m)) {
		return true;
	}
	bool owed = pump(m);
	m->in_call = false;
	return owed;
}
