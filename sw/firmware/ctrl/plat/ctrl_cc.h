// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_cc.h - the compiler extensions the control firmware uses, behind one
// switch with a portable C11 fallback (#665: the firmware is portable C11 and
// ports to a hard core, whose compiler need not take GNU C's attributes). It
// is the one file of the firmware outside test/ that names one.
//
// CTRL_CC_GNU is 1 where the compiler takes GNU C's attributes (__GNUC__,
// which GCC and Clang define), else 0; a build may set it. With 0 every
// definition below is plain C11 and the firmware does what it does with 1:
// only its code, and so its cost, may differ.
//   CTRL_CC_NOINLINE   a function kept out of line, so the hot code that
//                      calls it stays small (GNU noinline); nothing with 0.
//   ctrl_cc_ptr_load,  a pointer read or written in place on bytes of another
//   ctrl_cc_ptr_store  type, the pool's free-list link (GNU may_alias keeps
//                      the access defined); memcpy with 0.

#ifndef CTRL_CC_H
#define CTRL_CC_H

#ifndef CTRL_CC_GNU
#ifdef __GNUC__
#define CTRL_CC_GNU 1
#else
#define CTRL_CC_GNU 0
#endif
#endif

#if CTRL_CC_GNU
#define CTRL_CC_NOINLINE __attribute__((noinline))
typedef void *__attribute__((may_alias)) ctrl_cc_ptr;

static inline void *ctrl_cc_ptr_load(const void *at)
{
	return *(const ctrl_cc_ptr *)at;
}

static inline void ctrl_cc_ptr_store(void *at, void *value)
{
	*(ctrl_cc_ptr *)at = value;
}
#else
#include <string.h>

#define CTRL_CC_NOINLINE

static inline void *ctrl_cc_ptr_load(const void *at)
{
	void *value;
	memcpy(&value, at, sizeof value);
	return value;
}

static inline void ctrl_cc_ptr_store(void *at, void *value)
{
	memcpy(at, &value, sizeof value);
}
#endif

#endif // CTRL_CC_H
