// SPDX-License-Identifier: MIT
// Independent reviewer probe for the ADP seeding rule (issue 39, ADP-02).
// Build: cc -std=c11 -O1 -DNDEBUG -I<repo>/include seed_walk.c <repo>/src/adp.c -o seed_walk
// Part 1: random walk over every ADP input on two interfaces; after each input the
//         seed port must have been called once exactly when the machine left DOWN
//         and never otherwise, the generator must never be zero after a draw, and
//         each draw must stay in its Milan v1.2 5.6.3.5.2 / 5.6.3.5.3 range.
// Part 2: first-draw statistics (IEEE 1722.1-2021 6.2.4.2.2 uniform, host-distinct)
//         with parameters different from the suite's: 65,536 consecutive clock
//         samples for one host, 65,536 neighbouring hosts sampled together, and
//         256 interfaces of one host sampled together.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "adp.h"

static uint32_t seed_value;
static unsigned seed_calls;
static bool link_level[2];
static bool send_ok = true;
static uint32_t last_timer_ms;
static unsigned timer_starts;

static bool p_send(void *c, unsigned i, const uint8_t *f, size_t l) { (void)c; (void)i; (void)f; (void)l; return send_ok; }
static void p_start(void *c, unsigned i, uint32_t ms) { (void)c; (void)i; last_timer_ms = ms; timer_starts++; }
static void p_stop(void *c, unsigned i) { (void)c; (void)i; }
static void p_gptp(void *c, unsigned i, uint64_t *gm, uint8_t *d) { (void)c; (void)i; *gm = 1; *d = 0; }
static bool p_link(void *c, unsigned i) { (void)c; return link_level[i & 1u]; }
static uint32_t p_seed(void *c) { (void)c; seed_calls++; return seed_value; }

static const struct adp_ports ports = {NULL, p_send, p_start, p_stop, p_gptp, p_link, p_seed};

static uint64_t lcg = 0x243F6A8885A308D3ull;
static uint32_t rnd(void)
{
	lcg = lcg * 6364136223846793005ull + 1442695040888963407ull;
	return (uint32_t)(lcg >> 33);
}

static unsigned failures;
#define CHECK(c, ...) do { if (!(c)) { failures++; if (failures < 20) { printf("FAIL: " __VA_ARGS__); printf("\n"); } } } while (0)

