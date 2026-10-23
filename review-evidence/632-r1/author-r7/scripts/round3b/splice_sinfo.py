#!/usr/bin/env python3
"""Splice the processor head's E_SINFO block into the pinned generator.

usage: splice_sinfo.py HEAD_GEN PIN_GEN OUT
Copies PIN_GEN to OUT with its `place(E_SINFO, [` ... `])` block (and any
assert lines right after it) replaced by HEAD_GEN's. Each block must occur
exactly once in each file, so nothing else of the pinned generator moves.
"""
import re
import sys
from pathlib import Path

BLOCK = re.compile(r"^place\(E_SINFO, \[\n.*?^\]\)\n(?:assert rom\[E_SINFO[^\n]*\n)*",
                   re.M | re.S)


def block(text: str, what: str) -> str:
    found = BLOCK.findall(text)
    if len(found) != 1:
        raise SystemExit(f"{what}: E_SINFO block found {len(found)} times, expected 1")
    return found[0]


head = Path(sys.argv[1]).read_text()
pin = Path(sys.argv[2]).read_text()
new, old = block(head, "head"), block(pin, "pin")
Path(sys.argv[3]).write_text(pin.replace(old, new, 1))
print(f"spliced: {old.count(chr(10))} lines -> {new.count(chr(10))} lines")
