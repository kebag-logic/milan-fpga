/* Shift-and-subtract integer helpers for RV32I (no M extension); no operator here lowers to a helper call. */
typedef unsigned int u32; typedef int s32; typedef unsigned long long u64; typedef long long s64;
u32 __mulsi3(u32 a, u32 b) { u32 r = 0; while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
static u32 udivmod32(u32 n, u32 d, u32 *rem) { u32 q = 0, r = 0; int i;
  for (i = 31; i >= 0; i--) { r = (r << 1) | ((n >> i) & 1u); if (r >= d) { r -= d; q |= (1u << i); } } if (rem) *rem = r; return q; }
u32 __udivsi3(u32 n, u32 d) { return udivmod32(n, d, 0); }
u32 __umodsi3(u32 n, u32 d) { u32 r; udivmod32(n, d, &r); return r; }
s32 __divsi3(s32 a, s32 b) { int neg = (a < 0) != (b < 0); u32 q = udivmod32(a < 0 ? 0u - (u32)a : (u32)a, b < 0 ? 0u - (u32)b : (u32)b, 0); return neg ? (s32)(0u - q) : (s32)q; }
s32 __modsi3(s32 a, s32 b) { u32 r; udivmod32(a < 0 ? 0u - (u32)a : (u32)a, b < 0 ? 0u - (u32)b : (u32)b, &r); return a < 0 ? (s32)(0u - r) : (s32)r; }
static u64 udivmod64(u64 n, u64 d, u64 *rem) { u64 q = 0, r = 0; int i;
  for (i = 63; i >= 0; i--) { r = (r << 1) | ((n >> i) & 1u); if (r >= d) { r -= d; q |= ((u64)1 << i); } } if (rem) *rem = r; return q; }
u64 __udivdi3(u64 n, u64 d) { return udivmod64(n, d, 0); }
u64 __umoddi3(u64 n, u64 d) { u64 r; udivmod64(n, d, &r); return r; }
u64 __udivmoddi4(u64 n, u64 d, u64 *r) { return udivmod64(n, d, r); }
s64 __divdi3(s64 a, s64 b) { int neg = (a < 0) != (b < 0); u64 q = udivmod64(a < 0 ? 0u - (u64)a : (u64)a, b < 0 ? 0u - (u64)b : (u64)b, 0); return neg ? (s64)(0u - q) : (s64)q; }
s64 __moddi3(s64 a, s64 b) { u64 r; udivmod64(a < 0 ? 0u - (u64)a : (u64)a, b < 0 ? 0u - (u64)b : (u64)b, &r); return a < 0 ? (s64)(0u - r) : (s64)r; }
u64 __muldi3(u64 a, u64 b) { u64 r = 0; while (b) { if (b & 1u) r += a; a <<= 1; b >>= 1; } return r; }
typedef union { u64 all; struct { u32 lo, hi; } s; } dw;
u64 __ashldi3(u64 a, int b) { dw x, r; x.all = a; if (b == 0) return a; if (b >= 32) { r.s.lo = 0; r.s.hi = x.s.lo << (b - 32); }
  else { r.s.lo = x.s.lo << b; r.s.hi = (x.s.hi << b) | (x.s.lo >> (32 - b)); } return r.all; }
u64 __lshrdi3(u64 a, int b) { dw x, r; x.all = a; if (b == 0) return a; if (b >= 32) { r.s.hi = 0; r.s.lo = x.s.hi >> (b - 32); }
  else { r.s.hi = x.s.hi >> b; r.s.lo = (x.s.lo >> b) | (x.s.hi << (32 - b)); } return r.all; }
s64 __ashrdi3(s64 a, int b) { dw x, r; x.all = (u64)a; if (b == 0) return a; if (b >= 32) { r.s.hi = (u32)((s32)x.s.hi >> 31); r.s.lo = (u32)((s32)x.s.hi >> (b - 32)); }
  else { r.s.hi = (u32)((s32)x.s.hi >> b); r.s.lo = (x.s.lo >> b) | (x.s.hi << (32 - b)); } return (s64)r.all; }
