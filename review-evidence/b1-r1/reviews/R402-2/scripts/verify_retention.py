#!/usr/bin/env python3
"""Check the round-2 raw-retention statements of the two B1 findings pages.

1. Every raw-artifact row of both pages at the reviewed head has a retained
   copy with the row's size and SHA-256.
2. The retained file set equals the packet's raw index r1/RAW-ARTIFACTS.json,
   entry for entry, and every retained file hashes as its index entry.
3. The storage manifest verifies (sha256 of every listed file) and is
   byte-identical to the packet's retention/MANIFEST.sha256; the TSV likewise.
4. Every per-action r1/bench/<action>/raw-artifacts.json entry matches the
   retained copy of the same action and file name.

Prints relative names only; the storage location is an argument, not output.

usage: verify_retention.py <storage-dir containing raw/ and manifests> <repo-at-head> <author-r2-packet-dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PAGES = ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md")
ROLE = {"alignment port log": "ptp4l-slave.log", "grandmaster port log": "ptp4l-gm.log"}
FAILS = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAILS.append(label)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    store, repo, packet = map(Path, sys.argv[1:4])
    raw = store / "raw"
    files = {str(p.relative_to(raw)): (p.stat().st_size, sha(p)) for p in raw.rglob("*") if p.is_file()}
    print(f"retained files: {len(files)}, {sum(s for s, _ in files.values())} bytes")

    rows = []
    for page in PAGES:
        text = (repo / page).read_text()
        for m in re.finditer(r"^\| ([\w-]+) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|$", text, re.M):
            line = text.count("\n", 0, m.start()) + 1
            rows.append((f"{Path(page).name}:{line}", f"{m.group(1)}/{ROLE.get(m.group(2), m.group(2).strip('`'))}",
                         int(m.group(3)), m.group(4)))
    bad = [r for r in rows if files.get(r[1]) != (r[2], r[3])]
    for r in bad:
        print("  row mismatch", r[0], r[1])
    check(len(rows) == 100 and not bad, f"1. {len(rows)} page raw-artifact rows, {len(rows) - len(bad)} equal to their retained copy")

    idx = json.loads((packet / "r1" / "RAW-ARTIFACTS.json").read_text())
    index = {f["path"]: (f["bytes"], f["sha256"]) for f in idx["files"]}
    check(index == files and idx["count"] == len(files) and idx["total_bytes"] == sum(s for s, _ in files.values()),
          f"2. retained set equals the packet raw index ({len(index)} entries, count and total bytes agree)")

    man = (store / "MANIFEST.sha256").read_text().splitlines()
    ok = 0
    for line in man:
        d, rel = line.split(None, 1)
        p = store / rel.strip()
        ok += p.is_file() and sha(p) == d
    check(ok == len(man) == len(files), f"3a. storage MANIFEST.sha256 verifies {ok}/{len(man)}")
    pk = packet / "retention"
    check((pk / "MANIFEST.sha256").read_bytes() == (store / "MANIFEST.sha256").read_bytes()
          and (pk / "MANIFEST.tsv").read_bytes() == (store / "MANIFEST.tsv").read_bytes(),
          "3b. packet retention MANIFEST.sha256 and MANIFEST.tsv are byte-identical to the storage copies")
    tsv = [x.split("\t") for x in (pk / "MANIFEST.tsv").read_text().splitlines()[1:]]
    tsv_rows = {r[3]: r[0] for r in tsv if r[3] != "-"}
    page_rows = {r[0]: r[1] for r in rows}
    check(tsv_rows == page_rows, f"3c. the TSV's page-row column names exactly the {len(page_rows)} page rows, each against its file")

    n = mism = 0
    for f in sorted((packet / "r1" / "bench").glob("*/raw-artifacts.json")):
        action = f.parent.name
        for e in json.loads(f.read_text()):
            n += 1
            rel = f"{action}/{Path(e['path']).name}"
            if files.get(rel) != (e["size"], e["sha256"]):
                mism += 1
                print("  per-action mismatch", rel)
    check(n > 0 and mism == 0, f"4. {n} per-action raw-artifacts.json entries equal their retained copy")
    print(f"\nTOTAL fail={len(FAILS)}")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
