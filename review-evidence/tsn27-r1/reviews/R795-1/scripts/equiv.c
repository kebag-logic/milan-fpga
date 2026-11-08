// SPDX-License-Identifier: MIT
// Reviewer harness: wire_put_be (included head header) against the pre-change byte form,
// every width 0..8, guard bytes on both sides, special and pseudo-random values.
#include <stdint.h>
#include "wire.h"
static void ref_put_be(uint8_t *p, uint64_t value, unsigned bytes)
{
	for (unsigned i = 0; i < bytes; ++i)
		p[i] = (uint8_t)(value >> (8u * (bytes - 1u - i)));
}
static uint64_t state = UINT64_C(0x9E3779B97F4A7C15);
static uint64_t next(void)
{
	uint64_t z = (state += UINT64_C(0x9E3779B97F4A7C15));
	z = (z ^ (z >> 30)) * UINT64_C(0xBF58476D1CE4E5B9);
	z = (z ^ (z >> 27)) * UINT64_C(0x94D049BB133111EB);
	return z ^ (z >> 31);
}
static unsigned check(uint64_t v)
{
	for (unsigned bytes = 0; bytes <= 8; ++bytes) {
		for (unsigned off = 0; off < 4; ++off) {
			volatile uint8_t got[16], want[16];
			uint8_t g[16], w[16];
			for (unsigned i = 0; i < 16; ++i) g[i] = w[i] = (uint8_t)(0xA5u ^ i);
			wire_put_be(g + 4 + off, v, bytes);
			ref_put_be(w + 4 + off, v, bytes);
			for (unsigned i = 0; i < 16; ++i) { got[i] = g[i]; want[i] = w[i]; }
			for (unsigned i = 0; i < 16; ++i) if (got[i] != want[i]) return 1u + bytes;
		}
	}
	return 0;
}
unsigned run_equiv(unsigned rounds)
{
	static const uint64_t special[] = {0, ~UINT64_C(0), UINT64_C(0x00000000FFFFFFFF), UINT64_C(0xFFFFFFFF00000000),
		UINT64_C(0x0102030405060708), UINT64_C(0x8899AABBCCDDEEFF), UINT64_C(0x8000000000000000), 1,
		UINT64_C(0x80000000), UINT64_C(0x7FFFFFFF), UINT64_C(0x100000000), UINT64_C(0x00FF00FF00FF00FF)};
	for (unsigned i = 0; i < sizeof special / sizeof special[0]; ++i) { unsigned r = check(special[i]); if (r) return r; }
	for (unsigned k = 0; k < 64; ++k) { unsigned r = check(UINT64_C(1) << k); if (r) return r; r = check(~(UINT64_C(1) << k)); if (r) return r; }
	for (unsigned n = 0; n < rounds; ++n) { unsigned r = check(next()); if (r) return r; }
	return 0;
}
#ifdef HOSTED
#include <stdio.h>
int main(void) { unsigned r = run_equiv(2000000u); printf("equiv rc %u\n", r); return (int)r; }
#else
int main(void) { return (int)run_equiv(20000u); }
#endif
