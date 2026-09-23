#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned fix-sensitivity probes of the R228-F1 resolver change.

Copies a checkout to a disposable destination, replaces ONE exact snippet of
sw/builder/test_builder.py (it must occur exactly once), then runs the head's
gate 1b with the selected SDK mapped at the absolute selector. A mutation
whose gate stays green is a changed behaviour no control can see.

Usage: mutate_resolver.py <checkout> <scratch> <sdk-destination> <mutation> <out-dir>
"""

import shutil
import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    # _rv32_slot_mirror: back to the integer store list for its bail-out
    "RM1-slot-mirror-integer-only": (
        "        if rv32_store_bytes(mnem) is not None or \\\n"
        "                (rv32_memory_operand(args) and not rv32_is_load(mnem)) or \\\n"
        "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):\n",
        "        if mnem in (\"sw\", \"sh\", \"sb\") or \\\n"
        "                mnem in (\"call\", \"jal\", \"jalr\", \"tail\", \"jr\", \"ret\"):\n"),
    # the fail-closed default recognises only a displaced operand `N(reg)`
    "RM5-memory-operand-needs-displacement": (
        "RV32_MEM_BASE_RE = re.compile(r\"\\(\\s*([a-z0-9]+)\\s*\\)$\")",
        "RV32_MEM_BASE_RE = re.compile(r\"\\d\\(\\s*([a-z0-9]+)\\s*\\)$\")"),
    # a ranged store reported without its width
    "RM8-range-store-without-width": (
        "                                         held.hi + offset + width - 1)",
        "                                         held.hi + offset)"),
    # a symbol store forgets only the one word it starts in
    "RM11-sym-overlap-fixed-4": (
        "            _rv32_forget_overlap(state.mem, (\"sym\", held.name), at, width)",
        "            _rv32_forget_overlap(state.mem, (\"sym\", held.name), at, 4)"),
    # a frame store forgets only the one word it starts in
    "RM12-frame-overlap-fixed-4": (
        "            _rv32_forget_overlap(state.mem, (base,), offset, width)",
        "            _rv32_forget_overlap(state.mem, (base,), offset, 4)"),
}


def main() -> None:
    checkout, scratch, sdk, name, out = (Path(sys.argv[1]), Path(sys.argv[2]),
                                         Path(sys.argv[3]), sys.argv[4], Path(sys.argv[5]))
    old, new = MUTATIONS[name]
    copy = scratch / f"rm-{name}"
    if copy.exists():
        shutil.rmtree(copy)
    subprocess.run(["cp", "-a", str(checkout), str(copy)], check=True)
    target = copy / "sw/builder/test_builder.py"
    text = target.read_text()
    assert text.count(old) == 1, f"{name}: snippet occurs {text.count(old)} times"
    target.write_text(text.replace(old, new, 1))
    (out / f"{name}.diff").write_text(subprocess.run(
        ["git", "-C", str(copy), "diff"], capture_output=True, text=True).stdout)
    log = out / f"{name}.log"
    with log.open("w") as stream:
        run = subprocess.run([sys.executable, "-u", "sw/builder/test_firmware_compiler.py",
                              "--sdk-destination", str(sdk), "--audit",
                              str(scratch / f"rm-{name}-argv.jsonl")],
                             cwd=copy, stdout=stream, stderr=subprocess.STDOUT)
    with log.open("a") as stream:
        stream.write(f"exit={run.returncode}\n")
    print(f"{name} exit={run.returncode} ({'DETECTED' if run.returncode else 'UNDETECTED'})")


if __name__ == "__main__":
    main()
