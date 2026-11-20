# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of SRP's StreamID and MAC comparison (#665, srp_mbx.c's same): an equality test of n bytes, byte
for byte, in the receive filter, the indications and the registrar walk.

srp_mutants.py plants them with the rest of its table: each must fail its named observable, never only a build.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

TEST = "Srp.AListenerIsASourcesOnlyForItsStreamIDByteForByte"
#: same's loop over the bytes.
LOOP = "    while (n != 0u) {\n        --n;\n        if (a[n] != b[n]) {\n            return false;\n"


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the comparison, built with srp_mutants.Defect."""
    return (
        # the last byte not compared: a sink's StreamID and a Talker's that differs in its unique ID's low byte are
        # one. A Listener's is told apart from a source's by that byte before same is called (sources_of; #665's
        # ruling of 2026-11-20, item 3), so this one is planted under a Talker's near miss of a bound sink.
        kind("same-skips-the-last-byte", "SrpWalk.StreamMatcherNearMissSwapAndImmediateWithdrawal", LOOP,
             LOOP.replace("    while (n != 0u) {\n", "    --n;\n    while (n != 0u) {\n"),
             "adapter.ifs[0].sinks[0].declared", suite="srp_walk.cpp"),
        # the first byte not compared: a StreamID whose talker MAC differs in its first byte is a source's
        kind("same-skips-the-first-byte", TEST, LOOP, LOOP.replace("while (n != 0u)", "while (n > 1u)"),
             "differs from source 0's in byte 0 alone"),
        # a difference read as equality: every StreamID is every source's
        kind("same-on-a-difference", TEST, LOOP, LOOP.replace("return false;", "return true;"),
             "differs from source 0's in byte 0 alone"),
    )
