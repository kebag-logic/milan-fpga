/* SPDX-License-Identifier: 0BSD */
/*
 * xz_config.h — bare-metal configuration for the vendored xz_embedded
 * decoder (lib/xz from linux-7.0.11, 0BSD/public domain) running inside
 * the LiteX BIOS (Milan flashboot kernel decompression).
 *
 * Single-call mode only (XZ_DEC_SINGLE): the output buffer doubles as the
 * LZMA2 dictionary, so no dictionary allocation is needed. xz_dec_init()
 * still kmalloc()s its state (~40 KB with the LZMA2 probability arrays) —
 * served here by a trivial bump allocator over a DRAM arena provided by
 * boot.c (DRAM is initialised before flashboot runs).
 */
#ifndef XZ_CONFIG_H
#define XZ_CONFIG_H

#define XZ_DEC_SINGLE
/* no XZ_DEC_PREALLOC / XZ_DEC_DYNALLOC — single-call only */
/* no BCJ filters: plain `xz --check=crc32 --lzma2` streams only */

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#include "xz.h"

/* bump allocator over a DRAM arena (set up by milan_xz_set_arena()) */
void *milan_xz_alloc(size_t size);
void milan_xz_set_arena(void *base, size_t size);

#define kmalloc(size, flags) milan_xz_alloc(size)
#define kmalloc_obj(obj)     milan_xz_alloc(sizeof(obj))
#define kfree(ptr)           ((void)(ptr))
#define vmalloc(size)        milan_xz_alloc(size)
#define vfree(ptr)           ((void)(ptr))

#define memeq(a, b, size)    (memcmp(a, b, size) == 0)
#define memzero(buf, size)   memset(buf, 0, size)

#ifndef min
#define min(x, y) ((x) < (y) ? (x) : (y))
#endif
#define min_t(type, x, y) min((type)(x), (type)(y))

/* static inline markers used by the kernel sources */
#ifndef __always_inline
#define __always_inline inline
#endif
#ifndef fallthrough
#define fallthrough do {} while (0)
#endif

/* unaligned helpers (RISC-V RV64GC handles unaligned loads; keep safe) */
#define get_le32(p) get_unaligned_le32((const uint8_t *)(p))

static inline uint32_t get_unaligned_le32(const uint8_t *buf)
{
	return (uint32_t)buf[0] | ((uint32_t)buf[1] << 8)
	     | ((uint32_t)buf[2] << 16) | ((uint32_t)buf[3] << 24);
}
static inline uint32_t get_unaligned_be32(const uint8_t *buf)
{
	return ((uint32_t)buf[0] << 24) | ((uint32_t)buf[1] << 16)
	     | ((uint32_t)buf[2] << 8) | (uint32_t)buf[3];
}
static inline void put_unaligned_le32(uint32_t val, uint8_t *buf)
{
	buf[0] = (uint8_t)val; buf[1] = (uint8_t)(val >> 8);
	buf[2] = (uint8_t)(val >> 16); buf[3] = (uint8_t)(val >> 24);
}
static inline void put_unaligned_be32(uint32_t val, uint8_t *buf)
{
	buf[0] = (uint8_t)(val >> 24); buf[1] = (uint8_t)(val >> 16);
	buf[2] = (uint8_t)(val >> 8); buf[3] = (uint8_t)val;
}

#endif
