// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: MIT
// IEEE 1722.1-2021 Figure 6-1










#ifndef CTRL_WIRE_H
#define CTRL_WIRE_H

#include <stdint.h>


static inline uint16_t wire_be16(const uint8_t *p)
{
	return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]);
}


static inline uint32_t wire_be32(const uint8_t *p)
{
	return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | (uint32_t)p[3];
}


static inline uint64_t wire_be64(const uint8_t *p)
{
	return ((uint64_t)wire_be32(p) << 32) | (uint64_t)wire_be32(p + 4);
}


static inline void wire_put_be(uint8_t *p, uint64_t value, unsigned bytes)
{
	for (unsigned i = 0; i < bytes; ++i) {
		p[i] = (uint8_t)(value >> (8u * (bytes - 1u - i)));
	}
}

#endif
