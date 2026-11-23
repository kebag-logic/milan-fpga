# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's ledgered points (#665): each override's own image, the images it must refuse, the
planted ledgers that widen one, and the out-of-context mapper's override.

`ctrl_memory.LEDGERED` lets four images plan past the 56-RAMB36 budget, each only as its own point, under #665's
documented memory exceptions and the owner's rule of 2026-11-15 (#923's ruling of 2026-11-16): at 8x8 with two
interfaces the size fixture's at 60.5 RAMB36 (59.0 before GET_AS_PATH's read composed with SRP's Talker declarations,
#897, 59.5 before the map edits' commit through the EDIT window, #923, 60.0 before the largest legal record's cut,
#665) and the target platform's at 63.5 (60.5, the
owner's decision's cap of 2026-11-12, with SRP's Talker declarations, #895, and AECP's REBOOT, #871, 61.0 with the PHY
poll and its advertisement, #919, 61.5 on the composed flip train, #665, 62.0 with the commit, #923, 62.5 with the
StreamIDs held with their latest Talker kind, #925, 63.0 with each AAF Stream Input's format written into its
receive-monitor context, #946, and 63.5 with the SRP drain's charge, #977), and the
target platform's 8x8 image with one interface, a product image, at 59.0 (56.5 with the PHY poll, 57.0 on the composed
train, 57.5 with the commit, 58.0 with the largest legal record's cut and the hot list relearned on it, 59.0 with
lwSRP's one-interface options and the drain's charge, #977), and the size fixture's 8x8 image with one interface at
56.5 with them (#977); each is refused half a tile past. A measurement names its point, and the product SoC build
plans an image at the point whose symbols it carries (`ctrl_memory.own_point`; #665's ruling of 2026-11-17 keeps it
for the composed train). A `Case` here is what the ledger reads of one image. test_ctrl_memory.py writes each as an
ELF, through the `write` callable every function here takes, and grades what these return.
syn/ooc/ctrl_memory_ooc.py maps the platform's point only through `--ledgered`, so the ledger can map it
(#665 S9); `mapper_arms` grades that override and plants three defects in it.
"""

from __future__ import annotations

import contextlib
import dataclasses
import importlib
import io
import json
import shutil
import sys
import types
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import NamedTuple

import ctrl_memory

STAGE_1X1, STAGE_8X8 = 3454, 13594
FIXTURE, PLATFORM, PRODUCT = "8x8-two-interfaces", "platform-8x8-two-interfaces", "platform-8x8-one-interface"
#: The size fixture's 8x8 image with one interface (#977).
FIXTURE_ONE = "8x8-one-interface"
#: sizeof(struct ctrl_plat) in the platform's image at each point (plat/ctrl_plat.h), as ctrl_plat_image.py links
#: it: 1x1 with one and two interfaces, 8x8 with one and two.
PLAT_1X1_1, PLAT_1X1_2, PLAT_8X8_1, PLAT_8X8_2 = 18_112, 19_776, 19_008, 21_568


class Case(NamedTuple):
    """What the ledger reads of an image, None leaving a symbol out: `nvm_stage`'s size, the size fixture's
    `image_allocation` in interfaces (8 bytes each), the platform's `ctrl_plat` size; and the RAMB36 it plans."""

    stage: int
    interfaces: int | None
    plat: int | None
    tiles: float


#: Each ledgered point's own image, at its ledgered tiles.
OWN = {FIXTURE: Case(STAGE_8X8, 2, None, 60.5), PLATFORM: Case(STAGE_8X8, None, PLAT_8X8_2, 63.5),
       PRODUCT: Case(STAGE_8X8, None, PLAT_8X8_1, 59.0), FIXTURE_ONE: Case(STAGE_8X8, 1, None, 56.5)}
#: What the ledger must hold for each: the symbols that make an image that point, and its tiles.
HELD = {FIXTURE: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("image_allocation", 16)), 60.5),
        PLATFORM: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("ctrl_plat", PLAT_8X8_2)), 63.5),
        PRODUCT: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("ctrl_plat", PLAT_8X8_1)), 59.0),
        FIXTURE_ONE: (((ctrl_memory.STAGE_SYMBOL, STAGE_8X8), ("image_allocation", 8)), 56.5)}
