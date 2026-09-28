#!/usr/bin/env python3
"""Differential probe: can the builder test's reads of the composed page
flip, although each side passed on its own?

Usage: probe_builder_page_constants.py <candidate-clone>

`sw/builder/test_builder.py` reads docs/integration/BAREMETAL_FIRMWARE.md as
text (docs_source). The page is the one file PR #610 shares with the train
(#582). Both sides passed the builder bank on their own trees; the composed
page is base + #582 hunk + #610 hunk (disjoint). A text assertion can only
behave differently on the composition when it depends on text that BOTH
sides changed. This probe takes every string constant in test_builder.py
(literal and, where it compiles, as a regex under MULTILINE and DOTALL), counts its
matches on the four page versions, and classifies each constant whose count
moved away from the base: only on the #582 side, only on the #610 side, or on
both. "both" constants are printed in full; exit 1 if any exists, or if the
composed count is not the additive composition of the two sides.
"""
import ast
import re
import subprocess
import sys

repo = sys.argv[1]
PAGE = "docs/integration/BAREMETAL_FIRMWARE.md"
REVS = {"base": "c07232228c12b72805dd20e6852bf93f25794da0",
        "582": "c1fa4183f99293f8ee0777cda454d9d77855ca09",
        "610": "6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14",
        "cand": "c08becbbfdbf622ee678d5854312c53faf805d39"}


def show(rev, path):
    return subprocess.run(["git", "-c", "core.commitGraph=false", "-C", repo, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


pages = {k: show(v, PAGE) for k, v in REVS.items()}
src = show(REVS["cand"], "sw/builder/test_builder.py")
consts = sorted({n.value for n in ast.walk(ast.parse(src))
                 if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) >= 4})
moved = {"582": 0, "610": 0, "both": 0}
nonadd = 0
checked = 0
for s in consts:
    probes = [("lit", lambda t, s=s: t.count(s))]
    try:
        rx = re.compile(s, re.M | re.S)
        probes.append(("re", lambda t, rx=rx: sum(1 for _ in rx.finditer(t))))
    except (re.error, RecursionError, OverflowError):
        pass
    for kind, f in probes:
        try:
            c = {k: f(t) for k, t in pages.items()}
        except Exception:
            continue
        checked += 1
        d582 = c["582"] != c["base"]
        d610 = c["610"] != c["base"]
        if c["cand"] != c["582"] + c["610"] - c["base"]:
            nonadd += 1
            print(f"NON-ADDITIVE {kind} {s[:90]!r} counts={c}")
        if d582 and d610:
            moved["both"] += 1
            print(f"BOTH {kind} {s[:120]!r} counts={c}")
        elif d582:
            moved["582"] += 1
            print(f"582-only {kind} {s[:90]!r} counts={c}")
        elif d610:
            moved["610"] += 1
            print(f"610-only {kind} {s[:90]!r} counts={c}")
print(f"constants={len(consts)} probes={checked} moved: 582-only={moved['582']} "
      f"610-only={moved['610']} both={moved['both']} non-additive={nonadd}")
sys.exit(1 if moved["both"] or nonadd else 0)
