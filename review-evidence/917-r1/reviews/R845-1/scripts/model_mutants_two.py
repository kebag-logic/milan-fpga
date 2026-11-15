#!/usr/bin/env python3
"""Run named ctrl_mutants.py entries through the campaign's own shard selector (index i, stride the table length).
Usage: python3 -I model_mutants_two.py <clone> <out-dir> <name>..."""
import sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import ctrl_mutants as cm  # noqa: E402
idx = {m.name: i for i, m in enumerate(cm.MUTANTS)}
bad = False
for n in sys.argv[3:]:
    print(f"== {n}: index {idx[n]} of {len(cm.MUTANTS)}", flush=True)
    bad = cm.campaign(out / n, out / "reuse", 4, (1, 1), [idx[n], len(cm.MUTANTS)]) or bad
sys.exit(1 if bad else 0)
