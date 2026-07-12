// SPDX-License-Identifier: 0BSD
/*
 * milan_xz.c — flashboot kernel decompression for the LiteX BIOS.
 *
 * The kernel is flashed as the kernel build's own `Image.xz` artifact
 * (bootloader-decompressed by design; stream must be plain LZMA2 with
 * --check=crc32 or --check=none — deploy.sh enforces the flags). The BIOS
 * stages the FBI payload in DRAM, sniffs the xz magic, and either
 * decompresses (single-call xz_embedded: the destination buffer IS the
 * dictionary) or falls back to a plain copy for uncompressed images —
 * both flash layouts keep working during the transition.
 */
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include "xz.h"

/* the BIOS libc omits memcmp — the xz decoder needs it (magic + check) */
int memcmp(const void *a, const void *b, size_t n)
{
	const unsigned char *pa = a, *pb = b;
	while (n--) { if (*pa != *pb) return (int)*pa - (int)*pb; pa++; pb++; }
	return 0;
}

static uint8_t *arena_base;
static size_t   arena_size, arena_used;

void milan_xz_set_arena(void *base, size_t size)
{
	arena_base = base; arena_size = size; arena_used = 0;
}

void *milan_xz_alloc(size_t size)
{
	size = (size + 15) & ~(size_t)15;
	if (arena_used + size > arena_size)
		return NULL;
	void *p = arena_base + arena_used;
	arena_used += size;
	return p;
}

int milan_is_xz(const uint8_t *buf)
{
	static const uint8_t magic[6] = { 0xFD, '7', 'z', 'X', 'Z', 0x00 };
	return memcmp(buf, magic, sizeof(magic)) == 0;
}

/* returns decompressed length, or 0 on error */
unsigned long milan_unxz(const uint8_t *src, unsigned long src_len,
                         uint8_t *dst, unsigned long dst_max)
{
	struct xz_buf b;
	struct xz_dec *s;
	enum xz_ret ret;

	xz_crc32_init();
	s = xz_dec_init(XZ_SINGLE, 0);
	if (s == NULL) {
		printf("xz: no memory for decoder state\n");
		return 0;
	}
	b.in = src;  b.in_pos = 0;  b.in_size = src_len;
	b.out = dst; b.out_pos = 0; b.out_size = dst_max;
	ret = xz_dec_run(s, &b);
	xz_dec_end(s);
	if (ret != XZ_STREAM_END) {
		printf("xz: decode failed (%d) at in=%u out=%u\n",
		       (int)ret, (unsigned)b.in_pos, (unsigned)b.out_pos);
		return 0;
	}
	return (unsigned long)b.out_pos;
}
