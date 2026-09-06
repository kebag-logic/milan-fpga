/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for LiteX hw/common.h: the busy-wait advances model time. */
#ifndef HW_COMMON_H
#define HW_COMMON_H
#include "../nvm_host.h"
static inline void cdelay(int i) { nvm_host_tick(i); }
#endif