#: (what, override, image), each refused by `budget`: the point half a tile past its tiles, its image's other
#: points at its tiles and within the budget, the other override's image, an image carrying one of its two
#: symbols, and names the ledger does not hold.
REFUSED = (
    ("its own image at 61.0 RAMB36, half a tile past its 60.5", FIXTURE, OWN[FIXTURE]._replace(tiles=61.0)),
    ("the size fixture's 1x1 one-interface image at 60.5", FIXTURE, Case(STAGE_1X1, 1, None, 60.5)),
    ("the size fixture's 1x1 two-interface image at 60.5", FIXTURE, Case(STAGE_1X1, 2, None, 60.5)),
    ("the size fixture's 8x8 one-interface image at 60.5", FIXTURE, Case(STAGE_8X8, 1, None, 60.5)),
    ("its own image at 57.0 RAMB36, half a tile past its 56.5", FIXTURE_ONE, OWN[FIXTURE_ONE]._replace(tiles=57.0)),
    ("the size fixture's 1x1 one-interface image at 56.5", FIXTURE_ONE, Case(STAGE_1X1, 1, None, 56.5)),
    ("the size fixture's 8x8 two-interface image at 56.5", FIXTURE_ONE, OWN[FIXTURE]._replace(tiles=56.5)),
    ("the platform's 8x8 one-interface image at 56.5", FIXTURE_ONE, OWN[PRODUCT]._replace(tiles=56.5)),
    ("an 8x8 image with no image_allocation at 56.5", FIXTURE_ONE, Case(STAGE_8X8, None, None, 56.5)),
    ("an 8x8 image with no image_allocation at 60.5", FIXTURE, Case(STAGE_8X8, None, None, 60.5)),
    ("the size fixture's 1x1 one-interface image within the budget", FIXTURE, Case(STAGE_1X1, 1, None, 56.0)),
    ("the platform's 8x8 two-interface image at 60.5", FIXTURE, OWN[PLATFORM]._replace(tiles=60.5)),
    ("its own image at 64.0 RAMB36, half a tile past its 63.5", PLATFORM, OWN[PLATFORM]._replace(tiles=64.0)),
    ("the platform's 1x1 one-interface image at 63.5", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_1, 63.5)),
    ("the platform's 1x1 two-interface image at 63.5", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_2, 63.5)),
    ("the platform's 8x8 one-interface image at 63.5", PLATFORM, Case(STAGE_8X8, None, PLAT_8X8_1, 63.5)),
    ("an image with the point's ctrl_plat and the 1x1 stage at 63.5", PLATFORM,
     Case(STAGE_1X1, None, PLAT_8X8_2, 63.5)),
    ("an 8x8 image with no ctrl_plat at 63.5", PLATFORM, Case(STAGE_8X8, None, None, 63.5)),
    ("the platform's 1x1 one-interface image within the budget", PLATFORM, Case(STAGE_1X1, None, PLAT_1X1_1, 56.0)),
    ("the size fixture's 8x8 two-interface image at 63.5", PLATFORM, OWN[FIXTURE]._replace(tiles=63.5)),
    ("its own image at 59.5 RAMB36, half a tile past its 59.0", PRODUCT, OWN[PRODUCT]._replace(tiles=59.5)),
    ("the platform's 1x1 one-interface image at 59.0", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_1, 59.0)),
    ("the platform's 1x1 two-interface image at 59.0", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_2, 59.0)),
    ("the platform's 8x8 two-interface image at 59.0", PRODUCT, OWN[PLATFORM]._replace(tiles=59.0)),
    ("an image with the point's ctrl_plat and the 1x1 stage at 59.0", PRODUCT,
     Case(STAGE_1X1, None, PLAT_8X8_1, 59.0)),
    ("an 8x8 image with no ctrl_plat at 59.0", PRODUCT, Case(STAGE_8X8, None, None, 59.0)),
    ("the size fixture's 8x8 one-interface image at 59.0", PRODUCT, Case(STAGE_8X8, 1, None, 59.0)),
    ("the size fixture's 8x8 two-interface image, a name the ledger does not hold", "1x1-one-interface",
     OWN[FIXTURE]),
    ("the image of the point it names, a name the ledger does not hold", "1x1-one-interface",
     Case(STAGE_1X1, 1, None, 56.5)),
    ("the platform's 8x8 two-interface image, a name the ledger does not hold", "platform-1x1-one-interface",
     OWN[PLATFORM]),
    ("the platform's 1x1 one-interface image, a name the ledger does not hold", "platform-1x1-one-interface",
     Case(STAGE_1X1, None, PLAT_1X1_1, 56.5)),
)


