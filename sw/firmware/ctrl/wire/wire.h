// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// wire.h - the fixed-width, byte-order-explicit wire layer every protocol
// module shares (#665 lane F0).
//
// A wire field (an ADPDU's entity_id, an EtherType, an MRPDU's VectorHeader)
// is big-endian, the network order IEEE 1722.1-2021 Figure 6-1 and IEEE
// 802.1Q-2018 10.8 draw. These helpers read and write one byte at a time, so
// no value ever passes through a wider type in memory and the result does not
// depend on the host's own byte order or alignment rules. No compiler
// intrinsics.

#ifndef CTRL_WIRE_H
#define CTRL_WIRE_H

#include <stdint.h>

// A big-endian 16-bit wire field.
static inline uint16_t wire_be16(const uint8_t *p)
{
	return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]);
}

// A big-endian 32-bit wire field.
static inline uint32_t wire_be32(const uint8_t *p)
{
	return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | (uint32_t)p[3];
}

// A big-endian 64-bit wire field.
static inline uint64_t wire_be64(const uint8_t *p)
{
	return ((uint64_t)wire_be32(p) << 32) | (uint64_t)wire_be32(p + 4);
}

// Write a big-endian field of `bytes` bytes (1 to 8).
static inline void wire_put_be(uint8_t *p, uint64_t value, unsigned bytes)
{
	for (unsigned i = 0; i < bytes; ++i) {
		p[i] = (uint8_t)(value >> (8u * (bytes - 1u - i)));
	}
}

#endif // CTRL_WIRE_H
