#!/usr/bin/env python3
"""Compare verdict cells and numeric figures of the #629 bench page between two revisions.

Verdict cells: the second cell of every table row whose second cell carries a
verdict word (PASS, FAIL, NOT RUN, Met, Not met, Observed). Figures: the
multiset of numbers (with their unit word, if any) in each revision's page,
outside hex hashes. Prints added/removed figures so each can be judged.

Usage: verdict_figure_delta.py <repo> <rev-a> <rev-b>
"""
import collections, re, subprocess, sys

REPO, A, B = sys.argv[1:4]
PAGE = "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
VW = re.compile(r"\b(PASS|FAIL|NOT RUN|Met|Not met|Observed)\b")


def page(rev):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{PAGE}"], check=True,
                          capture_output=True, text=True).stdout.splitlines()


def verdicts(lines):
    out = []
    for ln in lines:
        if ln.startswith("|") and not ln.startswith("|---"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if len(cells) >= 2 and VW.search(cells[1]):
                out.append((cells[0], cells[1]))
    return out


def figures(lines):
    c = collections.Counter()
    for ln in lines:
        ln = re.sub(r"`[0-9a-f]{7,64}`|\b[0-9a-f]{40}\b|issuecomment-\d+|#[\w-]+\)", " ", ln)
        for m in re.finditer(r"[+-]?\d[\d,]*(?:\.\d+)?(?:\s*(?:ppm|s|ms|ns|dB|frames?|blocks?|ticks|%))?", ln):
            c[m.group(0)] += 1
    return c


la, lb = page(A), page(B)
va, vb = verdicts(la), verdicts(lb)
print(f"verdict cells: {len(va)} at {A[:8]}, {len(vb)} at {B[:8]}; identical: {va == vb}")
for x, y in zip(va, vb):
    if x != y:
        print("  CHANGED", x, "->", y)
fa, fb = figures(la), figures(lb)
print("figures removed:", dict(fa - fb))
print("figures added:", dict(fb - fa))
