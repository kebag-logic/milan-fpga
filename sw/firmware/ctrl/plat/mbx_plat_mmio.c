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
// does not say where the window is fails in mbx_mmio.h rather than guessing.
// mbx_mmio.h holds the two accesses, which the driver built for the window
// makes in place (mbx.c, #665).
//
// mbx_hal_wait() returns at once unless the platform defines CTRL_MBX_WFI,
// in which case the core waits for an interrupt. Returning early is always
// correct: the loop polls. The loop sleeps only after a pass that handled
// nothing and owes nothing (ctrl_loop.h), so every wake it then needs is a
// mailbox interrupt cause; a platform that defines CTRL_MBX_WFI must also
// enable that line as a wake source (on the switch-on SoC, the `ctrl_mbx`
// EventManager source and the CPU's interrupt mask).
//
// A hard core with a weakly ordered memory model must map the window as
// device (strongly ordered) memory, or give these functions a barrier before
// each write, so a record's words reach the window before the doorbell
// (TX_HEAD, RX_TAIL, EVT_TAIL) that commits or releases them.

#include <stdint.h>

#include "mbx_hal.h"
#include "mbx_mmio.h"

uint32_t mbx_hal_read32(uint32_t byte_offset)
{
	return mbx_mmio_read32(byte_offset);
}

void mbx_hal_write32(uint32_t byte_offset, uint32_t value)
{
	mbx_mmio_write32(byte_offset, value);
}

void mbx_hal_wait(void)
{
#ifdef CTRL_MBX_WFI
	CTRL_MBX_WFI();
#endif
}
