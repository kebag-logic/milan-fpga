# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's ledgered points (#665): each override's own image, the images it must refuse, and the
planted ledgers that widen one.

`ctrl_memory.LEDGERED` lets two images plan past the 56-RAMB36 budget, both at 8x8 with two interfaces, each
only by its own name: the size fixture's at 57.5 RAMB36 (rulings 6412739248 and 6425357821) and the target
platform's at 59.0 (ruling 6505997821). A `Case` here is what the ledger reads of one image. test_ctrl_memory.py
writes each as an ELF, through the `write` callable every function here takes, and grades what these return.
"""

from __future__ import annotations

import contextlib
import dataclasses
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

import ctrl_memory

STAGE_1X1, STAGE_8X8 = 3344, 13264
FIXTURE, PLATFORM = "8x8-two-interfaces", "platform-8x8-two-interfaces"
#: sizeof(struct ctrl_plat) in the platform's image at each point (plat/ctrl_plat.h), as ctrl_plat_image.py links
#: it: 1x1 with one and two interfaces, 8x8 with one and two.
PLAT_1X1_1, PLAT_1X1_2, PLAT_8X8_1, PLAT_8X8_2 = 18_432, 19_928, 19_088, 21_240


class Case(NamedTuple):
    """What the ledger reads of an image, None leaving a symbol out: `nvm_stage`'s size, the size fixture's
    `image_allocation` in interfaces (8 bytes each), the platform's `ctrl_plat` size; and the RAMB36 it plans."""

    stage: int
    interfaces: int | None
    plat: int | None
    tiles: float


#: Each ledgered point's own image, at its ledgered tiles.
OWN = {FIXTURE: Case(STAGE_8X8, 2, None, 57.5), PLATFORM: Case(STAGE_8X8, None, PLAT_8X8_2, 59.0)}
#: What the ledger must hold for each: the symbols that make an image that point, and its tiles.
HELD = {FIXTURE: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("image_allocation", 16)), 57.5),
        PLATFORM: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("ctrl_plat", PLAT_8X8_2)), 59.0)}
#: (what, override, image), each refused by `budget`: the point half a tile past its tiles, its image's other
#: points at its tiles and within the budget, the other override's image, an image carrying one of its two
#: symbols, and names the ledger does not hold.
REFUSED = (
    ("its own image at 58.0 RAMB36, half a tile past its 57.5", FIXTURE, OWN[FIXTURE]._replace(tiles=58.0)),
    ("the size fixture's 1x1 one-interface image at 57.5", FIXTURE, Case(STAGE_1X1, 1, None, 57.5)),
    ("the size fixture's 1x1 two-interface image at 57.5", FIXTURE, Case(STAGE_1X1, 2, None, 57.5)),
    ("the size fixture's 8x8 one-interface image at 57.5", FIXTURE, Case(STAGE_8X8, 1, None, 57.5)),
    ("an 8x8 image with no image_allocation at 57.5", FIXTURE, Case(STAGE_8X8, None, None, 57.5)),
    ("the size fixture's 1x1 one-interface image within the budget", FIXTURE, Case(STAGE_1X1, 1, None, 56.0)),
    ("the platform's 8x8 two-interface image at 57.5", FIXTURE, OWN[PLATFORM]._replace(tiles=57.5)),
    ("its own image at 59.5 RAMB36, half a tile past its 59.0", PLATFORM, OWN[PLATFORM]._replace(tiles=59.5)),
    ("the platform's 1x1 one-interface image at 59.0", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_1, 59.0)),
    ("the platform's 1x1 two-interface image at 59.0", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_2, 59.0)),
    ("the platform's 8x8 one-interface image at 59.0", PLATFORM, Case(STAGE_8X8, None, PLAT_8X8_1, 59.0)),
    ("an image with the point's ctrl_plat and the 1x1 stage at 59.0", PLATFORM,
     Case(STAGE_1X1, None, PLAT_8X8_2, 59.0)),
    ("an 8x8 image with no ctrl_plat at 59.0", PLATFORM, Case(STAGE_8X8, None, None, 59.0)),
    ("the platform's 1x1 one-interface image within the budget", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_1, 56.0)),
    ("the size fixture's 8x8 two-interface image at 59.0", PLATFORM, OWN[FIXTURE]._replace(tiles=59.0)),
    ("the size fixture's 8x8 two-interface image, a name the ledger does not hold", "8x8-one-interface",
     OWN[FIXTURE]),
    ("the image of the point it names, a name the ledger does not hold", "8x8-one-interface",
     Case(STAGE_8X8, 1, None, 57.5)),
    ("the platform's 8x8 two-interface image, a name the ledger does not hold", "platform-8x8-one-interface",
     OWN[PLATFORM]),
)


