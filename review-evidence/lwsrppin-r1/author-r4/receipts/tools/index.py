#!/usr/bin/env python3
"""index.py RECEIPTS_DIR: write RECEIPTS_DIR/INDEX.md, one row per file (bytes, sha256 prefix, what it is)."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
WHAT = [
    ("harness/train-2509db68/", "the train's own image at 2509db68: arm A's backlog-owed and srp-bound at 8x8/1if"),
    ("harness/grade-", "the run's grade: image identity, round 1's harness_grade.py, share_census.py, run.py's verdict lines"),
    ("harness/kept-", "kept_grade.py <build-dir> on arm A (the train's #969/#977 disposition)"),
    ("harness/la-window-", "la_window.py: each LeaveAll timer run-out, its MRPDU and the passes in the next second"),
    ("harness/egress-ledger-8x8", "egress_ledger.py --point 8x8-1if on arm A at the merge head"),
    ("harness/egress-ledger-selftest", "egress_ledger.py --selftest at the merge head"),
    ("harness/egress-compare", "the seven egress rows: pin 402834ac (round 1), train 2509db68, merge 507bce7f, ledger"),
    ("harness/identity", "harness ELF sha256 against the merge head's ledger images"),
    ("harness/variant-objects", "each variant's image objects against arm A's"),
    ("harness/run-", "run.py's log (cut head and tail where over 190,000 B)"),
    ("harness/table-", "run.py's results/table.md (cut head and tail where over 190,000 B)"),
    ("harness/build-", "the harness build.json (the image's recorded inputs and sha256)"),
    ("harness/selftest", "run.py --self-test (cut head and tail where over 190,000 B)"),
    ("harness/times", "each run's rc, start, end and head"),
    ("budget/train-", "load_grade/flip_grade at 2509db68 and the byte comparison"),
    ("budget/", "load_grade.py --check and flip_grade.py --check at the merge head"),
    ("merge/", "the merge's parents, base, paths and git merge-tree reproduction"),
    ("tools/", "a script this round ran"),
    ("pr-body-before-r4", "the PR body as it read before this round (05:49Z edit)"),
]
rows = []
for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    rel = f.relative_to(root).as_posix()
    data = f.read_bytes()
    what = next((w for k, w in WHAT if rel.startswith(k)), "")
    rows.append(f"| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()[:16]}` | {what} |")
head = """# Receipts: round 4, the CPU budget harness on the merge head's images and the PR body at 507bce7f

Merge head `507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698` (parents `30796098` and `2509db68`), pushed, unchanged this round.
Every file is text and under 200 KB, and there is no .gz. A log over 190,000 B is kept as its first and last 90,000 B,
with its full size and sha256 noted at the cut (`tools/rcopy.py`). Scratch (full logs and build trees) is under
`/data-2/milan/tmp/lwsrppin-a834/r4/`. Raw logs carry local paths, as in rounds 1 to 3.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
"""
(root / "INDEX.md").write_text(head + "\n".join(rows) + "\n")
print(len(rows), "files")
