#!/usr/bin/env python3
"""index.py RECEIPTS_DIR: write RECEIPTS_DIR/INDEX.md, one row per file (bytes, sha256 prefix, what it is)."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
WHAT = [
    ("ledger/derivation", "each figure: the tool's LEDGER, the rule computed apart in Decimal, the ruling's expected figure, the image that sets it"),
    ("ledger/measurements", "TRAIN and PINNED against round 4's backlog-owed.json (10 ns), and the results' image and file sha256"),
    ("ledger/egress-ledger-selftest", "egress_ledger.py --selftest at 67838b37 (72 controls, 18 mutants)"),
    ("ledger/egress-ledger-8x8-1if-from-log", "egress_ledger.py --point 8x8-1if at 67838b37 on round 4's arm A 8x8/1if run log"),
    ("ledger/egress-ledger-8x8-1if", "egress_ledger.py --point 8x8-1if at 67838b37 on round 4's arm A 8x8/1if results (merge head image)"),
    ("ledger/egress-ledger-train", "egress_ledger.py --point 8x8-1if at 67838b37 on round 4's backlog-owed results on the train's image 2509db68"),
    ("identity/identity", "image identity: the changed paths, the harness build inputs, the 28-file rebuild comparison"),
    ("identity/sha-67838b37", "sha256 of every ELF/bin/hex plat_ledger.py --build-dir writes at 67838b37"),
    ("identity/sha-507bce7f", "the same at 507bce7f (round 3's build)"),
    ("identity/plat-ledger", "plat_ledger.py --build-dir at 67838b37, its log"),
    ("commit/", "git show --stat --patch of the round's commit"),
    ("docs/run.log", "docs.yml steps at 67838b37: one line per step with its rc"),
    ("docs/docs-gates-2__15", "a docs.yml step's log (cut head and tail, over 190,000 B)"),
    ("docs/", "a docs.yml step's log, or the run's head/start/end/rc"),
    ("tools/", "a script this round ran"),
    ("pr-body-before-r5", "the live PR body as it read at the start of this round (updated 2026-11-24T22:48Z)"),
]
rows = []
for f in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    rel = f.relative_to(root).as_posix()
    data = f.read_bytes()
    what = next((w for k, w in WHAT if rel.startswith(k)), "")
    rows.append(f"| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()[:16]}` | {what} |")
head = """# Receipts: round 5, the held-egress ledger restated at 8x8/1if (the ruling on PR #992)

Head `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570`, one commit on `507bce7f`, local and not pushed. Every file is text
and under 200 KB, and there is no .gz. A log over 190,000 B is kept as its first and last 90,000 B, with its full
size and sha256 noted at the cut (`tools/rcopy.py`). Scratch is under `/data-2/milan/tmp/lwsrppin-a834/r5/`. The
measurements graded here are round 4's results directories, under `/data-2/milan/tmp/lwsrppin-a834/r4/harness/`.
Raw logs carry local paths.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
"""
(root / "INDEX.md").write_text(head + "\n".join(rows) + "\n")
print(len(rows), "files")
