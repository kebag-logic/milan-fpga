#!/usr/bin/env python3
"""Reviewer comparison (R514-1, #667): full render campaign, merge parent vs head.

Ruling 6012843714 (base re-pointed to the merge parent by 6016181662) requires
every check and every mutant of the render campaign to give the same result at
base and head. This compares the two complete campaign logs after removing
build chatter (compiler/simulator command lines and make directory lines) and
normalising per-run temporary directory names and the two tree roots.

usage: compare_render_campaign.py BASE_LOG HEAD_LOG BASE_ROOT HEAD_ROOT
Exit 0 only when the normalised logs are identical.
"""
import re
import sys
from pathlib import Path

NOISE = re.compile(r"^(g\+\+|ccache|make(\[\d+\])?:|/\S*verilator|- V e r i l a t i o n|- Verilator:|"
                   r"\S*perl |python3 \S*gen_|ar |rm |mkdir |cp |echo |In file included|\s+\||\s+\^|\s*\d+ \|)")


def normalise(path: Path, root: str) -> list[str]:
    out = []
    for line in path.read_text(errors="replace").splitlines():
        if NOISE.match(line):
            continue
        line = line.replace(root, "<ROOT>")
        line = re.sub(r"/tmp[^\s'\"]*|tdm8r?-?mutants?-[A-Za-z0-9_]+", "<TMP>", line)
        line = re.sub(r"\d+(\.\d+)? ?s (wall|elapsed)", "<T>", line)
        out.append(line)
    return out


def main() -> int:
    base_log, head_log, base_root, head_root = sys.argv[1:5]
    base = normalise(Path(base_log), base_root)
    head = normalise(Path(head_log), head_root)
    judg = re.compile(r"^\s*\[(PASS|FAIL)\]|checks: |RESULT|SURVIV|caught|mutant", re.I)
    jb = [l for l in base if judg.search(l)]
    jh = [l for l in head if judg.search(l)]
    print(f"normalised lines base={len(base)} head={len(head)}; judgment lines base={len(jb)} head={len(jh)}")
    print(f"judgment lines identical: {jb == jh}")
    print(f"normalised logs identical: {base == head}")
    if base != head:
        import difflib
        for d in list(difflib.unified_diff(base, head, "base", "head", n=0, lineterm=""))[:80]:
            print(d)
    for l in jb:
        if re.search(r"\[FAIL\]|SURVIV|RESULT|caught.*/", l):
            print("BASE-JUDGMENT", l)
    return 0 if jb == jh else 1


if __name__ == "__main__":
    raise SystemExit(main())