static void walk(unsigned steps)
{
	static const struct adp_entity e = {0x001B92FFFE0000A1ull, 2u, 0x001B920000A1ull, 0u, 1u, 0u, 1u, 0u, 0u};
	struct adp a[2];
	adp_init(&a[0], &e, &ports, 0, 0);
	adp_init(&a[1], &e, &ports, 1, 0);
	link_level[0] = link_level[1] = false;
	unsigned leaves = 0, samples = 0, inputs[8] = {0};
	for (unsigned s = 0; s < steps; ++s) {
		unsigned k = rnd() & 1u;
		struct adp *p = &a[k];
		enum adp_state before = p->state;
		enum adp_state other_before = a[k ^ 1u].state;
		uint32_t draws = p->draws;
		unsigned calls = seed_calls;
		seed_value = (rnd() & 3u) == 0u ? 7u : rnd();
		send_ok = (rnd() & 7u) != 0u;
		unsigned op = rnd() % 8u;
		inputs[op]++;
		bool from_enable = false;
		switch (op) {
		case 0: from_enable = !p->enabled; adp_set_enable(p, true); break;
		case 1: if ((rnd() & 3u) == 0u) { adp_set_enable(p, false); } break;
		case 2: link_level[k] = true; adp_link_change(p, true); break;
		case 3: link_level[k] = false; adp_link_change(p, false); break;
		case 4: adp_timer_expired(p); break;
		case 5: adp_gm_change(p); break;
		case 6: {
			uint8_t f[ADP_FRAME_BYTES];
			adp_build(p, ADP_MSG_ENTITY_DISCOVER, 0, f);
			if ((rnd() & 1u) != 0u) {
				memset(f + ADP_HEADER_BYTES + 4u, 0, 8);
			}
			adp_rx(p, f, sizeof f);
			break;
		}
		default: (void)adp_poll(p); break;
		}
		bool left = before == ADP_STATE_DOWN && p->state != ADP_STATE_DOWN;
		leaves += left;
		samples += seed_calls - calls;
		CHECK(seed_calls - calls == (left ? 1u : 0u), "step %u op %u: %u samples, left DOWN %d", s, op, seed_calls - calls, left);
		CHECK(a[k ^ 1u].state == other_before, "step %u: the other interface changed", s);
		if (p->draws != draws) {
			CHECK(p->draws == draws + 1u, "step %u: more than one draw", s);
			CHECK(p->rng != 0u, "step %u: generator at zero after a draw", s);
			uint32_t max = p->last_draw == ADP_DRAW_STARTUP ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS;
			CHECK(p->last_draw_ms <= max, "step %u: draw %u over %u", s, p->last_draw_ms, max);
			CHECK(last_timer_ms == p->last_draw_ms, "step %u: timer %u not the draw %u", s, last_timer_ms, p->last_draw_ms);
			CHECK((p->last_draw == ADP_DRAW_STARTUP) == (from_enable && left), "step %u: startup kind %d outside an enable that left DOWN", s, p->last_draw == ADP_DRAW_STARTUP);
		}
	}
	printf("walk: %u steps, %u leaves of DOWN, %u samples, inputs", steps, leaves, samples);
	for (unsigned i = 0; i < 8u; ++i) {
		printf(" %u", inputs[i]);
	}
	printf("\n");
	CHECK(leaves == samples, "samples %u != leaves %u", samples, leaves);
}

static uint32_t first_draw(const struct adp_entity *e, unsigned interface, uint32_t sample, bool startup)
{
	struct adp a;
	link_level[interface & 1u] = startup;
	adp_init(&a, e, &ports, interface, 0);
	seed_value = startup ? sample : 12345u;
	adp_set_enable(&a, true);
	if (!startup) {
		seed_value = sample;
		adp_link_change(&a, true);
	}
	return a.last_draw_ms;
}

// Chi-square over `bins` equal bins of [0, max]; returns statistic and checks it
// against the given 1 % critical value.
static double chi(const uint32_t *v, unsigned n, uint32_t max, unsigned bins)
{
	static unsigned count[256];
	memset(count, 0, sizeof count);
	for (unsigned i = 0; i < n; ++i) {
		unsigned b = (unsigned)(((uint64_t)v[i] * bins) / (max + 1u));
		count[b < bins ? b : bins - 1u]++;
	}
	// Expected counts are those of an ideal uniform 16-bit value through the
	// core's unchanged draw_ms mapping, so unequal bin widths are not counted.
	static unsigned ideal[256];
	memset(ideal, 0, sizeof ideal);
	for (uint32_t r16 = 0; r16 < 65536u; ++r16) {
		uint32_t ms = (r16 * (max + 1u)) >> 16;
		unsigned b = (unsigned)(((uint64_t)ms * bins) / (max + 1u));
		ideal[b < bins ? b : bins - 1u]++;
	}
	double s = 0;
	for (unsigned b = 0; b < bins; ++b) {
		double exp = (double)n * ideal[b] / 65536.0;
		double d = count[b] - exp;
		s += d * d / exp;
	}
	return s;
}

static unsigned distinct(const uint32_t *v, unsigned n)
{
	static unsigned char seen[4001];
	memset(seen, 0, sizeof seen);
	unsigned d = 0;
	for (unsigned i = 0; i < n; ++i) {
		if (!seen[v[i]]) {
			seen[v[i]] = 1;
			d++;
		}
	}
	return d;
}

