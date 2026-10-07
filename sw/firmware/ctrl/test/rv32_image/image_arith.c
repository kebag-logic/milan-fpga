// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// image_arith.c - the integer arithmetic helpers GCC calls on RV32I, which has
// no multiply or divide instruction and no 64-bit shift: every helper of
// fw_rv32.HELPERS, the set the rv32 arm lets the firmware leave open (it has
// no floating-point helper, so the firmware reaches none). The pinned SDK's
// libgcc is built for its one multilib, rv32imafd with the ilp32d ABI, so it
// cannot link into a soft-float RV32I image; the measured image takes these
// instead, and ctrl_image.py reports their bytes apart from the firmware's,
// like the C-runtime stand-ins. Each is a shift-and-add or shift-and-subtract
// loop on 32-bit words or with constant 64-bit shifts, so none calls a helper
// (ctrl_image.py refuses this object if it leaves a symbol open or calls one).
// Division by zero and the most negative value over -1 are undefined in C and
// are not relied on.

#include <stdint.h>

uint32_t __mulsi3(uint32_t a, uint32_t b);
int32_t __divsi3(int32_t a, int32_t b);
int32_t __modsi3(int32_t a, int32_t b);
uint32_t __udivsi3(uint32_t a, uint32_t b);
uint32_t __umodsi3(uint32_t a, uint32_t b);
int64_t __muldi3(int64_t a, int64_t b);
int64_t __divdi3(int64_t a, int64_t b);
int64_t __moddi3(int64_t a, int64_t b);
uint64_t __udivdi3(uint64_t a, uint64_t b);
uint64_t __umoddi3(uint64_t a, uint64_t b);
int64_t __lshrdi3(int64_t a, int b);
int64_t __ashldi3(int64_t a, int b);
int64_t __ashrdi3(int64_t a, int b);

// One bit of the quotient per step; `carry` holds the remainder's 33rd bit,
// so a divisor above 2^31 (2^63) still divides.
static uint32_t image_udivmod32(uint32_t n, uint32_t d, uint32_t *rem)
{
	uint32_t q = 0u;
	uint32_t r = 0u;
	for (unsigned i = 0u; i < 32u; ++i) {
		uint32_t carry = r >> 31;
		r = (r << 1) | (n >> 31);
		n <<= 1;
		q <<= 1;
		if (carry != 0u || r >= d) {
			r -= d;
			q |= 1u;
		}
	}
	*rem = r;
	return q;
}

static uint64_t image_udivmod64(uint64_t n, uint64_t d, uint64_t *rem)
{
	uint64_t q = 0u;
	uint64_t r = 0u;
	for (unsigned i = 0u; i < 64u; ++i) {
		uint64_t carry = r >> 63;
		r = (r << 1) | (n >> 63);
		n <<= 1;
		q <<= 1;
		if (carry != 0u || r >= d) {
			r -= d;
			q |= 1u;
		}
	}
	*rem = r;
	return q;
}

// A multiplier bit as a mask of 0 or all ones, through an empty asm so the
// compiler cannot see that it is one or the other: GCC turns `if (bit) p += x`
// and `p += x & -bit` into a product by the bit, which for 64 bits is a call
// to __muldi3, so from __muldi3 itself.
static uint32_t image_mask(uint32_t bit)
{
	uint32_t m = 0u - bit;
	__asm__("" : "+r"(m));
	return m;
}

static uint32_t image_abs32(int32_t v)
{
	return v < 0 ? 0u - (uint32_t)v : (uint32_t)v;
}

static uint64_t image_abs64(int64_t v)
{
	return v < 0 ? 0u - (uint64_t)v : (uint64_t)v;
}

uint32_t __mulsi3(uint32_t a, uint32_t b)
{
	uint32_t p = 0u;
	while (b != 0u) {
		p += a & image_mask(b & 1u);
		a <<= 1;
		b >>= 1;
	}
	return p;
}

uint32_t __udivsi3(uint32_t a, uint32_t b)
{
	uint32_t r;
	return image_udivmod32(a, b, &r);
}

uint32_t __umodsi3(uint32_t a, uint32_t b)
{
	uint32_t r;
	(void)image_udivmod32(a, b, &r);
	return r;
}

