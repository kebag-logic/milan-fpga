/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
#ifndef HW_COMMON_H
#define HW_COMMON_H
static inline void cdelay(int i) { while (i-- > 0) __asm__ volatile("nop"); }
#endif
