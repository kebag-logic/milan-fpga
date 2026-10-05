#!/usr/bin/env python3
"""R500-2: the full failure text of chosen lane-planted defects, so a reader
can see each fails for the defect it names. Run from the head's checkout root:

    python3 /path/to/r500_2_mutant_detail.py <scratch-dir> NAME [NAME ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import nvm_mutants                                       # noqa: E402
import test_ctrl_nvm as gate                             # noqa: E402
from nvm_bench import shape_inputs                       # noqa: E402

KEYS = ("terminal", "cause", "bind_terminal", "failed", "ok", "erases", "exhausted", "withheld",
        "abandoned", "abandoned_vd", "sm_unbinds", "sm_rollbacks", "commit_tries",
        "commit_refused", "protected")


def brief(text: str) -> str:
    """The finding with only the status keys a reader needs."""
    head = text.split("{", 1)[0]
    pairs = dict(re.findall(r"'(\w+)': (-?\d+)", text))
    return head + " ".join(f"{k}={pairs[k]}" for k in KEYS if k in pairs)


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    want = set(sys.argv[2:])
    inputs = shape_inputs(ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
    for m in nvm_mutants.MUTANTS:
        if m.name not in want:
            continue
        tree = work / m.name / "tree"
        nvm_mutants.plant(m, tree)
        b = gate.bench_for(inputs, work / m.name, tree)
        res = gate.grade(b, list(m.kills))
        for k in m.kills:
            print(f"MUTANT {m.name} / {k}: {len(res[k])} finding(s)", flush=True)
            for x in res[k][:3]:
                print(f"    {brief(x)[:300]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
