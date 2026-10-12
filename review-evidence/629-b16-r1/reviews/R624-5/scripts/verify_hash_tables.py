#!/usr/bin/env python3
"""R624-5: every `path` | bytes | sha256 row in lane B16's section and in the PR body against the published
packet (author-rN) and its RAW-ARTIFACTS.json.

usage: verify_hash_tables.py <findings.md> <pr_body.md> <author packet> <out.json>
"""
import hashlib, json, re, sys
from pathlib import Path

page, body, pk, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
lines = page.read_text().splitlines()
s = next(i for i, x in enumerate(lines) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
sect = [(i + 1, x) for i, x in enumerate(lines[s:], s)]
raw = {}
for x in json.loads((pk / "RAW-ARTIFACTS.json").read_text())["files"]:
    raw.setdefault(x["path"].rsplit("/", 1)[-1], []).append(x)
ROW = re.compile(r"^\|(?:\s*`?([\w,` -]+?)`?\s*\|)?\s*`([^`]+)`[^|]*\|\s*([\d,]+|Withheld|0)?\s*\|?\s*`([0-9a-f]{64})`\s*\|$")
res = {"page_packet_rows": 0, "page_raw_rows": 0, "body_rows": 0, "problems": [], "raw_unmatched": []}


def check(where, ln, path, size, h, run=None):
    f = pk / path
    if f.is_file():
        b = f.read_bytes()
        ok = hashlib.sha256(b).hexdigest() == h and (size in (None, "Withheld") or int(size.replace(",", "")) == len(b))
        if not ok:
            res["problems"].append([where, ln, path, "packet file differs"])
        return "packet"
    cands = raw.get(path.rsplit("/", 1)[-1], [])
    hit = [x for x in cands if x.get("sha256") == h]
    if hit:
        x = hit[0]
        if size not in (None, "Withheld") and "bytes" in x and int(size.replace(",", "")) != x["bytes"]:
            res["problems"].append([where, ln, path, "raw size differs"])
        return "raw"
    res["raw_unmatched"].append([where, ln, path, h[:12]])
    return None


header = []
for ln, x in sect:
    m = re.match(r"^\|(.*)\|$", x)
    if not m:
        header = []
        continue
    cells = [c.strip() for c in m.group(1).split("|")]
    if not header:
        header = cells  # the table's header row: the size is read only from a "Bytes" column
        continue
    if not re.search(r"`[0-9a-f]{64}`", x):
        continue
    h = re.search(r"`([0-9a-f]{64})`", cells[-1]).group(1)
    size = cells[header.index("Bytes")] if "Bytes" in header else None
    pm = re.search(r"`([^`]+\.[\w]+)`", " | ".join(cells[:-2]) if size else " | ".join(cells[:-1]))
    if not pm:
        continue
    kind = check("page", ln, pm.group(1), size, h)
    res["page_packet_rows" if kind == "packet" else "page_raw_rows"] += 1 if kind else 0
for ln, x in enumerate(body.read_text().splitlines(), 1):
    m = re.match(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$", x)
    if m:
        res["body_rows"] += 1
        check("body", ln, m.group(1), m.group(2), m.group(3))
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1)[:3000])
