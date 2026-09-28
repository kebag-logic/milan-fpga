#!/usr/bin/env python3
"""Anchor probe for the #70 / PR #610 composition candidate.

Usage: probe_anchors.py <candidate-clone>
Run with a Python that has the repository's locked Markdown renderer.

Checks, with the repository's own heading/anchor reader (scripts/gen_toc.py):
  1. every fragment link (same-page `#x` and cross-page `page.md#x`) written
     on the focus pages resolves to a rendered heading of its target;
  2. every fragment link anywhere in the tracked Markdown that points INTO a
     focus page resolves.
Focus pages: the five pages PR #610 changes and the pages the queued
predecessors (#582, #593, #75) changed. Exit 1 on any miss.
"""
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import gen_toc  # noqa: E402

FOCUS = [
    "docs/README.md",
    "docs/design/SAVED_STATE_FASTCONNECT.md",
    "docs/design/SAVED_STATE_MATERIALIZATION.md",
    "docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md",
    "docs/integration/BAREMETAL_FIRMWARE.md",
    "docs/AAF_LATENCY_TAPS.md",
    "docs/ENDSTATION_BUILDER.md",
    "docs/testing/CI_WORKFLOWS.md",
    "docs/testing/TESTING.md",
    "docs/design/GM_LOSS_RECOVERY.md",
    "docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md",
    "docs/findings/README.md",
    "REQUIREMENTS.md",
]
LINK = re.compile(r"\]\(([^)\s]*?)(?:#([^)\s]+))\)")
cache = {}


def anchors(path: Path) -> set:
    if path not in cache:
        cache[path] = {a for _, _, a in gen_toc.headings(path.read_text())}
    return cache[path]


def check(src: Path, only_into=None):
    ok = bad = 0
    for m in LINK.finditer(src.read_text()):
        target, frag = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        tgt = src if target == "" else (src.parent / target).resolve()
        if only_into is not None and tgt not in only_into:
            continue
        if tgt.suffix != ".md" or not tgt.exists():
            continue
        if frag in anchors(tgt):
            ok += 1
        else:
            bad += 1
            print(f"MISS {src.relative_to(repo)} -> {target or '(self)'}#{frag}")
    return ok, bad


focus = {(repo / f).resolve() for f in FOCUS}
tracked = subprocess.run(["git", "-C", str(repo), "ls-files", "*.md"],
                         capture_output=True, text=True, check=True).stdout.split()
tot_ok = tot_bad = 0
for f in FOCUS:
    ok, bad = check(repo / f)
    print(f"out-of {f}: {ok} resolved, {bad} missing")
    tot_ok += ok
    tot_bad += bad
into_ok = into_bad = 0
for f in tracked:
    p = (repo / f).resolve()
    if not p.exists():
        continue
    ok, bad = check(p, only_into=focus)
    into_ok += ok
    into_bad += bad
print(f"into focus pages from {len(tracked)} tracked pages: "
      f"{into_ok} resolved, {into_bad} missing")
print(f"TOTAL resolved={tot_ok + into_ok} missing={tot_bad + into_bad}")
sys.exit(1 if tot_bad + into_bad else 0)
