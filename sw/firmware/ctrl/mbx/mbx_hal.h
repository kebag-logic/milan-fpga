// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_hal.h - the three bus functions a host implements to run the
// control-plane firmware against the packet mailbox (#665 lane F0).
//
// THIS IS THE WHOLE BUS PORT. Everything above it (mbx.c, the event loop, the
// protocol adapters) is portable C11 that reaches the fabric only through
// these three calls, with 32-bit accesses and no DMA, as the #640 owner
// decision requires. The other half of the port, memory and the debug sink,
// is ../port (lwSRP's shlan_* functions on a static pool).
//
//   ../plat/mbx_plat_mmio.c   a memory-mapped window: volatile 32-bit loads
//                             and stores at CTRL_MBX_BASE. The on-chip RISC-V
//                             reaches it over Wishbone (KL_mbx_wb, the SoC's
//                             --ctrl-mailbox switch); a hard core reaches the
//                             same window over AXI4-Lite (KL_mbx_axil)
//   ../host/mbx_plat_host.c   the host: every access goes to the C model of
//                             the fabric side, which counts it
//
// The Verilator suite tb/verilator/mbx answers the same three calls with
// cycle-accurate bus transactions on the RTL.

// No synchronous callbacks (#678): a port must return before any core
// input is dispatched by the single bare-metal event loop. A port never
// calls back into a protocol core or the store, including on zero-delay
// timer arms or TX completion. Interrupts defer dispatch to the loop.
// F2 to F5 inherit this rule for every protocol port.

#ifndef MBX_HAL_H
#define MBX_HAL_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Read the 32-bit word at byte_offset (a multiple of 4) inside the window.
uint32_t mbx_hal_read32(uint32_t byte_offset);

// Write value to the 32-bit word at byte_offset (a multiple of 4) inside the
// window, all four byte lanes at once.
void mbx_hal_write32(uint32_t byte_offset, uint32_t value);

// Return when the mailbox interrupt may have work to report. Returning early
// is always correct: the caller polls the ring and event counters itself.
void mbx_hal_wait(void);

#ifdef __cplusplus
}
#endif

#endif // MBX_HAL_H
