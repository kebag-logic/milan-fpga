#!/usr/bin/env python3
"""Compare the engine's `make -j4 run` transcripts at base and head, and list each pass's record.

usage: compare_engine.py RUNS_RECEIPTS RUNS_SCRATCH
Normalisation drops the Verilator command and banner, compiler and sub-make directory lines and the reviewer's
own wall-time line, and masks the tree's own path; nothing else.
"""
import json, re, sys
from pathlib import Path

R, S = Path(sys.argv[1]), Path(sys.argv[2])
DROP = re.compile(r"^(g\+\+ |python3 \S*verilator|rm VKL|- V e r i l a t i o n|- Verilator:|make\[1\]: (Entering|Leaving)|"
                  r"\S*verilator --cc |wall [0-9.]+ s$|ccache )")

def norm(name):
    lines = (R / f"{name}.log").read_text(errors="replace").splitlines()
    tree = str(S / name)
    return [l.replace(tree, "<tree>") for l in lines if not DROP.search(l)], len(lines)

for a, b in (("eng-base-clean", "eng-head-clean"), ("eng-base-abort", "eng-head-abort")):
    (x, nx), (y, ny) = norm(a), norm(b)
    (R / f"{a}.norm").write_text("\n".join(x) + "\n"); (R / f"{b}.norm").write_text("\n".join(y) + "\n")
    print(f"{a} vs {b}: {'IDENTICAL' if x == y else 'DIFFERENT'} ({len(x)} normalised lines of {nx} / {len(y)} of {ny}); "
          f"rc {(R / f'{a}.rc').read_text().strip()} / {(R / f'{b}.rc').read_text().strip()}")
    if x != y:
        import difflib; print("".join(difflib.unified_diff([l + "\n" for l in x], [l + "\n" for l in y], a, b)))
for name in ("eng-base-clean", "eng-head-clean", "eng-base-abort", "eng-head-abort"):
    state = S / name / "tb/verilator/engine/obj_dir/engine-passes"
    recs = {p.name: json.loads(p.read_text()) for p in sorted(state.glob("*.json"))}
    marks = sorted(p.name for p in state.glob("*.stop"))
    print(f"{name}: records {recs}; stop marks {marks}; build.ok {(state / 'build.ok').exists()}")
    counts = [l for l in (R / f"{name}.log").read_text().splitlines() if re.match(r"^\d+ checks: ", l)]
    print(f"   check lines in order: {counts}")
