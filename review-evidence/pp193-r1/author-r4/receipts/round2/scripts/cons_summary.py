#!/usr/bin/env python3
"""Summaries of the large consumer logs (milan_dp, pp_shadow), and base-vs-head
diffs of their sorted check lines, normalized for paths and timings.

usage: cons_summary.py <base cons dir> <head cons dir> <out dir>
"""
import re
import sys
from pathlib import Path

base, head, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
NORM = [(re.compile(r"<scratch>/r2/[A-Za-z0-9_./-]+"), "<path>"),
        (re.compile(r"\b\d+(\.\d+)?\s*(s|ms|us|sec|seconds)\b"), "<t>"),
        (re.compile(r'"t_s": [0-9.]+'), '"t_s": <t>'),
        (re.compile(r'"idle_s": [0-9.]+'), '"idle_s": <t>'),
        (re.compile(r"Walltime [0-9.]+ s.*"), "Walltime <t>"),
        (re.compile(r"allocated [0-9.]+ MB"), "allocated <m>")]
CHECK = re.compile(r"(\[ok\]|\[PASS\]|\[FAIL\]|checks: |PASS:|FAIL:)")


def lines(p):
    res = []
    for line in p.read_text(errors="replace").splitlines():
        if not CHECK.search(line):
            continue
        for rx, tok in NORM:
            line = rx.sub(tok, line)
        res.append(line)
    return sorted(res)


for name in ("milan_dp", "pp_shadow", "milan_dp_render", "test_builder", "nvm_cosim_quick"):
    rows = []
    for side, d in (("base", base), ("head", head)):
        t = (d / f"{name}.log").read_text(errors="replace")
        rows.append(f"{side}: rc {(d / f'{name}.rc').read_text().strip()}, "
                    f"[ok] {t.count('[ok]')}, [PASS] {t.count('[PASS]')}, "
                    f"[FAIL] {t.count('[FAIL]')}, 'FAIL:' {t.count('FAIL:')}, "
                    f"check lines {len(lines(d / f'{name}.log'))}")
    b, h = lines(base / f"{name}.log"), lines(head / f"{name}.log")
    import difflib
    d = [x for x in difflib.unified_diff(b, h, "base", "head", lineterm="", n=0)]
    (out / f"{name}-checklines.diff").write_text("\n".join(d) + ("\n" if d else ""))
    rows.append("sorted check lines: " + ("identical" if not d else
                f"{sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---'))} lines differ"))
    (out / f"{name}-summary.txt").write_text("\n".join(rows) + "\n")
    print(name, "|", " | ".join(rows))
