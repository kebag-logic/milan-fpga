// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_debug.h - the debug sink behind shlan_printf (#665 lane F0).
//
// A protocol module prints through one formatter into one fixed line buffer,
// and the line goes to whatever sink the platform bound: the UART on the
// on-chip RISC-V, a capture buffer on the host. Nothing here allocates, and a
// line longer than the buffer is truncated, never split or dropped whole, so
// one print costs a bounded time. With no sink bound the text is discarded
// and counted.

#ifndef CTRL_DEBUG_H
#define CTRL_DEBUG_H

#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// The longest line one print emits, terminator excluded.
#define CTRL_DEBUG_LINE_BYTES 120u

// Where the text goes. Called once per print, with the formatted bytes.
typedef void (*ctrl_debug_sink_fn)(void *ctx, const char *text, size_t len);

void ctrl_debug_bind(ctrl_debug_sink_fn sink, void *ctx);

// Format and emit; returns the bytes handed to the sink (after truncation),
// or a negative value when the format itself failed.
int ctrl_debug_vprintf(const char *fmt, va_list ap);

// Prints the sink never saw: no sink bound, or the format failed.
uint32_t ctrl_debug_discarded(void);

// Prints that were longer than CTRL_DEBUG_LINE_BYTES.
uint32_t ctrl_debug_truncated(void);

#ifdef __cplusplus
}
#endif

#endif // CTRL_DEBUG_H
