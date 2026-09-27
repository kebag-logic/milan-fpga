#!/usr/bin/env python3
"""R347-2: name the shipped tests that kill R346-1's required mutants.

Usage: python3 -B r346_attribution.py <planner_mutants.py> <extracted-tree>

Reads the mutant table `M` from R346-1's unchanged public planner_mutants.py
with ast.literal_eval (the script is not executed), applies each required
mutant to the extracted tree, and reports the failing self-test names and
behave scenarios through kill_attribution.failing().  Bytes are restored.
"""
from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kill_attribution import failing  # noqa: E402

REQUIRED = ("A04", "A05", "P01", "P03", "P07", "C01", "C08")


def table(script: Path) -> dict:
    for node in ast.parse(script.read_text()).body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and getattr(node.targets[0], "id", None) == "M"):
            return ast.literal_eval(node.value)
    raise SystemExit("mutant table M not found")


def main() -> int:
    script, tree = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    print(f"script sha256 {hashlib.sha256(script.read_bytes()).hexdigest()}")
    mutants = table(script)
    target = tree / "tb/tools/torture_campaign.py"
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    try:
        for name, (old, new) in mutants.items():
            if name.split()[0] not in REQUIRED:
                continue
            if text.count(old) != 1:
                print(f"UNAPPLIED ({text.count(old)} matches) {name}")
                continue
            target.write_text(text.replace(old, new))
            tests, scen = failing(tree)
            target.write_bytes(original)
            print(f"{name}\n  self-test: {', '.join(tests) or 'none'}")
            for s in scen or ["none"]:
                print(f"  behave: {s}")
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    print(f"restored target sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
