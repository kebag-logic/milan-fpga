#!/usr/bin/env python3
"""Redact private identifiers from the lane packet's files (lane B5's redact.py, lane B7 changes).

usage: redact_b7.py <packet_dir> <map.json> <originals_dir>

The map (private, not in the packet) lists literal and regex substitutions to labels, and
`payload_strings`: any JSON `payload` field whose bytes contain one of them (the reference
peer's descriptor names, serial and firmware fields) is replaced whole. Each changed file's
original is saved under <originals_dir> by relative path (the first original is kept when a
pass repeats), and <packet_dir>/redaction.json records per file the original and retained
SHA-256 and the labels used.

Lane B7 changes against lane B5's redact.py:
  * tools are redacted too (the capture's channel layout appears in them), so a redacted tool
    is a record of the tool as run, not a runnable copy; its original is kept privately and
    both hashes are recorded;
  * descriptor payloads are matched by content (`payload_strings`), not only the ENTITY
    descriptor's shape;
  * summary/*/grade.json: the capture's per-channel identification table is replaced by
    the decoded count of the tone pair, which is what the grade uses.
MANIFEST.sha256, redaction.json and this file are not rewritten.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

pkt, mp, orig = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
SKIP = {"MANIFEST.sha256", "redaction.json", "tools/redact_b7.py"}
PAYLOAD = re.compile(r'("payload":\s*")([0-9a-f]+)(")')
pstr = [s.encode() for s in mp.get("payload_strings", [])]
# a repeated pass keeps the first original of every file and merges the record
prev = pkt / "redaction.json"
rec = json.load(open(prev))["files"] if prev.exists() else {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


for f in sorted(pkt.rglob("*")):
    rel = f.relative_to(pkt).as_posix()
    if not f.is_file() or rel in SKIP:
        continue
    raw = f.read_bytes()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        continue
    new, used = txt, set()
    if rel.startswith("summary/") and rel.endswith("/grade.json"):
        g = json.loads(new)
        ci = g.get("channel_identification")
        if isinstance(ci, dict) and isinstance(ci.get("channels"), list):
            dec = next((v for k, v in ci.items() if k.startswith("pair_")), None)
            g["channel_identification"] = dict(tone_pair_decoded=dec, frames=ci.get("frames"),
                                               channels="<capture-channel-table-redacted>")
            new = json.dumps(g, indent=1, default=float)
            used.add("<capture-channel-table-redacted>")

    def sub_payload(m):
        b = bytes.fromhex(m.group(2)) if len(m.group(2)) % 2 == 0 else b""
        if any(s in b for s in pstr):
            used.add("<peer-descriptor-redacted>")
            return m.group(1) + "<peer-descriptor-redacted>" + m.group(3)
        return m.group(0)

    new = PAYLOAD.sub(sub_payload, new)
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
        if not dst.exists():
            shutil.copy2(f, dst)
        f.write_text(new)
        first = dst.read_bytes()
        labels = sorted(used | set(rec.get(rel, {}).get("labels", [])))
        rec[rel] = dict(original_sha256=sha(first), retained_sha256=sha(new.encode()), labels=labels)
json.dump(dict(rule="every packet file but MANIFEST.sha256, redaction.json and tools/redact_b7.py; "
                    "map and originals private", files=rec),
          open(pkt / "redaction.json", "w"), indent=1, sort_keys=True)
print(json.dumps(dict(files_changed=len(rec))))
