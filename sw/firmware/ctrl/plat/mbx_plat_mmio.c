// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_plat_mmio.c - mbx_hal.h on a memory-mapped mailbox window: the on-chip
// RISC-V (Wishbone, KL_mbx_wb) and a hard core (AXI4-Lite, KL_mbx_axil)
// reach the same window this way, at the base their SoC maps it.
//
// The window is uncached I/O: every access is one volatile 32-bit load or
// store, so the compiler neither merges, splits, reorders nor drops one, and
// the bus sees exactly the accesses the driver makes. CTRL_MBX_BASE is the
// window's bus address, from the SoC's generated memory map; a build that
// does not say where the window is fails here rather than guessing.
//
// mbx_hal_wait() returns at once unless the platform defines CTRL_MBX_WFI,
// in which case the core waits for an interrupt (the mailbox line is one of
// its wake sources). Returning early is always correct: the loop polls.

#include <stdint.h>

#include "mbx_hal.h"

#ifndef CTRL_MBX_BASE
#error "CTRL_MBX_BASE: define the mailbox window's bus address (the SoC's generated memory map)"
#endif

static volatile uint32_t *word_at(uint32_t byte_offset)
{
	return (volatile uint32_t *)(uintptr_t)((uintptr_t)(CTRL_MBX_BASE) + byte_offset);
}

uint32_t mbx_hal_read32(uint32_t byte_offset)
{
	return *word_at(byte_offset);
}

void mbx_hal_write32(uint32_t byte_offset, uint32_t value)
{
	*word_at(byte_offset) = value;
}

void mbx_hal_wait(void)
{
#ifdef CTRL_MBX_WFI
	CTRL_MBX_WFI();
#endif
}
