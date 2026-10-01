#!/usr/bin/env python3
"""Redact the lane B4 packet's evidence and index the raw files (offline, no
bench access). Lane B3's package.py, steps 3 and 4 only.

usage: redact.py <packet_dir> <raw_root> <private_map_json>

Every text file in the packet's evidence directories (identity, restore, soc,
gates, summary, runs) is redacted with the private map: bench host names, interface
names, the controller's, the reference peer's and the grandmaster's
identifiers, the bridge network's addresses, console serials, home paths and
the account name become role labels. The original of each changed file is kept
under <raw_root>/packet-originals/. redaction.json lists, per file, the
original and retained SHA-256 and the labels used; it never lists the private
values. RAW-ARTIFACTS.json lists every file under <raw_root> by relative path,
size and SHA-256. A residual scan over the evidence and tools directories
reports any private token left.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

P, RAW, MAP = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
m = json.loads(MAP.read_text())
LIT = [(re.compile(re.escape(a), re.IGNORECASE), b) for a, b in m["literal"]]
RX = [(re.compile(a), b) for a, b in m["regex"]]
DIRS = ("identity", "restore", "soc", "gates", "summary", "runs")


def sha(b):
    return hashlib.sha256(b).hexdigest()


orig_root = RAW / "packet-originals"
records = []
for d in DIRS:
    for f in sorted((P / d).rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(P).as_posix()
        o = orig_root / rel
        data = o.read_bytes() if o.exists() else f.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("latin-1")
        new, labels = text, set()
        for r, b in LIT + RX:
            new, k = r.subn(b, new)
            if k:
                labels.add(b)
        if new != text:
            o.parent.mkdir(parents=True, exist_ok=True)
            if not o.exists():
                o.write_bytes(data)
            f.write_bytes(new.encode("utf-8"))
            records.append(dict(file=rel, original_sha256=sha(data), retained_sha256=sha(new.encode("utf-8")),
                                labels=sorted(labels)))
left = []
for d in DIRS + ("tools",):
    for f in sorted((P / d).rglob("*")):
        if f.is_file():
            t = f.read_bytes().decode("utf-8", "replace").lower()
            for c in m["check"]:
                if c.lower() in t:
                    left.append(f.relative_to(P).as_posix())
                    break
for name in ("HANDOFF.md", "PR-BODY.md", "TAKEN.md", "STOP.md", "REVIEW-READY.md"):
    f = P / name
    if f.is_file():
        t = f.read_text().lower()
        if any(c.lower() in t for c in m["check"]):
            left.append(name)
(P / "redaction.json").write_text(json.dumps(dict(
    rule=("Bench host names, interface names, the controller's, the reference peer's and the grandmaster's "
          "identifiers, the bridge network's addresses, console serials, home paths and the account name are "
          "replaced by the role labels listed per file. The DUT's entity, MAC and stream identifiers are public "
          "and retained. Each original stays under the raw root in packet-originals/, identified by its SHA-256."),
    files=records, residual_check_hits=len(left)), indent=1) + "\n")
idx = []
for f in sorted(RAW.rglob("*")):
    if f.is_file():
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        idx.append(dict(path=f.relative_to(RAW).as_posix(), bytes=f.stat().st_size, sha256=h.hexdigest()))
(P / "RAW-ARTIFACTS.json").write_text(json.dumps(dict(
    raw_root="/tmp/b4-a468/raw on the bench host (not published)", files=len(idx),
    total_bytes=sum(x["bytes"] for x in idx), entries=idx), indent=1) + "\n")
print(json.dumps(dict(redacted_files=len(records), residual_check_hits=left, raw_files=len(idx),
                      raw_bytes=sum(x["bytes"] for x in idx))))