static void stats(void)
{
	enum { N = 65536 };
	static uint32_t v[N];
	// 1 % critical values: 15 dof 30.58, 63 dof 92.01
	for (int startup = 0; startup <= 1; ++startup) {
		uint32_t max = startup ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS;
		struct adp_entity e = {0x0090E8FFFE3A0001ull, 7u, 0x0090E83A0001ull, 0u, 0u, 1u, 0u, 1u, 0u};
		for (unsigned i = 0; i < N; ++i) {
			v[i] = first_draw(&e, 0, 0x7FFF0000u + i, startup);
		}
		double c16 = chi(v, N, max, 16), c64 = chi(v, N, max, 64);
		printf("one host, %u consecutive samples, %s: chi16 %.2f chi64 %.2f distinct %u\n", N, startup ? "startup" : "link-up", c16, c64, distinct(v, N));
		CHECK(c16 < 30.58 && c64 < 92.01, "consecutive samples not uniform");
		for (unsigned i = 0; i < N; ++i) {
			struct adp_entity h = e;
			h.mac += i;
			h.entity_id += i;
			v[i] = first_draw(&h, 0, 0x7FFF0000u, startup);
		}
		c16 = chi(v, N, max, 16);
		c64 = chi(v, N, max, 64);
		printf("%u neighbouring hosts, one sample, %s: chi16 %.2f chi64 %.2f distinct %u\n", N, startup ? "startup" : "link-up", c16, c64, distinct(v, N));
		CHECK(c16 < 30.58 && c64 < 92.01, "neighbouring hosts not uniform");
		for (unsigned i = 0; i < N; ++i) {
			struct adp_entity h = e;
			h.entity_id += (uint64_t)i << 32;
			v[i] = first_draw(&h, 0, 0x7FFF0000u, startup);
		}
		c16 = chi(v, N, max, 16);
		printf("%u hosts differing only in the entity ID's high word, %s: chi16 %.2f distinct %u\n", N, startup ? "startup" : "link-up", c16, distinct(v, N));
		CHECK(c16 < 30.58, "entity ID high word not uniform");
		for (unsigned i = 0; i < 256u; ++i) {
			v[i] = first_draw(&e, i, 0x7FFF0000u, startup);
		}
		printf("256 interfaces of one host, one sample, %s: distinct %u of 256\n", startup ? "startup" : "link-up", distinct(v, 256));
	}
	// Boots alike but for the sample at a later LINK_UP after a startup draw.
	struct adp_entity e = {0x0090E8FFFE3A0001ull, 7u, 0x0090E83A0001ull, 0u, 0u, 1u, 0u, 1u, 0u};
	for (unsigned i = 0; i < N; ++i) {
		struct adp a;
		link_level[0] = true;
		adp_init(&a, &e, &ports, 0, 0);
		seed_value = 99u;
		adp_set_enable(&a, true);
		adp_link_change(&a, false);
		seed_value = 0x12340000u + i;
		adp_link_change(&a, true);
		v[i] = a.last_draw_ms;
	}
	double c16 = chi(v, N, ADP_DELAY_MAX_MS, 16), c64 = chi(v, N, ADP_DELAY_MAX_MS, 64);
	printf("%u boots alike but for the sample at a later LINK_UP: chi16 %.2f chi64 %.2f distinct %u of 4001\n", N, c16, c64, distinct(v, N));
	CHECK(c16 < 30.58 && c64 < 92.01, "later LINK_UP draws not uniform");
	unsigned d4096 = distinct(v, 4096);
	printf("first 4096 of those: distinct %u (about 2,565 expected)\n", d4096);
}

int main(int argc, char **argv)
{
	unsigned steps = argc > 1 ? (unsigned)strtoul(argv[1], NULL, 10) : 2000000u;
	walk(steps);
	stats();
	printf("%s: %u failures\n", failures ? "PROBE FAILED" : "PROBE PASSED", failures);
	return failures != 0;
}
