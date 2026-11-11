# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""mbx_dma_mutants.py - planted defects in the mailbox driver's record-mover
arm (#665): mbx/mbx.c's CTRL_MBX_DMA_BASE arms and plat/mbx_dma.h, and
the notice's fan port over them (aecp/aecp_mbx.c), each caught by the unit
arm's test of the driver as the split image builds it, over a register
model of the mover (test_mbx_dma_driver.cpp).
ctrl_mutants.py appends this table to its own.
"""

from __future__ import annotations

from ctrl_mutant import Mutant

MBX_C = "mbx/mbx.c"
MBX_DMA_H = "plat/mbx_dma.h"
RX_MOVE = "\tif (!mbx_dma_move(rx_base[ch], rx_words[ch], (uint32_t)tail + MBX_RX_HDR_WORDS, f->bytes, len, false)) {\n"
TX_WAIT = "\tif ((moving & TX_MOVED) != 0u && !mbx_dma_wait()) {\n\t\treturn false;\n\t}\n"
AECP_MBX_C = "aecp/aecp_mbx.c"
TX_MOVE = "\t\tmbx_dma_start(base, words, at, frame, len, true);\n"

MUTANTS = (
    Mutant("mover-receive-error-trusted", MBX_C, RX_MOVE, RX_MOVE.replace("false)) {", "false) && false) {"),
           "unit", "MbxDma.R2AMoveEndingInErrorResynchronises", "R2 a move that ends in ERR leaves no record"),
    Mutant("mover-receive-index-at-the-header", MBX_C, RX_MOVE, RX_MOVE.replace(" + MBX_RX_HDR_WORDS,", ","),
           "unit", "MbxDma.R1ARecordsPayloadIsMovedAndReleased", "R1 the move starts at the payload's first ring word"),
    Mutant("mover-transmit-error-committed", MBX_C, TX_WAIT, "\t(void)mbx_dma_wait();\n",
           "unit", "MbxDma.T2AMoveEndingInErrorIsNotCommitted", "T2 a move that ends in ERR is refused"),
    # a record's commit judges its own move alone (#665): the earlier rule waited on the mover for every record, so a
    # frame off a word inherited the ERR a move before it left
    Mutant("mover-commit-judges-every-record", MBX_C, "(moving & TX_MOVED) != 0u && !mbx_dma_wait()",
           "!mbx_dma_wait()", "unit", "MbxDma.T4ARecordTheWordLoopWroteInheritsNoEarlierMovesError",
           "T4 a frame off a word sent after a failed move is committed"),
    Mutant("mover-move-not-held-its-own", MBX_C, "\t\tmoving |= TX_MOVED;\n", "",
           "unit", "MbxDma.T2AMoveEndingInErrorIsNotCommitted", "T2 a move that ends in ERR is refused"),
    # a failed move reported for the record it carried: the earlier rule refused the record after it
    Mutant("mover-lost-record-reported-as-bad", MBX_C, "\t\treturn MBX_STATUS_LOST;\n",
           "\t\treturn MBX_STATUS_BAD;\n", "unit", "MbxDma.T2AMoveEndingInErrorIsNotCommitted",
           "T2 a begin that finds the record before it ended in ERR reports it lost",
           (("unit", "MbxDma.T5TheNoticeFanPortReportsALostFrameForItself",
             "T5 the fan after a frame whose move failed reports that frame lost"),)),
    Mutant("mover-fan-lost-reported-as-refused", AECP_MBX_C,
           "status == MBX_STATUS_LOST ? AECP_FAN_LOST : AECP_FAN_REFUSED", "AECP_FAN_REFUSED",
           "unit", "MbxDma.T5TheNoticeFanPortReportsALostFrameForItself",
           "T5 the fan after a frame whose move failed reports that frame lost"),
    # fan_end discarding its commit's result, the earlier rule
    Mutant("mover-fan-end-commit-discarded", AECP_MBX_C,
           "\tif (!mbx_tx_commit(MBX_CH_AECP)) {\n\t\treturn AECP_FAN_LOST;\n\t}\n",
           "\t(void)mbx_tx_commit(MBX_CH_AECP);\n", "unit", "MbxDma.T5TheNoticeFanPortReportsALostFrameForItself",
           "T5 fan_end reports a last frame whose move failed lost"),
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
