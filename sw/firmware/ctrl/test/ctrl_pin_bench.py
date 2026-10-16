# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Execute stack-pin controls at the mailbox and counter Makefile entry points."""

import sys
from pathlib import Path

from ctrl_build import ROOT, Refusal


def bench_arms(makefiles: list[Path], clone: Path, work: Path, edited: str) -> list[tuple]:
    """For every target of every Makefile builder that reaches the stack in its dry run: run it in a scratch
    copy of its directory against the clone with wire.h poisoned, with no simulator; it must refuse on the pin
    check and never reach the poisoned header; each target that runs the pin check passes the clone
    unpoisoned. And the planted Makefile without the pin prerequisite."""
    from ctrl_pin import (BENCH_TIMEOUT_S, COUNTER_TARGETS, NO_SIMULATOR, POISON, UNPINNED,
                          make, makefile_findings, mirror, stack_targets)

    simulator = work / "no_simulator.py"
    simulator.write_text(NO_SIMULATOR, encoding="utf-8")

    def poison() -> None:
        """The clone's wire.h, which every firmware build reads, ends in an #error."""
        wire = clone / "include/wire.h"
        wire.write_text(wire.read_text(encoding="utf-8") + f"\n{POISON}\n", encoding="utf-8")

    def bench(makefile: Path, target: str) -> tuple[bool, str]:
        """The target run for real in a fresh scratch copy: accepted, and its verdict on the stack."""
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        rc, out = make(copy, f"STACK_DIR={clone}", f"VERILATOR={sys.executable} -I {simulator}", target,
                       timeout=BENCH_TIMEOUT_S)
        said = [ln for ln in out.splitlines() if "tsn-c-stack" in ln or "PIN-POISON" in ln]
        if "PIN-POISON" in out:
            return True, f"exit {rc}: compiled the poisoned header: {said[-1].strip()}"
        return rc == 0, f"exit {rc}: {said[-1].strip() if said else 'no pin verdict'}"

    def unpinned(plant: tuple = UNPINNED) -> tuple[bool, str]:
        """The planted Makefile, judged as the gate judges every Makefile builder."""
        makefile, old, new, _ = plant
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        text = copy.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"the planted Makefile control's anchor occurs {text.count(old)} times")
        copy.write_text(text.replace(old, new), encoding="utf-8")
        found = makefile_findings([copy], work / "unpinned")
        return not found, found[0] if found else "no finding"

    arms = []
    for makefile in makefiles:
        where = makefile.relative_to(ROOT).as_posix()
        reaching, pins, _ = stack_targets(makefile, clone)
        arms += [(f"{where} make {pin}, the pinned clone", lambda: None, lambda m=makefile, t=pin: bench(m, t), "")
                 for pin in pins]
        for target in reaching:
            arms.append((f"{where} make {target}, the stack's wire.h poisoned", poison,
                         lambda m=makefile, t=target: bench(m, t), edited + "include/wire.h"))
    arms.append((f"{UNPINNED[0].relative_to(ROOT).as_posix()} planted with {UNPINNED[3]} unpinned", lambda: None,
                 unpinned, f"{UNPINNED[3]} builds against tsn-c-stack without the pin check"))
    for target in COUNTER_TARGETS:
        plant = (ROOT / "tb/verilator/milan_dp/Makefile", f"{target}: | stack-pin\n", f"{target}:\n", target)
        needle = f"{target} lacks its required stack-pin prerequisite" if target == "counters" else \
            f"{target} builds against tsn-c-stack without the pin check"
        arms.append((f"milan_dp planted with {target} unpinned", lambda: None,
                     lambda p=plant: unpinned(p), needle))
    return arms
