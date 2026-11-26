#!/usr/bin/env python3
"""Per planted defect, the failing checks at base layout vs head layout of the engine passes test.

usage: compare_plants.py RUNS_DIR
A check's identity is its [FAIL] line up to the first ':' (its label); timing-only checks that can also fail
on an overloaded host (the budget reaching its peak, the fail-fast run, the clean -j4 out-of-order finish)
are marked LOAD-SENSITIVE.
"""
import re, sys
from pathlib import Path

R = Path(sys.argv[1])
SENSITIVE = re.compile(r"passes at once|pass 1 fails and the run ends|finished out of order|a parent make -j3")

def fails(name):
    text = (R / f"{name}.log").read_text(errors="replace")
    total = sum(1 for l in text.splitlines() if l.startswith(("[PASS]", "[FAIL]")))
    labels = sorted({("LOAD-SENSITIVE " if SENSITIVE.search(l) else "")
                     + re.sub(r"/tmp/engine-passes-test-[^/ ]+", "<tmp>", l.split(":", 1)[0])
                     for l in text.splitlines() if l.startswith("[FAIL]")})
    summary = [l for l in text.splitlines() if l.startswith("engine passes test:")]
    return total, labels, summary[-1] if summary else "(no summary)"

for m in ["control", "failfast", "noforward", "exit128", "merged", "nochdir", "noprctl", "noignore"]:
    tb, fb, sb = fails(f"pt-base-{m}"); th, fh, sh = fails(f"pt-head-{m}")
    core = lambda s: [x for x in s if not x.startswith("LOAD-SENSITIVE")]
    same = core(fb) == core(fh)
    print(f"== {m}: base {sb} ({tb} checks) | head {sh} ({th} checks) | non-load-sensitive failing set "
          f"{'IDENTICAL' if same else 'DIFFERS'} ({len(core(fb))} vs {len(core(fh))})")
    for x in sorted(set(fb) | set(fh)):
        where = "both" if x in fb and x in fh else "base only" if x in fb else "head only"
        print(f"   {where:9} {x}")
for extra in ["pt-head-control-c0"]:
    t, f, s = fails(extra); print(f"== {extra}: {s} ({t} checks)"); [print("   ", x) for x in f]
