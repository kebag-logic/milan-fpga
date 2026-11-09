# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's simulation map (#859): the 32x32 shape's image planned past the budget with every byte over
it owed to #640, the images that map and the split placement's must refuse, and the planted map that must be caught.

test_ctrl_memory.py runs `arms`, through the `check` callable it takes, beside its other arms.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from pathlib import Path

import ctrl_memory
from ctrl_memory_elf import write_elf

#: The simulation map the 32x32 shape links into and its identity: the SRP pool at the shape.
SIM_MAP = "32x32-two-interfaces"
RAM = ctrl_memory.RAM.origin


def simulation_elf(tmp: Path, arena: int, bss: int) -> Path:
    """A simulation image: a tile of code in rom, `bss` bytes of .bss and the stack in sram, and the two
    symbols that make it the 32x32 size fixture's (`arena` the SRP pool's size)."""
    path = tmp / f"sim-{arena}-{bss}.elf"
    path.write_bytes(write_elf(0, [
        (".text", 0, 0, bytes((i * 7 + 3) & 0xFF for i in range(ctrl_memory.TILE_BYTES)), False),
        (".bss", RAM, RAM, bss, True), (".stack", RAM + bss, RAM + bss, 8192, True)],
        {"_start": 4, "image_arena": arena, "image_allocation": 16}))
    return path


def simulation_facts(tmp: Path) -> list[tuple[bool, str]]:
    """The simulation map (ctrl_memory.SIMULATION): the 32x32 image is planned in its regions past the
    budget with every byte over it ledgered to #640, by region and by its largest objects; the same
    image is refused the split placement's map, and an image that is not the shape's the simulation map."""
    out = []
    shape = ctrl_memory.SIMULATION[SIM_MAP]
    big = simulation_elf(tmp, 144_832, 300_000)
    try:
        plan = ctrl_memory.plan(ctrl_memory.read_elf(big), simulation=SIM_MAP)
        owed = plan.summary().get("owed", {})
        out += [(plan.tiles > ctrl_memory.BUDGET_TILES and owed.get("over_bytes", 0) > 0
                 and owed.get("to", "").startswith("#640"),
                 f"the 32x32 image is planned past 56 RAMB36 with its bytes over owed to #640 ({plan.tiles}, {owed})"),
                (set(owed.get("regions", {})) == {"rom", "sram"} and 1 <= len(owed.get("largest", [])) <= 5,
                 "the ledger is by region and by the five largest objects")]
    except ctrl_memory.Refusal as exc:
        out.append((False, f"the 32x32 image is refused its simulation map: {exc}"))
    for label, attempt, words in (
            ("the 32x32 image without its simulation map",
             lambda: ctrl_memory.plan(ctrl_memory.read_elf(big)), "outside"),
            ("the 8x8 SRP pool's image on the simulation map",
             lambda: ctrl_memory.plan(ctrl_memory.read_elf(simulation_elf(tmp, 48_064, 300_000)),
                                      simulation=SIM_MAP), f"is for the {shape.shape} image alone")):
        try:
            attempt()
            out.append((False, f"{label}: planned"))
        except ctrl_memory.Refusal as exc:
            out.append((words in str(exc), f"{label}: refused by its words ({exc})"))
    out.append((ctrl_memory.regions(SIM_MAP) == (shape.rom, shape.ram) and ctrl_memory.regions() ==
                (ctrl_memory.ROM, ctrl_memory.RAM), "the shipped regions are the split placement's, unchanged"))
    return out


def arms(problems: list[str], tmp: Path, check: Callable[[list[str], bool, str], None]) -> None:
    """simulation_facts, then the map planted without its identity, which must turn a fact red."""
    for holds, what in simulation_facts(tmp):
        check(problems, holds, what)
    shipped = ctrl_memory.SIMULATION
    ctrl_memory.SIMULATION = {SIM_MAP: dataclasses.replace(shipped[SIM_MAP], symbols=())}
    try:
        red = [what for holds, what in simulation_facts(tmp) if not holds]
    finally:
        ctrl_memory.SIMULATION = shipped
    check(problems, bool(red),
          f"PLANTED simulation map without its identity is caught: {red[0] if red else 'nothing red'}")
