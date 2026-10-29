// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_mmio.c - ctrl_plat_io.h on the split SoC's bus (#665).
//
// The CSR window and the UART are uncached I/O regions, as the mailbox window
// is (mbx_plat_mmio.c): every access is one volatile 32-bit load or store, so
// the bus sees exactly the accesses the platform makes, in program order. A
// hard core with a weakly ordered memory model must map both as device memory.

#include "ctrl_plat_io.h"

uint32_t ctrl_plat_io_read32(uintptr_t address)
{
	return *(volatile uint32_t *)address;
}

void ctrl_plat_io_write32(uintptr_t address, uint32_t value)
{
	*(volatile uint32_t *)address = value;
}
