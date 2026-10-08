// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// image_rt.c - stand-ins for the C runtime the firmware calls (rv32_include),
// which the SoC's image takes from its libbase: byte loops, and a formatter
// that copies its format unexpanded. They let the measured image link; their
// bytes are a floor for the runtime, and ctrl_image.py reports them apart
// from the firmware's.

#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>

void *memset(void *dst, int c, size_t n);
void *memcpy(void *dst, const void *src, size_t n);
void *memmove(void *dst, const void *src, size_t n);
int memcmp(const void *a, const void *b, size_t n);
int vsnprintf(char *out, size_t size, const char *fmt, va_list ap);

void *memset(void *dst, int c, size_t n)
{
	unsigned char *d = dst;
	while (n-- != 0u) {
		*d++ = (unsigned char)c;
	}
	return dst;
}

void *memcpy(void *dst, const void *src, size_t n)
{
	unsigned char *d = dst;
	const unsigned char *s = src;
	while (n-- != 0u) {
		*d++ = *s++;
	}
	return dst;
}

void *memmove(void *dst, const void *src, size_t n)
{
	unsigned char *d = dst;
	const unsigned char *s = src;
	if (d < s) {
		while (n-- != 0u) {
			*d++ = *s++;
		}
	} else {
		while (n-- != 0u) {
			d[n] = s[n];
		}
	}
	return dst;
}

int memcmp(const void *a, const void *b, size_t n)
{
	const unsigned char *x = a;
	const unsigned char *y = b;
	for (size_t i = 0; i < n; ++i) {
		if (x[i] != y[i]) {
			return x[i] < y[i] ? -1 : 1;
		}
	}
	return 0;
}

int vsnprintf(char *out, size_t size, const char *fmt, va_list ap)
{
	(void)ap;
	size_t n = 0;
	while (fmt[n] != '\0') {
		if (n + 1u < size) {
			out[n] = fmt[n];
		}
		++n;
	}
	if (size != 0u) {
		out[n < size ? n : size - 1u] = '\0';
	}
	return (int)n;
}
