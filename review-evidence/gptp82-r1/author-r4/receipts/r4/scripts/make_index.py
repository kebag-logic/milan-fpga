#!/usr/bin/env python3
"""Write RECEIPTS.md from the files present: every file under the output
directory except the index itself, with its size and sha256, in the table
under "## In this directory". The round-2 synthesis logs kept in scratch
are a separate table under "## Kept in scratch", which the verifier never
reads. Usage: make_index.py <outdir>"""
import hashlib, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
IN_DIR = "## In this directory"
SCRATCH_HDR = "## Kept in scratch (over 200 KB), by size and sha256"
GROUPS = [
    ("HANDOFF.md", "the handoff, rounds 1 to 4"),
    ("PR-BODY.md", "the PR body draft, rounds 1 to 4"),
    ("receipts/r4/gates/head/", "round 4: repository gates at head acfef36b (HEAD names the commit)"),
    ("receipts/r4/gates/base/", "round 4: repository gates at base 334e9fe6 (HEAD names the commit)"),
    ("receipts/r4/pgates/head-acfef36b/", "round 4: the full parent consumer list at local snapshot dd2e1fd9 (gitlink acfef36b)"),
    ("receipts/r4/pgates/base-334e9fe6/", "round 4: both idiom gates at local snapshot c85ab500 (gitlink 334e9fe6), the reproduced failure"),
    ("receipts/r4/pgates/dev-e4869fd0/", "round 4: both idiom gates at dev e9cbb676 as is (gitlink e4869fd0)"),
    ("receipts/r4/pgates/manager-334e9fe6/", "round 4: the manager's consumer receipts cited, the command template included"),
    ("receipts/r4/idiom/", "round 4: the idiom gates' per-file counts and the two files' findings, base and head"),
    ("receipts/r4/controls/", "round 4: the branch meta-run and the two planted controls of the phase-list split"),
    ("receipts/r4/parent/", "round 4: the local parent snapshots, submodules and the disabled push remote"),
    ("receipts/r4/scripts/", "round 4: the scratch scripts, host prefixes replaced by placeholders"),
    ("receipts/r4/", "round 4: identity comparisons, the lane log and the diffstat against 334e9fe6"),
    ("receipts/r3/gates/head/", "round 3: repository gates at head 334e9fe6 (HEAD names the commit)"),
    ("receipts/r3/gates/base/", "round 3: repository gates at base b9ade3a6 (HEAD names the commit)"),
    ("receipts/r3/gates/superseded-efa5e612/", "round 3: the two arm shards that failed at the superseded efa5e612"),
    ("receipts/r3/pgates/head/", "round 3: parent consumer gates at local commits 1687cf53 (pin) and c7c60bae (tests)"),
    ("receipts/r3/parent/", "round 3: the two local parent commits, their log and the disabled push remote"),
    ("receipts/r3/controls/", "round 3: non-vacuity runs, development arm runs, the meta-run and the reviewer's probes"),
    ("receipts/r3/iface/", "round 3: declarations without comments at four revisions"),
    ("receipts/r3/rom/", "round 3: ROM packing at base and head, and the image word differences"),
    ("receipts/r3/scripts/", "round 3: the scratch scripts, host prefixes replaced by placeholders"),
    ("receipts/gates/base/", "round 2: repository gates at base b9ade3a6 (HEAD names the commit)"),
    ("receipts/gates/head/", "round 2: repository gates at head 8f3c376d (HEAD names the commit)"),
    ("receipts/pgates/base/", "parent consumer gates, dev e9cbb676 as is (GITLINK e4869fd0)"),
    ("receipts/pgates/head/", "round 2: parent consumer gates at local commits e54c7c21 (gitlink) and 3d0cae2b (tests)"),
    ("receipts/parent/", "round 2: the two local parent commits: stats, the docs, ledger and test diffs"),
    ("receipts/controls/", "round 2: head harness against the base and round-1 RTL and ROM"),
    ("receipts/r651/head/", "round 2: R651-1 cold, gone and warm probes re-run at head"),
    ("receipts/r651/round1/", "round 2: the same probes at the round-1 head 85373de0"),
    ("receipts/iface/", "round 2: parameter and port declarations, comments stripped, at four revisions"),
    ("receipts/rom/", "round 2: ROM packing for the three images at head and base"),
    ("receipts/synth/", "round 2: synthesis-proxy statistics of the engine at base and head"),
    ("receipts/scripts/", "round 2: the scratch scripts these receipts were produced with"),
]
SCRATCH = [
    ("<scratch>/r2/synth/base/synth.log", 750086, "372e75c5133a18a2f458524a922c8fcf79d6cfa8da0eb63a5af8f4767fc3a6a1"),
    ("<scratch>/r2/synth/head-final/synth.log", 744897, "e4350b25f2af02a58bd57ed300df3b3bc63ffc623e3bc02546f8043a2e07e25c"),
    ("<scratch>/r2/synth/varb/synth.log", 744567, "fd64e5dded731fe622838f0e721f1d4dce3de0d9726cfc737092f9e99c121104"),
]
files = sorted(p for p in root.rglob("*") if p.is_file() and p.name != "RECEIPTS.md")
rows = []
for p in files:
    rel = p.relative_to(root).as_posix()
    data = p.read_bytes()
    assert len(data) < 200 * 1024, rel
    desc = next(d for g, d in GROUPS if rel == g or rel.startswith(g))
    rows.append((rel, len(data), hashlib.sha256(data).hexdigest(), desc))
out = ["# Receipts index, rounds 2 to 4", "",
       "Generated from the files present by `receipts/r4/scripts/make_index.py`.",
       "The table under the next heading lists every file under this directory except",
       "this index, with its size in bytes and sha256.",
       "`receipts/r4/scripts/verify_receipts.py <this directory>` checks that table, and only",
       "that table, against the directory: the same set of files, each size and digest.",
       "Round-3 and round-4 copies replace host path prefixes with placeholders such as `<scratch>`.", "",
       IN_DIR, "",
       "| file | bytes | sha256 | what it is |", "|---|---:|---|---|"]
out += [f"| `{r}` | {n} | `{h}` | {d} |" for r, n, h, d in rows]
out += ["", SCRATCH_HDR, "",
        "Not in this directory, so not part of the verified set.", "",
        "| scratch file | bytes | sha256 | what it is |", "|---|---:|---|---|"]
out += [f"| `{r}` | {n} | `{h}` | full synthesis log behind `receipts/synth/` |" for r, n, h in SCRATCH]
(root / "RECEIPTS.md").write_text("\n".join(out) + "\n")
print(f"indexed {len(rows)} files")
