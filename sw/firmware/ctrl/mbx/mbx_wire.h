// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_wire.h - the mailbox's own byte order, on top of the shared wire layer.
//
// Two orders meet in a ring and neither depends on the host's own:
//
//   * a WIRE field inside a frame is big-endian; ../wire/wire.h reads and
//     writes it one byte at a time;
//   * a RING word carries four frame bytes in little-endian lanes, the
//     contract's statement (sw/mailbox/mailbox.yaml): frame byte k sits in
//     ring word k/4 at bits [8*(k%4)+7 : 8*(k%4)]. ring_lanes_*() convert.
//
// Nothing here copies memory as a wider type, so a big-endian hard core reads
// the same values as the RISC-V does. No compiler intrinsics.

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
