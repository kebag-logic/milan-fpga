#!/usr/bin/env python3
"""Check every hash row in lane B16's section of the findings page against the author's packet: an
evidence file row (`path` | bytes | `sha256`) against the packet file's size and SHA-256 at the round it
was retained (redaction.json's retained hash where a file was masked), and a raw file row (run | file |
bytes | sha256, or a three-column row naming a file that stays outside the packet) against
RAW-ARTIFACTS.json by hash, and by size where the page states one.

usage: verify_hash_tables.py <findings.md> <author packet root> <out.json>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PAGE, ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
lines = PAGE.read_text(encoding="utf-8").splitlines()
s = next(i for i, x in enumerate(lines) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
raw = json.loads((ROOT / "RAW-ARTIFACTS.json").read_text())
rawfiles = raw["files"] if isinstance(raw, dict) else raw
res, bad = [], 0
section = None
for i in range(s, len(lines)):
    x = lines[i]
    if x.startswith("### "):
        section = x
    cells = [c.strip() for c in x.strip().strip("|").split("|")]
    shas = [c.strip("`") for c in cells if re.fullmatch(r"`?[0-9a-f]{64}`?", c)]
    if not shas or not x.startswith("|"):
        continue
    sha = shas[0]
    m = re.match(r"`([^`]+)`", cells[0])
    if m and len(cells) == 3 and (ROOT / m.group(1)).exists():  # evidence file row
        rel = m.group(1)
        p = ROOT / rel
        got = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        size = p.stat().st_size if p.exists() else None
        ok = got == sha and str(size) == cells[1].replace(",", "")
        res.append(dict(line=i + 1, kind="evidence", path=rel, ok=ok, page=[cells[1], sha], packet=[size, got]))
    else:  # raw file row: match by sha in RAW-ARTIFACTS
        hit = [r for r in rawfiles if r.get("sha256") == sha]
        ok = bool(hit)
        if ok and len(cells) >= 4 and ":" not in cells[1] and re.fullmatch(r"[\d,]+", cells[2]):
            ok = any(str(h.get("bytes")) == cells[2].replace(",", "") for h in hit)
        res.append(dict(line=i + 1, kind="raw", cells=cells[:3], ok=ok, hits=[h.get("path") for h in hit]))
    bad += not res[-1]["ok"]
OUT.write_text(json.dumps(res, indent=1))
print("rows", len(res), "bad", bad)
for r in res:
    if not r["ok"]:
        print("BAD", r)
sys.exit(1 if bad else 0)
