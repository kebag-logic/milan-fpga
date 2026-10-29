// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat_io.h - the split platform's bus port for the devices beside the
// mailbox: the datapath CSR window and the LiteX UART (#665 S3).
//
// Two calls, as mbx_hal.h is for the mailbox: one 32-bit load or store at a
// bus address. ctrl_plat_mmio.c is the target's, a volatile access; the host
// tests answer them with a register file. Every access the platform makes to
// those devices goes through here, so a test sees each one, in order.

#ifndef CTRL_PLAT_IO_H
#define CTRL_PLAT_IO_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint32_t ctrl_plat_io_read32(uintptr_t address);
void ctrl_plat_io_write32(uintptr_t address, uint32_t value);

#ifdef __cplusplus
}
#endif

#endif // CTRL_PLAT_IO_H
