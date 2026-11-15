// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_mmio.h - the memory-mapped window's two accesses, as inline functions
// (#665; FR_NFR.md 3.4.1).
//
// Each is one volatile 32-bit load or store of the word at CTRL_MBX_BASE plus
// the byte offset. mbx_plat_mmio.c's mbx_hal_read32() and mbx_hal_write32()
// are these. The driver (mbx.c), built for the window, makes them in place:
// on the split core a call a ring word, and the register spills the call
// forced around it, cost about 125 CPU cycles a word, against the access's 9.
// The bus sees the same accesses in the same order either way.

#ifndef MBX_MMIO_H
#define MBX_MMIO_H

#include <stdint.h>

#ifndef CTRL_MBX_BASE
#error "CTRL_MBX_BASE: define the mailbox window's bus address (the SoC's generated memory map)"
#endif

static inline volatile uint32_t *mbx_mmio_word(uint32_t byte_offset)
{
	return (volatile uint32_t *)(uintptr_t)((uintptr_t)(CTRL_MBX_BASE) + byte_offset);
}

static inline uint32_t mbx_mmio_read32(uint32_t byte_offset)
{
	return *mbx_mmio_word(byte_offset);
}

static inline void mbx_mmio_write32(uint32_t byte_offset, uint32_t value)
{
	*mbx_mmio_word(byte_offset) = value;
}

#endif // MBX_MMIO_H
