// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mbx_dma.h - the split placement's record mover (KL_mbx_dma, #665, owner
// decision 2026-10-29; NFR-SCOUT-03), for the mailbox driver.
//
// The mover copies one record's payload between a mailbox ring and the
// CPU's memory through the CPU's coherent DMA port, so the hart makes four
// register accesses a record instead of one uncached access a word. Its
// registers are one 32-bit word each from CTRL_MBX_DMA_BASE, in the order
// milan_soc.CTRL_MBX_DMA_REGISTERS gives them:
//   CFG     [15:0] the ring's word 0 as a word address in the mailbox
//           window; [31:16] the ring's words less one;
//   MEM     the memory side's first byte, on a word;
//   CMD     [15:0] the ring index of the payload's first word; [27:16] its
//           bytes; [31] 1 for memory to the ring. A write starts the move;
//   STATUS  [0] BUSY; [1] ERR, set by a refused start or an error response
//           and cleared by the next accepted start.
// A move leaves memory or the ring exactly as the driver's word loop would:
// in ring order, a transmit word's lanes past the length zero, a receive
// move's bytes past the length untouched. While it runs the mover owns the
// mailbox's host port, so every access the driver makes to the window
// waits for it.

#ifndef MBX_DMA_H
#define MBX_DMA_H

#include <stdbool.h>
#include <stdint.h>

#ifndef CTRL_MBX_DMA_BASE
#error "CTRL_MBX_DMA_BASE: define the record mover's CSR bank address (the SoC's generated memory map)"
#endif

#define MBX_DMA_REG_CFG 0x0u
#define MBX_DMA_REG_MEM 0x4u
#define MBX_DMA_REG_CMD 0x8u
#define MBX_DMA_REG_STATUS 0xCu
#define MBX_DMA_CFG_MASK_LSB 16u
#define MBX_DMA_CMD_LEN_LSB 16u
#define MBX_DMA_CMD_TO_RING (1u << 31)
#define MBX_DMA_STATUS_BUSY 0x1u
#define MBX_DMA_STATUS_ERR 0x2u

static inline volatile uint32_t *mbx_dma_reg(uint32_t reg)
{
	return (volatile uint32_t *)(uintptr_t)((uintptr_t)(CTRL_MBX_DMA_BASE) + reg);
}

// Move len bytes between the ring of `words` words at window byte offset
// `base`, from ring index `index` on, and the word-aligned buffer at p;
// to_ring moves memory to the ring. Returns once the move has ended, true
// unless it ended with ERR. The mover takes CMD the cycle after its write
// and is BUSY the cycle after that, well before the STATUS read that
// follows the write on the bus reaches it.
static inline bool mbx_dma_move(uint32_t base, uint32_t words, uint32_t index, const void *p, uint32_t len,
				bool to_ring)
{
	*mbx_dma_reg(MBX_DMA_REG_CFG) = (base >> 2) | ((words - 1u) << MBX_DMA_CFG_MASK_LSB);
	*mbx_dma_reg(MBX_DMA_REG_MEM) = (uint32_t)(uintptr_t)p;
	*mbx_dma_reg(MBX_DMA_REG_CMD) = (index & 0xFFFFu) | (len << MBX_DMA_CMD_LEN_LSB) |
					(to_ring ? MBX_DMA_CMD_TO_RING : 0u);
	uint32_t status;
	do {
		status = *mbx_dma_reg(MBX_DMA_REG_STATUS);
	} while ((status & MBX_DMA_STATUS_BUSY) != 0u);
	return (status & MBX_DMA_STATUS_ERR) == 0u;
}

#endif // MBX_DMA_H
