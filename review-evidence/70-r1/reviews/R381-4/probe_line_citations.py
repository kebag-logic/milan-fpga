#!/usr/bin/env python3
"""Line-citation drift probe for the #70 / PR #610 composition candidate.

Usage: probe_line_citations.py <candidate-clone> <source-base> <candidate>

For every `path:N` / `path:N-M` / `path:N,M` citation on the five pages PR #610
changes (as they stand at <candidate>), resolve the path, and for each cited line
compare its text at <source-base> (the tree the author cited against) with its text
at <candidate>. A citation whose file the queued predecessors changed and whose
cited line text moved is reported as DRIFT. Same-file anchors are unaffected.
Exit 1 on any DRIFT.
"""
import re
import subprocess
import sys
from pathlib import PurePosixPath

repo, base, cand = sys.argv[1:4]
PAGES = [
    "docs/README.md",
    "docs/design/SAVED_STATE_FASTCONNECT.md",
    "docs/design/SAVED_STATE_MATERIALIZATION.md",
    "docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md",
    "docs/integration/BAREMETAL_FIRMWARE.md",
]
CITE = re.compile(r"([A-Za-z0-9_./-]+\.(?:md|py|sv|svh|c|h|cpp|hpp|sh|yml|yaml|json|v|mk|feature|tsv|txt))"
                  r"(?:#L|:)(\d+(?:[-,]\d+)*)")


def git(*args: str) -> str:
    return subprocess.run(["git", "-c", "core.commitGraph=false", "-C", repo, *args],
                          capture_output=True, text=True).stdout


tracked = git("ls-tree", "-r", "--name-only", cand).split()
changed = set(git("diff", "--name-only", base, cand).split())
blobs = {}


def lines(rev: str, path: str):
    key = (rev, path)
    if key not in blobs:
        out = subprocess.run(["git", "-c", "core.commitGraph=false", "-C", repo, "show", f"{rev}:{path}"],
                             capture_output=True, text=True)
        blobs[key] = out.stdout.splitlines() if out.returncode == 0 else None
    return blobs[key]


def resolve(page: str, cited: str):
    if cited in tracked:
        return [cited]
    rel = str(PurePosixPath(page).parent / cited)
    parts = []
    for p in rel.split("/"):
        if p == "..":
            parts and parts.pop()
        elif p not in ("", "."):
            parts.append(p)
    rel = "/".join(parts)
    if rel in tracked:
        return [rel]
    return [t for t in tracked if t.endswith("/" + cited) or t == cited]


total = drift = in_changed = unresolved = 0
for page in PAGES:
    text = git("show", f"{cand}:{page}")
    for m in CITE.finditer(text):
        cited, spec = m.group(1), m.group(2)
        nums = []
        for part in spec.split(","):
            a, _, b = part.partition("-")
            nums += [int(a)] + ([int(b)] if b else [])
        hits = resolve(page, cited)
        if len(hits) != 1:
            unresolved += 1
            print(f"UNRESOLVED {page}: {cited}:{spec} ({len(hits)} candidates)")
            continue
        path = hits[0]
        for n in nums:
            total += 1
            if path not in changed:
                continue
            in_changed += 1
            old, new = lines(base, path), lines(cand, path)
            o = old[n - 1] if old and 0 < n <= len(old) else None
            c = new[n - 1] if new and 0 < n <= len(new) else None
            status = "SAME" if o == c else "DRIFT"
            drift += status == "DRIFT"
            print(f"{status} {page}: {cited}:{n} -> {path}")
            if status == "DRIFT":
                print(f"   base: {o!r}\n   cand: {c!r}")
print(f"citations(line numbers)={total} into-train-changed-files={in_changed} "
      f"drift={drift} unresolved-paths={unresolved}")
sys.exit(1 if drift else 0)
