// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// shlan_port.h - lwSRP's port layer, provided by the bare-metal firmware
// (#665 lane F0, the owner directive of 2026-10-05: "the HAL must carry
// lwSRP's port layer").
//
// lwSRP (github.com/kebag-logic/lwSRP) routes every allocation and every
// print through four functions declared in its src/ports/alloc.h, and its
// timers through src/ports/timer.h, whose shlan_timer_tick() the platform
// calls once per centisecond. Its own alloc.c maps the four onto malloc and
// vprintf, which a bare-metal target without a heap does not have. This
// firmware provides them instead:
//
//   shlan_malloc / shlan_calloc / shlan_free  ->  the static block pool
//                                                 (ctrl_pool.h), never a heap
//   shlan_printf                              ->  the debug sink (ctrl_debug.h)
//
// and the event loop (../loop/ctrl_loop.h) calls each registered
// centisecond consumer, lwSRP's shlan_timer_tick among them, once per tick
// the fabric's TICK event counts. The prototypes below are lwSRP's,
// restated so the firmware builds without the library; a build that links
// lwSRP links its timer.c and every other core file, and leaves its alloc.c
// out. The host test's lwsrp-port arm (../test/test_ctrl_firmware.py) builds
// lwSRP's own MRP core against this file and drives it through the mailbox.

// No synchronous callbacks (#678): a port must return before any core
// input is dispatched by the single bare-metal event loop. A port never
// calls back into a protocol core or the store, including on zero-delay
// timer arms or TX completion. Interrupts defer dispatch to the loop.
// F2 to F5 inherit this rule for every protocol port.

#ifndef SHLAN_PORT_H
#define SHLAN_PORT_H

#include <stddef.h>

#include "ctrl_pool.h"

#ifdef __cplusplus
extern "C" {
#endif

void *shlan_malloc(size_t size);
void *shlan_calloc(size_t nmemb, size_t size);
void shlan_free(void *ptr);
int shlan_printf(const char *fmt, ...);

// The pool the four functions draw on; bound once at boot, before any
// protocol module starts. Until then every allocation is refused.
void shlan_port_bind_pool(struct ctrl_pool *pool);

// The bound pool, for its counters (NULL before the bind).
struct ctrl_pool *shlan_port_pool(void);

#ifdef __cplusplus
}
#endif

#endif // SHLAN_PORT_H
