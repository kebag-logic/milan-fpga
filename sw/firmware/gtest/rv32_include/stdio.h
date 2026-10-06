/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* The bounded C11 formatter's declaration for object-only target checks.
 * This declares the runtime interface; it supplies no replacement formatter. */
#ifndef MILAN_RV32_STDIO_H
#define MILAN_RV32_STDIO_H

#include <stdarg.h>
#include <stddef.h>

int vsnprintf(char *restrict dst, size_t n, const char *restrict fmt, va_list ap);

#endif
