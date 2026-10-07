/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* The C11 assertion macro and its handler's declaration for object-only target
 * checks. This declares the runtime interface; it supplies no handler.
 * Like any <assert.h>, assert follows NDEBUG at each inclusion (C11 7.2). */
#undef assert
#ifdef NDEBUG
#define assert(ignore) ((void)0)
#else
#define assert(expr) ((expr) ? (void)0 : __assert_fail(#expr, __FILE__, __LINE__, __func__))
#endif

#ifndef MILAN_RV32_ASSERT_H
#define MILAN_RV32_ASSERT_H

#define static_assert _Static_assert

_Noreturn void __assert_fail(const char *expr, const char *file, unsigned int line, const char *func);

#endif
