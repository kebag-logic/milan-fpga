/* Host benchmark (#32): CPU cycles (x86 TSC) per ACMP entry whose work is its completion, the finish() walk, at a
 * given sink count: acmp_set_started toggling one bound sink's started flag (one publish, persist and change report),
 * and acmp_set_started leaving it as it is (no call), both through the real core with no-op ports.
 * Built against a core's src/acmp.c at ACMP_MAX_SINKS=32u. usage: bench SINKS ROUNDS */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>
#include "acmp.h"

void ctrl_reentry_assert(const char *m) { (void)m; }
static bool p_send(void *c, unsigned i, const uint8_t *f, size_t l) { (void)c; (void)i; (void)f; (void)l; return true; }
static uint32_t p_now(void *c) { (void)c; return 50000u; }
static void p_timer(void *c, unsigned i, bool a, uint32_t d) { (void)c; (void)i; (void)a; (void)d; }
static void p_gptp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 1; *d = 0; }
static uint32_t p_seed(void *c) { (void)c; return 7u; }
static void p_admit(void *c, unsigned i, unsigned s, bool b, uint64_t t) { (void)c; (void)i; (void)s; (void)b; (void)t; }
static void p_publish(void *c, unsigned i, unsigned s, bool b, bool st, uint64_t x, bool m)
{ (void)c; (void)i; (void)s; (void)b; (void)st; (void)x; (void)m; }
static bool e_locked(void *c, uint64_t *h) { (void)c; *h = 0; return false; }
static void e_source(void *c, unsigned i, struct acmp_source_state *o) { (void)c; (void)i; memset(o, 0, sizeof *o); }
static void e_srp(void *c, unsigned s, const struct acmp_stream *x) { (void)c; (void)s; (void)x; }
static void e_persist(void *c, unsigned s) { (void)c; (void)s; }
static void e_changed(void *c, unsigned s) { (void)c; (void)s; }
static const struct acmp_ports ports = {NULL, p_send, p_now, p_timer, p_gptp, p_seed, p_admit, p_publish};
static const struct acmp_env env = {NULL, e_locked, e_source, e_srp, e_persist, e_changed};

static int cmp(const void *x, const void *y) { uint64_t a = *(const uint64_t *)x, b = *(const uint64_t *)y; return a < b ? -1 : a > b; }

int main(int argc, char **argv)
{
	unsigned sinks = (unsigned)atoi(argv[1]), rounds = (unsigned)atoi(argv[2]);
	static struct acmp a;
	struct acmp_config cfg = {0};
	cfg.entity_id = 0x0A0B0C0D0E0F1011ull; cfg.n_interfaces = 2; cfg.mac[0] = 1; cfg.mac[1] = 2;
	cfg.n_sinks = sinks; cfg.n_sources = 0;
	for (unsigned k = 0; k < sinks; ++k) cfg.sink_interface[k] = (uint8_t)(k % 2u);
	if (!acmp_init(&a, &cfg, &ports, &env)) return 2;
	uint8_t rec[ACMP_BINDING_BYTES] = {0};
	rec[0] = 1u | 2u; rec[3] = 1; rec[11] = 0x55;
	for (unsigned k = 0; k < sinks; ++k) (void)acmp_restore_binding(&a, k, rec, ACMP_BINDING_BYTES);
	acmp_open(&a);
	uint64_t *t = malloc(sizeof *t * rounds), *u = malloc(sizeof *u * rounds);
	for (unsigned n = 0; n < rounds; ++n) {
		unsigned k = n % sinks;
		uint64_t s = __rdtsc();
		(void)acmp_set_started(&a, k, (n / sinks) % 2u == 0u);
		t[n] = __rdtsc() - s;
		s = __rdtsc();
		(void)acmp_set_started(&a, k, (n / sinks) % 2u == 0u);
		u[n] = __rdtsc() - s;
	}
	qsort(t, rounds, sizeof *t, cmp); qsort(u, rounds, sizeof *u, cmp);
	printf("sinks %u: a changing entry median %llu min %llu TSC cycles; an unchanged entry median %llu min %llu\n",
	       sinks, (unsigned long long)t[rounds / 2], (unsigned long long)t[0], (unsigned long long)u[rounds / 2],
	       (unsigned long long)u[0]);
	return 0;
}
