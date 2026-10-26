// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_mem.c - memcpy, memmove, memset and memcmp for the control core
// (#665; NFR-SCOUT-01/03, FR_NFR.md 3.4.1).
//
// The core is a cacheless RV32I hart and fetch-bound: every instruction
// costs about ten CPU cycles from block RAM, so a byte loop costs about fifty
// cycles a byte, and the AECP responses alone moved several kilobytes a
// pass. These move one 32-bit word per access, four words a turn, once the
// destination is aligned:
//   * memset fills the aligned middle with words;
//   * memcpy, and memmove when the destination does not overlap the source
//     from above, copy words when the source shares the destination's
//     alignment, and otherwise build each destination word from two aligned
//     source words (the merge);
//   * memmove when the destination overlaps the source from above copies
//     from the top down, in words when the two share their alignment and
//     otherwise by the same merge from the top (an insertion into a packed
//     list moves its tail up by an element of any length);
//   * memcmp compares a word at a time while the two share their alignment,
//     and returns the difference of the first differing bytes, as the
//     runtime's byte loop did (lwSRP compares attribute values with it).
// No access is misaligned, and none reads or writes outside [dst, dst + n)
// or [src, src + n): the merge composes its first word from bytes, and stops
// while the next aligned source word would run past the source.
//
// The merge puts the byte at the lower address in the lower bits of a word,
// which is a little-endian core's order (RV32I's); a big-endian core needs
// its own merge, so it does not build this one. The image links these ahead
// of the runtime archive's byte loops, and every turn is a plain loop the
// compiler cannot turn back into a call (the image builder refuses an object
// of this file that references any symbol).

#include <stddef.h>
#include <stdint.h>

#if defined(__BYTE_ORDER__) && defined(__ORDER_LITTLE_ENDIAN__) && __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
#error "ctrl_mem.c merges words in little-endian lane order"
#endif

void *memcpy(void *restrict dst, const void *restrict src, size_t n);
void *memmove(void *dst, const void *src, size_t n);
void *memset(void *dst, int c, size_t n);
int memcmp(const void *a, const void *b, size_t n);

#define WORD_BYTES 4u
#define WORD_MASK (WORD_BYTES - 1u)

static uint32_t load(const unsigned char *p)
{
	return *(const uint32_t *)(const void *)p;
}

static void store(unsigned char *p, uint32_t w)
{
	*(uint32_t *)(void *)p = w;
}

static unsigned misalignment(const void *p)
{
	return (unsigned)((uintptr_t)p & WORD_MASK);
}

// Copy n bytes upwards, lowest address first; dst may overlap src from below.
// Returns dst, so the public functions end in a tail call.
static void *forward(void *dst, const void *src, size_t n)
{
	unsigned char *d = dst;
	const unsigned char *s = src;
	while (n != 0u && misalignment(d) != 0u) {
		*d++ = *s++;
		--n;
	}
	unsigned off = misalignment(s);
	if (off == 0u) {
		for (; n >= 4u * WORD_BYTES; n -= 4u * WORD_BYTES, d += 4u * WORD_BYTES, s += 4u * WORD_BYTES) {
			uint32_t w0 = load(s), w1 = load(s + 4), w2 = load(s + 8), w3 = load(s + 12);
			store(d, w0);
			store(d + 4, w1);
			store(d + 8, w2);
			store(d + 12, w3);
		}
		for (; n >= WORD_BYTES; n -= WORD_BYTES, d += WORD_BYTES, s += WORD_BYTES) {
			store(d, load(s));
		}
	} else if (n >= 2u * WORD_BYTES - off) {
		// The merge. prev holds the aligned source word below the next
		// output word, with s[0..] in its top lanes (composed from bytes);
		// an output word is prev's top lanes over the next word's bottom
		// ones. Turn k reads the whole aligned word at s - off + 4 (k + 1),
		// which ends at s + 4k + 7 - off, so the turns stop while that is
		// still at most s + n - 1.
		unsigned lo = 8u * off, hi = 32u - lo;
		uint32_t prev = 0;
		for (unsigned k = off; k < WORD_BYTES; ++k) {
			prev |= (uint32_t)s[k - off] << (8u * k);
		}
		size_t turns = (n - (2u * WORD_BYTES - off)) / WORD_BYTES + 1u;
		const unsigned char *next = s - off + WORD_BYTES;
		n -= turns * WORD_BYTES;
		s += turns * WORD_BYTES;
		for (; turns >= 2u; turns -= 2u, next += 2u * WORD_BYTES, d += 2u * WORD_BYTES) {
			uint32_t w0 = load(next), w1 = load(next + 4);
			store(d, (prev >> lo) | (w0 << hi));
			store(d + 4, (w0 >> lo) | (w1 << hi));
			prev = w1;
		}
		if (turns != 0u) {
			store(d, (prev >> lo) | (load(next) << hi));
			d += WORD_BYTES;
		}
	}
	while (n != 0u) {
		*d++ = *s++;
		--n;
	}
	return dst;
}

