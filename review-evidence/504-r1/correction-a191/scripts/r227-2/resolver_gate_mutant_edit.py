#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Apply one named fix-removal edit to a disposable test_builder.py copy.

Every anchor must occur exactly once, or the edit refuses.
Usage: resolver_gate_mutant_edit.py <test_builder.py> <mutant-id>
"""

import sys
from pathlib import Path

EDITS = {
    # setup control: no edit; the probe clone itself must pass the gate
    "R0-pristine": [],
    # control: the FP classes leave the table (the default then reports them
    # as unclassified); the PR's literal class probes must redden
    "R1-fp-classes-dropped": [(
        '                    "fsh": 2, "fsw": 4, "fsd": 8, "fsq": 16}',
        "                    }")],
    # control: the class fail-closed default is deleted
    "R3-unclassified-default-dropped": [(
        "    if rv32_memory_operand(args) and not rv32_is_load(mnem):\n"
        "        _rv32_forget_symbols(state)\n"
        "        return (\"store\", (Rv32Where(\"unclassified\", f\"{mnem} {ops}\"), None))\n",
        "")],
    # the ranged store's footprint shrinks back to its first byte
    "R5-range-footprint-width": [(
        "                                         held.hi + offset + width - 1)",
        "                                         held.hi + offset)")],
    # the slot-mirror walk forgets the non-integer store classes again
    "R6-mirror-integer-stores-only": [(
        "        if rv32_store_bytes(mnem) is not None or \\\n"
        "                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n"
        "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):",
        "        if mnem in (\"sw\", \"sh\", \"sb\") or \\\n"
        "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):")],
    # every AMO (and SC) is modelled as writing its rs2 into the slot
    "R10-amo-value-rs2": [(
        '    if mnem in ("sb", "sh", "sw") or mnem.startswith("amoswap."):\n'
        "        return state.get(args[-2])",
        '    if mnem in ("sb", "sh", "sw") or RV32_ATOMIC_STORE_RE.match(mnem):\n'
        "        return state.get(args[-2])")],
}


def main() -> int:
    path, mutant = Path(sys.argv[1]), sys.argv[2]
    text = path.read_text()
    for old, new in EDITS[mutant]:
        assert text.count(old) == 1, f"{mutant}: anchor count {text.count(old)}"
        text = text.replace(old, new)
    path.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
