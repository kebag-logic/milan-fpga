// SPDX-License-Identifier: MIT
// Wrap-alias scenarios for the PORTING claim "Observing expiry clears answered,
// even with a Listener or an invalid destination, so an old probe cannot
// reappear after a later counter wrap". The service queries every 1e9 ms,
// inside the documented less-than-half-counter-range contract.
// build: cc -std=c11 -I<tree>/include <tree>/src/acmp.c wrap_alias_demo.c
// Exit 0 when both scenarios match the claim, 1 otherwise.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "acmp.h"
#include "wire.h"

#define OWN UINT64_C(0x020000fffe000001)

static uint32_t clock_now;
static bool da_valid = true;

static bool send(void *c, unsigned i, const uint8_t *f, size_t l) { (void)c; (void)i; (void)f; (void)l; return true; }
static uint32_t now_ms(void *c) { (void)c; return clock_now; }
static void timer(void *c, unsigned i, bool a, uint32_t d) { (void)c; (void)i; (void)a; (void)d; }
static void gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static uint32_t seed(void *c) { (void)c; return 1; }
static void admit(void *c, unsigned i, unsigned s, bool b, uint64_t t) { (void)c; (void)i; (void)s; (void)b; (void)t; }
static void publish(void *c, unsigned i, unsigned s, bool b, bool st, uint64_t id, bool m)
{ (void)c; (void)i; (void)s; (void)b; (void)st; (void)id; (void)m; }
static bool locked(void *c, uint64_t *e) { (void)c; (void)e; return false; }
static void source(void *c, unsigned i, struct acmp_source_state *o)
{ (void)c; (void)i; memset(o, 0, sizeof *o); o->dest_mac_valid = da_valid; o->stream.dest_mac = 0x91e0f0000001u; }
static void srp(void *c, unsigned s, const struct acmp_stream *st) { (void)c; (void)s; (void)st; }
static void note(void *c, unsigned s) { (void)c; (void)s; }

static const struct acmp_ports ports = {0, send, now_ms, timer, gptp, seed, admit, publish};
static const struct acmp_env env = {0, locked, source, srp, note, note};

static void probe(struct acmp *a)
{
	uint8_t f[ACMP_FRAME_BYTES] = {0};
	wire_put_be(f + 12, 0x22f0, 2);
	f[14] = 0xfc;
	wire_put_be(f + 16, 44, 2);
	wire_put_be(f + 34, OWN, 8);
	acmp_rx(a, 0, f, sizeof f);
}

static void init(struct acmp *a)
{
	struct acmp_config cfg;
	memset(&cfg, 0, sizeof cfg);
	cfg.da_fresh_ms = 15000u;
	cfg.entity_id = OWN;
	cfg.n_interfaces = 1;
	cfg.mac[0] = 0x020000000001u;
	cfg.n_sources = 1;
	(void)acmp_init(a, &cfg, &ports, &env);
}

// Service queries every 1e9 ms until 2^32 + 100 ms after the answer.
static void hold(struct acmp *a, uint32_t start)
{
	uint64_t t;
	for (t = 1000000000u; t < UINT64_C(0x100000000); t += 1000000000u) {
		clock_now = start + (uint32_t)t;
		(void)acmp_declaring(a, 0);
	}
	clock_now = start + 100u;  // 2^32 + 100 ms after the answer
}

int main(void)
{
	struct acmp a;
	int bad = 0;

	init(&a);
	da_valid = true;
	clock_now = 50000u;
	probe(&a);
	(void)acmp_listener_registered(&a, 0, 0, true);
	hold(&a, 50000u);
	(void)acmp_listener_registered(&a, 0, 0, false);
	bool listener_case = acmp_declaring(&a, 0);
	printf("listener-held 2^32+100 ms then withdrawn: declaring=%d (claim: 0)\n", listener_case);
	bad |= listener_case;

	init(&a);
	da_valid = true;
	clock_now = 50000u;
	probe(&a);
	da_valid = false;
	hold(&a, 50000u);
	da_valid = true;
	bool da_case = acmp_declaring(&a, 0);
	printf("destination invalid 2^32+100 ms then valid: declaring=%d (claim: 0)\n", da_case);
	bad |= da_case;
	return bad;
}
