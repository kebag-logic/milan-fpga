/* Reviewer stub runtime for size comparison only: byte-loop memory primitives
 * and shift/subtract integer helpers, RV32I ILP32, no calls to other helpers. */
typedef unsigned int u32; typedef int s32; typedef unsigned long long u64; typedef long long s64;
typedef unsigned long size_t;
void *memcpy(void *d, const void *s, size_t n) { unsigned char *a = d; const unsigned char *b = s; while (n--) *a++ = *b++; return d; }
void *memmove(void *d, const void *s, size_t n) { unsigned char *a = d; const unsigned char *b = s;
	if (a < b) { while (n--) *a++ = *b++; } else { a += n; b += n; while (n--) *--a = *--b; } return d; }
void *memset(void *d, int c, size_t n) { unsigned char *a = d; while (n--) *a++ = (unsigned char)c; return d; }
int memcmp(const void *x, const void *y, size_t n) { const unsigned char *a = x, *b = y;
	for (; n; --n, ++a, ++b) if (*a != *b) return *a < *b ? -1 : 1; return 0; }
u32 __mulsi3(u32 a, u32 b) { u32 r = 0; while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
u64 __muldi3(u64 a, u64 b) { u64 r = 0; while (b) { if ((u32)b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
static u32 udm32(u32 n, u32 d, u32 *rem) { u64 r = 0; u32 q = 0;
	for (int i = 31; i >= 0; --i) { r = (r << 1) | ((n >> i) & 1u); q <<= 1; if (r >= d) { r -= d; q |= 1u; } }
	if (rem) *rem = (u32)r; return q; }
u32 __udivsi3(u32 n, u32 d) { return udm32(n, d, 0); }
u32 __umodsi3(u32 n, u32 d) { u32 r; udm32(n, d, &r); return r; }
s32 __divsi3(s32 n, s32 d) { u32 q = udm32(n < 0 ? 0u - (u32)n : (u32)n, d < 0 ? 0u - (u32)d : (u32)d, 0); return (n < 0) != (d < 0) ? -(s32)q : (s32)q; }
s32 __modsi3(s32 n, s32 d) { u32 r; udm32(n < 0 ? 0u - (u32)n : (u32)n, d < 0 ? 0u - (u32)d : (u32)d, &r); return n < 0 ? -(s32)r : (s32)r; }
static u64 udm64(u64 n, u64 d, u64 *rem) { u64 q = 0, r = 0;
	for (int i = 0; i < 64; ++i) { r = (r << 1) | (u32)(n >> 63); n <<= 1; q <<= 1; if (r >= d) { r -= d; q |= 1u; } }
	if (rem) *rem = r; return q; }
u64 __udivdi3(u64 n, u64 d) { return udm64(n, d, 0); }
u64 __umoddi3(u64 n, u64 d) { u64 r; udm64(n, d, &r); return r; }
s64 __divdi3(s64 n, s64 d) { u64 q = udm64(n < 0 ? 0u - (u64)n : (u64)n, d < 0 ? 0u - (u64)d : (u64)d, 0); return (n < 0) != (d < 0) ? -(s64)q : (s64)q; }
s64 __moddi3(s64 n, s64 d) { u64 r; udm64(n < 0 ? 0u - (u64)n : (u64)n, d < 0 ? 0u - (u64)d : (u64)d, &r); return n < 0 ? -(s64)r : (s64)r; }
u64 __lshrdi3(u64 a, s32 b) { u32 lo = (u32)a, hi = (u32)(a >> 32); if (b == 0) return a;
	if (b >= 32) { lo = hi >> (b - 32); hi = 0; } else { lo = (lo >> b) | (hi << (32 - b)); hi >>= b; } return ((u64)hi << 32) | lo; }
u64 __ashldi3(u64 a, s32 b) { u32 lo = (u32)a, hi = (u32)(a >> 32); if (b == 0) return a;
	if (b >= 32) { hi = lo << (b - 32); lo = 0; } else { hi = (hi << b) | (lo >> (32 - b)); lo <<= b; } return ((u64)hi << 32) | lo; }
s64 __ashrdi3(s64 a, s32 b) { u32 lo = (u32)a; s32 hi = (s32)(a >> 32); if (b == 0) return a;
	if (b >= 32) { lo = (u32)(hi >> (b - 32)); hi = hi >> 31; } else { lo = (lo >> b) | ((u32)hi << (32 - b)); hi >>= b; } return (s64)(((u64)(u32)hi << 32) | lo); }
