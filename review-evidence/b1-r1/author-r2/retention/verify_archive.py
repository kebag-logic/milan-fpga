#!/usr/bin/env python3
"""Verify the durable raw copy of lane B1 and write its retention MANIFEST.

usage: verify_archive.py <archived-raw-root> <repo-at-head> <manifest-out.tsv>

Checks, for the lane's 213 raw files:
  1. every entry of the round-1 raw index (r1/RAW-ARTIFACTS.json: relative
     path, bytes, SHA-256) has an archived copy with the same size and hash,
     and the archive holds no file the index does not list;
  2. every raw-artifact row of both findings pages (action, file, bytes,
     SHA-256) equals the archived copy of <action>/<file>, and every archived
     console, controller transcript, tap capture, controller-port capture,
     event record and port log of those actions has a page row;
  3. every per-action index r1/bench/<action>/raw-artifacts.json agrees with
     the archived copy of the same file.

The MANIFEST has one row per archived file: path, bytes, SHA-256 and the page
row (page:line) it matches, or "-" for files the pages do not list. It
names no storage host.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "extract"))
from b1r2_common import PACKET, page_rows, raw_index, sha256  # noqa: E402

PAGE_KINDS = ("console.jsonl", "controller.jsonl", "tap.pcap", "controller-wire.pcap", "events.jsonl",
              "ptp4l-gm.log", "ptp4l-slave.log")


def main():
    root, repo, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    index, rows = raw_index(), page_rows(repo)
    ok = bad = 0

    def res(cond, msg):
        nonlocal ok, bad
        ok += cond
        bad += not cond
        if not cond:
            print("FAIL " + msg)

    archived = {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}
    have = {}
    for rel, p in sorted(archived.items()):
        have[rel] = (p.stat().st_size, sha256(p))
    # 1. index <-> archive
    for rel, (size, digest) in sorted(index.items()):
        res(have.get(rel) == (size, digest), f"index entry {rel} has no identical archived copy")
    for rel in sorted(set(have) - set(index)):
        res(False, f"archived file {rel} is not in the index")
    print(f"1. raw index: {len(index)} entries, archive {len(have)} files, identical {sum(1 for r in index if have.get(r) == index[r])}")
    # 2. page rows <-> archive
    matched = 0
    for rel, (page, line, size, digest) in sorted(rows.items()):
        cond = have.get(rel) == (size, digest)
        matched += cond
        res(cond, f"page row {page}:{line} {rel} differs from the archived copy")
    actions = sorted({r.split("/")[0] for r in rows})
    unlisted = [r for r in have if r.split("/")[0] in actions and r.split("/")[-1] in PAGE_KINDS
                and have[r][0] > 0 and r not in rows]
    res(not unlisted, f"archived page-kind files without a page row: {unlisted}")
    print(f"2. page rows: {len(rows)} rows over {len(actions)} actions, {matched} equal to their archived copy; "
          f"page-kind files without a row: {len(unlisted)}")
    # 3. per-action indexes
    n3 = 0
    for idx in sorted((PACKET / "r1" / "bench").glob("*/raw-artifacts.json")):
        action = idx.parent.name
        for e in json.loads(idx.read_text()):
            rel = f"{action}/{Path(e['path']).name}"
            res(have.get(rel) == (e["size"], e["sha256"]), f"per-action index {rel} differs from the archive")
            n3 += 1
    print(f"3. per-action indexes: {n3} entries checked against the archive")
    lines = ["path\tbytes\tsha256\tpage_row"]
    for rel, (size, digest) in sorted(have.items()):
        row = rows.get(rel)
        lines.append(f"{rel}\t{size}\t{digest}\t{row[0] + ':' + str(row[1]) if row else '-'}")
    out.write_text("\n".join(lines) + "\n")
    total = sum(s for s, _ in have.values())
    print(f"MANIFEST {out.name}: {len(have)} files, {total} bytes")
    print(f"TOTAL pass={ok} fail={bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
