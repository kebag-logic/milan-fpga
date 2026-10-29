# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""mbx_dma_mutants.py - planted defects in the mailbox driver's record-mover
arm (#665): mbx/mbx.c's CTRL_MBX_DMA_BASE arms and plat/mbx_dma.h, each
caught by the unit arm's test of the driver as the split image builds it,
over a register model of the mover (test_mbx_dma_driver.cpp).
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import Mutant

MBX_C = "mbx/mbx.c"
MBX_DMA_H = "plat/mbx_dma.h"
RX_MOVE = "\tif (!mbx_dma_move(rx_base[ch], rx_words[ch], (uint32_t)tail + MBX_RX_HDR_WORDS, f->bytes, len, false)) {\n"
TX_MOVE = "\t\tif (!mbx_dma_move(tx_base[ch], tx_words[ch], at, frame, len, true)) {\n\t\t\treturn MBX_STATUS_BAD;\n"

MUTANTS = (
    Mutant("mover-receive-error-trusted", MBX_C, RX_MOVE, RX_MOVE.replace("false)) {", "false) && false) {"),
           "unit", "MbxDma.R2AMoveEndingInErrorResynchronises", "R2 a move that ends in ERR leaves no record"),
    Mutant("mover-receive-index-at-the-header", MBX_C, RX_MOVE, RX_MOVE.replace(" + MBX_RX_HDR_WORDS,", ","),
           "unit", "MbxDma.R1ARecordsPayloadIsMovedAndReleased", "R1 the move starts at the payload's first ring word"),
    Mutant("mover-transmit-error-committed", MBX_C, TX_MOVE,
           TX_MOVE.replace("\t\t\treturn MBX_STATUS_BAD;\n", "\t\t\t;\n"),
           "unit", "MbxDma.T2AMoveEndingInErrorIsNotCommitted", "T2 a move that ends in ERR is refused"),
    Mutant("mover-transmit-frame-off-a-word-moved", MBX_C, "\tif (((uintptr_t)frame & 3u) == 0u) {\n" + TX_MOVE,
           "\tif (true) {\n" + TX_MOVE,
           "unit", "MbxDma.T3AFrameOffAWordTakesTheWordLoop", "T3 a frame off a word takes the word loop"),
    Mutant("mover-status-read-once", MBX_DMA_H, "\t} while ((status & MBX_DMA_STATUS_BUSY) != 0u);\n",
           "\t} while (false);\n",
           "unit", "MbxDma.R1ARecordsPayloadIsMovedAndReleased", "R1 the driver polls STATUS until BUSY falls"),
    Mutant("mover-error-ignored", MBX_DMA_H, "\treturn (status & MBX_DMA_STATUS_ERR) == 0u;\n", "\treturn true;\n",
           "unit", "MbxDma.R2AMoveEndingInErrorResynchronises", "R2 a move that ends in ERR leaves no record",
           (("unit", "MbxDma.T2AMoveEndingInErrorIsNotCommitted", "T2 a move that ends in ERR is refused"),)),
    Mutant("mover-ring-size-unshifted", MBX_DMA_H, "((words - 1u) << MBX_DMA_CFG_MASK_LSB)", "(words - 1u)",
           "unit", "MbxDma.R1ARecordsPayloadIsMovedAndReleased", "R1 CFG names the ring's base and size"),
    Mutant("mover-direction-dropped", MBX_DMA_H, "(to_ring ? MBX_DMA_CMD_TO_RING : 0u)", "(to_ring ? 0u : 0u)",
           "unit", "MbxDma.T1AFrameOnAWordIsMovedAndCommitted",
           "T1 the move runs memory to the ring from the payload's first word"),
)