def refusals(write: Callable[[Case], Path]) -> list[tuple[str, str, Callable[[], object]]]:
    """The `budget` rows of test_ctrl_memory.refusal_arms for the ledger: each point's own image planned without
    its override, then every REFUSED case under its override. Each attempt writes its image when it runs."""
    def attempt(case: Case, name: str | None = None) -> Callable[[], object]:
        """Plan `case` under the override `name`, looking `ctrl_memory` up when it runs, so a mutant is graded."""
        return lambda: ctrl_memory.plan(ctrl_memory.read_elf(write(case)), ledgered=name)
    return [*(("budget", f"the {name} point's image, {own.tiles} RAMB36, planned without its override", attempt(own))
              for name, own in OWN.items()),
            *(("budget", f"the {name} point's image with a ctrl_plat of another size, planned without an override",
               attempt(own._replace(plat=own.plat + 64))) for name, own in OWN.items() if name == PRODUCT),
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


def product_facts(write: Callable[[Case], Path], build: Callable[[Path], object]) -> Iterator[tuple[bool, str]]:
    """(holds, what): the product SoC build (`build`: milan_soc.add_ctrl_memory on a written image, its plan or the
    Refusal it raised) plans the product image at its entry's tiles by its symbols, and refuses it half a tile past
    and with a ctrl_plat of another size, each by `budget`."""
    own = OWN[PRODUCT]
    got = build(write(own))
    yield ((getattr(got, "ledgered", None), getattr(got, "tiles", None)) == (PRODUCT, own.tiles),
           f"the product SoC build plans the {PRODUCT} point's image at its {own.tiles} RAMB36 by its symbols ({got})")
    for what, case in (("half a tile past", own._replace(tiles=own.tiles + 0.5)),
                       ("with a ctrl_plat of another size", own._replace(plat=own.plat + 64))):
        got = build(write(case))
        yield (isinstance(got, ctrl_memory.Refusal) and got.rule == "budget",
               f"the product SoC build refuses the {PRODUCT} point's image {what} ({got})")


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
             ("the platform's entry at 64.0 RAMB36", PLATFORM, {"tiles": 64.0}),
             ("the size fixture's entry without image_allocation", FIXTURE, {"symbols": (stage,)}),
             ("the size fixture's entry at the platform's 63.5", FIXTURE, {"tiles": 63.5}),
             ("the product entry without ctrl_plat", PRODUCT, {"symbols": (stage,)}),
             ("the product entry at the 1x1 one-interface ctrl_plat and stage", PRODUCT,
              {"symbols": ((ctrl_memory.STAGE_SYMBOL, STAGE_1X1), ("ctrl_plat", PLAT_1X1_1))}),
             ("the product entry at 59.5 RAMB36", PRODUCT, {"tiles": 59.5}),
             ("the product entry at the two-interface ctrl_plat", PRODUCT,
              {"symbols": (stage, ("ctrl_plat", PLAT_8X8_2))}),
             ("the one-interface fixture's entry without image_allocation", FIXTURE_ONE, {"symbols": (stage,)}),
             ("the one-interface fixture's entry at the two-interface image_allocation", FIXTURE_ONE,
              {"symbols": (stage, ("image_allocation", 16))}),
             ("the one-interface fixture's entry at 57.0 RAMB36", FIXTURE_ONE, {"tiles": 57.0}))
    return [(what, {**held, name: dataclasses.replace(held[name], **change)}) for what, name, change in edits]


