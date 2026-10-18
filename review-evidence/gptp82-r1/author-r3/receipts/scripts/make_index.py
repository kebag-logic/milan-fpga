#!/usr/bin/env python3
"""Write RECEIPTS.md: every file under the output directory except the index
itself, with its size and sha256, plus the large receipts kept in scratch.
Usage: make_index.py <outdir>"""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
GROUPS = [
    ("HANDOFF.md", "the handoff, rounds 1 and 2"),
    ("PR-BODY.md", "the PR body draft"),
    ("receipts/gates/base/", "repository gates at base b9ade3a6 (HEAD names the commit)"),
    ("receipts/gates/head/", "repository gates at head 8f3c376d (HEAD names the commit)"),
    ("receipts/pgates/base/", "parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0)"),
    ("receipts/pgates/head/", "parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests)"),
    ("receipts/parent/", "the two local parent commits: stats, the docs, ledger and test diffs"),
    ("receipts/controls/", "head harness against the base and round-1 RTL and ROM"),
    ("receipts/r651/head/", "R651-1 cold, gone and warm probes re-run at head"),
    ("receipts/r651/round1/", "the same probes at the round-1 head 85373de0"),
    ("receipts/iface/", "parameter and port declarations, comments stripped, at four revisions"),
    ("receipts/rom/", "ROM packing for the three images at head and base"),
    ("receipts/synth/", "synthesis-proxy statistics of the engine at base and head"),
    ("receipts/scripts/", "the scratch scripts these receipts were produced with"),
]
SCRATCH = [
    ("<data>/tmp/gptp82-a649/r2/synth/base/synth.log", 750086, "372e75c5133a18a2f458524a922c8fcf79d6cfa8da0eb63a5af8f4767fc3a6a1"),
    ("<data>/tmp/gptp82-a649/r2/synth/head-final/synth.log", 744897, "e4350b25f2af02a58bd57ed300df3b3bc63ffc623e3bc02546f8043a2e07e25c"),
    ("<data>/tmp/gptp82-a649/r2/synth/varb/synth.log", 744567, "fd64e5dded731fe622838f0e721f1d4dce3de0d9726cfc737092f9e99c121104"),
]
files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "RECEIPTS.md")
rows = []
for p in files:
    rel = p.relative_to(root).as_posix()
    data = p.read_bytes()
    assert len(data) < 200 * 1024, rel
    desc = next(d for g, d in GROUPS if rel == g or rel.startswith(g))
    rows.append((rel, len(data), hashlib.sha256(data).hexdigest(), desc))
out = ["# Round 2 receipts index", "",
       "Every file under this directory except this index, with its size in bytes and sha256.",
       "`receipts/scripts/verify_receipts.py <this directory>` checks that the table and the",
       "directory match exactly.", "",
       "| file | bytes | sha256 | what it is |", "|---|---:|---|---|"]
out += [f"| `{r}` | {n} | `{h}` | {d} |" for r, n, h, d in rows]
out += ["", "## Kept in scratch (over 200 KB), by size and sha256", "",
        "| scratch file | bytes | sha256 | what it is |", "|---|---:|---|---|"]
out += [f"| `{r}` | {n} | `{h}` | full synthesis log behind `receipts/synth/` |" for r, n, h in SCRATCH]
(root / "RECEIPTS.md").write_text("\n".join(out) + "\n")
print(f"indexed {len(rows)} files")
