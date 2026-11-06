// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mmio_dma.h - the record mover's registers mbx/mbx.c is built over on the
// host (#665). The unit arm force-includes it, with mmio_window.h, into the
// driver built as the split image builds it, and points the driver's
// CTRL_MBX_DMA_BASE at ctrl_test_dma_base(), a register model of KL_mbx_dma
// (test_mbx_dma_driver.cpp). The driver forms each register's address from
// CTRL_MBX_DMA_BASE at every access (plat/mbx_dma.h), so the model sees each
// access before it is made, and takes a CMD written since the last one as a
// start.

#ifndef MMIO_DMA_H
#define MMIO_DMA_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// The mover's bank: CFG, MEM, CMD and STATUS, one word each
// (milan_soc.CTRL_MBX_DMA_REGISTERS).
#define CTRL_TEST_DMA_WORDS 4u

extern uint32_t ctrl_test_dma[CTRL_TEST_DMA_WORDS];
uintptr_t ctrl_test_dma_base(void);

#ifdef __cplusplus
}
#endif

#endif // MMIO_DMA_H