def refusals(write: Callable[[Case], Path]) -> list[tuple[str, str, Callable[[], object]]]:
    """The `budget` rows of test_ctrl_memory.refusal_arms for the ledger: each point's own image planned without
    its override, then every REFUSED case under its override. Each attempt writes its image when it runs."""
    def attempt(case: Case, name: str | None = None) -> Callable[[], object]:
        """Plan `case` under the override `name`, looking `ctrl_memory` up when it runs, so a mutant is graded."""
        return lambda: ctrl_memory.plan(ctrl_memory.read_elf(write(case)), ledgered=name)
    return [*(("budget", f"the {name} point's image, {own.tiles} RAMB36, planned without its override", attempt(own))
              for name, own in OWN.items()),
            *(("budget", f"the {name} override on {what}", attempt(case, name)) for what, name, case in REFUSED)]


def facts(write: Callable[[Case], Path]) -> Iterator[tuple[bool, str]]:
    """(holds, what): each override plans its own image to its tiles, and `plan --ledgered-point` accepts that
    image and refuses, exit 2, every REFUSED case under the same override."""
    for name, own in OWN.items():
        what = f"the {name} override plans its own point's image"
        try:
            summary = ctrl_memory.plan(ctrl_memory.read_elf(write(own)), ledgered=name).summary()
        except Exception as exc:     # a refusal here is the failure this fact exists to name
            yield False, f"{what}: raised {type(exc).__name__} ({exc})"
            continue
        got = tuple(summary.get(key) for key in ("tiles", "budget_tiles", "ledgered", "ledgered_tiles"))
        yield got == (own.tiles, 56, name, own.tiles), (f"{what}: {own.tiles} RAMB36, against the 56-RAMB36 budget "
                                                        f"and its ledgered {own.tiles} ({got})")
        others = [case for _, override, case in REFUSED if override == name]
        codes = []
        for case in (own, *others):
            with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
                codes.append(ctrl_memory.main(["plan", str(write(case)), "--ledgered-point", name]))
        yield codes == [0] + [2] * len(others), (f"`plan --ledgered-point {name}` accepts its point's image and "
                                                 f"refuses the {len(others)} cases its override must (exit codes "
                                                 f"{codes})")


def planted() -> list[tuple[str, dict[str, ctrl_memory.Ledgered]]]:
    """The ledger as it is, each copy with one entry widened to another point or image, or past its ruled tiles.

    Every one must turn the test red with the ledger's pin set aside, by a fact above or a REFUSED row.
    """
    held = ctrl_memory.LEDGERED
    stage = (ctrl_memory.STAGE_SYMBOL, STAGE_8X8)
    edits = (("the platform's entry without its staging buffer", PLATFORM, {"symbols": (("ctrl_plat", PLAT_8X8_2),)}),
             ("the platform's entry without ctrl_plat", PLATFORM, {"symbols": (stage,)}),
             ("the platform's entry at the 8x8 one-interface ctrl_plat", PLATFORM,
              {"symbols": (stage, ("ctrl_plat", PLAT_8X8_1))}),
             ("the platform's entry at 59.5 RAMB36", PLATFORM, {"tiles": 59.5}),
             ("the size fixture's entry without image_allocation", FIXTURE, {"symbols": (stage,)}),
             ("the size fixture's entry at the platform's 59.0", FIXTURE, {"tiles": 59.0}))
    return [(what, {**held, name: dataclasses.replace(held[name], **change)}) for what, name, change in edits]
