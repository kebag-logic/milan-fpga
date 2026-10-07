/* SPDX-License-Identifier: CERN-OHL-W-2.0 */
/* Freestanding C11 memory declarations for object-only target checks.
 * Implementations belong to the product's bare-metal C runtime. */
#ifndef MILAN_RV32_STRING_H
#define MILAN_RV32_STRING_H

#include <stddef.h>

void *memcpy(void *restrict dst, const void *restrict src, size_t n);
void *memset(void *dst, int value, size_t n);
void *memmove(void *dst, const void *src, size_t n);
int memcmp(const void *a, const void *b, size_t n);

#endif
