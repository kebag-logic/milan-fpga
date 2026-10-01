#!/usr/bin/env python3
"""Redact private identifiers from the lane packet's text files (lane B5).

usage: redact.py <packet_dir> <map.json> <originals_dir>

The map (private, not in the packet) lists literal and regex substitutions to
labels. Each changed file's original is saved under <originals_dir> by relative
path, and <packet_dir>/redaction.json records per file the original and retained
SHA-256 and the labels used. The peer's ENTITY descriptor payloads are replaced
whole, because they carry its name and serial fields. Tools, MANIFEST.sha256 and
redaction.json itself are not rewritten.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

pkt, mp, orig = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
SKIP = {"MANIFEST.sha256", "redaction.json"}
ENTITY_DESC = re.compile(r'("payload":")0000[0-9a-f]{4}00000000[0-9a-f]{600,}(")')  # cfg, reserved (any), ENTITY 0
rec = {}
for f in sorted(pkt.rglob("*")):
    rel = f.relative_to(pkt).as_posix()
    if not f.is_file() or rel in SKIP or rel.startswith("tools/"):
        continue
    raw = f.read_bytes()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("latin-1")
    new, used = txt, set()
    if "peer-descs" in rel or "census" in rel:
        n2 = ENTITY_DESC.sub(r"\1<peer-entity-descriptor-redacted>\2", new)
        if n2 != new:
            used.add("<peer-entity-descriptor-redacted>")
            new = n2
    for a, b in mp["literal"]:
        if a in new:
            new = new.replace(a, b)
            used.add(b)
    for a, b in mp["regex"]:
        n2 = re.sub(a, b, new)
        if n2 != new:
            used.add(b)
            new = n2
    if new != txt:
        dst = orig / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        f.write_bytes(new.encode("utf-8"))
        rec[rel] = dict(original_sha256=hashlib.sha256(raw).hexdigest(),
                        retained_sha256=hashlib.sha256(new.encode("utf-8")).hexdigest(), labels=sorted(used))
json.dump(dict(rule="literal and regex substitutions from a private map; originals kept outside the packet",
               files=rec), open(pkt / "redaction.json", "w"), indent=1)
print(f"{len(rec)} files redacted")
