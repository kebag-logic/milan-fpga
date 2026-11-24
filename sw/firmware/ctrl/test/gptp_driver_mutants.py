# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the mailbox driver's software gPTP publication and timestamp decoding."""

from ctrl_mutant import Mutant


MUTANTS = (
    Mutant("pub-gptp-generation-written-twice", "mbx/mbx.c", "if (k != state) {", "if (true) {",
           "unit", "DriverUnit.GptpPublicationCommitsAfterItsIdentityWords",
           "the generation commits the complete identity on its own interface"),
    Mutant("timestamp-high-word-shifted", "mbx/mbx.c",
           "MBX_EV_TIMESTAMP_W3_NS_HI_WIDTH) << 32)", "MBX_EV_TIMESTAMP_W3_NS_HI_WIDTH) << 16)",
           "unit", "DriverUnit.TimestampEventDecodesFlagsAndBothTimeWordsAcrossWrap",
           "the timestamp keeps all 64 time bits"),
)
