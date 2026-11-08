// SPDX-License-Identifier: MIT
// Compare the reviewed wire_put_be with the byte form for widths 0 to 8,
// edge values and 2^22 pseudo-random values, with guard bytes on both sides.
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "wire.h"

static void old_put_be(uint8_t *p, uint64_t value, unsigned bytes)
{
	for (unsigned i = 0; i < bytes; ++i)
		p[i] = (uint8_t)(value >> (8u * (bytes - 1u - i)));
}

static uint64_t state = 0x9E3779B97F4A7C15ull;
static uint64_t next(void)
{
	state ^= state << 13; state ^= state >> 7; state ^= state << 17;
	return state;
}

int main(void)
{
	static const uint64_t edges[] = {0, ~0ull, 1, 1ull << 63, 0x00000000FFFFFFFFull, 0xFFFFFFFF00000000ull,
		0x0102030405060708ull, 0x8000000080000000ull, 0x7FFFFFFF7FFFFFFFull, 0x00000001FFFFFFFFull};
	unsigned long checks = 0, bad = 0;
	for (unsigned long n = 0; n < (1ul << 22) + sizeof edges / sizeof edges[0]; ++n) {
		uint64_t v = n < sizeof edges / sizeof edges[0] ? edges[n] : next();
		for (unsigned bytes = 0; bytes <= 8; ++bytes) {
			uint8_t a[12], b[12];
			memset(a, 0xA5, sizeof a); memset(b, 0xA5, sizeof b);
			wire_put_be(a + 2, v, bytes);
			old_put_be(b + 2, v, bytes);
			++checks;
			if (memcmp(a, b, sizeof a) != 0) {
				if (bad++ < 5) printf("MISMATCH value=%016llx bytes=%u\n", (unsigned long long)v, bytes);
			}
		}
	}
	printf("checks=%lu mismatches=%lu\n", checks, bad);
	return bad != 0;
}
