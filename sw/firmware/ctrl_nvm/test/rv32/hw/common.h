/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* LiteX hw/common.h's busy-wait, for the RV32 freestanding build of the host
 * suite (#665 lane F1). */
#ifndef HW_COMMON_H
#define HW_COMMON_H
static inline void cdelay(int i)
{
	while (i > 0) {
		__asm__ volatile("nop");
		i--;
	}
}
#endif