// Copy n bytes downwards, highest address first; dst may overlap src from above.
static void *backward(void *dst, const void *src, size_t n)
{
	unsigned char *d = (unsigned char *)dst + n;
	const unsigned char *s = (const unsigned char *)src + n;
	while (n != 0u && misalignment(d) != 0u) {
		*--d = *--s;
		--n;
	}
	unsigned off = misalignment(s);
	if (off == 0u) {
		for (; n >= WORD_BYTES; n -= WORD_BYTES) {
			d -= WORD_BYTES;
			s -= WORD_BYTES;
			store(d, load(s));
		}
	} else if (n >= WORD_BYTES + off) {
		// The merge, from the top. prev holds s[-off..0) in its bottom lanes
		// (composed from bytes); an output word is the next lower aligned
		// word's top lanes under prev's bottom ones. Turn k reads the whole
		// aligned word at s - off - 4 (k + 1), so the turns stop while that
		// still starts at or above s - n. A write never reaches a word still
		// to be read: dst - src is 4m - off for some m >= 1, which puts each
		// written word at or above the end of the next one read.
		unsigned lo = 8u * off, hi = 32u - lo;
		const unsigned char *next = s - off;
		uint32_t prev = 0;
		for (unsigned k = 0; k < off; ++k) {
			prev |= (uint32_t)next[k] << (8u * k);
		}
		size_t turns = (n - off) / WORD_BYTES;
		n -= turns * WORD_BYTES;
		s -= turns * WORD_BYTES;
		for (; turns != 0u; --turns) {
			next -= WORD_BYTES;
			d -= WORD_BYTES;
			uint32_t w = load(next);
			store(d, (w >> lo) | (prev << hi));
			prev = w;
		}
	}
	while (n != 0u) {
		*--d = *--s;
		--n;
	}
	return dst;
}

void *memcpy(void *restrict dst, const void *restrict src, size_t n)
{
	return forward(dst, src, n);
}

void *memmove(void *dst, const void *src, size_t n)
{
	// Upwards is safe unless dst lies inside (src, src + n).
	if ((uintptr_t)dst - (uintptr_t)src >= n) {
		return forward(dst, src, n);
	}
	return backward(dst, src, n);
}

void *memset(void *dst, int c, size_t n)
{
	unsigned char *d = dst;
	unsigned char byte = (unsigned char)c;
	uint32_t fill = byte;
	fill |= fill << 8;
	fill |= fill << 16;
	while (n != 0u && misalignment(d) != 0u) {
		*d++ = byte;
		--n;
	}
	for (; n >= 4u * WORD_BYTES; n -= 4u * WORD_BYTES, d += 4u * WORD_BYTES) {
		store(d, fill);
		store(d + 4, fill);
		store(d + 8, fill);
		store(d + 12, fill);
	}
	for (; n >= WORD_BYTES; n -= WORD_BYTES, d += WORD_BYTES) {
		store(d, fill);
	}
	while (n != 0u) {
		*d++ = byte;
		--n;
	}
	return dst;
}

int memcmp(const void *a, const void *b, size_t n)
{
	const unsigned char *x = a;
	const unsigned char *y = b;
	if (misalignment(x) == misalignment(y)) {
		while (n != 0u && misalignment(x) != 0u && *x == *y) {
			++x;
			++y;
			--n;
		}
		while (n >= WORD_BYTES && misalignment(x) == 0u && load(x) == load(y)) {
			x += WORD_BYTES;
			y += WORD_BYTES;
			n -= WORD_BYTES;
		}
	}
	for (; n != 0u; --n, ++x, ++y) {
		if (*x != *y) {
			return *x - *y;
		}
	}
	return 0;
}