// C truncates toward zero: the quotient's sign is the operands' and the
// remainder's the dividend's.
int32_t __divsi3(int32_t a, int32_t b)
{
	uint32_t r;
	uint32_t q = image_udivmod32(image_abs32(a), image_abs32(b), &r);
	return (int32_t)((a < 0) != (b < 0) ? 0u - q : q);
}

int32_t __modsi3(int32_t a, int32_t b)
{
	uint32_t r;
	(void)image_udivmod32(image_abs32(a), image_abs32(b), &r);
	return (int32_t)(a < 0 ? 0u - r : r);
}

// On the halves, with the carry out of the low word by hand: GCC also folds
// a 64-bit `(m << 32) | m` into a product by 2^32 + 1.
int64_t __muldi3(int64_t a, int64_t b)
{
	uint32_t xlo = (uint32_t)a;
	uint32_t xhi = (uint32_t)((uint64_t)a >> 32);
	uint32_t ylo = (uint32_t)b;
	uint32_t yhi = (uint32_t)((uint64_t)b >> 32);
	uint32_t lo = 0u;
	uint32_t hi = 0u;
	while ((ylo | yhi) != 0u) {
		uint32_t m = image_mask(ylo & 1u);
		uint32_t add = xlo & m;
		lo += add;
		hi += (xhi & m) + (lo < add ? 1u : 0u);
		xhi = (xhi << 1) | (xlo >> 31);
		xlo <<= 1;
		ylo = (ylo >> 1) | (yhi << 31);
		yhi >>= 1;
	}
	return (int64_t)(((uint64_t)hi << 32) | lo);
}

uint64_t __udivdi3(uint64_t a, uint64_t b)
{
	uint64_t r;
	return image_udivmod64(a, b, &r);
}

uint64_t __umoddi3(uint64_t a, uint64_t b)
{
	uint64_t r;
	(void)image_udivmod64(a, b, &r);
	return r;
}

int64_t __divdi3(int64_t a, int64_t b)
{
	uint64_t r;
	uint64_t q = image_udivmod64(image_abs64(a), image_abs64(b), &r);
	return (int64_t)((a < 0) != (b < 0) ? 0u - q : q);
}

int64_t __moddi3(int64_t a, int64_t b)
{
	uint64_t r;
	(void)image_udivmod64(image_abs64(a), image_abs64(b), &r);
	return (int64_t)(a < 0 ? 0u - r : r);
}

// The shifts take 0 <= b < 64 (C's range) and work on the halves, whose
// shifts by a variable count are RV32I's own.
int64_t __lshrdi3(int64_t a, int b)
{
	uint32_t hi = (uint32_t)((uint64_t)a >> 32);
	uint32_t lo = (uint32_t)a;
	if (b >= 32) {
		lo = hi >> (b - 32);
		hi = 0u;
	} else if (b != 0) {
		lo = (lo >> b) | (hi << (32 - b));
		hi >>= b;
	}
	return (int64_t)(((uint64_t)hi << 32) | lo);
}

int64_t __ashldi3(int64_t a, int b)
{
	uint32_t hi = (uint32_t)((uint64_t)a >> 32);
	uint32_t lo = (uint32_t)a;
	if (b >= 32) {
		hi = lo << (b - 32);
		lo = 0u;
	} else if (b != 0) {
		hi = (hi << b) | (lo >> (32 - b));
		lo <<= b;
	}
	return (int64_t)(((uint64_t)hi << 32) | lo);
}

// GCC shifts a negative int32_t arithmetically, which fills with its sign.
int64_t __ashrdi3(int64_t a, int b)
{
	int32_t hi = (int32_t)((uint64_t)a >> 32);
	uint32_t lo = (uint32_t)a;
	if (b >= 32) {
		lo = (uint32_t)(hi >> (b - 32));
		hi >>= 31;
	} else if (b != 0) {
		lo = (lo >> b) | ((uint32_t)hi << (32 - b));
		hi >>= b;
	}
	return (int64_t)(((uint64_t)(uint32_t)hi << 32) | lo);
}
