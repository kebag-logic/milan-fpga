#!/usr/bin/env python3
"""R347-2: name the shipped test(s) that kill each R347-1 mutant.

Usage: python3 -B kill_attribution.py <extracted-tree>

Reuses the unchanged MUTANTS list from mutants.py (round 1).  For each mutant
it edits tb/tools/torture_campaign.py inside the extracted tree, runs the
planner --self-test (verbosity 2) and the plan behave feature, and prints the
failing unittest names and the failing behave scenarios.  Original bytes are
restored after every mutant and verified at the end.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutants import MUTANTS  # noqa: E402


def failing(tree: Path) -> tuple[list[str], list[str]]:
    target = tree / "tb/tools/torture_campaign.py"
    st = subprocess.run([sys.executable, "-B", str(target), "--self-test"], cwd=tree,
                        capture_output=True, text=True, timeout=600)
    tests = sorted({m.group(1) for m in re.finditer(
        r"^(?:FAIL|ERROR): (test_\w+)", st.stderr, re.M)})
    bh = subprocess.run([sys.executable, "-B", "-m", "behave",
                         "tests/features/torture_campaign_plan.feature", "-f", "plain",
                         "--no-snippets"], cwd=tree, capture_output=True, text=True,
                        timeout=600)
    scen = []
    if "Failing scenarios:" in bh.stdout:
        block = bh.stdout.split("Failing scenarios:", 1)[1]
        for line in block.splitlines()[1:]:
            if not line.startswith("  "):
                break
            scen.append(line.strip())
    return tests, scen


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    target = tree / "tb/tools/torture_campaign.py"
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    print(f"target sha256 {digest}")
    text = original.decode()
    try:
        for name, old, new in MUTANTS:
            if text.count(old) != 1:
                print(f"UNAPPLIED {name}")
                continue
            target.write_text(text.replace(old, new))
            tests, scen = failing(tree)
            target.write_bytes(original)
            print(f"{name}\n  self-test: {', '.join(tests) or 'none'}")
            for s in scen:
                print(f"  behave: {s}")
            if not scen:
                print("  behave: none")
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    print(f"restored target sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
