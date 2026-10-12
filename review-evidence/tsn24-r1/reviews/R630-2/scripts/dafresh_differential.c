// SPDX-License-Identifier: MIT
// Randomized differential check of acmp_declaring against an independent model of
// issue 24 acceptance 1-2: valid destination AND (accepted PROBE_TX answer younger
// than da_fresh_ms OR registered Listener), per source, with transport backpressure,
// owed-queue limits, interface mismatch, unknown IDs, Listener toggles and clock wrap.
// build: cc -std=c11 -I<tree>/include <tree>/src/acmp.c dafresh_differential.c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "acmp.h"
#include "wire.h"

#define NSRC 3u
#define OWN UINT64_C(0x020000fffe000001)

static uint32_t clock_now, send_delay;
static int accept_send;
static int da[NSRC];
static uint32_t rng_state;

static uint32_t rnd(void)
{
	rng_state ^= rng_state << 13;
	rng_state ^= rng_state >> 17;
	rng_state ^= rng_state << 5;
	return rng_state;
}

static bool p_send(void *c, unsigned i, const uint8_t *f, size_t n)
{
	(void)c; (void)i; (void)f; (void)n;
	if (!accept_send) return false;
	clock_now += send_delay;
	return true;
}
static uint32_t p_now(void *c) { (void)c; return clock_now; }
static void p_timer(void *c, unsigned i, bool a, uint32_t d) { (void)c; (void)i; (void)a; (void)d; }
static void p_gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static uint32_t p_seed(void *c) { (void)c; return 7; }
static void p_admit(void *c, unsigned i, unsigned s, bool b, uint64_t t) { (void)c; (void)i; (void)s; (void)b; (void)t; }
static void p_publish(void *c, unsigned i, unsigned s, bool b, bool st, uint64_t id, bool m)
{ (void)c; (void)i; (void)s; (void)b; (void)st; (void)id; (void)m; }
static bool e_locked(void *c, uint64_t *x) { (void)c; *x = 0; return false; }
static void e_source(void *c, unsigned idx, struct acmp_source_state *o)
{
	(void)c;
	memset(o, 0, sizeof *o);
	o->dest_mac_valid = idx < NSRC && da[idx];
}
static void e_srp(void *c, unsigned s, const struct acmp_stream *x) { (void)c; (void)s; (void)x; }
static void e_note(void *c, unsigned s) { (void)c; (void)s; }

static const struct acmp_ports ports = {0, p_send, p_now, p_timer, p_gptp, p_seed, p_admit, p_publish};
static const struct acmp_env env = {0, e_locked, e_source, e_srp, e_note, e_note};

static int queue[ACMP_OWED_MAX];
static unsigned qhead, qlen;
static int pinged[NSRC], lst[NSRC];
static uint32_t ts[NSRC];
static const unsigned iface[NSRC] = {0u, 1u, 0u};

static void model_sent(int tag)
{
	if (tag >= 0) {
		ts[tag] = clock_now + send_delay;
		pinged[tag] = 1;
	}
}

static void command(struct acmp *a, uint8_t msg, unsigned uid, unsigned interface)
{
	uint8_t f[ACMP_FRAME_BYTES] = {0};
	wire_put_be(f + 12, 0x22f0, 2);
	f[14] = 0xfc;
	f[15] = msg;
	wire_put_be(f + 16, 44, 2);
	wire_put_be(f + 34, OWN, 8);
	wire_put_be(f + 50, uid, 2);
	if (qlen < ACMP_OWED_MAX) {
		int tag = (msg == 0u && uid < NSRC && interface == iface[uid]) ? (int)uid : -1;
		if (qlen == 0u && accept_send) {
			model_sent(tag);
		} else {
			queue[(qhead + qlen) % ACMP_OWED_MAX] = tag;
			qlen++;
		}
	}
	acmp_rx(a, interface, f, sizeof f);
}

