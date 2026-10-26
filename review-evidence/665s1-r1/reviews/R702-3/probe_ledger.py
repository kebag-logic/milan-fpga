#!/usr/bin/env python3
"""Probe: plant defects into the ledgered-point override and require test_ctrl_memory's
rules arm (check_arms, which runs ledger_arms and every refusal_arms row) to turn red.

Each mutant is rebuilt by test_ctrl_memory's own `mutated` (one edit, matching once, in the
function's own source) and graded by its own `mutant_arms`, against the arm passing
unmutated in the same run. Not added to the tree's MUTANTS: docs/testing/TESTING.md counts
those, and that file is outside this lane.

Usage: <litex python> ledger_mutants.py <tree>
"""
import contextlib
import sys
import tempfile
from functools import partial
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/litex"))
import test_ctrl_memory as t  # noqa: E402

LEDGER = '"8x8-two-interfaces"'
CARRIED = "carried = {symbol: image.symbols.get(symbol, (0, None))[1] for symbol, _ in point.symbols}"
ROWS = (
    ("the override applies to every image", "budget", "ctrl_memory", "ledgered_tiles",
     "if carried != dict(point.symbols):", "if False:", "checks"),
    ("the override reads the shape only", "budget", "ctrl_memory", "ledgered_tiles", CARRIED,
     "carried = {symbol: image.symbols.get(symbol, (0, None))[1] if symbol == STAGE_SYMBOL else size "
     "for symbol, size in point.symbols}", "checks"),
    ("the override reads the interfaces only", "budget", "ctrl_memory", "ledgered_tiles", CARRIED,
     "carried = {symbol: image.symbols.get(symbol, (0, None))[1] if symbol != STAGE_SYMBOL else size "
     "for symbol, size in point.symbols}", "checks"),
    ("the override half a tile past its ledgered tiles", "budget", "ctrl_memory", "ledgered_tiles",
     "return point.tiles", "return point.tiles + 0.5", "checks"),
    ("an unknown name falls back to the ledgered point", "budget", "ctrl_memory", "ledgered_tiles",
     "point = LEDGERED.get(name)", f"point = LEDGERED.get(name, LEDGERED[{LEDGER}])", "checks"),
    ("the plan defaults to the override", "budget", "ctrl_memory", "plan",
     "ledgered: str | None = None) -> Plan:", f"ledgered: str | None = {LEDGER}) -> Plan:", "checks"),
    ("the override lifts the budget for every image", "budget", "ctrl_memory", "plan",
     "if ledgered is not None:\n        budget = ledgered_tiles(image, ledgered)",
     "if True:\n        budget = 57.0", "checks"),
    ("the SoC build takes the override", "budget", "milan_soc", "add_ctrl_memory",
     "soc.ctrl_plan = ctrl_memory.plan(soc.ctrl_image)",
     f"soc.ctrl_plan = ctrl_memory.plan(soc.ctrl_image, ledgered={LEDGER})", "checks"),
    ("the command line drops the override", "budget", "ctrl_memory", "main",
     "plan(image, ledgered=args.ledgered_point)", "plan(image)", "checks"),
    ("a second point in the ledger", "budget", "ctrl_memory", "ledgered_tiles",
     "point = LEDGERED.get(name)",
     "point = {**LEDGERED, '8x8-one-interface': Ledgered('8x8, one interface', "
     "((STAGE_SYMBOL, 13_264), ('image_allocation', 8)), 57.0, 'none')}.get(name)", "checks"),
)


def main() -> int:
    """The control first, then every mutant; exit 1 if the control fails or any mutant lives."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ledger-mutants-") as name:
        tmp = Path(name)
        print("-- control: the rules arm, unmutated")
        with contextlib.redirect_stdout(None):
            t.check_arms(problems, tmp)
        print(f"  control: {len(problems)} failure(s)")
        if problems:
            print("\n".join(problems))
            return 1
        t.MUTANTS = tuple(t.Mutant(*row) for row in ROWS)
        print(f"-- {len(t.MUTANTS)} planted mutants")
        t.mutant_arms(problems, tmp, green={"checks"})
        # A module constant, not a function: a second point added to LEDGERED itself.
        second = t.ctrl_memory.Ledgered("8x8, one interface", ((t.ctrl_memory.STAGE_SYMBOL, 13_264),
                                        ("image_allocation", 8)), 57.0, "none")
        caught: list[str] = []
        with t.patched(t.ctrl_memory, "LEDGERED", {**t.ctrl_memory.LEDGERED, "8x8-one-interface": second}), \
                contextlib.redirect_stdout(None):
            t.check_arms(caught, tmp)
        t.check(problems, bool(caught), "MUTANT 'a second point added to LEDGERED' (budget) is caught by the "
                                        f"checks arm: {caught[0] if caught else 'nothing went red'}")
    total = len(ROWS) + 1
    print(f"ledger_mutants: {total - len(problems)} of {total} caught")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
