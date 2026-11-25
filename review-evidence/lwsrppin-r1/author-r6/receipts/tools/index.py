#!/usr/bin/env python3
"""index.py RECEIPTS_DIR: write RECEIPTS_DIR/INDEX.md, one row per file (bytes, sha256 prefix, what it is).
Refuses a file that is not UTF-8 text or is 200 KB or more."""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
WHAT = [
    ("merge/merge-commit", "the merge commit's parents and subject, dev-soft-core's side (67838b37..HEAD --stat), the diagram files against e608f8d8 and the manifest diff"),
    ("merge/diagram-regeneration", "the conflicts, how they were resolved (generator only), the word diff against each parent, the pins named, the generator's --check and --selftest"),
    ("merge/diff-e608-head", "git diff e608f8d8 HEAD --stat, and its path set against this PR's own (2509db68..67838b37): equal"),
    ("merge/blob-identity", "each of this PR's paths: HEAD's blob against 67838b37's; every path outside them against e608f8d8's (0 differ)"),
    ("merge/dev-delta-per-path", "67838b37..HEAD against 2509db68..e608f8d8, path by path; SUBMODULES.md as git merge-file of the three sides"),
    ("merge/dev-delta-patches", "the whole-patch comparison (diagram files excluded) and why it is not byte-equal: SUBMODULES.md"),
    ("identity/identity", "image identity at 2b98e219 against 67838b37: plat_ledger result, the 28-file comparison, the 8x8/1if and 1x1/1if ctrl ELFs, why gptp_ucode.hex differs"),
    ("identity/plat-ledger-2b98e219", "plat_ledger.py --build-dir at 2b98e219, its log"),
    ("identity/sha-2b98e219", "sha256 of every ELF/bin/hex plat_ledger.py --build-dir writes at 2b98e219"),
    ("identity/sha-67838b37", "the same at 67838b37 (round 5's build)"),
    ("docs/summary", "the 12 docs gates at 2b98e219: one line per gate with its rc, time and last line"),
    ("docs/run", "the docs gates' head, porcelain before and after, and how each was run"),
    ("docs/", "a docs gate's log at 2b98e219"),
    ("suite/egress-ledger-selftest", "egress_ledger.py --selftest at 2b98e219 (72 controls, 18 mutants)"),
    ("suite/run-self-test", "run.py --self-test at 2b98e219, the ctrl_service_budget suite's self-test"),
    ("suite/run", "run.py --self-test: head, start, end, rc, porcelain after"),
    ("tools/", "a script this round ran"),
]
rows = []
for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "INDEX.md"):
    rel = path.relative_to(root).as_posix()
    data = path.read_bytes()
    data.decode("utf-8")
    if len(data) >= 200_000:
        raise SystemExit(f"{rel}: {len(data)} B, not under 200 KB")
    what = next(w for key, w in WHAT if rel.startswith(key))
    rows.append(f"| `{rel}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()[:16]}` | {what} |")
head = """# Receipts: round 6, the sync merge of dev-soft-core e608f8d8 (PR #992)

Head `2b98e219a5e2b0681f76be90083fc05e47a8f6c0`, the merge of `e608f8d8` into `67838b37`, local and not pushed. Every
file is text and under 200 KB. Scratch is under `/data-2/milan/tmp/lwsrppin-a834/r6/`. Raw logs carry local paths.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
"""
(root / "INDEX.md").write_text(head + "\n".join(rows) + "\n", encoding="utf-8")
print(f"INDEX.md: {len(rows)} files")
