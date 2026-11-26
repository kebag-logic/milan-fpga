/* Re-derives the A22 constant: every 32-bit clock sample whose seed mixes to
 * zero for the A22 fixture (rng 0, interface 0, the test entity), under the
 * plain modulo-2^32 sum and under the earlier end-around-carry sum, and then
 * checks the chosen sample against the real core linked from src/adp.c. */
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include "adp.h"
static uint32_t mix(uint32_t x)
{
	x = ~x + (x << 15); x ^= x >> 12; x += x << 2; x ^= x >> 4;
	x += (x << 3) + (x << 11); return x ^ (x >> 16);
}
static const uint64_t MAC = 0x001B921122AAull, EID = 0x1122334455667788ull;
static uint32_t sample_v;
static bool snd(void *c, unsigned i, const uint8_t *f, size_t l) { (void)c; (void)i; (void)f; (void)l; return true; }
static void tst(void *c, unsigned i, uint32_t d) { (void)c; (void)i; (void)d; }
static void tsp(void *c, unsigned i) { (void)c; (void)i; }
static void gp(void *c, unsigned i, uint64_t *g, uint8_t *d) { (void)c; (void)i; *g = 0; *d = 0; }
static bool lk(void *c, unsigned i) { (void)c; (void)i; return true; }
static uint32_t sd(void *c) { (void)c; return sample_v; }
int main(void)
{
	uint32_t id = (uint32_t)EID ^ (uint32_t)(EID >> 32);
	unsigned n_mod = 0, n_eac = 0; uint32_t s_mod = 0, s_eac = 0;
	uint32_t s = 0;
	do {
		uint32_t sum = (uint32_t)MAC + s;
		if (mix(mix(sum) ^ id) == 0u) { n_mod++; s_mod = s; }
		uint32_t eac = sum + (sum < s);
		if (mix(mix(eac) ^ id) == 0u) { n_eac++; s_eac = s; }
	} while (++s != 0u);
	printf("modular: %u sample(s) mix to zero, sample 0x%08X\n", n_mod, s_mod);
	printf("end-around: %u sample(s) mix to zero, sample 0x%08X\n", n_eac, s_eac);
	printf("mac low32 0x%08X + 0x%08X carries out of bit 31: %s\n", (uint32_t)MAC, s_mod,
	       ((uint64_t)(uint32_t)MAC + s_mod) >> 32 ? "yes" : "no");
	struct adp_entity e = {0}; e.entity_id = EID; e.mac = MAC;
	struct adp_ports p = {NULL, snd, tst, tsp, gp, lk, sd};
	const uint32_t probes[] = {0xDE81995Du, 0xDE81995Cu};
	for (unsigned k = 0; k < 2; ++k) {
		struct adp a; adp_init(&a, &e, &p, 0, 0); sample_v = probes[k];
		adp_set_enable(&a, true);
		printf("core: sample 0x%08X -> rng after first draw 0x%08X (state %d, draws %u)\n",
		       probes[k], a.rng, (int)a.state, a.draws);
	}
	uint32_t x = 1u; x ^= x << 13; x ^= x >> 17; x ^= x << 5;
	printf("xorshift32(1) = 0x%08X\n", x);
	return 0;
}
