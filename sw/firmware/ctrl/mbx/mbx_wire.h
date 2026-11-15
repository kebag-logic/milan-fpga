// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_wire.h - the mailbox's own byte order, on top of the shared wire layer.
//
// Two orders meet in a ring and neither depends on the host's own:
//
//   * a WIRE field inside a frame is big-endian; wire.h, the TSN stack's
//     (third_party/tsn-c-stack/include), reads and writes it byte by byte;
//   * a RING word carries four frame bytes in little-endian lanes, the
//     contract's statement (sw/mailbox/mailbox.yaml): frame byte k sits in
//     ring word k/4 at bits [8*(k%4)+7 : 8*(k%4)]. ring_lanes_*() convert.
//
// Only ring_lanes_store4/load4 access memory as a wider type, and only on a
// little-endian core, where the result is the byte form's; so a big-endian
// hard core reads the same values as the RISC-V does. No compiler intrinsics.

#ifndef MBX_WIRE_H
#define MBX_WIRE_H

#include <stdint.h>

#include "wire.h"

// The ring word holding frame bytes p[0..n-1] (n <= 4) in little-endian
// lanes; lanes past n are zero.
static inline uint32_t ring_lanes_pack(const uint8_t *p, unsigned n)
{
	uint32_t word = 0;
	for (unsigned i = 0; i < n && i < 4u; ++i) {
		word |= (uint32_t)p[i] << (8u * i);
	}
	return word;
}

// Frame bytes p[0..n-1] (n <= 4) out of a ring word's little-endian lanes.
static inline void ring_lanes_unpack(uint32_t word, uint8_t *p, unsigned n)
{
	for (unsigned i = 0; i < n && i < 4u; ++i) {
		p[i] = (uint8_t)(word >> (8u * i));
	}
}

// The ring word holding the four frame bytes p[0..3], and the four bytes out
// of one: the whole-word forms of the two above, which a record's words but
// its last use (#665: a byte loop a word cost the driver tens of thousands of
// cycles a pass).
static inline uint32_t ring_lanes_pack4(const uint8_t *p)
{
	return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

static inline void ring_lanes_unpack4(uint32_t word, uint8_t *p)
{
	p[0] = (uint8_t)word;
	p[1] = (uint8_t)(word >> 8);
	p[2] = (uint8_t)(word >> 16);
	p[3] = (uint8_t)(word >> 24);
}

// On a little-endian core a ring word's lanes are its bytes in memory order,
// so the four frame bytes at a word-aligned p are the word itself. The two
// below are ring_lanes_unpack4 and ring_lanes_pack4 in one 32-bit access
// there (#665: the mailbox window is uncached, and each byte access is a bus
// transaction of 9 CPU cycles), and are those two on any other core.
// p must be word-aligned.
#if defined(__BYTE_ORDER__) && defined(__ORDER_LITTLE_ENDIAN__) && __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
#define RING_LANES_NATIVE 1
#else
#define RING_LANES_NATIVE 0
#endif

static inline void ring_lanes_store4(uint32_t word, uint8_t *p)
{
#if RING_LANES_NATIVE
	*(uint32_t *)(void *)p = word;
#else
	ring_lanes_unpack4(word, p);
#endif
}

static inline uint32_t ring_lanes_load4(const uint8_t *p)
{
#if RING_LANES_NATIVE
	return *(const uint32_t *)(const void *)p;
#else
	return ring_lanes_pack4(p);
#endif
}

// The field [lsb +: width] of a 32-bit register or header word.
static inline uint32_t mbx_field(uint32_t word, uint32_t lsb, uint32_t width)
{
	uint32_t mask = width >= 32u ? 0xFFFFFFFFu : ((1u << width) - 1u);
	return (word >> lsb) & mask;
}

// value placed into the field [lsb +: width] of a 32-bit word.
static inline uint32_t mbx_place(uint32_t value, uint32_t lsb, uint32_t width)
{
	uint32_t mask = width >= 32u ? 0xFFFFFFFFu : ((1u << width) - 1u);
	return (value & mask) << lsb;
}

#endif // MBX_WIRE_H
