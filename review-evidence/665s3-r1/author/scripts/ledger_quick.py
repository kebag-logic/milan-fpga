"""Run test_ctrl_memory.py's rules arm, its ledger plants and its ledgered_tiles mutants alone (a quick check,
not a gate). usage: ledger_quick.py CHECKOUT"""
import contextlib
import sys
import tempfile
from functools import partial
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/litex"))
sys.argv = [sys.argv[0]]
import test_ctrl_memory as t  # noqa: E402

problems: list[str] = []
with tempfile.TemporaryDirectory(prefix="ledger-quick-") as name:
    tmp = Path(name)
    t.run_arm(problems, "rules", partial(t.check_arms, tmp=tmp))
    green = {"checks"} if not problems else set()
    t.run_arm(problems, "planted ledgers", partial(t.ledger_plant_arms, tmp=tmp, green=green))
    mine = tuple(m for m in t.MUTANTS if m.attribute == "ledgered_tiles")
    with contextlib.ExitStack() as stack:
        t.MUTANTS = mine
        t.run_arm(problems, "ledgered_tiles mutants", partial(t.mutant_arms, tmp=tmp, green=green))
print(f"{len(problems)} problem(s)")
for p in problems:
    print("FAIL:", p)
sys.exit(1 if problems else 0)