int main(int argc, char **argv)
{
	unsigned long seeds = argc > 1 ? strtoul(argv[1], 0, 10) : 200ul;
	unsigned long steps = argc > 2 ? strtoul(argv[2], 0, 10) : 20000ul;
	unsigned long queries = 0, trues = 0, edges = 0;
	for (unsigned long seed = 1; seed <= seeds; ++seed) {
		rng_state = (uint32_t)(seed * 2654435761u) | 1u;
		struct acmp_config cfg;
		memset(&cfg, 0, sizeof cfg);
		cfg.da_fresh_ms = 15000u;
		cfg.entity_id = OWN;
		cfg.n_interfaces = 2u;
		cfg.mac[0] = 0x020000000001u;
		cfg.mac[1] = 0x020000000002u;
		cfg.n_sources = NSRC;
		for (unsigned s = 0; s < NSRC; ++s) cfg.source_interface[s] = (uint8_t)iface[s];
		struct acmp a;
		if (!acmp_init(&a, &cfg, &ports, &env)) return 2;
		clock_now = (seed & 1u) ? UINT32_MAX - (rnd() % 200000u) : rnd();
		qhead = qlen = 0;
		for (unsigned s = 0; s < NSRC; ++s) { pinged[s] = lst[s] = 0; da[s] = (int)(rnd() & 1u); }
		accept_send = 1;
		for (unsigned long k = 0; k < steps; ++k) {
			send_delay = rnd() % 3u;
			switch (rnd() % 9u) {
			case 0: case 1: command(&a, 0u, rnd() % (NSRC + 1u), rnd() % 2u); break;
			case 2: command(&a, 4u, rnd() % NSRC, rnd() % 2u); break;
			case 3: accept_send = (rnd() % 4u) != 0u; break;
			case 4:
				if (qlen) {
					int tag = queue[qhead];
					bool ok = accept_send;
					if (ok) { model_sent(tag); qhead = (qhead + 1u) % ACMP_OWED_MAX; qlen--; }
				}
				(void)acmp_poll(&a);
				break;
			case 5: {
				unsigned s = rnd() % (NSRC + 1u), i = rnd() % 2u;
				bool level = rnd() & 1u;
				bool want = s < NSRC && i == iface[s];
				if (want) lst[s] = level;
				if (acmp_listener_registered(&a, i, s, level) != want) {
					printf("listener return mismatch seed %lu step %lu\n", seed, k);
					return 1;
				}
				break;
			}
			case 6: da[rnd() % NSRC] ^= 1; break;
			case 7: {
				static const uint32_t pick[] = {1u, 14999u, 15000u, 15001u, 7500u};
				clock_now += pick[rnd() % 5u];
				break;
			}
			default: clock_now += rnd() % 16000u; break;
			}
			if (a.owed_count != qlen) {
				printf("queue model mismatch seed %lu step %lu core %u model %u\n", seed, k, a.owed_count, qlen);
				return 1;
			}
			for (unsigned s = 0; s <= NSRC; ++s) {
				int want = 0;
				if (s < NSRC) {
					if (pinged[s] && (uint32_t)(clock_now - ts[s]) >= 15000u) pinged[s] = 0;
					if (pinged[s] && (uint32_t)(clock_now - ts[s]) == 14999u) edges++;
					want = da[s] && (pinged[s] || lst[s]);
				}
				int got = acmp_declaring(&a, s);
				queries++;
				trues += (unsigned long)got;
				if (got != want) {
					printf("MISMATCH seed %lu step %lu source %u core %d model %d now %u ts %u\n",
					       seed, k, s, got, want, clock_now, s < NSRC ? ts[s] : 0u);
					return 1;
				}
			}
		}
	}
	printf("PASS seeds=%lu steps=%lu queries=%lu true=%lu last-ms-fresh=%lu\n", seeds, steps, queries, trues, edges);
	return 0;
}