#: Each planted defect of the mapper's override: (what, the edit of ctrl_memory_ooc.main, its replacement).
_OVERRIDE = "ledgered=points.get(tag))"
MAPPER_MUTANTS = (("the mapper's override ignored", _OVERRIDE, "ledgered=None)"),
                  ("the mapper's override on every image", _OVERRIDE, "ledgered=next(iter(points.values()), None))"),
                  ("the mapper's stray override accepted", "if stray:", "if False:"))


def mapper() -> types.ModuleType:
    """syn/ooc/ctrl_memory_ooc.py, imported when first asked for: it needs LiteX, which nothing else here does."""
    path = str(Path(__file__).resolve().parents[2] / "syn/ooc")
    if path not in sys.path:
        sys.path.insert(0, path)
    return importlib.import_module("ctrl_memory_ooc")


def _mapped(tmp: Path, label: str, *argv: str) -> tuple[object, dict]:
    """The mapper's main, looked up when it runs, on argv into its own directory: (exit status, its plans)."""
    out = tmp / f"ooc-{label}"
    shutil.rmtree(out, ignore_errors=True)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            status: object = mapper().main([str(out), *argv])
        except SystemExit as exc:     # argparse refuses an override whose tag names no image by exiting
            status = exc.code
    plans = out / "ctrl_memory_plan.json"
    return status, json.loads(plans.read_text()) if plans.exists() else {}


def mapper_facts(write: Callable[[Case], Path], tmp: Path) -> Iterator[tuple[bool, str]]:
    """(holds, what): the mapper refuses the platform's point without `--ledgered`, maps it at its tiles with it
    beside an image of exactly the budget planned with no override, and refuses the override on that other image
    and on a tag that names no image, each exit 2."""
    own, within = OWN[PLATFORM], write(Case(STAGE_1X1, None, None, 56.0))
    status, _ = _mapped(tmp, "bare", f"p={write(own)}")
    yield status == 2, f"the mapper refuses the {PLATFORM} image without --ledgered (exit {status})"
    status, plans = _mapped(tmp, "held", f"w={within}", f"p={write(own)}", "--ledgered", f"p={PLATFORM}")
    held = {tag: (plan.get("tiles"), plan.get("ledgered")) for tag, plan in plans.items()}
    yield (status == 0 and held == {"w": (56.0, None), "p": (own.tiles, PLATFORM)},
           f"--ledgered p={PLATFORM} maps that image at {own.tiles} RAMB36 and the other at 56.0 with no override "
           f"(exit {status}, {held})")
    for label, tag, what in (("other", "w", "on another image"), ("stray", "x", "whose tag names no image")):
        status, _ = _mapped(tmp, label, f"w={within}", "--ledgered", f"{tag}={PLATFORM}")
        yield status == 2, f"the mapper refuses the {PLATFORM} override {what} (exit {status})"


def mapper_arms(problems: list[str], check: Callable[[list[str], bool, str], None], tmp: Path,
                write: Callable[[Case], Path], rebuild: Callable[[str, str], Callable[..., object]]) -> None:
    """The mapper's facts through test_ctrl_memory.py's `check`; then, only when every fact held, each
    MAPPER_MUTANTS edit of its main, rebuilt by `rebuild(old, new)`, must turn a fact red."""
    before = len(problems)
    for holds, what in mapper_facts(write, tmp):
        check(problems, holds, what)
    if len(problems) != before:
        check(problems, False, "the mapper's mutants are not graded: its facts fail unmutated")
        return
    module = mapper()
    original = module.main
    for name, old, new in MAPPER_MUTANTS:
        try:
            rebuilt = rebuild(old, new)
        except LookupError as exc:
            check(problems, False, f"MUTANT '{name}': {exc}")
            continue
        module.main = rebuilt
        try:
            red = [what for holds, what in mapper_facts(write, tmp) if not holds]
        except Exception as exc:     # a mutant that breaks the mapper outright is caught too
            red = [f"the arm raised {type(exc).__name__}: {exc}"]
        finally:
            module.main = original
        check(problems, bool(red), f"MUTANT '{name}' (ooc override) is caught by the mapper's facts: "
                                   f"{red[0] if red else 'nothing went red'}")
