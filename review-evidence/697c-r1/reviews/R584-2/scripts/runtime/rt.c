/* A reviewer-written stand-in runtime for differential image linking only: the SAME archives are
 * linked into the dev and the head image, so their ELF identity isolates the firmware objects.
 * Shift/add loops only, so the compiler cannot call back into these helpers. */
#include <stddef.h>
#include <stdint.h>
#ifdef RT_LIBC
void *memcpy(void *d, const void *s, size_t n) { unsigned char *a = d; const unsigned char *b = s; while (n--) *a++ = *b++; return d; }
void *memmove(void *d, const void *s, size_t n) { unsigned char *a = d; const unsigned char *b = s;
  if (a < b) { while (n--) *a++ = *b++; } else { a += n; b += n; while (n--) *--a = *--b; } return d; }
void *memset(void *d, int c, size_t n) { unsigned char *a = d; while (n--) *a++ = (unsigned char)c; return d; }
int memcmp(const void *x, const void *y, size_t n) { const unsigned char *a = x, *b = y;
  for (; n; n--, a++, b++) if (*a != *b) return *a < *b ? -1 : 1; return 0; }
#else
typedef union { uint64_t u; struct { uint32_t lo, hi; } w; } dw;
uint64_t __lshrdi3(uint64_t a, int b) { dw x, r; x.u = a; if (b == 0) return a;
  if (b >= 32) { r.w.hi = 0; r.w.lo = x.w.hi >> (b - 32); } else { r.w.hi = x.w.hi >> b; r.w.lo = (x.w.lo >> b) | (x.w.hi << (32 - b)); } return r.u; }
uint64_t __ashldi3(uint64_t a, int b) { dw x, r; x.u = a; if (b == 0) return a;
  if (b >= 32) { r.w.lo = 0; r.w.hi = x.w.lo << (b - 32); } else { r.w.lo = x.w.lo << b; r.w.hi = (x.w.hi << b) | (x.w.lo >> (32 - b)); } return r.u; }
int64_t __ashrdi3(int64_t a, int b) { dw x, r; x.u = (uint64_t)a; if (b == 0) return a;
  if (b >= 32) { r.w.hi = (uint32_t)((int32_t)x.w.hi >> 31); r.w.lo = (uint32_t)((int32_t)x.w.hi >> (b - 32)); }
  else { r.w.hi = (uint32_t)((int32_t)x.w.hi >> b); r.w.lo = (x.w.lo >> b) | (x.w.hi << (32 - b)); } return (int64_t)r.u; }
uint32_t __mulsi3(uint32_t a, uint32_t b) { uint32_t r = 0; while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
uint64_t __muldi3(uint64_t a, uint64_t b) { uint64_t r = 0; while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
static uint32_t udm32(uint32_t n, uint32_t d, uint32_t *rem) { uint32_t q = 0, r = 0; int i;
  for (i = 31; i >= 0; i--) { r = (r << 1) | ((n >> i) & 1u); if (r >= d) { r -= d; q |= 1u << i; } } if (rem) *rem = r; return q; }
uint64_t __udivmoddi4(uint64_t n, uint64_t d, uint64_t *rem) { uint64_t q = 0, r = 0; int i;
  for (i = 63; i >= 0; i--) { r = (r << 1) | ((n >> i) & 1u); if (r >= d) { r -= d; q |= (uint64_t)1 << i; } } if (rem) *rem = r; return q; }
uint32_t __udivsi3(uint32_t n, uint32_t d) { return udm32(n, d, 0); }
uint32_t __umodsi3(uint32_t n, uint32_t d) { uint32_t r; udm32(n, d, &r); return r; }
int32_t __divsi3(int32_t a, int32_t b) { uint32_t q = udm32(a < 0 ? -(uint32_t)a : (uint32_t)a, b < 0 ? -(uint32_t)b : (uint32_t)b, 0); return (a < 0) != (b < 0) ? -(int32_t)q : (int32_t)q; }
int32_t __modsi3(int32_t a, int32_t b) { uint32_t r; udm32(a < 0 ? -(uint32_t)a : (uint32_t)a, b < 0 ? -(uint32_t)b : (uint32_t)b, &r); return a < 0 ? -(int32_t)r : (int32_t)r; }
uint64_t __udivdi3(uint64_t n, uint64_t d) { return __udivmoddi4(n, d, 0); }
uint64_t __umoddi3(uint64_t n, uint64_t d) { uint64_t r; __udivmoddi4(n, d, &r); return r; }
int64_t __divdi3(int64_t a, int64_t b) { uint64_t q = __udivmoddi4(a < 0 ? -(uint64_t)a : (uint64_t)a, b < 0 ? -(uint64_t)b : (uint64_t)b, 0); return (a < 0) != (b < 0) ? -(int64_t)q : (int64_t)q; }
int64_t __moddi3(int64_t a, int64_t b) { uint64_t r; __udivmoddi4(a < 0 ? -(uint64_t)a : (uint64_t)a, b < 0 ? -(uint64_t)b : (uint64_t)b, &r); return a < 0 ? -(int64_t)r : (int64_t)r; }
int __clzsi2(uint32_t a) { int n = 0; if (!a) return 32; while (!(a & 0x80000000u)) { a <<= 1; n++; } return n; }
int __ctzsi2(uint32_t a) { int n = 0; if (!a) return 32; while (!(a & 1u)) { a >>= 1; n++; } return n; }
int __clzdi2(uint64_t a) { uint32_t h = (uint32_t)(a >> 32); return h ? __clzsi2(h) : 32 + __clzsi2((uint32_t)a); }
int __ctzdi2(uint64_t a) { uint32_t l = (uint32_t)a; return l ? __ctzsi2(l) : 32 + __ctzsi2((uint32_t)(a >> 32)); }
int __ucmpdi2(uint64_t a, uint64_t b) { return a < b ? 0 : a > b ? 2 : 1; }
#endif
