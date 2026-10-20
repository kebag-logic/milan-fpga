#!/usr/bin/env python3
"""Compare base and head records: usage compare.py <base dir> <head dir> <out dir> [--sorted]

Each <name>.log present on both sides is normalised (tree roots, scratch and
temporary directories, timings, Verilator's build statistics) and diffed;
with --sorted the lines are sorted first (parallel completion order). Writes
<out>/<name>.diff and prints one summary line per record."""
import difflib
import re
import sys
from pathlib import Path

ROOTS = [
    "<submodule>",
    "<lane>",
    "<scratch>/rec2/base-camps",
    "<scratch>/rec2/head-camps",
    "<scratch>/rec2/base-gates",
    "<scratch>/rec2/head-gates",
    "<scratch>/rec2/cons-base",
    "<scratch>/rec2/cons-head",
    "<parent>",
    "<scratch>",
]
SUBS = [
    (re.compile(r"/tmp/[A-Za-z0-9_.-]+-[a-z0-9_]{6,}"), "<tmp>"),
    (re.compile(r"/tmp/tmp[a-z0-9_]{6,}"), "<tmp>"),
    (re.compile(r"Walltime [0-9.]+ s.*"), "Walltime <t>"),
    (re.compile(r"Built from [0-9.]+ MB sources in [0-9]+ modules, into [0-9.]+ MB in [0-9]+ C\+\+ files needing [0-9.]+ MB"), "Built <stats>"),
    (re.compile(r"\b[0-9]+(\.[0-9]+)? ?(s|ms|sec|seconds)\b"), "<t>"),
    (re.compile(r"\(\s*[0-9]+(\.[0-9]+)?s\)"), "(<t>)"),
    (re.compile(r"\b(real|user|sys)\s+[0-9]+m[0-9.]+s"), r"\1 <t>"),
    (re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9:.]+"), "<date>"),
    (re.compile(r"make\[[0-9]+\]"), "make[n]"),
    (re.compile(r"all\.v:[0-9]+"), "all.v:N"),
]


def norm(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        for r in ROOTS:
            line = line.replace(r, "<root>")
        for pat, rep in SUBS:
            line = pat.sub(rep, line)
        out.append(line.rstrip())
    return out


def main() -> int:
    base, head, outd = map(Path, sys.argv[1:4])
    srt = "--sorted" in sys.argv
    outd.mkdir(parents=True, exist_ok=True)
    names = sorted({p.stem for p in base.glob("*.log")} | {p.stem for p in head.glob("*.log")})
    for n in names:
        b, h = base / f"{n}.log", head / f"{n}.log"
        brc = (base / f"{n}.rc").read_text().strip() if (base / f"{n}.rc").exists() else "-"
        hrc = (head / f"{n}.rc").read_text().strip() if (head / f"{n}.rc").exists() else "-"
        if not b.exists() or not h.exists():
            print(f"{n:28s} base rc={brc} head rc={hrc}  ONE SIDE ONLY")
            continue
        bl, hl = norm(b.read_text(errors="replace")), norm(h.read_text(errors="replace"))
        if srt:
            bl, hl = sorted(bl), sorted(hl)
        d = list(difflib.unified_diff(bl, hl, f"base/{n}", f"head/{n}", lineterm="", n=0))
        (outd / f"{n}.diff").write_text("\n".join(d) + ("\n" if d else ""))
        changed = sum(1 for x in d if x[:1] in "+-" and not x.startswith(("+++", "---")))
        print(f"{n:28s} base rc={brc} head rc={hrc}  {'identical' if not d else f'{changed} differing lines'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
